Release Notes
=============

v1.0.0-alpha.x
--------------

### Breaking changes

- Removed support for VFX Reference Platform CY22 or lower and added
  support for CY24. This means Python 3.7 and 3.9 builds are no longer
  tested or published, whereas Python 3.11 is now published.
  [OpenAssetIO#1351](https://github.com/OpenAssetIO/OpenAssetIO/issues/1351)

v1.0.0-alpha.9
--------------

### Breaking Changes

- C++ `getProperty` methods now return `std::optional<T>` rather
  than throwing when invoked without a default parameter. This mirrors
  the python behaviour of returning `None` in this case.
  [#57](https://github.com/OpenAssetIO/OpenAssetIO-TraitGen/issues/57)

v1.0.0-alpha.8
--------------

### Breaking Changes

- Updated to use non-deprecated version of `TraitsData`.
  Due to this, the required runtime openassetio version is now beta
  1.0.0.
  [#1127](https://github.com/OpenAssetIO/OpenAssetIO/issues/1127)

### Improvements

- Pinned `setuptools` version used to build from source to `68.x`, which
  is the latest version to maintain compatability with Python 3.7.
  [#59](https://github.com/OpenAssetIO/OpenAssetIO-TraitGen/issues/59)

### Bug fixes

- Added support for `setuptools` `69.0.0` and above. This `setuptools`
  update removed transitionary support for mismatched `setup.py` and
  `pyproject.toml` configurations. `setup.py` has been removed.
  [#59](https://github.com/OpenAssetIO/OpenAssetIO-TraitGen/issues/59)

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
