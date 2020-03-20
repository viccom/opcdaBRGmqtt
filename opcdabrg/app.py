#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
from opcdabrg.mqtt_pub import MQTTStreamPub
from opcdabrg.manager import OPCDABRGManager
from opcdabrg.service import OPCDABRG_Service
from opcdabrg.admin import opcdabrg_admin
import time


def init():
    stream_pub = MQTTStreamPub()
    logging.info("Staring mqtt opcdabrg publisher..")
    stream_pub.start()
    time.sleep(2)

    manager = OPCDABRGManager(stream_pub)
    logging.info("Staring opcdabrg manager..")
    manager.start()

    service = OPCDABRG_Service(manager)
    logging.info("Staring opcdabrg service..")
    service.start()

    return opcdabrg_admin, service
