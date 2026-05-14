from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Text, Whitespace


class TextWithCommentLexer(RegexLexer):
    tokens = {
        'root': [
            (r'^(#.*)(\n?)', bygroups(Comment.Single, Whitespace)),
            (r'([^\n]*?[ \t])(#.*)(\n?)', bygroups(Text, Comment.Single, Whitespace)),
            (r'\n', Whitespace),
            (r'[^\n]+', Text),
        ],
    }
