#-----------------------------------------------------------------------
# Package dependencies

find_package(OpenAssetIO REQUIRED)
find_package(Catch2 REQUIRED)


#-----------------------------------------------------------------------
# Target executable

add_executable(openassetio-traitgentest)
openassetio_traitgentest_set_default_target_properties(openassetio-traitgentest)


#-----------------------------------------------------------------------
# Target dependencies

target_sources(openassetio-traitgentest PRIVATE main.cpp test.cpp)
target_link_libraries(
    openassetio-traitgentest
    PRIVATE
    OpenAssetIO::openassetio-core
    Catch2::Catch2
)
target_include_directories(
    openassetio-traitgentest
    PRIVATE
    ${OPENASSETIO_TRAITGENTEST_ADDITIONAL_INCLUDE_DIRS}
)


#-----------------------------------------------------------------------
# CTest target

add_test(openassetio-traitgentest openassetio-traitgentest)
