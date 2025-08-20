import bz2
import copy
import enum
import os
import pickle
import string
import threading
import time

from globals import Globals
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl, WindowAlign, VSplit
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.styles import Style


PRINTABLE_CHARS = string.printable + 'öäüß' + '│├─└ '  # output from "tree"
BLOCK = '█'
VERTICAL_LINE = '│'
HORIZONTAL_LINE = '─'
ARROW_LEFT = '◂'
ARROW_RIGHT = '▸'
ARROW_UP = '▴'
ARROW_DOWN = '▾'
CROSSING_LINES = '┼'


class Color(enum.Enum):
    BLACK = '#333'
    GRAY = '#888'
    WHITE = '#fff'
    BROWN = '#840'
    RED = '#c00'
    ORANGE = '#f80'
    YELLOW = '#fc0'
    GREEN = '#0c0'
    LIGHT_BLUE = '#08c'
    BLUE = '#00c'
    PINK = '#c0c'
    PURPLE = '#808'


# Do not change, otherwise existing files cannot be read anymore
class Cell:
    def __init__(self, color, char=''):
        self.color = color
        self.char = char


class Mode(enum.Enum):
    BLOCK = 'Draw Block'
    FILL = 'Fill Area'
    LINE = 'Draw Line'
    ARROW = 'Draw Arrow'
    RECTANGLE = 'Draw Rectangle'
    TEXT = 'Text'


style_dict = {
    'background': 'bg:#444',
    'item': 'bg:#666 bold',
    'border': '#666',
    'no-border': '#444',
    'statusbar': 'bg:#333',
}

for color in Color:
    style_dict[color.name.lower()] = color.value

style = Style.from_dict(style_dict)


