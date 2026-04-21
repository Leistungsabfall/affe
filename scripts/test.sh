#!/usr/bin/env sh

activate_virtualenv() {
    . env/bin/activate
}

activate_virtualenv
coverage run \
    --source=handlers.keys,util.text_helper,util.lexer_helper \
    -m unittest discover "test" "$@" || exit 1
echo
coverage report -m --fail-under=100
