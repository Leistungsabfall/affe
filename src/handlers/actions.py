import subprocess
import time

from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.special import TextLexer

from background_update.auto_update_thread import AutoUpdateThread
from completers.fuzzy_word_completer import FuzzyWordCompleter
from dialogs.closable_dialog import ClosableDialog
from globals import Globals
from handlers.keys import handle_save, handle_select_all
from prompt_toolkit.application import get_app
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import Label, Button
from util.changelog_helper import get_changelog
from util.git_helper import file_is_untracked, GIT_ERROR_TEXT
from util.license_helper import get_license
from util.readme_helper import get_readme
from util.common import get_version_info, text_is_unsaved, read_file
from util.gui_helper import show_message, show_scrollable_dialog, is_menu_focused
from util.text_helper import move_cursor_to_next_match, get_find_matches
from util.third_party_licenses_helper import get_third_party_licenses


def handle_exit():
    def exit_():
        Globals.exit_request = True  # AutoUpdateThread will return not later than SUB_INTERVAL_SECONDS
        time.sleep(AutoUpdateThread.SUB_INTERVAL_SECONDS*1.5)
        get_app().exit()

    def save_and_exit(dialog):
        dialog.close()
        handle_save()
        exit_()

    def show_unsaved_changes_dialog():
        dialog = ClosableDialog(
            title='Unsaved changes in \'{}\''.format(Globals.file_name),
            body=Label(text='Unsaved changes will get lost if you exit without saving.', dont_extend_height=True),
            buttons=[
                Button(text='Go back', handler=lambda: dialog.close()),
                Button(text='Save & Exit', handler=lambda: save_and_exit(dialog)),
                Button(text='Exit without saving', handler=exit_),
            ],
        )
        dialog.show()

    if FuzzyWordCompleter.completion_active:
        FuzzyWordCompleter.completion_active = False
        Globals.text_field.buffer.cancel_completion()
        return

    if Globals.show_find_window:
        Globals.show_find_window = False
        Globals.show_replace_window = False
        return

    if Globals.git_blame_active:
        handle_toggle_git_blame()
        return

    if text_is_unsaved():
        show_unsaved_changes_dialog()
    else:
        exit_()


