from prompt_toolkit.styles import Style

dark_style = Style.from_dict({
    '': '#ccc bg:#333',
    'shadow': 'bg:#444',

    'statusbar': 'bg:#444',

    'scrollbar.background': 'bg:#444',

    'git-info-margin': 'bg:#444',
    'git-info-margin-active': 'bg:#2ae',

    'line-number': 'bg:#444',
    'current-line-number': '#444 bg:#888',

    'menu-bar': '#ccc bg:#333',
    'menu-bar.selected-item': '#fff bg:#666',
    'menu menu-bar.selected-item': '#fff bg:#333',
    'menu': '#fff bg:#666',

    'dialog.body': '#fff bg:#777',
    'dialog.body text-area': 'bg:#333',

    'dialog frame.label': '#fff bold',  # e.g. title of exit dialog
    'button.focused': '#fff bg:#333',  # e.g. buttons in exit dialog
    'checkbox.focused': '#fff bg:#333',

    'leading-whitespace': '#777',
    'trailing-whitespace': '#777',
    'multiple-whitespace': '#777',
    'tab': '#777',
    'matching-bracket.cursor': '#fd0 bg:#333 bold',
    'matching-bracket.other': '#fd0 bg:#333 bold',
    'word-under-cursor': '#6f6',

    'scrollbar.button': 'bg:#888',

    'find-and-replace-toolbar': '#ccc bg:#444',
    'find-and-replace-textfield': '#000 bg:#aaa',
    'find-and-replace-textfield-no-match': '#000 bg:#faa',
    'search': '#222 bg:#ff2',
    'search.current': '#222 bg:#f92',
})
