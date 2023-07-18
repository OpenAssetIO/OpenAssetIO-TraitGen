Release Notes
=============

v1.0.0-alpha.7
--------------

### Bug fixes

- Bumped `pyyaml` version to `6.0.0` to avoid issues with `cython` 3+,
  and `conan` `1.60.1` to be compatible with `pyyaml` `6.0.0`.
  [pyyaml/#601](https://github.com/yaml/pyyaml/issues/601)

v1.0.0-alpha.6
--------------

### Improvements

- Removed dependence on `TraitsBase` and `SpecificationBase` types in
  generated python code, rather generating the functionality previously
  provided by the base directly into the traits and specifications. This
  mirrors the approach taken by the C++ generator, and breaks a
  dependency on OpenAssetIO.
  [#19](https://github.com/OpenAssetIO/OpenAssetIO-TraitGen/issues/19)

v1.0.0-alpha.5
--------------

### New Features

- Added C++ trait and specification class generation, where the
  generated source tree consists of a header-only package, with a header
  file per class along with hoisting headers for convenience, broadly
  mirroring the source tree of the Python generator.
  [#11](https://github.com/OpenAssetIO/OpenAssetIO-TraitGen/issues/11)

### Bug fixes

- Fixed line breaks to no longer be platform-specific, and instead
  conform to Unix-style `\n`.

v1.0.0-alpha.4
--------------

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
