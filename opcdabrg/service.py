import threading
import logging
import json
import os
from mqtt_service import *
from hbmqtt_broker.conf import MQTT_PROT

API_RESULT = "@api/RESULT"
API_LIST = "@api/list"
match_api = re.compile(r'^@api/(.+)$')

class OPCDABRG_Service(BaseService):
    def __init__(self, manager):
        self._manager = manager
        mqtt_conn = "localhost:{0}".format(MQTT_PROT)
        BaseService.__init__(self, mqtt_conn, {
            "api": "v1/opcdabrg/api",
        })

    def start(self):
        BaseService.start(self)

    @whitelist.__func__
    def api_ping(self, id, params):
        print("id:", id, "params:", params)
        ret = 'pong'
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_found")

    @whitelist.__func__
    def api_opcservers_list(self, id, params):
        # print("params:", params)
        ret = self._manager.opcservers_list()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_servers")

    @whitelist.__func__
    def api_opctags_list(self, id, params):
        # print("params:", params)
        ret = self._manager.opctags_list
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_version")

    @whitelist.__func__
    def api_setConfig(self, id, params):
        # print("params:", params)
        opcConfig = params.get('config')
        ret = self._manager.on_setConfig(opcConfig)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_getConfig(self, id, params):
        # print("params:", params)
        ret = self._manager.on_getConfig()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_deviceRead(self, id, params):
        # print("params:", params)
        ret = self._manager.on_deviceRead()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_deviceWrite(self, id, params):
        # print("params:", params)
        tags = params.get('tags')
        values = params.get('values')
        ret = self._manager.on_deviceWrite(tags, values)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_tunnelPause(self, id, params):
        # print("params:", params)
        ret = self._manager.on_tunnelPause()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_tunnelResume(self, id, params):
        # print("params:", params)
        ret = self._manager.on_tunnelResume()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_tunnelClean(self, id, params):
        # print("params:", params)
        # command = params.get('start')
        ret = self._manager.on_tunnelClean()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_tunnelStatus(self, id, params):
        # print("params:", params)
        ret = self._manager.opctunnel_isrunning()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")
