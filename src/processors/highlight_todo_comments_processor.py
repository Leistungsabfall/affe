import re

from prompt_toolkit.formatted_text import fragment_list_to_text
from prompt_toolkit.layout.processors import Processor, Transformation
from prompt_toolkit.layout.utils import explode_text_fragments


class HighlightTodoCommentsProcessor(Processor):
    """
    Highlights TODO comments.
    """
    def __init__(self):
        self.style = 'class:todo-comment'
        self.token = 'todo'

    def apply_transformation(self, ti):
        fragments = ti.fragments

        if fragments:
            fragments = explode_text_fragments(fragments)
            for match in re.finditer(self.token, fragment_list_to_text(fragments), flags=re.IGNORECASE):
                fragment_part = fragments[match.start():match.start()+len(self.token)]
                if all(fragment[0].startswith('class:pygments.comment') for fragment in fragment_part):
                    for i in range(len(self.token)):
                        index = match.start() + i
                        fragments[index] = (fragments[index][0] + ' ' + self.style, fragments[index][1])

        return Transformation(fragments)
