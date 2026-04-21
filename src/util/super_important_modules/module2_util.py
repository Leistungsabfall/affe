import time
from threading import Thread

from prompt_toolkit.application import get_app
from util.super_important_modules.sunfish import Position, initial, parse, Searcher, render, MATE_LOWER


def get_pos(pos):
    result = []
    for i, row in enumerate(pos.board.split()):
        row2 = []
        for piece in row:
            row2.append(piece)
        result.append(row2)
    return result


class SunfishThread(Thread):
    BOARD_CHARS = 'abcdefgh'

    def __init__(self):
        super().__init__(daemon=True)

        self.hist = [Position(initial, 0, (True, True), (True, True), 0, 0)]
        self.searcher = Searcher()

        self.__move_request = None

        self.print_rotated = False
        self.move_in_progress = False
        self.opponent_move = ()
        self.win = False
        self.easy_mode = False

    def run(self):
        while True:
            if self.__move_request is not None:
                self.move_in_progress = True
                get_app().invalidate()
                self.__move()
                get_app().invalidate()
                self.move_in_progress = False
                self.__move_request = None
            time.sleep(0.01)

    def __move(self):
        def matrix_pos_to_human_pos(pos):
            x, y = pos
            try:
                x = self.BOARD_CHARS[x]
            except IndexError:
                x = -1
            y = 8 - y
            return f'{x}{y}'

        def human_pos_to_matrix(pos):
            x, y = pos
            x = self.BOARD_CHARS.index(x)
            y = 8 - int(y)
            return x, y

        def move_to_sunfish_format(move):
            try:
                move = parse(move[:2]), parse(move[2:])
            except ValueError:
                raise SyntaxError()
            if move not in self.hist[-1].gen_moves():
                raise SyntaxError()
            return move

        self.opponent_move = ()
        pos_src, pos_dst = self.__move_request
        move = matrix_pos_to_human_pos(pos_src) + matrix_pos_to_human_pos(pos_dst)
        try:
            move = move_to_sunfish_format(move)
        except SyntaxError:
            return
        self.piece_pos = (-1, -1)
        self.hist.append(self.hist[-1].move(move))

        self.print_rotated = True

        if self.hist[-1].score <= -MATE_LOWER:
            self.win = True
            return

        # Fire up the engine to look for a move.
        start = time.time()
        for _depth, move, score in self.searcher.search(self.hist[-1], self.hist):
            if time.time() - start > 1 or self.easy_mode:
                break

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        self.opponent_move = human_pos_to_matrix(render(119 - move[0])), human_pos_to_matrix(render(119 - move[1]))
        self.hist.append(self.hist[-1].move(move))
        self.print_rotated = False

    def request_move_in_background(self, pos_src, pos_dst):
        if self.__move_request is not None:
            return
        self.__move_request = (pos_src, pos_dst)
