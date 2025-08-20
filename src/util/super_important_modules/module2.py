from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl, WindowAlign, VSplit
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.styles import Style
from util.super_important_modules.module2_util import get_pos, SunfishThread
from util.super_important_modules.sunfish import MATE_LOWER

style = Style.from_dict({
    'white': '#fff',
    'black': '#000',
    'piece-style-click': 'bg:#4c4',
    'piece-style-drag': 'bg:#8c8',
    'background': 'bg:#333',
    'piece-style-opponent-dark': 'bg:#49f',
    'piece-style-opponent-light': 'bg:#4bf',
    'piece-style-dark': 'bg:#888',
    'piece-style-light': 'bg:#aaa',
    'statusbar-item': 'bg:#666 bold',
})


def get_statusbar_top_left_text():
    fragments = []
    fragments.append(('', ' chess.py'))
    return fragments


def get_statusbar_top_right_text(board):
    def add_space():
        fragments.append(('', '  '))

    def add_item(text, mouse_handler):
        fragments.append(('class:statusbar-item', text, mouse_handler))

    def mouse_handler_exit(mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            get_app().exit()

    def mouse_handler_toggle_easy_mode(mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            board.sunfish.easy_mode = not board.sunfish.easy_mode

    fragments = []
    x = 'x' if board.sunfish.easy_mode else ' '
    add_item(
        text=f' [{x}] Easy mode ',
        mouse_handler=mouse_handler_toggle_easy_mode,
    )

    add_space()

    add_item(
        text=' Close [x] ',
        mouse_handler=mouse_handler_exit,
    )
    return fragments


def get_statusbar_bottom_text():
    fragments = []
    fragments.append(('', ' Esc = Exit | Mouse click/drag = Move piece'))
    return fragments


class Board:
    BOARD_CHARS = 'ABCDEFGH'

    def __init__(self, sunfish):
        self.sunfish = sunfish
        self.formatted_text_control = FormattedTextControl(text=self.get_board, show_cursor=False)

        self.window = Window(
            content=self.formatted_text_control,
            style='class:background',
            width=64,
        )
        self.output = ''
        self.mouse_down_piece_pos = (-1, -1)
        self.mouse_down_piece_pos_old = (-1, -1)
        self.piece_pos = (-1, -1)
        self.old_piece_pos = (-1, -1)

        self.piece_style = ''

        self.initial_offset_x = 4
        self.initial_offset_y = 1  # statusbar does not count
        self.tile_size_x = 7
        self.tile_size_y = 3

        self.drag_active = False
        self.piece_already_clicked = False

        self.game_over = False

    def mouse_handler(self, mouse_event):
        def get_current_piece_pos():
            pos_x = (mouse_x - self.initial_offset_x) // self.tile_size_x
            pos_y = (mouse_y - self.initial_offset_y) // self.tile_size_y
            return pos_x, pos_y

        def reset_current_piece_pos():
            self.piece_pos = (-1, -1)

        def reset_mouse_piece_pos():
            self.mouse_down_piece_pos = (-1, -1)
            self.mouse_down_piece_pos_old = (-1, -1)

        if mouse_event.event_type in (MouseEventType.SCROLL_DOWN, MouseEventType.SCROLL_UP):
            return

        if self.game_over:
            return

        if self.sunfish.move_in_progress:
            reset_current_piece_pos()
            return

        mouse_x = mouse_event.position.x
        mouse_y = mouse_event.position.y
        self.piece_pos = get_current_piece_pos()
        if mouse_event.event_type == MouseEventType.MOUSE_DOWN:
            # click mode or init drag mode
            self.mouse_down_piece_pos_old = self.mouse_down_piece_pos
            self.mouse_down_piece_pos = get_current_piece_pos()
            self.piece_style = 'class:piece-style-click'
            self.piece_already_clicked = self.piece_pos == self.old_piece_pos
        elif mouse_event.event_type == MouseEventType.MOUSE_DOWN_MOVE:
            # drag mode
            if self.piece_pos != self.old_piece_pos:
                self.piece_style = 'class:piece-style-drag'
                self.drag_active = True

        elif mouse_event.event_type == MouseEventType.MOUSE_UP:
            # drag finished or click finished
            if self.drag_active:
                self.drag_active = False
                self.sunfish.request_move_in_background(self.mouse_down_piece_pos, self.piece_pos)
                reset_mouse_piece_pos()
                reset_current_piece_pos()
            elif self.piece_already_clicked:
                reset_mouse_piece_pos()
                reset_current_piece_pos()
            else:
                # clicked
                x, y = self.mouse_down_piece_pos
                x_old, y_old = self.mouse_down_piece_pos_old
                if self.mouse_down_piece_pos != self.mouse_down_piece_pos_old and all(i in range(0, 8) for i in (x, y, x_old, y_old)):
                    self.sunfish.request_move_in_background(self.mouse_down_piece_pos_old, self.mouse_down_piece_pos)
                    reset_current_piece_pos()
                    reset_mouse_piece_pos()

        self.old_piece_pos = self.piece_pos

    def get_board(self):
        if self.sunfish.win:
            self.game_over = True
            self.output = 'You won'
        elif self.sunfish.hist[-1].score <= -MATE_LOWER:
            self.game_over = True
            self.output = 'You lost'

        fragments = []
        fragments.append(('', ' '*(self.initial_offset_x+8*self.tile_size_x) + '\n', self.mouse_handler))
        for y in range(8):
            for i in range(3):
                if i == 1:
                    text = ' ' + str(8 - y) + ' '*2
                else:
                    text = ' '*4
                fragments.append(('', text, self.mouse_handler))
                for x in range(8):
                    if self.piece_pos == (x, y):
                        style = self.piece_style
                    elif (not y % 2 and x % 2) or (y % 2 and not x % 2):
                        if (x, y) in self.sunfish.opponent_move:
                            style = 'class:piece-style-opponent-dark'
                        else:
                            style = 'class:piece-style-dark'
                    else:
                        if (x, y) in self.sunfish.opponent_move:
                            style = 'class:piece-style-opponent-light'
                        else:
                            style = 'class:piece-style-light'
                    piece = ' '
                    if i == 1:
                        if self.sunfish.print_rotated:
                            square = get_pos(self.sunfish.hist[-1].rotate())[y][x]
                        else:
                            square = get_pos(self.sunfish.hist[-1])[y][x]
                        if square.islower():
                            style += ' class:black'
                        elif square.isupper():
                            style += ' class:white'
                        square = square.lower()
                        if square == 'r':
                            piece = '♜'
                        elif square == 'n':
                            piece = '♞'
                        elif square == 'b':
                            piece = '♝'
                        elif square == 'q':
                            piece = '♛'
                        elif square == 'k':
                            piece = '♚'
                        elif square == 'p':
                            piece = '♟'
                    fragments.append((style, ' '*3 + piece + ' '*3, self.mouse_handler))
                fragments.append(('', ' \n', self.mouse_handler))

        fragments.append(('', '\n', self.mouse_handler))
        for x in range(8):
            spaces = 7 if x == 0 else 6
            fragments.append(('', ' '*spaces + self.BOARD_CHARS[x], self.mouse_handler))

        fragments.append(('', '\n\n  ' + self.output, self.mouse_handler))
        return fragments

    def __pt_container__(self):
        return self.window


class Hints:
    def __init__(self, board):
        self.board = board
        self.show = False
        self.formatted_text_control = FormattedTextControl(text=self.get_hints, show_cursor=False)

        self.window = Window(
            content=self.formatted_text_control,
            style='class:background',
        )

    def get_hints(self):
        def mouse_handler(mouse_event):
            if mouse_event.event_type != MouseEventType.MOUSE_DOWN:
                return
            x = mouse_event.position.x
            y = mouse_event.position.y
            if y != 1:
                return
            if x not in range(0, 16):
                return
            self.show = not self.show

        fragments = []
        if self.board.sunfish.easy_mode:
            fragments.append(('', '\n'))
            x = 'x' if self.show else ' '
            fragments.append(('class:statusbar-item', f' [{x}] Show Hints ', mouse_handler))
        fragments.append(('', ' \n\n'))  # space for restricting mouse handler

        if self.board.sunfish.easy_mode and self.show:
            fragments.append(('', '1. E2 -> E3\n'))
            fragments.append(('', '2. D1 -> H5\n'))
            fragments.append(('', '3. G1 -> H3\n'))
            fragments.append(('', '4. H3 -> G5\n'))
            fragments.append(('', '5. H5 -> F7\n'))
            fragments.append(('', '6. G5 -> F7\n'))

        return fragments

    def __pt_container__(self):
        return self.window


def do_super_important_things():
    sunfish = SunfishThread()
    sunfish.start()

    kb = KeyBindings()

    @kb.add(Keys.Escape)
    def _(event):
        get_app().exit()

    board = Board(sunfish)
    hints = Hints(board)

    return Layout(
        HSplit(
            [
                VSplit(
                    children=[
                        Window(FormattedTextControl(get_statusbar_top_left_text)),
                        Window(FormattedTextControl(lambda: get_statusbar_top_right_text(board)), align=WindowAlign.RIGHT),
                    ],
                    height=1,
                    style='class:statusbar',
                ),
                VSplit(
                    children=[
                        board,
                        hints,
                    ],
                ),
                Window(FormattedTextControl(get_statusbar_bottom_text), height=1, style='class:statusbar'),
            ],
            key_bindings=kb,
        ),
        focused_element=board,
    )
