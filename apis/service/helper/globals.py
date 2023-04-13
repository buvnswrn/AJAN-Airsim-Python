import rdflib.namespace

PORT = 4203
IP_ADDRESS = "localhost"

answer = {True: "Sparql Behavior Tree was successfully generated!",
          False: "Sparql Behavior Tree couldn't be generated. please reformulate the instruction"}

roleVarMap = {'actor': '', 'dobj': '', 'indobj': ''}
depRoleMap = {'nsubj': 'actor', 'dobj': 'dobj', 'pobj': 'indobj', 'indobj': 'indobj'}
emptyTree = {'type': 'sequence', 'children': []}

templates = {

    "take-off":
        {
            'variables': [{'label': 'ROBOT_X', 'role': 'actor'}],
            'query': r'''
    PREFIX mosim: <http://www.dfki.de/mosim-ns#takeOff>

}'''
        },
    "land":
        {
            'variables': [{'label': 'ROBOT_X', 'role': 'actor'}],
            'query': r'''

 PREFIX mosim: <http://www.dfki.de/mosim-ns#land>

}'''
        },
    "captureImage":
        {
            'variables': [{'label': 'ROBOT_X', 'role': 'actor'}],
            'query': r'''

 PREFIX mosim: <http://www.dfki.de/mosim-ns#captureImage>

}'''
        },
    "moveTo":
        {
            'variables': [{'label': 'ROBOT_X', 'role': 'actor'}, {'label': 'POSITION', 'role': 'pobj'}],
            'query': r'''

 PREFIX mosim: <http://www.dfki.de/mosim-ns#moveTo>

}'''
        },
    "pick up":
        {
            'variables': [{'label': 'AVATAR_X', 'role': 'actor'}, {'label': 'BLOCK_X', 'role': 'dobj'}],
            'query': r'''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mosim: <http://www.dfki.de/mosim-ns#>
PREFIX actn: <http://www.ajan.de/actn#>
PREFIX strips: <http://www.ajan.de/behavior/strips-ns#>

CONSTRUCT
{
	<AVATAR_X> rdf:type mosim:Avatar .
	<AVATAR_X> strips:is mosim:Empty .	
	<BLOCK_X> strips:is mosim:Clear .
	<BLOCK_X> strips:is mosim:Table .
}
WHERE {
	<AVATAR_X> rdf:type mosim:Avatar .
	<AVATAR_X> strips:is mosim:Empty .	
	<BLOCK_X> strips:is mosim:Clear .
	<BLOCK_X> strips:is mosim:Table .

}'''
        },

    "put down":
        {
            'variables': [{'label': 'AVATAR_X', 'role': 'actor'}, {'label': 'BLOCK_X', 'role': 'dobj'}],
            'query': r'''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mosim: <http://www.dfki.de/mosim-ns#>
PREFIX actn: <http://www.ajan.de/actn#>
PREFIX strips: <http://www.ajan.de/behavior/strips-ns#>

CONSTRUCT
{
	<AVATAR_X> rdf:type mosim:Avatar .
	<BLOCK_X> strips:is mosim:Holding.
}
WHERE {
	<AVATAR_X> rdf:type mosim:Avatar .
	<BLOCK_X> strips:is mosim:Holding.
}
'''
        },

    "stack":
        {
            'variables': [{'label': 'AVATAR_X', 'role': 'actor'}, {'label': 'BLOCK_X', 'role': 'dobj'},
                          {'label': 'BLOCK_Y', 'role': 'indobj'}],
            'query': r'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mosim: <http://www.dfki.de/mosim-ns#>
PREFIX actn: <http://www.ajan.de/actn#>
PREFIX strips: <http://www.ajan.de/behavior/strips-ns#>

CONSTRUCT
{
	<AVATAR_X> rdf:type mosim:Avatar .
	<BLOCK_X> strips:is mosim:Holding.
	<BLOCK_Y> strips:is mosim:Clear .
}
WHERE {
	<AVATAR_X> rdf:type mosim:Avatar .
	<BLOCK_X> rdf:type mosim:Block.
	<BLOCK_X> strips:is mosim:Holding.
	<BLOCK_Y> rdf:type mosim:Block.
	<BLOCK_Y> strips:is mosim:Clear .
}
'''
        },

    "unstack":
        {
            'variables': [{'label': 'AVATAR_X', 'role': 'actor'}, {'label': 'BLOCK_X', 'role': 'dobj'}],
            'query': r'''
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX mosim: <http://www.dfki.de/mosim-ns#>
PREFIX actn: <http://www.ajan.de/actn#>
PREFIX strips: <http://www.ajan.de/behavior/strips-ns#>

CONSTRUCT
{
	<AVATAR_X> rdf:type mosim:Avatar .
	<AVATAR_X> strips:is mosim:Empty .	
	<BLOCK_X> strips:is mosim:Clear .
	<BLOCK_X> mosim:on ?blockY .
}
WHERE {
	<AVATAR_X> rdf:type mosim:Avatar .
	<AVATAR_X> strips:is mosim:Empty .	
	<BLOCK_X> strips:is mosim:Clear .
	<BLOCK_X> mosim:on ?blockY .
}
'''
        },
}

goals = {'unstack': 'http://localhost:8090/rdf4j/repositories/agents#GO_19828b78-c997-4dfe-ab9d-d125c6ba0456',
         'stack': 'http://localhost:8090/rdf4j/repositories/agents#GO_33be6676-6606-4a25-b391-050f2452aac8',
         'pick up': 'http://localhost:8090/rdf4j/repositories/agents#GO_d1bc3e81-8ca2-4dc8-ba26-dce0b41c5e53',
         'put down': 'http://localhost:8090/rdf4j/repositories/agents#GO_851c54e3-ee9e-4f04-9268-4465f9aa23ea'
         }
droneGoals = {'take-off': 'http://localhost:8090/rdf4j/repositories/agents#GO_19828b78-c997-4dfe-ab9d-d125c6ba04560',
              'land': 'http://localhost:8090/rdf4j/repositories/agents#GO_33be6676-6606-4a25-b391-050f2452aac80',
              'captureImage': 'http://localhost:8090/rdf4j/repositories/agents#GO_d1bc3e81-8ca2-4dc8-ba26-dce0b41c5e530',
              'moveTo': 'http://localhost:8090/rdf4j/repositories/agents#GO_851c54e3-ee9e-4f04-9268-4465f9aa23ea0'
              }

# entities
btBaseUri = "http://localhost:8090/rdf4j/repositories/behaviors#BT"
goalProducerBaseUri = "http://localhost:8090/rdf4j/repositories/behaviors#GoalProducer"
sequenceBaseUri = "http://localhost:8090/rdf4j/repositories/behaviors#Sequence"
sbtFixedRootUri = "http://localhost:8090/rdf4j/repositories/behaviors#BT_b5ef33eb-a660-4169-8909-951ffe2ab797"

# relations
firstUri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#first"
restUri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"
typeUri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
originBaseUri = "http://www.ajan.de/behavior/bt-ns#originBase"
sparqlUri = "http://www.ajan.de/behavior/bt-ns#sparql"
hasChildUri = "http://www.ajan.de/behavior/bt-ns#hasChild"
hasChildrenUri = "http://www.ajan.de/behavior/bt-ns#hasChildren"
labelUri = "http://www.w3.org/2000/01/rdf-schema#label"
commentUri = "http://www.w3.org/2000/01/rdf-schema#comment"
contentUri = "http://www.ajan.de/behavior/bt-ns#content"
goalUri = "http://www.ajan.de/ajan-ns#goal"

# constant entities
btUri = "http://www.ajan.de/behavior/bt-ns#BehaviorTree"
rootUri = "http://www.ajan.de/behavior/bt-ns#Root"
sequenceUri = "http://www.ajan.de/behavior/bt-ns#Sequence"
constructQueryUri = "http://www.ajan.de/behavior/bt-ns#ConstructQuery"
queryUri = "http://www.ajan.de/behavior/bt-ns#QueryUri"
agentKnowledgeUri = "http://www.ajan.de/ajan-ns#AgentKnowledge"
goalProducerUri = "http://www.ajan.de/behavior/bt-ns#GoalProducer"

# name spaces
ajanNs = rdflib.namespace.Namespace("http://www.ajan.de/ajan-ns#")
btNs = rdflib.namespace.Namespace("http://www.ajan.de/behavior/bt-ns#")
RDF = rdflib.namespace.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
