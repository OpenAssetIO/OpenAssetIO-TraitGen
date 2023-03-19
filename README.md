# OpenAssetIO Code Generation Tool

The `openassetio-traitgen` tool can be used to generate Trait and
Specification classes from a simple YAML description. This avoids
the laborious and error-prone task of creating these by hand.

This package is entirely self-contained and can be used without an
[OpenAssetIO](https://github.com/OpenAssetIO/OpenAssetIO)
installation. It provides code generation CLI, along with a
corresponding python package that can be used for custom generation.

## Supported languages

- Python 3.7+
- C++ 17+

## Installation

The package is available on PyPI, so to get the latest stable release
```bash
python -m pip install openassetio-traitgen
```

For the bleeding edge, the package can also be installed after cloning
this repository using

```bash
python -m pip install .
```

## Usage

```bash
openassetio-traitgen -h
```

## Development notes

This package follows the main
[OpenAssetIO contribution process](https://github.com/OpenAssetIO/OpenAssetIO/blob/main/contributing/PROCESS.md).

However, as an (almost) pure Python project, it adheres to strict PEP-8
naming conventions.

We recommend using a suitably configured Python virtual environment for
all development work.

To run the project tests, first install the test pre-requisites. Note
that though the tool itself has no runtime dependencies on
`openassetio`, the tests require it to verify the functionality of the
auto generated code.

```bash
python -m pip install -r tests/requirements.txt
```

Once this is done, you can then create an editable installation of the
package, and run the tests:

```bash
python -m pip install -e .
python -m pytest
```

### C++ tests

C++ tests run via `pytest` invoking CMake's `ctest` utility. The
dependencies for building/linting/running these tests can be installed
into a Python environment.

```bash
python -m pip install -r tests/ctest-requirements.txt
```

It is possible to execute _only_ the C++ tests.

```bash
python -m pytest -m ctest
```

Note that `ctest` will be skipped unless the
`OPENASSETIO_TRAITGENTEST_CMAKE_PRESET` environment variable is set.
Valid values are `"test"` and `"lint"`, where `"lint"` will perform both
static and dynamic analysis on the generated sources (as well as the
tests themselves).

Also ensure that OpenAssetIO is discoverable via CMake's
[`find_package`](https://cmake.org/cmake/help/v3.24/command/find_package.html).
For example, you may need to set the `CMAKE_PREFIX_PATH` environment
variable to an OpenAssetIO installation.