def handle_about():
    def get_text(monkey):
        created_by = 'Made with ♥  by Leistungsabfall.'
        left_indentation = ' ' * (80 - 4 - len(created_by))
        text_template = '{monkey}\n' \
            '{version}\n\n' \
            '{indentation}{created_by}'
        return text_template.format(
            monkey=monkey,
            version=get_version_info(),
            indentation=left_indentation,
            created_by=created_by,
        )

    monkey1 = r"""
                     __,__
            .--.  .-"     "-.  .--.
           / .. \/  .-. .-.  \/ .. \
          | |  '|  /   Y   \  |'  | |
          | \   \  \ 0 | 0 /  /   / |
           \ '- ,\.-"`` ``"-./, -' /
            `'-' /_   ^ ^   _\ '-'`
            .--'|  \._   _./  |'--. 
          /`    \   \ `~` /   /    `\
         /       '._ '---' _.'       \     The more features an application
        /           '~---~'   |       \    provides, the harder will people
       /        _.             \       \   actually start using it.
      /   .'-./`/        .'~'-.|\       \
     /   /    `\:       /      `\'.      \        - An unknown Monkey (2019)
    /   |       ;      |         '.`;    /
    \   \       ;      \           \/   /
     '.  \      ;       \       \   `  /
       '._'.     \       '.      |   ;/_
         /__>     '.       \_ _ _/   ,  '--.
       .'   '.   .-~~~~~-. /     |--'`~~-.  \
      // / .---'/  .-~~-._/ / / /---..__.'  /
     ((_(_/    /  /      (_(_(_(---.__    .'
               | |     _              `~~`
               | |     \'.
                \ '....' |
                 '.,___.'
    """
    monkey2 = r"""
                     __,__
            .--.  .-"     "-.  .--.
           / .. \/  .-. .-.  \/ .. \
          | |  '|  /   Y   \  |'  | |
          | \   \  \ - | - /  /   / |
           \ '- ,\.-"`` ``"-./, -' /
            `'-' /_   ^ ^   _\ '-'`
            .--'|  \._   _./  |'--. 
          /`    \   \ `~` /   /    `\
         /       '._ '---' _.'       \     The more features an application
        /           '~---~'   |       \    provides, the harder will people
       /        _.             \       \   actually start using it.
      /   .'-./`/        .'~'-.|\       \
     /   /    `\:       /      `\'.      \        - An unknown Monkey (2019)
    /   |       ;      |         '.`;    /
    \   \       ;      \           \/   /
     '.  \      ;       \       \   `  /
       '._'.     \       '.      |   ;/_
         /__>     '.       \_ _ _/   ,  '--.
       .'   '.   .-~~~~~-. /     |--'`~~-.  \
      // / .---'/  .-~~-._/ / / /---..__.'  /
     ((_(_/    /  /      (_(_(_(---.__    .'
               | |     _              `~~`
               | |     \'.
                \ '....' |
                 '.,___.'
    """

    monkey3 = r"""
                     __,__
            .--.  .-"     "-.  .--.
           / .. \/  .-. .-.  \/ .. \
          | |  '|  /   Y   \  |'  | |
          | \   \  \ 0 | 0 /  /   / |
           \ '- ,\.-"`` ``"-./, -' /
            `'-' /_   ^ ^   _\ '-'`
            .--'|  \._ _ _./  |'--.
          /`    \   \.-.  /   /    `\
         /       '._/  |-' _.'       \     The more features an application
        /          ;  /--~'   |       \    provides, the harder will people
       /        .'\|.-\--.     \       \   actually start using it.
      /   .'-. /.-.;\  |\|'~'-.|\       \
      \       `-./`|_\_/ `     `\'.      \        - An unknown Monkey (2019)
       '.      ;     ___)        '.`;    /
         '-.,_ ;     ___)          \/   /
          \   ``'------'\       \   `  /
           '.    \       '.      |   ;/_
         ___>     '.       \_ _ _/   ,  '--.
       .'   '.   .-~~~~~-. /     |--'`~~-.  \
      // / .---'/  .-~~-._/ / / /---..__.'  /
     ((_(_/    /  /      (_(_(_(---.__    .'
               | |     _              `~~`
               | |     \'.
                \ '....' |
                 '.,___.'
    """

    monkey4 = r"""
                     __,__
            .--.  .-"     "-.  .--.
           / .. \/  .-. .-.  \/ .. \
          | |  '|  /   Y   \  |'  | |
          | \   \  \ 0 | - /  /   / |
           \ '- ,\.-"`` ``"-./, -' /
            `'-' /_   ^ ^   _\ '-'`
            .--'|  \._   _./  |'--. 
          /`    \   \ `~` /   /    `\
         /       '._ '---' _.'       \     The more features an application
        /           '~---~'   |       \    provides, the harder will people
       /        _.             \       \   actually start using it.
      /   .'-./`/        .'~'-.|\       \
     /   /    `\:       /      `\'.      \        - An unknown Monkey (2019)
    /   |       ;      |         '.`;    /
    \   \       ;      \           \/   /
     '.  \      ;       \       \   `  /
       '._'.     \       '.      |   ;/_
         /__>     '.       \_ _ _/   ,  '--.
       .'   '.   .-~~~~~-. /     |--'`~~-.  \
      // / .---'/  .-~~-._/ / / /---..__.'  /
     ((_(_/    /  /      (_(_(_(---.__    .'
               | |     _              `~~`
               | |     \'.
                \ '....' |
                 '.,___.'
    """

    text1 = get_text(monkey=monkey1)
    text2 = get_text(monkey=monkey2)
    text3 = get_text(monkey=monkey3)
    text4 = get_text(monkey=monkey4)

    show_message(
        title='About',
        text=[
            text1,
            text1,
            text2,
            text1,
            text1,
            text1,
            text1,
            text2,
            text1,
            text2,
            text1,
            text1,
            text1,
            text1,
            text3,
            text3,
            text1,
            text1,
            text4,
            text1,
            text1,
        ],
        toggle_interval=0.5,
    )


