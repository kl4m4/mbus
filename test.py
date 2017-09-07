from lib_mbtcplogger import cTag
from lib_mbtcplogger import MBTag
from lib_mbtcplogger import TimestampTag
from lib_mbtcplogger import MBInterface
from lib_mbtcplogger import IndexTag
from lib_mbtcplogger import cConfReader
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('Program start')

mb = MBInterface()


conf = cConfReader('jobconfig.ini')
conf.Parse()



for tag in conf.getTagsList():
    #print(tag)
    if isinstance(tag, MBTag):
        tag.attachToMBInterface(mb)

for tag in conf.getTagsList():
    print(tag.retrieveValue())

