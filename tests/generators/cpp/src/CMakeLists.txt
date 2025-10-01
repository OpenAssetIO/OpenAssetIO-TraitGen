#-----------------------------------------------------------------------
# Package dependencies

find_package(OpenAssetIO REQUIRED)
find_package(Catch2 REQUIRED)

#-----------------------------------------------------------------------
# CMake/CTest target utilities.

##
# Helper function to create a test's build target for a given include
# type.
#
# The include type determines which style of includes are used in the
# test, i.e. what level of hoisting headers - package level, namespace
# level, or class level.
function(_create_build_target target_name include_type)
    string(TOUPPER OPENASSETIO_TRAITGENTEST_INCLUDES_${include_type} _include_toggle)

    #-------------------------------------------------------------------
    # Target executable

    add_executable(${target_name})
    openassetio_traitgentest_set_default_target_properties(${target_name})

    target_compile_definitions(${target_name} PRIVATE ${_include_toggle})

    #-------------------------------------------------------------------
    # Target dependencies

    target_sources(${target_name} PRIVATE main.cpp test.cpp)
    target_link_libraries(
        ${target_name}
        PRIVATE
        OpenAssetIO::openassetio-core
        Catch2::Catch2
    )
    target_include_directories(
        ${target_name}
        # Must make SYSTEM since e.g. DeprecatedSpecification inheriting
        # from DeprecatedSpecification_v1 triggers deprecation warnings
        # even if unused.
        SYSTEM PRIVATE
        ${OPENASSETIO_TRAITGENTEST_ADDITIONAL_INCLUDE_DIRS}
    )
endfunction()

#-----------------------------------------------------------------------
# Test each #include style variant.

foreach (include_type package subpackage namespace class)
    set(_target_name openassetio-traitgentest-${include_type})
    _create_build_target(${_target_name} ${include_type})
    add_test(NAME ${_target_name} COMMAND $<TARGET_FILE:${_target_name}>)
    if (MSVC)
        # If OpenAssetIO was built as a shared library, then Windows
        # needs the library on PATH.
        set_tests_properties(
            ${_target_name}
            PROPERTIES
            ENVIRONMENT
            PATH=$<TARGET_FILE_DIR:OpenAssetIO::openassetio-core>
        )
    endif ()
    # Allow [[deprecated]] - these will be tested in their own target.
    target_compile_options(${_target_name} PRIVATE -Wno-deprecated-declarations)
endforeach ()

#-----------------------------------------------------------------------
# Test deprecation warnings.

set(_target_name openassetio-traitgentest-deprecations)
_create_build_target(${_target_name} package)
# Don't build this target by default - it's only useful to check that
# deprecation warnings are correctly issued, and will fail the build
# otherwise.
set_target_properties(${_target_name} PROPERTIES EXCLUDE_FROM_ALL TRUE)

# Construct the error messages we expect to see, in order. Escape every
# character to make it a raw string match.
string(REGEX REPLACE "(.)" "\\\\\\1" _pass_regex
    "Unversioned trait view classes are deprecated, please use MultipleVersionsTrait_v1"
    " explicitly.")
list(APPEND _pass_regexps "${_pass_regex}")
string(REGEX REPLACE "(.)" "\\\\\\1" _pass_regex
    "The 'openassetio-traitgen-test-all:aNamespace.Deprecated' trait"
    " is deprecated.")
list(APPEND _pass_regexps "${_pass_regex}")
string(REGEX REPLACE "(.)" "\\\\\\1" _pass_regex
    "Unversioned specification view classes are deprecated, please use"
    " MultipleVersionsOfTraitSpecification_v1 explicitly.")
list(APPEND _pass_regexps "${_pass_regex}")
string(REGEX REPLACE "(.)" "\\\\\\1" _pass_regex
    "The 'test.Deprecated' specification of the 'openassetio_traitgen_test_all' package is"
    " deprecated.")
list(APPEND _pass_regexps "${_pass_regex}")
# Join into a single regex that matches all error messages in order.
list(JOIN _pass_regexps ".*" _pass_regexps)

# Building the target _is_ the test.
add_test(
    NAME ${_target_name}
    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target ${_target_name}
)
# Add expected failure regex for deprecation warnings.
set_tests_properties(${_target_name} PROPERTIES PASS_REGULAR_EXPRESSION "${_pass_regexps}")
