from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class ShowLeadingWhiteSpaceProcessor(Processor):
    """
    Make leading whitespace visible.

    :param get_char: Callable that returns one character.
    """
    def __init__(self, get_char=None, style='class:leading-whitespace'):
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

        # Walk through all te fragments.
        if fragments and fragment_list_to_text(fragments).startswith(' '):
            char = self.get_char()
            fragments = explode_text_fragments(fragments)

            for i in range(len(fragments)):
                if fragments[i][1] == ' ':
                    fragments[i] = (fragments[i][0] + ' ' + self.style, char)
                else:
                    break

        return Transformation(fragments)
