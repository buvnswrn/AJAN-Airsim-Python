import json

import airsim
import cv2

import numpy as np
import pandas as pd
import rdfpandas

from ultralytics import YOLO

import time

from scipy.spatial.transform import Rotation

from ..airsim_controller import client, initialize

model_path = 'models/yolov8n-pose.pt'
model: YOLO = YOLO(model_path)


def estimate_pose(camera_name="front_center", image_type=airsim.ImageType.Scene, return_type="json"):
    if client is None:
        initialize()
    image = client.simGetImage(camera_name, image_type)
    np_response_image = np.asarray(bytearray(image), dtype="uint8")
    decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
    results = model.track(decoded_frame, persist=True)
    returnValue = dict()
    returnValue['class'] = results[0].names
    returnValue['keypoints'] = results[0].keypoints.xy.numpy().tolist()
    print(results[0].names)
    print(results[0].keypoints.xy.data)
    annotated_frame = results[0].plot()
    cv2.imshow("Airsim Pose sensor", annotated_frame)
    if return_type == "turtle":
        rdfdf = pd.DataFrame(results[0].keypoints.xy.numpy().squeeze(), columns=['rdf:x', 'rdf:y'])
        rdfdf.index = ['keypoint:' + str(i) for i in range(len(rdfdf))]
        g = rdfpandas.to_graph(rdfdf)
        return g.serialize(format=return_type)
    return json.dumps(returnValue)
