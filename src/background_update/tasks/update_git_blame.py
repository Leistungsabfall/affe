import re
import subprocess
from datetime import datetime

from globals import Globals
from util.git_helper import file_is_untracked, GIT_UNCOMMITTED_TEXT


def run():
    def get_blame_info():
        p = subprocess.Popen(
            'git blame --line-porcelain {}'.format(Globals.relative_file_path_from_git_dir),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Globals.git_dir,
        )
        output = p.communicate()[0].decode('utf-8').strip()
        return output

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
                author_time_str = datetime.utcfromtimestamp(int(author_timestamp)).strftime('%Y-%m-%d')
                text = commit_hash + ' ' \
                    + author_time_str + ' ' \
                    + author + ': ' \
                    + commit_message
            git_blame_by_line.append(text)
        return git_blame_by_line

    if file_is_untracked():
        return

    if not Globals.git_blame_active:
        Globals.git_blame_by_line = []
        return

    git_blame_output = get_blame_info()

    if not git_blame_output:
        return

    try:
        Globals.git_blame_by_line = parse_blame_output()
    except Exception:
        return
