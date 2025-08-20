def get_changelog():
    try:
        import tmp_changelog_module
        return tmp_changelog_module.changelog
    except ImportError:
        with open('CHANGELOG.md', 'r', encoding='utf-8') as file_:
            return file_.read()
