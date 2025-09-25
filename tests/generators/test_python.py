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
Tests for the Python code generator.
"""

# pylint: disable=invalid-name,redefined-outer-name
# pylint: disable=too-few-public-methods
# pylint: disable=missing-class-docstring,missing-function-docstring

import inspect
import logging
import os
import sys

from typing import Any, NamedTuple

import pytest

from openassetio.trait import TraitsData
from openassetio_traitgen import generate
from openassetio_traitgen.generators import python as python_generator


#
# Tests: Packages and Structure
#
# These cases cover the structure of the generated packages, ensuring
# they contain the expected sub-modules, classes and their methods.
# Functional testing is covered later.
#


class Test_python_package_all:
    def test_package_is_importable(self, extended_python_path):
        # pylint: disable=unused-import,import-error,unused-argument,import-outside-toplevel
        import openassetio_traitgen_test_all

        # pylint: disable=pointless-statement
        del sys.modules["openassetio_traitgen_test_all"]

    def test_package_docstring(self, module_all):
        assert (
            module_all.__doc__
            == """
Test classes to validate the integrity of the openassetio-traitgen tool.
"""
        )


class Test_python_package_all_traits:
    def test_contains_declaration_namespaces(self, module_all):
        assert inspect.ismodule(module_all.traits.aNamespace)
        assert inspect.ismodule(module_all.traits.anotherNamespace)

    def test_aNamespace_docstring_contains_declaration_description(self, module_all):
        assert (
            module_all.traits.aNamespace.__doc__
            == """
Trait definitions in the 'aNamespace' namespace.

A Namespace
"""
        )

    def test_anotherNamespace_docstring_contains_declaration_description(self, module_all):
        assert (
            module_all.traits.anotherNamespace.__doc__
            == """
Trait definitions in the 'anotherNamespace' namespace.

Another Namespace
"""
        )

    def test_aNamespace_module_traits_are_suffixed_with_Trait(self, module_all):
        assert inspect.isclass(module_all.traits.aNamespace.NoPropertiesTrait_v1)
        assert inspect.isclass(module_all.traits.aNamespace.NoPropertiesMultipleUsageTrait_v1)
        assert inspect.isclass(module_all.traits.aNamespace.AllPropertiesTrait_v1)

    def test_anotherNamespace_module_traits_are_suffixed_with_Trait(self, module_all):
        assert inspect.isclass(module_all.traits.anotherNamespace.NoPropertiesTrait_v1)


class Test_python_package_all_traits_aNamespace_NoPropertiesTrait:
    def test_docstring_contains_description(self, module_all):
        assert (
            module_all.traits.aNamespace.NoPropertiesTrait_v1.__doc__
            == """
    Another trait, this time with no properties.
    """
        )

    def test_kId_is_declaration_id(self, module_all):
        assert (
            module_all.traits.aNamespace.NoPropertiesTrait_v1.kId
            == "openassetio-traitgen-test-all:aNamespace.NoProperties"
        )


class Test_python_package_all_traits_aNamespace_NoPropertiesMultipleUsageTrait:
    def test_has_expected_docstring(self, module_all):
        assert (
            module_all.traits.aNamespace.NoPropertiesMultipleUsageTrait_v1.__doc__
            == """
    Another trait, this time with multiple usage.
    Usage: entity, relationship
    """
        )

    def test_kId_is_declaration_id(self, module_all):
        assert (
            module_all.traits.aNamespace.NoPropertiesMultipleUsageTrait_v1.kId
            == "openassetio-traitgen-test-all:aNamespace.NoPropertiesMultipleUsage"
        )


class Test_python_package_all_traits_aNamespace_AllPropertiesTrait:
    def test_has_expected_docstring(self, module_all):
        assert (
            module_all.traits.aNamespace.AllPropertiesTrait_v1.__doc__
            == """
    A trait with properties of all types.
    """
        )

    def test_kId_is_declaration_id(self, module_all):
        assert (
            module_all.traits.aNamespace.AllPropertiesTrait_v1.kId
            == "openassetio-traitgen-test-all:aNamespace.AllProperties"
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_getters_with_expected_docstring(
        self, module_all, property_type
    ):
        property_name = f"{property_type}Property"
        function_name = f"get{property_type.capitalize()}Property"
        function = getattr(module_all.traits.aNamespace.AllPropertiesTrait_v1, function_name)

        assert inspect.isfunction(function)
        assert (
            function.__doc__
            == f"""
        Gets the value of the {property_name} property or the supplied default.

        A {property_type}-typed property.
        """
        )

    @pytest.mark.parametrize("property_type", ["string", "int", "float", "bool"])
    def test_has_prefixed_property_setters_with_expected_docstring(
        self, module_all, property_type
    ):
        property_name = f"{property_type}Property"
        function_name = f"set{property_type.capitalize()}Property"
        function = getattr(module_all.traits.aNamespace.AllPropertiesTrait_v1, function_name)

        assert inspect.isfunction(function)
        assert (
            function.__doc__
            == f"""
        Sets the {property_name} property.

        A {property_type}-typed property.
        """
        )


class Test_python_package_all_specifications:
    def test_contains_declaration_namespaces(self, module_all):
        assert inspect.ismodule(module_all.specifications.test)

    def test_test_docstring_contains_declaration_description(self, module_all):
        assert (
            module_all.specifications.test.__doc__
            == """
