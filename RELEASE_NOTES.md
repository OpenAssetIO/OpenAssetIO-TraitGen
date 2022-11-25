Release Notes
=============

v1.0.0-alpha.4

### Breaking Changes

- Changed `generate` interface from `languages` to `generator` when
  specifying generation targets. Removed ability for more than one
  `generator` to be run simultaneously.

- Removed `--python` option from command line interface, replaced with
  `--generator={generator}` option.

- Python generator no longer places module underneath `python`
  subdirectory, opting now to place module folder directly in
  `output_directory`

v1.0.0-alpha.3
--------------

### New Features

- Initial release. Branched from OpenAssetIO project from
 [this point forward](https://github.com/OpenAssetIO/OpenAssetIO/commit/a5a393178b522121e1afe2fdac4da1f4c81ac9d4).
