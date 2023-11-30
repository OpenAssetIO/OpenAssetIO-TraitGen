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
import functools

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=too-few-public-methods,too-many-arguments
# pylint: disable=missing-class-docstring,missing-function-docstring
# pylint: disable=too-many-return-statements

import logging
import os
import pathlib
import subprocess

import pytest
from tree_sitter_languages import get_parser, get_language

from openassetio_traitgen import generate
from openassetio_traitgen.generators import cpp as cpp_generator, cpp_keywords


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
            == """
/**
 * Test classes to validate the integrity of the openassetio-traitgen
 * tool.
 */
 """.strip()
        )


class Test_cpp_package_all_traits:
    def test_aNamespace_docstring_contains_declaration_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all", is_specification=False, namespace="aNamespace"
            )
            == """
/**
 * @namespace openassetio_traitgen_test_all::v1::traits::aNamespace
 *
 * Trait definitions in the 'aNamespace' namespace.
 *
 * A Namespace
 */
 """.strip()
        )

    def test_anotherNamespace_docstring_contains_declaration_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=False,
                namespace="anotherNamespace",
            )
            == """
/**
 * @namespace openassetio_traitgen_test_all::v1::traits::anotherNamespace
 *
 * Trait definitions in the 'anotherNamespace' namespace.
 *
 * Another Namespace
 */
 """.strip()
        )


class Test_cpp_package_all_specifications:
    def test_test_docstring_contains_declaration_description(self, docstring_for):
        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
            )
            == """
/**
 * @namespace openassetio_traitgen_test_all::v1::specifications::test
 *
 * Specification definitions in the 'test' namespace.
 *
 * Test specifications.
 */
 """.strip()
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
            == """
/**
 * Another trait, this time with no properties.
 */
 """.strip()
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
            == """
/**
 * Another trait, this time with multiple usage.
 * Usage: entity, relationship
 */
 """.strip()
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
            == """
/**
 * A trait with properties of all types.
 */
 """.strip()
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_getters_with_default_with_expected_docstring(
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
                has_default=False,
            )
            == f"""
  /**
   * Gets the value of the {property_name} property. Returns an empty
   * optional if not found or is of an unexpected type.
   *
   * A {property_type}-typed property.
   */
""".strip()
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_getters_without_default_with_expected_docstring(
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
                has_default=True,
            )
            == f"""
  /**
   * Gets the value of the {property_name} property or the supplied
   * default.
   *
   * A {property_type}-typed property.
   */
""".strip()
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
            == f"""
  /**
   * Sets the {property_name} property.
   *
   * A {property_type}-typed property.
   */
""".strip()
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
            == """
/**
 * A specification with two traits.
 */
""".strip()
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
            == """
  /**
   * Returns the view for the 'openassetio-traitgen-test-all:aNamespace.NoProperties'
   * trait wrapped around the data held in this instance.
   */
""".strip()
        )

        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="TwoLocalTraitsSpecification",
                func="anotherNamespaceNoPropertiesTrait",
            )
            == """
  /**
   * Returns the view for the 'openassetio-traitgen-test-all:anotherNamespace.NoProperties'
   * trait wrapped around the data held in this instance.
   */
""".strip()
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
            == """
/**
 * A specification referencing traits in another package.
 */
""".strip()
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
            == """
  /**
   * Returns the view for the 'openassetio-traitgen-test-traits-only:test.Another'
   * trait wrapped around the data held in this instance.
   */
""".strip()
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
            == """
/**
 * A specification referencing traits in this and another package.
 * Usage: entity, managementPolicy
 */
""".strip()
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
            == """
  /**
   * Returns the view for the 'openassetio-traitgen-test-all:aNamespace.NoProperties'
   * trait wrapped around the data held in this instance.
   */
""".strip()
        )

        assert (
            docstring_for(
                "openassetio_traitgen_test_all",
                is_specification=True,
                namespace="test",
                cls="LocalAndExternalTraitSpecification",
                func="openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait",
            )
            == """
  /**
   * Returns the view for the 'openassetio-traitgen-test-traits-only:aNamespace.NoProperties'
   * trait wrapped around the data held in this instance.
   */
""".strip()
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

    @pytest.mark.parametrize(
        "id_type",
        ("package_name", "specification_namespace", "trait_namespace"),
    )
    @pytest.mark.parametrize(
        "reserved_word",
        (
            # Check a representative keyword.
            next(iter(cpp_keywords.keywords)),
            "__dunder_implicitly_reserved",
            "traits",
            "specifications",
        ),
    )
    def test_when_identifiers_reserved_keywords_then_exception_raised(
        self,
        tmp_path_factory,
        a_capturing_logger,
        declaration_invalid_identifiers,
        id_type,
        reserved_word,
    ):
        output_dir = tmp_path_factory.mktemp("test_cpp_invalid_identifiers")
        with pytest.raises(ValueError) as err:
            cpp_generator.generate(
                declaration_invalid_identifiers(**{id_type: reserved_word}),
                {},
                output_dir,
                lambda _: _,
                a_capturing_logger,
            )
        assert (
            str(err.value) == f"'{reserved_word}' (from '{reserved_word}') is a reserved keyword."
        )


@pytest.mark.skipif(
    not os.environ.get("OPENASSETIO_TRAITGENTEST_CMAKE_PRESET"),
    reason="OPENASSETIO_TRAITGENTEST_CMAKE_PRESET environment variable is not set",
)
@pytest.mark.ctest
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
            os.environ["OPENASSETIO_TRAITGENTEST_CMAKE_PRESET"],
            f"-DCMAKE_PREFIX_PATH={build_dir}/.conan",
            f"-DOPENASSETIO_TRAITGENTEST_ADDITIONAL_INCLUDE_DIRS={include_paths}",
        ]
    )
    subprocess.check_call(["cmake", "--build", build_dir, "--config", "RelWithDebInfo"])
    # Run tests in CMake project.
    subprocess.check_call(
        ["ctest", "-VV", "--test-dir", build_dir, "--build-config", "RelWithDebInfo"]
    )


