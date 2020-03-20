#!/usr/bin/python
# -*- coding: UTF-8 -*-

import OpenOPCDA.OpenOPC as OpenOPC
import random


def opcServersList():
   opc = OpenOPC.client()
   ServersList = opc.servers()
   opc.close()
   # print('opcServersList:: ', ServersList)
   return ServersList



def opcInfo(opcdaserv):
   opc = OpenOPC.client()
   opc.connect(opcdaserv)
   # print('opcInfo:: ', opc.info())
   opc.close()


def opcTagsList(opcdaserv, node=None):
   opc = OpenOPC.client()
   opc.connect(opcdaserv)
   TagsList = opc.list(node)
   opc.close()
   # print('TagsList:: ', TagsList)
   return TagsList


def opcReadItem(client, items):
   v = client.read(items, sync=True)
   return v
   # from time import sleep
   # opc.read(items, group='group1')
   # print("start read items::")
   # while True:
   #    v = opc.read(items, sync=True)
   #    # print(v)
   #    for i in range(len(v)):
   #       if len(v[i]) == 4:
   #          (name, val, qual, time,) = v[i]
   #          print('% -30s % -30s % -10s % -20s' % (name, val, qual, time))
   #       if len(v[i]) == 5:
   #          (name, val, qual, time, error) = v[i]
   #          print('% -30s % -30s % -10s % -20s % -20s' % (name, val, qual, time, error))
   #    sleep(1)

def opcWriteItem(opcdaserv, item, value):
   opc = OpenOPC.client()
   opc.connect(opcdaserv)
   # print(opc.write((item, value)))
   opc.close()
