from flask_restx import Namespace, Resource
from flask import request, Response

from constants import constants
from .service import RealWorldExecution

realworld_controller_ns = Namespace('real_world_controller', description="Real world Controller")
realworld_controller_ns.logger.setLevel(constants.LOG_LEVEL)
realworld_controller_ns.logger.info("Starting Realworld Controller")
RealWorldExecution.set_logger(realworld_controller_ns.logger)


@realworld_controller_ns.route('/takeoff')
@realworld_controller_ns.doc(description="Takeoff the drone")
class Takeoff(Resource):
    @realworld_controller_ns.doc(description="Takeoff the drone")
    def post(self):
        RealWorldExecution.takeoff()
        return Response(status=200)


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
    def post(self):
        RealWorldExecution.move(request.json['x'], request.json['y'], request.json['z'])
        return Response(status=200)


@realworld_controller_ns.route('/capture_image')
@realworld_controller_ns.doc(description="Capture image from the drone")
class CaptureImage(Resource):
    @realworld_controller_ns.doc(description="Capture image from the drone")
    def post(self):
        RealWorldExecution.capture_image(constants.CAPTURE_FOLDER)
        return Response(status=200)