def handle_menu():
    if not is_menu_focused():
        get_app().layout.focus(Globals.root_container.window)
    else:
        get_app().layout.focus(Globals.text_field)


def handle_find():
    Globals.show_replace_window = False
    Globals.show_find_window = True
    Globals.text_field.buffer.exit_selection()
    move_cursor_to_next_match(keep_position_if_on_cursor=True)
    get_app().layout.focus(Globals.find_toolbar_text_field)
    handle_select_all()


def handle_replace():
    handle_find()
    Globals.show_replace_window = True
    get_app().layout.focus(Globals.replace_toolbar_text_field)
    handle_select_all()


def handle_on_find_toolbar_input_changed(move_cursor=True):
    if get_find_matches() or Globals.find_toolbar_text_field.text == '':
        Globals.find_toolbar_text_field.window.style = 'class:find-and-replace-textfield'
        if move_cursor:
            move_cursor_to_next_match(keep_position_if_on_cursor=True)
    else:
        Globals.find_toolbar_text_field.window.style = 'class:find-and-replace-textfield-no-match'


def handle_readme():
    text = """
    Congratulations, you made it to the help page!
    You can scroll through this document using the page up/page down keys or the mouse wheel.
    Press Esc to close this dialog.

===========
README.md

%s
""" % get_readme()

    show_scrollable_dialog(title='Readme', text=text, lexer=PygmentsLexer(MarkdownLexer))


def handle_changelog():
    text = get_changelog()
    show_scrollable_dialog(title='Changelog', text=text, lexer=PygmentsLexer(MarkdownLexer))


def handle_license():
    text = get_license()
    show_scrollable_dialog(title='License', text=text, lexer=PygmentsLexer(TextLexer))


def handle_third_party_licenses():
    text = get_third_party_licenses()
    show_scrollable_dialog(title='third-party-licenses', text=text, lexer=PygmentsLexer(TextLexer))


def handle_git_revert():
    def git_revert():
        dialog.close()
        if not Globals.git_dir:
            Globals.git_revert_failed = True
            return

        p = subprocess.Popen(
            ['git', 'checkout', '--', Globals.relative_file_path_from_git_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Globals.git_dir,
        )
        p.communicate()
        if p.returncode != 0:
            Globals.git_revert_failed = True
            return

        cursor_position = Globals.text_field.document.cursor_position
        original_cursor_position_row, original_cursor_position_col = \
            Globals.text_field.document.translate_index_to_position(cursor_position)

        new_text = read_file(Globals.file_path)
        Globals.text_field.text = new_text
        Globals.saved_text = new_text

        new_cursor_position = Globals.text_field.document.translate_row_col_to_index(
            original_cursor_position_row, original_cursor_position_col
        )
        Globals.text_field.buffer.cursor_position = new_cursor_position

    if file_is_untracked():
        dialog = ClosableDialog(
            title='Error restoring file from git',
            body=Label(text=GIT_ERROR_TEXT, dont_extend_height=True),
            buttons=[
                Button(text='Close', handler=lambda: dialog.close()),
            ],
        )
        dialog.show()
        return

    dialog = ClosableDialog(
        title='Restore from git',
        body=Label(text='Resets this file to the version stored in git (git checkout -- <file>).\n'
                        'Current changes will get lost.', dont_extend_height=True),
        buttons=[
            Button(text='Cancel', handler=lambda: dialog.close()),
            Button(text='Perform git checkout', handler=git_revert),
        ],
    )
    dialog.show()


def handle_toggle_git_blame():
    def update_menu_item():
        char = '*' if Globals.git_blame_active else ' '
        Globals.git_blame_menu_item.text = '[' + char + Globals.git_blame_menu_item.text[2:]

    if file_is_untracked():
        Globals.git_blame_active = False
        update_menu_item()
        dialog = ClosableDialog(
            title='Error getting git blame info',
            body=Label(text=GIT_ERROR_TEXT, dont_extend_height=True),
            buttons=[
                Button(text='Close', handler=lambda: dialog.close()),
            ],
        )
        dialog.show()
        return

    Globals.git_blame_active = not Globals.git_blame_active
    update_menu_item()
