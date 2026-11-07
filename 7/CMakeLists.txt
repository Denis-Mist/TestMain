cmake_minimum_required(VERSION 3.16)

project(calculator_gui_qtest LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Test)

add_library(calculator_gui STATIC
    mainwindow.cpp
    mainwindow.h
)

target_link_libraries(calculator_gui PUBLIC Qt6::Widgets)

add_executable(calculator_gui_tests
    tests/main.cpp
    tests/testcalculatorgui.cpp
    tests/testcalculatorgui.h
)

target_include_directories(calculator_gui_tests PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/tests
)

target_link_libraries(calculator_gui_tests PRIVATE
    calculator_gui
    Qt6::Test
    Qt6::Widgets
)

enable_testing()
add_test(NAME calculator_gui_unit COMMAND calculator_gui_tests)
