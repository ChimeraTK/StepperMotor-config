PROJECT(ChimeraTK_StepperMotor-config NONE)
cmake_minimum_required(VERSION 3.5)

# Note: Always keep MAJOR_VERSION and MINOR_VERSION identical to the server version. Count only the patch separately.
set(${PROJECT_NAME}_MAJOR_VERSION 01)
set(${PROJECT_NAME}_MINOR_VERSION 00)
set(${PROJECT_NAME}_PATCH_VERSION 02)
include(cmake/set_version_numbers.cmake)

include(cmake/config_generator_project.cmake)
