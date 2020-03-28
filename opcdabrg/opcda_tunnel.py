#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import logging
import time
import os
import json
import decimal
import re
from datetime import datetime
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
		self._opcConfig = {}
		self._opcdaclient = None
		self._timeInterval = 1
		self._isReading = False
		self._opctunnel_isrunning = False
		self._count = 0
		self._opcUtctimeFmt = False
		self._rtdata = None
		self.mqtt_clientid = None
		self._thread_stop = False

	def timestr2utc(self, time_str):
		result = re.split(r'[+]', time_str)
		return result[0]

	def timestr2timestamp(self, time_str):
		local_tm = datetime.fromtimestamp(0)
		utc_tm = datetime.utcfromtimestamp(0)
		offset = local_tm - utc_tm
		result = re.split(r'[+]', time_str)
		if result[0].find('.') != -1:
			utc_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
		else:
			utc_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
		utc_date = utc_date + offset
		return utc_date.timestamp()

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
		# print("clean end::", self._opctunnel_isrunning, self._opcConfig, self._isReading)
		return True

	def opcdaclient_isconnected(self):
		return self._opcdaclient.isconnected

	def brg_isrunning(self):
		return {"brg_status": self._opctunnel_isrunning}

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
								newtimestr = self.timestr2timestamp(ld[-1])
								del(ld[-1])
								ld.append(newtimestr)
								newdatas.append(ld)
						self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(newdatas, cls=DecimalEncoder))
						self._rtdata = newdatas
					else:
						self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(datas, cls=DecimalEncoder))
				except Exception as ex:
					logging.warning("read item's data err!err!err!")
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
					self._mqttpub.opcdabrg_datas(self.mqtt_clientid, json.dumps(uncertaindata, cls=DecimalEncoder))
					self._rtdata = None
				time.sleep(0.1)
				self._opcdaclient = OpenOPC.client()
				try:
					logging.info(str(self._count) + ": reconnect " + self._opcConfig.get('opcname') + self._opcConfig.get('opchost'))
					self._opcdaclient.connect(self._opcConfig.get('opcname'), self._opcConfig.get('opchost') or 'localhost')
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', 'connect ' + self._opcConfig.get('opcname') + ' successful']) )
				except Exception as ex:
					logging.warning('connect OPCDA Server err!err!err!')
					logging.exception(ex)
					self._mqttpub.opcdabrg_comm_pub(self.mqtt_clientid, json.dumps([int(time.time()), 'link', str(ex)]))
					time.sleep(1 + 5 * self._count)
					self._count = self._count + 1
				finally:
					if self._opcConfig.get('timeInterval'):
						self._timeInterval = self._opcConfig.get('timeInterval')

	def stop(self):
		self._thread_stop = True
		self.join()
