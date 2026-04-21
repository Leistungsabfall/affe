from globals import Globals
from util.lexer_helper import guess_lexer_wrapper


def run():
    current_lexer = Globals.text_field.lexer
    new_lexer = guess_lexer_wrapper(
        filename=Globals.file_path,
        text=Globals.text_field.text,
    )
    if new_lexer.pygments_lexer_cls != current_lexer.pygments_lexer_cls:
        Globals.text_field.lexer = new_lexer
