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

target_sources(openassetio-traitgentest PRIVATE main.cpp)
target_link_libraries(
    openassetio-traitgentest
    PRIVATE
    OpenAssetIO::openassetio-core
    Catch2::Catch2
)


#-----------------------------------------------------------------------
# CTest target

add_test(openassetio-traitgentest openassetio-traitgentest)
