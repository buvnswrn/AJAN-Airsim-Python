import cv2
from flask_restx import Namespace, Resource
from flask import request, Response
import airsim

from constants import constants
from .service import airsim_controller

airsim_controller_ns = Namespace('airsim_controller', description="Airsim Controller")


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


@airsim_controller_ns.route('/capture_image')
@airsim_controller_ns.doc(description="Capture image from the drone")
class CaptureImage(Resource):
    @airsim_controller_ns.doc(description="Capture image from the drone")
    def post(self):
        airsim_controller.captureImage(constants.CAPTURE_FOLDER)
        return Response(status=200)
