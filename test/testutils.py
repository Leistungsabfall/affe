from globals import Globals
from prompt_toolkit.widgets import TextArea

from toolbars.find import find_toolbar
from toolbars.replace import replace_toolbar


def init_text_field(text, cursor_position):
    Globals.text_field = TextArea(text=text)
    Globals.text_field.buffer.cursor_position = cursor_position


def init_find_toolbar(text, cursor_position):
    Globals.find_toolbar_text_field = TextArea(text=text)
    Globals.find_toolbar_text_field.buffer.cursor_position = cursor_position
    Globals.find_toolbar = find_toolbar


def init_replace_toolbar(text, cursor_position):
    Globals.replace_toolbar_text_field = TextArea(text=text)
    Globals.replace_toolbar_text_field.buffer.cursor_position = cursor_position
    Globals.replace_toolbar = replace_toolbar


@property
def text_field_buffer(_):
    return Globals.text_field.buffer


@property
def find_toolbar_buffer(_):
    return Globals.find_toolbar_text_field.buffer


@property
def replace_toolbar_buffer(_):
    return Globals.replace_toolbar_text_field.buffer


def has_focus(expected, _, actual):
    return actual == expected


class DummyRootContainer:
    window = None


Globals.root_container = DummyRootContainer
