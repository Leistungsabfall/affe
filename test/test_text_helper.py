import sys
sys.path.insert(0, 'python-prompt-toolkit')
sys.path.append('src')
sys.path.append('test')

import unittest
from unittest.mock import patch

from globals import Globals
from test.testutils import text_field_buffer, init_text_field, init_find_toolbar, init_replace_toolbar
from util import text_helper
from util.common import Direction


class TestTextHelper(unittest.TestCase):
    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_type_text(self):
        init_text_field('', 0)
        text_helper.type_text('a')
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('ac', 1)
        text_helper.type_text('b')
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('abc', 3)
        text_helper.type_text('{')
        self.assertEqual(Globals.text_field.text, 'abc{')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('abc', 3)
        text_helper.type_text('}')
        self.assertEqual(Globals.text_field.text, 'abc}')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1)

        init_text_field('abc{', 3+1)
        text_helper.type_text('}')
        self.assertEqual(Globals.text_field.text, 'abc{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1+1)

        init_text_field('abc{}', 3+1)
        text_helper.type_text('}')
        self.assertEqual(Globals.text_field.text, 'abc{}}')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1+1)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_remove_text_before_cursor(self):
        init_text_field('', 0)
        text_helper.remove_text_before_cursor(0)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.remove_text_before_cursor(1)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 0)
        text_helper.remove_text_before_cursor(1)
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 1)
        text_helper.remove_text_before_cursor(0)
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 2)
        text_helper.remove_text_before_cursor(1)
        self.assertEqual(Globals.text_field.text, 'ac')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 3)
        text_helper.remove_text_before_cursor(3)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_remove_text_after_cursor(self):
        init_text_field('', 0)
        text_helper.remove_text_after_cursor(0)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.remove_text_after_cursor(1)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 0)
        text_helper.remove_text_after_cursor(1)
        self.assertEqual(Globals.text_field.text, 'bc')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 1)
        text_helper.remove_text_after_cursor(0)
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 1)
        text_helper.remove_text_after_cursor(2)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 0)
        text_helper.remove_text_after_cursor(3)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

    def test_get_text_before_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_text_before_cursor(0), '')

        init_text_field('', 0)
        self.assertEqual(text_helper.get_text_before_cursor(1), '')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_text_before_cursor(1), '')

        init_text_field('abc', 1)
        self.assertEqual(text_helper.get_text_before_cursor(0), '')

        init_text_field('abc', 2)
        self.assertEqual(text_helper.get_text_before_cursor(1), 'b')

        init_text_field('abc', 3)
        self.assertEqual(text_helper.get_text_before_cursor(3), 'abc')

    def test_get_text_after_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_text_after_cursor(0), '')

        init_text_field('', 0)
        self.assertEqual(text_helper.get_text_after_cursor(1), '')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_text_after_cursor(1), 'a')

        init_text_field('abc', 1)
        self.assertEqual(text_helper.get_text_after_cursor(0), '')

        init_text_field('abc', 1)
        self.assertEqual(text_helper.get_text_after_cursor(1), 'b')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_text_after_cursor(3), 'abc')

    def test_get_char_before_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_char_before_cursor(), '')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_char_before_cursor(), '')

        init_text_field('abc', 1)
        self.assertEqual(text_helper.get_char_before_cursor(), 'a')

        init_text_field('abc', 2)
        self.assertEqual(text_helper.get_char_before_cursor(), 'b')

        init_text_field('abc', 3)
        self.assertEqual(text_helper.get_char_before_cursor(), 'c')

    def test_get_char_after_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_char_after_cursor(), '')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_char_after_cursor(), 'a')

        init_text_field('abc', 1)
        self.assertEqual(text_helper.get_char_after_cursor(), 'b')

        init_text_field('abc', 0)
        self.assertEqual(text_helper.get_char_after_cursor(), 'a')

    def test_get_line_until_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

        init_text_field('a', 0)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

        init_text_field('a', 1)
        self.assertEqual(text_helper.get_line_until_cursor(), 'a')

        init_text_field('\n', 0)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

        init_text_field('\n', 1)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

        init_text_field('\nab c\n', 1)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

        init_text_field('\nab c\n', 1+1)
        self.assertEqual(text_helper.get_line_until_cursor(), 'a')

        init_text_field('\nab c\n', 1+4)
        self.assertEqual(text_helper.get_line_until_cursor(), 'ab c')

        init_text_field('\nab c\n', 1+4+1)
        self.assertEqual(text_helper.get_line_until_cursor(), '')

    def test_get_spaces_before_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field(' ', 0)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field(' ', 1)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 1)

        init_text_field('ab', 0)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field('ab', 1)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field('ab', 2)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field('  ab   ', 2)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 2)

        init_text_field('  ab   ', 2+1)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field('  ab   ', 2+2)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 0)

        init_text_field('  ab   ', 2+2+1)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 1)

        init_text_field('  ab   ', 2+2+2)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 2)

        init_text_field('  ab   ', 2+2+3)
        self.assertEqual(text_helper.get_spaces_before_cursor(), 3)

    def test_get_line_after_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('a', 0)
        self.assertEqual(text_helper.get_line_after_cursor(), 'a')

        init_text_field('a', 1)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('\n', 0)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('\n', 1)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('\nab c\n', 0)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('\nab c\n', 1)
        self.assertEqual(text_helper.get_line_after_cursor(), 'ab c')

        init_text_field('\nab c\n', 1+1)
        self.assertEqual(text_helper.get_line_after_cursor(), 'b c')

        init_text_field('\nab c\n', 1+4)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

        init_text_field('\nab c\n', 1+4+1)
        self.assertEqual(text_helper.get_line_after_cursor(), '')

    def test_get_spaces_after_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field(' ', 0)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 1)

        init_text_field(' ', 1)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('ab', 0)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('ab', 1)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('ab', 2)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('  ab   ', 2)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('  ab   ', 2+1)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

        init_text_field('  ab   ', 2+2)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 3)

        init_text_field('  ab   ', 2+2+1)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 2)

        init_text_field('  ab   ', 2+2+2)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 1)

        init_text_field('  ab   ', 2+2+3)
        self.assertEqual(text_helper.get_spaces_after_cursor(), 0)

    def test_get_leading_spaces_until_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field(' ', 0)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field(' ', 1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 1)

        init_text_field('ab', 0)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field('ab', 1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field('ab', 2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field('  ab   ', 2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('  ab   ', 2+1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('  ab   ', 2+2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('  ab   ', 2+2+1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('  ab   ', 2+2+2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('  ab   ', 2+2+3)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('   \n  ', 0)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field('   \n  ', 1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 1)

        init_text_field('   \n  ', 2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('   \n  ', 2+1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 3)

        init_text_field('   \n  ', 4)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

        init_text_field('   \n  ', 4+1)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 1)

        init_text_field('   \n  ', 3+1+2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 2)

        init_text_field('   \na  ', 3+1+1+2)
        self.assertEqual(text_helper.get_leading_spaces_until_cursor(), 0)

    def test_is_autocompletion_active(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.is_autocompletion_active())

        Globals.text_field.buffer.start_completion()
        self.assertTrue(text_helper.is_autocompletion_active())

        Globals.text_field.buffer.cancel_completion()
        self.assertFalse(text_helper.is_autocompletion_active())

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_move_cursor(self):
        init_text_field('', 0)
        text_helper.move_cursor(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.move_cursor(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.move_cursor(Direction.Up)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.move_cursor(Direction.Down)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        text_helper.move_cursor(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        text_helper.move_cursor(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 0)
        text_helper.move_cursor(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        text_helper.move_cursor(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 0)
        text_helper.move_cursor(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        text_helper.move_cursor(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a\nb', 2)
        text_helper.move_cursor(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a\nb', 1)
        text_helper.move_cursor(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('abcd\nefg', 2)
        text_helper.move_cursor(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('abcd\nefg', 2)
        text_helper.move_cursor(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+2+2)

        init_text_field('abcd\nefg', 4+1+1)
        text_helper.move_cursor(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)

        init_text_field('abcd\nefg', 4+1+1)
        text_helper.move_cursor(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abcd\nefg', 4+1+1)
        with self.assertRaises(ValueError):
            text_helper.move_cursor('foo')

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_start_or_extend_selection(self):
        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '')

        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '')

        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '')

        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'cd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '\ncd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'b\ncd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ab\ncd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ab\ncd')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+3)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'e')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\n')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\ng')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+2)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\ngh')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+3)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\nghi')

        init_text_field('ab\ncdef\nghi', 2+1+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+3)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\nghi')

        init_text_field('ab\ncdef\nghi', 2+1+4+1+1)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'def\ng')

        init_text_field('ab\ncdef\nghi', 2+1+4+1+1)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'b\ncdef\ng')

        init_text_field('ab\ncdef\nghi', 2+1+4+1+1)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'b\ncdef\ng')

        init_text_field('ab\ncdef\nghi', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+2)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '\ncd')

        init_text_field('ab\ncdef\nghi', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.start_or_extend_selection(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+2)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '\ncdef\ngh')

        init_text_field('ab\ncdef\nghi', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.start_or_extend_selection(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+4+1+2)
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '\ncdef\ngh')

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_has_selection(self):
        init_text_field('ab\ncdef\nghi', 2)
        self.assertFalse(text_helper.has_selection())

        text_helper.start_or_extend_selection(Direction.Right)
        self.assertTrue(text_helper.has_selection())

    def test_get_word_under_cursor(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a', 1)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a\nbc', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a\nbc', 1)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a\nbc', 1+1)
        self.assertEqual(text_helper.get_word_under_cursor(), 'bc')

        init_text_field('a\nbc', 1+1+1)
        self.assertEqual(text_helper.get_word_under_cursor(), 'bc')

        init_text_field('a\nbc', 1+1+2)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a_function', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a_function')

        init_text_field('one-two', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'one')

        init_text_field('one-two', 3)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('one-two', 3+1)
        self.assertEqual(text_helper.get_word_under_cursor(), 'two')

        init_text_field('one+two', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'one')

        init_text_field('foo=2', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'foo')

        init_text_field('a b\tc', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a b\tc', 1)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a b\tc', 2)
        self.assertEqual(text_helper.get_word_under_cursor(), 'b')

        init_text_field('a b\tc', 3)
        self.assertEqual(text_helper.get_word_under_cursor(), '')

        init_text_field('a b\tc', 3+1)
        self.assertEqual(text_helper.get_word_under_cursor(), 'c')

        init_text_field('abc"', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'abc')

        init_text_field('abc\'', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'abc')

        init_text_field('a?', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a2', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a2')

        init_text_field('a#b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a(b)', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a.b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('äaöbü', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'äaöbü')

        init_text_field('a[b]', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a,b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a;b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a;b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a~b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a*b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a&b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('a|b', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'a')

        init_text_field('aßb', 0)
        self.assertEqual(text_helper.get_word_under_cursor(), 'aßb')

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_selected_text(self):
        init_text_field('ab\ncdef\nghi', 2)
        self.assertFalse(text_helper.get_selected_text())

        text_helper.start_or_extend_selection(Direction.Down)
        self.assertEqual(text_helper.get_selected_text(), '\ncd')

        text_helper.type_text('j')
        self.assertFalse(text_helper.get_selected_text())

    def test_in_between_matching_special_chars(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.in_between_matching_special_chars())

        init_text_field('{}', 0)
        self.assertFalse(text_helper.in_between_matching_special_chars())

        init_text_field('{}', 1)
        self.assertTrue(text_helper.in_between_matching_special_chars())

        init_text_field('{}', 2)
        self.assertFalse(text_helper.in_between_matching_special_chars())

        init_text_field('()', 1)
        self.assertTrue(text_helper.in_between_matching_special_chars())

        init_text_field('[]', 1)
        self.assertTrue(text_helper.in_between_matching_special_chars())

        init_text_field('""', 1)
        self.assertTrue(text_helper.in_between_matching_special_chars())

        init_text_field("''", 1)
        self.assertTrue(text_helper.in_between_matching_special_chars())

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_add_special_chars_pair(self):
        init_text_field('', 0)
        text_helper.add_special_chars_pair('{')
        self.assertEqual(Globals.text_field.text, '{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

    def test_is_special_char(self):
        self.assertTrue(text_helper.is_special_char('{'))
        self.assertTrue(text_helper.is_special_char('('))
        self.assertTrue(text_helper.is_special_char('['))
        self.assertTrue(text_helper.is_special_char('}'))
        self.assertTrue(text_helper.is_special_char(')'))
        self.assertTrue(text_helper.is_special_char(']'))
        self.assertTrue(text_helper.is_special_char('"'))
        self.assertTrue(text_helper.is_special_char("'"))
        self.assertFalse(text_helper.is_special_char(' '))
        self.assertFalse(text_helper.is_special_char('a'))
        self.assertFalse(text_helper.is_special_char('<'))
        self.assertFalse(text_helper.is_special_char('>'))

    def test_is_opening_special_char(self):
        self.assertTrue(text_helper.is_opening_special_char('{'))
        self.assertTrue(text_helper.is_opening_special_char('('))
        self.assertTrue(text_helper.is_opening_special_char('['))
        self.assertFalse(text_helper.is_opening_special_char('}'))
        self.assertFalse(text_helper.is_opening_special_char(')'))
        self.assertFalse(text_helper.is_opening_special_char(']'))
        self.assertFalse(text_helper.is_opening_special_char('"'))
        self.assertFalse(text_helper.is_opening_special_char("'"))
        self.assertFalse(text_helper.is_opening_special_char(' '))
        self.assertFalse(text_helper.is_opening_special_char('a'))
        self.assertFalse(text_helper.is_opening_special_char('<'))
        self.assertFalse(text_helper.is_opening_special_char('>'))

    def test_is_opening_and_closing_special_char(self):
        self.assertFalse(text_helper.is_opening_and_closing_special_char('{'))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('('))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('['))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('}'))
        self.assertFalse(text_helper.is_opening_and_closing_special_char(')'))
        self.assertFalse(text_helper.is_opening_and_closing_special_char(']'))
        self.assertTrue(text_helper.is_opening_and_closing_special_char('"'))
        self.assertTrue(text_helper.is_opening_and_closing_special_char("'"))
        self.assertFalse(text_helper.is_opening_and_closing_special_char(' '))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('a'))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('<'))
        self.assertFalse(text_helper.is_opening_and_closing_special_char('>'))

    def test_is_closing_special_char(self):
        self.assertFalse(text_helper.is_closing_special_char('{'))
        self.assertFalse(text_helper.is_closing_special_char('('))
        self.assertFalse(text_helper.is_closing_special_char('['))
        self.assertTrue(text_helper.is_closing_special_char('}'))
        self.assertTrue(text_helper.is_closing_special_char(')'))
        self.assertTrue(text_helper.is_closing_special_char(']'))
        self.assertFalse(text_helper.is_closing_special_char('"'))
        self.assertFalse(text_helper.is_closing_special_char("'"))
        self.assertFalse(text_helper.is_closing_special_char(' '))
        self.assertFalse(text_helper.is_closing_special_char('a'))
        self.assertFalse(text_helper.is_closing_special_char('<'))
        self.assertFalse(text_helper.is_closing_special_char('>'))

    def test_is_space(self):
        self.assertTrue(text_helper.is_space(''))
        self.assertTrue(text_helper.is_space(' '))
        self.assertTrue(text_helper.is_space('\t'))
        self.assertTrue(text_helper.is_space('\n'))
        self.assertFalse(text_helper.is_space('a'))
        self.assertFalse(text_helper.is_space('}'))
        self.assertFalse(text_helper.is_space('_'))
        self.assertTrue(text_helper.is_space('  '))
        self.assertFalse(text_helper.is_space('aa'))

    def test_is_cursor_surrounded_by_spaces(self):
        init_text_field('', 0)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field(' ', 0)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field(' ', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('  ', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('\n', 0)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('\n', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('\n\n', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('ab\n\nef', 2)
        self.assertFalse(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('ab\n\nef', 2+1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('ab\n\nef', 2+2)
        self.assertFalse(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('ab', 1)
        self.assertFalse(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('a b', 1)
        self.assertFalse(text_helper.is_cursor_surrounded_by_spaces())

        init_text_field('a b', 2)
        self.assertFalse(text_helper.is_cursor_surrounded_by_spaces())

    def test_is_cursor_surrounded_by_matching_special_chars(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('()', 0)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('()', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('()', 2)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('(}', 1)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('""', 0)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('""', 1)
        self.assertTrue(text_helper.is_cursor_surrounded_by_matching_special_chars())

        init_text_field('""', 2)
        self.assertFalse(text_helper.is_cursor_surrounded_by_matching_special_chars())

    def test_char_after_cursor_is_matching_closing_special_char(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.char_after_cursor_is_matching_closing_special_char('{'))

        init_text_field('}', 0)
        self.assertTrue(text_helper.char_after_cursor_is_matching_closing_special_char('{'))

        init_text_field(')', 0)
        self.assertFalse(text_helper.char_after_cursor_is_matching_closing_special_char('{'))

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_move_cursor_to_start_of_line(self):
        init_text_field('', 0)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('\n  b \ncd', 1+2+1+1+1+2)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1+1)

        init_text_field('\n  b \ncd', 1+2+1+1+1)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1+1)

        init_text_field('\n  b \ncd', 1+2+1+1)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('\n  b \ncd', 1)
        text_helper.move_cursor_to_start_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_move_cursor_to_end_of_line(self):
        init_text_field('', 0)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 1)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('\n  b \ncd', 0)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('\n  b \ncd', 1)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1)

        init_text_field('\n  b \ncd', 1+2+1+1)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1)

        init_text_field('\n  b \ncd', 1+2+1+1+1)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1+1+2)

        init_text_field('\n  b \ncd', 1+2+1+1+1+2)
        text_helper.move_cursor_to_end_of_line()
        self.assertEqual(Globals.text_field.text, '\n  b \ncd')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2+1+1+1+2)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_move_lines(self):
        init_text_field('', 0)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        with self.assertRaises(ValueError):
            text_helper.move_lines(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        with self.assertRaises(ValueError):
            text_helper.move_lines(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        Direction.Foo = 'foo'
        with self.assertRaises(ValueError):
            text_helper.move_lines(Direction.Foo)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 0)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a\nb', 0)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'b\na')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)

        init_text_field('a\nb', 1)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'b\na')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1)

        init_text_field('a\nb', 1+1)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'b\na')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a\nb', 1+1+1)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'b\na')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a\nb', 1+1)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)

        init_text_field('a\nb', 1)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aa\nb', 1)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'b\naa')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1)

        init_text_field('a\nbb', 1+1+1)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'bb\na')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a\nb\nc\nd\ne', 1+1+1+1)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a\nc\nd\nb\ne')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1+1+1)
        self.assertTrue(text_helper.has_selection())

        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'c\nd\na\nb\ne')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1)
        self.assertTrue(text_helper.has_selection())

        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'c\nd\na\nb\ne')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a\nb\ncc\nd\ne', 5)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a\nd\nb\ncc\ne')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertTrue(text_helper.has_selection())

        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a\nd\ne\nb\ncc')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        self.assertTrue(text_helper.has_selection())

        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'a\nd\ne\nb\ncc')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a\n\nb\nc', 3)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a\nb\nc\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 5)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a\nb\n', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, '\na\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertTrue(text_helper.has_selection())

        init_text_field('\na\nbb\nccc', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.move_lines(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'a\nbb\nccc\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+2+1+3)
        self.assertTrue(text_helper.has_selection())

        text_helper.move_lines(Direction.Down)
        self.assertEqual(Globals.text_field.text, '\na\nbb\nccc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1+2+1+3)
        self.assertTrue(text_helper.has_selection())

    def test_move_cursor_to_next_match(self):
        init_text_field('', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=False)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=False)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=True)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=False)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=False)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=True)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=False)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=False)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=True)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('aaa', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=False)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aaa', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=False)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('aaa', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=False, backwards=True)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('aaa', 0)
        init_find_toolbar('a', 0)
        text_helper.move_cursor_to_next_match(keep_position_if_on_cursor=True, backwards=True)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

    def test_replace_match(self):
        init_text_field('', 0)
        init_find_toolbar('', 0)
        init_replace_toolbar('', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=False)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        init_find_toolbar('', 0)
        init_replace_toolbar('', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=True)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('aaa', 1)
        init_find_toolbar('a', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=False)
        self.assertEqual(Globals.text_field.text, 'aba')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('aaa', 1)
        init_find_toolbar('a', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=True)
        self.assertEqual(Globals.text_field.text, 'bbb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aaa', 1)
        init_find_toolbar('A', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        text_helper.replace_match(replace_all=False)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aaa', 1)
        init_find_toolbar('A', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=False)
        self.assertEqual(Globals.text_field.text, 'aba')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('aaa', 1)
        init_find_toolbar('a', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        text_helper.replace_match(replace_all=True)
        self.assertEqual(Globals.text_field.text, 'bbb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aaa', 1)
        init_find_toolbar('A', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        text_helper.replace_match(replace_all=True)
        self.assertEqual(Globals.text_field.text, 'aaa')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('aaa', 1)
        init_find_toolbar('A', 0)
        init_replace_toolbar('b', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        text_helper.replace_match(replace_all=True)
        self.assertEqual(Globals.text_field.text, 'bbb')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

    def test_get_find_matches(self):
        init_text_field('', 0)
        init_find_toolbar('', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        self.assertEqual(text_helper.get_find_matches(), 0)

        init_text_field('', 0)
        init_find_toolbar('', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        self.assertEqual(text_helper.get_find_matches(), 0)

        init_text_field('aaa', 0)
        init_find_toolbar('A', 0)
        Globals.find_toolbar_match_case_checkbox.checked = False
        self.assertEqual(text_helper.get_find_matches(), 3)

        init_text_field('aaa', 0)
        init_find_toolbar('A', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        self.assertEqual(text_helper.get_find_matches(), 0)

        init_text_field('aAA', 0)
        init_find_toolbar('A', 0)
        Globals.find_toolbar_match_case_checkbox.checked = True
        self.assertEqual(text_helper.get_find_matches(), 2)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_has_next_line(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.has_next_line())

        init_text_field('a', 0)
        self.assertFalse(text_helper.has_next_line())

        init_text_field('a', 1)
        self.assertFalse(text_helper.has_next_line())

        init_text_field('a\n', 0)
        self.assertTrue(text_helper.has_next_line())

        init_text_field('a\n', 1)
        self.assertTrue(text_helper.has_next_line())

        init_text_field('a\n', 2)
        self.assertFalse(text_helper.has_next_line())

    def test_get_indentation_for_line(self):
        line = ''
        self.assertEqual(text_helper.get_indentation_for_line(line), 0)

        line = 'a'
        self.assertEqual(text_helper.get_indentation_for_line(line), 0)

        line = ' a'
        self.assertEqual(text_helper.get_indentation_for_line(line), 1)

        line = ' a  '
        self.assertEqual(text_helper.get_indentation_for_line(line), 1)

        line = '    '
        self.assertEqual(text_helper.get_indentation_for_line(line), 4)

        line = '     a '
        self.assertEqual(text_helper.get_indentation_for_line(line), 5)

        line = 'a '
        self.assertEqual(text_helper.get_indentation_for_line(line), 0)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_current_indentation(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_current_indentation(), 0)

        init_text_field('a', 0)
        self.assertEqual(text_helper.get_current_indentation(), 0)

        init_text_field(' a', 0)
        self.assertEqual(text_helper.get_current_indentation(), 1)

        init_text_field(' a  ', 0)
        self.assertEqual(text_helper.get_current_indentation(), 1)

        init_text_field('    ', 0)
        self.assertEqual(text_helper.get_current_indentation(), 4)

        init_text_field('     a ', 0)
        self.assertEqual(text_helper.get_current_indentation(), 5)

        init_text_field('     a ', 7)
        self.assertEqual(text_helper.get_current_indentation(), 5)

        init_text_field('    \n', 0)
        self.assertEqual(text_helper.get_current_indentation(), 4)

        init_text_field('    \n', 5)
        self.assertEqual(text_helper.get_current_indentation(), 0)

        init_text_field('  a\n   ', 3+1)
        self.assertEqual(text_helper.get_current_indentation(), 3)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_start_line_index_of_selection(self):
        init_text_field('', 0)
        with self.assertRaises(AttributeError):
            text_helper.get_start_line_index_of_selection()

        init_text_field('a\nb', 1)
        with self.assertRaises(AttributeError):
            text_helper.get_start_line_index_of_selection()

        init_text_field('a\nbcd', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_line_index_of_selection(), 0)

        init_text_field('a\nbcd', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_line_index_of_selection(), 0)

        init_text_field('a\nbcd', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_line_index_of_selection(), 1)

        init_text_field('a\nbcd', 4)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(text_helper.get_start_line_index_of_selection(), 0)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_end_line_index_of_selection(self):
        init_text_field('', 0)
        with self.assertRaises(AttributeError):
            text_helper.get_end_line_index_of_selection()

        init_text_field('a\nb', 1)
        with self.assertRaises(AttributeError):
            text_helper.get_end_line_index_of_selection()

        init_text_field('a\nbcd', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_line_index_of_selection(), 0)

        init_text_field('a\nbcd', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_line_index_of_selection(), 1)

        init_text_field('a\nbcd', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_line_index_of_selection(), 1)

        init_text_field('a\nbcd', 4)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(text_helper.get_end_line_index_of_selection(), 1)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_start_cursor_position_of_selection(self):
        init_text_field('', 0)
        with self.assertRaises(AttributeError):
            text_helper.get_start_cursor_position_of_selection()

        init_text_field('a\nb', 1)
        with self.assertRaises(AttributeError):
            text_helper.get_start_cursor_position_of_selection()

        init_text_field('a\nbcd', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)

        init_text_field('a\nbcd', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 1)

        init_text_field('a\nbcd', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)

        init_text_field('a\nbcd', 4)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 4)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_end_cursor_position_of_selection(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('a\nb', 1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

        init_text_field('a\nbcd', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

        init_text_field('a\nbcd', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field('a\nbcd', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 3)

        init_text_field('a\nbcd', 4)
        text_helper.start_or_extend_selection(Direction.Up)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_indent_selection(self):
        init_text_field('a', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 4+1)

        init_text_field('a', 1)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 4+1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('a\nb', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, '    a\n    b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2+4+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 4+2+4+1)

        init_text_field('a\nb\nc', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n    b\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+4+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2+4+1)

        init_text_field('a\nb\nc', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n    b\n    c')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+4+2+4+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2+4+2+4+1)

        init_text_field('a\nb\nc', 2)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.indent_selection()
        self.assertEqual(Globals.text_field.text, '    a\n    b\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 4+2+4+1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_unindent_selection(self):
        init_text_field('a', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

        init_text_field('a', 1)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field(' a', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

        init_text_field('     a', 4+1)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, ' a')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field('a\n b', 2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 3)

        init_text_field('a\n b', 2+1)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 3)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field('a\n b\n     c', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n b\n     c')
        self.assertEqual(Globals.text_field.document.cursor_position, 5+5+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 5+5+1)

        init_text_field('a\n b\n     c', 1+2+2+5+1)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n b\n     c')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 1+2+2+5+1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('a\n b\n     c', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\nb\n    c')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 4+4+1)

        init_text_field('a\n b\n     c', 1+2+2+5+1)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.start_or_extend_selection(Direction.Up)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n b\n     c')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 1+2+2+5+1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('a\n', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field(' a\n', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field('    a\n', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

        init_text_field('     a\n', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, ' a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 3)

        init_text_field('a\n ', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n ')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 3)

        init_text_field('a\n    ', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 6)

        init_text_field('a\n     ', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n     ')
        self.assertEqual(Globals.text_field.document.cursor_position, 7)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 7)

        init_text_field('    a\n', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        text_helper.unindent_selection()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 2)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_get_autocomplete_suggestions(self):
        init_text_field('', 0)
        self.assertEqual(text_helper.get_autocomplete_suggestions(''), [])
        text_helper.type_text(' ')
        self.assertEqual(text_helper.get_autocomplete_suggestions(' '), [])

        init_text_field(' ', 0)
        self.assertEqual(text_helper.get_autocomplete_suggestions(''), [])
        text_helper.type_text(' ')
        self.assertEqual(text_helper.get_autocomplete_suggestions(' '), [])

        init_text_field('APP_NAME', 0)
        self.assertEqual(text_helper.get_autocomplete_suggestions(''), [])
        init_text_field('APP_NAME foobar', 0)
        self.assertEqual(text_helper.get_autocomplete_suggestions(''), ['foobar'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('APP_NAM')
        self.assertEqual(text_helper.get_autocomplete_suggestions('APP_NAM'), ['APP_NAME'])
        text_helper.type_text('E')
        self.assertEqual(text_helper.get_autocomplete_suggestions('APP_NAME'), [])
        text_helper.type_text('E')
        self.assertEqual(text_helper.get_autocomplete_suggestions('APP_NAMEE'), [])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('app_nam')
        self.assertEqual(text_helper.get_autocomplete_suggestions('app_nam'), ['APP_NAME'])
        text_helper.type_text('e')
        self.assertEqual(text_helper.get_autocomplete_suggestions('app_name'), ['APP_NAME'])
        text_helper.type_text('e')
        self.assertEqual(text_helper.get_autocomplete_suggestions('app_namee'), [])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('APPNAME')
        self.assertEqual(text_helper.get_autocomplete_suggestions('APPNAME'), ['APP_NAME'])
        init_text_field(' APP_NAME', 0)
        text_helper.type_text('appnam')
        self.assertEqual(text_helper.get_autocomplete_suggestions('appnam'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('AN')
        self.assertEqual(text_helper.get_autocomplete_suggestions('AN'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('an')
        self.assertEqual(text_helper.get_autocomplete_suggestions('an'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('AP')
        self.assertEqual(text_helper.get_autocomplete_suggestions('AP'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('ap')
        self.assertEqual(text_helper.get_autocomplete_suggestions('ap'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('AM')
        self.assertEqual(text_helper.get_autocomplete_suggestions('AM'), ['APP_NAME'])

        init_text_field(' APP_NAME', 0)
        text_helper.type_text('am')
        self.assertEqual(text_helper.get_autocomplete_suggestions('am'), ['APP_NAME'])

        init_text_field(' subsystem', 0)
        text_helper.type_text('subss')
        self.assertEqual(text_helper.get_autocomplete_suggestions('subss'), ['subsystem'])

        init_text_field(' subsystem', 0)
        text_helper.type_text('subssm')
        self.assertEqual(text_helper.get_autocomplete_suggestions('subssm'), ['subsystem'])

        init_text_field(' subsystem', 0)
        text_helper.type_text('subsss')
        self.assertEqual(text_helper.get_autocomplete_suggestions('subsss'), [])

        init_text_field(' clipboard', 0)
        text_helper.type_text('baild')
        self.assertEqual(text_helper.get_autocomplete_suggestions('baild'), [])

        init_text_field(' clipboard', 0)
        text_helper.type_text('baildd')
        self.assertEqual(text_helper.get_autocomplete_suggestions('baildd'), [])

        init_text_field(' bar Bar', 0)
        text_helper.type_text('b')
        self.assertEqual(text_helper.get_autocomplete_suggestions('b'), ['bar', 'Bar'])

        init_text_field(' bar Bar', 0)
        text_helper.type_text('B')
        self.assertEqual(text_helper.get_autocomplete_suggestions('B'), ['Bar', 'bar'])

        init_text_field(' Bar bar', 0)
        text_helper.type_text('b')
        self.assertEqual(text_helper.get_autocomplete_suggestions('b'), ['bar', 'Bar'])

        init_text_field(' Bar bar', 0)
        text_helper.type_text('B')
        self.assertEqual(text_helper.get_autocomplete_suggestions('B'), ['Bar', 'bar'])

        init_text_field(' __main foo Bar zzz', 0)
        text_helper.type_text('a')
        self.assertEqual(text_helper.get_autocomplete_suggestions('a'), ['__main', 'Bar'])

        init_text_field(' AppName ApplicationName appname zzz', 0)
        text_helper.type_text('A')
        self.assertEqual(text_helper.get_autocomplete_suggestions('A'), ['ApplicationName', 'AppName', 'appname'])

        init_text_field(' AppName applicationname rapidport zzz', 0)
        text_helper.type_text('app')
        self.assertEqual(text_helper.get_autocomplete_suggestions('app'), ['applicationname', 'AppName', 'rapidport'])

        init_text_field(' AppName applicationname rapidport zzz', 0)
        text_helper.type_text('App')
        self.assertEqual(text_helper.get_autocomplete_suggestions('App'), ['AppName', 'applicationname', 'rapidport'])

        init_text_field(' AppName applicationname rapidport zzz', 0)
        text_helper.type_text('api')
        self.assertEqual(text_helper.get_autocomplete_suggestions('api'), ['applicationname', 'rapidport'])

        init_text_field(' rapidport artificial_port_identifier zzz', 0)
        text_helper.type_text('rapi')
        self.assertEqual(text_helper.get_autocomplete_suggestions('rapi'), ['rapidport', 'artificial_port_identifier'])

        init_text_field(' rapidport artificial_port_identifier zzz', 0)
        text_helper.type_text('api')
        self.assertEqual(text_helper.get_autocomplete_suggestions('api'), ['artificial_port_identifier', 'rapidport'])

        init_text_field(' __ __2 1234', 0)
        text_helper.type_text('_')
        self.assertEqual(text_helper.get_autocomplete_suggestions('_'), [])

        init_text_field(' __ __2 1234 a2', 0)
        text_helper.type_text('2')
        self.assertEqual(text_helper.get_autocomplete_suggestions('2'), ['a2'])

        init_text_field(' abc,def', 0)
        text_helper.type_text('d')
        self.assertEqual(text_helper.get_autocomplete_suggestions('d'), ['def'])

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_select_next_word(self):
        with self.assertRaises(ValueError):
            init_text_field('', 0)
            text_helper.select_next_word(Direction.Up)

        init_text_field('', 0)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 0)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 2)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 3)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 4)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 6)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 8)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 8)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 11)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 11)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 12)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 12)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 15)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 15)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 19)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 19)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 21)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 21)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 22)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 22)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 24)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 24)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 25)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 25)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 27)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 27)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 28)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 28)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 28)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 28)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 27)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 27)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 25)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 25)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 24)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 24)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 22)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 22)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 21)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 21)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 19)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 19)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 15)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 15)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 12)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 12)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 11)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 11)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 8)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 8)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 6)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 4)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 3)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 2)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field(' "a bc, def|ghi\n  \njk lm.no\n', 0)
        text_helper.select_next_word(Direction.Left)
        self.assertEqual(Globals.text_field.text, ' "a bc, def|ghi\n  \njk lm.no\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('23, 45a67', 0)
        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, '23, 45a67')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, '23, 45a67')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        text_helper.select_next_word(Direction.Right)
        self.assertEqual(Globals.text_field.text, '23, 45a67')
        self.assertEqual(Globals.text_field.document.cursor_position, 9)
