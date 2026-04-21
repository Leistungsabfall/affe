from globals import Globals
from prompt_toolkit.layout import VSplit, HorizontalAlign, D
from prompt_toolkit.widgets import Label, TextArea, Button, Frame
from util.gui_helper import get_find_and_replace_toolbar_key_bindings
from util.text_helper import replace_match

Globals.replace_toolbar_text_field = TextArea(
    focus_on_click=True,
    style='class:find-and-replace-textfield',
    width=D(preferred=1000),
)
Globals.replace_toolbar_replace_button = Button(
    'Replace (F4)',
    handler=replace_match,
)
Globals.replace_toolbar_replace_all_button = Button(
    'Replace All (F5)',
    handler=lambda: replace_match(replace_all=True),
)

replace_toolbar = Frame(
    style='class:find-and-replace-toolbar',
    body=VSplit(
        align=HorizontalAlign.LEFT,
        children=[
            Label('Replace: ', dont_extend_width=True),
            Globals.replace_toolbar_text_field,
            Label(' ', dont_extend_width=True),
            Globals.replace_toolbar_replace_button,
            Label(' ', dont_extend_width=True),
            Globals.replace_toolbar_replace_all_button,
        ],
        key_bindings=get_find_and_replace_toolbar_key_bindings(),
    )
)
