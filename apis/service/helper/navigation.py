import json

import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as mqtt_subscribe
import paho.mqtt.publish as mqtt_publish

from constants.mavic2_api_constants import MQTT

position = {}
USERNAME = "drone_vslam"
PASSWORD = "Dr0ne-vsl4m"


class Navigation:
    __mqtt_client: mqtt.Client = None

    @staticmethod
    def on_connect(mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    @staticmethod
    def on_message(mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        print("Message received:" +str(msg.payload))

    @staticmethod
    def on_publish(self, mqttc, obj, mid):
        print("Published mid: " + str(mid))

    @staticmethod
    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    @staticmethod
    def on_log(self, mqttc, obj, level, string):
        print("message:" + type(string))
        # print("message:"+string)

    def __init__(self, loop_forever=False, logging=True):
        print("Initializing MQTT Client")
        self.__mqtt_client = mqtt.Client(transport="websockets")
        self.__mqtt_client.on_message = self.on_message
        self.__mqtt_client.on_connect = self.on_connect
        self.__mqtt_client.on_publish = self.on_publish
        self.__mqtt_client.on_subscribe = self.on_subscribe
        self.__mqtt_client.on_log = self.on_log
        self.__mqtt_client.username_pw_set(username=USERNAME, password=PASSWORD)
        self.__mqtt_client.connect(MQTT.DOMAIN, MQTT.WEBSOCKET_PORT, keepalive=60)

        if logging:
            self.__mqtt_client.enable_logger()

        if loop_forever:
            self.__mqtt_client.loop_forever()

        # return __mqtt_client

    def __del__(self):
        print("Disconnecting MQTT Client")
        # self.__mqtt_client.disconnect()

    def is_initialized(self):
        return True if self.__mqtt_client is None else False

    def get_client(self):
        return self.__mqtt_client

    def subscribe_forever(self, channel):
        print("Subscribing to:" + channel)
        return self.__mqtt_client.subscribe(channel)

    def subscribe(self,channel):
        print("Subscribing to:"+channel)
        auth = {'username': USERNAME, 'password': PASSWORD}
        result = mqtt_subscribe.simple(channel, hostname=MQTT.DOMAIN, keepalive=60, auth=auth)
        if result is not None:
            return json.loads(result.payload)
        else:
            return "Result not returned"

    def publish_forever(self, channel):
        print("Publishing to:" + channel)
        return self.__mqtt_client.publish(channel)

    def publish(self, channel, message=None):
        if message is None:
            message = {}
        print("Publishing to:" + channel+" with payload: "+str(message))
        auth = {'username': USERNAME, 'password': PASSWORD}
        return mqtt_publish.single(channel, hostname=MQTT.DOMAIN, payload=str(message), auth=auth)

    def get_positions(self):
        pass
