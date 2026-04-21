import re

from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments
from util import text_helper


class HighlightWordUnderCursorProcessor(Processor):
    """
    Highlights the current word under the cursor.
    """
    def __init__(self):
        self.style = 'class:word-under-cursor'

    def apply_transformation(self, transformation_input):
        buffer_control, document, lineno, source_to_display, fragments, _, _ = transformation_input.unpack()

        if fragments:
            fragments = explode_text_fragments(fragments)
            word_under_cursor = text_helper.get_word_under_cursor()

            if len(word_under_cursor.strip()) > 0:
                for match in re.finditer(r'\w+', fragment_list_to_text(fragments)):
                    if match.group() == word_under_cursor:
                        for i in range(match.start(), match.end()):
                            fragments[i] = (fragments[i][0] + ' ' + self.style, fragments[i][1])
                            # if fragments[i][1] == 'P': print(fragments[i][0])

        return Transformation(fragments)
