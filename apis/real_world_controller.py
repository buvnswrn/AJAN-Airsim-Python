import configparser

from flask_restx import Namespace, Resource, fields
from flask import request, Response, make_response
from rdflib import Graph, RDF
from .service.vocabulary.POMDPVocabulary import _Planned_Action, createIRI, pomdp_ns
from Configuration import global_config
from constants import constants
from .service import RealWorldExecution
from .service.helper import detect_pose

realworld_controller_ns = Namespace('real_world_controller', description="Real world Controller")
realworld_controller_ns.logger.setLevel(constants.LOG_LEVEL)
realworld_controller_ns.logger.info("Starting Realworld Controller")
RealWorldExecution.set_logger(realworld_controller_ns.logger)

coordinates_data_format = realworld_controller_ns.model("Coordinates", {
    "x": fields.Float(required=True, description="value of x coordinate", default=1.6),
    "y": fields.Float(required=True, description="value of y coordinate", default=0.7),
    "z": fields.Float(required=True, description="value of z coordinate", default=2.3),
})

get_object_data_format = realworld_controller_ns.model('GetObjectDataFormat', {
    "objectOfInterest": fields.String(required=True, description="Object of interest")
})

if global_config['DEFAULT'].getboolean('enableRealWorldExecution'):
    RealWorldExecution.initialize()


@realworld_controller_ns.route('/takeoff')
@realworld_controller_ns.doc(description="Takeoff the drone")
class Takeoff(Resource):
    @realworld_controller_ns.doc(description="Takeoff the drone")
    def post(self):
        success, message = RealWorldExecution.takeoff()
        if success:
            return Response(status=200)
        else:
            return Response(status=403, response=message)


@realworld_controller_ns.route('/land')
@realworld_controller_ns.doc(description="Land the drone")
class Land(Resource):
    @realworld_controller_ns.doc(description="Land the drone")
    def post(self):
        RealWorldExecution.land()
        return Response(status=200)


# @realworld_controller_ns.route('/hover')
# @realworld_controller_ns.doc(description="Hover the drone")
# class Hover(Resource):
#     @realworld_controller_ns.doc(description="Hover the drone")
#     def post(self):
#         RealWorldExecution.hover()


@realworld_controller_ns.route('/move')
@realworld_controller_ns.doc(description="Move the drone")
class Move(Resource):
    @realworld_controller_ns.doc(description="Move the drone")
    @realworld_controller_ns.expect(coordinates_data_format)
    def post(self):
        RealWorldExecution.move(request.json['x'], request.json['y'], request.json['z'])
        # RealWorldExecution.move(1.6, 0.7, 2.3)
        return Response(status=200)

    @realworld_controller_ns.param('object_of_interest', 'Object of interest', default="Shelf-1")
    # @realworld_controller_ns.expect(fields.String)
    def get(self):
        return Response(status=200) \
            if RealWorldExecution.move_to_known_position(request.args.get('object_of_interest')) \
            else Response(status=400)


@realworld_controller_ns.route('/move-one-step-rdf')
@realworld_controller_ns.doc(description="Move the drone one step forward in the given direction - left or right by "
                                         "receiving RDF input from AJAN service")
class MoveOneStepRDF(Resource):
    @realworld_controller_ns.doc(description="Move the drone one step in a given direction")
    @realworld_controller_ns.expect(get_object_data_format)
    def post(self):
        graph = Graph().parse(data=request.data.decode("utf-8"), format="turtle")
        attr_node = [s for s, p, o in graph.triples((None, RDF.type, _Planned_Action))][0]
        motion_iri = createIRI(pomdp_ns, "motion")
        direction = str([o for s, p, o in graph.triples((attr_node, motion_iri, None))][0])
        return Response(status=200) \
            if RealWorldExecution.turn_one_step(direction) \
            else Response(status=400)


@realworld_controller_ns.route('/turn-one-step-rdf')
@realworld_controller_ns.doc(description="Turn the drone one step forward in the given direction - left or right by "
                                         "receiving RDF input from AJAN service")
