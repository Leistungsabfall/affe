import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import unittest
from unittest import mock

from pygments.lexers.python import PythonLexer
from pygments.lexers.shell import BashLexer
from prompt_toolkit.lexers import PygmentsLexer

from globals import Globals
from test.testutils import init_text_field

from background_update.tasks import update_lexer


class TestUpdateLexer(unittest.TestCase):
    def setUp(self):
        self.saved_file_path = Globals.file_path
        self.saved_text_field = Globals.text_field
        update_lexer._Cache.filename = None
        update_lexer._Cache.text = None

    def tearDown(self):
        Globals.file_path = self.saved_file_path
        Globals.text_field = self.saved_text_field

    def test_lexer_is_only_guessed_if_file_name_or_text_changed(self):
        Globals.file_path = 'script'
        init_text_field('#!/usr/bin/env python\n', 0)
        Globals.text_field.lexer = PygmentsLexer(BashLexer)

        with mock.patch.object(update_lexer, 'guess_lexer_wrapper', wraps=update_lexer.guess_lexer_wrapper) as guess:
            update_lexer.run()
            self.assertIs(Globals.text_field.lexer.pygments_lexer_cls, PythonLexer)

            update_lexer.run()
            self.assertEqual(guess.call_count, 1)

            Globals.text_field.text = '#!/bin/bash\n'
            update_lexer.run()
            self.assertEqual(guess.call_count, 2)
            self.assertIs(Globals.text_field.lexer.pygments_lexer_cls, BashLexer)

            Globals.file_path = 'script.py'
            update_lexer.run()
            self.assertEqual(guess.call_count, 3)
            self.assertIs(Globals.text_field.lexer.pygments_lexer_cls, PythonLexer)
