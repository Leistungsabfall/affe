import sys
sys.path.insert(0, 'python-prompt-toolkit')
sys.path.append('src')
sys.path.append('test')

import os
import unittest
from unittest.mock import patch

from globals import Globals
from handlers import keys
from test.testutils import text_field_buffer, has_focus, init_text_field, init_find_toolbar, init_replace_toolbar, \
    find_toolbar_buffer, replace_toolbar_buffer
from util import text_helper
from util.common import Direction


class TestHandler(unittest.TestCase):
    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_char(self):
        init_text_field('', 0)
        keys.handle_char('{')
        self.assertEqual(Globals.text_field.text, '{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '()')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        keys.handle_char('[')
        self.assertEqual(Globals.text_field.text, '[]')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        keys.handle_char('"')
        self.assertEqual(Globals.text_field.text, '""')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        keys.handle_char("'")
        self.assertEqual(Globals.text_field.text, "''")
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('{', 0)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '}{')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('{', 1)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('{}', 1)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('[', 1)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '[}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('[}', 1)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, '[}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('[}', 1)
        keys.handle_char(')')
        self.assertEqual(Globals.text_field.text, '[)}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a}', 1)
        keys.handle_char('}')
        self.assertEqual(Globals.text_field.text, 'a}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('(', 1)
        keys.handle_char(')')
        self.assertEqual(Globals.text_field.text, '()')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('[', 1)
        keys.handle_char(']')
        self.assertEqual(Globals.text_field.text, '[]')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('"', 1)
        keys.handle_char('"')
        self.assertEqual(Globals.text_field.text, '""')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field("'", 1)
        keys.handle_char("'")
        self.assertEqual(Globals.text_field.text, "''")
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('(a', 2)
        keys.handle_char(')')
        self.assertEqual(Globals.text_field.text, '(a)')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('(a)', 2)
        keys.handle_char(')')
        self.assertEqual(Globals.text_field.text, '(a)')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('""', 1)
        keys.handle_char('"')
        self.assertEqual(Globals.text_field.text, '""')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('""', 1)
        keys.handle_char(']')
        self.assertEqual(Globals.text_field.text, '"]"')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a', 0)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '(a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 0)
        keys.handle_char('"')
        self.assertEqual(Globals.text_field.text, '"a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, 'a()')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a', 1)
        keys.handle_char('"')
        self.assertEqual(Globals.text_field.text, 'a"')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('()', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '(())')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('(a', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '((a')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('(]', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '(()]')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('("', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '(("')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('((', 1)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '(((')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field(')', 0)
        keys.handle_char('(')
        self.assertEqual(Globals.text_field.text, '()')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_char('b')
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

        @patch('prompt_toolkit.application.Application.current_buffer', find_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.find_toolbar, *args, **kwargs))
        def test_in_find_toolbar():
            init_find_toolbar('', 0)
            keys.handle_char('a')
            self.assertEqual(Globals.find_toolbar_text_field.text, 'a')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 1)

            init_find_toolbar('b', 0)
            keys.handle_char('a')
            self.assertEqual(Globals.find_toolbar_text_field.text, 'ab')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 1)

            init_find_toolbar('', 0)
            keys.handle_char('{')
            self.assertEqual(Globals.find_toolbar_text_field.text, '{')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 1)

        test_in_find_toolbar()

    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_handle_enter(self):
        init_text_field('', 0)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('12', 0)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '\n12')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('12', 1)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '1\n2')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)

        init_text_field('12', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '12\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1)

        init_text_field('  ', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '  \n  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+2+1)

        init_text_field('    ', 4)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '    \n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+1)

        init_text_field('  \n  ', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '  \n  \n  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+2+1)

        init_text_field(' \n  ', 1)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, ' \n \n  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+1)

        init_text_field('  \n ', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '  \n  \n ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+2+1)

        init_text_field('  ', 0)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '\n  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('    ', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '  \n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+2+1)

        init_text_field('{}', 0)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '\n{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('{}', 1)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '{\n    \n}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+4)

        init_text_field('{}', 2)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '{}\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1)

        init_text_field('    {}', 4+1)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '    {\n        \n    }')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1+4+4)

        init_text_field('}', 0)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '\n}')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('    }', 4)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, '    \n    }')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+4)

        init_text_field('abc', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('abc', 1)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, 'a\nbc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abc', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, 'a\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a', 1)
        keys.handle_autocomplete()
        keys.handle_enter()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(Globals.text_field.buffer.complete_state, None)

        @patch('prompt_toolkit.application.Application.current_buffer', find_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.find_toolbar, *args, **kwargs))
        def test_in_find_toolbar():
            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('', 0)
            keys.handle_enter()
            self.assertEqual(Globals.find_toolbar_text_field.text, '')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4)

            init_text_field('asdf\nasdf', 0)
            init_find_toolbar('sd', 2)
            keys.handle_enter()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'sd')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('sd', 2)
            keys.handle_enter()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'sd')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)

            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('Sd', 2)
            keys.handle_enter()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'Sd')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)

            Globals.find_toolbar_match_case_checkbox.checked = True
            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('Sd', 2)
            keys.handle_enter()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'Sd')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4)

        test_in_find_toolbar()

        @patch('prompt_toolkit.application.Application.current_buffer', replace_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.replace_toolbar, *args, **kwargs))
        def test_in_replace_toolbar():
            init_text_field('asdf\nasdf', 4)
            init_replace_toolbar('', 0)
            keys.handle_enter()
            self.assertEqual(Globals.replace_toolbar_text_field.text, '')
            self.assertEqual(Globals.replace_toolbar_text_field.document.cursor_position, 0)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4)

            init_text_field('asdf\nasdf', 0)
            init_find_toolbar('asdf', 0)
            init_replace_toolbar('fdsa', 2)
            keys.handle_enter()
            self.assertEqual(Globals.replace_toolbar_text_field.text, 'fdsa')
            self.assertEqual(Globals.replace_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'fdsa\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('asdf', 0)
            init_replace_toolbar('fdsa', 2)
            keys.handle_enter()
            self.assertEqual(Globals.replace_toolbar_text_field.text, 'fdsa')
            self.assertEqual(Globals.replace_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nfdsa')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

            init_text_field('asdf\nasdf', 4)
            init_find_toolbar('asdf', 0)
            init_replace_toolbar('asdf', 2)
            keys.handle_enter()
            self.assertEqual(Globals.replace_toolbar_text_field.text, 'asdf')
            self.assertEqual(Globals.replace_toolbar_text_field.document.cursor_position, 2)
            self.assertEqual(Globals.text_field.text, 'asdf\nasdf')
            self.assertEqual(Globals.text_field.document.cursor_position, 4)

        test_in_replace_toolbar()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_jump_to_new_line(self):
        init_text_field('', 0)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, '\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('    ', 4)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, '    \n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+4)

        init_text_field('    (', 4+1)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, '    (\n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1+4)

        init_text_field('a', 0)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('aaaabbbb', 4)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, 'aaaabbbb\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+1)

        init_text_field('    aaaabbbb', 4+4)
        keys.handle_jump_to_new_line()
        self.assertEqual(Globals.text_field.text, '    aaaabbbb\n    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+4+1+4)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_jump_to_new_line()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_tab(self):
        init_text_field('', 0)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    ', 0)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, '        ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    ', 4)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, '        ')
        self.assertEqual(Globals.text_field.document.cursor_position, 8)

        init_text_field('a', 0)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('a', 1)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, 'a    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4)

        init_text_field('a', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_tab()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

        init_text_field('a', 1)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_tab()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_tab()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

        def called():
            called.value = 1

        @patch('prompt_toolkit.buffer.Buffer.auto_down', lambda *args, **kwargs: called())
        def test_tab_in_autocompletion():
            init_text_field('a', 1)
            keys.handle_autocomplete()
            keys.handle_tab()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)
            self.assertEqual(called.value, 1)

        test_tab_in_autocompletion()

        def called():
            called.value = 2

        @patch('handlers.keys.is_find_and_replace_toolbar_focused', lambda *args, **kwargs: True)
        @patch('handlers.keys.walk_through_find_and_replace_toolbar', lambda *args, **kwargs: called())
        def test_tab_in_find_toolbar():
            init_find_toolbar('a', 1)
            keys.handle_tab()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'a')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 1)
            self.assertEqual(called.value, 2)

        test_tab_in_find_toolbar()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_backtab(self):
        init_text_field('', 0)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('    ', 0)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('    ', 4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('     ', 4+1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('     ', 4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, ' ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('    a', 4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('     a', 4+1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    a', 4+1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('     a', 4+1+1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

        init_text_field(' ', 0)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field(' ', 1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('        ', 0)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('        ', 4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('        ', 4+4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('a     b', 1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'a b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a     b', 1+4)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'a b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('ab', 1)
        keys.handle_backtab()
        self.assertEqual(Globals.text_field.text, 'ab')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_backtab()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('    a', 4)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_backtab()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a     b', 1+4)
            keys.handle_backtab()
            self.assertEqual(Globals.text_field.text, 'a     b')
            self.assertEqual(Globals.text_field.document.cursor_position, 1+4)

        test_in_menu()

        def called():
            called.value = 1

        @patch('prompt_toolkit.buffer.Buffer.auto_up', lambda *args, **kwargs: called())
        def test_backtab_in_autocompletion():
            init_text_field('a     b', 1+4)
            keys.handle_autocomplete()
            keys.handle_tab()
            keys.handle_backtab()
            self.assertEqual(Globals.text_field.text, 'a     b')
            self.assertEqual(Globals.text_field.document.cursor_position, 1+4)
            self.assertEqual(called.value, 1)

        test_backtab_in_autocompletion()

        def called():
            called.value = 2

        @patch('handlers.keys.is_find_and_replace_toolbar_focused', lambda *args, **kwargs: True)
        @patch('handlers.keys.walk_through_find_and_replace_toolbar', lambda *args, **kwargs: called())
        def test_tab_in_find_toolbar():
            init_find_toolbar('a    ', 1+4)
            keys.handle_backtab()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'a    ')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 1+4)
            self.assertEqual(called.value, 2)

        test_tab_in_find_toolbar()

    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_autocomplete(self):
        init_text_field('', 0)
        self.assertFalse(text_helper.is_autocompletion_active())

        keys.handle_autocomplete()
        self.assertTrue(text_helper.is_autocompletion_active())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_autocomplete()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

        def called():
            called.value = 1

        @patch('prompt_toolkit.buffer.Buffer.complete_next', lambda *args, **kwargs: called())
        def test_trigger_multiple():
            init_text_field('', 0)
            keys.handle_autocomplete()
            keys.handle_autocomplete()
            self.assertEqual(called.value, 1)

        test_trigger_multiple()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_backspace(self):
        init_text_field('', 0)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field(' ', 0)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, ' ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field(' ', 1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('   ', 1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('   ', 2)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, ' ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('   ', 3)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('    ', 4)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('     ', 4+1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('        ', 4)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('        ', 8)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    ab', 4+2)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 5)

        init_text_field('    a', 4+1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('a{}', 3)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a{')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a{}', 2)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a{}', 1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '{}')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 2)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'ac')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a         ', 1+4+4+1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a        ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4+4)

        init_text_field('a        ', 1+4+4)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a       ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4+3)

        init_text_field('a       ', 1+4+3)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a      ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4+2)

        init_text_field('a      ', 1+4+2)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a     ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4+1)

        init_text_field('a     ', 1+4+1)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a    ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+4)

        init_text_field('a    ', 1+4)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a   ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+3)

        init_text_field('a   ', 1+3)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a  ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+2)

        init_text_field('a  ', 1+2)
        keys.handle_backspace()
        self.assertEqual(Globals.text_field.text, 'a ')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_backspace()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

        @patch('prompt_toolkit.application.Application.current_buffer', find_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.find_toolbar, *args, **kwargs))
        def test_in_find_toolbar():
            init_find_toolbar('', 0)
            keys.handle_backspace()
            self.assertEqual(Globals.find_toolbar_text_field.text, '')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

            init_find_toolbar('a', 0)
            keys.handle_backspace()
            self.assertEqual(Globals.find_toolbar_text_field.text, 'a')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

            init_find_toolbar('a', 1)
            keys.handle_backspace()
            self.assertEqual(Globals.find_toolbar_text_field.text, '')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

            init_find_toolbar('    ', 4)
            keys.handle_backspace()
            self.assertEqual(Globals.find_toolbar_text_field.text, '   ')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 4-1)

            init_find_toolbar('{}', 1)
            keys.handle_backspace()
            self.assertEqual(Globals.find_toolbar_text_field.text, '}')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

        test_in_find_toolbar()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_delete(self):
        init_text_field('', 0)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a    b', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'a   b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a   b', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'a  b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a  b', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'a b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a b', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'ab')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('ab', 1)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 2)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_delete()
        self.assertEqual(Globals.text_field.text, 'ac')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.root_container.window, *args, **kwargs))
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_delete()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_arrow(self):
        init_text_field('', 0)
        keys.handle_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+1)
        keys.handle_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1)
        keys.handle_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4)
        keys.handle_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4)
        keys.handle_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+2)
        keys.handle_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+3)
        keys.handle_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 1)
        keys.handle_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)
        self.assertFalse(text_helper.has_selection())

        def called():
            called.value = 1

        @patch('prompt_toolkit.buffer.Buffer.complete_previous', lambda *args, **kwargs: called())
        def test_move_cursor_up_in_autocompletion():
            init_text_field('abcd\nefg', 4+1+1)
            keys.handle_autocomplete()
            keys.handle_arrow(Direction.Up)
            self.assertEqual(Globals.text_field.text, 'abcd\nefg')
            self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)
            self.assertEqual(called.value, 1)

        test_move_cursor_up_in_autocompletion()

        @patch('prompt_toolkit.buffer.Buffer.complete_previous', lambda *args, **kwargs: called())
        def test_move_cursor_down_in_autocompletion():
            init_text_field('abcd\nefg', 1)
            keys.handle_autocomplete()
            keys.handle_arrow(Direction.Down)
            self.assertEqual(Globals.text_field.text, 'abcd\nefg')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)
            self.assertEqual(called.value, 1)

        test_move_cursor_down_in_autocompletion()

        def test_cursor_is_moved_to_start_of_selection():
            init_text_field('abcd', 3)
            text_helper.start_or_extend_selection(Direction.Left)
            text_helper.start_or_extend_selection(Direction.Left)
            keys.handle_arrow(Direction.Right)
            self.assertEqual(Globals.text_field.text, 'abcd')
            self.assertEqual(Globals.text_field.document.cursor_position, 3)

        def test_cursor_is_moved_to_end_of_selection():
            init_text_field('abcd', 1)
            text_helper.start_or_extend_selection(Direction.Right)
            text_helper.start_or_extend_selection(Direction.Right)
            keys.handle_arrow(Direction.Left)
            self.assertEqual(Globals.text_field.text, 'abcd')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_cursor_is_moved_to_start_of_selection()
        test_cursor_is_moved_to_end_of_selection()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_shift_arrow(self):
        init_text_field('', 0)
        keys.handle_shift_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_shift_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_shift_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('', 0)
        keys.handle_shift_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_shift_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertTrue(text_helper.has_selection())

        keys.handle_shift_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_shift_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 2)
        keys.handle_shift_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+1)
        keys.handle_shift_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1)
        keys.handle_shift_arrow(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4)
        keys.handle_shift_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4)
        keys.handle_shift_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+2)
        keys.handle_shift_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 4+1+3)
        keys.handle_shift_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+3)
        self.assertTrue(text_helper.has_selection())

        init_text_field('abcd\nefg', 1)
        keys.handle_shift_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'abcd\nefg')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1+1)
        self.assertTrue(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_shift_arrow(Direction.Right)
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_cut(self):
        init_text_field('', 0)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a', 0)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a', 1)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 1)
        keys.handle_shift_arrow(Direction.Right)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'a\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 1)
        keys.handle_shift_arrow(Direction.Down)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'adef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 2+1)
        keys.handle_shift_arrow(Direction.Left)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'abcdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 2+1+4+1+2)
        keys.handle_shift_arrow(Direction.Up)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'ab\ncdi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 2+1+4+1+2)
        keys.handle_shift_arrow(Direction.Up)
        keys.handle_shift_arrow(Direction.Left)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'ab\nci')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('\nb', 0)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'b')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a\n', 2)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a\nb', 0)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'b')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a\nb', 1)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'b')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a\nb', 2)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a\nb', 3)
        keys.handle_cut()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_cut()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_copy(self):
        init_text_field('', 0)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('abc\n\ndef', 3+1)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('a', 0)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a', 1)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'a\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertTrue(text_helper.has_selection())

        init_text_field('a', 1)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertTrue(text_helper.has_selection())

        init_text_field('ab\ncdef\nghi', 1)
        keys.handle_shift_arrow(Direction.Right)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'b')

        init_text_field('ab\ncdef\nghi', 1)
        keys.handle_shift_arrow(Direction.Down)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+1)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'b\nc')

        init_text_field('ab\ncdef\nghi', 2+1)
        keys.handle_shift_arrow(Direction.Left)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, '\n')

        init_text_field('ab\ncdef\nghi', 2+1+4+1+2)
        keys.handle_shift_arrow(Direction.Up)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+2)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'ef\ngh')

        init_text_field('ab\ncdef\nghi', 2+1+4+1+2)
        keys.handle_shift_arrow(Direction.Up)
        keys.handle_shift_arrow(Direction.Left)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'ab\ncdef\nghi')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+1)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.buffer.copy_selection().text, 'def\ngh')

        init_text_field('a\nb', 0)
        keys.handle_copy()
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertTrue(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_copy()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_paste(self):
        # advanced paste tests would need mocking
        init_text_field('abc', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_paste()
        self.assertFalse(text_helper.has_selection())

        init_text_field('abc', 1)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_paste('d')
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'adc')

        init_text_field('abc', 0)
        keys.handle_paste('1\r2')
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '1\n2abc')

        init_text_field('abc', 0)
        keys.handle_paste('1\r\n2')
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '1\n2abc')

        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_paste()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_save(self):
        def remove_file():
            try:
                os.remove(temp_file)
            except OSError:
                pass

        init_text_field('abc\n\n     \n     def\n     \nasdf', 3+2+5+1+5+2)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\n\n     def\n\nasdf\n')
        self.assertEqual(Globals.saved_text, 'abc\n\n\n     def\n\nasdf\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+3+5+2)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.git_untracked = False
        Globals.git_status_by_line = dict()
        init_text_field('abc\n\n     \n     def\n     \nasdf', 3+2+5+1+5+2)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\n     \n     def\n     \nasdf')
        self.assertEqual(Globals.saved_text, 'abc\n\n     \n     def\n     \nasdf')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+2+5+1+5+2)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.git_untracked = True
        Globals.git_status_by_line = dict()
        init_text_field('abc\n\n     \n     def\n     \nasdf', 3+2+5+1+5+2)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\n\n     def\n\nasdf\n')
        self.assertEqual(Globals.saved_text, 'abc\n\n\n     def\n\nasdf\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+3+5+2)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.git_untracked = False
        Globals.git_status_by_line = {2: "modified", 5: "modified"}
        init_text_field('abc\n\n     \n     def\n     \nasdf', 3+2+5+1+5+2)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\n\n     def\n     \nasdf\n')
        self.assertEqual(Globals.saved_text, 'abc\n\n\n     def\n     \nasdf\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+3+5+2)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.git_untracked = True
        Globals.git_status_by_line = dict()
        init_text_field('abc  \n\tdef\t \t', 0)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\tdef\n')
        self.assertEqual(Globals.saved_text, 'abc\n\tdef\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.git_untracked = False
        Globals.git_status_by_line = {0: "modified"}
        init_text_field('abc  \n\tdef\t \t', 0)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertTrue(os.path.isfile(temp_file))
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), 'abc\n\tdef\t \t')
        self.assertEqual(Globals.saved_text, 'abc\n\tdef\t \t')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)
        init_text_field('', 0)
        keys.handle_save()
        with open(temp_file, 'r') as file_:
            self.assertEqual(file_.read(), '')
        self.assertEqual(Globals.saved_text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        os.remove(temp_file)

        Globals.read_only = True
        init_text_field('abc', 0)
        temp_file = 'temp.txt'
        Globals.file_path = temp_file
        remove_file()
        self.assertFalse(os.path.exists(temp_file))
        self.assertFalse(Globals.saved_text)
        keys.handle_save()
        self.assertFalse(os.path.isfile(temp_file))
        Globals.read_only = False

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_save()
            self.assertTrue(os.path.isfile(temp_file))
            os.remove(temp_file)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_select_all(self):
        init_text_field('', 0)
        keys.handle_select_all()
        self.assertFalse(text_helper.has_selection())

        init_text_field('abc\nd ef', 0)
        keys.handle_select_all()
        self.assertEqual(text_helper.get_selected_text(), 'abc\nd ef')

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_select_all()
            self.assertFalse(text_helper.has_selection())

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_undo(self):
        # in real life save_to_undo_stack is called automatically when keys are pressed
        init_text_field('', 0)
        Globals.text_field.buffer.save_to_undo_stack()
        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 1)
        Globals.text_field.buffer.save_to_undo_stack()
        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 1)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.move_cursor(Direction.Right)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.remove_text_before_cursor(1)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.type_text('d')
        Globals.text_field.buffer.save_to_undo_stack()
        self.assertEqual(Globals.text_field.text, 'adc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, 'ac')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            text_helper.type_text('b')
            self.assertEqual(Globals.text_field.text, 'ab')
            self.assertEqual(Globals.text_field.document.cursor_position, 2)
            keys.handle_undo()
            self.assertEqual(Globals.text_field.text, 'ab')
            self.assertEqual(Globals.text_field.document.cursor_position, 2)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_redo(self):
        # in real life save_to_undo_stack is called automatically when keys are pressed
        init_text_field('', 0)
        Globals.text_field.buffer.save_to_undo_stack()
        keys.handle_redo()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc', 1)
        Globals.text_field.buffer.save_to_undo_stack()
        keys.handle_redo()
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc', 1)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.move_cursor(Direction.Right)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.remove_text_before_cursor(1)
        Globals.text_field.buffer.save_to_undo_stack()
        text_helper.type_text('d')
        Globals.text_field.buffer.save_to_undo_stack()
        keys.handle_undo()
        keys.handle_undo()
        keys.handle_undo()
        self.assertEqual(Globals.text_field.text, 'abc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        keys.handle_redo()
        self.assertEqual(Globals.text_field.text, 'ac')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        keys.handle_redo()
        self.assertEqual(Globals.text_field.text, 'adc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        keys.handle_redo()
        self.assertEqual(Globals.text_field.text, 'adc')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            text_helper.type_text('b')
            text_helper.type_text('c')
            self.assertEqual(Globals.text_field.text, 'abc')
            self.assertEqual(Globals.text_field.document.cursor_position, 3)
            keys.handle_undo()
            keys.handle_undo()
            keys.handle_redo()
            self.assertEqual(Globals.text_field.text, 'abc')
            self.assertEqual(Globals.text_field.document.cursor_position, 3)

        test_in_menu()

    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_control_home(self):
        init_text_field('', 0)
        keys.handle_control_home()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc\n\ndef', 0)
        keys.handle_control_home()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc\n\ndef', 3+1)
        keys.handle_control_home()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc\n\ndef', 3+1+1+3)
        keys.handle_control_home()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 1)
            keys.handle_control_home()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 1)

        test_in_menu()

    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_control_end(self):
        init_text_field('', 0)
        keys.handle_control_end()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('abc\n\ndef', 0)
        keys.handle_control_end()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1+1+3)

        init_text_field('abc\n\ndef', 3+1)
        keys.handle_control_end()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1+1+3)

        init_text_field('abc\n\ndef', 3+1+1+3)
        keys.handle_control_end()
        self.assertEqual(Globals.text_field.text, 'abc\n\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1+1+3)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_control_end()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

        test_in_menu()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_control_arrow(self):
        init_text_field('aaa\n\nbb\nc', 3+2)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_control_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'aaa\nbb\nc\n')
        self.assertEqual(Globals.text_field.document.cursor_position, 8)
        self.assertTrue(text_helper.has_selection())

        keys.handle_control_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'aaa\n\nbb\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 9)
        self.assertTrue(text_helper.has_selection())

        init_text_field('aaa\n\nbb\nc', 3+2)
        keys.handle_control_arrow(Direction.Up)
        self.assertEqual(Globals.text_field.text, 'aaa\nbb\n\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+1)
        self.assertFalse(text_helper.has_selection())

        keys.handle_control_arrow(Direction.Down)
        self.assertEqual(Globals.text_field.text, 'aaa\n\nbb\nc')
        self.assertEqual(Globals.text_field.document.cursor_position, 3+2)
        self.assertFalse(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_control_arrow(Direction.Right)
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)
            self.assertFalse(text_helper.has_selection())

        test_in_menu()

        init_text_field('a;bcd e', 2)
        keys.handle_control_arrow(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'a;bcd e')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+3)
        self.assertFalse(text_helper.has_selection())

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_comment(self):
        init_text_field('', 0)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '# ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('', 0)
        Globals.file_path = '.tex'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '% ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('', 0)
        Globals.file_path = '.txt'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '# ')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('', 0)
        Globals.file_path = '.cpp'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// ')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('', 0)
        Globals.file_path = '.h'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// ')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('a', 0)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '# a')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a', 1)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '# a')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('# a', 0)
        Globals.file_path = '.c'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('# a', 0)
        Globals.file_path = '.sh'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('# a', 1)
        Globals.file_path = '.sh'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('# a', 2)
        Globals.file_path = '.sh'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('# a', 3)
        Globals.file_path = '.sh'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('', 0)
        Globals.file_path = '.xml'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '<!--  -->')
        self.assertEqual(Globals.text_field.document.cursor_position, 5)

        init_text_field('a', 0)
        Globals.file_path = '.html'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '<!-- a -->')
        self.assertEqual(Globals.text_field.document.cursor_position, 5)

        init_text_field('a\nb', 0)
        Globals.file_path = '.cs'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

        init_text_field('a\nb', 1)
        Globals.file_path = '.cs'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

        init_text_field('a\nb', 2)
        Globals.file_path = '.cs'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a\n// b')
        self.assertEqual(Globals.text_field.document.cursor_position, 1+1+3)

        init_text_field('a\n# b', 2)
        Globals.file_path = '.foo'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('a\n# b', 5)
        Globals.file_path = '.foo'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a\nb')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)

        init_text_field('    a', 0)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    a', 1)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    a', 2)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    a', 3)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    a', 4)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    a', 4+1)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    # a', 0)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 1)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 2)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 3)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 4)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 4+1)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 4+2)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('    # a', 4+3)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+1)

        init_text_field('    # a\n    # b', 0)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a\n    # b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2)

        init_text_field('    # a\n    # b', 4+4)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a\n    b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+4)

        init_text_field('    a\n    b', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a\n    # b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+4+2)

        init_text_field('    # a\n    b', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # # a\n    # b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+6+4+2)

        init_text_field('    a\n    # b', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a\n    # # b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+4+2)

        init_text_field('    # a\n    # b', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a\n    b')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2+4)

        init_text_field('    a\n        bcd', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a\n    #     bcd')
        self.assertEqual(Globals.text_field.document.cursor_position,  4+4+4+2)

        init_text_field('    a\nb', 0)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '#     a\n# b')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+4+2+2)

        init_text_field('    a\n        bcd', 5)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    # a\n    #     bcd')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+4+2)
        self.assertFalse(text_helper.has_selection())
        text_helper.start_or_extend_selection(Direction.Up)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a\n        bcd')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2+4)
        self.assertFalse(text_helper.has_selection())

        init_text_field('    a\n        bcd', 5)
        Globals.file_path = '.htm'
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    <!-- a -->\n    <!--     bcd -->')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+4+3+3+1+4+4+1)
        self.assertFalse(text_helper.has_selection())
        text_helper.start_or_extend_selection(Direction.Up)
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '    a\n        bcd')
        self.assertEqual(Globals.text_field.document.cursor_position, 4+2+4)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#a', 0)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#a', 1)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#a', 2)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#', 0)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#', 1)
        Globals.file_path = '.py'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('<!-- a -->', 0)
        Globals.file_path = '.html'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('<!--a-->', 0)
        Globals.file_path = '.html'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertFalse(text_helper.has_selection())

        init_text_field('def a = 1', 0)
        Globals.file_path = '.groovy'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// def a = 1')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('stages {\n  echo\n}', 0)
        Globals.file_path = 'ReleaseJenkinsFile'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// stages {\n  echo\n}')
        self.assertEqual(Globals.text_field.document.cursor_position, 2+1+6+1+1+1)
        self.assertFalse(text_helper.has_selection())

        init_text_field('#foobar { foo: bar; }', 0)
        Globals.file_path = 'style.css'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '/* #foobar { foo: bar; } */')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo\nbar', 0)
        Globals.file_path = 'start.bat'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'REM foo\nbar')
        self.assertEqual(Globals.text_field.document.cursor_position, 8)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'run.cmd'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, 'REM foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'diagram.puml'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'diagram.plantuml'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'diagram.pu'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'app.proto'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '// foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 3)
        self.assertFalse(text_helper.has_selection())

        init_text_field('foo', 0)
        Globals.file_path = 'byobu.ahk'
        keys.handle_comment()
        self.assertEqual(Globals.text_field.text, '; foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)
        self.assertFalse(text_helper.has_selection())

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_comment()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

        test_in_menu()

        @patch('prompt_toolkit.application.Application.current_buffer', find_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.find_toolbar, *args, **kwargs))
        def test_in_find_toolbar():
            init_text_field('a', 0)
            init_find_toolbar('b', 0)
            keys.handle_comment()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)
            self.assertEqual(Globals.find_toolbar_text_field.text, 'b')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

        test_in_find_toolbar()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_handle_select_word_under_cursor(self):
        init_text_field('', 0)
        keys.handle_select_word_under_cursor()
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('asdf;1234', 0)
        keys.handle_select_word_under_cursor()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'asdf;1234')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        keys.handle_select_word_under_cursor()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'asdf;1234')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('asdf;1234', 2)
        keys.start_or_extend_selection(Direction.Right)
        keys.handle_select_word_under_cursor()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(text_helper.get_selected_text(), 'asdf')
        self.assertEqual(Globals.text_field.text, 'asdf;1234')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)

        init_text_field('asdf;1234', 6)
        keys.handle_select_word_under_cursor()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(text_helper.get_selected_text(), '1234')
        self.assertEqual(Globals.text_field.text, 'asdf;1234')
        self.assertEqual(Globals.text_field.document.cursor_position, 9)

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    @patch('prompt_toolkit.layout.Layout.has_focus',
           lambda *args, **kwargs: has_focus(Globals.text_field, *args, **kwargs))
    def test_handle_toggle_case(self):
        init_text_field('', 0)
        keys.handle_toggle_case()
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'A')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('a', 1)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'A')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('ab', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        self.assertTrue(text_helper.has_selection())
        keys.handle_toggle_case()
        self.assertEqual(Globals.text_field.text, 'Ab')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('AB', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'aB')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('ab', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'AB')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('AB', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'ab')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('aB', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'AB')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('Ab', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'AB')
        self.assertEqual(Globals.text_field.document.cursor_position, 2)

        init_text_field('Import foo', 0)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'IMPORT foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'import foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)

        init_text_field('Import foo', 8)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'Import FOO')
        self.assertEqual(Globals.text_field.document.cursor_position, 10)
        keys.handle_toggle_case()
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'Import foo')
        self.assertEqual(Globals.text_field.document.cursor_position, 10)

        @patch('prompt_toolkit.layout.Layout.has_focus', lambda *args, **kwargs: False)
        def test_in_menu():
            init_text_field('a', 0)
            keys.handle_toggle_case()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)

        test_in_menu()

        @patch('prompt_toolkit.application.Application.current_buffer', find_toolbar_buffer)
        @patch('prompt_toolkit.layout.Layout.has_focus',
               lambda *args, **kwargs: has_focus(Globals.find_toolbar, *args, **kwargs))
        def test_in_find_toolbar():
            init_text_field('a', 0)
            init_find_toolbar('b', 0)
            keys.handle_toggle_case()
            self.assertEqual(Globals.text_field.text, 'a')
            self.assertEqual(Globals.text_field.document.cursor_position, 0)
            self.assertEqual(Globals.find_toolbar_text_field.text, 'b')
            self.assertEqual(Globals.find_toolbar_text_field.document.cursor_position, 0)

        test_in_find_toolbar()

    @patch('prompt_toolkit.application.Application.current_buffer', text_field_buffer)
    def test_handle_select_rest_of_line(self):
        init_text_field('', 0)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('', 0)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, '')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

        init_text_field('a', 0)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 1)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 1)

        init_text_field('a', 1)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('a', 1)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'a')
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.document.cursor_position, 1)

        init_text_field('abc def\n ghi jkl \nmno', 7+1+1+1)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertEqual(Globals.text_field.text, 'abc def\n ghi jkl \nmno')
        self.assertEqual(Globals.text_field.document.cursor_position, 7+1+1+8)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 7+1+1+1)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 7+1+1+8)

        init_text_field('abc def\n ghi jkl \nmno', 4)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertEqual(Globals.text_field.text, 'abc def\n ghi jkl \nmno')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 4)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('abc def\n ghi jkl \nmno', 4)
        with self.assertRaises(ValueError):
            keys.handle_select_rest_of_line(Direction.Up)

        init_text_field('abcdef', 0)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        text_helper.start_or_extend_selection(Direction.Right)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abcdef')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 0)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 6)

        init_text_field('abcdef', 6)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abcdef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 6)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('abcdef', 5)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abcdef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 5)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('abcdef', 3)
        text_helper.start_or_extend_selection(Direction.Left)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abcdef')
        self.assertEqual(Globals.text_field.document.cursor_position, 6)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 6)

        init_text_field('abc\ndef', 5)
        text_helper.start_or_extend_selection(Direction.Up)
        keys.handle_select_rest_of_line(Direction.Left)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abc\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 5)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 0)

        init_text_field('abc\ndef', 2)
        text_helper.start_or_extend_selection(Direction.Down)
        keys.handle_select_rest_of_line(Direction.Right)
        self.assertTrue(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'abc\ndef')
        self.assertEqual(Globals.text_field.document.cursor_position, 7)
        self.assertEqual(text_helper.get_start_cursor_position_of_selection(), 2)
        self.assertEqual(text_helper.get_end_cursor_position_of_selection(), 7)

    def test_handle_home(self):
        init_text_field('asdf', 0)
        keys.handle_select_rest_of_line(Direction.Right)
        keys.handle_home()
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'asdf')
        self.assertEqual(Globals.text_field.document.cursor_position, 0)

    def test_handle_end(self):
        init_text_field('asdf', 4)
        keys.handle_select_rest_of_line(Direction.Left)
        keys.handle_end()
        self.assertFalse(text_helper.has_selection())
        self.assertEqual(Globals.text_field.text, 'asdf')
        self.assertEqual(Globals.text_field.document.cursor_position, 4)
