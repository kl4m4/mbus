from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging
import configparser
import sys
from lib_mbtcplogger import cConfReader

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

if len(sys.argv)<2:
    log.debug("no config file!")
    exit()
else:
    log.debug("reading ini file: {0}".format(sys.argv[1]))

confreader = cConfReader(sys.argv[1])
confreader.Parse()