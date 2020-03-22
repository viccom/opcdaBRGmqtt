import OpenOPCDA.OpenOPC as OpenOPC
import random


def opcTagsList(opcdaserv):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	TagsList = opc.list(flat=True)
	opc.close()
	return TagsList


def opcReadItem(opcdaserv, items, interval=1):
	from time import sleep
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	# opc.read(items, group='group1')
	print("start read items::")
	while True:
		v = opc.read(items, sync=True)
		# print(v)
		for i in range(len(v)):
			if len(v[i]) == 4:
				(name, val, qual, time,) = v[i]
				print('% -30s % -30s % -10s % -20s' % (name, val, qual, time))
			if len(v[i]) == 5:
				(name, val, qual, time, error) = v[i]
				print('% -30s % -30s % -10s % -20s % -20s' % (name, val, qual, time, error))
		sleep(interval)


def opcWriteItem(opcdaserv, item, value):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	print(opc.write((item, value)))
	opc.close()


def opcServersList():
	opc = OpenOPC.client()
	ServersList = opc.servers()
	opc.close()
	print('opcServersList:: ', ServersList)
	return ServersList


def opcInfo(opcdaserv):
	opc = OpenOPC.client()
	opc.connect(opcdaserv)
	print('opcInfo:: ', opc.info())
	opc.close()


if __name__ == '__main__':
	opcservers = opcServersList()
	opcdaserv = 'Matrikon.OPC.Simulation.1'
	nodename = 'numeric.sin'
	taglist = ['Random.Int1', 'Random.Int2', 'Random.Real4']
	try:
		opc = OpenOPC.client()
		opc.connect(opcdaserv)
		# print(dir(opc))
	except Exception as ex:
		print('err!err!err!err!')
		print(ex)
	finally:
		print(opc.isconnected)
		items_flat = opc.list('Simulation Items.Random', flat=True)
		# rp = opc.properties('Random.Int4')
		# print(rp)
		for item in items_flat:
			print(item)

		# r = opc.list()
		# print(type(r))
		# for v in r:
		# 	print(v)
		# 	itemP = None
		# 	try:
		# 		itemP = opc.properties(v)
		# 	except Exception as ex:
		# 		pass
		# 	finally:
		# 		if not itemP:
		# 			ret = opc.list(v)
		# 			if ret:
		# 				for val in ret:
		# 					itempp = None
		# 					try:
		# 						itempp = opc.properties(val)
		# 					except Exception as ex:
		# 						pass
		# 					finally:
		# 						if itempp:
		# 							print(itempp)
		# 						else:
		# 							r2 = opc.list(v + '.' + val)
		# 							if r2:
		# 								print(r2)
		# 		else:
		# 			print(itemP)
	# if opcdaserv in opcservers:
	#    opcInfo(opcdaserv)
	# opcTagsList(opcdaserv, nodename)
	# opcReadItem(opcdaserv, opcTagsList(opcdaserv, nodename), 1)
	# opcWriteItem(opcdaserv, 'Bucket Brigade.Int2', random.randint(1, 100))
