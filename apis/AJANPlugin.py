from flask_restx import Namespace, Resource, fields
from flask import Response, request
from .service import AJANPlugin, airsim_controller, UnityService, RealWorldExecution
from constants import constants
from multiprocessing import Process
import logging
import sys

ajan_plugin_ns = Namespace('ajan_plugin', description="AJAN Plugin for processing RDF Input from AJAN Service "
                                                      "and control Drone using Airsim")

ajan_plugin_ns.logger.setLevel(constants.LOG_LEVEL)
ajan_plugin_ns.logger.info("Starting AJAN Service")
# logging.getLogger().addHandler(logging.StreamHandler())

# region Models
rdf_model = ajan_plugin_ns.model("RDFModel", {
    'rdf_data': fields.String(required=True, description="The RDF Data model as a string")
})


# endregion


@ajan_plugin_ns.route('/execute_actions')
@ajan_plugin_ns.expect(rdf_model)
@ajan_plugin_ns.doc(description="Execute actions from RDF Input")
class ExecuteActions(Resource):
    @ajan_plugin_ns.doc(description="Execute actions from RDF Input")
    def post(self):
        data = str(request.data.decode('utf-8'))
        actions_array = AJANPlugin.parse_and_get_actions(data, "turtle")
        ajan_plugin_ns.logger.debug(actions_array)
        for key in actions_array:
            execute_actions(actions_array[key])
        return Response(status=200)


def execute_actions(actions_array):
    ajan_plugin_ns.logger.debug("Received actions: " + str(actions_array))
    for actions in actions_array:
        for action in actions:
            simulation = None
            real_world_execution = None
            if action.__contains__("take-off"):
                ajan_plugin_ns.logger.info("Executing action: " + action)
                simulation = Process(target=airsim_controller.takeoff)
                real_world_execution = Process(target=RealWorldExecution.takeoff)
            elif action.__contains__("land"):
                simulation = Process(target=airsim_controller.land)
                real_world_execution = Process(target=RealWorldExecution.land)
            elif action.__contains__("captureImage"):
                # TODO: have to watch out for the boxes to take pictures
                simulation = Process(target=airsim_controller.captureImage, args=(constants.CAPTURE_FOLDER,))
                real_world_execution = Process(target=RealWorldExecution.capture_image,
                                               args=(constants.CAPTURE_FOLDER,))
            elif action.__contains__("moveto"):
                ajan_plugin_ns.logger.info("Executing action: " + action)
                robot, action = action[7:action.__len__() - 1].split(",")
                action = action.replace("$", "").replace(")", "").lstrip()
                x, y, z = UnityService.get_position_for_symbolic_location(action)
                # TODO: Find a way to pass multiple parameters to process in python
                airsim_controller.move(x, y, z, 10)
                simulation = Process(target=airsim_controller.move, args=(x, y, z, 10,))
                real_world_execution = Process(target=RealWorldExecution.move, args=(x, y, z,))
                # TODO: Find a way to get the symbolic location of objects in the scene in real world
            else:
                ajan_plugin_ns.logger.info("Action not supported: " + action)
            if simulation is not None and real_world_execution is not None:
                simulation.start()
                real_world_execution.start()
