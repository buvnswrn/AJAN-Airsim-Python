import rdflib


def parse_and_get_actions(data_string, fmt):
    g = rdflib.Graph()
    g.parse(data=data_string, format=fmt)
    actions = []
    for s, p, o in g:
        action_URI = rdflib.term.URIRef('http://www.ajan.de/behavior/mdp-ns#hasAction')
        if p == action_URI:
            action = str(o)
            action = action[1:action.__len__()-1]
            action = action.split(";, ")
            if action.__len__() == 1:
                action = action[0].replace(";", "")
                actions.append(action)
            else:
                for a in action:
                    a = a.replace(";", "")
                    actions.append(a)
    return actions
