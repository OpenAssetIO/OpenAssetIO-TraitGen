#
#   Copyright 2023 The Foundry Visionmongers Ltd
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
Tests for the C++ code generator.
"""

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring,missing-function-docstring

import logging
import os
import subprocess

import pytest
from tree_sitter_languages import get_parser

from openassetio_traitgen import generate
from openassetio_traitgen.generators import cpp as cpp_generator


#
# Tests: Packages and Structure
#
# These cases cover the structure of the generated headers. In
# particular, docstrings/comments are checked, which cannot be checked
# within a C++ test suite.
#


class Test_cpp_package_all:
    def test_package_docstring(self, docstring_for):
        assert (
            docstring_for("openassetio_traitgen_test_all")
            == """*
 * Test classes to validate the integrity of the openassetio-traitgen tool.
 """
        )


class Test_cpp_package_all_traits:
    def test_aNamespace_docstring_contains_declaration_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all", is_specification=False, namespace="aNamespace"
            )
            == """*
 * Trait definitions in the 'aNamespace' namespace.
 *
 * A Namespace
 """
        )

    def test_anotherNamespace_docstring_contains_declaration_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="anotherNamespace",
            )
            == """*
 * Trait definitions in the 'anotherNamespace' namespace.
 *
 * Another Namespace
 """
        )


class Test_cpp_package_all_traits_aNamespace_NoPropertiesTrait:
    def test_docstring_contains_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="aNamespace",
                cls="NoPropertiesTrait",
            )
            == """*
     * Another trait, this time with no properties.
     """
        )


class Test_cpp_package_all_traits_aNamespace_NoPropertiesMultipleUsageTrait:
    def test_has_expected_docstring(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="aNamespace",
                cls="NoPropertiesMultipleUsageTrait",
            )
            == """*
     * Another trait, this time with multiple usage.
     * Usage: entity, relationship
     """
        )


class Test_cpp_package_all_traits_aNamespace_AllPropertiesTrait:
    def test_has_expected_docstring(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="aNamespace",
                cls="AllPropertiesTrait",
            )
            == """*
     * A trait with properties of all types.
     """
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_getters_with_expected_docstring(
        self, docstring_for, property_type
    ):
        property_name = f"{property_type}Property"
        function_name = f"get{property_type.capitalize()}Property"
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="aNamespace",
                cls="AllPropertiesTrait",
                func=function_name,
            )
            == f"""*
         * Gets the value of the {property_name} property or the supplied default.
         *
         * A {property_type}-typed property.
         """
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_setters_with_expected_docstring(
        self, docstring_for, property_type
    ):
        property_name = f"{property_type}Property"
        function_name = f"set{property_type.capitalize()}Property"

        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="aNamespace",
                cls="AllPropertiesTrait",
                func=function_name,
            )
            == f"""*
         * Sets the {property_name} property.
         *
         * A {property_type}-typed property.
         """
        )


class Test_cpp_package_all_specifications_test_TwoLocalTraitsSpecification:
    def test_docstring_contains_description(self, docstring_for):
        docstring_for(
            "openassetio_traitgen_test_all",
            is_specification=True,
            namespace="test",
            cls="TwoLocalTraitsSpecification",
        )
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="TwoLocalTraitsSpecification",
            )
            == """*
     * A specification with two traits.
     """
        )

    def test_has_trait_getters_with_expected_docstring(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="TwoLocalTraitsSpecification",
                func="aNamespaceNoPropertiesTrait",
            )
            == """*
         * Returns the view for the 'openassetio-traitgen-test-all:aNamespace.NoProperties' trait wrapped around
         * the data held in this instance.
         """
        )

        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="TwoLocalTraitsSpecification",
                func="anotherNamespaceNoPropertiesTrait",
            )
            == """*
         * Returns the view for the 'openassetio-traitgen-test-all:anotherNamespace.NoProperties' trait wrapped around
         * the data held in this instance.
         """
        )


class Test_cpp_package_all_specifications_test_OneExternalTraitSpecification:
    def test_docstring_contains_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="OneExternalTraitSpecification",
            )
            == """*
     * A specification referencing traits in another package.
     """
        )

    def test_has_trait_getters_with_expected_docstring(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="OneExternalTraitSpecification",
                func="anotherTrait",
            )
            == """*
         * Returns the view for the 'openassetio-traitgen-test-traits-only:test.Another' trait wrapped around
         * the data held in this instance.
         """
        )


class Test_cpp_package_all_specifications_test_LocalAndExternalTraitSpecification:
    def test_docstring_contains_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="LocalAndExternalTraitSpecification",
            )
            == """*
     * A specification referencing traits in this and another package.
     * Usage: entity, managementPolicy
     """
        )

    def test_has_trait_getters_with_expected_docstring(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="LocalAndExternalTraitSpecification",
                func="openassetioTraitgenTestAllANamespaceNoPropertiesTrait",
            )
            == """*
         * Returns the view for the 'openassetio-traitgen-test-all:aNamespace.NoProperties' trait wrapped around
         * the data held in this instance.
         """
        )
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="LocalAndExternalTraitSpecification",
                func="openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait",
            )
            == """*
         * Returns the view for the 'openassetio-traitgen-test-traits-only:aNamespace.NoProperties' trait wrapped around
         * the data held in this instance.
         """
        )


class Test_generate:
    def test_when_files_created_then_creation_callback_is_called(
        self, declaration_exotic_values, creations_exotic_values, tmp_path_factory
    ):
        output_dir = tmp_path_factory.mktemp("test_cpp_generate_callback")
        expected = [os.path.join(output_dir, p) for p in creations_exotic_values]

        actual = []

        def creation_callback(path):
            actual.append(path)

        cpp_generator.generate(
            declaration_exotic_values,
            {},
            output_dir,
            creation_callback,
            logging.Logger("Test_generate"),
        )

        assert actual == expected

    def test_when_names_invalid_then_warnings_are_logged(
        self,
        declaration_exotic_values,
        warnings_exotic_values,
        a_capturing_logger,
        tmp_path_factory,
    ):
        output_dir = tmp_path_factory.mktemp("test_cpp_generate_warnings")
        cpp_generator.generate(
            declaration_exotic_values, {}, output_dir, lambda _: _, a_capturing_logger
        )

        assert a_capturing_logger.handlers[0].messages == warnings_exotic_values


def test_cpp_project(generated_path, tmp_path_factory, cpp_project_dir):
    build_dir = tmp_path_factory.mktemp("test_cpp_project")

    # Install third-party C++ library dependencies.
    subprocess.check_call(
        [
            "conan",
            "install",
            "--install-folder",
            f"{build_dir}/.conan",
            "-g",
            "CMakeDeps",
            "-s",
            "build_type=RelWithDebInfo",
            cpp_project_dir,
        ]
    )

    include_paths = ";".join(
        (
            f"{generated_path}/openassetio_traitgen_test_all/include",
            f"{generated_path}/openassetio_traitgen_test_specifications_only/include",
            f"{generated_path}/openassetio_traitgen_test_traits_only/include",
        )
    )

    # Configure CMake project
    subprocess.check_call(
        [
            "cmake",
            "-S",
            cpp_project_dir,
            "-B",
            build_dir,
            "--preset",
            "test",
            f"-DCMAKE_PREFIX_PATH={build_dir}/.conan",
            f"-DOPENASSETIO_TRAITGENTEST_ADDITIONAL_INCLUDE_DIRS={include_paths}",
        ]
    )
    subprocess.check_call(["cmake", "--build", build_dir])
    # Run tests in CMake project.
    subprocess.check_call(["ctest", "-VV", "--test-dir", build_dir])


#
# Fixtures
#


@pytest.fixture
def docstring_for(cpp_parser, generated_path):
    def fn(package_name, is_specification=None, namespace=None, cls=None, func=None):
        return ""

    return fn


@pytest.fixture(scope="module")
def cpp_parser():
    return get_parser("cpp")


@pytest.fixture(scope="module")
def cpp_project_dir():
    return os.path.join(os.path.dirname(__file__), "cpp")


@pytest.fixture(scope="module")
def generated_path(
    yaml_path_all, yaml_path_traits_only, yaml_path_specifications_only, tmp_path_factory
):
    output_dir = tmp_path_factory.mktemp("generated_path")

    def creation_callback(_):
        pass

    # As there are dependencies between the different packages, we need
    # to generate them all together to avoid import errors.
    for description in (yaml_path_all, yaml_path_traits_only, yaml_path_specifications_only):
        generate(
            description_path=description,
            output_directory=str(output_dir),
            generator="cpp",
            creation_callback=creation_callback,
            logger=logging.Logger(name="Capturing logger"),
        )

    return output_dir


@pytest.fixture
def creations_exotic_values():
    return [
        os.path.join("p_p"),
        os.path.join("p_p", "traits"),
        os.path.join("p_p", "traits", "t_n.py"),
        os.path.join("p_p", "traits", "__init__.py"),
        os.path.join("p_p", "specifications"),
        os.path.join("p_p", "specifications", "s_n.py"),
        os.path.join("p_p", "specifications", "__init__.py"),
        os.path.join("p_p", "__init__.py"),
    ]


@pytest.fixture
def warnings_exotic_values():
    return [
        (logging.WARNING, "Conforming 'p📦p' to 'p_p' for module name"),
        (logging.WARNING, "Conforming 't!n' to 't_n' for module name"),
        (logging.WARNING, "Conforming 't&' to 'T' for class name"),
        (logging.WARNING, "Conforming 'p$' to 'P' for property accessor name"),
        (logging.WARNING, "Conforming 'p$' to 'p' for variable name"),
        (logging.WARNING, "Conforming 's!n' to 's_n' for module name"),
        (logging.WARNING, "Conforming 's^' to 'S' for class name"),
        (logging.WARNING, "Conforming 't!n' to 't_n' for module name"),
        (logging.WARNING, "Conforming 't&' to 'T' for class name"),
        (logging.WARNING, "Conforming 't!n' to 't_n' for module name"),
        (logging.WARNING, "Conforming 't&' to 'T' for class name"),
    ]