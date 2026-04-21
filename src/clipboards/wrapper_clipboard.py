import os, sys

from clipboards.file_clipboard import FileClipboard
from clipboards.pb_clipboard import PBClipboard
from clipboards.wayland_clipboard import WaylandClipboard
from clipboards.x_clipboard import XClipboard
from prompt_toolkit.clipboard import Clipboard, ClipboardData
from prompt_toolkit.selection import SelectionType

XDG_SESSION_TYPE = os.getenv('XDG_SESSION_TYPE')

class WrapperClipboard(Clipboard):
    def set_data(self, data):
        assert isinstance(data, ClipboardData)
        text = data.text

        try:
            if sys.platform == 'linux':
                if XDG_SESSION_TYPE == 'wayland':
                    WaylandClipboard.write(text)
                elif XDG_SESSION_TYPE in ('x11', 'xorg'):
                    XClipboard.write(text)
                else:
                    raise Exception()
            elif sys.platform == 'darwin':
                PBClipboard.write(text)
            else:
                raise Exception()
        except Exception:
            FileClipboard.write(text)

    def get_data(self):
        try:
            if sys.platform == 'linux':
                if XDG_SESSION_TYPE == 'wayland':
                    text = WaylandClipboard.read()
                elif XDG_SESSION_TYPE in ('x11', 'xorg'):
                    text = XClipboard.read()
                else:
                    raise Exception()
            elif sys.platform == 'darwin':
                text = PBClipboard.read()
            else:
                raise Exception()
        except Exception:
            text = FileClipboard.read()

        return ClipboardData(
            text=text.replace('\r\n', '\n'),
            type=SelectionType.CHARACTERS)
