from dialogs.closable_dialog import ClosableDialog
from globals import Globals
from prompt_toolkit import HTML
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.scroll import scroll_forward, scroll_backward
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, D
from prompt_toolkit.widgets import Label, Button, Frame, TextArea
from util.common import Direction


def is_text_field_focused():
    return get_app().layout.has_focus(Globals.text_field)


def is_find_and_replace_toolbar_focused():
    return get_app().layout.has_focus(Globals.find_toolbar) or get_app().layout.has_focus(Globals.replace_toolbar)


def is_find_toolbar_focused():
    return get_app().layout.has_focus(Globals.find_toolbar)


def is_replace_toolbar_focused():
    return get_app().layout.has_focus(Globals.replace_toolbar)


def is_menu_focused():
    return get_app().layout.has_focus(Globals.root_container.window)


def show_message(title, text, toggle_interval=0.0):
    start_text = text if type(text) == str else text[0]
    dialog = ClosableDialog(
        toggle_texts=text,
        toggle_interval=toggle_interval,
        title=title,
        body=HSplit([
            Label(text=start_text),
        ]),
        buttons=[
            Button(text='Close', handler=lambda: dialog.close()),
        ],
        width=D(preferred=80),
        modal=True,
    )
    dialog.show()


def show_scrollable_dialog(title, text, lexer=None):
    def add_key_bindings():
        @bindings.add(Keys.Enter)
        @bindings.add('space')
        @bindings.add(Keys.Escape)
        @bindings.add(Keys.Backspace)
        def _(event):
            dialog.close()

        @bindings.add(Keys.PageDown)
        def _(event):
            scroll_forward(event)

        @bindings.add(Keys.PageUp)
        def _(event):
            scroll_backward(event)

        @bindings.add(Keys.Down)
        def _(event):
            get_app().current_buffer.cursor_down(1)

        @bindings.add(Keys.Up)
        def _(event):
            get_app().current_buffer.cursor_up(1)

    bindings = KeyBindings()
    add_key_bindings()

    text_area = TextArea(
        text=text,
        width=D(preferred=1000),
        height=D(preferred=1000),
        scrollbar=True,
        read_only=True,
        lexer=lexer,
    )
    dialog = ClosableDialog(
        title=title,
        body=Frame(
            body=HSplit(
                children=[
                    text_area,
                    Button(text='Close', handler=lambda: dialog.close()),
                ],
            ),
            key_bindings=bindings,
        ),
    )
    dialog.show()


def walk_through_find_and_replace_toolbar(direction):
    directions = (Direction.Left, Direction.Right)
    if direction not in directions:
        raise ValueError('Only the following directions are supported: {}'.format(directions))

    if is_find_toolbar_focused():
        if direction == Direction.Right:
            if get_app().layout.has_focus(Globals.find_toolbar_text_field):
                if Globals.show_replace_window:
                    get_app().layout.focus(Globals.replace_toolbar_text_field)
                else:
                    get_app().layout.focus(Globals.find_toolbar_up_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_up_button):
                get_app().layout.focus(Globals.find_toolbar_down_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_down_button):
                get_app().layout.focus(Globals.find_toolbar_match_case_checkbox)
            elif get_app().layout.has_focus(Globals.find_toolbar_match_case_checkbox):
                get_app().layout.focus(Globals.find_toolbar_close_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_close_button):
                if Globals.show_replace_window:
                    get_app().layout.focus(Globals.replace_toolbar_replace_button)
                else:
                    get_app().layout.focus(Globals.find_toolbar_text_field)
            else:
                raise NotImplementedError

        elif direction == Direction.Left:
            if get_app().layout.has_focus(Globals.find_toolbar_text_field):
                if Globals.show_replace_window:
                    get_app().layout.focus(Globals.replace_toolbar_replace_all_button)
                else:
                    get_app().layout.focus(Globals.find_toolbar_close_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_up_button):
                if Globals.show_replace_window:
                    get_app().layout.focus(Globals.replace_toolbar_text_field)
                else:
                    get_app().layout.focus(Globals.find_toolbar_text_field)
            elif get_app().layout.has_focus(Globals.find_toolbar_down_button):
                get_app().layout.focus(Globals.find_toolbar_up_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_match_case_checkbox):
                get_app().layout.focus(Globals.find_toolbar_down_button)
            elif get_app().layout.has_focus(Globals.find_toolbar_close_button):
                get_app().layout.focus(Globals.find_toolbar_match_case_checkbox)
            else:
                raise NotImplementedError

    elif is_replace_toolbar_focused():
        if direction == Direction.Right:
            if get_app().layout.has_focus(Globals.replace_toolbar_text_field):
                get_app().layout.focus(Globals.find_toolbar_up_button)
            elif get_app().layout.has_focus(Globals.replace_toolbar_replace_button):
                get_app().layout.focus(Globals.replace_toolbar_replace_all_button)
            elif get_app().layout.has_focus(Globals.replace_toolbar_replace_all_button):
                get_app().layout.focus(Globals.find_toolbar_text_field)
            else:
                raise NotImplementedError

        elif direction == Direction.Left:
            if get_app().layout.has_focus(Globals.replace_toolbar_text_field):
                get_app().layout.focus(Globals.find_toolbar_text_field)
            elif get_app().layout.has_focus(Globals.replace_toolbar_replace_button):
                get_app().layout.focus(Globals.find_toolbar_close_button)
            elif get_app().layout.has_focus(Globals.replace_toolbar_replace_all_button):
                get_app().layout.focus(Globals.replace_toolbar_replace_button)
            else:
                raise NotImplementedError

    else:
        raise ValueError('"Find and replace" toolbar has to be focused')


def update_find_toolbar_if_visible(*args, **kwargs):
    if Globals.show_find_window:
        from handlers.actions import handle_on_find_toolbar_input_changed
        handle_on_find_toolbar_input_changed(move_cursor=False)


def get_find_and_replace_toolbar_key_bindings():
    def add_key_bindings():
        @bindings.add(Keys.Escape)
        def _(event):
            from toolbars.find import close_find_and_replace_toolbar
            close_find_and_replace_toolbar()

        @bindings.add(Keys.F2)
        def _(event):
            from util.text_helper import move_cursor_to_next_match
            move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True)

        @bindings.add(Keys.F3)
        def _(event):
            from util.text_helper import move_cursor_to_next_match
            move_cursor_to_next_match(keep_position_if_on_cursor=False)

        @bindings.add(Keys.F4)
        def _(event):
            from util.text_helper import replace_match
            replace_match()

        @bindings.add(Keys.F5)
        def _(event):
            from util.text_helper import replace_match
            replace_match(replace_all=True)

    bindings = KeyBindings()
    add_key_bindings()
    return bindings


def get_line_prefix(lineno, wrap_count):
    try:
        git_status = Globals.git_status_by_line[lineno]
        if 'deleted' in git_status.value and (lineno == 0 or wrap_count > 0):
            return HTML('<git-deleted>█</git-deleted> ')
        return git_status
    except KeyError:
        return '  '
