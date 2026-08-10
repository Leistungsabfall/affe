# Changelog

## 1.1.4 - 2026-08-10

* Improve emoji support
* Update terminal title with current file name
* Update dependencies

## 1.1.3 - 2026-07-12

* Improve startup time by lazy-loading some imports
* Add lexer support for the following files:
  * `.npmrc`
  * `Kustomization`

## 1.1.2 - 2026-06-15

* Add `-v, --version` flag to display the current version of `affe` and exit.
* Fix Wayland clipboard paste appending a spurious trailing newline.

## 1.1.1 - 2026-04-28

* Fix `TextWithCommentLexer` to correctly handle inline comments by ensuring a space before the `#` is required for it to be recognized as a comment. This prevents valid text containing `#` from being misclassified as a comment.

## 1.1.0 - 2026-04-24

* Re-release after move to GitHub and using GitHub releases for distribution
* **Hint:** The update process has been changed. If you have installed a previous version of `affe` < `1.1.0`, please delete it from `/usr/local/bin/affe` before installing the new version.
