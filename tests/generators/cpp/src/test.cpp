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
#elif defined OPENASSETIO_TRAITGENTEST_INCLUDES_CLASS
#include <openassetio_traitgen_test_all/specifications/test/LocalAndExternalTraitSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/OneExternalTraitSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/TwoLocalTraitsSpecification.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/AllPropertiesTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/NoPropertiesMultipleUsageTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/NoPropertiesTrait.hpp>
#include <openassetio_traitgen_test_all/traits/anotherNamespace/NoPropertiesTrait.hpp>
#include <openassetio_traitgen_test_specifications_only/specifications/test/SomeSpecification.hpp>
#else
#error "An #include style must be chosen"
#endif

namespace openassetio_abi = openassetio::v1;

TEST_CASE("openassetio_traitgen_test_all - all expected traits are defined") {
  STATIC_REQUIRE(
      std::is_class_v<openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait>);
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

TEST_CASE("openassetio_traitgen_test_all - traits are under an ABI namespace") {
  STATIC_REQUIRE(
      std::is_same_v<openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait,
                     openassetio_traitgen_test_all::v1::traits::aNamespace::NoPropertiesTrait>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait,
          openassetio_traitgen_test_all::v1::traits::aNamespace::NoPropertiesMultipleUsageTrait>);
  STATIC_REQUIRE(
      std::is_same_v<openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait,
                     openassetio_traitgen_test_all::v1::traits::aNamespace::AllPropertiesTrait>);
  STATIC_REQUIRE(std::is_same_v<
                 openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait,
                 openassetio_traitgen_test_all::v1::traits::anotherNamespace::NoPropertiesTrait>);
}

TEST_CASE("openassetio_traitgen_test_all - specifications are under an ABI namespace") {
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification,
          openassetio_traitgen_test_all::v1::specifications::test::OneExternalTraitSpecification>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification,
          openassetio_traitgen_test_all::v1::specifications::test::OneExternalTraitSpecification>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification,
          openassetio_traitgen_test_all::v1::specifications::test::TwoLocalTraitsSpecification>);
}

