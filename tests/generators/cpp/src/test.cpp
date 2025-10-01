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
#include <openassetio_traitgen_test_all/specifications/test/DeprecatedSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/LocalAndExternalTraitSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/MultipleVersionsOfTraitSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/OneExternalTraitSpecification.hpp>
#include <openassetio_traitgen_test_all/specifications/test/TwoLocalTraitsSpecification.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/AllPropertiesTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/DeprecatedTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/MultipleVersionsTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/NoPropertiesMultipleUsageTrait.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace/NoPropertiesTrait.hpp>
#include <openassetio_traitgen_test_all/traits/anotherNamespace/NoPropertiesTrait.hpp>
#include <openassetio_traitgen_test_specifications_only/specifications/test/SomeSpecification.hpp>
#else
#error "An #include style must be chosen"
#endif

namespace openassetio_abi = openassetio::v1;

// False-positive linter errors with Catch2 macros.
// NOLINTBEGIN(bugprone-chained-comparison)

TEST_CASE("openassetio_traitgen_test_all - all expected traits are defined") {
  STATIC_REQUIRE(
      std::is_class_v<openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait_v1>);
  STATIC_REQUIRE(
      std::is_class_v<openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1>);
  STATIC_REQUIRE(std::is_class_v<
                 openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait_v1>);
  STATIC_REQUIRE(std::is_class_v<
                 openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1>);
  STATIC_REQUIRE(std::is_class_v<
                 openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2>);
}

TEST_CASE("openassetio_traitgen_test_all - all expected specifications are defined") {
  STATIC_REQUIRE(std::is_class_v<openassetio_traitgen_test_all::specifications::test::
                                     LocalAndExternalTraitSpecification_v1>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification_v1>);
  STATIC_REQUIRE(
      std::is_class_v<
          openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification_v1>);
  STATIC_REQUIRE(std::is_class_v<openassetio_traitgen_test_all::specifications::test::
                                     MultipleVersionsOfTraitSpecification_v1>);
  STATIC_REQUIRE(std::is_class_v<openassetio_traitgen_test_all::specifications::test::
                                     MultipleVersionsOfTraitSpecification_v2>);
}

TEST_CASE("openassetio_traitgen_test_all - traits are under an ABI namespace") {
  STATIC_REQUIRE(
      std::is_same_v<openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1,
                     openassetio_traitgen_test_all::v1::traits::aNamespace::NoPropertiesTrait_v1>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait_v1,
          openassetio_traitgen_test_all::v1::traits::aNamespace::
              NoPropertiesMultipleUsageTrait_v1>);
  STATIC_REQUIRE(std::is_same_v<
                 openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1,
                 openassetio_traitgen_test_all::v1::traits::aNamespace::AllPropertiesTrait_v1>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait_v1,
          openassetio_traitgen_test_all::v1::traits::anotherNamespace::NoPropertiesTrait_v1>);
  STATIC_REQUIRE(std::is_same_v<
                 openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1,
                 openassetio_traitgen_test_all::v1::traits::aNamespace::MultipleVersionsTrait_v1>);
  STATIC_REQUIRE(std::is_same_v<
                 openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2,
                 openassetio_traitgen_test_all::v1::traits::aNamespace::MultipleVersionsTrait_v2>);
}

TEST_CASE("openassetio_traitgen_test_all - specifications are under an ABI namespace") {
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification_v1,
          openassetio_traitgen_test_all::v1::specifications::test::
              OneExternalTraitSpecification_v1>);
  STATIC_REQUIRE(
      std::is_same_v<
          openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification_v1,
          openassetio_traitgen_test_all::v1::specifications::test::
              TwoLocalTraitsSpecification_v1>);
  STATIC_REQUIRE(std::is_same_v<openassetio_traitgen_test_all::specifications::test::
                                    MultipleVersionsOfTraitSpecification_v1,
                                openassetio_traitgen_test_all::v1::specifications::test::
                                    MultipleVersionsOfTraitSpecification_v1>);
  STATIC_REQUIRE(std::is_same_v<openassetio_traitgen_test_all::specifications::test::
                                    MultipleVersionsOfTraitSpecification_v2,
                                openassetio_traitgen_test_all::v1::specifications::test::
                                    MultipleVersionsOfTraitSpecification_v2>);
}

