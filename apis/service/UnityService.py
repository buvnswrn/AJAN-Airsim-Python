import requests
from constants.constants import NAVMESH_PATH_URL, REQUEST_TEMPLATE, headers


def get_navmesh_path(start_x: float, start_y: float, start_z: float, end_x: float, end_y: float, end_z: float):
    message = REQUEST_TEMPLATE.format(start_x=str(start_x), start_y=str(start_y),
                                                             start_z=str(start_z),
                                                             end_x=str(end_x), end_y=str(end_y), end_z=str(end_z))
    print(message)
    response = requests.request("POST", NAVMESH_PATH_URL, headers=headers,
                                data=message)
    print("Response:", response.text)
    return response.text


# def get_navmesh_path(data):
#     response = requests.request("POST", NAVMESH_PATH_URL, headers=headers,
#                                 data=data)
#     print("Response:", response.text)
#     return response.text
