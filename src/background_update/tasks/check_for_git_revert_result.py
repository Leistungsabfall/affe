from globals import Globals
from util.git_helper import GIT_ERROR_TEXT
from util.gui_helper import show_message


def run():
    if Globals.git_revert_failed:
        show_message(
            title='Error performing git checkout',
            text='Restoring failed. ' + GIT_ERROR_TEXT,
        )
        Globals.git_revert_failed = False
