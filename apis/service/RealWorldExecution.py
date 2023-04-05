import logging
import os.path
import time

import numpy
import requests
from PIL import Image
from io import BytesIO
import cv2

import constants.constants
from apis.service.helper.navigation import Navigation
from constants import MissionState
from constants.mavic2_api_constants import MQTT

__navigation = None
__current_state = MissionState.NOT_INITIALIZED
__logger = logging.getLogger(__name__)

known_position = {"position": "Drone-Home"}

def set_logger(logger):
    global __logger
    __logger = logger

def get_navigation():
    global __navigation
    if __navigation is None:
        __navigation = Navigation()
    return __navigation


navigation = get_navigation()


def bound(low, high, value):
    return max(low, min(high, value))


def get_position(x: float, y: float, z: float = 2.3, rot: float = 0, pitch: float = -90):
    return {
        "pos": {
            "x": bound(0, 2.3, x),
            "y": bound(0, 5.5, y),
            "z": z if z >= 0 else 0
        },
        "rot": bound(-180, 180, rot),
        "pitch": bound(-90, 30, pitch)
    }


def takeoff():
    __logger.info("Taking off...")
    navigation.publish(MQTT.PUBLISH_CHANNELS.TAKE_OFF_AND_HAND_OVER_CONTROL)
    take_off_message = navigation.subscribe(MQTT.SUBSCRIBE_CHANNELS.TAKE_OFF_AND_HANDOVER_CONTROL)
    check(navigation, MQTT.PHYSICAL.HOVERING)
    if take_off_message["status"] == "Accepted":
        return True


def land():
    navigation.publish(MQTT.PUBLISH_CHANNELS.emergencyLanding)
    land_message = navigation.subscribe(MQTT.SUBSCRIBE_CHANNELS.emergencyLanding)
    check(navigation,MQTT.PHYSICAL.HOVERING)
    check(navigation, MQTT.PHYSICAL.ONGROUND)
    print(land_message)
    if land_message["status"] == "Accepted":
        return True


def move(x, y, z):
    location = get_position(x, y, z)
    navigation.publish(MQTT.PUBLISH_CHANNELS.MOVE_TO_POINT, location)
    move_message = navigation.subscribe(MQTT.SUBSCRIBE_CHANNELS.MOVE_TO_POINT)
    if move_message["status"] == "Accepted" and check(navigation, "HOVERING"):
        # TODO: Check whether check_hovering works
        return True


def capture_image(capture_folder):
    check_exists_or_create(capture_folder)
    __logger.info("Capturing image...")
    filename = capture_folder + "captured_world_image_" + time.strftime("%Y%m%d-%H%M%S") + constants.constants.IMAGE_EXT
    try:
        response = requests.get(MQTT.LIVE_IMAGE_URL)
        img = numpy.array(Image.open(BytesIO(response.content)).convert('RGB'))[:, :, ::-1].copy()
        cv2.imwrite(filename, img)
    except:
        __logger.debug("Cannot save Image")


# region Helper Functions
def check_exists_or_create(folder):
    if os.path.exists(folder):
        return
    os.makedirs(folder)


def check(navigation, physical_state):
    message_01 = navigation.subscribe(
        MQTT.SUBSCRIBE_CHANNELS.PHYSICAL)  # Monitor drone state using Physical Endpoint
    while message_01["status"] != physical_state:  # Check for HOVERING status which indicates the command completion
            __logger.debug("In state:{0}".format(message_01["status"]))
            message_01 = navigation.subscribe(MQTT.SUBSCRIBE_CHANNELS.PHYSICAL)
# endregion
