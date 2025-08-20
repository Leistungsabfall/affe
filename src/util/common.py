import os
import shutil
import signal
import subprocess
import sys
import tempfile

import pygments
import requests
from packaging.version import Version

from globals import Globals
from prompt_toolkit.formatted_text import PygmentsTokens
from util.lexer_helper import guess_lexer_wrapper
from util.version_helper import get_version

opening_special_chars = ('{', '(', '[')
closing_special_chars = ('}', ')', ']')
opening_and_closing_special_chars = ('"', "'")

special_char_mapping = {
    '[': ']',
    '(': ')',
    '{': '}',
    '"': '"',
    "'": "'",
}


def check_for_xclip():
    if shutil.which('xclip'):
        return
    print('xclip is needed for system-wide clipboard support.')
    print('Please install it:')
    print()
    print('    sudo apt install xclip')
    print()
    print('If you\'re on a headless system you can bypass this check by running:')
    print()
    print('    affe <file> --headless')
    print()
    sys.exit(1)


def check_for_file(ignore_readonly):
    def is_directory():
        return os.path.isdir(Globals.file_path)

    def not_readable():
        return os.path.isfile(Globals.file_path) and not os.access(Globals.file_path, os.R_OK) and not root()

    def root():
        return os.getuid() == 0

    def readonly():
        return os.path.isfile(Globals.file_path) and not os.access(Globals.file_path, os.W_OK) and not root()

    def directory_does_not_exist():
        directory_ = os.path.dirname(Globals.file_path)
        return directory_ != '' and not os.path.exists(directory_)

    def not_writable():
        if os.path.isfile(Globals.file_path):
            return False

        try:
            with open(Globals.file_path, 'w'):
                pass
            os.remove(Globals.file_path)
            return False
        except IOError:
            return True

    def wait_for_enter_or_ctrl_c():
        def restore_sighandler():
            signal.signal(signal.SIGINT, orig_sighandler)

        def exit_(_, __):
            restore_sighandler()
            sys.exit(0)

        orig_sighandler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, exit_)
        input()
        restore_sighandler()

    if not Globals.file_path:
        print(get_version_info())
        print('I need a file to open. Run me like this:')
        print()
        print('  affe <file>')
        print()
        sys.exit(0)

    if is_directory():
        print('I can\'t handle directories. Please give me a file:')
        print()
        print('  affe <file>')
        print()
        sys.exit(1)

    if not_readable():
        print('Can\'t open file for reading.')
        print('Try using sudo:')
        print()
        print('    sudo affe {}'.format(Globals.file_path))
        print()
        sys.exit(1)

    if readonly() and not ignore_readonly:
        print('Can\'t open file for writing.')
        print('Try using sudo:')
        print()
        print('    sudo affe {}'.format(Globals.file_path))
        print()
        print('Press Enter to continue in read-only mode or Ctrl+C to quit...')
        wait_for_enter_or_ctrl_c()
        Globals.read_only = True

    if directory_does_not_exist():
        directory = os.path.dirname(Globals.file_path)
        print('Directory "{}" does not exist.'.format(directory))
        print('Create with:')
        print()
        print('    (sudo) mkdir -p {}'.format(directory))
        print()
        sys.exit(1)

    if not_writable():
        print('Can\'t create file in this directory.')
        print('Try using sudo:')
        print()
        print('    sudo affe {}'.format(Globals.file_path))
        print()
        sys.exit(1)


def get_version_info():
    return 'This is affe - a full-fledged editor (version {}).'.format(get_version())


def text_is_unsaved():
    return Globals.text_field.text != Globals.saved_text


class Direction:
    Down = 'down'
    Left = 'left'
    Right = 'right'
    Up = 'up'


def read_file(file_path):
    for encoding in ('utf-8', 'latin1'):
        try:
            with open(file_path, mode='r', encoding=encoding) as file_:
                return file_.read()
        except FileNotFoundError:
            return ''
        except UnicodeDecodeError:
            pass
    raise LookupError('Error reading file {}'.format(file_path))


def print_text(file_path, style):
    from prompt_toolkit import print_formatted_text
    text = read_file(file_path)
    if not os.path.isfile(file_path):
        print('File does not exist.')
        sys.exit(1)
    lexer = guess_lexer_wrapper(file_path, text).pygments_lexer
    tokens = list(pygments.lex(text, lexer=lexer))
    print_formatted_text(PygmentsTokens(tokens), style=style)


def update():
    current_version = get_version()
    if current_version == 'dev':
        print('Preventing update from local "dev" version.')
        sys.exit(1)
    latest_version = requests.get(url="https://affe.sh/bin/version.txt").text.strip()
    if current_version == latest_version:
        print('You already have the latest version ({}).'.format(current_version))
        sys.exit(0)
    if Version(current_version) < Version(latest_version):
        print('There is an update available!')
        res = input('Do you want to update from {} to {}? (y/n) '.format(current_version, latest_version)).strip()
        if res.lower() != 'y':
            print('Aborting update.')
            sys.exit(0)
        print('Downloading installation script.')
        script_name = "linux"
        if sys.platform == "win32":
            if not os.path.exists(os.path.join(os.environ["USERDIR"], "bin")):
                print("Aborting update. Please update only in Git Bash for Windows.")
                sys.exit(1)
            script_name = "windows"
        install_script = requests.get("https://affe.sh/{}".format(script_name)).text
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(install_script)
        print('Calling installation script.\n')
        current_dir = os.getcwd()
        os.chdir(tempfile.gettempdir())
        p = subprocess.Popen(['sh', temp_file.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        os.chdir(current_dir)
        stdout, _ = p.communicate()
        os.unlink(temp_file.name)
        print(stdout.decode('utf-8'))
        sys.exit(0)
    if current_version > latest_version:
        print('Local version ({}) is newer than version on server ({}). '
              'What did you do? :O'.format(current_version, latest_version))
        sys.exit(1)
