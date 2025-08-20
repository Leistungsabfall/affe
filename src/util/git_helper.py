import os
import shutil
import subprocess

from globals import Globals


GIT_ERROR_TEXT = 'This file does not seem to be tracked by git.'
GIT_UNCOMMITTED_TEXT = 'not committed yet'


def file_is_untracked():
    if not Globals.git_dir:
        return True

    if not os.path.exists(Globals.file_path):
        return True

    if Globals.file_path.endswith('COMMIT_EDITMSG'):
        return True

    if shutil.which('git') is None:
        return True

    p = subprocess.Popen(
        'git check-ignore {}'.format(Globals.relative_file_path_from_git_dir),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Globals.git_dir,
    )
    p.communicate()
    if p.returncode == 0:
        return True

    p = subprocess.Popen(
        'git --no-optional-locks status --porcelain {}'.format(Globals.relative_file_path_from_git_dir),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Globals.git_dir,
    )
    output = p.communicate()[0].decode('utf-8').strip()
    return output.startswith('?? ')
