#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import logging
import time
import os
import re
from opcdabrg.opcda import *

class OPCDATunnel(threading.Thread):
    def __init__(self, mqttpub):
        threading.Thread.__init__(self)
        self._mqttpub = mqttpub
        self._opctunnel_isrunning = False
        self._opcConfig = None
        self._opcdaclient = None
        self.mqtt_clientid = None
        self._thread_stop = False

    def get_opcConfig(self):
        return self._opcConfig

    def start_opctunnel(self, opcConfig):
        self._opcConfig = opcConfig
        self.mqtt_clientid = opcConfig.get('clientid')
        self._opctunnel_isrunning = True

    def get_opcDatas(self):
        opcClient = OpenOPC.client()
        try:
            opcClient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
        except Exception as ex:
            logging.warning('connect OPCDA Server err!err!err!')
            logging.exception(ex)
        if opcClient.isconnected:
            try:
                datas = opcClient.read(self._opcConfig.get('tags'), sync=True)
                opcClient.close()
                return datas
            except Exception as ex:
                logging.warning('readItem err!err!err!')
                logging.exception(ex)
                opcClient.close()
        else:
            return None

    def set_opcDatas(self):
        return self._opcConfig

    def loop_readDatas(self, client):
        if client.isconnected:
            try:
                datas = client.read(self._opcConfig.get('tags'), sync=True)
                return datas
            except Exception as ex:
                logging.warning('readItem err!err!err!')
                logging.exception(ex)

    def opctunnel_pause(self):
        self._opctunnel_isrunning = False
        return True

    def opctunnel_resume(self):
        self._opctunnel_isrunning = True
        return True

    def opctunnel_clean(self):
        self._opctunnel_isrunning = None
        self._opcConfig = None
        return True

    def opctunnel_isrunning(self):
        return self._opctunnel_isrunning

    def run(self):
        if not os.path.exists("userdata"):
            os.mkdir("userdata")
        if os.path.exists("userdata/opcconfig.csv"):
            csvdatas = load_csv('userdata/opcconfig.csv')
            if csvdatas:
                self.start_opctunnel(csvdatas)
        self._opcdaclient = OpenOPC.client()
        if self._opcConfig:
            try:
                self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
            except Exception as ex:
                logging.warning('connect OPCDA Server err!err!err!')
                logging.exception(ex)
                # print(str(ex))
                self._mqttpub.opcdabrg_log_pub('x1x1', str(ex))
        while not self._thread_stop:
            if not self._opctunnel_isrunning:
                time.sleep(1)
                continue

    def stop(self):
        self._thread_stop = True
        self.join()
