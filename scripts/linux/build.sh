#!/bin/bash
set -e

APP_NAME="affe"
ROOT_DIR=$(realpath $(dirname $0)/../..)
TMP_README_MODULE="src/tmp_readme_module.py"
TMP_CHANGELOG_MODULE="src/tmp_changelog_module.py"
TMP_LICENSE_MODULE="src/tmp_license_module.py"
TMP_THIRD_PARTY_LICENSES_MODULE="src/tmp_third_party_licenses_module.py"
TMP_VERSION_MODULE="src/tmp_version_module.py"

ensure_env_exists() {
    if ! [ -d env ]; then
        echo "env/ dir is missing. Please run ./setup.sh first"
        exit 1
    fi
}

activate_virtualenv() {
    . env/bin/activate
}

run_tests() {
    echo "Running unit tests:"
    python -m unittest discover test/ -f || { echo -e "\nAll tests have to pass. Aborting."; exit 1; }
    echo
}

create_readme_info() {
    readme=$(<README.md)
    echo "readme = r'''$readme'''" > $TMP_README_MODULE
}

create_changelog_info() {
    changelog=$(<CHANGELOG.md)
    echo "changelog = r'''$changelog'''" > $TMP_CHANGELOG_MODULE
}

create_license_info() {
    license=$(<LICENSE)
    echo "license = r'''$license'''" > $TMP_LICENSE_MODULE
}

create_third_party_licenses_info() {
    third_party_licenses=$(<third-party-licenses.txt)
    echo "third_party_licenses = r'''$third_party_licenses'''" > $TMP_THIRD_PARTY_LICENSES_MODULE
}

create_version_info() {
    if [ -z "$VERSION_STRING" ]; then
        version="dev"
    else
        version=$VERSION_STRING
    fi
    echo "version = '$version'" > $TMP_VERSION_MODULE
}

freeze_app() {
    echo "Building application:"
    PYTHONOPTIMIZE=2 pyinstaller --distpath "." --paths=$ROOT_DIR/python-prompt-toolkit --onefile --name $APP_NAME src/main.py || exit 1
    mv affe bin/affe
    echo
}

cleanup() {
    rm -r build $APP_NAME.spec $TMP_README_MODULE $TMP_CHANGELOG_MODULE $TMP_LICENSE_MODULE $TMP_THIRD_PARTY_LICENSES_MODULE $TMP_VERSION_MODULE
}

cd $ROOT_DIR
ensure_env_exists
activate_virtualenv
run_tests
create_readme_info
create_changelog_info
create_license_info
create_third_party_licenses_info
create_version_info
freeze_app
cleanup
echo "Build finished"
