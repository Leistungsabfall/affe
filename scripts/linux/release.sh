#!/bin/bash

RELEASE_USING_DOCKER_SCRIPT="release_using_ubuntu_1804_docker.sh"
ROOT_DIR=$(realpath $(dirname $0)/../..)
VERSION_STRING="$2"

if [ "$1" != "--override" ]; then
    echo
    echo "Please use '$RELEASE_USING_DOCKER_SCRIPT' script."
    exit 1
fi

ensure_backwards_compatibility() {
    expected="18.04"
    actual=$(grep '^VERSION_ID=' /etc/os-release | cut -d'"' -f 2)
    if [ $expected != $actual ]; then
        echo
        echo "Expected Ubuntu $expected, got $actual in '$RELEASE_USING_DOCKER_SCRIPT'."
        exit 1
    fi
}

ensure_on_main_branch() {
    echo
    echo "Checking if current branch is main..."
    branch=$(git rev-parse --abbrev-ref HEAD)
    if [ "$branch" != "main" ]; then
        echo
        echo "Current branch is '$branch'"
        exit 1
    fi
    echo "...OK"
}

ensure_no_untracked_files() {
    echo
    echo "Checking for untracked files..."
    files=$(git ls-files --others --exclude-standard)
    if [ "$files" != "" ]; then
        echo
        echo "====="
        git status
        echo "====="
        echo
        echo "Found some untracked files"
        exit 1
    fi
    echo "...OK"
}

ensure_no_uncommitted_changes() {
    echo
    echo "Checking for uncommitted changes..."
    git diff-index --quiet HEAD --
    if [ $? != 0 ]; then
        echo
        echo "====="
        git status
        echo "====="
        echo
        echo "Found some uncommitted changes"
        exit 1
    fi
    echo "...OK"
}

ensure_no_unpushed_commits() {
    echo
    echo "Checking for unpushed commits..."
    local_commit_id=$(git log | head -n 1 | cut -d ' ' -f 2)
    remote_commit_id=$(git log origin/main | head -n 1 | cut -d ' ' -f 2)
    if [ "$local_commit_id" != "$remote_commit_id" ]; then
        echo
        echo "====="
        git status
        echo "====="
        echo
        echo "Found unpushed commit(s)"
        exit 1
    fi
    echo "...OK"
}

check_git_tag() {
    echo
    echo "Checking if current commit is tagged..."
    git_tag=$(git describe --tags --exact-match HEAD)
    if [ $? == 0 ]; then
        echo
        echo "Current commit is already tagged with tag '$git_tag'."
        exit 1
    fi
    echo "...OK"
}

test_and_build() {
    echo
    VERSION_STRING=$VERSION_STRING ./scripts/linux/build.sh || exit 1
}

cd $ROOT_DIR
ensure_backwards_compatibility
ensure_on_main_branch
ensure_no_untracked_files
ensure_no_uncommitted_changes
ensure_no_unpushed_commits
check_git_tag
test_and_build
