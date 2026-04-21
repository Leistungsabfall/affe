import re

from globals import Globals
from prompt_toolkit.application import get_app
from prompt_toolkit.selection import SelectionType
from util.common import special_char_mapping, Direction, closing_special_chars, opening_special_chars, \
    opening_and_closing_special_chars
from util.gui_helper import update_find_toolbar_if_visible
from util.super_important_modules.module1 import do_super_important_things


def type_text(text, cursor_position_offset=0):
    get_app().current_buffer.cut_selection()
    get_app().current_buffer.insert_text(text)
    get_app().current_buffer.cursor_position += cursor_position_offset


def remove_text_before_cursor(count):
    get_app().current_buffer.cut_selection()
    get_app().current_buffer.delete_before_cursor(count)


def remove_text_after_cursor(count):
    get_app().current_buffer.cut_selection()
    get_app().current_buffer.delete(count)


def get_text_before_cursor(count):
    cursor_position = Globals.text_field.document.cursor_position
    return Globals.text_field.text[cursor_position-count:cursor_position]


def get_text_after_cursor(count):
    cursor_position = Globals.text_field.document.cursor_position
    return Globals.text_field.text[cursor_position:cursor_position+count]


def get_char_before_cursor():
    return get_text_before_cursor(1)


def get_char_after_cursor():
    return get_text_after_cursor(1)


def get_line_until_cursor():
    cursor_position = Globals.text_field.document.cursor_position
    return Globals.text_field.text[:cursor_position].rsplit('\n', maxsplit=1)[-1]


def get_spaces_before_cursor():
    line_until_cursor = get_line_until_cursor()
    return len(line_until_cursor) - len(line_until_cursor.rstrip(' '))


def get_line_after_cursor():
    cursor_position = Globals.text_field.document.cursor_position
    return Globals.text_field.text[cursor_position:].split('\n', maxsplit=1)[0]


def get_spaces_after_cursor():
    line_after_cursor = get_line_after_cursor()
    return len(line_after_cursor) - len(line_after_cursor.lstrip(' '))


def get_leading_spaces_until_cursor():
    line_until_cursor = get_line_until_cursor()
    return len(line_until_cursor) - len(line_until_cursor.lstrip(' '))


def is_autocompletion_active():
    return Globals.text_field.buffer.complete_state is not None


def move_cursor(direction: Direction):
    def move_cursor_left():
        buffer.cursor_position -= 1

    def move_cursor_right():
        buffer.cursor_position += 1

    buffer = get_app().current_buffer
    if direction == Direction.Down:
        buffer.cursor_down(1)
    elif direction == Direction.Up:
        buffer.cursor_up(1)
    elif direction == Direction.Left:
        move_cursor_left()
    elif direction == Direction.Right:
        move_cursor_right()
    else:
        raise ValueError('Unknown direction: {}'.format(direction))


def start_or_extend_selection(direction: Direction):
    buffer = get_app().current_buffer
    if has_selection():
        move_cursor(direction)
        if buffer.selection_state.original_cursor_position == buffer.cursor_position:
            buffer.exit_selection()
    else:
        if len(buffer.text) > 0:
            buffer.start_selection(selection_type=SelectionType.CHARACTERS)
        move_cursor(direction)


def has_selection():
    return bool(get_app().current_buffer.selection_state)


def get_word_under_cursor():
    def char_under_cursor_is_alpha():
        return re.match(r'\w', buffer.document.current_char)

    def get_alpha_chars_before_cursor():
        if not char_under_cursor_is_alpha() and not get_selected_text():
            return ''
        return re.split(r'\W+', buffer.document.current_line_before_cursor)[-1]

    def get_alpha_chars_after_cursor():
        return re.split(r'\W+', buffer.document.current_line_after_cursor)[0]

    buffer = Globals.text_field.buffer
    word_under_cursor = get_alpha_chars_before_cursor() + get_alpha_chars_after_cursor()
    return word_under_cursor


def get_selected_text():
    clipboard_data = Globals.text_field.buffer.copy_selection()
    return clipboard_data.text


def in_between_matching_special_chars():
    try:
        return special_char_mapping[get_char_before_cursor()] == get_char_after_cursor()
    except KeyError:
        return False


