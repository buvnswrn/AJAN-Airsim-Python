from flask_restx import Namespace, Resource
from flask import Response


ajan_plugin_ns = Namespace('ajan_plugin', description="AJAN Plugin for processing RDF Input from AJAN Service "
                                                      "and control Drone using Airsim")


@ajan_plugin_ns.route('/execute_actions')
@ajan_plugin_ns.doc(description="Execute actions from RDF Input")
class ExecuteActions(Resource):
    @ajan_plugin_ns.doc(description="Execute actions from RDF Input")
    def post(self):
        # TODO: receive RDF input from AJAN service
        return Response(status=200)
