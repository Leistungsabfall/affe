from globals import Globals
from handlers.actions import handle_on_find_toolbar_input_changed
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import VSplit, HorizontalAlign, D
from prompt_toolkit.widgets import Label, TextArea, Button, Checkbox, Frame
from util.gui_helper import get_find_and_replace_toolbar_key_bindings
from util.text_helper import move_cursor_to_next_match


def close_find_and_replace_toolbar():
    def select_nearest_match():
        Globals.text_field.buffer.cursor_position += match + len(search_text)
        Globals.text_field.buffer.start_selection()
        Globals.text_field.buffer.cursor_position -= len(search_text)

    match_case = Globals.find_toolbar_match_case_checkbox.checked
    search_text = Globals.find_toolbar_text_field.buffer.text
    match = Globals.text_field.document.find(
        search_text,
        include_current_position=True,
        ignore_case=not match_case,
    )
    if match is not None:
        select_nearest_match()
    get_app().layout.focus(Globals.text_field)
    Globals.show_find_window = False
    Globals.show_replace_window = False


def __match_case_callback(checked):
    handle_on_find_toolbar_input_changed()


Globals.find_toolbar_text_field = TextArea(
    focus_on_click=True,
    style='class:find-and-replace-textfield',
    width=D(preferred=1000),
)
Globals.find_toolbar_text_field.buffer.on_text_changed += handle_on_find_toolbar_input_changed
Globals.find_toolbar_up_button = Button(
    'Up (F2)',
    handler=lambda: move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True),
)
Globals.find_toolbar_down_button = Button(
    'Down (F3)',
    handler=lambda: move_cursor_to_next_match(keep_position_if_on_cursor=False),
)
Globals.find_toolbar_match_case_checkbox = Checkbox('Match Case', callback=__match_case_callback)
Globals.find_toolbar_close_button = Button('Close (Esc)', handler=close_find_and_replace_toolbar)

find_toolbar = Frame(
    style='class:find-and-replace-toolbar',
    body=VSplit(
        align=HorizontalAlign.LEFT,
        children=[
            Label('Find:    ', dont_extend_width=True),
            Globals.find_toolbar_text_field,
            Label(' ', dont_extend_width=True),
            Globals.find_toolbar_up_button,
            Label(' ', dont_extend_width=True),
            Globals.find_toolbar_down_button,
            Label(' ', dont_extend_width=True),
            Globals.find_toolbar_match_case_checkbox,
            Label(' ', dont_extend_width=True),
            Globals.find_toolbar_close_button,
        ],
        key_bindings=get_find_and_replace_toolbar_key_bindings(),
    )
)