def add_special_chars_pair(opening_special_char):
    closing_special_char = special_char_mapping[opening_special_char]
    special_char_pair = opening_special_char+closing_special_char
    type_text(
        text=special_char_pair,
        cursor_position_offset=-1,
    )


def is_special_char(char):
    return char in special_char_mapping.keys() or char in special_char_mapping.values()


def is_opening_special_char(char):
    return char in opening_special_chars


def is_opening_and_closing_special_char(char):
    return char in opening_and_closing_special_chars


def is_closing_special_char(char):
    return char in closing_special_chars


def is_space(string):
    return all(char.isspace() or char == '' for char in string)


def is_cursor_surrounded_by_spaces():
    return is_space(get_char_before_cursor()) and is_space(get_char_after_cursor())


def is_cursor_surrounded_by_matching_special_chars():
    try:
        return special_char_mapping[get_char_before_cursor()] == get_char_after_cursor()
    except KeyError:
        return False


def char_after_cursor_is_matching_closing_special_char(char):
    return special_char_mapping[char] == get_char_after_cursor()


def move_cursor_to_start_of_line():
    buffer = get_app().current_buffer
    buffer.cursor_position += buffer.document.get_start_of_line_position()


def move_cursor_to_end_of_line():
    buffer = get_app().current_buffer
    buffer.cursor_position += buffer.document.get_end_of_line_position()


def get_start_cursor_position_of_selection():
    return get_app().current_buffer.document.selection.original_cursor_position


def get_end_cursor_position_of_selection():
    return get_app().current_buffer.cursor_position


def get_start_line_index_of_selection():
    buffer = get_app().current_buffer
    cursor_position_start = get_start_cursor_position_of_selection()
    cursor_position_end = get_end_cursor_position_of_selection()
    return min(
        buffer.document.translate_index_to_position(cursor_position_start)[0],
        buffer.document.translate_index_to_position(cursor_position_end)[0],
    )


def get_end_line_index_of_selection():
    buffer = get_app().current_buffer
    cursor_position_start = get_start_cursor_position_of_selection()
    cursor_position_end = get_end_cursor_position_of_selection()
    return max(
        buffer.document.translate_index_to_position(cursor_position_start)[0],
        buffer.document.translate_index_to_position(cursor_position_end)[0],
    )


def get_current_indentation():
    return len(get_app().current_buffer.document.leading_whitespace_in_current_line)


def get_indentation_for_line(line):
    length = len(line) - len(line.lstrip())
    return len(line[:length])


def move_lines(direction):
    def swap_lines():
        lines[index+offset], lines[index] = lines[index], lines[index+offset]

    buffer = Globals.text_field.buffer
    line_index = buffer.document.cursor_position_row
    index_in_line = buffer.document.cursor_position_col
    lines = list(buffer.document.lines)
    keep_selection = False

    if has_selection():
        keep_selection = True
        cursor_position_start = get_start_cursor_position_of_selection()
        line_index_start = get_start_line_index_of_selection()
        line_index_end = get_end_line_index_of_selection()
    else:
        line_index_start = line_index_end = line_index

    if direction == Direction.Up:
        if line_index_start == 0:
            return

        offset = -1
        for index in range(line_index_start, line_index_end+1):
            swap_lines()

    elif direction == Direction.Down:
        if line_index_end == len(lines) - 1:
            return

        offset = +1
        for index in range(line_index_end, line_index_start-1, -1):
            swap_lines()

    else:
        directions = ', '.join((Direction.Up, Direction.Down))
        raise ValueError('Only the following directions are supported: {}'.format(directions))

    if keep_selection:
        selection_line_index, selection_index_in_line = \
            buffer.document.translate_index_to_position(cursor_position_start)

    buffer.text = '\n'.join(lines)

    new_cursor_position = buffer.document.translate_row_col_to_index(
        line_index + offset,
        index_in_line,
    )

    if keep_selection:
        buffer.cursor_position = buffer.document.translate_row_col_to_index(
            selection_line_index + offset,
            selection_index_in_line,
        )
        buffer.start_selection(selection_type=SelectionType.CHARACTERS)
    buffer.cursor_position = new_cursor_position


