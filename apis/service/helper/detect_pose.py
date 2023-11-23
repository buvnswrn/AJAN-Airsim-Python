import json

import airsim
import cv2

import numpy as np
import pandas as pd
import rdfpandas
from rdflib import RDF, BNode, Literal, XSD

from ultralytics import YOLO
from ..vocabulary.POMDPVocabulary import _Pose, _Type, _Pandas, _Keypoint, createIRI, keypoint_ns, _Keypoints, \
    _CurrentObservation, _Id

import time

from scipy.spatial.transform import Rotation

from ..airsim_controller import client, initialize

model_path = 'models/yolov8n-pose.pt'
model: YOLO = YOLO(model_path)


def estimate_pose(id=0, camera_name="front_center", image_type=airsim.ImageType.Scene, return_type="json"):
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
        rdfdf.index = [ keypoint_ns[str(i)] for i in range(len(rdfdf))]
        g = rdfpandas.to_graph(rdfdf)
        g.add((_CurrentObservation, RDF.value, _Id))
        g.add((_Id, RDF.value, Literal(id, datatype=XSD.integer)))
        g.add((_Id, _Type, XSD.integer))
        g.add((_CurrentObservation, RDF.value, _Pose))
        g.add((_Pose, _Type, _Pandas))
        keypoint_node = BNode("poseDataFrame")
        g.add((_Pose, RDF.value, _Keypoints))
        for i in range(len(rdfdf)):
            g.add((_Keypoints, RDF.value, keypoint_ns[str(i)]))
        return g.serialize(format=return_type)
    return json.dumps(returnValue)
