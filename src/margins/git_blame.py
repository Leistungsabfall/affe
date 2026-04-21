from globals import Globals
from prompt_toolkit.application import get_app
from prompt_toolkit.layout import Margin
from util.common import text_is_unsaved
from util.git_helper import GIT_UNCOMMITTED_TEXT


class GitBlameMargin(Margin):
    def __init__(self):
        self.__width = 0

    def get_width(self, ui_content):
        if not Globals.git_blame_active:
            self.__width = 0
            return self.__width

        try:
            window_width = get_app().renderer.output.get_size().columns
            self.__width = min(
                window_width // 2,
                max(len(text) for text in Globals.git_blame_by_line)
            )
        except ValueError:
            self.__width = 0
        return self.__width

    def create_margin(self, window_render_info, width, height):
        def calculate_fg_color(bg_color):
            # return black or white color depending on background color
            # http://stackoverflow.com/a/3943023/112731
            # https://stackoverflow.com/questions/35969656/how-can-i-generate-the-opposite-color-according-to-current-color

            r = int(bg_color[0:2], base=16)
            g = int(bg_color[2:4], base=16)
            b = int(bg_color[4:6], base=16)

            if (r * 0.299 + g * 0.587 + b * 0.114) > 125:
                return '000000'
            else:
                return 'FFFFFF'

        def get_text():
            try:
                return Globals.git_blame_by_line[lineno]
            except IndexError:
                return ''

        if not Globals.git_blame_active:
            return

        result = []

        last_lineno = None
        style = ''
        for lineno in window_render_info.displayed_lines:
            if text_is_unsaved():
                style = 'reverse'
                text = 'Save to refresh git blame info...'
            elif lineno == last_lineno:
                style += ' bold'
                text = ' ↳'
            else:
                text = get_text()
                if text == GIT_UNCOMMITTED_TEXT:
                    style = 'reverse'
                elif text:
                    bg = text[:6]
                    fg = calculate_fg_color(bg)
                    style = 'bg:#{bg} fg:#{fg}'.format(bg=bg, fg=fg)
                else:
                    style = ''
            text += ' ' * (self.__width - len(text))
            result.append((style, text + '\n'))
            last_lineno = lineno

        return result
