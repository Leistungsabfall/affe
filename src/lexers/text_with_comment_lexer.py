from pygments.lexer import RegexLexer
from pygments.token import Text, Comment


class TextWithCommentLexer(RegexLexer):
    tokens = {
        'root': [
            (r'#.*$', Comment),
            (r'.', Text),
        ],
    }