TEST_CASE("openassetio_traitgen_test_all - specifications have expected trait sets") {
  CHECK(openassetio_traitgen_test_all::specifications::test::
            LocalAndExternalTraitSpecification_v1::kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId,
            openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait_v1::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::TwoLocalTraitsSpecification_v1::
            kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId,
            openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait_v1::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::OneExternalTraitSpecification_v1::
            kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_traits_only::traits::test::AnotherTrait_v1::kId});
  CHECK(openassetio_traitgen_test_all::specifications::test::
            MultipleVersionsOfTraitSpecification_v1::kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId,
            openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1::kId,
        });
  CHECK(openassetio_traitgen_test_all::specifications::test::
            MultipleVersionsOfTraitSpecification_v2::kTraitSet ==
        openassetio_abi::trait::TraitSet{
            openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId,
            openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2::kId,
        });
}

TEST_CASE("openassetio_traitgen_test_all - traits have expected IDs") {
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId ==
        "openassetio-traitgen-test-all:aNamespace.NoProperties");
  CHECK(
      openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesMultipleUsageTrait_v1::kId ==
      "openassetio-traitgen-test-all:aNamespace.NoPropertiesMultipleUsage");
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1::kId ==
        "openassetio-traitgen-test-all:aNamespace.AllProperties");
  CHECK(openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait_v1::kId ==
        "openassetio-traitgen-test-all:anotherNamespace.NoProperties");
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1::kId ==
        "openassetio-traitgen-test-all:aNamespace.MultipleVersions");
  CHECK(openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2::kId ==
        "openassetio-traitgen-test-all:aNamespace.MultipleVersions.v2");
}

SCENARIO("Unversioned trait") {
  using openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait;
  using openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1;
  using openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2;

  THEN("unversioned trait is a subclass of v1") {
    STATIC_REQUIRE(std::is_base_of_v<MultipleVersionsTrait_v1, MultipleVersionsTrait>);
  }

  WHEN("ID of unversioned trait is retrieved") {
    const auto traitId = MultipleVersionsTrait::kId;

    THEN("unversioned trait ID is the same as v1") {
      CHECK(traitId == MultipleVersionsTrait_v1::kId);
      CHECK(traitId != MultipleVersionsTrait_v2::kId);
    }
  }

  WHEN("unversioned trait is constructed") {
    const auto traitsData = openassetio::trait::TraitsData::make();
    // Construct rather than using static_assert to be confident that
    // the constructor is available.

    const MultipleVersionsTrait trait{traitsData};

    THEN("unversioned trait has same members as v1") {
      // Just checking that the member function exists.
      CHECK(!trait.getOldProperty().has_value());
    }
  }
}

