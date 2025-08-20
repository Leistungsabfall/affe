import re

from globals import Globals
from util import text_helper


def get_statusbar_bottom_left_text():
    text = ' Esc = Exit | F7 = Menu | F12 = Readme'

    fragments = []
    fragments.append(('class:statusbar', text))
    return fragments


def get_statusbar_bottom_right_text():
    def cursor_is_on_match(text, match_case):
        document = text_helper.get_text_after_cursor(len(text))
        if match_case:
            return text == document
        return text.lower() == document.lower()

    def get_current_match(text, match_case):
        cursor_position = Globals.text_field.buffer.cursor_position
        text_until_cursor = Globals.text_field.buffer.text[:cursor_position]
        if match_case:
            return text_until_cursor.count(text) + 1
        return text_until_cursor.lower().count(text.lower()) + 1

    def get_info_about_current_search():
        text = Globals.find_toolbar_text_field.text

        if len(text) == 0:
            return ''

        match_case = Globals.find_toolbar_match_case_checkbox.checked
        if match_case:
            flags = 0
        else:
            flags = re.IGNORECASE

        matches = len(tuple(re.finditer(re.escape(text), Globals.text_field.buffer.text, flags=flags)))
        if matches == 0:
            return '(no matches)'
        if not cursor_is_on_match(text, match_case):
            if matches == 1:
                return '(1 match)'.format(matches)
            return '({} matches)'.format(matches)
        return '(match {} of {})'.format(get_current_match(text, match_case), matches)

    def get_info_about_selected_text():
        selected_text = text_helper.get_selected_text()
        if not selected_text:
            return ''

        lines_count = selected_text.count('\n') + 1
        text = '(selected chars: {}, lines: {})'.format(
            len(selected_text),
            lines_count,
        )
        return text

    return '{} {}:{} '.format(
        get_info_about_current_search() if Globals.show_find_window else get_info_about_selected_text(),
        str(Globals.text_field.document.cursor_position_row + 1).rjust(4+1),
        str(Globals.text_field.document.cursor_position_col + 1).ljust(2+1),
    )
