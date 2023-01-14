## FLASK_CONFIG

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5002

## Airsim
CAPTURE_FOLDER = "."

## Unity Service
NAVMESH_PATH_URL = "http://localhost:8099/navmeshpath/"
REQUEST_TEMPLATE = "{{'start_position': {{'x':{start_x},'y':{start_y},'z':{start_z}}},'end_position': {{'x':{end_x},'y':{end_y},'z':{end_z}}}}}"
headers = {'Content-Type': 'application/json'}
