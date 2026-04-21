from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class ShowMultipleWhiteSpaceProcessor(Processor):
    """
    Make multiple ( > 1 ) white spaces within a line visible by replacing them with dots.
    """
    def __init__(self):
        def get_char():
            if '\xb7'.encode(get_app().output.encoding(), 'replace') == b'?':
                return '.'
            else:
                return '\xb7'

        self.style = 'class:multiple-whitespace'
        self.get_char = get_char

    def apply_transformation(self, ti):
        fragments = ti.fragments
        char = self.get_char()

        if fragments and '  ' in fragment_list_to_text(fragments).strip(' '):
            fragments = explode_text_fragments(fragments)

            for i in range(len(fragments) - 1):
                if fragments[i][1] == ' ' and fragments[i+1][1] == ' ':
                    # regular character followed by two spaces
                    fragments[i] = (fragments[i][0] + ' ' + self.style, char)
                    fragments[i+1] = (fragments[i+1][0] + ' ' + self.style, char)
                elif self.style in fragments[i][0] and fragments[i+1][1] == ' ':
                    # multiple white space character followed by space
                    fragments[i+1] = (fragments[i+1][0] + ' ' + self.style, char)
        return Transformation(fragments)
