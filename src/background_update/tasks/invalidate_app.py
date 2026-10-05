from globals import Globals
from prompt_toolkit.application import get_app


class _Cache:
    render_state = None


def get_render_state():
    """
    Everything the background tasks may change which is visible on screen.
    """
    app = get_app()
    return (
        Globals.saved_text,
        Globals.text_field.lexer,
        Globals.git_dir,
        Globals.git_status_by_line,
        Globals.git_branch,
        Globals.git_dirty_indicator,
        Globals.git_untracked,
        Globals.git_blame_active,
        Globals.git_blame_by_line,
        app.layout.current_window,
        tuple(getattr(app.layout.container, 'floats', ())),
    )


def run():
    render_state = get_render_state()
    if render_state == _Cache.render_state:
        return  # nothing changed, so there's no need to redraw
    _Cache.render_state = render_state
    get_app().invalidate()
