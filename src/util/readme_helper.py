import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FILE_NAME = 'README.md'


def get_readme():
    for path in (FILE_NAME, 'res/{}'.format(FILE_NAME)):
        try:
            with open(os.path.join(PROJECT_ROOT, path), 'r', encoding='utf-8') as file_:
                return file_.read()
        except FileNotFoundError:
            continue
    raise FileNotFoundError('{} not found'.format(FILE_NAME))
