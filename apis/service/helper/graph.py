import json
import sys
from rdflib import Graph, URIRef, BNode, Literal
from rdflib.namespace import RDF, XSD
import time
import uuid
import random
from . import globals as g

def uuidGen():
    return time.time_ns().__str__() + str(random.randint(0, 99999))


def createGraph(label, rootUri):
    graph = Graph()
    sequenceNode = URIRef(g.sequenceBaseUri + uuidGen())
    rootNode = URIRef(g.btBaseUri + uuidGen()) if rootUri == "" else URIRef(rootUri)
    sbtLabel = Literal('NLP_BT (' + time.strftime("%H:%M", time.localtime()) + ')',
                       datatype=XSD.string) if label == "" else Literal(label)

    graph.add((rootNode, URIRef(g.typeUri), URIRef(g.btUri)))
    graph.add((rootNode, URIRef(g.typeUri), URIRef(g.rootUri)))
    graph.add((rootNode, URIRef(g.commentUri), Literal('comment about root node', datatype=XSD.string)))
    graph.add((rootNode, URIRef(g.labelUri), sbtLabel))
    graph.add((rootNode, URIRef(g.hasChildUri), sequenceNode))
    graph.add((sequenceNode, URIRef(g.typeUri), URIRef(g.sequenceUri)))
    graph.add((sequenceNode, URIRef(g.labelUri), Literal('label about the sequence node ', datatype=XSD.string)))
    graph.add((sequenceNode, URIRef(g.hasChildrenUri), g.RDF.nil))

    return graph, sequenceNode


def GenerateSparqlQuery(actionDic):
    query = g.templates[actionDic]['query']
    print(query)
    return query


def addSeqChild(graph, seq, ins, event, query):
    currentS = seq
    currentP = URIRef(g.hasChildrenUri)
    while graph.value(subject=currentS, predicate=currentP) != g.RDF.nil:
        currentS = graph.value(subject=currentS, predicate=currentP)
        currentP = g.RDF.rest

    print(currentS)

    blankNode = BNode("genid-" + uuid.uuid1().hex)
    graph.remove((currentS, currentP, g.RDF.nil))
    graph.add((currentS, currentP, blankNode))
    graph.add((blankNode, g.RDF.rest, g.RDF.nil))
    # newBlankNode = URIRef("_blank:"+timestamp())
    # contentBlankNode = URIRef("_content:"+timestamp())

    goalProducer = URIRef(g.goalProducerBaseUri + uuidGen())
    contentBlankNode = BNode("genid-" + uuid.uuid1().hex)
    graph.add((blankNode, g.RDF.first, goalProducer))
    graph.add((goalProducer, URIRef(g.typeUri), URIRef(g.goalProducerUri)))
    graph.add((goalProducer, URIRef(g.labelUri), Literal(ins, datatype=XSD.string)))
    graph.add((goalProducer, URIRef(g.commentUri), Literal('comment for goalproducer', datatype=XSD.string)))
    graph.add((goalProducer, URIRef(g.goalUri), URIRef(g.droneGoals[event])))  # here you give the action URI
    # graph.add((goalProducer, URIRef(g.goalUri), URIRef("actionURI")))
    graph.add((goalProducer, URIRef(g.contentUri), contentBlankNode))
    graph.add((contentBlankNode, URIRef(g.typeUri), URIRef(g.constructQueryUri)))
    graph.add((contentBlankNode, URIRef(g.typeUri), URIRef(g.queryUri)))
    graph.add((contentBlankNode, URIRef(g.originBaseUri), URIRef(g.agentKnowledgeUri)))
    graph.add((contentBlankNode, URIRef(g.sparqlUri), Literal(query, datatype=XSD.string)))

    print(graph.serialize(format="turtle"))
    return blankNode


def process(data):
    # print(data["label"])
    # print(data["uri"])
    # graph, seq = creatGraph(data["label"],data["uri"])
    graph, seq = createGraph("Drone SBT", "http://localhost:8090/rdf4j/repositories/behaviors#BT_00000000000")

    for actionDic in data:
        # print(actionDic)
        # print(data[actionDic])
        # print("generated tree")
        query = GenerateSparqlQuery(actionDic)
        # addUpdateNode(graph, seq)
        addSeqChild(graph, seq, actionDic, actionDic, query)

    SBT = graph.serialize(format="nt")
    # print("Graph data:", SBT)
    return True, SBT


if __name__ == "__main__":
    data = {"takeOff": {"actor": "Mavic2"},
            "land": {"actor": "Mavic2"},
            "captureImage": {"actor": "Mavic2", "pobj": "shelf1"},
            "moveTo": {"actor": "Mavic2", "pobj": "position1"}
            }
    process(data)
