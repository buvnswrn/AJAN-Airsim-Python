from flask_restx import Namespace, Resource
from flask import Response, request
from .service import AJANPlugin, airsim_controller, UnityService
from constants import constants
import logging
import sys

ajan_plugin_ns = Namespace('ajan_plugin', description="AJAN Plugin for processing RDF Input from AJAN Service "
                                                      "and control Drone using Airsim")

ajan_plugin_ns.logger.setLevel(constants.LOG_LEVEL)
ajan_plugin_ns.logger.info("Starting AJAN Service")
# logging.getLogger().addHandler(logging.StreamHandler())


@ajan_plugin_ns.route('/execute_actions')
@ajan_plugin_ns.doc(description="Execute actions from RDF Input")
class ExecuteActions(Resource):
    @ajan_plugin_ns.doc(description="Execute actions from RDF Input")
    def post(self):
        data = str(request.data.decode('utf-8'))
        actions_array = AJANPlugin.parse_and_get_actions(data, "turtle")
        ajan_plugin_ns.logger.debug(actions_array)
        for key in actions_array:
            executeActions(actions_array[key])
        return Response(status=200)


def executeActions(actions_array):
    ajan_plugin_ns.logger.debug("Received actions: " + str(actions_array))
    for actions in actions_array:
        for action in actions:
            if action.__contains__("take-off"):
                ajan_plugin_ns.logger.info("Executing action: " + action)
                # TODO: have to watch out for the location to take off
                airsim_controller.takeoff()
                # TODO: Write a lab execution API for Takeoff
            elif action.__contains__("land"):
                airsim_controller.land()
                # TODO: Write a lab execution API for Landing
            elif action.__contains__("captureImage"):
                # TODO: have to watch out for the boxes to take pictures
                airsim_controller.captureImage(constants.CAPTURE_FOLDER)
                # TODO: Write a lab execution API for Capture Image
            elif action.__contains__("moveto"):
                ajan_plugin_ns.logger.info("Executing action: " + action)
                robot, action = action[7:action.__len__()-1].split(",")
                action = action.replace("$", "").replace(")", "").lstrip()
                x, y, z = UnityService.get_position_for_symbolic_location(action)
                airsim_controller.move(x, y, z, 10)
                # TODO: Write a lab execution API for Moving
            else:
                ajan_plugin_ns.logger.info("Action not supported: " + action)




