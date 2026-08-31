import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

from globals import Globals
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


def check_for_clipboard_manager():
    def display_hint(clipboard):
        print('{} is needed for system-wide clipboard support.'.format(clipboard))
        print('Please install it using your package manager.')
        print()
        print('If you\'re on a headless system you can bypass this check temporarily by running:')
        print()
        print('    affe --headless <file>')
        print()
        print('You can also add the following line to your shell profile file (e.g. ~/.profile or ~/.zprofile) to bypass this check permanently:')
        print()
        print('    export AFFE_HEADLESS=1')
        print()
        sys.exit(1)

    window_manager = os.getenv('XDG_SESSION_TYPE')
    if not window_manager or window_manager == 'tty':
        return
    elif window_manager == 'wayland':
        clipboard = 'wl-clipboard'
        if not (shutil.which('wl-copy') and shutil.which('wl-paste')):
            display_hint(clipboard)
    elif window_manager in ('x11', 'xorg'):
        clipboard = 'xclip'
        if not shutil.which(clipboard):
            display_hint(clipboard)


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
    import pygments

    from prompt_toolkit import print_formatted_text
    from prompt_toolkit.formatted_text import PygmentsTokens

    from util.lexer_helper import guess_lexer_wrapper

    text = read_file(file_path)
    if not os.path.isfile(file_path):
        print('File does not exist.')
        sys.exit(1)
    lexer = guess_lexer_wrapper(file_path, text).pygments_lexer
    tokens = list(pygments.lex(text, lexer=lexer))
    print_formatted_text(PygmentsTokens(tokens), style=style)


def update():
    import requests

    from packaging.version import Version

    repo_url = 'https://github.com/Leistungsabfall/affe'
    repo_api_url = 'https://api.github.com/repos/Leistungsabfall/affe'
    timeout = 10
    version_regex = r'^[0-9]+\.[0-9]+\.[0-9]+$'
    current_version = get_version()
    if current_version == 'dev':
        print('Preventing update from local "dev" version.')
        sys.exit(1)
    if sys.platform == 'win32':
        print('Automatic update is not supported on Windows.')
        sys.exit(1)
    try:
        latest_version_response = requests.get(
            url='{}/releases/latest'.format(repo_url),
            allow_redirects=True,
            timeout=timeout,
        )
        latest_version_response.raise_for_status()
        latest_version = latest_version_response.url.split('/')[-1]
        if not re.match(version_regex, latest_version):
            print('Could not fetch latest version from GitHub, trying fallback method.')
            latest_version_response = requests.get(
                url='{}/releases/latest'.format(repo_api_url),
                timeout=timeout,
            )
            latest_version_response.raise_for_status()
            release = latest_version_response.json()
            latest_version = release.get('tag_name', '').strip()
            if not re.match(version_regex, latest_version):
                print('Could not fetch latest version due to GitHub API rate limits, try again later.')
                sys.exit(1)

        if current_version == latest_version:
            print('You already have the latest version ({}).'.format(current_version))
            sys.exit(0)
        if Version(current_version) < Version(latest_version):
            print('There is an update available! 🎉')
            res = input('Do you want to update from {} to {}? (y/n) '.format(current_version, latest_version)).strip()
            if res.lower() != 'y':
                print('Aborting update.')
                sys.exit(0)
            print('Downloading installation script.')
            script_name = 'install'
            install_script_response = requests.get('https://affe.sh/{}'.format(script_name), timeout=timeout)
            install_script_response.raise_for_status()
            install_script = install_script_response.text
            with tempfile.NamedTemporaryFile(mode='w') as temp_file:
                temp_file.write(install_script)
                temp_file.flush()
                print('Calling installation script.\n')
                p = subprocess.Popen(
                    args=['sh', temp_file.name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=tempfile.gettempdir(),
                    text=True,
                    bufsize=1,
                    )
                if p.stdout is not None:
                    for line in p.stdout:
                        print(line, end='')
                p.wait()
                sys.exit(0)
        if Version(current_version) > Version(latest_version):
            print('Local version ({}) is newer than version on server ({}). '
                  'What did you do? 🤯'.format(current_version, latest_version))
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print('Update failed with the following error:')
        print()
        print(str(e))
        print()
        print('Please try again later and visit https://affe.sh.')
        sys.exit(1)


def update_terminal_title(title):
    print('\033]0;affe: {}\007'.format(title), end='', flush=True)


def reset_terminal_title():
    print('\033]0;\007', end='', flush=True)
