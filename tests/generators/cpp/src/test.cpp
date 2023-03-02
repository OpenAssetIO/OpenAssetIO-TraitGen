// SPDX-License-Identifier: Apache-2.0
// Copyright 2022 The Foundry Visionmongers Ltd
#include <string_view>
#include <type_traits>

#include <catch2/catch.hpp>

#if defined OPENASSETIO_TRAITGENTEST_INCLUDES_PACKAGE
#include <openassetio_traitgen_test_all/openassetio_traitgen_test_all.hpp>
#include <openassetio_traitgen_test_specifications_only/openassetio_traitgen_test_specifications_only.hpp>
#elif defined OPENASSETIO_TRAITGENTEST_INCLUDES_SUBPACKAGE
#include <openassetio_traitgen_test_all/specifications/specifications.hpp>
#include <openassetio_traitgen_test_all/traits/traits.hpp>
#include <openassetio_traitgen_test_specifications_only/specifications/specifications.hpp>
#elif defined OPENASSETIO_TRAITGENTEST_INCLUDES_NAMESPACE
#include <openassetio_traitgen_test_all/specifications/test.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace.hpp>
#include <openassetio_traitgen_test_all/traits/anotherNamespace.hpp>
#include <openassetio_traitgen_test_specifications_only/specifications/test.hpp>
#else
#error "An #include style must be chosen"
#endif

TEST_CASE("openassetio_traitgen_test_all - all expected traits are defined") {
  using openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait;
  STATIC_REQUIRE(std::is_class_v<NoPropertiesTrait>);
  STATIC_REQUIRE(
      std::is_base_of_v<openassetio::trait::TraitBase<NoPropertiesTrait>, NoPropertiesTrait>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait>);
  STATIC_REQUIRE(
      std::is_class_v<openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait>);
  STATIC_REQUIRE(
      std::is_class_v<openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait>);
}

TEST_CASE("openassetio_traitgen_test_all - all expected specifications are defined") {
  STATIC_REQUIRE(std::is_class_v<openassetio_traitgen_test_all::specifications::test::
                                     LocalAndExternalTraitSpecification>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification>);
}

TEST_CASE("openassetio_traitgen_test_all - specifications have expected trait sets") {
  CHECK(openassetio_traitgen_test_all::specifications::test::LocalAndExternalTraitSpecification::
            kTraitSet ==
        openassetio::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId,
            openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification::
            kTraitSet ==
        openassetio::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId,
            openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification::
            kTraitSet ==
        openassetio::trait::TraitSet{
            openassetio_traitgen_test_traits_only::traits::test::AnotherTrait::kId});
}

TEST_CASE("openassetio_traitgen_test_all - traits have expected IDs") {
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId ==
        "openassetio-traitgen-test-all:aNamespace.NoProperties");
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait::kId ==
        "openassetio-traitgen-test-all:aNamespace.NoPropertiesMultipleUsage");
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait::kId ==
        "openassetio-traitgen-test-all:aNamespace.AllProperties");
  CHECK(openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait::kId ==
        "openassetio-traitgen-test-all:anotherNamespace.NoProperties");
}

namespace openassetio_traitgen_test_traits_only {
// Will fail if `specifications` is already defined (i.e. as namespace).
constexpr std::string_view specifications = "not defined";  // NOLINT
}  // namespace openassetio_traitgen_test_traits_only

TEST_CASE("openassetio_traitgen_test_traits_only - no specifications are defined") {
  STATIC_REQUIRE(openassetio_traitgen_test_traits_only::specifications == "not defined");
}

namespace openassetio_traitgen_test_specifications_only {
// Will fail if `traits` is already defined (i.e. as namespace).
constexpr std::string_view traits = "not defined";  // NOLINT
}  // namespace openassetio_traitgen_test_specifications_only

TEST_CASE("openassetio_traitgen_test_specifications_only - no traits are defined") {
  STATIC_REQUIRE(openassetio_traitgen_test_specifications_only::traits == "not defined");
}

namespace {
/**
 * Fixture struct for parameterizing tests on trait property type.
 *
 * Uses knowledge of the expected structure of the generated
 * AllPropertiesTrait.
 *
 * @tparam PropertyType Type of property to specialise for.
 */
template <typename PropertyType>
struct PropertyFixture;

template <>
struct PropertyFixture<openassetio::Bool> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio::trait::property::Key kPropertyKey = "boolProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Bool";
  static constexpr openassetio::Bool kDefaultValue = false;
  static constexpr openassetio::Bool kExpectedValue = true;
  static constexpr openassetio::Int kMismatchedTypeValue = 123;

  template <typename... Args>
  [[nodiscard]] auto getProperty(Args&&... args) const {
    return trait.getBoolProperty(std::forward<Args>(args)...);
  }

  template <typename... Args>
  void setProperty(Args&&... args) {
    trait.setBoolProperty(std::forward<Args>(args)...);
  }
};

template <>
struct PropertyFixture<openassetio::Int> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio::trait::property::Key kPropertyKey = "intProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Int";
  static constexpr openassetio::Int kDefaultValue = 456;
  static constexpr openassetio::Int kExpectedValue = 123;
  static constexpr openassetio::Bool kMismatchedTypeValue = true;

  template <typename... Args>
  [[nodiscard]] auto getProperty(Args&&... args) const {
    return trait.getIntProperty(std::forward<Args>(args)...);
  }

  template <typename... Args>
  void setProperty(Args&&... args) {
    trait.setIntProperty(std::forward<Args>(args)...);
  }
};

