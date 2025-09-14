import json

import airsim
import cv2
import pandas as pd
import rdfpandas
from rdflib import RDF, BNode, Literal, XSD
from ultralytics import YOLO

from ..airsim_controller import get_sim_image
from ..vocabulary.POMDPVocabulary import createIRI, _Point, _Attributes, _Observation, pomdp_ns, _Pandas, _Id, _Type, \
    _For_Hash

model_path = 'models/yolov8n-pose.pt'
model: YOLO = YOLO(model_path)


def estimate_pose(id=0, camera_name="front_center", image_type=airsim.ImageType.Scene, return_type="json", write=False):
    decoded_frame = get_sim_image(camera_name, image_type)
    return get_pose_estimation(decoded_frame, id, return_type, write)


def get_pose_estimation(decoded_frame, id, return_type="json", write=False):
    results = model.track(decoded_frame, persist=True)
    returnValue = dict()
    confidence = results[0].boxes.conf[0].tolist() if len(results[0].boxes.conf) > 0 else 0
    returnValue['class'] = results[0].names
    if confidence > 0.5:
        returnValue['keypoints'] = results[0].keypoints.xy.numpy().tolist()
    else:
        returnValue['keypoints'] = []
    print(results[0].names)
    print(results[0].keypoints.xy.data)
    annotated_frame = results[0].plot()
    if write:
        cv2.imwrite("pose_annotated_frame.jpg", annotated_frame)
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

        if(len(rdfdf)>0):
            pose_node = BNode()
            g.add((pose_node, RDF.type, _Pandas))
            for i in range(len(rdfdf)):
                g.add((pose_node, RDF.value, createIRI(_Point, str(i))))
        else:
            pose_node = RDF.nil
        g.add((_Id, _Type, XSD.integer))
        g.add((attributes_node, createIRI(pomdp_ns, "pose"), pose_node))
        return g.serialize(format=return_type)
    return json.dumps(returnValue)



