from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Declare arguments
    declared_arguments = []
    
    # Get package share directory
    pkg_share = FindPackageShare("ur10e_2fg7_description").find("ur10e_2fg7_description")
    world_file = os.path.join(pkg_share, "worlds", "gazebo_world.world")
    
    # Initialize Arguments
    robot_description_content = Command(
        [
            FindExecutable(name="xacro"), " ",
            PathJoinSubstitution(
                [FindPackageShare("ur10e_2fg7_description"), "urdf", "ur10e_2fg7.urdf.xacro"]
            ),
            " ",
            "name:=ur",
            " ",
            "ur_type:=ur10e"
        ]
    )
    
    robot_description = {"robot_description": robot_description_content}
    
    # Launch Gazebo with your world file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare("gazebo_ros"),
                "launch",
                "gazebo.launch.py"
            ])
        ]),
        launch_arguments={
            'world': world_file,
            'verbose': 'true'
        }.items()
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "ur10e_2fg7",
            "-z", "0.1"  # Small offset to prevent ground intersection
        ],
        output="screen",
    )
    
    # Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description],
    )
    
    # Joint State Publisher GUI
    joint_state_publisher_gui = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
        name="joint_state_publisher_gui",
    )
    
    # RVIZ Configuration
    rviz_config_file = PathJoinSubstitution(
        [FindPackageShare("ur10e_2fg7_description"), "config", "view_robot.rviz"]
    )
    
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )
    
    nodes_to_start = [
        gazebo,
        robot_state_publisher,
        spawn_entity,
        joint_state_publisher_gui,
        rviz_node,
    ]
    
    return LaunchDescription(declared_arguments + nodes_to_start)
