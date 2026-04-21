#!/usr/bin/env sh
set -eu

TARGET_DIR="$1"

rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR/res"

cp scripts/affe "$TARGET_DIR"
cp -R lib "$TARGET_DIR/res"
cp -R src "$TARGET_DIR/res"
cp CHANGELOG.md "$TARGET_DIR/res"
cp LICENSE "$TARGET_DIR/res"
cp README.md "$TARGET_DIR/res"
cp requirements.txt "$TARGET_DIR/res"
cp third-party-licenses.txt "$TARGET_DIR/res"
cp version.txt "$TARGET_DIR/res" 2>/dev/null || true
