from flask_restx import Namespace, Resource, fields
from flask import Response, request
from .service import UnityService

unity_service_ns = Namespace('Unity-service', description="Unity Service for retrieving object data and Navmesh Path "
                                                          "from Unity")


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

# endregion


@unity_service_ns.route('/get-objects')
@unity_service_ns.doc(description="Get objects and their positions from Unity")
class GetObjects(Resource):
    def post(self):
        # TODO: receive RDF input from AJAN service
        return Response(status=200)


@unity_service_ns.route('/get-navmesh-path')
@unity_service_ns.doc(description="Get Navmesh Path from Unity")
class GetNavmeshPath(Resource):
    @unity_service_ns.expect(navmesh_data_format)
    def post(self):
        s_x, s_y, s_z = request.json["start_position"].values()
        e_x, e_y, e_z = request.json["end_position"].values()
        return UnityService.get_navmesh_path(s_x, s_y, s_z, e_x, e_y, e_z)
