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
A traitgen generator that outputs a C++ package based on the
openassetio_traitgen PackageDefinition model.
"""
# TODO(DF): Refactor to pull out common code, then remove this
#  suppression.
# pylint: disable=duplicate-code

import logging
import os
import re

from typing import List, Callable, Union

import jinja2

from . import helpers, cpp_keywords
from ..datamodel import (
    PackageDeclaration,
    PropertyType,
    NamespaceDeclaration,
    SpecificationDeclaration,
    TraitDeclaration,
)


__all__ = ["generate"]

#
## Code Generation
#

OPENASSETIO_ABI_VERSION = "v1"
TRAITGEN_ABI_VERSION = "v1"


# pylint: disable=too-many-locals
def generate(
    package_declaration: PackageDeclaration,
    globals_: dict,
    output_directory: str,
    creation_callback,
    logger: logging.Logger,
):
    """
    Generates a C++ package for the supplied definition under
    output_directory.
    """
    env = _create_jinja_env(globals_, logger)

    Renderer(env, package_declaration, creation_callback).render_package(output_directory)


class Renderer:
    """
    Encapsulates the various stages of rendering a C++ package for the
    supplied package declaration.

    Terminology follows that of the source YAML, i.e. "package",
    "namespace", "module", etc., and translates to directory names,
    (hoisting) header file names, C++ namespaces and C++ classes, as
    appropriate.
    """

    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        env: jinja2.Environment,
        package: PackageDeclaration,
        creation_callback: Callable,
    ):
        self.__env = env
        self.__package = package
        self.__creation_callback = creation_callback

    def render_package(self, output_directory: str):
        """
        Render a package declaration to a C++ header-only package.

        Headers for all traits and specifications are rendered, followed
        by a top-level convenience hoisting header that imports
        everything under this package.

        @param output_directory: Top-level directory to place rendered
        artifacts. Subdirectories will be created to contain trait,
        specification, namespace and class headers, as appropriate.
        """
        # Top level package directory, under an "include" subdirectory
        package_name = self.__env.filters["to_cpp_namespace_name"](self.__package.id)
        package_abs_path = self.__create_dir_with_path_components(
            output_directory, package_name, "include", package_name
        )

        # Collect which sub-packages we should import at the top level,
        # so they're available without needing to `#include` each
        # individual header file.
        imports = []

        # Sub-packages for traits and specifications
        for kind in ("traits", "specifications"):
            file_name = self.__render_traits_or_specifications(package_abs_path, kind)
            if file_name is not None:
                imports.append(f"{kind}/{file_name}")

        # Top-level package header that includes everything.
        self.__render_package_template(
            package_abs_path, package_name, self.__package.description, imports
        )

    def __render_traits_or_specifications(
        self, parent_abs_path: str, kind: str
    ) -> Union[str, None]:
        """
        Render all the headers of a particular "kind" (traits or
        specifications) for the package.

        If the package has no members of this kind, then this is a
        no-op.

        Headers are rendered under a directory appropriate to this
        "kind". An additional top-level convenience hoisting header is
        rendered outside that directory, which (recursively) imports all
        related headers.
        """
        namespaces = getattr(self.__package, kind, None)
        if not namespaces:
            # The package has no subpackage of this kind.
            return None
        # Create the directory for the sub-package of this "kind"
        # (traits or specifications).
        kind_abs_path = self.__create_dir_with_path_components(parent_abs_path, kind)

        # Collect the resulting file names for each namespace, so we can
        # pre-import them in the sub-package header.
        imports = []

        # Generate the file structure for each namespace in this "kind".
        for namespace in namespaces:
            file_name = self.__render_namespace(namespace, kind_abs_path, kind)
            imports.append(file_name)

        # Generate the sub-package header that pre-imports all the
        # namespaces for this "kind".
        imports.sort()
        docstring = f"{kind.capitalize()} defined in the '{self.__package.id}' package."
        return self.__render_package_template(kind_abs_path, kind, docstring, imports)

    def __render_namespace(
        self, namespace: NamespaceDeclaration, parent_abs_path: str, kind: str
    ) -> str:
        """
        Render the headers for a trait namespace.

        The headers for each member class (trait view or specification)
        are rendered, along with a convenience namespace hoisting header
        that imports all the member class headers.

        The namespace header is placed alongside a directory with the
        same basename, and the individual class headers are placed in
        that directory.
        """
        namespace_name = self.__env.filters["to_cpp_namespace_name"](namespace.id)
        namespace_abs_path = self.__create_dir_with_path_components(
            parent_abs_path, namespace_name
        )
        imports = []

        # Render a file per class (trait or specification).
        for declaration in namespace.members:
            if kind == "traits":
                file_name = self.__render_trait(namespace, declaration, namespace_abs_path)
            else:
                file_name = self.__render_specification(namespace, declaration, namespace_abs_path)

            imports.append(f"{namespace_name}/{file_name}")

        # Generate the namespace header that pre-imports all the
        # classes.
        imports.sort()
        self.__render_template(
            kind,
            os.path.join(parent_abs_path, f"{namespace_name}.hpp"),
            {
                "package": self.__package,
                "namespace": namespace,
                "relImports": imports,
                "traitgen_abi_version": TRAITGEN_ABI_VERSION,
            },
        )
        return f"{namespace_name}.hpp"

    def __render_trait(
        self,
        namespace: NamespaceDeclaration,
        declaration: TraitDeclaration,
        namespace_abs_path: str,
    ) -> str:
        """
        Render the template for a trait header.

        Creates a single header file containing a single trait view
        class.
        """
        cls_name = self.__env.filters["to_cpp_class_name"](declaration.name) + "Trait"
        self.__render_template(
            "trait",
            os.path.join(namespace_abs_path, f"{cls_name}.hpp"),
            {
                "package": self.__package,
                "namespace": namespace,
                "trait": declaration,
                "openassetio_abi_version": OPENASSETIO_ABI_VERSION,
                "traitgen_abi_version": TRAITGEN_ABI_VERSION,
            },
        )
        return f"{cls_name}.hpp"

    def __render_specification(
        self,
        namespace: NamespaceDeclaration,
        declaration: SpecificationDeclaration,
        namespace_abs_path: str,
    ) -> str:
        """
        Render the template for a specification header.

        Creates a single header file containing a single specification
        class.
        """
        cls_name = self.__env.filters["to_cpp_class_name"](declaration.id) + "Specification"
        self.__render_template(
            "specification",
            os.path.join(namespace_abs_path, f"{cls_name}.hpp"),
            {
                "package": self.__package,
                "namespace": namespace,
                "specification": declaration,
                "openassetio_abi_version": OPENASSETIO_ABI_VERSION,
                "traitgen_abi_version": TRAITGEN_ABI_VERSION,
            },
        )
        return f"{cls_name}.hpp"

    def __render_package_template(
        self, package_abs_path: str, name: str, docstring: str, imports: List[str]
    ) -> str:
        """
        Render the template for a logical "package" header.

        I.e. a convenience hoisting header that collects all related
        headers into one.
        """
        self.__render_template(
            "package",
            os.path.join(package_abs_path, f"{name}.hpp"),
            {"docstring": docstring, "relImports": imports},
        )
        return f"{name}.hpp"

    def __render_template(self, name: str, path: str, variables: dict):
        """
        A convenience to render a named template into its corresponding
        file and call the creation_callback.
        """
        # pylint: disable=line-too-long
        # NB: Jinja assumes '/' on all plaftorms:
        #  https://github.com/pallets/jinja/blob/7fb13bf94443f067c74204a1aee368fdf0591764/src/jinja2/loaders.py#L29
        template = self.__env.get_template(f"cpp/{name}.hpp.in")
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(template.render(variables))
        self.__creation_callback(path)

    def __create_dir_with_path_components(self, *args) -> str:
        """
        A convenience to create a directory from the supplied path
        components, calling the creation_callback and returning its path
        as a string.
        """
        path = os.path.join(*args)
        os.makedirs(path, exist_ok=True)
        self.__creation_callback(path)
        return path


#
## Jinja setup
#


def _create_jinja_env(env_globals, logger):
    """
    Creates a custom Jinja2 environment with:
     - A package a loader that automatically finds templates within a
       'templates' directory in the openassetio_traitgen python package.
     - Updated globals.
     - Custom filters.
    """
    env = jinja2.Environment(loader=jinja2.PackageLoader("openassetio_traitgen"))
    env.globals.update(env_globals)
    _install_custom_filters(env, logger)
    return env


# Custom filters


def _install_custom_filters(environment, logger):
    """
    Installs custom filters in to the Jinja template environment that
    allow data from the model to be conformed to C++-specific standards.

    The to_cpp* methods will log a warning if the string is changed from
    the input during this process. An error will be raised if this
    resulted in an empty string.
    """
    # pylint: disable=too-many-statements

    logged_warnings = set()

    def validate_identifier(string: str, original: str):
        """
        Validates some string is a legal C++ variable name.
        """
        if not string.isidentifier():
            raise ValueError(f"'{string}' (from '{original}') is not a valid C++ identifier.")
        if (
            string in cpp_keywords.keywords
            or string.startswith("__")
            or string in ("traits", "specifications")
        ):
            raise ValueError(f"'{string}' (from '{original}') is a reserved keyword.")

    def to_cpp_namespace_name(string: str):
        """
        Conforms the supplied string a legal namespace name.
        """
        # Don't warn for - to _ since hyphenated namespaces are common
        # enough that warning on it would add too much log noise.
        no_hypens = string.replace("-", "_")
        namespace_name = re.sub(r"[^a-zA-Z0-9_]", "_", no_hypens)
        if namespace_name != no_hypens:
            msg = f"Conforming '{string}' to '{namespace_name}' for namespace name"
            if msg not in logged_warnings:
                logged_warnings.add(msg)
                logger.warning(msg)
        validate_identifier(namespace_name, string)
        return namespace_name

    def to_cpp_class_name(string: str):
        """
        Conforms the supplied string to a legal C++ class name.
        """
        class_name = helpers.to_upper_camel_alnum(string)
        if class_name != string:
            msg = f"Conforming '{string}' to '{class_name}' for class name"
            if msg not in logged_warnings:
                logged_warnings.add(msg)
                logger.warning(msg)
        validate_identifier(class_name, string)
        return class_name

    def to_cpp_trait_accessor_name(name_parts: List[str]):
        """
        Conforms the supplied trait name to a legal function name
        beginning with a lowercase letter.
        """
        capitalized_parts = [helpers.to_upper_camel_alnum(part) for part in name_parts]
        unique_name = "".join(capitalized_parts)
        accessor_name = helpers.to_lower_camel_alnum(unique_name)
        # We expect the first letter to change to lowercase
        if accessor_name != f"{unique_name[0].lower()}{unique_name[1:]}":
            msg = f"Conforming '{unique_name}' to '{accessor_name}' for trait getter name"
            if msg not in logged_warnings:
                logged_warnings.add(msg)
                logger.warning(msg)
        validate_identifier(accessor_name, unique_name)
        return accessor_name

    def to_cpp_var_accessor_name(string: str):
        """
        Conforms the supplied string a legal function name, but
        beginning with an uppercase letter so it can be prefixed with
        get or set.
        """
        accessor_name = helpers.to_upper_camel_alnum(string)
        if accessor_name != f"{string[0].upper()}{string[1:]}":
            msg = f"Conforming '{string}' to '{accessor_name}' for property accessor name"
            if msg not in logged_warnings:
                logged_warnings.add(msg)
                logger.warning(msg)
        validate_identifier(accessor_name, string)
        return accessor_name

    def to_cpp_var_name(string: str):
        """
        Conforms the supplied string to a valid C++ var name,
        starting with a lowercase letter.
        """
        var_name = helpers.to_lower_camel_alnum(string)
        if var_name != string:
            msg = f"Conforming '{string}' to '{var_name}' for variable name"
            if msg not in logged_warnings:
                logged_warnings.add(msg)
                logger.warning(msg)
        validate_identifier(var_name, string)
        return var_name

    type_map = {
        PropertyType.STRING: "openassetio::Str",
        PropertyType.INTEGER: "openassetio::Int",
        PropertyType.FLOAT: "openassetio::Float",
        PropertyType.BOOL: "openassetio::Bool",
        PropertyType.DICT: "openassetio::InfoDictionary",
    }

    is_moveable_map = {
        PropertyType.STRING: True,
        PropertyType.INTEGER: False,
        PropertyType.FLOAT: False,
        PropertyType.BOOL: False,
        PropertyType.DICT: True,
    }

    def to_cpp_type(declaration_type):
        """
        Returns the C++ value type for a property declaration (PropertyType).
        """
        if declaration_type == PropertyType.DICT:
            raise TypeError("Dictionary types are not yet supported as trait properties")
        return type_map[declaration_type]

    def is_moveable_type(declaration_type):
        """
        Returns whether std::move can be applied to the value type for
        a property.
        """
        return is_moveable_map[declaration_type]

    environment.filters["to_upper_camel_alnum"] = helpers.to_upper_camel_alnum
    environment.filters["to_cpp_namespace_name"] = to_cpp_namespace_name
    environment.filters["to_cpp_class_name"] = to_cpp_class_name
    environment.filters["to_cpp_trait_accessor_name"] = to_cpp_trait_accessor_name
    environment.filters["to_cpp_var_accessor_name"] = to_cpp_var_accessor_name
    environment.filters["to_cpp_var_name"] = to_cpp_var_name
    environment.filters["to_cpp_type"] = to_cpp_type
    environment.filters["is_moveable_type"] = is_moveable_type
