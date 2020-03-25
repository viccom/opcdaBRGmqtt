#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import logging
import time
import os
import json
import decimal
from opcdabrg.opcda import *

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

class OPCDATunnel(threading.Thread):
	def __init__(self, mqttpub):
		threading.Thread.__init__(self)
		self._mqttpub = mqttpub
		self._opctunnel_isrunning = False
		self._opcConfig = None
		self._opcdaclient = None
		self._timeInterval = 1
		self._count = 0
		self.mqtt_clientid = None
		self._thread_stop = False

	def get_opcConfig(self):
		return self._opcConfig

	def start_opctunnel(self, opcConfig):
		if self._opcdaclient.isconnected:
			logging.info("1. _opcdaclient is linked:: ", self._opcdaclient.isconnected)
			self._opcdaclient.close()
			logging.warning("2. close _opcdaclient:: ", self._opcdaclient.isconnected)
		else:
			logging.warning("3. _opcdaclient is closed:: ")
		self._opcConfig = opcConfig
		self.mqtt_clientid = opcConfig.get('clientid')
		save_csv('userdata/opcconfig.csv', self._opcConfig)
		self._opctunnel_isrunning = True
		self._count = 0
		return True

	def get_opcDatas(self):
		opcClient = OpenOPC.client()
		try:
			opcClient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
		except Exception as ex:
			logging.warning('connect OPCDA Server err!err!err!')
			logging.exception(ex)
		if opcClient.isconnected:
			try:
				datas = opcClient.read(self._opcConfig.get('opcitems'), sync=True)
				return datas
			except Exception as ex:
				logging.warning('readItem err!err!err!')
				logging.exception(ex)
				opcClient.close()
			finally:
				opcClient.close()
		else:
			return None

	def set_opcDatas(self, tags_values):
		opcClient = OpenOPC.client()
		try:
			opcClient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
		except Exception as ex:
			logging.warning('connect OPCDA Server err!err!err!')
			logging.exception(ex)
		if opcClient.isconnected:
			try:
				retw = opcClient.write(tags_values)
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'write', str(retw)]))
				return retw
			except Exception as ex:
				logging.warning('Write Item err!err!err!')
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'write', str(ex)]))
				logging.exception(ex)
				opcClient.close()
			finally:
				opcClient.close()
		else:
			return None

	def opctunnel_pause(self):
		self._opctunnel_isrunning = False
		return True

	def opctunnel_resume(self):
		self._opctunnel_isrunning = True
		return True

	def opctunnel_clean(self):
		if self._opcdaclient and self._opcdaclient.isconnected:
			logging.info("opcdaclient closing!")
			self._opcdaclient.close()
		self._opctunnel_isrunning = None
		self._opcConfig = None
		logging.info("opctunnel has cleaned!")
		return True

	def opctunnel_isrunning(self):
		return self._opcdaclient.isconnected

	def run(self):
		self._opcdaclient = OpenOPC.client()
		if not os.path.exists("userdata"):
			os.mkdir("userdata")
		if os.path.exists("userdata/opcconfig.csv"):
			csvdatas = load_csv('userdata/opcconfig.csv')
			if csvdatas:
				self.start_opctunnel(csvdatas)
				logging.info('start opctunnel with opcconfig.csv')
		if self._opcConfig:
			try:
				self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']))
			except Exception as ex:
				logging.warning('connect OPCDA Server err!err!err!')
				logging.exception(ex)
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', str(ex)]))
			finally:
				if self._opcConfig.get('timeInterval'):
					self._timeInterval = self._opcConfig.get('timeInterval')
				pass
				# print(self._opcConfig.get('opcname'), self._opcConfig.get('opcitems'))
		while not self._thread_stop:
			self._mqttpub.opcdabrg_status(self.mqtt_clientid, json.dumps([int(time.time()), 'status', self._opcdaclient.isconnected]))
			if not self._opctunnel_isrunning:
				time.sleep(1)
				continue
			elif self._opcdaclient.isconnected:
				self._count = 0
				try:
					# print('opcitems::', self._opcConfig.get('opcitems'))
					datas = self._opcdaclient.read(self._opcConfig.get('opcitems'), sync=True)
					# print('datas::', json.dumps(datas, cls=DecimalEncoder))
					self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(datas, cls=DecimalEncoder))
				except Exception as ex:
					logging.warning("read item's data err!err!err!")
					logging.exception(ex)
					self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'read', str(ex)]))
					self._opcdaclient.close()
				finally:
					time.sleep(self._timeInterval)
			else:
				time.sleep(0.1)
				self._opcdaclient = OpenOPC.client()
				try:
					print(self._count, self._opcConfig.get('opcname'), self._opcConfig.get('opchost'))
					self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
					self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']) )
				except Exception as ex:
					logging.warning('connect OPCDA Server err!err!err!')
					logging.exception(ex)
					self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', str(ex)]))
					time.sleep(1 + 5 * self._count)
					self._count = self._count + 1
				finally:
					if self._opcConfig.get('timeInterval'):
						self._timeInterval = self._opcConfig.get('timeInterval')

	def stop(self):
		self._thread_stop = True
		self.join()
