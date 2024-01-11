import configparser

import cv2
from flask_restx import Namespace, Resource, fields
from flask import request, Response, jsonify
import airsim
import logging

from rdflib import Graph, RDF

from constants import constants
from .service import airsim_controller
from Configuration import global_config
from .service.vocabulary.POMDPVocabulary import createIRI, pomdp_ns, _Planned_Action

airsim_controller_ns = Namespace('airsim_controller', description="Airsim Controller")
airsim_controller_ns.logger.setLevel(constants.LOG_LEVEL)
airsim_controller_ns.logger.info("Starting Airsim Controller")
airsim_controller.set_logger(airsim_controller_ns.logger)

if global_config['DEFAULT'].getboolean('enableAirsim'):
    airsim_controller.initialize()

move_one_step_data = airsim_controller_ns.model('MoveOneStepDataFormat', {
    "direction": fields.String(required=True, description="Direction to move one step")
})


@airsim_controller_ns.route('/takeoff')
@airsim_controller_ns.doc(description="Takeoff the drone")
class Takeoff(Resource):
    @airsim_controller_ns.doc(description="Takeoff the drone")
    def post(self):
        airsim_controller.takeoff()
        return Response(status=200)


@airsim_controller_ns.route('/land')
@airsim_controller_ns.doc(description="Land the drone")
class Land(Resource):
    @airsim_controller_ns.doc(description="Land the drone")
    def post(self):
        airsim_controller.land()
        return Response(status=200)


@airsim_controller_ns.route('/hover')
@airsim_controller_ns.doc(description="Hover the drone")
class Hover(Resource):
    @airsim_controller_ns.doc(description="Hover the drone")
    def post(self):
        airsim_controller.hover()
        return Response(status=200)


@airsim_controller_ns.route('/move')
@airsim_controller_ns.doc(description="Move the drone")
class Move(Resource):
    @airsim_controller_ns.doc(description="Move the drone")
    def post(self):
        airsim_controller.move(request.json['x'], request.json['y'], request.json['z'], request.json['v'])
        return Response(status=200)


@airsim_controller_ns.route('/move-one-step')
@airsim_controller_ns.doc(description="Move the drone one step forward in the given direction - left or right")
class MoveOneStep(Resource):
    @airsim_controller_ns.doc(description="Move the drone one step in a given direction")
    @airsim_controller_ns.expect(move_one_step_data)
    def post(self):
        direction = request.json['direction']
        motion = request.json['motion']
        airsim_controller.move_one_step(direction)
        return Response(status=200)


@airsim_controller_ns.route('/move-one-step-rdf')
@airsim_controller_ns.doc(description="Move the drone one step forward in the given direction - left or right by "
                                      "taking rdf input")
class MoveOneStep(Resource):
    @airsim_controller_ns.doc(description="Move the drone one step in a given direction")
    @airsim_controller_ns.expect(move_one_step_data)
    def post(self):
        graph = Graph().parse(data=request.data.decode("utf-8"), format='turtle')
        attr_node = [s for s, p, o in graph.triples((None, RDF.type, _Planned_Action))][0]
        motion_iri = createIRI(pomdp_ns, "motion")
        direction = str([o for s, p, o in graph.triples((attr_node, motion_iri, None))][0])
        airsim_controller.move_one_step(direction)
        return Response(status=200)


@airsim_controller_ns.route('/move-one-step-right')
@airsim_controller_ns.doc(description="Move the drone one step forward in the right direction")
class MoveOneStepRight(Resource):
    @airsim_controller_ns.doc(description="Move the drone one step in right direction")
    def post(self):
        airsim_controller.move_one_step("right")
        return Response(status=200)


@airsim_controller_ns.route('/move-one-step-left')
@airsim_controller_ns.doc(description="Move the drone one step forward in the left direction")
class MoveOneStepLeft(Resource):
    @airsim_controller_ns.doc(description="Move the drone one step in left direction")
    def post(self):
        airsim_controller.move_one_step("left")
        return Response(status=200)


@airsim_controller_ns.route('/perceive')
@airsim_controller_ns.doc(description="Dummy Perceive Method")
class Perceive(Resource):
    @airsim_controller_ns.doc(description="Dummy Perceive Method")
    def post(self):
        print("Perceiving")
        return Response(status=200)


@airsim_controller_ns.route('/capture_image')
@airsim_controller_ns.doc(description="Capture image from the drone")
class CaptureImage(Resource):
    @airsim_controller_ns.doc(description="Capture image from the drone")
    def post(self):
        airsim_controller.captureImage(constants.CAPTURE_FOLDER)
        return Response(status=200)


@airsim_controller_ns.route('/get-current-position')
@airsim_controller_ns.doc(description="Get the current position of the drone")
class GetCurrentPosition(Resource):
    @airsim_controller_ns.doc(description="Get the current position of the drone")
    def post(self):
        response = airsim_controller.get_current_position()
        return jsonify(response)
