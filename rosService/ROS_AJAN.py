from fastapi import APIRouter
from laser_tag.srv import TagActionObs
from rospy_message_converter import message_converter
import rospy

ros_ajan_ns = APIRouter(prefix="/AJAN/ros")


def service_call(service_name, action):
    rospy.wait_for_service(service_name)
    try:
        service_proxy = rospy.ServiceProxy(service_name, TagActionObs)
        response = service_proxy(action=action)
        return message_converter.convert_ros_message_to_dictionary(response)
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed:{str(e)}")
        return None


@ros_ajan_ns.post("/call-service/{service-name}")
def call_service(service_name: str, action: int):
    response = service_call(service_name, action)
    if response is not None:
        return response
    else:
        return {"message": "Service Call Failed"}
