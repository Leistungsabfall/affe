#!/bin/bash
set -e

ROOT_DIR=$(realpath $(dirname $0)/../..)

install_dependencies() {
    common="git"
    clipboard="xclip"
    pyinstaller="binutils"
    sudo apt -y install $common $clipboard $pyinstaller
}

install_python3.8() {
    if ! command -v python3.8 > /dev/null; then
        echo "Installing Python 3.8"
        scripts/linux/install_python3.8.sh
    fi
}

create_virtualenv() {
    python3.8 -m venv env
}

activate_virtualenv() {
    . env/bin/activate
}

upgrade_pip() {
    pip install --upgrade pip
}

install_env_dependencies() {
    pip install --upgrade -r requirements.txt
}

create_symlink() {
    echo "Creating symlink as /usr/local/bin/affe"
    sudo rm -f /usr/local/bin/affe
    sudo ln -s $ROOT_DIR/bin/affe /usr/local/bin/affe
}

cd $ROOT_DIR
install_dependencies
install_python3.8
create_virtualenv
activate_virtualenv
upgrade_pip
install_env_dependencies
create_symlink
