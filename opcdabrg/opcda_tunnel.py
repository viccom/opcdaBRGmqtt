#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import logging
import time
import os
import re
from opcdabrg.opcda import *

class OPCDATunnel(threading.Thread):
	def __init__(self, manager):
		threading.Thread.__init__(self)
		self._manager = manager
		self._opctunnel_isrunning = False
		self._opcConfig = None
		self.opcda_name = None
		self.opcda_host = None
		self.opcda_tags = None
		self.mqtt_clientid = None
		self._thread_stop = False

	def get_opcConfig(self):
		return self._opcConfig

	def start_opctunnel(self, opcConfig):
		self._opcConfig = opcConfig
		self.opcda_name = opcConfig.get('opcname')
		self.opcda_host = opcConfig.get('opchost')
		self.opcda_tags = opcConfig.get('opctags')
		self.mqtt_clientid = opcConfig.get('clientid')
		self._opctunnel_isrunning = True

	def get_opcDatas(self):
		opcClient = OpenOPC.client()
		try:
			opcClient.connect(self.pcda_name, self.opcda_host)
		except Exception as ex:
			logging.warning('connect OPCDA Server err!err!err!')
			logging.exception(ex)
		if opcClient.isconnected:
			try:
				datas = opcClient.read(self.opcda_tags, sync=True)
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

	def opctunnel_pause(self):
		self._opctunnel_isrunning = False
		return True

	def opctunnel_resume(self):
		self._opctunnel_isrunning = True
		return True

	def opctunnel_clean(self):
		self._opctunnel_isrunning = None
		self._opcConfig = None
		return self._opctunnel_isrunning

	def opctunnel_isrunning(self):
		return self._opctunnel_isrunning

	def run(self):
		while not self._thread_stop:
			if not self._opctunnel_isrunning:
				time.sleep(1)
				continue
			self._opctunnel_isrunning = False

	def stop(self):
		self._thread_stop = True
		self.join()
