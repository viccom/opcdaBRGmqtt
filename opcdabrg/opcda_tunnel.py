#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import logging
import time
import os
import json
import decimal
import re
from opcdabrg.opcda import *
from dateutil.parser import parse
from configparser import ConfigParser

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
		self._opcConfig = {}
		self._opcdaclient = None
		self._timeInterval = 1
		self._timezone = '+00:00'
		self._isReading = False
		self._opctunnel_isrunning = False
		self._count = 0
		self._opcUtctimeFmt = False
		self._rtdata = None
		self.mqtt_clientid = None
		self._thread_stop = False

	def get_opcConfig(self):
		return self._opcConfig

	def start_opctunnel(self, opcConfig):
		if self._opcdaclient.isconnected:
			logging.info("1. _opcdaclient is linked!")
			self._opcdaclient.close()
			logging.warning("2. close _opcdaclient!")
		else:
			logging.warning("3. _opcdaclient has closed!")
		self._opcConfig = opcConfig
		self.mqtt_clientid = opcConfig.get('clientid')
		if opcConfig.get('timeInterval'):
			if int(self._opcConfig.get('timeInterval')) > 0:
				self._timeInterval = int(self._opcConfig.get('timeInterval'))
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
				self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'write', self._opcConfig.get('opcname') + '/' + json.dumps(tags_values) + '/' + str(retw)]))
				return retw
			except Exception as ex:
				logging.warning('Write Item err!err!err!')
				self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'write', self._opcConfig.get('opcname') + '/' + json.dumps(tags_values) + '/' + str(ex)]))
				logging.exception(ex)
				opcClient.close()
			finally:
				opcClient.close()
		else:
			return None

	def opctunnel_pause(self):
		self._opctunnel_isrunning = False
		return {"brg_status": self._opctunnel_isrunning}

	def opctunnel_resume(self):
		self._opctunnel_isrunning = True
		return {"brg_status": self._opctunnel_isrunning}

	def opctunnel_clean(self):
		# print("clean::", self._opctunnel_isrunning, len(self._opcConfig), self._isReading)
		while self._isReading:
			# logging.info('wait clean')
			time.sleep(1)
		self._opctunnel_isrunning = False
		self._opcConfig = {}
		self.mqtt_clientid = None
		if self._opcdaclient and self._opcdaclient.isconnected:
			logging.info("opcdaclient closing!")
			self._opcdaclient.close()
		logging.info("opctunnel has cleaned!")
		if os.path.exists("userdata/opcconfig.csv"):
			os.remove("userdata/opcconfig.csv")
		# print("clean end::", self._opctunnel_isrunning, self._opcConfig, self._isReading)
		return True

	def opcdaclient_isconnected(self):
		return self._opcdaclient.isconnected

	def brg_isrunning(self):
		return {"brg_status": self._opctunnel_isrunning}

	def get_timezone(self):
		config = ConfigParser()
		if os.access(os.getcwd() + '\\config.ini', os.F_OK):
			config.read('config.ini')
			if config.getint('system', 'timezone_offset'):
				timezone_offset = config.getint('system', 'timezone_offset')
		return timezone_map.get(str(timezone_offset))

	def run(self):
		self._opcdaclient = OpenOPC.client()
		if self.get_timezone():
			self._timezone = self.get_timezone()
		if not os.path.exists("userdata"):
			os.mkdir("userdata")
		if os.path.exists("userdata/opcconfig.csv"):
			csvdatas = load_csv('userdata/opcconfig.csv')
			if csvdatas:
				self.start_opctunnel(csvdatas)
				logging.info('start opctunnel with opcconfig.csv')
			else:
				logging.info('start opctunnel without opcconfig')
		if self._opcConfig:
			try:
				self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']))
				self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']))
			except Exception as ex:
				logging.warning('connect OPCDA Server err!err!err!')
				logging.exception(ex)
				self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', self._opcConfig.get('opcname') + str(ex)]))
				self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', self._opcConfig.get('opcname') + str(ex)]))
			finally:
				if self._opcConfig.get('timeInterval'):
					if int(self._opcConfig.get('timeInterval')) > 0:
						self._timeInterval = int(self._opcConfig.get('timeInterval'))
				pass
				# print(self._opcConfig.get('opcname'), self._opcConfig.get('opcitems'))
		while not self._thread_stop:
			if self._opcdaclient.isconnected is True:
				self._mqttpub.opcdabrg_status(self.mqtt_clientid, json.dumps([int(time.time()), 'status', "online"]))
			else:
				self._mqttpub.opcdabrg_status(self.mqtt_clientid,
				                              json.dumps([int(time.time()), 'status', 'offline']))
			# print(self._opctunnel_isrunning, len(self._opcConfig), self._isReading)
			if not self._opctunnel_isrunning or not self._opcConfig:
				# print("idle!")
				time.sleep(1)
				continue
			# else:
			# 	self._isReading = True
			# 	print("busy!")
			# 	time.sleep(5)
			# 	self._isReading = False
			elif self._opcdaclient.isconnected:
				self._count = 0
				try:
					# print('opcitems::', self._opcConfig.get('opcitems'))
					self._isReading = True
					datas = self._opcdaclient.read(self._opcConfig.get('opcitems'), sync=True)
					# print('datas::', json.dumps(datas, cls=DecimalEncoder))
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'read', self._opcConfig.get('opcname') + '/Success']))
					if not self._opcUtctimeFmt:
						newdatas = []
						for data in datas:
							if data:
								ld = list(data)
								newtimestamp = parse(ld[-1].replace('+00:00', self._timezone)).timestamp()
								newvalue = ld[1]
								if type(newvalue) == memoryview:
									newvalue = str(newvalue.tobytes(), encoding='gbk', errors='ignore')
								if type(newvalue) == bytes:
									newvalue = str(newvalue, encoding='gbk', errors='ignore')
								newdatal = [ld[0], newvalue, ld[2], newtimestamp]
								newdatas.append(newdatal)
						try:
							self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(newdatas, cls=DecimalEncoder))
						except Exception as ex:
							logging.error("json datas err!err!err!")
							logging.exception(ex)
						self._rtdata = newdatas
					else:
						try:
							self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(datas, cls=DecimalEncoder))
						except Exception as ex:
							logging.error("json datas err!err!err!")
							logging.exception(ex)
						self._rtdata = datas
				except Exception as ex:
					logging.error("read item's data err!err!err!")
					logging.exception(ex)
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'read', self._opcConfig.get('opcname') + '/' + str(ex)]))
					self._opcdaclient.close()
				finally:
					self._isReading = False
					time.sleep(self._timeInterval)
			else:
				if self._rtdata:
					uncertaindata = []
					for data in self._rtdata:
						newdata = [data[0], data[1], 'uncertain', data[3]]
						uncertaindata.append(newdata)
					try:
						self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(uncertaindata, cls=DecimalEncoder))
					except Exception as ex:
						logging.exception(ex)
					self._rtdata = None
				time.sleep(0.1)
				self._opcdaclient = OpenOPC.client()
				try:
					logging.info(str(self._count) + ": reconnect " + self._opcConfig.get('opcname') + self._opcConfig.get('opchost'))
					self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
					self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']) )
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']) )
				except Exception as ex:
					logging.error('connect OPCDA Server err!err!err!')
					logging.exception(ex)
					self._mqttpub.opcdabrg_log_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', self._opcConfig.get('opcname') + str(ex)]))
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', self._opcConfig.get('opcname') + str(ex)]))
					time.sleep(1 + 5 * self._count)
					self._count = self._count + 1
				finally:
					if self._opcConfig.get('timeInterval'):
						if int(self._opcConfig.get('timeInterval')) > 0:
							self._timeInterval = int(self._opcConfig.get('timeInterval'))
		logging.warning("Close opcdatunnel!")

	def stop(self):
		self._thread_stop = True
		self.join()
