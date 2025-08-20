#!/bin/bash

ROOT_DIR=$(realpath $(dirname $0)/../..)

install_dependencies() {
    sudo apt -y install build-essential libssl-dev zlib1g-dev libbz2-dev \
                        libreadline-dev libsqlite3-dev wget curl llvm \
                        libncurses5-dev libncursesw5-dev xz-utils tk-dev \
                        libffi-dev liblzma-dev python3-openssl git
}

extract_source_code() {
    tar -xf setup/Python-3.8.20.tgz
}

build_python_from_sources() {
    cd Python-3.8.20/
    ./configure --enable-optimizations --enable-shared
    make -j$(nproc)
    sudo make altinstall
    sudo cp /usr/local/lib/libpython3.8.so.1.0 /usr/lib
}

cleanup() {
    cd $ROOT_DIR
    sudo rm -rf Python-3.8.20/
}

cd $ROOT_DIR
install_dependencies
extract_source_code
build_python_from_sources
cleanup
