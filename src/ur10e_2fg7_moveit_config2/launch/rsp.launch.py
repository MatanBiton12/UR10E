from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_rsp_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("ur10e_2fg7", package_name="ur10e_2fg7_moveit_config2").to_moveit_configs()
    return generate_rsp_launch(moveit_config)
