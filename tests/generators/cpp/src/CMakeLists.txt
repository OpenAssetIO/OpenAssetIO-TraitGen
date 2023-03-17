#-----------------------------------------------------------------------
# Package dependencies

find_package(OpenAssetIO REQUIRED)
find_package(Catch2 REQUIRED)


#-----------------------------------------------------------------------
# Loop compile-time variants

foreach (include_type package subpackage namespace class)

    set(_target_name openassetio-traitgentest-${include_type})
    string(TOUPPER OPENASSETIO_TRAITGENTEST_INCLUDES_${include_type} _include_toggle)

    #-----------------------------------------------------------------------
    # Target executable

    add_executable(${_target_name})
    openassetio_traitgentest_set_default_target_properties(${_target_name})

    target_compile_definitions(${_target_name} PRIVATE ${_include_toggle})

    #-----------------------------------------------------------------------
    # Target dependencies

    target_sources(${_target_name} PRIVATE main.cpp test.cpp)
    target_link_libraries(
        ${_target_name}
        PRIVATE
        OpenAssetIO::openassetio-core
        Catch2::Catch2
    )
    target_include_directories(
        ${_target_name}
        PRIVATE
        ${OPENASSETIO_TRAITGENTEST_ADDITIONAL_INCLUDE_DIRS}
    )


    #-----------------------------------------------------------------------
    # CTest target

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
    endif()

endforeach ()
