cmake_minimum_required(VERSION 3.16)

project(temperature_sensor_qtest LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Test)

add_library(temperature_sensor STATIC
    temperaturesensor.cpp
    temperaturesensor.h
)

target_link_libraries(temperature_sensor PUBLIC Qt6::Core)

target_include_directories(temperature_sensor PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(temperature_sensor_tests
    tests/main.cpp
    tests/testtemperaturesensor.cpp
    tests/testtemperaturesensor.h
)

target_link_libraries(temperature_sensor_tests PRIVATE
    temperature_sensor
    Qt6::Test
)

enable_testing()
add_test(NAME temperature_sensor_unit COMMAND temperature_sensor_tests)
