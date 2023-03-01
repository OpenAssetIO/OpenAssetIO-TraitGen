// SPDX-License-Identifier: Apache-2.0
// Copyright 2022 The Foundry Visionmongers Ltd
#include <catch2/catch.hpp>

#if defined OPENASSETIO_TRAITGENTEST_INCLUDES_PACKAGE
#include <openassetio_traitgen_test_all/openassetio_traitgen_test_all.hpp>
#elif defined OPENASSETIO_TRAITGENTEST_INCLUDES_SUBPACKAGE
#include <openassetio_traitgen_test_all/specifications/specifications.hpp>
#include <openassetio_traitgen_test_all/traits/traits.hpp>
#elif defined OPENASSETIO_TRAITGENTEST_INCLUDES_NAMESPACE
#include <openassetio_traitgen_test_all/specifications/test.hpp>
#include <openassetio_traitgen_test_all/traits/aNamespace.hpp>
#include <openassetio_traitgen_test_all/traits/anotherNamespace.hpp>
#else
#error "An #include style must be chosen"
#endif
