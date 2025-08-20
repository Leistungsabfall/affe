def get_readme():
    try:
        import tmp_readme_module
        return tmp_readme_module.readme
    except ImportError:
        with open('README.md', 'r', encoding='utf-8') as file_:
            return file_.read()
