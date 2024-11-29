def generate_launch_description():
    # ... (previous code remains the same until spawn_entity)

    # Create a robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': Command([
                FindExecutable(name='xacro'), ' ',
                PathJoinSubstitution([pkg_share, 'urdf', 'ur10e_2fg7.urdf.xacro'])
            ])
        }]
    )

    # Spawn controllers after the gazebo_ros2_control plugin is loaded
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    load_gripper_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'gripper_controller'],
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        TimerAction(
            period=5.0,
            actions=[load_joint_state_controller]
        ),
        TimerAction(
            period=6.0,
            actions=[load_joint_trajectory_controller]
        ),
        TimerAction(
            period=7.0,
            actions=[load_gripper_controller]
        )
    ])
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Paths
    pkg_share = FindPackageShare("ur10e_2fg7_description").find("ur10e_2fg7_description")
    
    # Robot state publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": Command([
                FindExecutable(name="xacro"), " ",
                PathJoinSubstitution([pkg_share, "urdf", "ur10e_2fg7.urdf.xacro"])
            ])
        }]
    )

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([FindPackageShare("gazebo_ros"), "/launch", "/gazebo.launch.py"]),
    )

    # Spawn robot
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "robot_description", "-entity", "ur10e_2fg7"],
        output="screen"
    )

    # Load controllers
    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_joint_trajectory_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_trajectory_controller'],
        output='screen'
    )

    load_gripper_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'gripper_controller'],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        spawn_entity,
        TimerAction(
            period=5.0,
            actions=[load_joint_state_controller]
        ),
        TimerAction(
            period=6.0,
            actions=[load_joint_trajectory_controller]
        ),
        TimerAction(
            period=7.0,
            actions=[load_gripper_controller]
        )
    ])