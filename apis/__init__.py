from flask_restx import Api
from .airsim_controller import airsim_controller_ns
from .AJANPlugin import ajan_plugin_ns
from .UnityService import unity_service_ns

api = Api(version="0.1", title="AJAN-Airsim Controller", description="API for controlling Airsim through AJAN")
api.add_namespace(airsim_controller_ns)
api.add_namespace(ajan_plugin_ns)
api.add_namespace(unity_service_ns)
