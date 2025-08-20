import os

from collections import OrderedDict

from pygments.lexers import get_lexer_for_filename, guess_lexer
from pygments.lexers.c_cpp import CLexer
from pygments.lexers.configs import IniLexer, UnixConfigLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.jvm import GroovyLexer
from pygments.lexers.make import MakefileLexer, CMakeLexer
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.objective import ObjectiveCLexer
from pygments.lexers.perl import PerlLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.shell import BashLexer
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound

from prompt_toolkit.lexers import PygmentsLexer, SimpleLexer

from lexers.text_with_comment_lexer import TextWithCommentLexer


def __check_ssh_config_files(filename):
    if filename in ('ssh_config', 'sshd_config'):
        return True
    path = os.path.realpath(filename)
    return path.startswith('/home/') and path.endswith('/.ssh/config')


def __check_requirements_txt(filename):
    return 'requirements' in filename and filename.endswith('.txt')


def __check_ini_content(text):
    return any(line.strip().startswith('[') and line.strip().endswith(']') for line in text.splitlines())


def __check_yocto_endings(filename):
    yocto_endings = ('.conf', '.conf.sample', '.bb', '.bbappend', '.bbclass', '.inc')
    blacklist_endings = ('resolv.conf', 'cntlm.conf', '.tmux.conf')
    return any(filename.endswith(ending) for ending in yocto_endings) and not any(filename.endswith(ending) for ending in blacklist_endings)


def guess_lexer_wrapper(filename, text):
    if __check_ssh_config_files(filename):
        return PygmentsLexer(TextWithCommentLexer)
    if __check_requirements_txt(filename):
        return PygmentsLexer(TextWithCommentLexer)

    if __check_yocto_endings(filename):
        if __check_ini_content(text):
            # file has yocto-like ending but contains ini-style sections, e.g.: [section]
            return PygmentsLexer(IniLexer)
        return PygmentsLexer(BashLexer)

    lexers_assignment = OrderedDict()
    lexers_assignment[UnixConfigLexer] = ('group', 'passwd', 'shadow')
    lexers_assignment[BashLexer] = (
        'bashrc', 'profile',
        'interfaces', 'hosts', '.uuu',
        '.ac', '.m4',  # autoconf
        '.env',
    )
    lexers_assignment[CLexer] = (
        '.c', '.h',
        '.c.in', '.h.in',
    )
    lexers_assignment[IniLexer] = (
        'gitconfig',
        'Cargo.lock',
    )

    lexers_assignment[TextWithCommentLexer] = (
        'gitignore', 'gitattributes', 'commit_editmsg', 'merge_msg', 'git-rebase-todo',
        'fstab',
        '.netrc', '_netrc',
        '.conf',
        '.tmux',
    )
    lexers_assignment[MarkdownLexer] = ('readme', 'readme.md')
    lexers_assignment[GroovyLexer] = ('jenkinsfile',)
    lexers_assignment[MakefileLexer] = (
        'Makefile', 'build.ninja',
        'Makefile.in', 'Makefile.am',
    )
    lexers_assignment[CMakeLexer] = ('cmakelists.txt', '.cmake')
    lexers_assignment[TextLexer] = (
        '.txt', '.text',
        'license', 'changelog', 'changes', 'authors',
        'syslog', '.log',
    )
    lexers_assignment[PerlLexer] = ('.pl', '.perl')
    lexers_assignment[YamlLexer] = ('clang-format',)
    lexers_assignment[ObjectiveCLexer] = ('.pu', '.puml', '.plantuml')
    lexers_assignment[PythonLexer] = ('.spec',)

    for lexer, file_endings in lexers_assignment.items():
        if any(filename.lower().endswith(ending.lower()) for ending in file_endings):
            return PygmentsLexer(lexer)

    try:
        pygments_lexer = get_lexer_for_filename(filename)
        # print(pygments_lexer)
    except ClassNotFound:
        try:
            pygments_lexer = guess_lexer(text)
            # print(pygments_lexer)
        except ClassNotFound:
            return SimpleLexer()
    return PygmentsLexer(pygments_lexer.__class__)
