import time
from threading import Thread

from background_update.tasks import update_git_info, check_for_git_revert_result, check_for_external_changes, \
    update_lexer, invalidate_app, update_git_blame
from globals import Globals


class AutoUpdateThread(Thread):
    SUB_INTERVAL_SECONDS = 0.1
    MULTIPLIER = 10

    def __init__(self):
        super().__init__(daemon=True)

    def run(self):
        while True:
            check_for_external_changes.run()
            check_for_git_revert_result.run()
            update_lexer.run()
            update_git_info.run()
            update_git_blame.run()
            invalidate_app.run()
            for i in range(self.MULTIPLIER):
                time.sleep(self.SUB_INTERVAL_SECONDS)
                if Globals.exit_request:
                    return
