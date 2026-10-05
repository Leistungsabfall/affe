import os
import time

from dialogs.closable_dialog import ClosableDialog
from globals import Globals
from prompt_toolkit.widgets import Label, Button
from util.common import read_file
from util.gui_helper import is_text_field_focused

# Timestamps may be coarse, so a modification can (rarely) leave the stat
# signature unchanged. Re-read the file after this interval in any case.
FULL_CHECK_INTERVAL_SECONDS = 10


class _Cache:
    stat_signature = None
    last_read = None


def get_stat_signature(path):
    try:
        st = os.stat(path)
    except OSError:
        return None
    return st.st_mtime_ns, st.st_ctime_ns, st.st_size, st.st_ino


def is_read_needed(stat_signature):
    return (
        _Cache.last_read is None
        or stat_signature != _Cache.stat_signature
        or time.monotonic() - _Cache.last_read >= FULL_CHECK_INTERVAL_SECONDS
    )


def run():
    def read_file_from_disk(silent=True):
        try:
            return read_file(Globals.file_path)
        except LookupError:
            if silent:
                return ''
            raise

    def ignore():
        # reload file to prevent race condition (file content changed while dialog is shown)
        text_on_disk = read_file_from_disk()
        Globals.saved_text = text_on_disk
        dialog.close()

    def reload_from_disk():
        # reload file to prevent race condition (file reverted to old state while dialog is shown)
        text_on_disk = read_file_from_disk()
        cursor_x = Globals.text_field.document.cursor_position_col
        cursor_y = Globals.text_field.document.cursor_position_row
        cursor_position = Globals.text_field.document.translate_row_col_to_index(cursor_y, cursor_x)
        Globals.text_field.text = text_on_disk
        Globals.saved_text = text_on_disk
        Globals.text_field.buffer.cursor_position = cursor_position
        dialog.close()

    if Globals.save_in_progress:
        return
    if not is_text_field_focused():
        return
    # stat before reading, so a modification during reading is detected next time
    stat_signature = get_stat_signature(Globals.file_path)
    if not is_read_needed(stat_signature):
        return  # file on disk is unchanged
    try:
        text_on_disk = read_file_from_disk(silent=False)
    except LookupError:
        return

    if Globals.save_in_progress:
        # prevent race condition (Globals.saved_text modified while reading file)
        return
    _Cache.stat_signature = stat_signature
    _Cache.last_read = time.monotonic()

    if Globals.saved_text == text_on_disk:
        return
    Globals.saved_text = text_on_disk
    if Globals.text_field.text == Globals.saved_text:
        return
    dialog = ClosableDialog(
        title='File content of \'{}\' has changed'.format(Globals.file_name),
        body=Label(text='The file on disk has been externally modified.', dont_extend_height=True),
        buttons=[
            Button(text='Ignore', handler=ignore),
            Button(text='Reload from disk', handler=reload_from_disk),
        ],
    )
    dialog.show()
