from globals import Globals
from handlers import actions, keys
from key_bindings.bindings import init_key_bindings
from prompt_toolkit.layout import Float, CompletionsMenu
from prompt_toolkit.widgets import MenuContainer, MenuItem
from util.common import Direction


def get_main_menu(body):
    file_menu = MenuItem(
        'File',
        children=[
            MenuItem('Save             (Ctrl+S)', handler=keys.handle_save),
            MenuItem('-', disabled=True),
            MenuItem('Restore from git (Ctrl+G)', handler=actions.handle_git_revert),
            MenuItem('-', disabled=True),
            MenuItem('Exit             (Esc)', handler=actions.handle_exit),
        ]
    )
    edit_menu = MenuItem(
        'Edit',
        children=[
            MenuItem('Undo                (Ctrl+Z)', handler=keys.handle_undo),
            MenuItem('Redo                (Ctrl+Y)', handler=keys.handle_redo),
            MenuItem('-', disabled=True),
            MenuItem('Cut                 (Ctrl+X)', handler=keys.handle_cut),
            MenuItem('Copy                (Ctrl+C)', handler=keys.handle_copy),
            MenuItem('Paste               (Ctrl+V)', handler=keys.handle_paste),
            MenuItem('Select All          (Ctrl+A)', handler=keys.handle_select_all),
            MenuItem('-', disabled=True),
            MenuItem('Find                (Ctrl+F)', handler=actions.handle_find),
            MenuItem('Replace             (Ctrl+R)', handler=actions.handle_replace),
            MenuItem('-', disabled=True),
            MenuItem('Comment/Uncomment   (Ctrl+K)', handler=keys.handle_comment),
            MenuItem('Select current word (Ctrl+W)', handler=keys.handle_select_word_under_cursor),
            MenuItem('Jump to new line    (Ctrl+N)', handler=keys.handle_jump_to_new_line),
            MenuItem('Toggle case         (Ctrl+T)', handler=keys.handle_toggle_case),
            MenuItem('-', disabled=True),
            MenuItem('Move selection up   (Ctrl+Up)', handler=lambda: keys.handle_control_arrow(Direction.Up)),
            MenuItem('Move selection down (Ctrl+Down)', handler=lambda: keys.handle_control_arrow(Direction.Down)),
        ]
    )
    Globals.git_blame_menu_item = MenuItem('[ ] git blame (Ctrl+B)', handler=actions.handle_toggle_git_blame)
    view_menu = MenuItem(
        'View',
        children=[
            Globals.git_blame_menu_item,
        ]
    )
    help_menu = MenuItem(
        'Help',
        children=[
            MenuItem('Readme (F12)        ', handler=actions.handle_readme),
            MenuItem('Changelog           ', handler=actions.handle_changelog),
            MenuItem('License             ', handler=actions.handle_license),
            MenuItem('Third-party-licenses', handler=actions.handle_third_party_licenses),
            MenuItem('About               ', handler=actions.handle_about),
        ]
    )
    root_container = MenuContainer(
        body=body,
        menu_items=[
            file_menu,
            edit_menu,
            view_menu,
            help_menu,
        ], floats=[
            Float(
                xcursor=True,
                ycursor=True,
                content=CompletionsMenu(
                    max_height=16,
                    scroll_offset=1,
                )
            ),
        ],
        key_bindings=init_key_bindings(),
    )
    return root_container
