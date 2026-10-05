import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import os
import shutil
import subprocess
import tempfile
import unittest

from globals import Globals
from test.testutils import init_text_field

from background_update.tasks import update_git_blame, update_git_info
from util.git_helper import COMMAND_NOT_FOUND_RETURN_CODE, file_is_untracked, run_command


GIT_GLOBALS = (
    'file_path', 'git_dir', 'relative_file_path_from_git_dir', 'git_status_by_line', 'git_branch',
    'git_dirty_indicator', 'git_untracked', 'git_blame_active', 'git_blame_by_line', 'text_field',
)


@unittest.skipIf(shutil.which('git') is None or shutil.which('diff') is None, 'git and diff are required')
class TestGit(unittest.TestCase):
    def setUp(self):
        self.saved_globals = {name: getattr(Globals, name) for name in GIT_GLOBALS}
        self.repo_dir = os.path.realpath(tempfile.mkdtemp())
        self.git('init', '-q')
        self.git('symbolic-ref', 'HEAD', 'refs/heads/main')

    def tearDown(self):
        for name, value in self.saved_globals.items():
            setattr(Globals, name, value)
        shutil.rmtree(self.repo_dir)

    def git(self, *args):
        subprocess.run(
            ['git', '-c', 'user.name=Monkey', '-c', 'user.email=monkey@affe.sh', '-c', 'commit.gpgsign=false', *args],
            cwd=self.repo_dir,
            check=True,
            stdout=subprocess.DEVNULL,
        )

    def create_file(self, name, text):
        path = os.path.join(self.repo_dir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(text)
        return path

    def commit_file(self, name, text):
        path = self.create_file(name, text)
        self.git('add', '--', name)
        self.git('commit', '-q', '-m', 'add file')
        return path

    def open_file(self, path, text):
        Globals.file_path = path
        init_text_field(text, 0)

    def test_inline_diff_for_file_path_with_spaces(self):
        path = self.commit_file('dir with spaces/my file.txt', 'a\nb\nc\n')
        self.open_file(path, 'a\nB\nc\nd\n')

        update_git_info.run()

        self.assertEqual(Globals.git_dir, self.repo_dir)
        self.assertEqual(Globals.relative_file_path_from_git_dir, 'dir with spaces/my file.txt')
        self.assertEqual(Globals.git_branch, 'main')
        self.assertFalse(Globals.git_dirty_indicator)
        self.assertFalse(Globals.git_untracked)
        self.assertEqual(sorted(Globals.git_status_by_line), [1, 3])
        self.assertIn('git-modified', Globals.git_status_by_line[1].value)
        self.assertIn('git-added', Globals.git_status_by_line[3].value)

    def test_dirty_indicator(self):
        path = self.commit_file('file.txt', 'a\n')
        self.create_file('file.txt', 'b\n')
        self.open_file(path, 'b\n')

        update_git_info.run()

        self.assertTrue(Globals.git_dirty_indicator)

    def test_file_name_with_glob_characters_is_matched_literally(self):
        path = self.commit_file('file[1].txt', 'a\n')
        self.create_file('file1.txt', 'untracked\n')
        self.open_file(path, 'a\n')

        update_git_info.run()

        self.assertFalse(Globals.git_dirty_indicator)
        self.assertFalse(Globals.git_untracked)

    def test_untracked_file(self):
        self.commit_file('tracked.txt', 'a\n')
        path = self.create_file('untracked file.txt', 'a\n')
        self.open_file(path, 'a\n')

        update_git_info.run()

        self.assertTrue(file_is_untracked())
        self.assertEqual(Globals.git_status_by_line, dict())

    def test_detached_head(self):
        path = self.commit_file('file.txt', 'a\n')
        self.git('checkout', '-q', '--detach')
        self.open_file(path, 'a\n')

        update_git_info.run()

        self.assertEqual(Globals.git_branch, 'detached*')

    def test_git_blame_for_file_path_with_spaces(self):
        path = self.commit_file('my file.txt', 'a\nb\n')
        self.open_file(path, 'a\nb\n')
        update_git_info.run()
        Globals.git_blame_active = True

        update_git_blame.run()

        self.assertEqual(len(Globals.git_blame_by_line), 2)
        for text in Globals.git_blame_by_line:
            self.assertIn(' Monkey: add file', text)

    def test_run_command_missing_executable(self):
        self.assertEqual(run_command(['affe-command-that-does-not-exist']), (COMMAND_NOT_FOUND_RETURN_CODE, b''))
        self.assertEqual(run_command(['affe-command-that-does-not-exist'], text=True), (COMMAND_NOT_FOUND_RETURN_CODE, ''))
