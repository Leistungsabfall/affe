from globals import Globals
from util.common import text_is_unsaved


def get_statusbar_top_text():
    def append_space():
        fragments.append((class_statusbar, ' '))

    def append_filename():
        append_space()
        fragments.append((class_statusbar, Globals.file_path))

    def append_modification_indicator():
        fragments.append((class_statusbar, '*'))

    def append_read_only():
        append_space()
        fragments.append((class_statusbar+class_read_only_indicator, '[READ-ONLY]'))

    def append_git_branch():
        append_space()
        fragments.append((class_statusbar+class_git_branch, '({})'.format(Globals.git_branch)))

    def append_git_dirty_indicator():
        fragments.append((class_statusbar+class_git_modified_indicator, '*'))

    class_statusbar = 'class:statusbar '
    class_git_branch = 'class:git-branch '
    class_git_modified_indicator = 'class:git-modified-indicator '
    class_read_only_indicator = 'class:read-only-indicator '
    fragments = []
    append_filename()
    if text_is_unsaved():
        append_modification_indicator()
    if Globals.read_only:
        append_read_only()
    if Globals.git_branch:
        append_git_branch()
        if Globals.git_dirty_indicator:
            append_git_dirty_indicator()
    return fragments
