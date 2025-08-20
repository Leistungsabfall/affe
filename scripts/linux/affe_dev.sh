#!/bin/bash

ROOT_DIR=$(realpath $(dirname $0)/../..)
export PYTHONPATH="$PYTHONPATH:$ROOT_DIR/python-prompt-toolkit"

activate_virtualenv() {
    . $ROOT_DIR/env/bin/activate
}

activate_virtualenv
python $ROOT_DIR/src/main.py "$@"
