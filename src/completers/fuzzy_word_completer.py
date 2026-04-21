import re

from prompt_toolkit.completion import Completer, Completion
from util.text_helper import get_autocomplete_suggestions


class FuzzyWordCompleter(Completer):
    completion_active = False

    def get_completions(self, document, complete_event):
        def is_alpha(char):
            return re.match(r'\w+', char)

        def get_prefix():
            match = ''
            for match in re.findall(r'\w+', document.text[:document.cursor_position]):
                pass  # make sure match contains the last match
            return match

        if complete_event.completion_requested:  # Ctrl+Space has just been pressed
            FuzzyWordCompleter.completion_active = True
            prefix = ''
        elif not FuzzyWordCompleter.completion_active:
            return

        if is_alpha(document.char_before_cursor):
            prefix = get_prefix()
        elif not complete_event.completion_requested:  # completion ends when char before cursor is non-alpha
            FuzzyWordCompleter.completion_active = False
            return

        for word in get_autocomplete_suggestions(prefix):
            yield Completion(word, start_position=0 - len(prefix))
