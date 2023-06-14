from fastapi import FastAPI
from rosService import ROS_AJAN
import rospy

app = FastAPI(title="AJAN-ROS", description="API for controlling ROS through AJAN")
app.include_router(ROS_AJAN.ros_ajan_ns, tags=['ROS Service'])


@app.on_event("startup")
def ros_init():
    rospy.init_node("ros_ajan_node", anonymous=True)


@app.on_event("shutdown")
def ros_shutdown():
    rospy.signal_shutdown("ros_ajan_node")

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
