cmake_minimum_required(VERSION 3.21)

project(
    TraitGenTest
    VERSION 1.0.0
)

enable_testing()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(IS_GCC_OR_CLANG TRUE)
else ()
    set(IS_GCC_OR_CLANG FALSE)
endif ()
if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND
    CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL 5.0)
    set(IS_GCC_GTEQ_5 TRUE)
else ()
    set(IS_GCC_GTEQ_5 FALSE)
endif ()

# Additional include directories for CMake utils.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)

#-----------------------------------------------------------------------
# Options

# Default treating compiler warnings as errors to OFF, since
# consumers of this project may use unpredictable toolchains.
# For dev/CI we should remember to switch this ON, though!
option(OPENASSETIO_TRAITGENTEST_WARNINGS_AS_ERRORS "Treat compiler warnings as errors" OFF)

# Enable clang-format formatting check.
option(OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_FORMAT "Enable clang-format check during build" OFF)

# Enable clang-tidy static analysis tool.
option(OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_TIDY "Enable clang-tidy analysis during build" OFF)

# Enable cpplint linter.
option(OPENASSETIO_TRAITGENTEST_ENABLE_CPPLINT "Enable cpplint linter during build" OFF)

# Enable cmake-lint linter.
option(OPENASSETIO_TRAITGENTEST_ENABLE_CMAKE_LINT "Enable cmake-lint linter during build" OFF)

if (IS_GCC_OR_CLANG)
    # Sanitizers (primarily for tests)
    option(OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
    option(OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_UNDEFINED_BEHAVIOR
        "Enable undefined behavior sanitizer" OFF)
endif ()

# Disable C++11 ABI by default, as per current VFX reference
# platform(s), but allow optionally enabling.
if (IS_GCC_GTEQ_5)
    option(OPENASSETIO_TRAITGENTEST_GLIBCXX_USE_CXX11_ABI
        "For gcc, use the new C++11 library ABI" OFF)
endif ()


#-----------------------------------------------------------------------
# Target linting and properties

include(StaticAnalyzers)
if (OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_FORMAT)
    enable_clang_format()
endif ()
if (OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_TIDY)
    enable_clang_tidy()
endif ()
if (OPENASSETIO_TRAITGENTEST_ENABLE_CPPLINT)
    enable_cpplint()
endif ()
if (OPENASSETIO_TRAITGENTEST_ENABLE_CMAKE_LINT)
    enable_cmake_lint()
endif ()

include(DefaultTargetProperties)


#-----------------------------------------------------------------------
# Targets

add_subdirectory(src)


#-----------------------------------------------------------------------
# Print a status dump
# cmake-lint: disable=C0301

message(STATUS "CMake package search path       = ${CMAKE_PREFIX_PATH}")
message(STATUS "Warnings as errors              = ${OPENASSETIO_TRAITGENTEST_WARNINGS_AS_ERRORS}")
message(STATUS "Linter: clang-tidy              = ${OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_TIDY} [${OPENASSETIO_TRAITGENTEST_CLANGTIDY_EXE}]")
message(STATUS "Linter: cpplint                 = ${OPENASSETIO_TRAITGENTEST_ENABLE_CPPLINT} [${OPENASSETIO_TRAITGENTEST_CPPLINT_EXE}]")
message(STATUS "Linter: clang-format            = ${OPENASSETIO_TRAITGENTEST_ENABLE_CLANG_FORMAT} [${OPENASSETIO_TRAITGENTEST_CLANGFORMAT_EXE}]")
message(STATUS "Linter: cmake-lint              = ${OPENASSETIO_TRAITGENTEST_ENABLE_CMAKE_LINT} [${OPENASSETIO_TRAITGENTEST_CMAKELINT_EXE}]")
if (IS_GCC_GTEQ_5)
    message(STATUS "New C++11 ABI for gcc           = ${OPENASSETIO_TRAITGENTEST_GLIBCXX_USE_CXX11_ABI}")
endif ()
if (IS_GCC_OR_CLANG)
    message(STATUS "Sanitizer: Address              = ${OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_ADDRESS}")
    message(STATUS "Sanitizer: Undefined behavior   = ${OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_UNDEFINED_BEHAVIOR}")
endif ()
