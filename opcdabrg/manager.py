import threading
import logging
import re
import time
import json
import os
from ping3 import ping
import configparser
import requests
import hashlib
from time import sleep
from opcdabrg.opcda import *
from opcdabrg.opcda_tunnel import OPCDATunnel


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return None
    myHash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest().upper()

class OPCDABRGManager(threading.Thread):
    def __init__(self, stream_pub):
        threading.Thread.__init__(self)
        self._thread_stop = False
        self._mqtt_stream_pub = stream_pub
        self._opcdatunnel = None

    def list_opcservers(self, opchost=None):
        return list_OPCServers(opchost)

    def list_opctags(self, opcserver, opchost=None):
        result = opcTagsList(opcserver, opchost)
        return result

    def on_setConfig(self, opcConfig):
        if not self._opcdatunnel.mqtt_clientid:
            self._opcdatunnel.start_opctunnel(opcConfig)
            return {"status": "starting"}
        elif self._opcdatunnel.mqtt_clientid == opcConfig.get('clientid'):
            self._opcdatunnel.start_opctunnel(opcConfig)
            return {"status": "updating"}
        else:
            return {"status": "busying"}

    def on_setConfigForced(self, opcConfig):
        if self._opcdatunnel.opctunnel_clean():
            self._opcdatunnel.start_opctunnel(opcConfig)
        return {"status": "reinitialize"}

    def on_getConfig(self):
        return self._opcdatunnel.get_opcConfig()

    def on_deviceRead(self):
        if self._opcdatunnel.opctunnel_isrunning():
            return self._opcdatunnel.get_opcDatas()
        else:
            return None

    def on_deviceWrite(self, tags_values):
        if not self._opcdatunnel.opctunnel_isrunning():
            return self._opcdatunnel.set_opcDatas(tags_values)
        else:
            return None

    def api_tunnelPause(self):
        return self._opcdatunnel.opctunnel_pause()

    def on_tunnelResume(self):
        return self._opcdatunnel.opctunnel_resume()

    def on_tunnelClean(self):
        return self._opcdatunnel.opctunnel_clean()

    def opctunnel_status(self):
        return self._opcdatunnel.opctunnel_isrunning()

    def on_event(self, event, ul_value):
        return True

    def start(self):
        self._opcdatunnel = OPCDATunnel(self._mqtt_stream_pub)
        self._opcdatunnel.start()
        threading.Thread.start(self)

    def run(self):
        while not self._thread_stop:
            time.sleep(1)
        logging.warning("Close OPCDABRG!")

    def stop(self):
        self._opcdatunnel.stop()
        self._thread_stop = True
        self.join()
