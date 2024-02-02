import json

import airsim
import cv2
from rdflib import BNode, Graph, Literal, RDF
from ultralytics import YOLO

from apis.service.airsim_controller import get_sim_image
from ..vocabulary.POMDPVocabulary import createIRI, _Point, _Attributes, _Observation, pomdp_ns, _Pandas, _Id, _Type, \
    _For_Hash, _4dVector, _Probability, _rdf, _Vector
from ..vocabulary.UnityVocabulary import unity_ns

model_path = 'models/custom_object_detection.pt'
model: YOLO = YOLO(model_path)

# classNames = ["Box", "Shelf"]
classNames = {1: "Shelf", 4: "Box"}


def get_object_detection(decoded_frame, id, conf=0.3, return_type="json", write=False):
    # results = model.predict(decoded_frame, conf=0.5, classes=classNames)[0]
    results = model.track(decoded_frame, conf=conf, classes=list(classNames.keys()), persist=True)[0]
    returnValue = dict()
    counter = {4: 0, 1: 0}
    for i in range(len(results.boxes.cls)):
        class_id = results.boxes.cls[i].tolist()
        object_location = results.boxes.xywh[0].tolist()
        confidence = results.boxes.conf[i].tolist()
        if class_id in counter:
            counter[class_id] += 1
        else:
            counter[class_id] = 1
        object_name = classNames[class_id] + "_" + str(counter[class_id])
        returnValue[object_name] = {"location": object_location, "probability": confidence}
    print(returnValue)
    annotated_frame = results.plot()
    if write:
        cv2.imwrite("object_annotated_frame.jpg", annotated_frame)
        cv2.imwrite("object_frame.jpg", decoded_frame)
    cv2.imshow("Object sensor", annotated_frame)
    if return_type == "turtle":
        g = Graph()
        attributes_node = BNode()
        for_hash_node = BNode()
        g.add((_Observation, _Attributes, attributes_node))
        g.add((_Observation, _For_Hash, for_hash_node))
        g.add((for_hash_node, RDF.value, Literal("object_id")))
        g.add((for_hash_node, RDF.value, Literal("objects")))

        g.add((attributes_node, createIRI(pomdp_ns, "object_id"), Literal(id)))
        objects_node = createIRI(pomdp_ns, "objects")
        objects_value_node = BNode()
        g.add((attributes_node, objects_node, objects_value_node))
        g.add((objects_value_node, RDF.type, _Vector))
        for object_name in returnValue.keys():
            object_relation_node = unity_ns[object_name]

            g.add((objects_value_node, RDF.value, object_relation_node))

            object_node = BNode(object_name)
            g.add((attributes_node, object_relation_node, object_node))  # TODO: check if deleted in pomdp_py.
            object_location = returnValue[object_name]["location"]

            g.add((object_node, RDF.type, _4dVector))
            g.add((object_node, _rdf.x, Literal(object_location[0])))
            g.add((object_node, _rdf.y, Literal(object_location[1])))
            g.add((object_node, _rdf.w, Literal(object_location[2])))
            g.add((object_node, _rdf.h, Literal(object_location[3])))

            object_probability = returnValue[object_name]["probability"]
            probability_node = createIRI(unity_ns, object_name + "_" + "probability")  # Check if this can be accessed.
            g.add((attributes_node, probability_node, Literal(object_probability)))
        return g.serialize(format=return_type)
    return json.dumps(returnValue)


def detect_objects(id=0, camera_name="front_center", image_type=airsim.ImageType.Scene, conf=0.3, return_type="json",
                   write=False):
    decoded_frame = get_sim_image(camera_name, image_type)
    return get_object_detection(decoded_frame, id, conf, return_type, write)


def draw_boxes():
    pass
