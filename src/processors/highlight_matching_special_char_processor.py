from prompt_toolkit.application import get_app
from prompt_toolkit.cache import SimpleCache
from prompt_toolkit.document import Document
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class HighlightMatchingSpecialCharProcessor(Processor):
    """
    When the cursor is on or right after a bracket, it highlights the matching
    bracket.

    :param max_cursor_distance: Only highlight matching brackets when the
        cursor is within this distance. (From inside a `Processor`, we can't
        know which lines will be visible on the screen. But we also don't want
        to scan the whole document for matching brackets on each key press, so
        we limit to this value.)
    """
    _closing_braces = '])}>'

    def __init__(self, chars='[](){}<>', max_cursor_distance=5000):
        self.chars = chars
        self.max_cursor_distance = max_cursor_distance

        self._positions_cache = SimpleCache(maxsize=8)

    def _get_positions_to_highlight(self, document):
        """
        Return a list of (row, col) tuples that need to be highlighted.
        """
        # Try for the character under the cursor.
        if document.current_char and document.current_char in self.chars:
            pos = document.find_matching_bracket_position(
                    start_pos=document.cursor_position - self.max_cursor_distance,
                    end_pos=document.cursor_position + self.max_cursor_distance)

        # Try for the character before the cursor.
        elif document.char_before_cursor and document.char_before_cursor in self.chars:  # Bugfix from original code
            document = Document(document.text, document.cursor_position - 1)

            pos = document.find_matching_bracket_position(
                    start_pos=document.cursor_position - self.max_cursor_distance,
                    end_pos=document.cursor_position + self.max_cursor_distance)
        else:
            pos = None

        # Return a list of (row, col) tuples that need to be highlighted.
        if pos:
            pos += document.cursor_position  # pos is relative.
            row, col = document.translate_index_to_position(pos)
            return [(row, col), (document.cursor_position_row, document.cursor_position_col)]
        else:
            return []

    def apply_transformation(self, transformation_input):
        buffer_control, document, lineno, source_to_display, fragments, _, _ = transformation_input.unpack()

        # When the application is in the 'done' state, don't highlight.
        if get_app().is_done:
            return Transformation(fragments)

        # Get the highlight positions.
        key = (get_app().render_counter, document.text, document.cursor_position)
        positions = self._positions_cache.get(
            key, lambda: self._get_positions_to_highlight(document))

        # Apply if positions were found at this line.
        if positions:
            for row, col in positions:
                if row == lineno:
                    col = source_to_display(col)
                    fragments = explode_text_fragments(fragments)
                    style, text = fragments[col]

                    if col == document.cursor_position_col:
                        style += ' class:matching-bracket.cursor '
                    else:
                        style += ' class:matching-bracket.other '

                    fragments[col] = (style, text)

        return Transformation(fragments)
