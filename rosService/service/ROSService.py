from fastapi import HTTPException
from laser_tag.srv import TagActionObs
from rospy_message_converter import message_converter
import rospy

service_client: rospy.ServiceProxy


def service_call(service_name, action):
    rospy.wait_for_service(service_name)
    global service_client
    try:
        response = service_client(action=action)
        return message_converter.convert_ros_message_to_dictionary(response)
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Service call failed:{str(e)}")
    except NameError as name_error:
        rospy.logerr(f"Service client not defined:{str(name_error)}")
        raise HTTPException(status_code=500, detail="Initialize the client before calling")



def get_param(service_name):
    return rospy.get_param(service_name)


def wait_for_service(service_name):
    return rospy.wait_for_service(service=service_name)


def setup_service_client(service_name):
    global service_client
    service_client = rospy.ServiceProxy(service_name, TagActionObs)
    return True
