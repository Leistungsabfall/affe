import os
import shutil
import subprocess

from globals import Globals


GIT_ERROR_TEXT = 'This file does not seem to be tracked by git.'
GIT_UNCOMMITTED_TEXT = 'not committed yet'
COMMAND_NOT_FOUND_RETURN_CODE = 127


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
