import json
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
        x, y, z = c.get_airsim_values(waypoint['x'], waypoint['y'], waypoint['z'])
        # x, y, z = c.get_airsim_values(x, y, z)
        client.moveToPositionAsync(x, y, z, v).join()
    return True


def move_one_step(direction):
    pos = client.simGetVehiclePose().position
    x = pos.x_val
    y = pos.y_val
    z = pos.z_val
    if direction == 'left':
        y -= 1
    if direction == 'right':
        y += 1
    x += 1
    client.moveToPositionAsync(x, y, z, 1).join()
    return True


def turn_one_step(direction):
    if direction == 'left':
        client.rotateToYawAsync(-90).join()
    if direction == 'right':
        client.rotateToYawAsync(90).join()
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
