import sys
sys.path.insert(0, 'lib')
sys.path.append('src')

import os
import shutil
import tempfile
import unittest
from unittest import mock

from globals import Globals
from test.testutils import init_text_field

from background_update.tasks import check_for_external_changes


class TestCheckForExternalChanges(unittest.TestCase):
    def setUp(self):
        self.saved = {name: getattr(Globals, name) for name in ('file_path', 'text_field', 'saved_text', 'save_in_progress')}
        self.temp_dir = tempfile.mkdtemp()
        self.path = os.path.join(self.temp_dir, 'file.txt')
        self.write('a\n')
        Globals.file_path = self.path
        Globals.saved_text = 'a\n'
        Globals.save_in_progress = False
        init_text_field('a\n', 0)
        check_for_external_changes._Cache.stat_signature = None
        check_for_external_changes._Cache.last_read = None

        for target, kwargs in (
            ('is_text_field_focused', dict(return_value=True)),
            ('ClosableDialog', dict()),
        ):
            patcher = mock.patch.object(check_for_external_changes, target, **kwargs)
            setattr(self, target, patcher.start())
            self.addCleanup(patcher.stop)
        patcher = mock.patch.object(check_for_external_changes, 'read_file', wraps=check_for_external_changes.read_file)
        self.read_file = patcher.start()
        self.addCleanup(patcher.stop)

    def tearDown(self):
        for name, value in self.saved.items():
            setattr(Globals, name, value)
        shutil.rmtree(self.temp_dir)

    def write(self, text):
        with open(self.path, 'w') as f:
            f.write(text)

    def test_file_is_only_read_if_changed(self):
        check_for_external_changes.run()
        check_for_external_changes.run()
        self.assertEqual(self.read_file.call_count, 1)
        self.ClosableDialog.assert_not_called()

        Globals.text_field.text = 'b\n'
        self.write('b\n')
        check_for_external_changes.run()
        self.assertEqual(self.read_file.call_count, 2)
        self.assertEqual(Globals.saved_text, 'b\n')
        self.ClosableDialog.assert_not_called()  # text field content equals the new file content

    def test_dialog_is_shown_if_unsaved_text_differs(self):
        Globals.text_field.text = 'unsaved\n'
        check_for_external_changes.run()
        self.ClosableDialog.assert_not_called()

        self.write('changed\n')
        check_for_external_changes.run()
        self.ClosableDialog.assert_called_once()
        self.assertEqual(Globals.saved_text, 'changed\n')

    def test_file_is_read_after_full_check_interval(self):
        check_for_external_changes.run()
        check_for_external_changes._Cache.last_read -= check_for_external_changes.FULL_CHECK_INTERVAL_SECONDS
        check_for_external_changes.run()
        self.assertEqual(self.read_file.call_count, 2)

    def test_file_is_read_again_if_save_was_in_progress(self):
        def save_while_reading(path):
            Globals.save_in_progress = True
            return 'a\n'

        self.read_file.side_effect = save_while_reading
        check_for_external_changes.run()
        Globals.save_in_progress = False
        self.read_file.side_effect = None
        check_for_external_changes.run()
        self.assertEqual(self.read_file.call_count, 2)
