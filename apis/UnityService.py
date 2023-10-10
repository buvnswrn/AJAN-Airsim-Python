from flask_restx import Namespace, Resource, fields
from flask import Response, request
from .service import UnityService
import constants.constants as constants

unity_service_ns = Namespace('Unity-service', description="Unity Service for retrieving object data and Navmesh Path "
                                                          "from Unity")
unity_service_ns.logger.setLevel(constants.LOG_LEVEL)
unity_service_ns.logger.info("Starting Unity Service")

UnityService.set_logger(unity_service_ns.logger)

# region Request models
coordinates_data_format = unity_service_ns.model("Coordinates", {
    "x": fields.Float(required=True, description="value of x coordinate"),
    "y": fields.Float(required=True, description="value of y coordinate"),
    "z": fields.Float(required=True, description="value of z coordinate"),
})

navmesh_data_format = unity_service_ns.model('NavmeshDataFormat', {
    "start_position": fields.Nested(coordinates_data_format),
    "end_position": fields.Nested(coordinates_data_format)
})

get_object_data_format = unity_service_ns.model('GetObjectDataFormat', {
    "objectOfInterest": fields.String(required=True, description="Object of interest")
})


# endregion


@unity_service_ns.route('/get-objects')
@unity_service_ns.doc(description="Get objects and their positions from Unity")
class GetObjects(Resource):
    @unity_service_ns.expect(get_object_data_format)
    def post(self):
        # TODO: receive RDF input from AJAN service
        name = request.json['objectOfInterest']
        response = UnityService.get_objects(name)
        unity_service_ns.logger.debug(UnityService.get_position_for_symbolic_location(name))
        return response


@unity_service_ns.route('/get-visible-objects')
@unity_service_ns.doc(description="Get Objects and their positions that are infront of the drone")
class GetVisibleObjects(Resource):
    @unity_service_ns.expect(get_object_data_format)
    def post(self):
        name = request.json['objectOfInterest']
        response = UnityService.get_visible_objects(name)
        return response


@unity_service_ns.route('/get-navmesh-path')
@unity_service_ns.doc(description="Get Navmesh Path from Unity")
class GetNavmeshPath(Resource):
    @unity_service_ns.expect(navmesh_data_format)
    def post(self):
        s_x, s_y, s_z = request.json["start_position"].values()
        e_x, e_y, e_z = request.json["end_position"].values()
        return UnityService.get_navmesh_path(s_x, s_y, s_z, e_x, e_y, e_z)
