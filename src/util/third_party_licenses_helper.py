def get_third_party_licenses():
    try:
        import tmp_third_party_licenses_module
        return tmp_third_party_licenses_module.third_party_licenses
    except ImportError:
        with open('third-party-licenses.txt', 'r', encoding='utf-8') as file_:
            return file_.read()
