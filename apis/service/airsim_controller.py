import json
import math
import time

import cv2
import airsim
import logging

import numpy as np

from .helper import coordinates as c
from .UnityService import get_navmesh_path
from Configuration import global_config
import sys

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
client: airsim.MultirotorClient = None
_logger = None
airsim_config = global_config['AIRSIM']


def initialize():
    global client
    global _logger
    print("Initializing Airsim Controller at:" + airsim_config['ip'] + ":" + airsim_config['port'])
    client = airsim.MultirotorClient(ip=airsim_config['ip'], port=airsim_config.getint('port'))
    # client = airsim.MultirotorClient()

    client.confirmConnection()
    client.enableApiControl(True)
    _logger = logging.getLogger(__name__)


def set_logger(logger):
    global _logger
    _logger = logger


def takeoff():
    _logger.info("Taking off...")
    client.takeoffAsync().join()
    return True


def land():
    _logger.info("Landing...")
    client.landAsync().join()
    return True


def hover():
    _logger.info("Hovering...")
    client.hoverAsync().join()
    return True


def turn_toward_object(x, y, z, curr_x, curr_y, curr_z):
    dx = x - curr_x
    dy = y - curr_y
    # angle = math.atan2(dy, dx) * 180 / math.pi
    angle = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle)
    # angle_degrees = (angle_degrees + 180) % 360 - 180
    client.rotateToYawAsync(angle_degrees).join()


def move(x, y, z, v):
    _logger.info("Moving to:" + str(x) + "," + str(y) + "," + str(z) + "in velocity:" + str(v))
    current_position = client.simGetVehiclePose().position
    curr_x, curr_y, curr_z = c.get_unity_values(current_position.x_val, current_position.y_val, current_position.z_val)
    navmesh_response = get_navmesh_path(curr_x, curr_y, curr_z, x, y, z)
    waypoints = json.loads(navmesh_response)
    if len(waypoints) == 0:
        waypoints = get_navmesh_path(curr_x + 10, curr_y, curr_z, x, y, z)
        if len(waypoints) == 0:
            waypoints = get_navmesh_path(curr_x - 10, curr_y, curr_z, x, y, z)
            if len(waypoints) == 0:
                waypoints = get_navmesh_path(curr_x, curr_y, curr_z + 10, x, y, z)
                if len(waypoints) == 0:
                    waypoints = get_navmesh_path(curr_x, curr_y, curr_z + 10, x, y, z)
                    if len(waypoints) == 0:
                        raise Exception(
                            "No path found: from" + str(curr_x) + "," + str(curr_y) + "," + str(curr_z) + " to " + str(
                                x) + "," + str(y) + "," + str(z))
    for waypoint in waypoints[1:]:
        x, y, z = c.get_airsim_values(waypoint['x'], curr_y, waypoint['z'])
        # x, y, z = c.get_airsim_values(x, y, z)
        client.moveToPositionAsync(x, y, z, v).join()
    client.moveToPositionAsync(x, y - 1, z, v).join()
    turn_toward_object(x, y, z, curr_x, curr_y, curr_z)
    return True


def move_one_step(direction):
    print("Moving " + direction)
    pos = client.simGetVehiclePose().position
    x = pos.x_val
    y = pos.y_val
    z = pos.z_val
    if direction == 'left':
        y -= 1
    if direction == 'right':
        y += 1
    if direction == 'forward':
        x += 1
    if direction == 'backward':
        x -= 1
    if direction == 'up':
        z -= 1
    if direction == 'down':
        z += 1
    if -4.1 < z < -0.612:
        move_safer(direction, x, y, z)
    else:
        z = max(-4.1, min(z, -0.612))  # -4.1 is the max y value and -0.612 is the min y value allowed
        # z = max(0.612, min(z, 4.1))  # 4.1 is the max y value and 0.612 is the min y value allowed
        move_safer(direction, x, y, z)
    return True


def move_safer(direction, x, y, z):
    """
    Eradicated the issue of drone stuck in the down action due to Airsim's bug
    :param direction: which direction to move. Only for down action the bug is eradicated
    :param x: the x coordinate
    :param y: the y coordinate
    :param z: the z coordinate
    :return: None
    """
    if direction != "down":
        client.moveToPositionAsync(x, y, z, 1).join()
    else:
        client.moveToPositionAsync(x, y, z, 1)
        time.sleep(2)


def check_if_end_position_reached(x, y, z):
    """
    Check if the end position is reached
    :param x:
    :param y:
    :param z:
    :return:
    """
    end_pos = client.simGetVehiclePose().position
    diff_x = end_pos.x_val - x
    diff_y = end_pos.y_val - y
    diff_z = end_pos.z_val - z
    if diff_x <= 0.2 and diff_y <= 0.2 and diff_z <= 0.2:
        return True
    else:
        client.moveToPositionAsync(x + diff_x if diff_x > 0.2 else x,
                                   y + diff_y if diff_y > 0.2 else y,
                                   z + diff_z if diff_z > 0.2 else z, 1).join()
        check_if_end_position_reached(x, y, z)


def turn_one_step(direction):
    print("Turning " + direction)
    if direction == 'left':
        client.rotateToYawAsync(90).join()
    if direction == 'right':
        client.rotateToYawAsync(-90).join()
    return True


def get_current_position():
    pos = client.simGetVehiclePose().position
    return {"x": pos.x_val, "y": pos.y_val, "z": pos.z_val}


def captureImage(foldername):
    logging.info("Capturing image...")
    filename = foldername + "captured_sim_image_" + time.strftime("%Y%m%d-%H%M%S") + ".png"
    image = client.simGetImage(str(0), airsim.ImageType.Scene)
    img_array = cv2.imdecode(airsim.string_to_uint8_array(image), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(filename, img_array)


def get_sim_image(camera_name, image_type):
    if client is None:
        initialize()
    image = client.simGetImage(camera_name, image_type)
    np_response_image = np.asarray(bytearray(image), dtype="uint8")
    decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
    return decoded_frame
