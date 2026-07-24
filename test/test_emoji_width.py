import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

from collections import defaultdict
from types import SimpleNamespace
import unittest

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl, UIContent
from prompt_toolkit.layout.processors import TabsProcessor
from prompt_toolkit.layout.screen import Char, Point, Screen, Size, WritePosition
from prompt_toolkit.output import ColorDepth, DummyOutput
from prompt_toolkit.renderer import _output_screen_diff
from prompt_toolkit.styles import DEFAULT_ATTRS


class RecordingOutput(DummyOutput):
    def __init__(self):
        self.events = []
        self.cursor_x = 0
        self.marker_positions = []

    def write(self, data):
        self.events.append(('write', data))
        if data == '\r':
            self.cursor_x = 0
        else:
            if data == '|':
                self.marker_positions.append(self.cursor_x)
            # Simulate a terminal that renders a new emoji as one cell.
            self.cursor_x += len(data)

    def cursor_forward(self, amount):
        self.events.append(('cursor_forward', amount))
        self.cursor_x += amount

    def cursor_backward(self, amount):
        self.cursor_x -= amount


class TestEmojiWidth(unittest.TestCase):
    def render_line(self, text):
        content = UIContent(
            get_line=lambda _: [('', text)],
            line_count=1,
        )
        screen = Screen()
        Window()._copy_body(
            content,
            screen,
            WritePosition(0, 0, 80, 1),
            0,
            80,
        )
        return screen.data_buffer[0]

    def test_complex_emoji_occupy_two_cells(self):
        emoji = [
            '👨‍⚕️',
            '👩🏽‍💻',
            '👨‍👩‍👧‍👦',
            '🏳️‍🌈',
            '🐦‍🔥',
            '🧑‍🧑‍🧒‍🧒',
            '1️⃣',
            '🇩🇪',
            '❤️',
        ]

        for value in emoji:
            with self.subTest(emoji=value):
                row = self.render_line('A' + value + 'B')
                self.assertEqual(row[1].char, value)
                self.assertEqual(row[1].width, 2)
                self.assertEqual(row[3].char, 'B')

    def test_text_presentation_emoji_occupies_one_cell(self):
        row = self.render_line('A☀︎B')

        self.assertEqual(row[1].char, '☀︎')
        self.assertEqual(row[1].width, 1)
        self.assertEqual(row[2].char, 'B')

    def test_single_codepoint_wide_emoji_normalizes_terminal_cursor(self):
        window = object()
        app = SimpleNamespace(
            layout=SimpleNamespace(current_window=window),
        )
        output = RecordingOutput()
        screen = Screen()
        screen.data_buffer[0][0] = Char('🫨')
        screen.data_buffer[0][1] = Char('')
        screen.data_buffer[0][9] = Char('|')
        screen.height = 1
        screen.set_cursor_position(window, Point(x=0, y=0))

        _output_screen_diff(
            app,
            output,
            screen,
            Point(x=0, y=0),
            ColorDepth.DEFAULT,
            attrs_for_style_string=defaultdict(lambda: DEFAULT_ATTRS),
            size=Size(rows=1, columns=10),
        )

        self.assertEqual(output.marker_positions, [9])

    def test_right_at_end_of_flag_lines_does_not_move_cursor(self):
        buffer = Buffer(document=Document('🇦🇷\n🇩🇪\n'))
        control = BufferControl(
            buffer=buffer,
            input_processors=[TabsProcessor()],
        )

        self.assertEqual(buffer.document.cursor_position_row, 2)
        self.assertEqual(buffer.document.cursor_position_col, 0)
        end_position = buffer.cursor_position

        for _ in range(2):
            buffer.cursor_position += 1
            content = control.create_content(80, 10)
            self.assertEqual(buffer.cursor_position, end_position)
            self.assertEqual(content.cursor_position, Point(x=0, y=2))
