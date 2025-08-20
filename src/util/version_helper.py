def get_version():
    try:
        import tmp_version_module
        return tmp_version_module.version
    except ImportError:
        return 'dev'
