import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp, hooks

def on_after_recv(data):
    master, bytes_data = data
    print(bytes_data)

hooks.install_hook('modbus.Master.after_recv', on_after_recv)
print("a")
try:
    def on_before_connect(args):
        master = args[0]
        print("on_before_connect", master._host, master._port)

    hooks.install_hook("modbus_tcp.TcpMaster.before_connect", on_before_connect)

    def on_after_recv(args):
        response = args[1]
        print("on_after_recv", len(response), "bytes received")

    hooks.install_hook("modbus_tcp.TcpMaster.after_recv", on_after_recv)

    # Connect to the slave
    master = modbus_tcp.TcpMaster()
    master.set_timeout(5.0)

    print("aaa")
    print(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 3))
    while True:
        tmp = 1+1
        
except modbus_tk.modbus.ModbusError as exc:
        logger.error("%s- Code=%d", exc, exc.get_exception_code())
        