from prompt_toolkit.application import get_app
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class ShowTrailingWhiteSpaceProcessor(Processor):
    """
    Make trailing whitespace visible.

    :param get_char: Callable that returns one character.
    """
    def __init__(self, get_char=None, style='class:trailing-whitespace'):
        assert get_char is None or callable(get_char)

        if get_char is None:
            def get_char():
                if '\xb7'.encode(get_app().output.encoding(), 'replace') == b'?':
                    return '.'
                else:
                    return '\xb7'

        self.style = style
        self.get_char = get_char

    def apply_transformation(self, ti):
        fragments = ti.fragments

        if fragments and fragments[-1][1].endswith(' '):
            char = self.get_char()
            fragments = explode_text_fragments(fragments)

            # Walk backwards through all te fragments and replace whitespace.
            for i in range(len(fragments) - 1, -1, -1):
                if fragments[i][1] == ' ':
                    fragments[i] = (fragments[i][0] + ' ' + self.style, char)
                else:
                    break

        return Transformation(fragments)
