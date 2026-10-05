import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import unittest
from types import SimpleNamespace
from unittest import mock

from globals import Globals
from test.testutils import init_text_field

from background_update.tasks import invalidate_app


class TestInvalidateApp(unittest.TestCase):
    def setUp(self):
        self.saved = {name: getattr(Globals, name) for name in ('text_field', 'saved_text', 'git_status_by_line', 'git_branch')}
        init_text_field('text', 0)
        invalidate_app._Cache.render_state = None
        self.app = mock.Mock()
        self.app.layout = SimpleNamespace(current_window='window', container=SimpleNamespace(floats=[]))
        patcher = mock.patch.object(invalidate_app, 'get_app', return_value=self.app)
        patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        for name, value in self.saved.items():
            setattr(Globals, name, value)

    def assert_invalidated(self, expected):
        self.app.invalidate.reset_mock()
        invalidate_app.run()
        self.assertEqual(self.app.invalidate.called, expected)

    def test_only_invalidates_if_render_state_changed(self):
        self.assert_invalidated(True)
        self.assert_invalidated(False)

        Globals.saved_text = 'saved'
        self.assert_invalidated(True)
        self.assert_invalidated(False)

        Globals.git_status_by_line = {0: 'x'}
        self.assert_invalidated(True)

        Globals.git_branch = 'feature'
        self.assert_invalidated(True)

        self.app.layout.container.floats.insert(0, 'dialog')
        self.assert_invalidated(True)

        self.app.layout.current_window = 'dialog window'
        self.assert_invalidated(True)

        Globals.text_field.lexer = mock.Mock()
        self.assert_invalidated(True)
        self.assert_invalidated(False)
