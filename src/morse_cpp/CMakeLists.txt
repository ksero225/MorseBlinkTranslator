cmake_minimum_required(VERSION 3.8)
project(morse_cpp)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(morse_interfaces REQUIRED)

add_executable(morse_encoder_service_node src/morse_encoder_service_node.cpp)
ament_target_dependencies(morse_encoder_service_node
  rclcpp
  std_msgs
  morse_interfaces
)

add_executable(morse_client_node src/morse_client_node.cpp)
ament_target_dependencies(morse_client_node
  rclcpp
  morse_interfaces
)

install(TARGETS
  morse_encoder_service_node
  morse_client_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()