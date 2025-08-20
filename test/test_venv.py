import unittest

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata


def get_requirement(name):
    with open('requirements.txt', 'r') as file:
        for line in file.readlines():
            if line.startswith(name):
                return line.strip()
        raise ValueError('Package {name} not found in requirements.txt'.format(name=name))


class TestVenv(unittest.TestCase):
    def __check_requirement(self, requirement, installed_version):
        if not requirement.endswith(installed_version):
            self.fail(
                'Expected requirement {requirement} but got {installed_version}.\n'
                'Looks like the virtual environment is outdated.\n'
                'Fix it by running setup again:\n\n'
                '    ./setup.sh'.format(
                    requirement=requirement, installed_version=installed_version
                )
            )

    def test_package_versions(self):
        packages = (
            'coverage',
            'pygments',
            'pyinstaller',
            'six',
            'wcwidth',
            'wheel',
        )
        for package in packages:
            self.__check_requirement(
                requirement=get_requirement(package),
                installed_version=metadata.version(package),
            )
