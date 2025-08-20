from completers.fuzzy_word_completer import FuzzyWordCompleter
from globals import Globals
from prompt_toolkit.application import get_app
from prompt_toolkit.clipboard import ClipboardData
from prompt_toolkit.selection import SelectionType
from util.common import Direction
from util.gui_helper import is_text_field_focused, is_find_and_replace_toolbar_focused, is_menu_focused, \
    is_find_toolbar_focused, is_replace_toolbar_focused, walk_through_find_and_replace_toolbar
from util.text_helper import type_text, is_closing_special_char, char_after_cursor_is_matching_closing_special_char, \
    add_special_chars_pair, is_space, is_cursor_surrounded_by_matching_special_chars, is_opening_special_char, \
    get_char_after_cursor, is_opening_and_closing_special_char, is_cursor_surrounded_by_spaces, \
    get_spaces_after_cursor, get_leading_spaces_until_cursor, is_autocompletion_active, get_spaces_before_cursor, \
    remove_text_before_cursor, remove_text_after_cursor, in_between_matching_special_chars, has_selection, \
    move_cursor, start_or_extend_selection, move_cursor_to_end_of_line, move_cursor_to_start_of_line, move_lines, \
    move_cursor_to_next_match, replace_match, get_selected_text, has_next_line, get_start_line_index_of_selection, \
    get_end_line_index_of_selection, get_current_indentation, get_indentation_for_line, \
    get_end_cursor_position_of_selection, get_start_cursor_position_of_selection, indent_selection, \
    unindent_selection, select_next_word


def handle_char(char):
    if is_find_and_replace_toolbar_focused():
        type_text(char)
        return

    if not is_text_field_focused():
        return

    char_after_cursor = get_char_after_cursor()
    if is_opening_and_closing_special_char(char) and is_cursor_surrounded_by_spaces():
        add_special_chars_pair(char)
        return

    if is_opening_special_char(char):
        if is_space(char_after_cursor) or is_cursor_surrounded_by_matching_special_chars():
            add_special_chars_pair(char)
            return

        if is_closing_special_char(char_after_cursor) and not char_after_cursor_is_matching_closing_special_char(char):
            add_special_chars_pair(char)
            return

    if (is_closing_special_char(char) or is_opening_and_closing_special_char(char)) \
            and char_after_cursor == char:
        handle_arrow(Direction.Right)
        return

    type_text(char)


def handle_enter():
    if is_find_toolbar_focused():
        if not Globals.find_toolbar_text_field.text:
            return
        if not move_cursor_to_next_match(keep_position_if_on_cursor=False):
            pass  # text not found
        return
    if is_replace_toolbar_focused():
        replace_match()
        return

    if is_autocompletion_active():
        Globals.text_field.buffer.complete_state = None
        FuzzyWordCompleter.completion_active = False
        return

    if has_selection():
        Globals.text_field.buffer.cut_selection()
        Globals.text_field.buffer.newline()
        return

    spaces_after_cursor = get_spaces_after_cursor()
    if not spaces_after_cursor and not in_between_matching_special_chars():
        Globals.text_field.buffer.newline()
        return

    text = '\n'
    cursor_position_offset = 0
    if spaces_after_cursor:
        text += ' '*get_leading_spaces_until_cursor()
        cursor_position_offset += 0
    if in_between_matching_special_chars():
        current_indentation = get_leading_spaces_until_cursor()
        text += ' '*(current_indentation + 4) + '\n' + ' '*current_indentation
        cursor_position_offset += -1*(current_indentation+1)

    type_text(text, cursor_position_offset)


def handle_jump_to_new_line():
    if not is_text_field_focused():
        return

    move_cursor_to_end_of_line()

    current_indentation = get_leading_spaces_until_cursor()
    text = '\n' + ' '*current_indentation
    type_text(text)


def handle_tab():
    if is_find_and_replace_toolbar_focused():
        walk_through_find_and_replace_toolbar(Direction.Right)
        return

    if not is_text_field_focused():
        return

    if is_autocompletion_active():
        get_app().current_buffer.auto_down()
        return

    if has_selection():
        indent_selection()
        return

    type_text('    ')


