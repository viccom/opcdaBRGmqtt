#!/usr/bin/python
# -*- coding: UTF-8 -*-

import OpenOPCDA.OpenOPC as OpenOPC
import csv
import random


def load_csv(path):
	opcconfig = {}
	tags = []
	with open(path, 'r') as csvFile:
		# 读取csv文件,返回的是迭代类型
		reader = csv.reader(csvFile)
		for i, item in enumerate(reader):
			if i == 0 and item[0].lower() != "opcname":
				print("CSV file's line 1 format is not correct!")
				return None
			elif i == 1:
				opcconfig['opcname'] = item[0]
				opcconfig['opchost'] = item[1]
				opcconfig['clientid'] = item[2]
			elif i > 2:
				tags.append(item)
	csvFile.close()
	opcconfig['opctags'] = tags
	return opcconfig


def save_csv(path, opcconfig):
	headers = ['OPCNAME', 'OPCHOST', 'CLIENTID']
	csv_datas = []
	csv_datas.append(headers)
	csv_datas.append([opcconfig['opcname'], opcconfig['opchost'], opcconfig['clientid']])
	tagheaders = ['tagname', 'datatype', 'opcitem']
	csv_datas.append(tagheaders)
	csv_datas.append(opcconfig['opctags'])
	with open('_Modbus点表.csv', 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(csv_datas)
	return True


def opcServersList():
	opc = OpenOPC.client()
	ServersList = opc.servers()
	opc.close()
	return ServersList


def opcInfo(opcdaserv):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	opcinfo = opc.info()
	opc.close()
	return opcinfo


def opcTagsList(opcdaserv, node=None):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	TagsList = opc.list(node)
	opc.close()
	return TagsList


def opcReadItem(client, items):
	v = client.read(items, sync=True)
	return v


def opcWriteItem(opcdaserv, item, value):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	# print(opc.write((item, value)))
	opc.close()
