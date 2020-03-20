import OpenOPCDA.OpenOPC as OpenOPC
import random

def opcTagsList(opcdaserv, node=None):
   opc = OpenOPC.client()
   opc.connect(opcdaserv)
   TagsList = opc.list(node)
   opc.close()
   print('TagsList:: ', TagsList)
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
   opcdaserv = 'zzzz.Simulator.1'
   nodename = 'numeric.sin'
   taglist = ['Random.Int1', 'Random.Int2', 'Random.Real4']
   try:
      opc = OpenOPC.client()
      opc.connect(opcdaserv)
      print(dir(opc))
   except Exception as ex:
      print('err!err!err!err!')
      print(ex)
   print(opc.isconnected)
   # if opcdaserv in opcservers:
   #    opcInfo(opcdaserv)
      # opcTagsList(opcdaserv, nodename)
      # opcReadItem(opcdaserv, opcTagsList(opcdaserv, nodename), 1)
      # opcWriteItem(opcdaserv, 'Bucket Brigade.Int2', random.randint(1, 100))
