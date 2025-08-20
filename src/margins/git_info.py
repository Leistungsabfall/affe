from globals import Globals
from prompt_toolkit.layout import Margin


class GitMinimapMargin(Margin):
    def get_width(self, ui_content):
        return 1

    def create_margin(self, window_render_info, width, height):
        content_height = window_render_info.content_height
        window_height = window_render_info.window_height

        def get_style_for_line(index):
            try:
                _ = Globals.git_status_by_line[index].value
            except KeyError:
                return 'class:git-info-margin'
            return 'class:git-info-margin-active'

        result = []

        if content_height <= window_height:
            for i in range(window_height):
                style = get_style_for_line(i)
                result.append((style, ' \n'))
        else:
            result = [('class:git-info-margin', ' \n') for _ in range(window_height)]
            for i in Globals.git_status_by_line:
                try:
                    result[int((i / content_height) * window_height)] = ('class:git-info-margin-active', ' \n')
                except IndexError:
                    pass
        return result
