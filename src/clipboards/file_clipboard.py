import base64
import getpass
import os
import sys
import tempfile


class FileClipboard:
    @staticmethod
    def __get_path():
        def get_username():
            if sys.platform == 'win32':
                return getpass.getuser()
            try:
                return os.environ['USER']
            except KeyError:
                return ''

        filename = 'affe_clipboard_{user}'.format(user=get_username())
        return os.path.join(tempfile.gettempdir(), filename)

    @staticmethod
    def write(text):
        text = base64.b64encode(text.encode('utf-8'))
        with open(FileClipboard.__get_path(), 'wb') as file_:
            file_.write(text)
        os.chmod(FileClipboard.__get_path(), 0o600)

    @staticmethod
    def read():
        try:
            with open(FileClipboard.__get_path(), 'rb') as file_:
                text = file_.read()
                text = base64.b64decode(text)
                return text.decode('utf-8')
        except FileNotFoundError:
            return ''
