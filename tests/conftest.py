#
#   Copyright 2022 The Foundry Visionmongers Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""
Shared fixtures for traitgen tests
"""

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=missing-class-docstring,missing-function-docstring

import logging
import os
import yaml

import pytest

from openassetio_traitgen import datamodel


@pytest.fixture(scope="package")
def resources_dir():
    """
    The path to the resources directory for this test suite
    """
    test_dir = os.path.dirname(__file__)
    return os.path.join(test_dir, "resources")


@pytest.fixture(scope="package")
def yaml_path_all(resources_dir):
    return os.path.join(resources_dir, "openassetio-traitgen-test-all.yaml")


@pytest.fixture(scope="package")
def yaml_path_traits_only(resources_dir):
    return os.path.join(resources_dir, "openassetio-traitgen-test-traits-only.yaml")


@pytest.fixture(scope="package")
def yaml_path_specifications_only(resources_dir):
    return os.path.join(resources_dir, "openassetio-traitgen-test-specifications-only.yaml")


@pytest.fixture(scope="package")
def yaml_path_invalid(resources_dir):
    return os.path.join(resources_dir, "invalid.yaml")


@pytest.fixture(scope="package")
def yaml_path_invalid_values(resources_dir):
    return os.path.join(resources_dir, "invalid_values.yaml")


@pytest.fixture(scope="package")
def yaml_path_minimal(resources_dir):
    return os.path.join(resources_dir, "minimal.yaml")


@pytest.fixture(scope="package")
def description_all(yaml_path_all):
    with open(yaml_path_all, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_traits_only(yaml_path_traits_only):
    with open(yaml_path_traits_only, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_specifications_only(yaml_path_specifications_only):
    with open(yaml_path_specifications_only, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_invalid(yaml_path_invalid):
    with open(yaml_path_invalid, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_invalid_values(yaml_path_invalid_values):
    with open(yaml_path_invalid_values, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_minimal(yaml_path_minimal):
    with open(yaml_path_minimal, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


@pytest.fixture(scope="package")
def description_exotic_values():
    return {
        "package": "p📦p",
        "description": "p",
        "traits": {
            "t!n": {
                "description": "n",
                "members": {
                    "t&": {
                        "versions": {
                            "1": {
                                "description": "t",
                                "properties": {"p$": {"type": "boolean", "description": "p"}},
                            }
                        }
                    }
                },
            }
        },
        "specifications": {
            "s!n": {
                "description": "",
                "members": {
                    "s^": {
                        "versions": {
                            "1": {
                                "description": "",
                                "traitSet": [
                                    {
                                        "package": "p📦p",
                                        "namespace": "t!n",
                                        "name": "t&",
                                        "version": "1",
                                    }
                                ],
                            }
                        }
                    }
                },
            }
        },
    }


@pytest.fixture
def declaration_all():
    # By design the parser sorts all namespace, trait, specification lists, and
    # traitSets by id/name to ensure stable generation from dict/map centric
    # descriptions.
    return datamodel.PackageDeclaration(
        id="openassetio-traitgen-test-all",
        description="Test classes to validate the integrity of the openassetio-traitgen tool.",
        traits=[
            datamodel.NamespaceDeclaration(
                id="aNamespace",
                description="A Namespace",
                members=[
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:aNamespace.AllProperties",
                        version="1",
                        name="AllProperties",
                        description="A trait with properties of all types.",
                        usage=[],
                        properties=[
                            datamodel.PropertyDeclaration(
                                id="boolProperty",
                                type=datamodel.PropertyType.BOOL,
                                description="A bool-typed property.",
                            ),
                            datamodel.PropertyDeclaration(
                                id="floatProperty",
                                type=datamodel.PropertyType.FLOAT,
                                description="A float-typed property.",
                            ),
                            datamodel.PropertyDeclaration(
                                id="intProperty",
                                type=datamodel.PropertyType.INTEGER,
                                description="A int-typed property.",
                            ),
                            datamodel.PropertyDeclaration(
                                id="stringProperty",
                                type=datamodel.PropertyType.STRING,
                                description="A string-typed property.",
                            ),
                            # TODO(DF): Add DICT property, once supported.
                        ],
                    ),
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:aNamespace.MultipleVersions",
                        version="1",
                        name="MultipleVersions",
                        description="A trait with multiple versions, version 1.",
                        usage=[],
                        properties=[
                            datamodel.PropertyDeclaration(
                                id="oldProperty",
                                type=datamodel.PropertyType.STRING,
                                description="A deprecated string-typed property.",
                            ),
                        ],
                    ),
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:aNamespace.MultipleVersions.v2",
                        version="2",
                        name="MultipleVersions",
                        description="A trait with multiple versions, version 2.",
                        usage=[],
                        properties=[
                            datamodel.PropertyDeclaration(
                                id="newProperty",
                                type=datamodel.PropertyType.INTEGER,
                                description="A new int-typed property.",
                            ),
                        ],
                    ),
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:aNamespace.NoProperties",
                        version="1",
                        name="NoProperties",
                        description="Another trait, this time with no properties.",
                        properties=[],
                        usage=[],
                    ),
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:aNamespace.NoPropertiesMultipleUsage",
                        version="1",
                        name="NoPropertiesMultipleUsage",
                        description="Another trait, this time with multiple usage.",
                        properties=[],
                        usage=["entity", "relationship"],
                    ),
                ],
            ),
            datamodel.NamespaceDeclaration(
                id="anotherNamespace",
                description="Another Namespace",
                members=[
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-all:anotherNamespace.NoProperties",
                        version="1",
                        name="NoProperties",
                        description="Another NoProperties trait in a different namespace",
                        properties=[],
                        usage=[],
                    ),
                ],
            ),
        ],
        specifications=[
            datamodel.NamespaceDeclaration(
                id="test",
                description="Test specifications.",
                members=[
                    datamodel.SpecificationDeclaration(
                        id="LocalAndExternalTrait",
                        version="1",
                        description=(
                            "A specification referencing traits in this and another package."
                        ),
                        usage=["entity", "managementPolicy"],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.NoProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=(
                                    "openassetio-traitgen-test-all",
                                    "aNamespace",
                                    "NoProperties",
                                ),
                            ),
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-traits-only:aNamespace.NoProperties",
                                package="openassetio-traitgen-test-traits-only",
                                namespace="aNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=(
                                    "openassetio-traitgen-test-traits-only",
                                    "aNamespace",
                                    "NoProperties",
                                ),
                            ),
                        ],
                    ),
                    datamodel.SpecificationDeclaration(
                        id="MultipleVersionsOfTrait",
                        version="1",
                        description=(
                            "Version 1 of a specification referencing version 1 of a trait."
                        ),
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.MultipleVersions",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="MultipleVersions",
                                version="1",
                                unique_name_parts=("MultipleVersions",),
                            ),
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.NoProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=("NoProperties",),
                            ),
                        ],
                    ),
                    datamodel.SpecificationDeclaration(
                        id="MultipleVersionsOfTrait",
                        version="2",
                        description=(
                            "Version 2 of a specification referencing version 2 of a" " trait."
                        ),
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.MultipleVersions.v2",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="MultipleVersions",
                                version="2",
                                unique_name_parts=("MultipleVersions",),
                            ),
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.NoProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=("NoProperties",),
                            ),
                        ],
                    ),
                    datamodel.SpecificationDeclaration(
                        id="OneExternalTrait",
                        version="1",
                        description="A specification referencing traits in another package.",
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-traits-only:test.Another",
                                package="openassetio-traitgen-test-traits-only",
                                namespace="test",
                                name="Another",
                                version="1",
                                unique_name_parts=("Another",),
                            ),
                        ],
                    ),
                    datamodel.SpecificationDeclaration(
                        id="TwoLocalTraits",
                        version="1",
                        description="A specification with two traits.",
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.NoProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=("aNamespace", "NoProperties"),
                            ),
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:anotherNamespace.NoProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="anotherNamespace",
                                name="NoProperties",
                                version="1",
                                unique_name_parts=("anotherNamespace", "NoProperties"),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


@pytest.fixture
def declaration_traits_only():
    return datamodel.PackageDeclaration(
        id="openassetio-traitgen-test-traits-only",
        description=(
            "Test classes to validate the integrity of the openassetio-traitgen tool when only "
            "traits are defined."
        ),
        traits=[
            datamodel.NamespaceDeclaration(
                id="aNamespace",
                description="A namespace that overlaps with the all package",
                members=[
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-traits-only:aNamespace.NoProperties",
                        name="NoProperties",
                        version="1",
                        description="Yet Another No Properties Trait",
                        properties=[],
                        usage=["managementPolicy"],
                    ),
                ],
            ),
            datamodel.NamespaceDeclaration(
                id="test",
                description="A namespace for testing.",
                members=[
                    datamodel.TraitDeclaration(
                        id="openassetio-traitgen-test-traits-only:test.Another",
                        name="Another",
                        version="1",
                        description="Yet Another Trait",
                        properties=[],
                        usage=["managementPolicy"],
                    ),
                ],
            ),
        ],
        specifications=[],
    )


@pytest.fixture
def declaration_specifications_only():
    return datamodel.PackageDeclaration(
        id="openassetio-traitgen-test-specifications-only",
        description=(
            "Test classes to validate the integrity of the openassetio-traitgen tool when only "
            "specifications are defined."
        ),
        traits=[],
        specifications=[
            datamodel.NamespaceDeclaration(
                id="test",
                description="More test specifications.",
                members=[
                    datamodel.SpecificationDeclaration(
                        id="Some",
                        version="1",
                        description="Some specification",
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-all:aNamespace.AllProperties",
                                package="openassetio-traitgen-test-all",
                                namespace="aNamespace",
                                name="AllProperties",
                                version="1",
                                unique_name_parts=("AllProperties",),
                            ),
                            datamodel.TraitReference(
                                id="openassetio-traitgen-test-traits-only:test.Another",
                                package="openassetio-traitgen-test-traits-only",
                                namespace="test",
                                name="Another",
                                version="1",
                                unique_name_parts=("Another",),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )


@pytest.fixture
def declaration_exotic_values():
    """
    A declaration that contains exotic values that should be used to
    ensure generators properly handle a variety of incoming values.

    The up-front description validation presently doesn't allow these
    to be loaded from YAML, but we may relax this constraint in the
    future (eg: as part of l18n), and so its critical that generators
    of ASCII constrained languages sanitize and conform inputs (with
    warnings).
    """
    return datamodel.PackageDeclaration(
        id="p📦p",
        description="p",
        traits=[
            datamodel.NamespaceDeclaration(
                id="t!n",
                description="n",
                members=[
                    datamodel.TraitDeclaration(
                        id="p📦p:t!n.t&",
                        version="1",
                        name="t&",
                        description="t",
                        usage=[],
                        properties=[
                            datamodel.PropertyDeclaration(
                                id="p$", description="p", type=datamodel.PropertyType.BOOL
                            )
                        ],
                    ),
                ],
            ),
        ],
        specifications=[
            datamodel.NamespaceDeclaration(
                id="s!n",
                description="",
                members=[
                    datamodel.SpecificationDeclaration(
                        id="s^",
                        version="1",
                        description="",
                        usage=[],
                        trait_set=[
                            datamodel.TraitReference(
                                id="p📦p:t!n.t&",
                                package="p📦p",
                                namespace="t!n",
                                name="t&",
                                version="1",
                                unique_name_parts=("t&",),
                            )
                        ],
                    )
                ],
            )
        ],
    )


@pytest.fixture(scope="session")
def declaration_invalid_identifiers():
    """
    A declaration that contains given identifiers (or a valid identifier
    if not given) that should be used to ensure generators properly
    throw an error when encountered.
    """

    def fn(package_name=None, specification_namespace=None, trait_namespace=None):
        return datamodel.PackageDeclaration(
            id=(package_name or "valid_package"),
            description="",
            traits=[
                datamodel.NamespaceDeclaration(
                    id=(trait_namespace or "valid_namespace"),
                    description="",
                    members=[
                        datamodel.TraitDeclaration(
                            id="some_trait",
                            version="1",
                            name="some_trait",
                            description="",
                            usage=[],
                            properties=[],
                        ),
                    ],
                ),
            ],
            specifications=[
                datamodel.NamespaceDeclaration(
                    id=(specification_namespace or "valid_namespace"),
                    description="",
                    members=[
                        datamodel.SpecificationDeclaration(
                            id="some_specification",
                            version="1",
                            description="",
                            usage=[],
                            trait_set=[
                                datamodel.TraitReference(
                                    id="some_trait",
                                    name="some_trait",
                                    namespace="some_namespace",
                                    package="some_package",
                                    version="1",
                                    unique_name_parts=("some_trait",),
                                )
                            ],
                        )
                    ],
                )
            ],
        )

    return fn


# Note: This is here as the CLI tests use python generation to check
# functionality/console output.
@pytest.fixture
def creations_minimal_by_generator():
    """
    The expected list of creations (relative to the output dir)
    from python generation of minimal.yaml.
    """
    return {
        "python": [
            os.path.join("p_p"),
            os.path.join("p_p", "traits"),
            os.path.join("p_p", "traits", "tn.py"),
            os.path.join("p_p", "traits", "__init__.py"),
            os.path.join("p_p", "specifications"),
            os.path.join("p_p", "specifications", "sn.py"),
            os.path.join("p_p", "specifications", "__init__.py"),
            os.path.join("p_p", "__init__.py"),
        ],
        "cpp": [
            os.path.join("p_p", "include", "p_p"),
            os.path.join("p_p", "include", "p_p", "traits"),
            os.path.join("p_p", "include", "p_p", "traits", "tn"),
            os.path.join("p_p", "include", "p_p", "traits", "tn", "TTrait.hpp"),
            os.path.join("p_p", "include", "p_p", "traits", "tn.hpp"),
            os.path.join("p_p", "include", "p_p", "traits", "traits.hpp"),
            os.path.join("p_p", "include", "p_p", "specifications"),
            os.path.join("p_p", "include", "p_p", "specifications", "sn"),
            os.path.join("p_p", "include", "p_p", "specifications", "sn", "SSpecification.hpp"),
            os.path.join("p_p", "include", "p_p", "specifications", "sn.hpp"),
            os.path.join("p_p", "include", "p_p", "specifications", "specifications.hpp"),
            os.path.join("p_p", "include", "p_p", "p_p.hpp"),
        ],
    }


@pytest.fixture
def a_capturing_logger():
    logger = logging.Logger("test_openassetio_traitgen")

    class CapturingHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.messages = []

        def emit(self, record: logging.LogRecord):
            self.messages.append((record.levelno, record.getMessage()))

    handler = CapturingHandler()
    logger.addHandler(handler)
    return logger
