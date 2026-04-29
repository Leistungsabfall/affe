import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import unittest

from pygments.token import Comment, Text

from lexers.text_with_comment_lexer import TextWithCommentLexer

class TestLexerHelper(unittest.TestCase):
    def test_comments_in_text_with_comment_lexer(self):
        lexer = TextWithCommentLexer()
        text = "text # inline comment\n" \
               "# full line comment with space\n" \
               "#full line comment without space\n" \
               "comment#invalid text2"

        emitted = [(ttype, value) for ttype, value in lexer.get_tokens(text) if value]

        text_values = ''.join(value for ttype, value in emitted if ttype in Text)
        comment_values = ''.join(value for ttype, value in emitted if ttype in Comment)

        self.assertIn("text", text_values)
        self.assertIn("inline comment", comment_values)
        self.assertIn("full line comment with space", comment_values)
        self.assertIn("full line comment without space", comment_values)
        self.assertIn("comment#invalid text2", text_values)
