import json

import airsim
import cv2

import numpy as np
import pandas as pd
import rdfpandas
from rdflib import RDF, BNode, Literal, XSD

from ultralytics import YOLO


import time

from scipy.spatial.transform import Rotation

from ..airsim_controller import client, initialize
from ..vocabulary.POMDPVocabulary import createIRI, _Point, _Attributes, _Observation, pomdp_ns, _Pandas, _Id, _Type

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
        rdfdf.index = [createIRI(_Point, str(i)) for i in range(len(rdfdf))]
        g = rdfpandas.to_graph(rdfdf)

        attributes_node = BNode()
        for_hash_node = BNode()
        g.add((_Observation, _Attributes, attributes_node))

        g.add((attributes_node, createIRI(pomdp_ns, "personId"), Literal(id, datatype=XSD.integer)))
        pose_node = BNode()
        g.add((attributes_node, createIRI(pomdp_ns, "pose"), pose_node))
        g.add((pose_node, RDF.type, _Pandas))
        g.add((_Id, _Type, XSD.integer))
        for i in range(len(rdfdf)):
            g.add((pose_node, RDF.value, createIRI(_Point, str(i))))
        return g.serialize(format=return_type)
    return json.dumps(returnValue)