def handle_backtab():
    if is_find_and_replace_toolbar_focused():
        walk_through_find_and_replace_toolbar(Direction.Left)
        return

    if not is_text_field_focused():
        return

    if is_autocompletion_active():
        get_app().current_buffer.auto_up()
        return

    if has_selection():
        unindent_selection()
        return

    spaces_before_cursor = get_spaces_before_cursor()
    spaces_after_cursor = get_spaces_after_cursor()
    spaces_leading = get_leading_spaces_until_cursor()

    if spaces_before_cursor > 0:
        mod = spaces_before_cursor % 4
        spaces_to_remove = mod if mod > 0 else 4
        remove_text_before_cursor(spaces_to_remove)
    elif spaces_after_cursor > 0:
        mod = spaces_after_cursor % 4
        spaces_to_remove = 4 if spaces_after_cursor >= 4 else mod
        remove_text_after_cursor(spaces_to_remove)
    elif spaces_leading:
        mod = spaces_leading % 4
        spaces_to_remove = mod if mod > 0 else 4
        cursor_position = get_app().current_buffer.cursor_position
        cursor_position_in_line = get_app().current_buffer.document.translate_index_to_position(cursor_position)[1]
        move_cursor_to_start_of_line()
        remove_text_after_cursor(spaces_to_remove)
        get_app().current_buffer.cursor_position += cursor_position_in_line - spaces_to_remove


def handle_autocomplete():
    if not is_text_field_focused():
        return

    buffer = Globals.text_field.buffer
    if is_autocompletion_active():
        buffer.complete_next()
    else:
        buffer.start_completion(select_first=False)


def handle_backspace():
    if is_find_and_replace_toolbar_focused():
        remove_text_before_cursor(1)
        return

    if not is_text_field_focused():
        return

    if has_selection():
        Globals.text_field.buffer.cut_selection()
        return

    if in_between_matching_special_chars():
        remove_text_before_cursor(1)
        remove_text_after_cursor(1)
        return

    spaces_before_cursor = get_spaces_before_cursor()
    if is_space(Globals.text_field.document.current_line) and spaces_before_cursor > 0:
        mod = spaces_before_cursor % 4
        spaces_to_remove = mod if mod > 0 else 4
        remove_text_before_cursor(spaces_to_remove)
    else:
        remove_text_before_cursor(1)


def handle_delete():
    if is_menu_focused():
        return

    if has_selection():
        Globals.text_field.buffer.cut_selection()
        return

    remove_text_after_cursor(1)


def handle_arrow(direction: Direction):
    buffer = get_app().current_buffer
    if is_autocompletion_active():
        if direction == Direction.Up:
            buffer.complete_previous()
            return
        elif direction == Direction.Down:
            buffer.complete_next()
            return

    if has_selection():
        # mimics behaviour of other text editors:
        # jump to start/end of selection when exiting the selection by moving cursor left/right
        start = get_start_cursor_position_of_selection()
        end = get_end_cursor_position_of_selection()
        if start > end:
            start, end = end, start
        buffer.exit_selection()
        if direction == Direction.Left:
            buffer.cursor_position = start + 1
        if direction == Direction.Right:
            buffer.cursor_position = end - 1

    move_cursor(direction)


def handle_shift_arrow(direction: Direction):
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    start_or_extend_selection(direction)


def handle_cut():
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    buffer = get_app().current_buffer
    if not buffer.text:
        return

    if len(buffer.copy_selection().text) > 0:
        data = buffer.cut_selection()
        get_app().clipboard.set_data(data)
        return

    if len(buffer.document.current_line) == 0:
        data = ClipboardData(text='\n')
        get_app().clipboard.set_data(data)
        buffer.delete(count=1)
        return

    move_cursor_to_start_of_line()
    start_or_extend_selection(Direction.Right)
    move_cursor_to_end_of_line()
    move_cursor(Direction.Right)  # include possible newline char
    data = buffer.cut_selection()
    if len(data.text) > 0:
        get_app().clipboard.set_data(data)


def handle_copy():
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    buffer = get_app().current_buffer
    if not buffer.text:
        return

    data = buffer.copy_selection()
    if len(data.text) > 0:
        get_app().clipboard.set_data(data)
        return

    if len(buffer.document.current_line) == 0:
        return

    move_cursor_to_start_of_line()
    start_or_extend_selection(Direction.Right)
    move_cursor_to_end_of_line()

    if buffer.document.is_cursor_at_the_end:
        buffer.insert_text('\n', move_cursor=False)
        move_cursor_to_start_of_line()
        start_or_extend_selection(Direction.Right)
        move_cursor_to_end_of_line()

    move_cursor(Direction.Right)  # include newline char

    data = buffer.copy_selection()
    if len(data.text) > 0:
        get_app().clipboard.set_data(data)


def handle_paste(text=None):
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    buffer = get_app().current_buffer
    buffer.cut_selection()

    if text is None:
        buffer.paste_clipboard_data(get_app().clipboard.get_data())
        return

    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n')
    buffer.insert_text(text)


