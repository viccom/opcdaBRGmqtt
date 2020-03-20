import threading
import logging
import os
import base64
from mqtt_service.pub_client import MQTTStreamPubBase


class MQTTStreamPub(MQTTStreamPubBase):
    def __init__(self):
        MQTTStreamPubBase.__init__(self, "opcdabrg")

    def opcdabrg_out_pub(self, key, data):
        topic = "VNET_STREAM/{0}/OUT".format(key)
        payload = base64.b64encode(data)
        return self.publish(topic=topic, payload=payload, qos=1)

    def opcdabrg_in_pub(self, key, data):
        topic = "VNET_STREAM/{0}/IN".format(key)
        payload = base64.b64encode(data)
        return self.publish(topic=topic, payload=payload, qos=1)

    def opcdabrg_status(self, key, info):
        topic = "OPCDABRG_STATUS/{0}".format(key)
        return self.publish(topic=topic, payload=info, qos=1)

    def opcdabrg_datas(self, key, info):
        topic = "OPCDABRG_DATAS/{0}".format(key)
        return self.publish(topic=topic, payload=info, qos=1)

    def opcdabrg_log_pub(self, key, info):
        topic = "OPCDABRG_LOGS/{0}".format(key)
        return self.publish(topic=topic, payload=info, qos=1, retain=True)
