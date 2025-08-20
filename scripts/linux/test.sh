#!/bin/bash

ROOT_DIR=$(realpath $(dirname $0)/../..)

activate_virtualenv() {
    . env/bin/activate
}

cd $ROOT_DIR
activate_virtualenv
coverage run \
    --source=handlers.keys,util.text_helper,util.lexer_helper \
    -m unittest discover $ROOT_DIR/test "$@" || exit 1
echo
coverage report -m
rm .coverage
