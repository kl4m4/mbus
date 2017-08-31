import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

server = modbus_tcp.Server()
server.start()
slave1 = server.add_slave(1)
slave1.add_block('0', cst.HOLDING_REGISTERS, 0, 10)
slave1.set_values('0', 0, 1.0)
slave1.set_values('0', 1, 1.1)
slave1.set_values('0', 2, 1.2)
slave1.set_values('0', 3, 1.3)
slave1.set_values('0', 4, 1.4)
slave1.set_values('0', 5, 1.5)
slave1.set_values('0', 6, 1.6)
slave1.set_values('0', 7, 1.7)
slave1.set_values('0', 8, 1.8)

while True:
    tmp = 1+1