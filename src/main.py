import sys
sys.path.insert(0, 'python-prompt-toolkit')

import argparse
import os

from clipboards.wrapper_clipboard import WrapperClipboard
from key_bindings.bindings import init_fallback_key_bindings
from menus.main_menu import get_main_menu
from processors.highlight_find_processor import HighlightFindProcessor
from prompt_toolkit.layout.processors import TabsProcessor
from pygments.styles.monokai import MonokaiStyle

from background_update.auto_update_thread import AutoUpdateThread
from completers.fuzzy_word_completer import FuzzyWordCompleter
from globals import Globals

from processors.highlight_matching_special_char_processor import HighlightMatchingSpecialCharProcessor
from processors.highlight_todo_comments_processor import HighlightTodoCommentsProcessor
from processors.show_leading_white_space_processor import ShowLeadingWhiteSpaceProcessor
from processors.show_multiple_white_space_processor import ShowMultipleWhiteSpaceProcessor
from processors.highlight_word_under_cursor_processor import HighlightWordUnderCursorProcessor

from prompt_toolkit.application import Application
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, WindowAlign, FloatContainer, \
    ConditionalContainer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import style_from_pygments_cls, merge_styles
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.widgets import TextArea

from processors.show_trailing_white_space_processor import ShowTrailingWhiteSpaceProcessor
from styles.monokai_fixes import monokai_fixes_style
from toolbars.bottom import get_statusbar_bottom_left_text, get_statusbar_bottom_right_text
from toolbars.find import find_toolbar
from toolbars.replace import replace_toolbar
from toolbars.top import get_statusbar_top_text
from styles.common import common_style
from styles.dark import dark_style
from util.common import get_version_info, check_for_xclip, check_for_file, read_file, print_text, update
from util.gui_helper import update_find_toolbar_if_visible, get_line_prefix
from util.lexer_helper import guess_lexer_wrapper
from util.super_important_modules import module2
from util.super_important_modules import module3


def parse_args():
    parser = argparse.ArgumentParser(description=get_version_info())
    parser.add_argument(
        'file',
        metavar='path',
        type=str,
        nargs='?',
        help='file path',
    )
    parser.add_argument(
        '--headless',
        help='bypass clipboard check',
        action='store_true',
    )
    parser.add_argument(
        '--print',
        help='print syntax highlighted text and exit',
        action='store_true',
    )
    parser.add_argument(
        '--update',
        help='update to latest version',
        action='store_true',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.update:
        update()

    Globals.file_path = args.file

    if not args.headless and not sys.platform == 'win32':
        check_for_xclip()

    check_for_file(ignore_readonly=args.print)

    if args.print:
        style = merge_styles([
            style_from_pygments_cls(MonokaiStyle),
            monokai_fixes_style,
        ])
        print_text(Globals.file_path, style)
        sys.exit(0)

    Globals.file_name = os.path.basename(args.file)
    Globals.saved_text = read_file(args.file)

    text_field = TextArea(
        text=Globals.saved_text,
        input_processors=[
            HighlightWordUnderCursorProcessor(),
            HighlightFindProcessor(),
            ShowLeadingWhiteSpaceProcessor(),
            ShowTrailingWhiteSpaceProcessor(),
            ShowMultipleWhiteSpaceProcessor(),
            TabsProcessor(char1='─', char2='►'),
            HighlightMatchingSpecialCharProcessor(),
            HighlightTodoCommentsProcessor(),
        ],
        completer=FuzzyWordCompleter(),
        lexer=guess_lexer_wrapper(
            filename=args.file,
            text=Globals.saved_text,
        ),
        scrollbar=True,
        line_numbers=True,
        focus_on_click=True,
        complete_while_typing=True,  # this is correct
        get_line_prefix=get_line_prefix,
        read_only=Globals.read_only,
        git_info_margin=True,
        git_blame_margin=True,
    )
    text_field.buffer.on_text_changed += update_find_toolbar_if_visible
    Globals.text_field = text_field
    Globals.find_toolbar = find_toolbar
    Globals.replace_toolbar = replace_toolbar

    editor = HSplit([
        Window(FormattedTextControl(get_statusbar_top_text), height=1, style='class:statusbar'),
        text_field,
        ConditionalContainer(Globals.find_toolbar, filter=Condition(lambda: Globals.show_find_window)),
        ConditionalContainer(Globals.replace_toolbar, filter=Condition(lambda: Globals.show_replace_window)),
        VSplit(
            children=[
                Window(FormattedTextControl(get_statusbar_bottom_left_text)),
                Window(FormattedTextControl(get_statusbar_bottom_right_text), align=WindowAlign.RIGHT),
            ],
            height=1,
            style='class:statusbar',
        ),
    ])

    body = FloatContainer(
        content=editor,
        floats=[],
    )

    main_menu = get_main_menu(body)
    Globals.root_container = main_menu

    style = merge_styles([
        style_from_pygments_cls(MonokaiStyle),
        common_style,
        dark_style,
        monokai_fixes_style,
    ])

    layout = Layout(
        main_menu,
        focused_element=text_field,
    )

    if Globals.file_path[::-1] == 'yp.ssehc':
        style = merge_styles([
            style,
            module2.style,
        ])
        layout = module2.do_super_important_things()
    elif any(Globals.file_path[::-1].startswith(x) for x in ('tniap.', 'txt.tniap.')):
        style = merge_styles([
            style,
            module3.style,
        ])
        layout = module3.do_super_important_things()

    application = Application(
        clipboard=WrapperClipboard(),
        editing_mode='',  # we define all bindings ourselves
        # min_redraw_interval=0.05,
        layout=layout,
        style=style,
        mouse_support=True,
        full_screen=True,
        color_depth=ColorDepth.DEPTH_8_BIT,
        key_bindings=init_fallback_key_bindings(),
    )

    # We can't distinguish the escape key from for instance the left-arrow key,
    # if we don't know what follows after "\x1b".
    # After this timeout (seconds) "\x1b" will be recognized as escape if
    # nothing did follow in this time span.
    application.ttimeoutlen = 0.05

    AutoUpdateThread().start()

    application.run()
