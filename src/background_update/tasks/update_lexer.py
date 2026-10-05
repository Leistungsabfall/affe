from globals import Globals
from util.lexer_helper import guess_lexer_wrapper


class _Cache:
    filename = None
    text = None


def run():
    filename = Globals.file_path
    text = Globals.text_field.text
    if filename == _Cache.filename and text == _Cache.text:
        return  # the guessed lexer only depends on file name and text

    current_lexer = Globals.text_field.lexer
    new_lexer = guess_lexer_wrapper(
        filename=filename,
        text=text,
    )
    if new_lexer.pygments_lexer_cls != current_lexer.pygments_lexer_cls:
        Globals.text_field.lexer = new_lexer
    _Cache.filename = filename
    _Cache.text = text
