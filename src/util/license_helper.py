def get_license():
    try:
        import tmp_license_module
        return tmp_license_module.license
    except ImportError:
        with open('LICENSE', 'r', encoding='utf-8') as file_:
            return file_.read()
