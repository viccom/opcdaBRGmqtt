#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import opcdabrg.OpenOPC as OpenOPC
import csv
import random


def load_csv(path):
	opcconfig = {}
	tags = []
	items = []
	with open(path, 'r') as csvFile:
		# 读取csv文件,返回的是迭代类型
		reader = csv.reader(csvFile)
		for i, item in enumerate(reader):
			if i == 0 and item[0].lower() != "opcname":
				logging.warning("CSV file's line 1 format is not correct!")
				return None
			elif i == 1:
				opcconfig['opcname'] = item[0]
				opcconfig['opchost'] = item[1]
				opcconfig['clientid'] = item[2]
			elif i > 2:
				tags.append(item)
				items.append(item[2].strip())
	csvFile.close()
	opcconfig['opctags'] = tags
	opcconfig['opcitems'] = items
	return opcconfig


def save_csv(path, configdatas):
	headers = ['OPCNAME', 'OPCHOST', 'CLIENTID']
	csv_datas = []
	csv_datas.append(headers)
	csv_datas.append([configdatas['opcname'], configdatas['opchost'], configdatas['clientid']])
	tagheaders = ['tagname', 'datatype', 'opcitem']
	csv_datas.append(tagheaders)
	for v in configdatas['opctags']:
		csv_datas.append(v)
	with open(path, 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(csv_datas)
	return True


def list_OPCServers(opchost):
	opc = OpenOPC.client()
	_ServersList = opc.servers(opc_host=opchost)
	opc.close()
	return _ServersList

def opcInfo(opcdaserv, opchost):
	opc = OpenOPC.client()
	opc.connect(opcdaserv, opc_host=opchost)
	opcinfo = opc.info()
	opc.close()
	return opcinfo


def opcTagsList(opcdaserv, opchost):
	opc = OpenOPC.client()
	print(opchost)
	opc.connect(opcdaserv, opc_host=opchost)
	TagsList = None
	if opc.isconnected:
		TagsList = opc.list('*', flat=True)
	opc.close()
	return TagsList


def opcReadItem(client, items):
	v = client.read(items, sync=True)
	return v


def opcWriteItem(opcdaserv, opchost, item, value):
	opc = OpenOPC.client()
	opc.connect(opcdaserv, opc_host=opchost)
	ret = opc.write((item, value))
	opc.close()
	return ret
