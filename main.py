import logging
import os
import sys
import time
import importlib
from hbmqtt_broker import MQTTBroker
from admin import start_admin
from helper import _dict
from configparser import ConfigParser
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import webbrowser

serivces = [
    'opcdabrg'
]

blueprints = []
context = _dict({})


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    if sys.argv[0] != os.path.split(os.path.realpath(__file__))[1]:
        if os.path.split(sys.argv[0])[0]:
            os.chdir(os.path.split(sys.argv[0])[0])
    log_level = 'INFO'
    log_filenum = 9
    log_maxsize = 4
    config = ConfigParser()
    if os.access(os.getcwd() + '\\config.ini', os.F_OK):
        config.read('config.ini')
        if config.get('log', 'level'):
            log_level = config.get('log', 'level')
        if config.get('log', 'filenum'):
            log_filenum = int(config.get('log', 'filenum'))
        if config.get('log', 'maxsize'):
            log_maxsize = int(config.get('log', 'maxsize'))
    else:
        config.read('config.ini')
        config.add_section("log")
        config.set("log", 'level', 'INFO')
        config.set("log", 'filenum', '9')
        config.set("log", 'maxsize', '4')
        config.write(open('config.ini', 'w'))
    level = logging.getLevelName(log_level)
    logging.basicConfig(level=level, format=formatter)
    if not os.path.exists("log"):
        os.mkdir("log")

    log = logging.getLogger()
    # 输出到文件
    fh = RotatingFileHandler('./log/log.log', mode='a+', maxBytes=log_maxsize * 1024 * 1024, backupCount=log_filenum, delay=True)
    fh.setFormatter(logging.Formatter(formatter))
    log.addHandler(fh)

    logging.info("当前工作路径：" + str(os.getcwd()))

    broker = MQTTBroker()
    logging.info("Staring hbmqtt broker..")
    broker.start()
    time.sleep(1)

    for m in serivces:
        service_module = importlib.import_module('{0}.app'.format(m))
        blueprint, service = service_module.init()
        blueprints.append(blueprint)
        service_name = "{0}_service".format(m)
        context[service_name] = service
        time.sleep(1)

    logging.info("Staring Admin!!")
    # webbrowser.open("http://localhost:3080")
    start_admin(blueprints, context)
    logging.info("CLOSING!!")
