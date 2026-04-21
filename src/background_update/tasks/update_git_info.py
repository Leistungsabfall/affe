import os
import subprocess
import tempfile

from prompt_toolkit import HTML

from globals import Globals
from util.git_helper import file_is_untracked


def run():
    def is_dirty():
        p = subprocess.Popen(
            'git --no-optional-locks status --porcelain {}'.format(Globals.relative_file_path_from_git_dir),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Globals.git_dir,
        )
        output = p.communicate()[0].decode('utf-8').strip()
        return bool(output)

    def get_branch():
        p = subprocess.Popen(
            'git rev-parse --abbrev-ref HEAD',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Globals.git_dir,
        )
        output = p.communicate()[0].decode('utf-8').strip()
        if output == "HEAD":
            return 'detached*'
        return output

    def get_git_dir_for_file(path):
        while path != '/':
            path = os.path.dirname(path)
            try:
                if '.git' in os.listdir(path):
                    return path
            except (FileNotFoundError, PermissionError):
                pass
        return ''

    def get_relative_file_path_from_git_dir(path):
        # /home/git_dir/foo/bla.txt => foo/bla.txt
        return path.split(Globals.git_dir + '/', maxsplit=1)[-1]

    def write_file_from_git():
        p = subprocess.Popen(
            'git cat-file -p :%s > %s' % (Globals.relative_file_path_from_git_dir, git_file.name),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Globals.git_dir,
        )
        p.communicate()
        return p.returncode == 0

    def write_file_from_current_text():
        current_file.write(Globals.text_field.text)
        current_file.flush()

    def get_diff():
        p = subprocess.Popen(
            'diff %s %s --unified=0 \n' % (git_file.name, current_file.name),
            universal_newlines=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            output = str(p.communicate()[0]).strip().split('\n')
        except UnicodeDecodeError:
            return []
        if p.returncode == 1:  # from "diff --help": 0 means no diff, 1 means diff, 2 means problems
            return output
        return []

    def plus_in_rest_of_chunk():
        return any(line.startswith('+') for line in chunk[line_index+1:])

    def minus_in_preceding_part_of_chunk():
        return any(line.startswith('-') for line in reversed(chunk[:line_index]))

    def get_chunk():
        chunk_until_diff_end = git_diff[git_diff_index+1:]
        for index, line in enumerate(chunk_until_diff_end):
            if index > 0 and line.startswith('@@'):
                return chunk_until_diff_end[:index]
        return chunk_until_diff_end

    try:
        file_path = os.path.realpath(Globals.file_path)
    except FileNotFoundError:
        Globals.git_status_by_line = dict()
        return
    Globals.git_dir = get_git_dir_for_file(file_path)
    Globals.relative_file_path_from_git_dir = get_relative_file_path_from_git_dir(file_path)

    if not Globals.git_dir:
        Globals.git_status_by_line = dict()
        return

    Globals.git_dirty_indicator = is_dirty()
    Globals.git_branch = get_branch()
    Globals.git_untracked = file_is_untracked()

    with tempfile.NamedTemporaryFile('w') as git_file, tempfile.NamedTemporaryFile('w') as current_file:
        git_status_by_line = dict()

        if not write_file_from_git():
            Globals.git_status_by_line = dict()
            return

        write_file_from_current_text()
        git_diff = get_diff()

        for git_diff_index, line in enumerate(git_diff):
            if not line.startswith('@@'):
                continue

            # -1 because normal diff indices are +1 off, except if first line is deleted, then diff index is correct
            chunk_index_in_current_text = max(0, int(line.split('+')[-1].split(' @@')[0].split(',')[0]) - 1)
            chunk = get_chunk()
            counter = 0
            for line_index, chunk_line in enumerate(chunk):
                if chunk_line.startswith('-') and not plus_in_rest_of_chunk():
                    git_status_by_line[chunk_index_in_current_text+counter] = HTML('<git-deleted>▂</git-deleted> ')
                elif chunk_line.startswith('+'):
                    if minus_in_preceding_part_of_chunk():
                        git_status_by_line[chunk_index_in_current_text+counter] = HTML('<git-modified>█</git-modified> ')
                    else:
                        git_status_by_line[chunk_index_in_current_text+counter] = HTML('<git-added>█</git-added> ')
                    counter += 1
                else:
                    pass  # could end up here, e.g. diff may print "no newline at end of file"

        Globals.git_status_by_line = git_status_by_line
