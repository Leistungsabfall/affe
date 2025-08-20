#!/bin/bash
set -e

ROOT_DIR=$(realpath $(dirname $0)/../..)
VERSION_STRING="$1"
GID=$(id -g)
IMAGE="ubuntu:18.04"
COMMAND="mv env/ /tmp/env_bak/; \
        cp -r /tmp_ssh /root/.ssh && \
        apt update && \
        apt install -y sudo python3.8-dev python3.8-venv python3-pip && \
        update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1 && \
        update-alternatives --set python3 /usr/bin/python3.8 && \
        ./scripts/linux/setup.sh && \
        export USER=$USER && \
        git config --global --add safe.directory /workdir && \
        ./scripts/linux/release.sh --override $VERSION_STRING && \
        rm -r env/ && \
        mv /tmp/env_bak/ env/; \
        chown $UID:$GID bin/affe"

cd $ROOT_DIR

if [ -z "$VERSION_STRING" ]; then
    echo
    echo "Usage: $0 <version_string>"
    exit 1
fi

docker pull $IMAGE  # for possible updates

docker run \
    -it \
    --network host \
    -v $ROOT_DIR:/workdir \
    -v ~/.ssh:/tmp_ssh \
    -w /workdir \
    $IMAGE \
    sh -c "$COMMAND"

echo "Updating version info file in bin directory..."
echo "$VERSION_STRING" > bin/version.txt
echo "... done"
echo
echo "To finish the release, perform the following steps:"
echo "  1. Commit and push the updated binary 'bin/affe' and 'bin/version.txt'"
echo "  2. On Windows:"
echo "    2.1 Make sure the repo is up to date"
echo "    2.2 Call 'release.bat $VERSION_STRING'"
echo "    2.3 Commit and push the changes"
echo "    2.4 Tag the release: 'git tag $VERSION_STRING' and 'git push --tags'"
echo
