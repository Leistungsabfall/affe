class Globals:
    read_only = False

    text_field = None
    git_status_by_line = dict()
    git_blame_active = False
    git_blame_by_line = []
    saved_text = ''
    save_in_progress = False
    file_name = ''
    file_path = ''
    exit_request = False

    show_find_window = False
    show_replace_window = False

    find_toolbar = None
    find_toolbar_text_field = None
    find_toolbar_up_button = None
    find_toolbar_down_button = None
    find_toolbar_match_case_checkbox = None
    find_toolbar_close_button = None

    replace_toolbar = None
    replace_toolbar_text_field = None
    replace_toolbar_replace_button = None
    replace_toolbar_replace_all_button = None

    root_container = None

    git_revert_failed = False

    git_branch = ''
    git_dirty_indicator = False

    git_dir = ''
    relative_file_path_from_git_dir = ''
    git_untracked = True

    git_blame_menu_item = None