TEST_CASE("openassetio_traitgen_test_all - specifications have expected trait sets") {
  CHECK(openassetio_traitgen_test_all::specifications::test::LocalAndExternalTraitSpecification::
            kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId,
            openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification::
            kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId,
            openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification::
            kTraitSet ==
        openassetio_abi::trait::TraitSet{
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

SCENARIO("Common specification utility functions") {
  GIVEN("a specification constructed using its create function") {
    auto specification =
        openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification::create();

    WHEN("its TraitsData is retrieved") {
      openassetio::trait::TraitsDataPtr traitsData;
      traitsData = specification.traitsData();

      THEN("the TraitsData is imbued with the expected traits") {
        CHECK(
            traitsData->traitSet() ==
            openassetio::trait::TraitSet{
                openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait::kId,
                openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait::kId});
      }

      AND_WHEN("the retrieved TraitsData is modified") {
        traitsData->addTrait("dummy_trait");

        THEN("the specification's TraitsData has been updated") {
          CHECK(specification.traitsData()->hasTrait("dummy_trait"));
        }
      }
    }
  }
}

SCENARIO("Common trait utility functions") {
  GIVEN("a TraitsData and a trait view on it") {
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;
    auto traitsData = openassetio::trait::TraitsData::make();
    const AllPropertiesTrait trait{traitsData};

    WHEN("trait view class method is used to query whether TraitsData is imbued") {
      const bool isImbued = AllPropertiesTrait::isImbuedTo(traitsData);

      THEN("it is not yet imbued") { CHECK(isImbued == false); }
    }
    WHEN("trait view instance method is used to query whether TraitsData is imbued") {
      const bool isImbued = trait.isImbued();

      THEN("it is not yet imbued") { CHECK(isImbued == false); }
    }

    AND_GIVEN("TraitsData is imbued with the trait") {
      traitsData->addTrait(AllPropertiesTrait::kId);

      WHEN("trait view class method is used to query whether TraitsData is imbued") {
        const bool isImbued = AllPropertiesTrait::isImbuedTo(traitsData);

        THEN("it is imbued") { CHECK(isImbued == true); }
      }
      WHEN("trait view instance method is used to query whether TraitsData is imbued") {
        const bool isImbued = trait.isImbued();

        THEN("it is imbued") { CHECK(isImbued == true); }
      }
    }

    WHEN("trait view class method is used to imbue the TraitsData") {
      AllPropertiesTrait::imbueTo(traitsData);

      THEN("TraitsData is imbued") { CHECK(traitsData->hasTrait(AllPropertiesTrait::kId)); }
    }

    WHEN("trait view instance method is used to imbue the TraitsData") {
      trait.imbue();

      THEN("TraitsData is imbued") { CHECK(traitsData->hasTrait(AllPropertiesTrait::kId)); }
    }
  }
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
struct PropertyFixture<openassetio_abi::Bool> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio_abi::trait::property::Key kPropertyKey = "boolProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Bool";
  static constexpr openassetio_abi::Bool kDefaultValue = false;
  static constexpr openassetio_abi::Bool kExpectedValue = true;
  static constexpr openassetio_abi::Int kMismatchedTypeValue = 123;

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
struct PropertyFixture<openassetio_abi::Int> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio_abi::trait::property::Key kPropertyKey = "intProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Int";
  static constexpr openassetio_abi::Int kDefaultValue = 456;
  static constexpr openassetio_abi::Int kExpectedValue = 123;
  static constexpr openassetio_abi::Bool kMismatchedTypeValue = true;

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
struct PropertyFixture<openassetio_abi::Float> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio_abi::trait::property::Key kPropertyKey = "floatProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Float";
  static constexpr openassetio_abi::Float kDefaultValue = 12.3;
  static constexpr openassetio_abi::Float kExpectedValue = 45.6;
  static constexpr openassetio_abi::Int kMismatchedTypeValue = 123;

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
struct PropertyFixture<openassetio_abi::Str> {
  using AllPropertiesTrait = openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  AllPropertiesTrait trait;

  static inline const openassetio_abi::trait::property::Key kPropertyKey = "stringProperty";
  static constexpr std::string_view kPropertyType = "openassetio::Str";
  static inline const openassetio_abi::Str kDefaultValue = "⛅ outside today";
  static inline const openassetio_abi::Str kExpectedValue = "🐁";
  static constexpr openassetio_abi::Int kMismatchedTypeValue = 123;

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

TEMPLATE_TEST_CASE("Property getters", "", openassetio_abi::Bool, openassetio_abi::Int,
                   openassetio_abi::Float, openassetio_abi::Str) {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a fully populated TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait::kId});

    traitsData->setTraitProperty(AllPropertiesTrait::kId, Fixture::kPropertyKey,
                                 Fixture::kExpectedValue);

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      const std::optional<PropertyType> value = fixture.getProperty();

      THEN("value is as expected") {
        REQUIRE(value.has_value());
        // Guard required because clang-tidy isn't clever enough to
        // understand the require.
        if (value.has_value()) {
          CHECK(value.value() == Fixture::kExpectedValue);
        }
      }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("value is as expected") { CHECK(value == Fixture::kExpectedValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of an imbued TraitsData with no properties set") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait::kId});

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      THEN("optional return is empty") { CHECK(!fixture.getProperty().has_value()); }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();

    const Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is queried without a default") {
      THEN("optional return is empty") { CHECK(!fixture.getProperty().has_value()); }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of a TraitsData populated with unexpected types") {
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait::kId});

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

TEMPLATE_TEST_CASE("Property setters", "", openassetio_abi::Bool, openassetio_abi::Int,
                   openassetio_abi::Float, openassetio_abi::Str) {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();
    Fixture fixture{AllPropertiesTrait{traitsData}};

    WHEN("property is set") {
      fixture.setProperty(Fixture::kExpectedValue);

      THEN("TraitsData contains expected value") {
        openassetio_abi::trait::property::Value value;
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
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();
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

SCENARIO("Specifications providing trait views") {
  GIVEN("a LocalAndExternalTraitSpecification") {
    const auto specification = openassetio_traitgen_test_all::specifications::test::
        LocalAndExternalTraitSpecification::create();

    WHEN(
        "an openassetio-traitgen-test-traits-only:aNamespace.NoProperties trait view is "
        "requested") {
      const auto trait =
          specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<decltype(trait), const openassetio_traitgen_test_traits_only::traits::
                                                aNamespace::NoPropertiesTrait>);
      }
    }

    WHEN("an openassetio-traitgen-test-all:aNamespace.NoProperties trait view is requested") {
      const auto trait = specification.openassetioTraitgenTestAllANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait>);
      }
    }
  }

  GIVEN("a OneExternalTraitSpecification") {
    const auto specification = openassetio_traitgen_test_all::specifications::test::
        OneExternalTraitSpecification::create();

    WHEN("an AnotherTrait trait view is requested") {
      const auto trait = specification.anotherTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(std::is_same_v<
                       decltype(trait),
                       const openassetio_traitgen_test_traits_only::traits::test::AnotherTrait>);
      }
    }
  }

  GIVEN("a TwoLocalTraitsSpecification") {
    const auto specification =
        openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification::create();

    WHEN("an aNamespace.NoPropertiesTrait trait view is requested") {
      const auto trait = specification.aNamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait>);
      }
    }

    WHEN("an anotherNamespace.NoPropertiesTrait trait view is requested") {
      const auto trait = specification.anotherNamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait>);
      }
    }
  }

  GIVEN("a SomeSpecification") {
    const auto specification = openassetio_traitgen_test_specifications_only::specifications::
        test::SomeSpecification::create();

    WHEN("an AllPropertiesTrait trait view is requested") {
      const auto trait = specification.allPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait>);
      }
    }

    WHEN("an AnotherTrait trait view is requested") {
      const auto trait = specification.anotherTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(std::is_same_v<
                       decltype(trait),
                       const openassetio_traitgen_test_traits_only::traits::test::AnotherTrait>);
      }
    }
  }
}

SCENARIO("Specification-provided trait views updating wrapped TraitsData") {
  GIVEN("an external TraitsData") {
    const auto traitsData = openassetio_abi::trait::TraitsData::make();

    AND_GIVEN("a specification wrapping the TraitsData") {
      const openassetio_traitgen_test_all::specifications::test::LocalAndExternalTraitSpecification
          specification{traitsData};

      THEN("TraitsData has not yet been imbued") {
        CHECK(!traitsData->hasTrait(
            openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait::kId));
      }

      AND_GIVEN("a trait view requested from the specification") {
        const auto trait =
            specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait();

        WHEN("the trait view's TraitsData is imbued by the trait view") {
          trait.imbue();

          THEN("the specification's TraitsData is also updated") {
            CHECK(traitsData->hasTrait(openassetio_traitgen_test_traits_only::traits::aNamespace::
                                           NoPropertiesTrait::kId));
          }
        }
      }
    }
  }
}
