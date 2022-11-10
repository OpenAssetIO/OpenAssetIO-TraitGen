# OpenAssetIO Code Generation Tool

The `openassetio-traitgen` tool can be used to generate Trait and
Specification classes from a simple YAML description. This avoids
the laborious and error-prone task of creating these by hand.

This package is entirely self-contained and can be used without an
`openassetio` installation. It provides code generation CLI, along with
a corresponding python package that can be used for custom generation.

## Supported languages

- Python 3.7+

## Installation

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

However, as a pure Python project, it adheres to strict PEP-8 naming
conventions.

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
