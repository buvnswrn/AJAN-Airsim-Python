from rdflib import URIRef, Namespace

pomdp_ns = Namespace("http://www.dfki.de/pomdp-ns#")
pomdp_ns1 = Namespace("http://www.dfki.de/pomdp-ns/POMDP/data/")
keypoint_ns = Namespace("http://www.dfki.de/pomdp-ns/POMDP/data/keypoint#")
POMDP = URIRef("http://www.dfki.de/pomdp-ns#POMDP")


_Observation = pomdp_ns["Observation"]

_Type = pomdp_ns["type"]
_CurrentObservation = pomdp_ns["CurrentObservation"]

_Pose = pomdp_ns1["pose"]
_Id = pomdp_ns1["id"]
_Keypoint = pomdp_ns1["keypoint"]
_Keypoints = pomdp_ns1["keypoints"]
_Pandas = pomdp_ns1["pandasDataFrame"]


def createIRI(namespace, _id):
    return URIRef(str(namespace).replace("#", "/") + "#" + str(_id))
