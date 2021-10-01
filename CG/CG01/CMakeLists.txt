cmake_minimum_required(VERSION 3.16)
project(CG01 VERSION 0.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -Wall -fconcepts")

find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)
find_package(glm REQUIRED)

file(GLOB_RECURSE HEADERS src/include/*.hh)
file(GLOB_RECURSE SOURCES src/src/*.cc)

file(GLOB_RECURSE VENDOR_HEADERS src/vendor/include/*.h)
file(GLOB_RECURSE VENDOR_SOURCES src/vendor/src/*.cc src/vendor/src/*.c)

include_directories(src/vendor/include src/include)

add_executable(CG01_Triangle ${VENDOR_HEADERS} ${VENDOR_SOURCES} ${HEADERS} ${SOURCES} src/triangle.cc)
target_link_libraries(CG01_Triangle OpenGL::GL glfw -lX11 -ldl)

add_executable(CG01_Cube ${VENDOR_HEADERS} ${VENDOR_SOURCES} ${HEADERS} ${SOURCES} src/cube.cc)
target_link_libraries(CG01_Cube OpenGL::GL glfw -lX11 -ldl)
