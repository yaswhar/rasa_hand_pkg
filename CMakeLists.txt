cmake_minimum_required(VERSION 3.8)
project(rasa_hand_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate the service
# rosidl_generate_interfaces(${PROJECT_NAME}
#   "srv/SetServo.srv"
# )

include_directories(include ${rclcpp_INCLUDE_DIRS})
link_directories(${rclcpp_LIBRARY_DIRS})

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
install(PROGRAMS
  scripts/servo_tester_node.py
  DESTINATION lib/${PROJECT_NAME}
)

include_directories(include ${rclcpp_INCLUDE_DIRS})
link_directories(${rclcpp_LIBRARY_DIRS})

add_executable(cpp_executable src/cpp_node.cpp)
ament_target_dependencies(cpp_executable rclcpp)
# rosidl_target_interfaces(cpp_executable ${PROJECT_NAME} "rosidl_typesupport_cpp")

install(
  TARGETS
  cpp_executable
  DESTINATION lib/${PROJECT_NAME}
)

# Add a c++ library
add_library(${PROJECT_NAME} src/cpp_node.cpp)
target_link_libraries(${PROJECT_NAME} ${rclcpp_LIBRARIES})

# Install C++ headers
install(
  DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
  FILES_MATCHING PATTERN "*.hpp")

# Install launch files
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()