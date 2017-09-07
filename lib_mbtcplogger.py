import logging
import configparser
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import datetime

class cTag(object):
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.nextTag = None
    def retrieveValue(self):
        raise NotImplementedError("Subclasses should implement this!")
    def selfConfig(self, configfile):
        raise NotImplementedError("Subclasses should implement this!")

class MBTag(cTag):
    def __init__(self, tag_name):
        logging.debug("MBTag __init__")
        self.tag_name = tag_name
        self.tag_desc = None
        self.ip = None
        self.port = None
        self.unit = None
        self.method = None
        self.offset = None
    def retrieveValue(self):
        logging.debug("MBTag retrieveValue")
        return self.mb_interface.Query(self.ip, self.port, self.unit, self.method, self.offset)
    def selfConfig(self, configfile):
        logging.debug("MBTag selfConfig")
        config = configparser.ConfigParser()
        config.read(configfile)
        self.tag_desc = config[self.tag_name]['tag_desc']
        self.ip = config[self.tag_name]['slave_ip']
        self.port = config[self.tag_name]['slave_port']
        self.unit = config[self.tag_name]['slave_unit']
        self.method = config[self.tag_name]['method']
        self.offset = config[self.tag_name]['address']
    def attachToMBInterface(self, mb_interface):
        logging.debug("MBTag attachToMBInterface")
        self.mb_interface = mb_interface
    def __str__(self):
        return "{0}:{1} unit={2} type={3} offset={4} name={5} desc={6}".format(self.ip, self.port, self.unit, self.method, self.offset, self.tag_name, self.tag_desc)

          
class TimestampTag(cTag):
    def __init__(self, tag_name):
        logging.debug("TimestampTag __init__")
        cTag.__init__(self, tag_name);
    def retrieveValue(self):
        logging.debug("TimestampTag retrieveValue")
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    def selfConfig(self, configfile):
        logging.debug("TimestampTag selfConfig")
        pass
    def __str__(self):
        return "TimestampTag"

class IndexTag(cTag):
    def __init__(self, tag_name):
        logging.debug("IndexTag __init__")
        cTag.__init__(self, tag_name);
        self.counter = 0
    def retrieveValue(self):
        logging.debug("IndexTag retrieveValue")
        self.counter = self.counter + 1
        return self.counter
    def resetCounter(self):
        logging.debug("IndexTag resetCounter")
        self.counter = 0
    def selfConfig(self, configfile):
        logging.debug("IndexTag selfConfig")
        pass
    def __str__(self):
        return "IndexTag"
    
class MBInterface(ModbusClient):
    def __init__(self):
        logging.debug("MBInterface __init__")
        self.clientslist = []
    def Query(self, ip, port, unit, querytype, address):
        logging.debug("MBInterface Query")
        #print("Zapytanie modbusowe do {0}:{1} unit={2} type={3} address={4}".format(ip, port, unit, querytype, address))
        got_it = False
        client_to_use = None
        for cl in self.clientslist:
            if cl.host == ip:
                # uzyj tego obiektu klienta
                logging.debug("MBInterface Query - host already known")
                got_it = True
                client_to_use = cl
        if got_it == False:
            logging.debug("MBInterface Query - host used for first time")
            client_to_use = ModbusClient(ip,port)
            self.clientslist.append(client_to_use)
        logging.debug("MBInterface Query - assembling query: {0}:{1} unit={2} type={3} address={4}".format(client_to_use.host, client_to_use.port, unit, querytype, address))
        logging.debug("TODO: actual query request!!!!!!")
        return 234.5


class cConfReader(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.tagslist = []
        self.config = configparser.ConfigParser()
        self.config.read(filepath)
        logging.basicConfig()
        log = logging.getLogger()
        log.debug("cConfReader __init__()")
        
        try:
            self.config.defaults()['tags_list']
        except:
            log.debug("ini file error")
            exit()
        log.debug("ini file read")
        
    def Parse(self):
        logging.basicConfig()
        log = logging.getLogger()
        log.debug("cConfReader Parse()")
        # read DEFAULT -> tags_list
        for tag in self.config.defaults()['tags_list'].split(','):
            tag_name = tag.strip()
            source_type = self.config[tag_name]['tag_source']
            
            if source_type == 'timestamp':
                tmp = TimestampTag(tag_name)
            elif source_type == 'pollindex':
                tmp = IndexTag(tag_name)
            elif source_type == 'modbustcp':
                tmp = MBTag(tag_name)
                
            tmp.selfConfig(self.filepath)
            self.tagslist.append(tmp)
            
    def getTagsList(self):
        return self.tagslist