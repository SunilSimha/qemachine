# test space for poking the IMC17 step motor that controls the bellows

import socket

bellows_port = ('128.114.17.188', 10001)
setup_port = ('128.114.17.188', 9999)

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# s.bind(('128.114.17.188', 10001))  # didn't work
# bind() is for setting up server ports, not connecting

s.connect(('128.114.17.188', 10001))  # worked


s.gettimeout()

