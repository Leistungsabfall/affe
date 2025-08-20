from prompt_toolkit.styles import Style

monokai_fixes_style = Style.from_dict({
    'pygments.comment': '#999 noitalic',
    'pygments.comment.preproc': '#ca2',  # cpp: #include
    'pygments.error': '#fff bg:#333',  # e.g. unknown file types, prefer white text over red text
    'pygments.generic.heading': '#fff bold',  # Markdown Header (#)
    'pygments.generic.subheading': '#fff bold',  # Markdown Header (## - ######)
    'pygments.keyword.type': '#f5e',  # cpp: vfc::uint32_t
    'pygments.literal.string.doc': 'noitalic',  # Python multiline comment
    'pygments.literal.string.symbol': '#f50',  # {} in {b} in ansi_key_sequences.txt
    'pygments.literal.string.interpol': '#ae81ff',  # ${VARIABLE} in bash, '{foo} foo' in python
    'pygments.name.builtin':  '#f90',  # Python: self, True, None, ...
    'pygments.name.builtin.pseudo': '#f90',  # Python: self, True, None, ...
    'pygments.name.namespace': '#f8f8f2',  # Python imports (import <name>)
    'pygments.name.variable': '#f8f8f2',  # bashrc: PATH
    'pygments.name.variable.magic': '#77f',  # Python: __name__
    'pygments.operator.word': '#66d9ef',  # Python: and, not, in ...
    'pygments.punctuation': '#6ff',  # Python: () [] ,
})
