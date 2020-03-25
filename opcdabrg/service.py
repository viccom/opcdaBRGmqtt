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
        # print("id:", id, "params:", params)
        ret = 'pong'
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_found")

    @whitelist.__func__
    def api_opcservers_list(self, id, params):
        # print("params:", params)
        opchost = params.get('opchost') or 'localhost'
        ret = self._manager.list_opcservers(opchost)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_servers")

    @whitelist.__func__
    def api_opctags_list(self, id, params):
        # print("params:", params)
        opcserver = params.get('opcserver')
        opchost = params.get('opchost') or 'localhost'
        ret = self._manager.list_opctags(opcserver, opchost)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no_version")

    @whitelist.__func__
    def api_setConfig(self, id, params):
        # print("params:", params)
        # opcConfig = {"opcname":"name", "opchost":"host", "opcitems":['item1','item2'], "opctags": [['name','type','item'],['name','type','item']]}
        opcConfig = params.get('config')
        ret = None
        if opcConfig.get('opcname') and opcConfig.get('clientid') and opcConfig.get('opctags'):
            ret = self._manager.on_setConfig(opcConfig)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "no")

    @whitelist.__func__
    def api_setConfigForced(self, id, params):
        # print("params:", params)
        opcConfig = params.get('config')
        ret = None
        if opcConfig.get('opcname') and opcConfig.get('clientid') and opcConfig.get('opctags'):
            ret = self._manager.on_setConfigForced(opcConfig)
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
        # tags_values = [(item, value),(item, value)] or (item, value)
        tags_values = params.get('tags_values')
        ret = self._manager.on_deviceWrite(tags_values)
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "unknown")

    @whitelist.__func__
    def api_tunnelPause(self, id, params):
        # print("params:", params)
        ret = self._manager.on_tunnelPause()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "unknown")

    @whitelist.__func__
    def api_tunnelResume(self, id, params):
        # print("params:", params)
        ret = self._manager.on_tunnelResume()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "unknown")

    @whitelist.__func__
    def api_tunnelClean(self, id, params):
        # print("params:", params)
        # command = params.get('start')
        ret = self._manager.on_tunnelClean()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "unknown")

    @whitelist.__func__
    def api_tunnelStatus(self, id, params):
        # print("params:", params)
        ret = self._manager.opctunnel_status()
        if ret:
            return self.success("api", id, ret)
        else:
            return self.failure("api", id, "unknown")
