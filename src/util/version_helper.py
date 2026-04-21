import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FILE_NAME = 'version.txt'

def get_version():
    for path in (FILE_NAME, 'res/{}'.format(FILE_NAME)):
        try:
            with open(os.path.join(PROJECT_ROOT, path), 'r', encoding='utf-8') as file_:
                version = file_.read().strip()
                return version
        except FileNotFoundError:
            continue
    return 'dev'