TEST_CASE("Deprecated trait causes deprecation compiler warning") {
  // Ensure that the deprecated trait does indeed cause a deprecation
  // warning if used. Note that to see this we must remove the
  // diagnostic suppression. See
  // openassetio-traitgentest-deprecations CTest target.
  using openassetio_traitgen_test_all::traits::aNamespace::DeprecatedTrait_v1;

  const DeprecatedTrait_v1 trait{openassetio::trait::TraitsData::make()};
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
    auto specification = openassetio_traitgen_test_all::specifications::test::
        TwoLocalTraitsSpecification_v1::create();

    WHEN("its TraitsData is retrieved") {
      const openassetio::trait::TraitsDataPtr& traitsData = specification.traitsData();

      THEN("the TraitsData is imbued with the expected traits") {
        CHECK(traitsData->traitSet() ==
              openassetio::trait::TraitSet{
                  openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1::kId,
                  openassetio_traitgen_test_all::traits::anotherNamespace::NoPropertiesTrait_v1::
                      kId});
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
    using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;
    auto traitsData = openassetio::trait::TraitsData::make();
    const AllPropertiesTrait_v1 trait{traitsData};

    WHEN("trait view class method is used to query whether TraitsData is imbued") {
      const bool isImbued = AllPropertiesTrait_v1::isImbuedTo(traitsData);

      THEN("it is not yet imbued") { CHECK(isImbued == false); }
    }
    WHEN("trait view instance method is used to query whether TraitsData is imbued") {
      const bool isImbued = trait.isImbued();

      THEN("it is not yet imbued") { CHECK(isImbued == false); }
    }

    AND_GIVEN("TraitsData is imbued with the trait") {
      traitsData->addTrait(AllPropertiesTrait_v1::kId);

      WHEN("trait view class method is used to query whether TraitsData is imbued") {
        const bool isImbued = AllPropertiesTrait_v1::isImbuedTo(traitsData);

        THEN("it is imbued") { CHECK(isImbued == true); }
      }
      WHEN("trait view instance method is used to query whether TraitsData is imbued") {
        const bool isImbued = trait.isImbued();

        THEN("it is imbued") { CHECK(isImbued == true); }
      }
    }

    WHEN("trait view class method is used to imbue the TraitsData") {
      AllPropertiesTrait_v1::imbueTo(traitsData);

      THEN("TraitsData is imbued") { CHECK(traitsData->hasTrait(AllPropertiesTrait_v1::kId)); }
    }

    WHEN("trait view instance method is used to imbue the TraitsData") {
      trait.imbue();

      THEN("TraitsData is imbued") { CHECK(traitsData->hasTrait(AllPropertiesTrait_v1::kId)); }
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
  using AllPropertiesTrait =
      openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

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
  using AllPropertiesTrait =
      openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

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
  using AllPropertiesTrait =
      openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

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
  using AllPropertiesTrait =
      openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

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
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a fully populated TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait_v1::kId});

    traitsData->setTraitProperty(AllPropertiesTrait_v1::kId, Fixture::kPropertyKey,
                                 Fixture::kExpectedValue);

    const Fixture fixture{AllPropertiesTrait_v1{traitsData}};

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
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait_v1::kId});

    const Fixture fixture{AllPropertiesTrait_v1{traitsData}};

    WHEN("property is queried without a default") {
      THEN("optional return is empty") { CHECK(!fixture.getProperty().has_value()); }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();

    const Fixture fixture{AllPropertiesTrait_v1{traitsData}};

    WHEN("property is queried without a default") {
      THEN("optional return is empty") { CHECK(!fixture.getProperty().has_value()); }
    }

    WHEN("property is queried with a default") {
      const PropertyType value = fixture.getProperty(Fixture::kDefaultValue);

      THEN("default is returned") { CHECK(value == Fixture::kDefaultValue); }
    }
  }

  GIVEN("an AllPropertiesTrait view of a TraitsData populated with unexpected types") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make({AllPropertiesTrait_v1::kId});

    traitsData->setTraitProperty(AllPropertiesTrait_v1::kId, Fixture::kPropertyKey,
                                 Fixture::kMismatchedTypeValue);

    const Fixture fixture{AllPropertiesTrait_v1{traitsData}};

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
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

  using PropertyType = TestType;  // Catch2-injected template param.
  using Fixture = PropertyFixture<PropertyType>;

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();
    Fixture fixture{AllPropertiesTrait_v1{traitsData}};

    WHEN("property is set") {
      fixture.setProperty(Fixture::kExpectedValue);

      THEN("TraitsData contains expected value") {
        openassetio_abi::trait::property::Value value;
        [[maybe_unused]] const bool hasProp = traitsData->getTraitProperty(
            &value, AllPropertiesTrait_v1::kId, Fixture::kPropertyKey);

        const PropertyType actualValue = std::get<PropertyType>(value);

        CHECK(actualValue == Fixture::kExpectedValue);
      }

      THEN("TraitsData has been imbued") {
        CHECK(traitsData->hasTrait(AllPropertiesTrait_v1::kId));
      }
    }
  }
}

SCENARIO("Moveable property setters") {
  using openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1;

  GIVEN("an AllPropertiesTrait view of a blank TraitsData") {
    const openassetio_abi::trait::TraitsDataPtr traitsData =
        openassetio_abi::trait::TraitsData::make();
    AllPropertiesTrait_v1 trait{traitsData};

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
        LocalAndExternalTraitSpecification_v1::create();

    WHEN(
        "an openassetio-traitgen-test-traits-only:aNamespace.NoProperties trait view is "
        "requested") {
      const auto trait =
          specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<decltype(trait), const openassetio_traitgen_test_traits_only::traits::
                                                aNamespace::NoPropertiesTrait_v1>);
      }
    }
    WHEN("an openassetio-traitgen-test-all:aNamespace.NoProperties trait view is requested") {
      const auto trait = specification.openassetioTraitgenTestAllANamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1>);
      }
    }
  }
  GIVEN("a OneExternalTraitSpecification") {
    const auto specification = openassetio_traitgen_test_all::specifications::test::
        OneExternalTraitSpecification_v1::create();

    WHEN("an AnotherTrait trait view is requested") {
      const auto trait = specification.anotherTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_traits_only::traits::test::AnotherTrait_v1>);
      }
    }
  }
  GIVEN("a TwoLocalTraitsSpecification") {
    const auto specification = openassetio_traitgen_test_all::specifications::test::
        TwoLocalTraitsSpecification_v1::create();

    WHEN("an aNamespace.NoPropertiesTrait trait view is requested") {
      const auto trait = specification.aNamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1>);
      }
    }
    WHEN("an anotherNamespace.NoPropertiesTrait trait view is requested") {
      const auto trait = specification.anotherNamespaceNoPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<decltype(trait), const openassetio_traitgen_test_all::traits::
                                                anotherNamespace::NoPropertiesTrait_v1>);
      }
    }
  }
  GIVEN("a SomeSpecification") {
    const auto specification = openassetio_traitgen_test_specifications_only::specifications::
        test::SomeSpecification_v1::create();

    WHEN("an AllPropertiesTrait trait view is requested") {
      const auto trait = specification.allPropertiesTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_all::traits::aNamespace::AllPropertiesTrait_v1>);
      }
    }
    WHEN("an AnotherTrait trait view is requested") {
      const auto trait = specification.anotherTrait();

      THEN("trait view has expected type") {
        STATIC_REQUIRE(
            std::is_same_v<
                decltype(trait),
                const openassetio_traitgen_test_traits_only::traits::test::AnotherTrait_v1>);
      }
    }
  }
}