def move_cursor_to_next_match(keep_position_if_on_cursor, backwards=False):
    def get_rel_pos_of_next_match(from_start=False):
        match_case = Globals.find_toolbar_match_case_checkbox.checked
        if backwards:
            return Globals.text_field.document.find_backwards(
                search_string,
                ignore_case=not match_case,
            )
        return Globals.text_field.document.find(
            search_string,
            include_current_position=keep_position_if_on_cursor or from_start,
            ignore_case=not match_case,
        )

    Globals.text_field.buffer.exit_selection()
    search_string = Globals.find_toolbar_text_field.buffer.text
    match = get_rel_pos_of_next_match()
    if match is None:
        old_cursor_position = Globals.text_field.buffer.cursor_position
        if backwards:
            Globals.text_field.buffer.cursor_position = len(Globals.text_field.text)
        else:
            Globals.text_field.buffer.cursor_position = 0
        match = get_rel_pos_of_next_match(from_start=True)
        if match is None:
            Globals.text_field.buffer.cursor_position = old_cursor_position
            return False

    Globals.text_field.buffer.cursor_position += match
    return True


def replace_match(replace_all=False):
    def replace_all_matches():
        match_case = Globals.find_toolbar_match_case_checkbox.checked
        if match_case:
            flags = 0
        else:
            flags = re.IGNORECASE

        Globals.text_field.buffer.text = re.sub(
            re.escape(find_text),
            replace_text,
            Globals.text_field.buffer.text,
            flags=flags,
        )

    def replace_current_match():
        Globals.text_field.buffer.on_text_changed -= update_find_toolbar_if_visible
        Globals.text_field.buffer.start_selection()
        Globals.text_field.buffer.cursor_position += len(find_text)
        Globals.text_field.buffer.cut_selection()
        update_find_toolbar_if_visible()
        Globals.text_field.buffer.on_text_changed += update_find_toolbar_if_visible
        Globals.text_field.buffer.insert_text(replace_text)
        move_cursor_to_next_match(keep_position_if_on_cursor=True)

    find_text = Globals.find_toolbar_text_field.text
    replace_text = Globals.replace_toolbar_text_field.text

    if find_text == replace_text and get_find_matches() and Globals.find_toolbar_match_case_checkbox.checked:
        do_super_important_things()
        return

    if not move_cursor_to_next_match(keep_position_if_on_cursor=True):
        return

    if replace_all:
        replace_all_matches()
    else:
        replace_current_match()


def get_find_matches():
    text = Globals.find_toolbar_text_field.text

    if not text:
        return 0

    match_case = Globals.find_toolbar_match_case_checkbox.checked
    if match_case:
        flags = 0
    else:
        flags = re.IGNORECASE

    return len(tuple(re.finditer(re.escape(text), Globals.text_field.buffer.text, flags=flags)))


def has_next_line():
    document = get_app().current_buffer.document
    return document.line_count - 1 > document.cursor_position_row


def indent_selection():
    buffer = get_app().current_buffer

    cursor_position_start = get_start_cursor_position_of_selection()
    cursor_position_end = get_end_cursor_position_of_selection()

    line_index_start = get_start_line_index_of_selection()
    line_index_end = get_end_line_index_of_selection()

    lines = list(buffer.document.lines)

    for i in range(line_index_start, line_index_end+1):
        lines[i] = '    ' + lines[i]
    buffer.text = '\n'.join(lines)

    new_cursor_position_start = buffer.document.translate_row_col_to_index(line_index_start, 0)
    new_cursor_position_end = buffer.document.translate_row_col_to_index(line_index_end, len(lines[line_index_end]))

    if cursor_position_start < cursor_position_end:
        buffer.cursor_position = new_cursor_position_start
        buffer.start_selection()
        buffer.cursor_position = new_cursor_position_end
    else:
        buffer.cursor_position = new_cursor_position_end
        buffer.start_selection()
        buffer.cursor_position = new_cursor_position_start