class MoveOneStepRDF(Resource):
    @realworld_controller_ns.doc(description="Turn the drone one step in a given direction")
    @realworld_controller_ns.expect(get_object_data_format)
    def post(self):
        graph = Graph().parse(data=request.data.decode("utf-8"), format="turtle")
        attr_node = [s for s, p, o in graph.triples((None, RDF.type, _Planned_Action))][0]
        motion_iri = createIRI(pomdp_ns, "motion")
        direction = str([o for s, p, o in graph.triples((attr_node, motion_iri, None))][0])
        return Response(status=200) \
            if RealWorldExecution.turn_one_step(direction) \
            else Response(status=400)


@realworld_controller_ns.route('/turn-one-step')
@realworld_controller_ns.doc(description="Turn the drone one step forward in the given direction - left or right by "
                                         "receiving RDF input from AJAN service")
class MoveOneStepRDF(Resource):
    @realworld_controller_ns.doc(description="Turn the drone one step in a given direction")
    @realworld_controller_ns.expect(get_object_data_format)
    def post(self):
        direction = request.json['direction']
        return Response(status=200) \
            if RealWorldExecution.turn_one_step(direction) \
            else Response(status=400)


@realworld_controller_ns.route('/perceive')
@realworld_controller_ns.doc(description="Perceive the drone environment")
class Perceive(Resource):
    @realworld_controller_ns.doc(description="Perceive the drone environment")
    def post(self):
        print("Perceiving")  # Dummy perceive function
        return Response(status=200)


@realworld_controller_ns.route('/get-pose-sensor-reading')
@realworld_controller_ns.doc(description="Get observation from the drone environment")
class GetObservation(Resource):
    @realworld_controller_ns.doc(description="Get observation from the drone environment")
    @realworld_controller_ns.expect(get_object_data_format)
    def post(self):
        # get image
        img = RealWorldExecution.get_image()
        # detect pose
        pose_id = request.json['id']
        expected_return_type = request.json['return_type']
        write = bool(request.json['write']) if request.json.keys().__contains__('write') else True
        if expected_return_type is not None:
            response = make_response(detect_pose.get_pose_estimation(img, pose_id, expected_return_type, write))
            response.mimetype = "text/plain"
            return response
        return detect_pose.get_pose_estimation(img, pose_id)


@realworld_controller_ns.route('/capture_image')
@realworld_controller_ns.doc(description="Capture image from the drone")
class CaptureImage(Resource):
    @realworld_controller_ns.doc(description="Capture image from the drone")
    def post(self):
        RealWorldExecution.capture_image(constants.CAPTURE_FOLDER)
        return Response(status=200)


@realworld_controller_ns.route('/turn_live_image_on')
@realworld_controller_ns.doc(description="Turn live image on")
class TurnLiveImageOn(Resource):
    @realworld_controller_ns.doc(description="Turn live image on")
    def post(self):
        RealWorldExecution.turn_live_image_on()
        return Response(status=200)


@realworld_controller_ns.route('/turn_live_image_off')
@realworld_controller_ns.doc(description="Turn live image off")
class TurnLiveImageOff(Resource):
    @realworld_controller_ns.doc(description="Turn live image off")
    def post(self):
        RealWorldExecution.turn_live_image_off()
        return Response(status=200)


@realworld_controller_ns.route('/get-objects/<string:object_of_interest>')
@realworld_controller_ns.route('/get-objects')
@realworld_controller_ns.doc(description="Get known positions from the drone environment")
# @realworld_controller_ns.expect(get_object_data_format)
class GetObjects(Resource):
    @realworld_controller_ns.doc(description="Get known positions from the drone environment")
    def get(self, object_of_interest):
        return Response(status=200, mimetype='application/json',
                        response=RealWorldExecution.get_objects(object_of_interest))

    def get(self):
        return Response(status=200, mimetype='application/json',
                        response=RealWorldExecution.get_objects(None))
