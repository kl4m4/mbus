from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import configparser
import sys
from lib_mbtcplogger import cTag
from lib_mbtcplogger import MBTag
from lib_mbtcplogger import TimestampTag
from lib_mbtcplogger import MBInterface
from lib_mbtcplogger import IndexTag
from lib_mbtcplogger import cConfReader
from lib_mbtcplogger import Logger
import logging
import time

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

if len(sys.argv)<2:
    log.debug("no config file!")
    exit()
else:
    log.debug("reading ini file: {0}".format(sys.argv[1]))

conf = cConfReader(sys.argv[1])
conf.Parse()

mb = MBInterface()
for tag in conf.getTagsList():
    if isinstance(tag, MBTag):
        tag.attachToMBInterface(mb)

logger = Logger(conf.poll_interval_ms, conf.getTagsList(), conf.delimiter_char)
#print(logger.ExecutePoll())
logger.Loop()
    