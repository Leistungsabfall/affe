import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import unittest

from pygments.token import Comment, Text

from lexers.text_with_comment_lexer import TextWithCommentLexer

class TestLexerHelper(unittest.TestCase):
    def test_comments_in_text_with_comment_lexer(self):
        lexer = TextWithCommentLexer()
        text = 'text # inline comment\n' \
               '# full line comment with space\n' \
               '#full line comment without space\n' \
               'comment#invalid text2'

        observed = [
            (ttype, value.strip())
            for _, ttype, value in lexer.get_tokens_unprocessed(text)
            if value.strip() and value != '\n'
        ]

        expected = [
            (Text, 'text'),
            (Comment, '# inline comment'),
            (Comment, '# full line comment with space'),
            (Comment, '#full line comment without space'),
            (Text, 'comment'),
            (Text, '#'),
            (Text, 'invalid'),
            (Text, 'text2'),
        ]

        self.assertEqual(expected, observed)
