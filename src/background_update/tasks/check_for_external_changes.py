from dialogs.closable_dialog import ClosableDialog
from globals import Globals
from prompt_toolkit.widgets import Label, Button
from util.common import read_file
from util.gui_helper import is_text_field_focused


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
    try:
        text_on_disk = read_file_from_disk(silent=False)
    except LookupError:
        return

    if Globals.save_in_progress:
        # prevent race condition (Globals.saved_text modified while reading file)
        return

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
