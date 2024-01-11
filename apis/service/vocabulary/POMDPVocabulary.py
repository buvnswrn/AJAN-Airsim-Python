from rdflib import URIRef, Namespace

pomdp_ns = Namespace("http://www.dfki.de/pomdp-ns#")
pomdp_ns1 = Namespace("http://www.dfki.de/pomdp-ns/POMDP/data/")
keypoint_ns = Namespace("http://www.dfki.de/pomdp-ns/POMDP/data/keypoint#")
POMDP = URIRef("http://www.dfki.de/pomdp-ns#POMDP")


_Observation = pomdp_ns["Observation"]

_Type = pomdp_ns["type"]
_CurrentObservation = pomdp_ns["CurrentObservation"]

_Id = pomdp_ns["id"]
_Name = pomdp_ns["name"]
_Attributes = pomdp_ns["attributes"]
_To_Print = pomdp_ns["to_print"]
_For_Hash = pomdp_ns["for_hash"]
_Planned_Action = pomdp_ns["plannedAction"]

# Datatypes
_Pandas = pomdp_ns1["pandasDataFrame"]
_2dVector = pomdp_ns1["2dVector"]
_3dVector = pomdp_ns1["3dVector"]

_Point = pomdp_ns1["Point"]


def createIRI(namespace, _id):
    return URIRef(str(namespace).replace("#", "/") + "_" + str(_id))
