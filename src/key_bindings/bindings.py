from globals import Globals
from prompt_toolkit.application import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.scroll import scroll_backward, scroll_forward
from prompt_toolkit.keys import Keys

from handlers import actions
from handlers import keys
from util.common import Direction


def init_key_bindings():
    bindings = KeyBindings()
    __append_custom_bindings(bindings)
    return bindings


def init_fallback_key_bindings():
    # Bugfix: These bindings should only be available when opening 'unsaved changes' dialog
    # using Escape + invalid key sequence (e.g. Esc+F10)
    bindings = KeyBindings()

    @bindings.add(Keys.Left)
    @bindings.add(Keys.BackTab)
    def _(event):
        get_app().layout.focus_previous()

    @bindings.add(Keys.Right)
    @bindings.add(Keys.Tab)
    def _(event):
        get_app().layout.focus_next()

    return bindings


def __append_custom_bindings(bindings):
    @bindings.add(Keys.Any)
    def _(event):
        def is_valid_char():
            # True: Input '!' has key '!' and data '!'
            # False: Input 'Ctrl+B' has key 'c-b', but data '\x02'
            return event.data == event.key_sequence[0].key

        def check_control_7():
            keypress = event.key_sequence[0]
            if keypress.key == 'c-_' and keypress.data == '\x1f':
                keys.handle_comment()
            return

        if not is_valid_char():
            check_control_7()
            return
        char = event.data
        keys.handle_char(char)

    @bindings.add(Keys.Escape)
    def _(event):
        def check_control_slash():
            sequences = ('[1;5o', 'O5o')  # different sequences for Ctrl + / (Numpad) in different terminals
            if len(queue) not in (len(sequence) for sequence in sequences):
                return
            for sequence in sequences:
                for index, char in enumerate(sequence):
                    keypress = queue[index]
                    if char != keypress.key or char != keypress.data:
                        break
                keys.handle_comment()
                return

        queue = event.key_processor.empty_queue()
        if queue:
            check_control_slash()
            return  # no pure Esc key, e.g. Alt+F10 escape sequence
        actions.handle_exit()

    # Disabling save_before for actions that don't manipulate text in order to keep redo functionality
    @bindings.add(Keys.ControlS, save_before=lambda _: False)
    def _(event):
        keys.handle_save()

    @bindings.add(Keys.F7, save_before=lambda _: False)
    def _(event):
        actions.handle_menu()

    @bindings.add(Keys.F12, save_before=lambda _: False)
    def _(event):
        actions.handle_readme()

    @bindings.add(Keys.ControlSpace, save_before=lambda _: False)
    def _(event):
        keys.handle_autocomplete()

    @bindings.add(Keys.Enter)
    def _(event):
        keys.handle_enter()

    @bindings.add(Keys.ControlN)
    def _(event):
        keys.handle_jump_to_new_line()

    @bindings.add(Keys.Tab)
    def _(event):
        keys.handle_tab()

    @bindings.add(Keys.BackTab)
    def _(event):
        keys.handle_backtab()

    @bindings.add(Keys.Backspace)
    def _(event):
        keys.handle_backspace()

    @bindings.add(Keys.Delete)
    def _(event):
        keys.handle_delete()

    @bindings.add(Keys.Left, save_before=lambda _: False)
    def _(event):
        keys.handle_arrow(Direction.Left)

    @bindings.add(Keys.Right, save_before=lambda _: False)
    def _(event):
        keys.handle_arrow(Direction.Right)

    @bindings.add(Keys.Up, save_before=lambda _: False)
    def _(event):
        keys.handle_arrow(Direction.Up)

    @bindings.add(Keys.Down, save_before=lambda _: False)
    def _(event):
        keys.handle_arrow(Direction.Down)

    @bindings.add(Keys.ShiftLeft, save_before=lambda _: False)
    def _(event):
        keys.handle_shift_arrow(Direction.Left)

    @bindings.add(Keys.ShiftRight, save_before=lambda _: False)
    def _(event):
        keys.handle_shift_arrow(Direction.Right)

    @bindings.add(Keys.ShiftUp, save_before=lambda _: False)
    def _(event):
        keys.handle_shift_arrow(Direction.Up)

    @bindings.add(Keys.ShiftDown, save_before=lambda _: False)
    def _(event):
        keys.handle_shift_arrow(Direction.Down)

    @bindings.add(Keys.ControlZ, save_before=lambda _: False)
    def _(event):
        keys.handle_undo()

    @bindings.add(Keys.ControlY, save_before=lambda _: False)
    def _(event):
        keys.handle_redo()

    @bindings.add(Keys.ControlX)
    def _(event):
        keys.handle_cut()

    @bindings.add(Keys.ControlA, save_before=lambda _: False)
    def _(event):
        keys.handle_select_all()

    @bindings.add(Keys.ControlC, save_before=lambda _: False)
    def _(event):
        keys.handle_copy()

    @bindings.add(Keys.ControlV)
    def _(event):
        keys.handle_paste()

    @bindings.add(Keys.PageUp, save_before=lambda _: False)
    def _(event):
        Globals.text_field.buffer.exit_selection()
        scroll_backward(event)

    @bindings.add(Keys.PageDown, save_before=lambda _: False)
    def _(event):
        Globals.text_field.buffer.exit_selection()
        scroll_forward(event)

    @bindings.add(Keys.ShiftPageUp, save_before=lambda _: False)
    def _(event):
        Globals.text_field.buffer.exit_selection()
        scroll_backward(event, half=True)

    @bindings.add(Keys.ShiftPageDown, save_before=lambda _: False)
    def _(event):
        Globals.text_field.buffer.exit_selection()
        scroll_forward(event, half=True)

    @bindings.add(Keys.Home, save_before=lambda _: False)
    def _(event):
        keys.handle_home()

    @bindings.add(Keys.End, save_before=lambda _: False)
    def _(event):
        keys.handle_end()

    @bindings.add(Keys.ControlHome, save_before=lambda _: False)
    @bindings.add(Keys.ControlPageUp, save_before=lambda _: False)
    def _(event):
        keys.handle_control_home()

    @bindings.add(Keys.ControlEnd, save_before=lambda _: False)
    @bindings.add(Keys.ControlPageDown, save_before=lambda _: False)
    def _(event):
        keys.handle_control_end()

    @bindings.add(Keys.ShiftHome, save_before=lambda _: False)
    def _(event):
        keys.handle_select_rest_of_line(Direction.Left)

    @bindings.add(Keys.ShiftEnd, save_before=lambda _: False)
    def _(event):
        keys.handle_select_rest_of_line(Direction.Right)

    @bindings.add(Keys.ControlLeft, save_before=lambda _: False)
    def _(event):
        keys.handle_control_arrow(Direction.Left)

    @bindings.add(Keys.ControlRight, save_before=lambda _: False)
    def _(event):
        keys.handle_control_arrow(Direction.Right)

    @bindings.add(Keys.ControlUp)
    def _(event):
        keys.handle_control_arrow(Direction.Up)

    @bindings.add(Keys.ControlDown)
    def _(event):
        keys.handle_control_arrow(Direction.Down)

    @bindings.add(Keys.ControlF, save_before=lambda _: False)
    def _(event):
        actions.handle_find()

    @bindings.add(Keys.ControlR)
    def _(event):
        actions.handle_replace()

    @bindings.add(Keys.ControlK)
    def _(event):
        keys.handle_comment()

    @bindings.add(Keys.ControlW, save_before=lambda _: False)
    def _(event):
        keys.handle_select_word_under_cursor()

    @bindings.add(Keys.ControlT)
    def _(event):
        keys.handle_toggle_case()

    @bindings.add(Keys.ControlG, save_before=lambda _: False)
    def _(event):
        actions.handle_git_revert()

    @bindings.add(Keys.BracketedPaste)  # real "paste" event (e.g. Ctrl+Shift+V)
    def _(event):
        text = event.data
        keys.handle_paste(text)

    @bindings.add(Keys.ControlB, save_before=lambda _: False)
    def _(event):
        actions.handle_toggle_git_blame()