Specification definitions in the 'test' namespace.

Test specifications.
"""
        )

    def test_test_module_specifications_are_suffixed_with_Specification(self, module_all):
        assert inspect.isclass(module_all.specifications.test.TwoLocalTraitsSpecification_v1)
        assert inspect.isclass(module_all.specifications.test.OneExternalTraitSpecification_v1)
        assert inspect.isclass(
            module_all.specifications.test.LocalAndExternalTraitSpecification_v1
        )


class Test_python_package_all_specifications_test_TwoLocalTraitsSpecification:
    def test_docstring_contains_description(self, module_all):
        assert (
            module_all.specifications.test.TwoLocalTraitsSpecification_v1.__doc__
            == """
    A specification with two traits.
    """
        )

    def test_trait_set_composes_target_trait_kIds(self, module_all):
        expected = {
            module_all.traits.aNamespace.NoPropertiesTrait_v1.kId,
            module_all.traits.anotherNamespace.NoPropertiesTrait_v1.kId,
        }
        assert module_all.specifications.test.TwoLocalTraitsSpecification_v1.kTraitSet == expected

    def test_has_trait_getters_with_expected_docstring(self, module_all):
        trait_one = module_all.traits.aNamespace.NoPropertiesTrait_v1
        trait_two = module_all.traits.anotherNamespace.NoPropertiesTrait_v1
        test = module_all.specifications.test

        assert inspect.isfunction(test.TwoLocalTraitsSpecification_v1.aNamespaceNoPropertiesTrait)
        assert (
            test.TwoLocalTraitsSpecification_v1.aNamespaceNoPropertiesTrait.__doc__
            == f"""
        Returns the view for the '{trait_one.kId}' trait wrapped around
        the data held in this instance.
        """
        )

        assert inspect.isfunction(
            test.TwoLocalTraitsSpecification_v1.anotherNamespaceNoPropertiesTrait
        )
        assert (
            test.TwoLocalTraitsSpecification_v1.anotherNamespaceNoPropertiesTrait.__doc__
            == f"""
        Returns the view for the '{trait_two.kId}' trait wrapped around
        the data held in this instance.
        """
        )


class Test_python_package_all_specifications_test_OneExternalTraitSpecification:
    def test_docstring_contains_description(self, module_all):
        assert (
            module_all.specifications.test.OneExternalTraitSpecification_v1.__doc__
            == """
    A specification referencing traits in another package.
    """
        )

    def test_trait_set_composes_target_trait_kIds(self, module_all, module_traits_only):
        expected = {
            module_traits_only.traits.test.AnotherTrait_v1.kId,
        }
        assert (
            module_all.specifications.test.OneExternalTraitSpecification_v1.kTraitSet == expected
        )

    def test_has_trait_getters_with_expected_docstring(self, module_all, module_traits_only):
        trait = module_traits_only.traits.test.AnotherTrait_v1

        assert inspect.isfunction(
            module_all.specifications.test.OneExternalTraitSpecification_v1.anotherTrait
        )
        assert (
            module_all.specifications.test.OneExternalTraitSpecification_v1.anotherTrait.__doc__
            == f"""
        Returns the view for the '{trait.kId}' trait wrapped around
        the data held in this instance.
        """
        )


class Test_python_package_all_specifications_test_LocalAndExternalTraitSpecification:
    def test_docstring_contains_description(self, module_all):
        assert (
            module_all.specifications.test.LocalAndExternalTraitSpecification_v1.__doc__
            == """
    A specification referencing traits in this and another package.
    Usage: entity, managementPolicy
    """
        )

    def test_trait_set_composes_target_trait_kIds(self, module_all, module_traits_only):
        expected = {
            module_all.traits.aNamespace.NoPropertiesTrait_v1.kId,
            module_traits_only.traits.aNamespace.NoPropertiesTrait_v1.kId,
        }
        assert (
            module_all.specifications.test.LocalAndExternalTraitSpecification_v1.kTraitSet
            == expected
        )

    def test_has_trait_getters_with_expected_docstring(self, module_all, module_traits_only):
        trait_one = module_all.traits.aNamespace.NoPropertiesTrait_v1
        trait_two = module_traits_only.traits.aNamespace.NoPropertiesTrait_v1
        spec = module_all.specifications.test.LocalAndExternalTraitSpecification_v1

        assert inspect.isfunction(spec.openassetioTraitgenTestAllANamespaceNoPropertiesTrait)
        assert (
            spec.openassetioTraitgenTestAllANamespaceNoPropertiesTrait.__doc__
            == f"""
        Returns the view for the '{trait_one.kId}' trait wrapped around
        the data held in this instance.
        """
        )
        assert inspect.isfunction(
            spec.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait
        )
        assert (
            spec.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait.__doc__
            == f"""
        Returns the view for the '{trait_two.kId}' trait wrapped around
        the data held in this instance.
        """
        )


class Test_python_package_traits_only:
    def test_package_is_importable(self, extended_python_path):
        # pylint: disable=unused-import,import-error,unused-argument,import-outside-toplevel
        import openassetio_traitgen_test_traits_only

        del sys.modules["openassetio_traitgen_test_traits_only"]

    def test_no_specifications_module(self, module_traits_only):
        with pytest.raises(AttributeError):
            module_traits_only.specifications  # pylint: disable=pointless-statement

    def test_traits_are_suffixed_with_Trait(self, module_traits_only):
        assert inspect.isclass(module_traits_only.traits.test.AnotherTrait_v1)
        assert inspect.isclass(module_traits_only.traits.aNamespace.NoPropertiesTrait_v1)


class Test_python_package_specifications_only:
    def test_package_is_importable(self, extended_python_path):
        # pylint: disable=unused-import,import-error,unused-argument,import-outside-toplevel
        import openassetio_traitgen_test_specifications_only

        del sys.modules["openassetio_traitgen_test_specifications_only"]

    def test_no_traits_module(self, module_specifications_only):
        with pytest.raises(AttributeError):
            module_specifications_only.traits  # pylint: disable=pointless-statement

    def test_specifications_are_suffixed_with_Specification(self, module_specifications_only):
        assert inspect.isclass(module_specifications_only.specifications.test.SomeSpecification_v1)


#
# Tests: Functionality
#
# These cases cover the functionality of the auto-generated methods.
# They specifically target only one Trait and Specification that exhaust
# possible options rather than re-testing all generated permutations.
#


class Test_AllPropertiesTrait:
    def test_traitId_is_composed_of_package_aNamespace_and_name(self, all_properties_trait):
        assert all_properties_trait.kId == "openassetio-traitgen-test-all:aNamespace.AllProperties"


class Test_AllPropertiesTrait_isImbued:
    def test_when_data_has_trait_returns_true(self, all_properties_trait):
        a_data = TraitsData({all_properties_trait.kId})
        assert all_properties_trait.isImbuedTo(a_data) is True
        trait = all_properties_trait(a_data)
        assert trait.isImbued() is True

    def test_when_data_does_not_have_trait_returns_false(self, all_properties_trait):
        a_data = TraitsData({"someOtherTrait"})
        assert all_properties_trait.isImbuedTo(a_data) is False
        trait = all_properties_trait(a_data)
        assert trait.isImbued() is False


class Test_AllPropertiesTrait_imbue:
    def test_when_data_empty_then_adds_trait(self, all_properties_trait):
        a_data = TraitsData()
        trait = all_properties_trait(a_data)
        trait.imbue()
        assert trait.isImbued()
        assert trait.kId in a_data.traitSet()

    def test_when_data_has_trait_then_is_noop(self, all_properties_trait):
        a_data = TraitsData({all_properties_trait.kId})
        trait = all_properties_trait(a_data)
        trait.imbue()


class Test_AllPropertiesTrait_imbueTo:
    def test_when_data_empty_then_adds_trait(self, all_properties_trait):
        a_data = TraitsData()
        all_properties_trait.imbueTo(a_data)
        assert all_properties_trait.kId in a_data.traitSet()

    def test_when_data_has_trait_then_is_noop(self, all_properties_trait):
        a_data = TraitsData({all_properties_trait.kId})
        all_properties_trait.imbueTo(a_data)


class PropertyTestValues(NamedTuple):
    name: str
    valid_value: Any
    invalid_value: Any


kAllPropertiesTrait_property_test_values = (
    PropertyTestValues("boolProperty", True, 123),
    PropertyTestValues("intProperty", 42, False),
    PropertyTestValues("floatProperty", 12.3, False),
    PropertyTestValues("stringProperty", "⛅ outside today", 12),
    # Re-instate once InfoDictionary is supported in TraitsData
    # See: https://github.com/OpenAssetIO/OpenAssetIO/issues/527
    # PropertyTestValues("dictProperty", {"a": 1, "b": "2", "c": False}, "Mouse"),
)


@pytest.mark.parametrize("property_", kAllPropertiesTrait_property_test_values)
class Test_AllPropertiesTrait_getter:
    def test_when_property_is_set_then_returns_expected_value(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        an_all_properties_traitsData.setTraitProperty(
            all_properties_trait.kId, property_.name, property_.valid_value
        )
        a_trait = all_properties_trait(an_all_properties_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter() == property_.valid_value

    def test_when_trait_not_set_then_returns_None(
        self, all_properties_trait, an_empty_traitsData, property_
    ):
        a_trait = all_properties_trait(an_empty_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter() is None

    def test_when_trait_not_set_and_default_given_then_returns_default(
        self, all_properties_trait, an_empty_traitsData, property_
    ):
        a_trait = all_properties_trait(an_empty_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter(defaultValue=property_.valid_value) == property_.valid_value

    def test_when_property_not_set_then_returns_None(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        a_trait = all_properties_trait(an_all_properties_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter() is None

    def test_when_property_not_set_and_default_given_then_returns_default(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        a_trait = all_properties_trait(an_all_properties_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter(defaultValue=property_.valid_value) == property_.valid_value

    def test_when_property_has_wrong_type_then_raises_TypeError(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        an_all_properties_traitsData.setTraitProperty(
            all_properties_trait.kId, property_.name, property_.invalid_value
        )
        a_trait = all_properties_trait(an_all_properties_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        with pytest.raises(TypeError) as err:
            assert getter()

        assert (
            str(err.value)
            == f"Invalid stored value type: '{type(property_.invalid_value).__name__}' should be "
            f"'{type(property_.valid_value).__name__}'."
        )

    def test_when_property_has_wrong_type_and_default_given_then_returns_default(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        an_all_properties_traitsData.setTraitProperty(
            all_properties_trait.kId, property_.name, property_.invalid_value
        )
        a_trait = all_properties_trait(an_all_properties_traitsData)
        getter = getattr(a_trait, f"get{property_.name[0].upper()}{property_.name[1:]}")

        assert getter(defaultValue=property_.valid_value) == property_.valid_value


@pytest.mark.parametrize("property_", kAllPropertiesTrait_property_test_values)
class Test_AllPropertiesTrait_set:
    def test_when_set_then_trait_data_contains_value(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        a_trait = all_properties_trait(an_all_properties_traitsData)
        setter = getattr(a_trait, f"set{property_.name[0].upper()}{property_.name[1:]}")

        setter(property_.valid_value)

        actual = an_all_properties_traitsData.getTraitProperty(
            all_properties_trait.kId, property_.name
        )
        assert actual == property_.valid_value

    def test_when_traitsData_does_not_have_trait_then_set_also_imbues(
        self, all_properties_trait, an_empty_traitsData, property_
    ):
        a_trait = all_properties_trait(an_empty_traitsData)
        setter = getattr(a_trait, f"set{property_.name[0].upper()}{property_.name[1:]}")

        setter(property_.valid_value)

        actual = an_empty_traitsData.getTraitProperty(all_properties_trait.kId, property_.name)
        assert actual == property_.valid_value

    def test_when_type_is_wrong_then_TypeError_is_raised(
        self, all_properties_trait, an_all_properties_traitsData, property_
    ):
        a_trait = all_properties_trait(an_all_properties_traitsData)
        setter = getattr(a_trait, f"set{property_.name[0].upper()}{property_.name[1:]}")

        with pytest.raises(TypeError) as err:
            setter(property_.invalid_value)

        assert (
            # pylint: disable=line-too-long
            str(err.value)
            == f"{property_.name} must be a '{type(property_.valid_value).__name__}'."
        )


class Test_MultipleVersionsTrait:
    def test_version_1_has_expected_id(self, module_all):
        assert module_all.traits.aNamespace.MultipleVersionsTrait_v1.kId == (
            "openassetio-traitgen-test-all:aNamespace.MultipleVersions"
        )

    def test_version_2_has_expected_id(self, module_all):
        assert module_all.traits.aNamespace.MultipleVersionsTrait_v2.kId == (
            "openassetio-traitgen-test-all:aNamespace.MultipleVersions.v2"
        )

    def test_version_1_has_expected_docstring(self, module_all):
        assert (
            module_all.traits.aNamespace.MultipleVersionsTrait_v1.__doc__
            == """
    A trait with multiple versions, version 1.
    Usage: entity
    """
        )

    def test_version_2_has_expected_docstring(self, module_all):
        assert (
            module_all.traits.aNamespace.MultipleVersionsTrait_v2.__doc__
            == """
    A trait with multiple versions, version 2.
    """
        )

    def test_version_1_has_expected_property(self, module_all):
        assert hasattr(module_all.traits.aNamespace.MultipleVersionsTrait_v1, "getOldProperty")
        assert not hasattr(module_all.traits.aNamespace.MultipleVersionsTrait_v1, "getNewProperty")

    def test_version_2_has_expected_property(self, module_all):
        assert not hasattr(module_all.traits.aNamespace.MultipleVersionsTrait_v2, "getOldProperty")
        assert hasattr(module_all.traits.aNamespace.MultipleVersionsTrait_v2, "getNewProperty")

    def test_unversioned_is_version_1(self, module_all):
        assert issubclass(
            module_all.traits.aNamespace.MultipleVersionsTrait,
            module_all.traits.aNamespace.MultipleVersionsTrait_v1,
        )

        # Create an empty class and get its __dict__ keys.
        builtin_attr_names = set(type("Empty", (), {}).__dict__.keys())

        # Get attributes defined on subclass, minus builtin attrs.
        user_defined_attr_names = [
            attr_name
            for attr_name in module_all.traits.aNamespace.MultipleVersionsTrait.__dict__
            if attr_name not in builtin_attr_names
        ]
        # Ensure no overrides of the base class, other than constructor
        # (for deprecation warning).
        assert user_defined_attr_names == ["__init__"]

    def test_unversioned_has_same_docstring_as_version_1_but_with_deprecation(self, module_all):
        assert (
            module_all.traits.aNamespace.MultipleVersionsTrait.__doc__
            == module_all.traits.aNamespace.MultipleVersionsTrait_v1.__doc__.rstrip()
            + """

    @deprecated Unversioned trait view classes are deprecated, please
    use MultipleVersionsTrait_v1 explicitly.
    """
        )
        assert (
            module_all.traits.aNamespace.MultipleVersionsTrait.__doc__
            != module_all.traits.aNamespace.MultipleVersionsTrait_v2.__doc__
        )

    def test_when_unversioned_constructed_then_logs_deprecation_warning(self, module_all):
        expected_warning = (
            "Unversioned trait view classes are deprecated. Please switch from"
            " MultipleVersionsTrait to MultipleVersionsTrait_v1."
        )
        with pytest.deprecated_call(match=expected_warning):
            module_all.traits.aNamespace.MultipleVersionsTrait(TraitsData())

    def test_when_unversioned_constructed_then_calls_base_constructor(self, module_all):
        data = TraitsData()
        trait = module_all.traits.aNamespace.MultipleVersionsTrait(data)
        expected_value = "some string"
        # Ensure TraitsData is passed through (i.e. no AttributeError).
        trait.setOldProperty(expected_value)
        actual_value = trait.getOldProperty()

        assert actual_value == expected_value


class Test_DeprecatedTrait:
    def test_when_constructed_then_logs_deprecation_warning(self, module_all):
        expected_warning = (
            "The 'openassetio-traitgen-test-all:aNamespace.Deprecated' trait is deprecated."
        )
        with pytest.deprecated_call(match=expected_warning):
            module_all.traits.aNamespace.DeprecatedTrait_v1(TraitsData())

    def test_docstring_contains_deprecation_notice(self, module_all):
        assert (
            module_all.traits.aNamespace.DeprecatedTrait_v1.__doc__
            == """
    A deprecated trait.

    @deprecated This trait is flagged for future removal.
    """
        )


class Test_LocalAndExternalTraitSpecification:
    def test_external_trait_accessor_is_of_expected_type(
        self, local_and_external_trait_specification, module_traits_only
    ):
        a_specification = local_and_external_trait_specification(TraitsData())
        assert isinstance(
            a_specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait(),
            module_traits_only.traits.aNamespace.NoPropertiesTrait_v1,
        )

    def test_external_trait_instance_wraps_specifications_traits_data(
        self, local_and_external_trait_specification
    ):
        a_traits_data = TraitsData()
        a_specification = local_and_external_trait_specification(a_traits_data)
        a_trait = a_specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait()
        assert (
            a_trait._NoPropertiesTrait_v1__data  # pylint: disable=protected-access
            is a_traits_data
        )

    def test_package_local_trait_accessor_is_of_expected_type(
        self, local_and_external_trait_specification, module_all
    ):
        a_specification = local_and_external_trait_specification(TraitsData())
        assert isinstance(
            a_specification.openassetioTraitgenTestAllANamespaceNoPropertiesTrait(),
            module_all.traits.aNamespace.NoPropertiesTrait_v1,
        )

    def test_local_trait_instance_wraps_specifications_traits_data(
        self, local_and_external_trait_specification
    ):
        a_traits_data = TraitsData()
        a_specification = local_and_external_trait_specification(a_traits_data)
        a_trait = a_specification.openassetioTraitgenTestAllANamespaceNoPropertiesTrait()
        assert (
            a_trait._NoPropertiesTrait_v1__data  # pylint: disable=protected-access
            is a_traits_data
        )

    def test_default_constructor_raises_error(self, local_and_external_trait_specification):
        with pytest.raises(TypeError):
            local_and_external_trait_specification()  # pylint: disable=no-value-for-parameter

    def test_when_supplied_invalid_object_then_raises_TypeError(
        self, local_and_external_trait_specification
    ):
        with pytest.raises(TypeError):
            local_and_external_trait_specification({})
        with pytest.raises(TypeError):
            local_and_external_trait_specification(None)
        with pytest.raises(TypeError):
            local_and_external_trait_specification("a string")

    def test_all_traits_set_in_data(self, local_and_external_trait_specification):
        specification = local_and_external_trait_specification.create()
        data = specification.traitsData()
        assert data.traitSet() == local_and_external_trait_specification.kTraitSet


class Test_MultipleVersionsOfTraitSpecification:

    def test_version_1_has_version_1_of_trait(self, module_all):
        assert (
            module_all.specifications.test.MultipleVersionsOfTraitSpecification_v1.kTraitSet
            == {
                module_all.traits.aNamespace.MultipleVersionsTrait_v1.kId,
                module_all.traits.aNamespace.NoPropertiesTrait_v1.kId,
            }
        )

    def test_version_2_has_version_2_of_trait(self, module_all):
        assert (
            module_all.specifications.test.MultipleVersionsOfTraitSpecification_v2.kTraitSet
            == {
                module_all.traits.aNamespace.MultipleVersionsTrait_v2.kId,
                module_all.traits.aNamespace.NoPropertiesTrait_v1.kId,
            }
        )

    def test_unversioned_is_version_1(self, module_all):
        assert issubclass(
            module_all.specifications.test.MultipleVersionsOfTraitSpecification,
            module_all.specifications.test.MultipleVersionsOfTraitSpecification_v1,
        )

        # Create an empty class and get its __dict__ keys.
        builtin_attr_names = set(type("Empty", (), {}).__dict__.keys())

        # Get attributes defined on subclass, minus builtin attrs.
        user_defined_attr_names = [
            attr_name
            for attr_name in module_all.traits.aNamespace.MultipleVersionsTrait.__dict__
            if attr_name not in builtin_attr_names
        ]
        # Ensure no overrides of the base class, other than constructor
        # (for deprecation warning).
        assert user_defined_attr_names == ["__init__"]

    def test_unversioned_has_same_docstring_as_version_1_but_with_deprecation(self, module_all):
        spec = module_all.specifications.test.MultipleVersionsOfTraitSpecification
        spec_v1 = module_all.specifications.test.MultipleVersionsOfTraitSpecification_v1
        assert (
            spec.__doc__
            == spec_v1.__doc__.rstrip()
            + """

    @deprecated Unversioned specification view classes are deprecated,
    please use MultipleVersionsOfTraitSpecification_v1 explicitly.
    """
        )
        assert (
            module_all.specifications.test.MultipleVersionsOfTraitSpecification.__doc__
            != module_all.specifications.test.MultipleVersionsOfTraitSpecification_v2.__doc__
        )

    def test_when_unversioned_constructed_then_logs_deprecation_warning(self, module_all):
        expected_warning = (
            "Unversioned specification view classes are deprecated. Please switch from"
            " MultipleVersionsOfTraitSpecification to MultipleVersionsOfTraitSpecification_v1."
        )
        with pytest.deprecated_call(match=expected_warning):
            module_all.specifications.test.MultipleVersionsOfTraitSpecification(TraitsData())

        with pytest.deprecated_call(match=expected_warning):
            module_all.specifications.test.MultipleVersionsOfTraitSpecification.create()

    def test_when_unversioned_created_then_is_correct_instance(self, module_all):
        spec = module_all.specifications.test.MultipleVersionsOfTraitSpecification.create()

        assert isinstance(
            spec, module_all.specifications.test.MultipleVersionsOfTraitSpecification
        )

    def test_when_unversioned_constructed_then_calls_base_constructor(self, module_all):
        data = TraitsData()
        spec = module_all.specifications.test.MultipleVersionsOfTraitSpecification(data)
        expected_value = "some string"
        # Ensure TraitsData is passed through (i.e. no AttributeError).
        spec.multipleVersionsTrait().setOldProperty(expected_value)
        actual_value = spec.multipleVersionsTrait().getOldProperty()

        assert actual_value == expected_value


class Test_DeprecatedSpecification:
    def test_when_constructed_then_logs_deprecation_warning(self, module_all):
        expected_warning = (
            "The 'test.Deprecated' specification of the 'openassetio_traitgen_test_all' package is"
            " deprecated."
        )
        with pytest.deprecated_call(match=expected_warning):
            module_all.specifications.test.DeprecatedSpecification_v1(TraitsData())

    def test_docstring_contains_deprecation_notice(self, module_all):
        assert (
            module_all.specifications.test.DeprecatedSpecification_v1.__doc__
            == """
    A deprecated specification.

    @deprecated This specification is flagged for future removal.
    """
        )


class Test_generate:
    def test_when_files_created_then_creation_callback_is_called(
        self, declaration_exotic_values, creations_exotic_values, tmp_path_factory
    ):
        output_dir = tmp_path_factory.mktemp("test_python_generate_callback")
        expected = [os.path.join(output_dir, p) for p in creations_exotic_values]

        actual = []

        def creation_callback(path):
            actual.append(path)

        python_generator.generate(
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
        output_dir = tmp_path_factory.mktemp("test_python_generate_warnings")
        python_generator.generate(
            declaration_exotic_values, {}, output_dir, lambda _: _, a_capturing_logger
        )

        assert a_capturing_logger.handlers[0].messages == warnings_exotic_values


#
# Fixtures
#


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
            output_directory=output_dir,
            generator="python",
            creation_callback=creation_callback,
            logger=logging.Logger(name="Capturing logger"),
        )

    return output_dir


@pytest.fixture
def extended_python_path(generated_path, monkeypatch):
    """
    Temporarily extends sys.path to include the generated code directory.
    """
    monkeypatch.syspath_prepend(generated_path)


@pytest.fixture
def module_all(extended_python_path):
    """
    Retrieves the python module corresponding to the 'all' description.
    """
    # pylint: disable=import-error,unused-argument,import-outside-toplevel
    import openassetio_traitgen_test_all

    del sys.modules["openassetio_traitgen_test_all"]

    return openassetio_traitgen_test_all


@pytest.fixture
def module_traits_only(extended_python_path):
    """
    Retrieves the python module corresponding to the 'traits-only' description.
    """
    # pylint: disable=import-error,unused-argument,import-outside-toplevel
    import openassetio_traitgen_test_traits_only

    del sys.modules["openassetio_traitgen_test_traits_only"]

    return openassetio_traitgen_test_traits_only


@pytest.fixture
def module_specifications_only(extended_python_path):
    """
    Retrieves the python module corresponding to the 'specifications-only' description.
    """
    # pylint: disable=import-error,unused-argument,import-outside-toplevel
    import openassetio_traitgen_test_specifications_only

    del sys.modules["openassetio_traitgen_test_specifications_only"]

    return openassetio_traitgen_test_specifications_only


@pytest.fixture
def all_properties_trait(module_all):
    return module_all.traits.aNamespace.AllPropertiesTrait_v1


@pytest.fixture
def an_empty_traitsData():
    return TraitsData(set())


@pytest.fixture
def an_all_properties_traitsData(module_all):
    return TraitsData({module_all.traits.aNamespace.AllPropertiesTrait_v1.kId})


@pytest.fixture
def local_and_external_trait_specification(module_all):
    return module_all.specifications.test.LocalAndExternalTraitSpecification_v1


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
    ]
