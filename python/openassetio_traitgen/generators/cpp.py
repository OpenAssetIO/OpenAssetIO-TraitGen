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

import keyword
import logging
import os
import re

from typing import List

import jinja2

from . import helpers
from ..datamodel import PackageDeclaration, PropertyType


__all__ = ["generate"]

#
## Code Generation
#


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

    def render_template(name: str, path: str, variables: dict):
        """
        A convenience to render a named template into its corresponding
        file and call the creation_callback.
        """
        # pylint: disable=line-too-long
        # NB: Jinja assumes '/' on all plaftorms:
        #  https://github.com/pallets/jinja/blob/7fb13bf94443f067c74204a1aee368fdf0591764/src/jinja2/loaders.py#L29
        template = env.get_template(f"cpp/{name}.hpp.in")
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(template.render(variables))
        creation_callback(path)

    def create_dir_with_path_components(*args) -> str:
        """
        A convenience to create a directory from the supplied path
        components, calling the creation_callback and returning its path
        as a string.
        """
        path = os.path.join(*args)
        os.makedirs(path, exist_ok=True)
        creation_callback(path)
        return path

    # Top level package directory, under an "include" subdirectory
    package_name = env.filters["to_cpp_module_name"](package_declaration.id)
    package_dir_path = create_dir_with_path_components(
        output_directory, package_name, "include", package_name
    )

    # Collect which sub-packages we should import at the top level, so
    # they're available without needing to `#include` each individual
    # header file.
    package_init_imports = []

    # Sub-packages for traits and specifications
    for kind in ("traits", "specifications"):

        namespaces = getattr(package_declaration, kind, None)
        if namespaces:

            package_init_imports.append(f"{kind}/{kind}.hpp")

            # Create the directory for the sub-package
            subpackage_dir_path = create_dir_with_path_components(package_dir_path, kind)

            # Collect the resulting module names for each namespace
            # So we can pre-import them in the sub-package init.
            subpackage_init_imports = []

            # Generate a single-file module for each namespace
            for namespace in namespaces:
                safe_namespace = env.filters["to_cpp_module_name"](namespace.id)
                subpackage_init_imports.append(f"{safe_namespace}.hpp")
                render_template(
                    kind,
                    os.path.join(subpackage_dir_path, f"{safe_namespace}.hpp"),
                    {
                        "package": package_declaration,
                        "namespace": namespace,
                        "imports": helpers.package_dependencies(namespace.members),
                    },
                )

            # Generate the sub-package headers that pre-imports all the
            # submodules.
            subpackage_init_imports.sort()
            docstring = f"{kind.capitalize()} defined in the '{package_declaration.id}' package."
            render_template(
                "package",
                os.path.join(subpackage_dir_path, kind + ".hpp"),
                {"docstring": docstring, "relImports": subpackage_init_imports},
            )

    # Top-level package header that includes everything.
    render_template(
        "package",
        os.path.join(package_dir_path, package_name + ".hpp"),
        {"docstring": package_declaration.description, "relImports": package_init_imports},
    )


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

    def validate_identifier(string: str, original: str):
        """
        Validates some string is a legal C++ variable name.
        """
        # TODO(DF): equivalent for C++
        # if not string.isidentifier():
        #     raise ValueError(f"{string}' (from '{original}' is not a valid C++ identifier.")
        # if keyword.iskeyword(string):
        #     raise ValueError(f"{string}' (from '{original}' is a reserved C++ keyword.")

    def to_cpp_module_name(string: str):
        """
        Conforms the supplied string a legal module name.
        """
        # Don't warn for - to _ since hyphenated namespaces are common
        # enough that warning on it would add too much log noise.
        no_hypens = string.replace("-", "_")
        module_name = re.sub(r"[^a-zA-Z0-9_]", "_", no_hypens)
        if module_name != no_hypens:
            logger.warning(f"Conforming '{string}' to '{module_name}' for module name")
        return module_name

    def to_cpp_class_name(string: str):
        """
        Conforms the supplied string to a legal C++ class name.
        """
        class_name = helpers.to_upper_camel_alnum(string)
        if class_name != string:
            logger.warning(f"Conforming '{string}' to '{class_name}' for class name")
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
            logger.warning(
                f"Conforming '{unique_name}' to '{accessor_name}' for trait getter name"
            )
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
            logger.warning(
                f"Conforming '{string}' to '{accessor_name}' for property accessor name"
            )
        validate_identifier(accessor_name, string)
        return accessor_name

    def to_cpp_var_name(string: str):
        """
        Conforms the supplied string to a valid C++ var name,
        starting with a lowercase letter.
        """
        var_name = helpers.to_lower_camel_alnum(string)
        if var_name != string:
            logger.warning(f"Conforming '{string}' to '{var_name}' for variable name")
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
    environment.filters["to_cpp_module_name"] = to_cpp_module_name
    environment.filters["to_cpp_class_name"] = to_cpp_class_name
    environment.filters["to_cpp_trait_accessor_name"] = to_cpp_trait_accessor_name
    environment.filters["to_cpp_var_accessor_name"] = to_cpp_var_accessor_name
    environment.filters["to_cpp_var_name"] = to_cpp_var_name
    environment.filters["to_cpp_type"] = to_cpp_type
    environment.filters["is_moveable_type"] = is_moveable_type