template <>
struct PropertyFixture<openassetio::Float> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio::trait::property::Key kPropertyKey = "floatProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Float";
  static constexpr openassetio::Float kDefaultValue = 12.3;
  static constexpr openassetio::Float kExpectedValue = 45.6;
  static constexpr openassetio::Int kMismatchedTypeValue = 123;

  template <typename... Args>
  [[nodiscard]] auto getProperty(Args&&... args) const {
    return trait.getFloatProperty(std::forward<Args>(args)...);
  }

  template <typename... Args>
  void setProperty(Args&&... args) {
    trait.setFloatProperty(std::forward<Args>(args)...);
  }
};

template <>
struct PropertyFixture<openassetio::Str> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio::trait::property::Key kPropertyKey = "stringProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Str";
  static inline const openassetio::Str kDefaultValue = "⛅ outside today";
  static inline const openassetio::Str kExpectedValue = "🐁";
  static constexpr openassetio::Int kMismatchedTypeValue = 123;

  template <typename... Args>
  [[nodiscard]] auto getProperty(Args&&... args) const {
    return trait.getStringProperty(std::forward<Args>(args)...);
  }

  template <typename... Args>
  void setProperty(Args&&... args) {
    trait.setStringProperty(std::forward<Args>(args)...);
  }
};
}  // namespace

TEMPLATE_TEST_CASE("Property getters", "", openassetio::Bool, openassetio::Int, openassetio::Float,
                   openassetio::Str) {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a fully populated TraitsData") {
    const openassetio::TraitsDataPtr traitsData =
        openassetio::TraitsData::make({AllPropertiesTrait::kId});

    traitsData->setTraitProperty(AllPropertiesTrait::kId, Fixture::kPropertyKey,
                                 Fixture::kExpectedValue);

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      const PropertyType value = fixture.getProperty();

      THEN("value is as expected") { CHECK(value == Fixture::kExpectedValue); }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("value is as expected") { CHECK(value == Fixture::kExpectedValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of an imbued TraitsData with no properties set") {
    const openassetio::TraitsDataPtr traitsData =
        openassetio::TraitsData::make({AllPropertiesTrait::kId});

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      THEN("exception is thrown") {
        CHECK_THROWS_MATCHES(fixture.getProperty(), std::runtime_error,
                             Catch::Matchers::Message("Property is not set."));
      }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

    const openassetio::TraitsDataPtr traitsData = openassetio::TraitsData::make();

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      THEN("exception is thrown") {
        // TODO(DF): better deterministic exception message.
        CHECK_THROWS_AS(fixture.getProperty(), std::out_of_range);
      }
    }

    WHEN("property is queried with a default") {
      THEN("exception is thrown") {
        // TODO(DF): better deterministic exception message.
        CHECK_THROWS_AS(fixture.getProperty(Fixture::kDefaultValue), std::out_of_range);
      }
    }
  }

  GIVEN("an AllPropertiesTrait view of a TraitsData populated with unexpected types") {
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

    const openassetio::TraitsDataPtr traitsData =
        openassetio::TraitsData::make({AllPropertiesTrait::kId});

    traitsData->setTraitProperty(AllPropertiesTrait::kId, Fixture::kPropertyKey,
                                 Fixture::kMismatchedTypeValue);

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      THEN("exception is thrown") {
        std::string expectedMsg = "Invalid stored value type: should be '";
        expectedMsg += Fixture::kPropertyType;
        expectedMsg += "'.";

        CHECK_THROWS_MATCHES(fixture.getProperty(), std::runtime_error,
                             Catch::Matchers::Message(expectedMsg));
      }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }
}

TEMPLATE_TEST_CASE("Property setters", "", openassetio::Bool, openassetio::Int, openassetio::Float,
                   openassetio::Str) {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio::TraitsDataPtr traitsData = openassetio::TraitsData::make();
    Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is set") {
      fixture.setProperty(Fixture::kExpectedValue);

      THEN("TraitsData contains expected value") {
        openassetio::trait::property::Value value;
        [[maybe_unused]] const bool hasProp =
            traitsData->getTraitProperty(&value, AllPropertiesTrait::kId, Fixture::kPropertyKey);

        const PropertyType actualValue = std::get<PropertyType>(value);

        CHECK(actualValue == Fixture::kExpectedValue);
      }

      THEN("TraitsData has been imbued") { CHECK(traitsData->hasTrait(AllPropertiesTrait::kId)); }
    }
  }
}

SCENARIO("Moveable property setters") {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio::TraitsDataPtr traitsData = openassetio::TraitsData::make();
    AllPropertiesTrait trait{traitsData};

    WHEN("string property is set with a moveable string") {
      std::string value = "some string";
      trait.setStringProperty(std::move(value));

      THEN("string has been moved") {
        // Rely on clang-tidy and/or compiler warnings (-as-errors) to
        // flag an unsatisfied std::move.
      }
    }
  }
}

SCENARIO("LocalAndExternalTraitSpecification") {
  GIVEN("a LocalAndExternalTraitSpecification") {
    const auto traitsData = openassetio::TraitsData::make();

    const openassetio_traitgen_test_all::specifications::test::LocalAndExternalTraitSpecification
        specification{traitsData};

    WHEN("an externally defined trait view is requested") {
      const auto trait =
          specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                std::remove_const_t<decltype(trait)>,
                openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait>);
      }

      AND_WHEN("the trait view's TraitsData is imbued by the trait view") {
        trait.imbue();

        THEN("the specification's TraitsData is updated") {
          CHECK(traitsData->hasTrait(
              openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait::kId));
        }
      }
    }

    WHEN("a locally defined trait view is requested") {
      const auto trait = specification.openassetioTraitgenTestAllANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<std::remove_const_t<decltype(trait)>,
                           openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait>);
      }

      AND_WHEN("the trait view's TraitsData is imbued by the trait view") {
        trait.imbue();

        THEN("the specification's TraitsData is updated") {
          CHECK(traitsData->hasTrait(
              openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId));
        }
      }
    }
  }
}