def handle_save():
    def already_in_git(index):
        if Globals.git_untracked:
            return False

        if index in Globals.git_status_by_line:
            return False

        return True

    def strip_whitespace_lines():
        stripped_text = []
        for index, line in enumerate(Globals.text_field.text.split('\n')):
            if already_in_git(index):
                stripped_text.append(line)
            else:
                stripped_text.append(line.rstrip())

        Globals.text_field.text = '\n'.join(stripped_text)

    def ensure_newline_at_end():
        last_line_index = len(Globals.text_field.text.split('\n')) - 1
        if Globals.text_field.text and not Globals.text_field.text.endswith('\n') \
                and not already_in_git(last_line_index):
            Globals.text_field.buffer.text += '\n'

    if Globals.read_only:
        return

    Globals.save_in_progress = True
    cursor_position = Globals.text_field.document.cursor_position
    original_cursor_position_row, original_cursor_position_col = \
        Globals.text_field.document.translate_index_to_position(cursor_position)
    strip_whitespace_lines()
    ensure_newline_at_end()
    new_cursor_position = Globals.text_field.document.translate_row_col_to_index(
        original_cursor_position_row, original_cursor_position_col
    )
    Globals.text_field.buffer.cursor_position = new_cursor_position
    with open(Globals.file_path, 'w', encoding='utf-8') as file_:
        file_.write(Globals.text_field.text)
    Globals.saved_text = Globals.text_field.text
    Globals.save_in_progress = False


def handle_select_all():
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    buffer = get_app().current_buffer
    if not buffer.text:
        return
    buffer.cursor_position = 0
    buffer.start_selection()
    buffer.cursor_position = len(buffer.text)


def handle_undo():
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    get_app().current_buffer.undo()


def handle_redo():
    if not is_text_field_focused() and not is_find_and_replace_toolbar_focused():
        return

    get_app().current_buffer.redo()


def handle_home():
    buffer = get_app().current_buffer
    buffer.exit_selection()
    move_cursor_to_start_of_line()


def handle_end():
    buffer = get_app().current_buffer
    buffer.exit_selection()
    move_cursor_to_end_of_line()


def handle_control_home():
    if not is_text_field_focused():
        return

    Globals.text_field.buffer.exit_selection()
    Globals.text_field.buffer.cursor_position = 0


def handle_control_end():
    if not is_text_field_focused():
        return

    Globals.text_field.buffer.exit_selection()
    Globals.text_field.buffer.cursor_position = len(Globals.text_field.text)


def handle_control_arrow(direction):
    if not is_text_field_focused():
        return

    if direction in (Direction.Up, Direction.Down):
        move_lines(direction)
    else:
        select_next_word(direction)


def handle_comment():
    def get_comment_prefix():
        if any(file_path.endswith(ending) for ending in c_style_endings) or file_path.lower().endswith('jenkinsfile'):
            return '//'
        elif any(file_path.endswith(ending) for ending in xml_style_endings):
            return '<!--'
        elif any(file_path.endswith(ending) for ending in latex_style_endings):
            return '%'
        elif any(file_path.endswith(ending) for ending in css_style_endings):
            return '/*'
        elif any(file_path.endswith(ending) for ending in batch_style_endings):
            return 'REM'
        elif any(file_path.endswith(ending) for ending in autohotkey_style_endings):
            return ';'
        return '#'

    def get_comment_suffix():
        if any(file_path.endswith(ending) for ending in xml_style_endings):
            return '-->'
        elif any(file_path.endswith(ending) for ending in css_style_endings):
            return '*/'
        return ''

    def comment_single_line(comment_mode=None):
        def move_cursor_to_next_line():
            move_cursor(Direction.Down)
            move_cursor_to_start_of_line()

        document = buffer.document
        current_line = document.current_line
        current_position_in_line = document.cursor_position_col

        move_cursor_to_start_of_line()
        buffer.cursor_position += current_indentation
        complete_comment_prefix = comment_prefix + ' '
        complete_comment_suffix = ' ' + comment_suffix

        # comment in
        if current_line[current_indentation:].startswith(comment_prefix) and comment_mode != 'out':
            chars_to_remove = len(comment_prefix)
            try:
                if current_line[current_indentation+len(comment_prefix)] == ' ':
                    chars_to_remove += 1
            except IndexError:
                pass
            remove_text_after_cursor(chars_to_remove)
            buffer.cursor_position += max(0, current_position_in_line - current_indentation - chars_to_remove)

            if comment_suffix:
                original_cursor_position = buffer.cursor_position
                move_cursor_to_end_of_line()

                chars_to_remove = len(comment_suffix)
                if buffer.text[buffer.cursor_position-len(comment_suffix)-1] == ' ':
                    chars_to_remove += 1
                remove_text_before_cursor(chars_to_remove)
                buffer.cursor_position = original_cursor_position

            if has_next_line():
                move_cursor_to_next_line()
            return

        # comment out
        buffer.insert_text(complete_comment_prefix)

        if comment_suffix:
            original_cursor_position = buffer.cursor_position
            move_cursor_to_end_of_line()
            buffer.insert_text(complete_comment_suffix)
            buffer.cursor_position = original_cursor_position

        if has_next_line():
            move_cursor_to_next_line()

    def comment_multiple_lines():
        document = buffer.document
        line_index_start = get_start_line_index_of_selection()
        line_index_end = get_end_line_index_of_selection()
        buffer.exit_selection()

        comment_mode = 'out'
        if all(document.lines[index][get_current_indentation():].startswith(get_comment_prefix())
               for index in range(line_index_start, line_index_end + 1)):
            comment_mode = 'in'

        current_cursor_position = buffer.cursor_position
        current_column = buffer.document.translate_index_to_position(current_cursor_position)[1]
        for index in range(line_index_start, line_index_end + 1):
            buffer.cursor_position = buffer.document.translate_row_col_to_index(index, current_column)
            comment_single_line(comment_mode)

    if not is_text_field_focused():
        return

    c_style_endings = (
        '.c', '.h',
        '.cpp', '.hpp',
        '.cc', '.hh',
        '.c++', '.h++',
        '.cp',
        '.cxx', '.hxx',
        '.java',
        '.groovy',
        '.ino',
        '.cs',
        '.go',
        '.php',
        '.js',
        '.rs',
        '.plantuml', '.puml', '.pu',
        '.proto',
    )
    xml_style_endings = (
        '.xml',
        '.html', '.htm', '.xhtml',
        '.launch',
    )

    latex_style_endings = (
        '.tex', '.aux', '.toc',
        '.ps',
    )
    css_style_endings = (
        '.css',
        '.less',
        '.sass',
        '.scss',
        '.php',
        '.sql',
    )
    batch_style_endings = (
        '.bat',
        '.cmd',
    )
    autohotkey_style_endings = (
        '.ahk',
    )
    buffer = Globals.text_field.buffer
    file_path = Globals.file_path.lower()
    comment_prefix = get_comment_prefix()
    comment_suffix = get_comment_suffix()

    if not get_selected_text():
        current_indentation = get_current_indentation()
        comment_single_line()
    else:
        selected_lines = buffer.document.lines[get_start_line_index_of_selection():get_end_line_index_of_selection()+1]
        current_indentation = min(get_indentation_for_line(line) for line in selected_lines)
        comment_multiple_lines()