#
# Fixtures
#


@pytest.fixture
def docstring_for(rootnode_for, cpp_language):
    """
    Provides a function that extracts docstring comments from either
    * a package (top-level hoisting header file docstring)
    * sub-package (trait/specification hoisting header file docstring)
    * namespace (C++ `namespace` docstring within a specific
      trait/specification header file)
    * class (trait/specification type)
    * function (trait property accessor or specification trait view
      factory function).

    This relies on the particular known file system layout of generated
    files, and the known layout of their contents.

    The first omitted argument (i.e. None) delimits the scope to extract
    the docstrings from. E.g. to extract the docstring for the
    "my_namespace" trait namespace of a package called "my_package"

      docstring_for(
        "my_package", is_specification=False, namespace="my_namespace")
    """

    def fn(
        package_name,
        is_specification=None,
        namespace=None,
        cls=None,
        func=None,
        has_default=None,
    ):
        """
        @param package_name: Name of package to parse docstring from.
        @param is_specification: Whether to parse docstring within a
        specification or a trait sub-package, if any.
        @param namespace: Which C++ namespace to parse docstring from,
        if any.
        @param cls: Which class to parse docstring from, if any.
        @param func: Which function within the `cls` to parse docstring
        from, if any.
        @param has_default: If True/False then signals that `func` has
        an overload with a `defaultValue` argument, and hence selects
        which of the overloads to parse. If None then assumes no
        overload.
        @return: String containing docstring for selected element.
        """
        root_node = rootnode_for(package_name, is_specification, namespace, cls)

        if is_specification is None:
            # Top-level package docstring
            query = cpp_language.query("""(translation_unit . (comment) @docstring)""")
            return query.captures(root_node)[0][0].text.decode()

        if namespace is None:
            # Trait/specification hoisted file docstring
            query = cpp_language.query("""(translation_unit . (comment) @docstring)""")
            return query.captures(root_node)[0][0].text.decode()

        if cls is None:
            # Namespace docstring.
            query = cpp_language.query("""((comment) . (preproc_include)) @docstring""")
            return query.captures(root_node)[0][0].text.decode()

        query = cpp_language.query(
            f"""(
            (comment) @docstring . (class_specifier name: (type_identifier) @struct_name) @struct
            (#eq? @struct_name "{cls}")
        )"""
        )

        if func is None:
            # Class docstring.
            return query.captures(root_node)[0][0].text.decode()

        struct_node = query.captures(root_node)[1][0]
        query = cpp_language.query(
            f"""(
            (comment) @docstring
            .
            (function_definition
                declarator: (
                    function_declarator
                    declarator: (field_identifier) @func_name (eq? @func_name "{func}")
                ) @func_decl
            )
            )"""
        )

        if has_default is None:
            # Setter function docstring.
            return query.captures(struct_node)[0][0].text.decode()

        # Getter function docstring.

        # Frustratingly, no way to test non-existence of a child node
        # (i.e. check a function has no params) so we have to iterate
        # over the results.
        (
            first_doc,
            first_decl,
            _,
            second_doc,
            second_decl,
            _,
        ) = (node for node, key in query.captures(struct_node))

        query = cpp_language.query(
            """(parameter_list (
                   parameter_declaration declarator: (
                       reference_declarator (identifier) @var_name
                       (eq? @var_name "defaultValue") )))"""
        )

        first_has_default = bool(query.captures(first_decl))
        second_has_default = bool(query.captures(second_decl))
        assert first_has_default ^ second_has_default

        if has_default == first_has_default:
            return first_doc.text.decode()
        return second_doc.text.decode()

    return fn


