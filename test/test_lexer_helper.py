import sys
sys.path.insert(0, 'python-prompt-toolkit')
sys.path.append('src')
sys.path.append('test')

import os
import unittest

from pygments.lexers.c_cpp import CLexer
from pygments.lexers.configs import IniLexer, SystemdLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.html import XmlLexer
from pygments.lexers.jvm import GroovyLexer
from pygments.lexers.make import MakefileLexer, CMakeLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.objective import ObjectiveCLexer
from pygments.lexers.perl import PerlLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.robotframework import RobotFrameworkLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from prompt_toolkit.lexers import SimpleLexer
from util import lexer_helper
from util.lexer_helper import guess_lexer_wrapper

from lexers.text_with_comment_lexer import TextWithCommentLexer


class TestLexerHelper(unittest.TestCase):
    def test_guess_lexer_by_file_content(self):
        lexer = guess_lexer_wrapper(
            filename='',
            text='#include <stdio.h>',
        )
        self.assertEqual(lexer.pygments_lexer_cls, CLexer)

        lexer = guess_lexer_wrapper(
            filename='foo',
            text='<html></html>',
        )
        self.assertEqual(lexer.pygments_lexer_cls, XmlLexer)

        lexer = guess_lexer_wrapper(
            filename='',
            text='',
        )
        self.assertEqual(lexer.pygments_lexer_cls, TextLexer)

        # simulate old pygments behaviour using monkeypatch
        def guess_lexer_mock(text):
            if not text:
                raise ClassNotFound()

        original_guess_lexer = lexer_helper.guess_lexer
        lexer_helper.guess_lexer = guess_lexer_mock
        lexer = guess_lexer_wrapper(
            filename='',
            text='',
        )
        lexer_helper.guess_lexer = original_guess_lexer
        self.assertIsInstance(lexer, SimpleLexer)

    def test_filename_has_priority_over_content(self):
        lexer = guess_lexer_wrapper(
            filename='script.sh',
            text='import sys\nprint(sys)',
        )
        self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

        lexer = guess_lexer_wrapper(
            filename='main.py',
            text='#include <stdio.h>',
        )
        self.assertEqual(lexer.pygments_lexer_cls, PythonLexer)

    def test_shell_files(self):
        filenames = (
            '.bashrc',
            '/home/foo/profile',
            'bash.bashrc',
            'script.sh',
            'execute.bash',
            'run.zsh',
            'start.ksh',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

    def test_config_files(self):
        filenames = (
            'network/interfaces',
            '/etc/hosts',
            'partition.uuu',
            'foobar.uuu',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

    def test_systemd_files(self):
        filenames = (
            '/etc/systemd/system/foo.service',
            'bar.target',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, SystemdLexer)

    def test_yocto_files(self):
        filenames = (
            'local.conf',
            'local.conf.sample',
            'affe_git.bb',
            'recipes-fixes/htop/htop.bbappend',
            'common.bbclass',
            'kernel.inc',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

    def test_readme_files(self):
        filenames = (
            'readme',
            'project/README',
            'readme.md',
            'README.md',
            'project/README.MD',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, MarkdownLexer)

    def test_gitconfig_files(self):
        filenames = (
            '~/.gitconfig',
            '/etc/gitconfig',
            '.gitconfig',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, IniLexer)

    def test_regular_text_with_comment_support_files(self):
        filenames = (
            'git/COMMIT_EDITMSG',
            'COMMIT_EDITMSG',
            'MERGE_MSG',
            'gitignore',
            'git-rebase-todo',
            '/etc/fstab',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_jenkins_files(self):
        filenames = (
            'project/jenkinsfile',
            'JENKINSFILE',
            '/project/GlobalJenkinsfile',
            'Jenkinsfile',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, GroovyLexer)

    def test_make_files(self):
        filenames = (
            'Makefile',
            'build.ninja',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, MakefileLexer)

    def test_requirements_txt_files(self):
        filenames = (
            'requirements.txt',
            'example-requirements.txt',
            'requirements-dev.txt',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_cmake_files(self):
        filenames = (
            'CMakeLists.txt',
            'util.cmake',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, CMakeLexer)

    def test_text_files(self):
        for text in ('', '123: foo\n'):
            filenames = (
                'readme.txt',
                'license.text',
                'LICENSE',
                'CHANGELOG',
                'CHANGES',
                'AUTHORS',
                'syslog.log',
                'syslog',
                'warnings.log',
                'CMakeOutput.log',
            )
            for filename in filenames:
                lexer = guess_lexer_wrapper(filename=filename, text=text)
                self.assertEqual(lexer.pygments_lexer_cls, TextLexer, msg='Text: "{0}"'.format(text))

    def test_perl_files(self):
        filenames = (
            'Markdown.pl',
            'script.perl',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, PerlLexer)

    def test_ini_config_files(self):
        filename = 'local.conf'
        text = '\n' \
               '\n' \
               '# some\n' \
               '; random\n' \
               '    noise\n' \
               '[section]\n' \
               '    key=value'
        lexer = guess_lexer_wrapper(filename=filename, text=text)
        self.assertEqual(lexer.pygments_lexer_cls, IniLexer)

    def test_yocto_config_files(self):
        filename = 'local.conf'
        text = 'LCONF_VERSION = "6"\n' \
               '\n' \
               'BBPATH = "${TOPDIR}"'
        lexer = guess_lexer_wrapper(filename=filename, text=text)
        self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

    def test_robot_framework_files(self):
        filenames = (
            'test.robot',
            'foobar.robot',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, RobotFrameworkLexer)

    def test_resource_files(self):
        filename = 'common.resource'
        text = 'from foo import bar\n'
        lexer = guess_lexer_wrapper(filename=filename, text=text)
        self.assertEqual(lexer.pygments_lexer_cls, RobotFrameworkLexer)

        filename = 'common.resource'
        text = '# comment\n' \
               '*** MySection ***\n'
        lexer = guess_lexer_wrapper(filename=filename, text=text)
        self.assertEqual(lexer.pygments_lexer_cls, RobotFrameworkLexer)

        filename = 'common.resource'
        text = 'Library foo\n' \
               '| | start | executable\n'
        lexer = guess_lexer_wrapper(filename=filename, text=text)
        self.assertEqual(lexer.pygments_lexer_cls, RobotFrameworkLexer)

    def test_clang_format_files(self):
        filenames = (
            '.clang-format',
            '_clang-format',
            'clang-format',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, YamlLexer)

    def test_plantuml_files(self):
        filenames = (
            'diagram.pu',
            'class.puml',
            'sequence_diagram.plantuml',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, ObjectiveCLexer)

    def test_ssh_config_files(self):
        def realpath_mock(*args, **kwargs):
            path = realpath_orig(*args, **kwargs)
            if path[1] == ':':  # e.g. 'C:\Windows'
                path = path[2:]
            path = path.replace('\\', '/')
            return path

        if sys.platform == 'win32':
            realpath_orig = os.path.realpath
            os.path.realpath = realpath_mock

        filenames = (
            'ssh_config',
            'sshd_config',
            '/home/affe/.ssh/config',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

        filenames = (
            'config',
            '/etc/backup/config',
            '/home/affe/.ssh/config_bak',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertNotEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_spec_files(self):
        lexer = guess_lexer_wrapper(filename='lightimer.spec', text='')
        self.assertEqual(lexer.pygments_lexer_cls, PythonLexer)

    def test_netrc_files(self):
        filenames = (
            '.netrc',
            '~/.netrc',
            '_netrc',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_env_files(self):
        lexer = guess_lexer_wrapper(filename='.env', text='')
        self.assertEqual(lexer.pygments_lexer_cls, BashLexer)

    def test_cargo_lock_files(self):
        lexer = guess_lexer_wrapper(filename='Cargo.lock', text='')
        self.assertEqual(lexer.pygments_lexer_cls, IniLexer)

    def test_resolv_conf_files(self):
        lexer = guess_lexer_wrapper(filename='resolv.conf', text='')
        self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_cntlm_conf_files(self):
        lexer = guess_lexer_wrapper(filename='cntlm.conf', text='')
        self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)

    def test_tmux_conf_files(self):
        filenames = (
            '.tmux.conf',
            'keybindings.tmux',
        )
        for filename in filenames:
            lexer = guess_lexer_wrapper(filename=filename, text='')
            self.assertEqual(lexer.pygments_lexer_cls, TextWithCommentLexer)
