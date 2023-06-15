from fastapi import APIRouter, HTTPException
from .service import ROSService

ros_ajan_ns = APIRouter(prefix="/AJAN/ros")


@ros_ajan_ns.post("/call-service/{service-name}")
def call_service(service_name: str, action: int):
    response = ROSService.service_call(service_name, action)
    if response is not None:
        return response
    else:
        return {"message": "Service Call Failed"}


@ros_ajan_ns.post("/get-param/{service-name}")
def get_param(service_name: str):
    return ROSService.get_param(service_name)


@ros_ajan_ns.post("/wait-for-service/{service-name}")
def wait_for_service(service_name: str):
    return ROSService.wait_for_service(service_name)


@ros_ajan_ns.post("/initialize-service-client/{service-name}")
def wait_for_service(service_name: str):
    if ROSService.setup_service_client(service_name) is False:
        raise HTTPException(status_code=500)

