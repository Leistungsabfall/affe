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
               '# full line comment\n' \
               '#full line comment\n' \
               'text#invalid inline comment\n' \
               'text #inline comment\n' \
               'text# invalid inline comment'

        observed = [
            (ttype, value)
            for _, ttype, value in lexer.get_tokens_unprocessed(text)
        ]
        self.maxDiff = None
        expected = [
            (Text, 'text '),
            (Comment.Single, '# inline comment'),
            (Text.Whitespace, '\n'),
            (Comment.Single, '# full line comment'),
            (Text.Whitespace, '\n'),
            (Comment.Single, '#full line comment'),
            (Text.Whitespace, '\n'),
            (Text, 'text#invalid inline comment'),
            (Text.Whitespace, '\n'),
            (Text, 'text '),
            (Comment.Single, '#inline comment'),
            (Text.Whitespace, '\n'),
            (Text, 'text# invalid inline comment'),
        ]

        self.assertEqual(expected, observed)
