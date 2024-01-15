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
from ..vocabulary.POMDPVocabulary import createIRI, _Point, _Attributes, _Observation, pomdp_ns, _Pandas, _Id, _Type, \
    _For_Hash

model_path = 'models/yolov8n-pose.pt'
model: YOLO = YOLO(model_path)


def estimate_pose(id=0, camera_name="front_center", image_type=airsim.ImageType.Scene, return_type="json"):
    decoded_frame = get_sim_image(camera_name, image_type)
    return get_pose_estimation(decoded_frame, id, return_type)


def get_pose_estimation(decoded_frame, id, return_type="json"):
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
        g.add((_Observation, _For_Hash, for_hash_node))
        g.add((for_hash_node, RDF.value, Literal("person_id")))
        g.add((for_hash_node, RDF.value, Literal("pose")))

        g.add((attributes_node, createIRI(pomdp_ns, "person_id"), Literal(id, datatype=XSD.integer)))
        pose_node = BNode()
        g.add((attributes_node, createIRI(pomdp_ns, "pose"), pose_node))
        g.add((pose_node, RDF.type, _Pandas))
        g.add((_Id, _Type, XSD.integer))
        for i in range(len(rdfdf)):
            g.add((pose_node, RDF.value, createIRI(_Point, str(i))))
        return g.serialize(format=return_type)
    return json.dumps(returnValue)


def get_sim_image(camera_name, image_type):
    if client is None:
        initialize()
    image = client.simGetImage(camera_name, image_type)
    np_response_image = np.asarray(bytearray(image), dtype="uint8")
    decoded_frame = cv2.imdecode(np_response_image, cv2.IMREAD_COLOR)
    return decoded_frame
