import json
import time

import cv2
import airsim
import logging
from .helper import coordinates as c
from .UnityService import get_navmesh_path
import sys

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
client: airsim.MultirotorClient = None
_logger = None


def initialize():
    global client
    global _logger
    client = airsim.MultirotorClient()
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
    _logger.info("Moving to:"+str(x)+","+str(y)+","+str(z)+"in velocity:"+str(v))
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


def captureImage(foldername):
    logging.info("Capturing image...")
    filename = foldername + "captured_sim_image_" + time.strftime("%Y%m%d-%H%M%S") + ".png"
    image = client.simGetImage(str(0), airsim.ImageType.Scene)
    img_array = cv2.imdecode(airsim.string_to_uint8_array(image), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(filename, img_array)
