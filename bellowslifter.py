# test space for poking the IMC17 step motor that controls the bellows
"""

"""
import socket

# transliteration of the tkl code
def readbytes(fd):
    # This procedure is called as a fileevent when there are characters
    # to read on the bellows lifter serial port.
    
    if fd=='':
        return 1
    # from there the code adds the value to a global variable
    # ewwwww
    return 0

def StatusDecode(status):
    status_dict = {
            0: 'OK'
            1: 'INIT_ERROR'
            2: 'BAD_COMMAND'
            3: 'OUT_OF_RANGE'
            7: 'OVERLOAD'
        }
    # return status translation, or UNKNOWN if not found
    return status_dict.get(status, 'UNKNOWN_STATUS_%i' %status)


def sendmsg(msg):
    readyw = 0
    while(port['ready'] == 0):
        send_querymsg '/1?0'
        position = readposition()
        if port['status'] != 'OK':
            # log an error
        if port['ready'] == 0:
            readyw += 1
            if readyw >= 3:
                # error code log here
                rbuf = Timeout
                pause(20)
    # log message
    # clear recieve buffers
    # send message
    # clear output buffer?
    return





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

