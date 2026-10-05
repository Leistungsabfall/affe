import re

from globals import Globals
from prompt_toolkit.cache import SimpleCache
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
        self._word_under_cursor_cache = SimpleCache(maxsize=8)

    def _get_word_under_cursor(self):
        # The word under the cursor is the same for every line, so compute it
        # only once per buffer state instead of once per displayed line.
        buffer = Globals.text_field.buffer
        selection = buffer.selection_state
        key = (
            buffer.text,
            buffer.cursor_position,
            selection.original_cursor_position if selection else None,
            selection.type if selection else None,
        )
        return self._word_under_cursor_cache.get(key, text_helper.get_word_under_cursor)

    def apply_transformation(self, transformation_input):
        buffer_control, document, lineno, source_to_display, fragments, _, _ = transformation_input.unpack()

        if fragments:
            fragments = explode_text_fragments(fragments)
            word_under_cursor = self._get_word_under_cursor()

            if len(word_under_cursor.strip()) > 0:
                for match in re.finditer(r'\w+', fragment_list_to_text(fragments)):
                    if match.group() == word_under_cursor:
                        for i in range(match.start(), match.end()):
                            fragments[i] = (fragments[i][0] + ' ' + self.style, fragments[i][1])
                            # if fragments[i][1] == 'P': print(fragments[i][0])

        return Transformation(fragments)
