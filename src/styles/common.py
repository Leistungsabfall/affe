from prompt_toolkit.styles import Style

common_style = Style.from_dict({
    'control-character': '#fff bold',  # e.g. ^[[ bash escape sequences in log files

    'git-added': '#0b0',
    'git-modified': '#ea0',
    'git-deleted': '#c00',

    'todo-comment': '#444 bg:#EE0',

    'git-modified-indicator': '#f00',

    'git-branch': '#0ff',

    'read-only-indicator': 'bold',
})
