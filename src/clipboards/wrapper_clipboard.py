from clipboards.file_clipboard import FileClipboard
from clipboards.x_clipboard import XClipboard
from prompt_toolkit.clipboard import Clipboard, ClipboardData
from prompt_toolkit.selection import SelectionType


class WrapperClipboard(Clipboard):
    def set_data(self, data):
        assert isinstance(data, ClipboardData)
        text = data.text

        try:
            XClipboard.write(text)
        except Exception:
            FileClipboard.write(text)

    def get_data(self):
        try:
            text = XClipboard.read()
        except Exception:
            text = FileClipboard.read()

        return ClipboardData(
            text=text.replace('\r\n', '\n'),
            type=SelectionType.CHARACTERS)
