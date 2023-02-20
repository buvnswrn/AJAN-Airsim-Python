import rdflib
from rdflib.graph import Seq
from rdflib.namespace import RDF, RDFS
import collections
def parse_and_get_actions(data_string, fmt):
    g = rdflib.Graph()
    g.parse(data=data_string, format=fmt)
    actions = dict()
    MDPActions_subject = rdflib.URIRef("http://www.ajan.de/behavior/mdp-ns#MDPExecuteActions")
    hasAction = rdflib.term.URIRef('http://www.ajan.de/behavior/mdp-ns#hasAction')
    label = rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#label')
    actions_list = g.objects(MDPActions_subject, hasAction)
    for action in actions_list:
        rest = action
        round_num, turn_num = None, None
        while rest != RDF.nil:
            action_num = g.value(rest, label)
            if action_num is not None:
                round_num, turn_num = action_num.split("_")
                round_num = int(round_num)
                turn_num = int(turn_num)
            try:
                turn_dict = actions[round_num]
            except KeyError:
                actions[round_num] = dict()
            first_element = g.value(rest, RDF.first)
            if first_element is not None:
                actions[round_num][turn_num] = first_element.__str__()
            rest = g.objects(rest, RDF.rest).__next__()
    # formatting the actions dictionary to list
    sorted_actions = dict()
    for key in sorted(actions):
        sorted_actions[key] = list()
        for key1 in sorted(actions[key]):
            sorted_actions[key].append(actions[key][key1])
    # for s, p, o in g:
    #     action_URI = rdflib.term.URIRef('http://www.ajan.de/behavior/mdp-ns#hasAction')
    #     action_list = g.objects(action_URI)
    #     action_list = action_list.__next__()
    #     if p == action_URI:
    #         action = str(o)
    #         action = action[1:action.__len__()-1]
    #         action = action.split(";, ")
    #         if action.__len__() == 1:
    #             action = action[0].replace(";", "")
    #             actions.append(action)
    #         else:
    #             for a in action:
    #                 a = a.replace(";", "")
    #                 actions.append(a)
    return sorted_actions
