import os
import shutil
import subprocess
import time

from globals import Globals


GIT_ERROR_TEXT = 'This file does not seem to be tracked by git.'
GIT_UNCOMMITTED_TEXT = 'not committed yet'
COMMAND_NOT_FOUND_RETURN_CODE = 127

# Even if no watched git state changed, refresh after this interval to pick up
# changes to state which is not watched (e.g. a global excludes file).
FULL_REFRESH_INTERVAL_SECONDS = 10


def run_command(args, cwd=None, stdout=subprocess.PIPE, text=False):
    """
    Run a command without a shell and return (return code, stdout).
    File paths are passed as separate arguments, so they don't need quoting.
    """
    try:
        p = subprocess.Popen(
            args,
            stdout=stdout,
            stderr=subprocess.DEVNULL,
            cwd=cwd,
            universal_newlines=text,
        )
    except OSError:
        return COMMAND_NOT_FOUND_RETURN_CODE, '' if text else b''
    output = p.communicate()[0]
    return p.returncode, output


def run_git(*args, stdout=subprocess.PIPE):
    return run_command(['git', *args], cwd=Globals.git_dir, stdout=stdout)


def file_is_untracked():
    if not Globals.git_dir:
        return True

    if not os.path.exists(Globals.file_path):
        return True

    if Globals.file_path.endswith('COMMIT_EDITMSG'):
        return True

    if shutil.which('git') is None:
        return True

    returncode, _ = run_git('check-ignore', '--', Globals.relative_file_path_from_git_dir)
    if returncode == 0:
        return True

    _, output = run_git(
        '--no-optional-locks', '--literal-pathspecs', 'status', '--porcelain', '--',
        Globals.relative_file_path_from_git_dir,
    )
    return output.decode('utf-8').strip().startswith('?? ')


def _get_stat_signature(path):
    try:
        st = os.stat(path)
    except OSError:
        return None
    return st.st_mtime_ns, st.st_ctime_ns, st.st_size, st.st_ino


def _read_text(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except (OSError, UnicodeDecodeError):
        return None


def _read_index_checksum(path):
    # the git index ends with a checksum over its whole content
    try:
        with open(path, 'rb') as f:
            f.seek(-20, os.SEEK_END)
            return f.read()
    except OSError:
        return None


def _get_git_metadata_dirs(git_dir):
    """
    Return (git dir, common git dir). Both differ from '<git_dir>/.git' for
    worktrees and submodules, where '.git' is a file pointing elsewhere.
    """
    dot_git = os.path.join(git_dir, '.git')
    metadata_dir = dot_git
    if not os.path.isdir(dot_git):
        content = _read_text(dot_git) or ''
        if content.startswith('gitdir:'):
            metadata_dir = os.path.join(git_dir, content[len('gitdir:'):].strip())
    common_dir = metadata_dir
    common_dir_content = _read_text(os.path.join(metadata_dir, 'commondir'))
    if common_dir_content:
        common_dir = os.path.join(metadata_dir, common_dir_content)
    return metadata_dir, common_dir


def get_git_state_fingerprint(file_path, git_dir):
    """
    Cheap fingerprint (no subprocesses) of everything on disk the git
    related background tasks depend on. If it is unchanged, git output for
    the file is expected to be unchanged as well.
    """
    metadata_dir, common_dir = _get_git_metadata_dirs(git_dir)
    head = _read_text(os.path.join(metadata_dir, 'HEAD'))
    head_ref = None
    if head and head.startswith('ref:'):
        head_ref = _read_text(os.path.join(common_dir, head[len('ref:'):].strip()))
    index_checksum = _read_index_checksum(os.path.join(metadata_dir, 'index'))
    paths = [
        file_path,
        os.path.join(metadata_dir, 'index'),
        os.path.join(metadata_dir, 'logs', 'HEAD'),
        os.path.join(common_dir, 'packed-refs'),
        os.path.join(common_dir, 'config'),
        os.path.join(common_dir, 'info', 'exclude'),
        os.path.join(git_dir, '.mailmap'),
    ]

    directory = os.path.dirname(file_path)
    while True:
        paths.append(os.path.join(directory, '.gitignore'))
        if directory == git_dir or os.path.dirname(directory) == directory:
            break
        directory = os.path.dirname(directory)

    return (file_path, git_dir, head, head_ref, index_checksum) + tuple(_get_stat_signature(path) for path in paths)


class GitStateCache:
    """
    Remembers the git state fingerprint of the last refresh, so expensive git
    calls can be skipped while nothing relevant changed.
    """
    def __init__(self):
        self.key = None
        self.last_refresh = None

    def is_refresh_needed(self, key):
        return (
            key != self.key
            or self.last_refresh is None
            or time.monotonic() - self.last_refresh >= FULL_REFRESH_INTERVAL_SECONDS
        )

    def mark_refreshed(self, key):
        self.key = key
        self.last_refresh = time.monotonic()

    def reset(self):
        self.key = None
        self.last_refresh = None
