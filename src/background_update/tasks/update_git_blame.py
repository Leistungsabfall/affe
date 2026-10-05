import os
import re
from datetime import datetime, timezone

from globals import Globals
from util.git_helper import file_is_untracked, get_git_state_fingerprint, run_git, GitStateCache, \
    GIT_UNCOMMITTED_TEXT


git_state_cache = GitStateCache()


def run():
    def get_blame_info():
        _, output = run_git('blame', '--line-porcelain', '--', Globals.relative_file_path_from_git_dir)
        return output.decode('utf-8').strip()

    def parse_blame_output():
        git_blame_by_line = []
        for chunk in re.split(r'\n\t[^\n]*\n', git_blame_output):
            commit_hash = chunk[:7]
            if commit_hash == '0000000':
                text = GIT_UNCOMMITTED_TEXT
            else:
                author = re.search(r'author (?P<author>[^\n]*)\n', chunk).groupdict()['author']
                commit_message = re.search(r'summary (?P<msg>[^\n]*)\n', chunk).groupdict()['msg']
                author_timestamp = re.search(r'author-time (?P<time>[^\n]*)\n', chunk).groupdict()['time']
                author_time_str = datetime.fromtimestamp(int(author_timestamp), timezone.utc).strftime('%Y-%m-%d')
                text = commit_hash + ' ' \
                    + author_time_str + ' ' \
                    + author + ': ' \
                    + commit_message
            git_blame_by_line.append(text)
        return git_blame_by_line

    def get_cache_key():
        if not Globals.git_dir:
            return Globals.git_blame_active, Globals.file_path
        try:
            file_path = os.path.realpath(Globals.file_path)
        except OSError:
            return Globals.git_blame_active, Globals.file_path
        return Globals.git_blame_active, get_git_state_fingerprint(file_path, Globals.git_dir)

    # git blame only depends on the file on disk and the git state, not on the unsaved text
    cache_key = get_cache_key()
    if not git_state_cache.is_refresh_needed(cache_key):
        return

    if file_is_untracked():
        git_state_cache.mark_refreshed(cache_key)
        return

    if not Globals.git_blame_active:
        Globals.git_blame_by_line = []
        git_state_cache.mark_refreshed(cache_key)
        return

    git_blame_output = get_blame_info()

    if not git_blame_output:
        return

    try:
        Globals.git_blame_by_line = parse_blame_output()
    except Exception:
        return
    git_state_cache.mark_refreshed(cache_key)
