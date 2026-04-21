import re

from globals import Globals
from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class HighlightFindProcessor(Processor):
    """
    Processor that highlights search matches in the document.
    Note that this doesn't support multiline search matches yet.

    The style classes 'search' and 'search.current' will be applied to the
    content.
    """
    _classname = 'search'
    _classname_current = 'search.current'

    def apply_transformation(self, transformation_input):
        buffer_control, document, lineno, source_to_display, fragments, _, _ = transformation_input.unpack()

        search_text = Globals.find_toolbar_text_field.buffer.text
        searchmatch_fragment = ' class:%s ' % (self._classname, )
        searchmatch_current_fragment = ' class:%s ' % (self._classname_current, )

        if Globals.show_find_window:
            # For each search match, replace the style string.
            line_text = fragment_list_to_text(fragments)
            fragments = explode_text_fragments(fragments)

            match_case = Globals.find_toolbar_match_case_checkbox.checked
            if match_case:
                flags = 0
            else:
                flags = re.IGNORECASE

            # Get cursor column.
            if document.cursor_position_row == lineno:
                cursor_column = source_to_display(document.cursor_position_col)
            else:
                cursor_column = None

            for match in re.finditer(re.escape(search_text), line_text, flags=flags):
                if cursor_column is not None:
                    on_cursor = match.start() <= cursor_column < match.end()
                else:
                    on_cursor = False

                for i in range(match.start(), match.end()):
                    old_fragment, text = fragments[i]
                    if on_cursor:
                        fragments[i] = (old_fragment + searchmatch_current_fragment, fragments[i][1])
                    else:
                        fragments[i] = (old_fragment + searchmatch_fragment, fragments[i][1])

        return Transformation(fragments)