@pytest.fixture(scope="module")
def rootnode_for(cpp_parser, generated_path):
    """
    Provides a function that returns an AST for a particular file in the
    generated hierarchy, using the Tree-sitter library.

    This relies on the particular known file system layout of generated
    files.

    The first `None`-valued argument delimits the file to extract the
    AST for. E.g. the AST for the top-level package hoisting header file
    for a package called "my_package" would be extracted by calling:

      rootnode_for("my_package", None, None)
    """

    @functools.lru_cache(maxsize=None)
    def fn(package_name, is_specification, namespace, cls):
        """
        @param package_name: Name of package to parse.
        @param is_specification: Whether to parse within a specification
        or a trait sub-package, if any.
        @param namespace: Which specific C++ namespace header file to
        parse, if any.
        @return: Tree-sitter root AST node for file.
        """
        file_path = pathlib.Path(generated_path) / package_name / "include" / package_name
        if is_specification is not None:
            file_path /= "specifications" if is_specification else "traits"
            if namespace is not None:
                file_path /= namespace
                if cls is not None:
                    file_path /= cls
        else:
            file_path /= package_name

        file_path = file_path.with_suffix(".hpp")

        with open(file_path, "rb") as f:
            return cpp_parser.parse(f.read()).root_node

    return fn


@pytest.fixture(scope="module")
def cpp_parser():
    return get_parser("cpp")


@pytest.fixture(scope="module")
def cpp_language():
    return get_language("cpp")


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
        os.path.join("p_p", "include", "p_p"),
        os.path.join("p_p", "include", "p_p", "traits"),
        os.path.join("p_p", "include", "p_p", "traits", "t_n"),
        os.path.join("p_p", "include", "p_p", "traits", "t_n", "TTrait.hpp"),
        os.path.join("p_p", "include", "p_p", "traits", "t_n.hpp"),
        os.path.join("p_p", "include", "p_p", "traits", "traits.hpp"),
        os.path.join("p_p", "include", "p_p", "specifications"),
        os.path.join("p_p", "include", "p_p", "specifications", "s_n"),
        os.path.join("p_p", "include", "p_p", "specifications", "s_n", "SSpecification.hpp"),
        os.path.join("p_p", "include", "p_p", "specifications", "s_n.hpp"),
        os.path.join("p_p", "include", "p_p", "specifications", "specifications.hpp"),
        os.path.join("p_p", "include", "p_p", "p_p.hpp"),
    ]


@pytest.fixture
def warnings_exotic_values():
    return [
        (logging.WARNING, "Conforming 'p📦p' to 'p_p' for namespace name"),
        (logging.WARNING, "Conforming 't!n' to 't_n' for namespace name"),
        (logging.WARNING, "Conforming 't&' to 'T' for class name"),
        (logging.WARNING, "Conforming 'p$' to 'P' for property accessor name"),
        (logging.WARNING, "Conforming 'p$' to 'p' for variable name"),
        (logging.WARNING, "Conforming 's!n' to 's_n' for namespace name"),
        (logging.WARNING, "Conforming 's^' to 'S' for class name"),
    ]
