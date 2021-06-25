from network import Sigfox
import socket

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

data=50.20
battery= 2035


data_in_int= int(data)
batt_data_in_int= int(battery)
data_in_bytes = data_in_int.to_bytes(2,'big')
batt_data_in_bytes = batt_data_in_int.to_bytes(2,'big')

# send some bytes
s.send(data_in_bytes+batt_data_in_bytes)