SCENARIO("Specification-provided trait views updating wrapped TraitsData") {
  GIVEN("an external TraitsData") {
    const auto traitsData = openassetio_abi::trait::TraitsData::make();

    AND_GIVEN("a specification wrapping the TraitsData") {
      const openassetio_traitgen_test_all::specifications::test::
          LocalAndExternalTraitSpecification_v1 specification{traitsData};

      THEN("TraitsData has not yet been imbued") {
        CHECK(!traitsData->hasTrait(
            openassetio_traitgen_test_traits_only::traits::aNamespace::NoPropertiesTrait_v1::kId));
      }
      AND_GIVEN("a trait view requested from the specification") {
        const auto trait =
            specification.openassetioTraitgenTestTraitsOnlyANamespaceNoPropertiesTrait();

        WHEN("the trait view's TraitsData is imbued by the trait view") {
          trait.imbue();

          THEN("the specification's TraitsData is also updated") {
            CHECK(traitsData->hasTrait(openassetio_traitgen_test_traits_only::traits::aNamespace::
                                           NoPropertiesTrait_v1::kId));
          }
        }
      }
    }
  }
}

SCENARIO("Specifications using different versions of traits") {
  using openassetio_traitgen_test_all::specifications::test::
      MultipleVersionsOfTraitSpecification_v1;
  using openassetio_traitgen_test_all::specifications::test::
      MultipleVersionsOfTraitSpecification_v2;
  GIVEN("two versions of a specification that expose different versions of the same traits") {
    using openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v1;
    using openassetio_traitgen_test_all::traits::aNamespace::MultipleVersionsTrait_v2;
    using openassetio_traitgen_test_all::traits::aNamespace::NoPropertiesTrait_v1;

    THEN("the two specifications expose the same methods but return different versioned traits") {
      STATIC_REQUIRE(
          std::is_same_v<std::decay_t<decltype(MultipleVersionsOfTraitSpecification_v1::create()
                                                   .multipleVersionsTrait())>,
                         MultipleVersionsTrait_v1>);
      STATIC_REQUIRE(
          std::is_same_v<std::decay_t<decltype(MultipleVersionsOfTraitSpecification_v2::create()
                                                   .multipleVersionsTrait())>,
                         MultipleVersionsTrait_v2>);
    }

    AND_GIVEN("an unversioned specification type") {
      using openassetio_traitgen_test_all::specifications::test::
          MultipleVersionsOfTraitSpecification;

      THEN("the trait set of the unversioned specification matches that of v1") {
        CHECK(MultipleVersionsOfTraitSpecification::kTraitSet ==
              MultipleVersionsOfTraitSpecification_v1::kTraitSet);
        CHECK(MultipleVersionsOfTraitSpecification::kTraitSet !=
              MultipleVersionsOfTraitSpecification_v2::kTraitSet);
      }

      WHEN("unversioned specification is constructed") {
        const auto traitsData = openassetio::trait::TraitsData::make();
        // Construct rather than using static_assert to be confident that
        // the constructor is available.
        const MultipleVersionsOfTraitSpecification specification{traitsData};

        THEN("unversioned specification has same members as v1") {
          // Just checking that the member function exists.
          CHECK(!specification.multipleVersionsTrait().getOldProperty().has_value());
        }
      }

      WHEN("unversioned specification is created") {
        const auto specification = MultipleVersionsOfTraitSpecification::create();

        THEN("unversioned specification is of the correct class") {
          STATIC_REQUIRE(std::is_same_v<std::decay_t<decltype(specification)>,
                                        MultipleVersionsOfTraitSpecification>);
        }
      }
    }
  }
}

TEST_CASE("Deprecated specification causes deprecation compiler warning") {
  using openassetio_traitgen_test_all::specifications::test::DeprecatedSpecification_v1;
  // Ensure that the deprecated specification does indeed cause a
  // deprecation warning if used. Note that to see this we must
  // remove the diagnostic suppression. See
  // openassetio-traitgentest-deprecations CTest target.
  const auto spec = DeprecatedSpecification_v1::create();
}

// NOLINTEND(bugprone-chained-comparison)
