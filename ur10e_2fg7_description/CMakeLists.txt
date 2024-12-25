cmake_minimum_required(VERSION 3.8)
project(ur10e_2fg7_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(ur_description REQUIRED)
find_package(gazebo_ros2_control REQUIRED)
find_package(xacro REQUIRED)
find_package(onrobot_2fg7 REQUIRED)

# Install directories
install(
  DIRECTORY config launch urdf worlds resource
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
