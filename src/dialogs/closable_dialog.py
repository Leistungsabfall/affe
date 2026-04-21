import time
from threading import Thread

from prompt_toolkit.application import get_app
from prompt_toolkit.eventloop import Future, From, Return, ensure_future
from prompt_toolkit.layout import Float
from prompt_toolkit.widgets import Dialog


class TextUpdateThread(Thread):
    def __init__(self, dialog, texts, interval):
        self.dialog = dialog
        self.texts = texts
        self.interval = interval
        self.current_index = -1
        self.running = True
        super().__init__(daemon=True)

    def run(self):
        index = 1
        while self.running:
            time.sleep(self.interval)
            label = self.dialog.body.children[0].content
            label.text = self.texts[index % len(self.texts)]
            get_app().invalidate()
            index += 1


class ClosableDialog:
    def __init__(self, toggle_texts=None, toggle_interval=0.0, *args, **kwargs):
        self.future = Future()
        self.dialog = Dialog(close_callback=self.close, *args, **kwargs)
        self.text_update_thread = None

        if toggle_interval and toggle_texts is not None:
            self.text_update_thread = TextUpdateThread(self.dialog, toggle_texts, toggle_interval)
            self.text_update_thread.start()

    def show(self):
        def coroutine():
            yield From(self.__show_as_float())

        ensure_future(coroutine())

    def close(self):
        if self.text_update_thread is not None:
            self.text_update_thread.running = False
        self.future.set_result(None)

    def __pt_container__(self):
        return self.dialog

    def __show_as_float(self):
        float_ = Float(content=self)
        get_app().layout.container.floats.insert(0, float_)

        focused_before = get_app().layout.current_window
        get_app().layout.focus(self)
        result = yield self.future
        get_app().layout.focus(focused_before)

        if float_ in get_app().layout.container.floats:
            get_app().layout.container.floats.remove(float_)

        raise Return(result)
