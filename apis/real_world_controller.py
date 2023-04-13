from flask_restx import Namespace, Resource, fields
from flask import request, Response

from constants import constants
from .service import RealWorldExecution

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

RealWorldExecution.initialize()


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


@realworld_controller_ns.route('/capture_image')
@realworld_controller_ns.doc(description="Capture image from the drone")
class CaptureImage(Resource):
    @realworld_controller_ns.doc(description="Capture image from the drone")
    def post(self):
        RealWorldExecution.capture_image(constants.CAPTURE_FOLDER)
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