def handle_select_word_under_cursor():
    buffer = get_app().current_buffer
    start, end = buffer.document.find_boundaries_of_current_word()
    if start == end:
        return
    if start >= 0 and get_selected_text():
        return
    buffer.cursor_position += start
    buffer.start_selection(selection_type=SelectionType.CHARACTERS)
    buffer.cursor_position += end - start


def handle_toggle_case():
    if not is_text_field_focused():
        return

    buffer = get_app().current_buffer
    selected_text = get_selected_text()

    if not selected_text:
        start, end = buffer.document.find_boundaries_of_current_word()
        if start == end:
            return
        buffer.cursor_position += start
        buffer.start_selection(selection_type=SelectionType.CHARACTERS)
        buffer.cursor_position += end - start
        selected_text = get_selected_text()

    cursor_position_start = get_start_cursor_position_of_selection()
    cursor_position_end = get_end_cursor_position_of_selection()

    buffer.cut_selection()
    if selected_text == selected_text.upper():
        buffer.insert_text(selected_text.lower())
    else:
        buffer.insert_text(selected_text.upper())

    buffer.cursor_position = cursor_position_start
    buffer.start_selection()
    buffer.cursor_position = cursor_position_end


def handle_select_rest_of_line(direction):
    buffer = get_app().current_buffer

    if direction == Direction.Left:
        if has_selection():
            first_line_index = min(get_start_line_index_of_selection(), get_end_line_index_of_selection())
            max_cursor_pos = max(get_start_cursor_position_of_selection(), get_end_cursor_position_of_selection())
            buffer.cursor_position = max_cursor_pos
            buffer.start_selection()
            buffer.cursor_position = buffer.document.translate_row_col_to_index(first_line_index, 0)
            move_cursor_to_start_of_line()
        elif buffer.document.cursor_position_col > 0:
            buffer.start_selection()
            move_cursor_to_start_of_line()

    elif direction == Direction.Right:
        if has_selection():
            last_line_index = max(get_start_line_index_of_selection(), get_end_line_index_of_selection())
            min_cursor_pos = min(get_start_cursor_position_of_selection(), get_end_cursor_position_of_selection())
            buffer.cursor_position = min_cursor_pos
            buffer.start_selection()
            buffer.cursor_position = buffer.document.translate_row_col_to_index(last_line_index, 0)
            move_cursor_to_end_of_line()
        elif buffer.document.cursor_position_col < len(buffer.document.current_line):
            buffer.start_selection()
            move_cursor_to_end_of_line()
    else:
        raise ValueError('Only the following directions are supported: {}'.format(Direction.Left, Direction.Right))
