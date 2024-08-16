# SPDX-License-Identifier: Apache-2.0
# Copyright 2013-2022 The Foundry Visionmongers Ltd

include(CompilerWarnings)

# Top level function to configure all the default target properties.
function(openassetio_traitgentest_set_default_target_properties target_name)
    #-------------------------------------------------------------------
    # C++ standard

    # Minimum C++ standard as per current VFX reference platform CY21+.
    target_compile_features(${target_name} PRIVATE cxx_std_17)

    set_target_properties(
        ${target_name}
        PROPERTIES
        # Ensure the proposed compiler supports our minimum C++
        # standard.
        CXX_STANDARD_REQUIRED ON
        # Disable compiler extensions. E.g. use -std=c++11  instead of
        # -std=gnu++11.  Helps limit cross-platform issues.
        CXX_EXTENSIONS OFF
    )

    #-------------------------------------------------------------------
    # Compiler warnings

    openassetio_traitgentest_set_default_compiler_warnings(${target_name})

    #-------------------------------------------------------------------
    # Symbol visibility

    # Hide symbols from this library by default.
    set_target_properties(
        ${target_name}
        PROPERTIES
        C_VISIBILITY_PRESET hidden
        CXX_VISIBILITY_PRESET hidden
        VISIBILITY_INLINES_HIDDEN YES
    )

    # Hide all symbols from external statically linked libraries.
    if (IS_GCC_OR_CLANG AND NOT APPLE)
        # TODO(TC): Find a way to hide symbols on macOS
        target_link_options(${target_name} PRIVATE "-Wl,--exclude-libs,ALL")
    endif ()

    #-------------------------------------------------------------------
    # Library version

    get_target_property(target_type ${target_name} TYPE)

    if (NOT ${target_type} STREQUAL EXECUTABLE)
        # When building or installing appropriate symlinks are created, if
        # supported.
        set_target_properties(
            ${target_name}
            PROPERTIES
            VERSION ${PROJECT_VERSION}
            SOVERSION ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
        )
    endif ()

    #-------------------------------------------------------------------
    # Sanitizers

    if (IS_GCC_OR_CLANG)
        if (OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_ADDRESS)
            list(APPEND sanitizers "address")
        endif ()

        if (OPENASSETIO_TRAITGENTEST_ENABLE_SANITIZER_UNDEFINED_BEHAVIOR)
            list(APPEND sanitizers "undefined")
        endif ()

        list(JOIN sanitizers "," sanitize_arg)

        if (sanitize_arg AND NOT "${sanitize_arg}" STREQUAL "")
            # Add sanitizers, including
            # * -fno-omit-frame-pointer to enable stack traces on
            #   failure.
            # * -fno-sanitize-recover=all to force the program to exit
            #   with an error code on failure.
            target_compile_options(${target_name}
                PRIVATE
                -fno-sanitize-recover=all
                -fsanitize=${sanitize_arg}
                -fno-omit-frame-pointer)
            target_link_options(${target_name}
                PRIVATE
                -fno-sanitize-recover=all
                -fsanitize=${sanitize_arg}
                -fno-omit-frame-pointer)
        endif ()
    endif ()

    #-------------------------------------------------------------------
    # Linters/analyzers

    if (TARGET openassetio-traitgentest-cpplint)
        add_dependencies(${target_name} openassetio-traitgentest-cpplint)
    endif ()

    if (TARGET openassetio-traitgentest-clangformat)
        add_dependencies(${target_name} openassetio-traitgentest-clangformat)
    endif ()

    if (TARGET openassetio-traitgentest-cmakelint)
        add_dependencies(${target_name} openassetio-traitgentest-cmakelint)
    endif ()
endfunction()
