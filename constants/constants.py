import logging

## FLASK_CONFIG

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5002

## Airsim
CAPTURE_FOLDER = "./imgs/"
IMAGE_EXT = ".png"
## Unity Service
URL = "http://localhost:8099/"
NAVMESH_PATH_URL = URL + "navmeshpath/"
OBJECTS_URL = URL + "getObjects/"
VISIBLE_OBJECTS_URL = URL + "getvisibleobjects/"
NAVMESH_REQUEST_TEMPLATE = "{{'start_position': {{'x':{start_x},'y':{start_y},'z':{start_z}}},'end_position': {{'x':{end_x},'y':{end_y},'z':{end_z}}}}}"
GET_OBJECTS_REQUEST_TEMPLATE = "{{'objectOfInterest':'{name}'}}"
headers = {'Content-Type': 'application/json'}


LOG_LEVEL = logging.DEBUG

# AJAN
RDF_FORMAT = "turtle"
