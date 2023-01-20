import json

import requests
from constants.constants import NAVMESH_PATH_URL, NAVMESH_REQUEST_TEMPLATE, headers, GET_OBJECTS_REQUEST_TEMPLATE, \
    OBJECTS_URL
from constants.object_mapping import object_name_for_symbolic_position
import logging
import sys
# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

cached_positions = {}
_logger = logging.getLogger(__name__)
def set_logger(logger):
    global _logger
    _logger = logger

def get_navmesh_path(start_x: float, start_y: float, start_z: float, end_x: float, end_y: float, end_z: float):
    message = NAVMESH_REQUEST_TEMPLATE.format(start_x=str(start_x), start_y=str(start_y),
                                              start_z=str(start_z),
                                              end_x=str(end_x), end_y=str(end_y), end_z=str(end_z))
    _logger.debug(message)
    response = requests.request("POST", NAVMESH_PATH_URL, headers=headers,
                                data=message)
    _logger.debug("Response: "+response.text.__str__())
    return response.text


def get_objects(name: str):
    message = GET_OBJECTS_REQUEST_TEMPLATE.format(name=name)
    _logger.debug(message.__str__())
    response = requests.request("POST", OBJECTS_URL, headers=headers, data=message)
    _logger.debug("Response: "+response.text.__str__())
    return response.text


def get_positions_for_symbolic_location(symbolic_location: str):
    object_name, id = symbolic_location.split("_")
    if object_name in cached_positions:
        if id in cached_positions[object_name]:
            return cached_positions
    name = get_object_name_from_symbolic_name(object_name)
    objects = json.loads(get_objects(name))
    object_position = {}
    for object in objects:
        _, id = object["name"].split("_")
        position = object["position"]
        object_position[id] = position
    cached_positions[object_name] = object_position
    return cached_positions

def get_position_for_symbolic_location(symbolic_location: str):
    object_name, id = symbolic_location.split("_")
    positions = get_positions_for_symbolic_location(symbolic_location)
    return positions[object_name][id]['x'], positions[object_name][id]['y'], positions[object_name][id]['z']
def get_object_name_from_symbolic_name(object_name):
    return object_name_for_symbolic_position[object_name]

# def get_navmesh_path(data):
#     response = requests.request("POST", NAVMESH_PATH_URL, headers=headers,
#                                 data=data)
#     print("Response:", response.text)
#     return response.text
