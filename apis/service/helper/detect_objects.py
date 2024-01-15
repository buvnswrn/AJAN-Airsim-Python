import json

import airsim
import cv2
from ultralytics import YOLO

from apis.service.airsim_controller import get_sim_image

model_path = 'models/custom_object_detection.pt'
model: YOLO = YOLO(model_path)

# classNames = ["Box", "Shelf"]
classNames = {1: "Shelf", 4: "Box"}


def get_object_detection(decoded_frame, id, conf=0.2, return_type="json", write=False):
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
        object_name = classNames[class_id]+"_" + str(counter[class_id])
        returnValue[object_name] = {"location": object_location, "probability": confidence}
    print(returnValue)
    annotated_frame = results.plot()
    if write:
        cv2.imwrite("object_annotated_frame.jpg", annotated_frame)
    cv2.imshow("Object sensor", annotated_frame)
    return json.dumps(returnValue)


def detect_objects(id=0, camera_name="front_center", image_type=airsim.ImageType.Scene, conf=0.2, return_type="json", write=False):
    decoded_frame = get_sim_image(camera_name, image_type)
    return get_object_detection(decoded_frame, id, conf, return_type, write)


def draw_boxes():
    pass