def unindent_selection():
    buffer = get_app().current_buffer

    cursor_position_start = get_start_cursor_position_of_selection()
    cursor_position_end = get_end_cursor_position_of_selection()

    line_index_start = get_start_line_index_of_selection()
    line_index_end = get_end_line_index_of_selection()

    lines = list(buffer.document.lines)

    spaces_to_remove = min(
        4,
        min(
            get_indentation_for_line(lines[i])
            for i in range(line_index_start, line_index_end + 1)
            if len(lines[i]) > 0
        )
    )

    for i in range(line_index_start, line_index_end+1):
        lines[i] = lines[i][spaces_to_remove:]
    buffer.text = '\n'.join(lines)

    new_cursor_position_start = buffer.document.translate_row_col_to_index(line_index_start, 0)
    new_cursor_position_end = buffer.document.translate_row_col_to_index(line_index_end, len(lines[line_index_end]))

    if cursor_position_start < cursor_position_end:
        buffer.cursor_position = new_cursor_position_start
        if new_cursor_position_end != new_cursor_position_start:
            buffer.start_selection()
            buffer.cursor_position = new_cursor_position_end
    else:
        buffer.cursor_position = new_cursor_position_end
        if new_cursor_position_end != new_cursor_position_start:
            buffer.start_selection()
            buffer.cursor_position = new_cursor_position_start


def get_autocomplete_suggestions(prefix):
    def exclude_duplicates():
        return list(set(words))

    def filter_possible_matches():
        return [
            word for word in words
            if len(word) > 1
            and word != word_under_cursor
            and word != prefix
            and (word[0].isalpha() or (word[0] == '_' and any(c.isalpha() for c in word)))
        ]

    def sort_case_insensitive(iterable):
        return sorted(iterable, key=lambda key: key.lower())

    def fuzzy_match(word):
        if len(prefix) > len(word):
            return False
        matches = 0
        needed_matches = len(prefix)
        for char_prefix in prefix.lower():
            for index, char_word in enumerate(word.lower()):
                if char_word == char_prefix:
                    word = word[index + 1:]
                    matches += 1
                    break
        return matches == needed_matches

    text = re.sub(r'\W+', '\n', Globals.text_field.text)
    word_under_cursor = get_word_under_cursor()
    words = text.split('\n')
    words = exclude_duplicates()
    words = filter_possible_matches()

    words_with_prefix_case_sensitive = []
    for word in words[:]:  # deepcopy words since we don't want to manipulate the original list while iterating
        if prefix and word.startswith(prefix):  # if prefix => if no prefix, sort case insensitive (next block)
            words.remove(word)
            words_with_prefix_case_sensitive.append(word)
    words_with_prefix_case_sensitive = sort_case_insensitive(words_with_prefix_case_sensitive)

    words_with_prefix_case_insensitive = []
    for word in words[:]:  # deepcopy words since we don't want to manipulate the original list while iterating
        if word.lower().startswith(prefix.lower()):
            words.remove(word)
            words_with_prefix_case_insensitive.append(word)
    words_with_prefix_case_insensitive = sort_case_insensitive(words_with_prefix_case_insensitive)

    words_with_fuzzy_match = []
    for word in words[:]:  # deepcopy words since we don't want to manipulate the original list while iterating
        if fuzzy_match(word):
            words.remove(word)
            words_with_fuzzy_match.append(word)
    words_with_fuzzy_match = sort_case_insensitive(words_with_fuzzy_match)

    words = words_with_prefix_case_sensitive + words_with_prefix_case_insensitive + words_with_fuzzy_match
    return words


def select_next_word(direction):
    def is_alpha(char):
        return re.match(r'\w+', char)

    buffer = get_app().current_buffer
    if direction == Direction.Left:
        if buffer.cursor_position == 0:
            return
        initial_char = buffer.text[max(0, buffer.cursor_position - 1)]
        while True:
            if buffer.cursor_position <= 1:
                buffer.cursor_position = 0
                return
            buffer.cursor_position -= 1
            if is_alpha(initial_char) and not is_alpha(buffer.text[buffer.cursor_position-1]):
                return
            if not is_alpha(initial_char) and is_alpha(buffer.text[buffer.cursor_position-1]):
                return

    elif direction == Direction.Right:
        if buffer.cursor_position == len(buffer.text):
            return
        initial_char = buffer.text[buffer.cursor_position]
        while True:
            if buffer.cursor_position >= len(buffer.text) - 1:
                buffer.cursor_position = len(buffer.text)
                return
            buffer.cursor_position += 1
            if is_alpha(initial_char) and not is_alpha(buffer.text[buffer.cursor_position]):
                return
            if not is_alpha(initial_char) and is_alpha(buffer.text[buffer.cursor_position]):
                return
    else:
        directions = ', '.join((Direction.Up, Direction.Down))
        raise ValueError('Only the following directions are supported: {}'.format(directions))
