import time

import cv2
import airsim
import logging
from .helper import coordinates as c

client: airsim.MultirotorClient = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)


def takeoff():
    logging.info("Taking off...")
    client.takeoffAsync().join()
    return True


def land():
    logging.info("Landing...")
    client.landAsync().join()
    return True


def hover():
    logging.info("Hovering...")
    client.hoverAsync().join()
    return True


def move(x, y, z, v):
    logging.info("Moving...")
    x, y, z = c.get_airsim_values(x, y, z)
    client.moveToPositionAsync(x, y, z, v).join()
    return True


def captureImage(foldername):
    logging.info("Capturing image...")
    filename = foldername + "captured_image" + time.strftime("%Y%m%d-%H%M%S") + ".png"
    image = client.simGetImage(str(0), airsim.ImageType.Scene).join()
    img_array = cv2.imdecode(airsim.string_to_uint8_array(image), cv2.IMREAD_UNCHANGED)
    cv2.imwrite(filename, img_array)