# Taken from https://github.com/encukou/bresenham (2021.18.01)
def bresenham(x0, y0, x1, y1):
    """
    Implementation of Bresenham's line drawing algorithm
    See en.wikipedia.org/wiki/Bresenham's_line_algorithm

    Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2*dy - dx
    y = 0

    for x in range(dx + 1):
        yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy


def get_statusbar_top_left_text(board):
    def border_for_color(color):
        if color == board.current_color:
            return 'class:border'
        return 'class:no-border'

    def mouse_handler_mode(mouse_event, mode):
        board.current_mode = mode

    def mouse_handler_color(mouse_event, color):
        if mouse_event.event_type != MouseEventType.MOUSE_UP:
            return
        board.current_color = color

    fragments = []
    fragments.append(('class:statusbar', ' ' + Globals.file_path + ' '*1000))
    fragments.append(('', '\n\n'))
    for mode in Mode:
        indicator = 'x' if board.current_mode == mode else ' '
        fragments.append(('class:item', f' [{indicator}] {mode.value} ', lambda event, mode=mode: mouse_handler_mode(event, mode)))
        fragments.append(('', '  '))
    fragments.append(('', '\n'))

    for color in Color:
        fragments.append((border_for_color(color.value), '▄▄▄▄', lambda event, color=color: mouse_handler_color(event, color.value)))
    fragments.append(('', '\n'))

    for color in Color:
        fragments.append((border_for_color(color.value), '█', lambda event, color=color: mouse_handler_color(event, color.value)))
        fragments.append(('bg:' + color.value, '  ', lambda event, color=color: mouse_handler_color(event, color.value)))
        fragments.append((border_for_color(color.value), '█', lambda event, color=color: mouse_handler_color(event, color.value)))
    fragments.append(('', '\n'))

    for color in Color:
        fragments.append((border_for_color(color.value), '▀▀▀▀', lambda event, color=color: mouse_handler_color(event, color.value)))
    return fragments


def get_statusbar_top_right_text(board):
    def mouse_handler_exit(mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            x, y = mouse_event.position
            if x == y == 0:
                return
            board.quit_request = True
            get_app().exit()

    fragments = []

    # bugfix for mouse handler range
    fragments.append(('class:statusbar', ' ', mouse_handler_exit))
    fragments.append(('class:item', ' Close [x] ', mouse_handler_exit))
    fragments.append(('', '\n\n\n'))
    return fragments


def get_statusbar_bottom_text():
    fragments = []
    fragments.append(('', ' Esc = Exit | Ctrl+S = Save | Ctrl+A = Export to ASCII | Scroll = Undo'))
    return fragments


class Board:
    def __init__(self):
        def read_board_from_file():
            if Globals.file_path.endswith('.paint'):
                with bz2.open(Globals.file_path, 'rb') as file:
                    board = pickle.load(file)
                    return board

            with open(Globals.file_path, 'r', encoding='utf-8') as file:  # .paint.txt
                content = file.readlines()
            Globals.file_path = Globals.file_path[:-4]
            height_content = len(content)
            width_content = len(content[0])
            board = [[Cell(Color.WHITE.value) for _ in range(width_content)] for _ in range(height_content)]
            for y in range(height_content):
                for x in range(width_content-1):
                    block = content[y][x]
                    if block == BLOCK:
                        cell = Cell(Color.BLACK.value)
                    elif block == ' ':
                        cell = Cell(Color.WHITE.value)
                    else:
                        cell = Cell(Color.BLACK.value, block)
                    board[y][x] = cell
            return board

        def make_cursor_blink():
            flag = True
            while not self.quit_request:
                if self.current_mode == Mode.TEXT:
                    if flag:
                        self.current_cursor_style = '#aaa bg:#555'
                    else:
                        self.current_cursor_style = '#555 bg:#aaa'
                    flag = not flag
                    get_app().invalidate()
                for _ in range(10):
                    if self.quit_request:
                        return
                    time.sleep(0.04)

        def round_up_to_next_even(n):
            return n if n % 2 == 0 else n + 1

        self.current_mode = Mode.BLOCK

        if os.path.exists(Globals.file_path):
            self.board = read_board_from_file()
        else:
            ts = os.get_terminal_size()
            height = ts.lines - 5
            width = round_up_to_next_even(ts.columns)
            self.board = [[Cell(Color.WHITE.value) for _ in range(width)] for _ in range(height-2)]

        self.old_board = copy.deepcopy(self.board)
        self.old_xy = None, None
        self.current_color = Color.BLACK.value
        self.formatted_text_control = FormattedTextControl(text=self.get_board_fragments, show_cursor=False)
        self.cursor_pos = None
        self.last_cursor_redraw_time = 0
        self.current_cursor_style = ''
        self.shape_start = None
        self.shape_end = None
        self.line_direction = None
        self.quit_request = False
        cursor_blink_thread = threading.Thread(target=make_cursor_blink, daemon=True)
        cursor_blink_thread.start()

        self.window = Window(
            content=self.formatted_text_control,
            style='class:background',
        )

    def fill_area(self, x, y):
        def flood_fill(x, y):
            stack = {(x, y)}

            while stack:
                x, y = stack.pop()

                if x < 0 or y < 0:
                    continue

                try:
                    if self.board[y][x].color == self.current_color or self.board[y][x].color != Color.WHITE.value:
                        continue
                except IndexError:
                    continue

                self.board[y][x].color = self.current_color

                stack.add((x - 1, y))
                stack.add((x + 1, y))
                stack.add((x, y + 1))
                stack.add((x, y - 1))

        flood_fill(x, y)

    def backup(self):
        self.old_board = copy.deepcopy(self.board)

    def restore(self):
        self.board = copy.deepcopy(self.old_board)

    def mouse_handler(self, mouse_event, y, x):
        if mouse_event.event_type in (MouseEventType.SCROLL_DOWN, MouseEventType.SCROLL_UP):
            self.restore()
            return

        if self.current_mode == Mode.TEXT:
            self.cursor_pos = (x, y)
            return

        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            # click mode or init drag mode

            if self.current_mode in (Mode.BLOCK, Mode.FILL, Mode.RECTANGLE, Mode.ARROW, Mode.LINE):
                self.backup()
            if self.current_mode in (Mode.RECTANGLE, Mode.ARROW, Mode.LINE):
                self.shape_start = (x, y)

        if self.current_mode == Mode.BLOCK:
            try:
                color = self.current_color
                if None not in self.old_xy:
                    # noinspection PyTypeChecker
                    for dx, dy in bresenham(self.old_xy[0], self.old_xy[1], x, y):
                        self.board[dy][dx] = Cell(color)
                        if dx % 2 == 0:
                            self.board[dy][dx+1] = Cell(color)
                        else:
                            self.board[dy][dx-1] = Cell(color)

                self.board[y][x] = Cell(color)
                if x % 2 == 0:
                    self.board[y][x+1] = Cell(color)
                else:
                    self.board[y][x-1] = Cell(color)
                self.old_xy = x, y
            except IndexError:
                return
        elif self.current_mode == Mode.FILL:
            self.fill_area(x, y)
        elif self.current_mode in (Mode.RECTANGLE, Mode.ARROW, Mode.LINE):
            self.shape_end = (x, y)

        if mouse_event.event_type == MouseEventType.MOUSE_DOWN_MOVE:
            # drag mode
            pass

        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            # drag finished or click finished
            self.old_xy = (None, None)

            if self.current_mode in (Mode.RECTANGLE, Mode.ARROW, Mode.LINE):
                if self.current_mode == Mode.RECTANGLE:
                    coords = self.__get_rectangle_coords()
                elif self.current_mode == Mode.ARROW:
                    coords = self.__get_arrow_coords()
                elif self.current_mode == Mode.LINE:
                    coords = self.__get_line_coords()
                for coord, char in coords.items():
                    x, y = coord
                    self.board[y][x] = Cell(self.current_color, char)
                self.shape_start = None
                self.shape_end = None

    def __get_rectangle_coords(self):
        rectangle_coords = dict()
        if self.shape_start is None or self.shape_end is None or self.shape_start == self.shape_end or self.current_color == Color.WHITE.value:
            return rectangle_coords
        start_x, start_y = self.shape_start
        end_x, end_y = self.shape_end
        rectangle_coords[start_x, start_y] = CROSSING_LINES
        rectangle_coords[end_x, end_y] = CROSSING_LINES
        rectangle_coords[start_x, end_y] = CROSSING_LINES
        rectangle_coords[end_x, start_y] = CROSSING_LINES
        if start_x < end_x:
            range_obj = range(start_x+1, end_x)
        else:
            range_obj = range(start_x-1, end_x, -1)
        for x in range_obj:
            rectangle_coords[x, start_y] = self.__get_result_char(x, start_y, HORIZONTAL_LINE)
            rectangle_coords[x, end_y] = self.__get_result_char(x, end_y, HORIZONTAL_LINE)
        if start_y < end_y:
            range_obj = range(start_y+1, end_y)
        else:
            range_obj = range(start_y-1, end_y, -1)
        for y in range_obj:
            rectangle_coords[start_x, y] = self.__get_result_char(start_x, y, VERTICAL_LINE)
            rectangle_coords[end_x, y] = self.__get_result_char(end_x, y, VERTICAL_LINE)
        return rectangle_coords

    def __get_arrow_coords(self):
        arrow_coords = dict()
        if self.shape_start is None or self.shape_end is None or self.shape_start == self.shape_end or self.current_color == Color.WHITE.value:
            return arrow_coords
        start_x, start_y = self.shape_start
        end_x, end_y = self.shape_end
        diff_x = abs(end_x - start_x) // 2
        diff_y = abs(end_y - start_y)
        if diff_x >= diff_y:
            if start_x < end_x:
                arrow_coords[end_x, start_y] = ARROW_RIGHT
                range_obj = range(start_x, end_x)
            else:
                arrow_coords[end_x, start_y] = ARROW_LEFT
                range_obj = range(start_x, end_x, -1)
            for x in range_obj:
                arrow_coords[x, start_y] = self.__get_result_char(x, start_y, HORIZONTAL_LINE)
        else:
            if start_y < end_y:
                arrow_coords[start_x, end_y] = ARROW_DOWN
                range_obj = range(start_y, end_y)
            else:
                arrow_coords[start_x, end_y] = ARROW_UP
                range_obj = range(start_y, end_y, -1)
            for y in range_obj:
                arrow_coords[start_x, y] = self.__get_result_char(start_x, y, VERTICAL_LINE)
        return arrow_coords

    def __get_line_coords(self):
        line_coords = dict()
        if self.shape_start is None or self.shape_end is None or self.shape_start == self.shape_end or self.current_color == Color.WHITE.value:
            return line_coords
        start_x, start_y = self.shape_start
        end_x, end_y = self.shape_end
        diff_x = abs(end_x - start_x) // 2
        diff_y = abs(end_y - start_y)
        if diff_x >= diff_y:
            if start_x < end_x:
                range_obj = range(start_x, end_x+1)
            else:
                range_obj = range(start_x, end_x-1, -1)
            for x in range_obj:
                line_coords[x, start_y] = self.__get_result_char(x, start_y, HORIZONTAL_LINE)
        else:
            if start_y < end_y:
                range_obj = range(start_y, end_y+1)
            else:
                range_obj = range(start_y, end_y-1, -1)
            for y in range_obj:
                line_coords[start_x, y] = self.__get_result_char(start_x, y, VERTICAL_LINE)
        return line_coords

    def __get_result_char(self, x, y, temp_char):
        if self.shape_start == self.shape_end:
            return CROSSING_LINES
        cell_char = self.board[y][x].char
        if cell_char in (
                VERTICAL_LINE,
                HORIZONTAL_LINE,
                CROSSING_LINES,
                ARROW_LEFT,
                ARROW_RIGHT,
                ARROW_UP,
                ARROW_DOWN,
        ):
            if cell_char == temp_char:
                return temp_char
            return CROSSING_LINES
        return temp_char

    def get_board_fragments(self):
        fragments = []
        if self.current_mode == Mode.RECTANGLE:
            coords = self.__get_rectangle_coords()
        elif self.current_mode == Mode.ARROW:
            coords = self.__get_arrow_coords()
        elif self.current_mode == Mode.LINE:
            coords = self.__get_line_coords()
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                char = self.board[y][x].char or ' '
                if self.current_mode == Mode.TEXT and self.cursor_pos == (x, y):
                    style = self.current_cursor_style
                else:
                    color = self.board[y][x].color
                    if char in ('', ' '):
                        style = 'bg:' + color
                    else:
                        style = 'bg:' + Color.WHITE.value + ' ' + color
                if self.current_mode in (Mode.RECTANGLE, Mode.ARROW, Mode.LINE):
                    try:
                        char = coords[x, y]
                        style = 'bg:' + Color.WHITE.value + ' ' + self.current_color
                    except KeyError:
                        pass

                fragments.append((style, char, lambda event, y=y, x=x: self.mouse_handler(event, y, x)))
            fragments.append(('', '\n'))
        return fragments

    def __pt_container__(self):
        return self.window


def do_super_important_things():
    def __paste(text):
        class Event:
            def __init__(self, data):
                self.data = data

        if board.current_mode != Mode.TEXT:
            return
        board.backup()
        x, y = board.cursor_pos
        for char in text:
            if char in '\r\n':
                if len(board.board) > y + 1:
                    y += 1
                    board.cursor_pos = (x, y)
                else:
                    break
            event = Event(char)
            add_char(event, backup=False)

    kb = KeyBindings()

    @kb.add(Keys.ControlV)
    def _(event):
        text = get_app().clipboard.get_data().text
        __paste(text)

    @kb.add(Keys.BracketedPaste)  # real "paste" event (e.g. Ctrl+Shift+V)
    def _(event):
        text = event.data
        __paste(text)

    @kb.add(Keys.Escape)
    def _(event):
        board.quit_request = True
        get_app().exit()

    @kb.add(Keys.Any)
    def add_char(event, backup=True):
        char = event.data
        if char in '\t\n\r\v\f':
            return
        if char.lower() not in PRINTABLE_CHARS.lower():
            return
        if char == ' ':
            char = ' '  # support for "tree" using nbsp as indentation

        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        if backup:
            board.backup()
        x, y = board.cursor_pos
        board.board[y][x].char = char
        if char == ' ':
            color = Color.WHITE.value
        else:
            color = board.current_color
        board.board[y][x].color = color
        if len(board.board[y]) > x + 1:
            board.cursor_pos = (x+1, y)

    @kb.add('backspace')
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        x, y = board.cursor_pos
        if x == 0:
            return
        x -= 1
        if x < 0:
            board.cursor_pos = None
            return
        board.backup()
        board.cursor_pos = (x, y)
        board.board[y][x].char = ''
        board.board[y][x].color = Color.WHITE.value

    @kb.add(Keys.Delete)
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        board.backup()
        x, y = board.cursor_pos
        board.board[y][x].char = ''
        board.board[y][x].color = Color.WHITE.value

    @kb.add(Keys.Left)
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        x, y = board.cursor_pos
        if x == 0:
            return
        board.cursor_pos = (x-1, y)

    @kb.add(Keys.Right)
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        x, y = board.cursor_pos
        if len(board.board[y]) > x + 1:
            board.cursor_pos = (x+1, y)

    @kb.add(Keys.Up)
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        x, y = board.cursor_pos
        if y == 0:
            return
        board.cursor_pos = (x, y-1)

    @kb.add(Keys.Down)
    def _(event):
        if board.current_mode != Mode.TEXT or board.cursor_pos is None:
            return
        x, y = board.cursor_pos
        if len(board.board) > y + 1:
            board.cursor_pos = (x, y+1)

    @kb.add('enter')
    def _(event):
        pass

    @kb.add(Keys.ControlS)
    def save(event=None):
        with bz2.open(Globals.file_path, 'wb') as file:
            pickle.dump(board.board, file)

    @kb.add(Keys.ControlA)
    def _(event):
        save()
        filename = Globals.file_path + '.txt'
        min_x = len(board.board[0]) // 2
        min_y = len(board.board)
        max_x = 0
        max_y = 0
        for y in range(len(board.board)):
            for x in range(len(board.board[0])):
                cell = board.board[y][x]
                if cell.char not in ('', ' ') or cell.color != Color.WHITE.value:
                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y
        output = ''
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                cell = board.board[y][x]
                if cell.char not in ('', ' '):
                    output += cell.char
                elif cell.color == Color.WHITE.value:
                    output += ' '
                else:
                    output += BLOCK
            output += '\n'
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output)

    board = Board()

    return Layout(
        HSplit(
            [
                VSplit(
                    children=[
                        Window(FormattedTextControl(lambda: get_statusbar_top_left_text(board)), height=6),
                        Window(FormattedTextControl(lambda: get_statusbar_top_right_text(board)), align=WindowAlign.RIGHT, height=1),
                    ],
                    style='class:background',
                ),
                board,
                Window(FormattedTextControl(get_statusbar_bottom_text), height=1, style='class:statusbar'),
            ],
            key_bindings=kb,
        ),
        focused_element=board,
    )
