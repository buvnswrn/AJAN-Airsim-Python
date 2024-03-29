from flask_restx import Namespace, Resource, fields
from flask import Response, request, make_response
from rdflib import Graph, RDF

from .service import UnityService
import constants.constants as constants
from .service.helper import detect_pose, detect_objects
from .service.vocabulary.POMDPVocabulary import createIRI, pomdp_ns

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
    "objectOfInterest": fields.String(required=True, description="Object of interest"),
    "return_type": fields.String(required=False, description="Return Type of the object")
})

return_type = unity_service_ns.model('ReturnType', {
    "return_type": fields.String(required=False, description="Return type")
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
        return_type = request.json["return_type"] if request.json.keys().__contains__('return_type') else "json"
        response = UnityService.get_visible_objects(name, return_type)
        return make_response(response)


@unity_service_ns.route('/get-visible-objects-rdf')
@unity_service_ns.doc(description="Get Objects and their positions that are infront of the drone")
class GetVisibleObjects(Resource):
    @unity_service_ns.expect(get_object_data_format)
    def post(self):
        graph = Graph().parse(data=request.data.decode("utf-8"), format='turtle')
        name = str([o for s, p, o in graph.triples((pomdp_ns["objectOfInterest"], RDF.value, None))][0])
        objects_turtle = UnityService.get_visible_objects(name, "turtle")
        response = make_response(objects_turtle)
        response.headers['Content-Type'] = 'text/turtle'
        return response


@unity_service_ns.route('/get-navmesh-path')
@unity_service_ns.doc(description="Get Navmesh Path from Unity")
class GetNavmeshPath(Resource):
    @unity_service_ns.expect(navmesh_data_format)
    def post(self):
        s_x, s_y, s_z = request.json["start_position"].values()
        e_x, e_y, e_z = request.json["end_position"].values()
        return UnityService.get_navmesh_path(s_x, s_y, s_z, e_x, e_y, e_z)


@unity_service_ns.route("/get-pose-sensor-reading")
@unity_service_ns.doc(description="Get the image from camera and detect the pose and return the keypoints")
class GetPoseSensorReading(Resource):
    @unity_service_ns.expect(return_type)
    def post(self):
        expected_return_type = request.json['return_type']
        id = request.json['id']
        write = request.json['write'] if request.json.keys().__contains__('write') else False
        if expected_return_type is not None:
            response = make_response(detect_pose.estimate_pose(id=id, return_type=expected_return_type, write=write))
            response.mimetype = "text/plain"
            return response
        return detect_pose.estimate_pose(id=id)


@unity_service_ns.route("/get-object-sensor-reading")
@unity_service_ns.doc(description="Get the image from camera and detect the objects and return the bounding boxes")
class GetObjectSensorReading(Resource):
    @unity_service_ns.expect(return_type)
    def post(self):
        expected_return_type = request.json['return_type']
        id = request.json['id']
        write = request.json['write'] if request.json.keys().__contains__('write') else False
        confidence_level = request.json['conf'] if request.json.keys().__contains__('conf') else 0.3
        if expected_return_type is not None:
            response = make_response(detect_objects.detect_objects(id=id, conf=confidence_level,
                                                                   return_type=expected_return_type, write=write))
            response.mimetype = "text/plain"
            return response
        return detect_objects.detect_objects(id)
