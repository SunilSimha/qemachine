

import socket
import re
from time import sleep

class TungstenLamp:
    # tcl version is tungstenlamp.tcl.sin
    # main control code in tcl version is the function SetWLamp
    # SetWLamp is about 200 lines long
    def __init__(self, ip_port_tuple, timeout=8, message_size=1024, verbose=False):
        self.verbose = verbose
        self.message_size = message_size

        # set up the communication here
        # record the ip address and port
        self.ip_address = ip_port_tuple[0]
        self.port_number = ip_port_tuple[1]
        # build the socket
        self._lan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._lan_socket.settimeout(timeout)

        # connect to the port and ip address.
        self._lan_socket.connect(ip_port_tuple)
        # when the BK powers down, b'\x00\x00\x00' will be found in the output buffer
        # when the BK powers up, b'\x00' will be found in the output buffer.
        # Not sure if the source of the above is the Lantronix or the BK power supply.
        # Random characters can also be found in the output buffer, these are probably noise

        # start remote session by disabling the front panel.
        # If the user really wants the front panel, they can reverse this by sending b'ENDS00\r"
        self._send_message(b'SESS00\r', empty=False)

        # recieve the ok, and discard. This also clears the buffer
        self._receive_message()

        # I haven't found the initialization commands in the tcl code
        # possible initialization calls
        # 'SESS00\r' disables the front keypad and puts ps in remote mode
        # 'SVOP00{volts}\r' sets the upper voltage limit

    # methods for controlling the current

    # prototypes for sending and recieving communications from the current controller.
    # these will probably be wrappers for a generic communication class

    def _send_message(self, output_string, verbose=None, empty=True, **kwargs):
        # strings must be in binary ASCII
        if verbose is None:
            verbose = self.verbose

        if empty:
            # empty the buffer by performing a call and response, and discarding the reply
            # this is a cludge, to deal with noise appearing in the bitstream
            # simply requesting the buffer to send it's data empties the data
            # but the request will result in a timeout error if there is no data to receive
            # in the future, someone should figure out a better way of emptying the buffer
            self._lan_socket.sendall(b'GETS00\r')
            if verbose:
                print('Command sent:', b'GETS00\r')
            sleep(0.1)  # sleep briefly to let the message send
            self._receive_message()

        self._lan_socket.sendall(output_string, **kwargs)
        if verbose:
            print('Command sent:', output_string)
        sleep(0.1)  # sleep briefly to let the message send

    def _receive_message(self, verbose=None, **kwargs):
        if verbose is None:
            verbose = self.verbose
        # connection should automatically time out after 8 secs
        reply = self._lan_socket.recv(self.message_size, **kwargs)

        if reply == '':
            # this means the lantronix closed the socket for some reason
            # close this end, and raise error
            self._lan_socket.close()
            raise BrokenPipeError(str(self.ip_address) + str(self.port_number) + 'closed connection')

        # check for end of string having a 'OK\r'
        tries = 1
        while reply[-3:] != b'OK\r':
            # if verbose:
            #     print('Message request', tries, 'received:', reply)

            # it should never take more than 2 tries
            # give it five tries, then raise an error
            if tries == 5:
                # possible exception classes:
                # ValueError
                # RuntimeError
                # consider makign a custom error
                raise RuntimeError('Unexpected reply: BK Precision power supply responded with', reply)
            # sleep for a moment
            sleep(0.1)
            # get more of the buffer
            reply += self._lan_socket.recv(self.message_size, **kwargs)
            tries += 1

        if verbose:
            print('Reply received:', reply)

        return reply

    def off(self):
        self._send_message(output_string=b'SOUT001\r')

        self._receive_message()

    def on(self):
        self._send_message(output_string=b'SOUT000\r')

    def set_volts(self, voltage):
        # formating is 3 numaric characters, with the last one being the decimal place
        # eg, float input  12.3
        # characters  123
        # string passed  'VOLT00123\r'

        # multiply float by ten, then truncate
        sanitized_input = int(voltage * 10)
        command = b'VOLT00%(volts)03d\r' % {b'volts': sanitized_input}
        # command = b'VOLT00{:03d}\r'.format(sanitized_input)
        self._send_message(command)

        # pause while the command
        # clear the buffer.
        # This will raise an error if the most recent command did not execute
        # not sure if I should return this function
        self._receive_message()

    def set_curr(self, current):
        # formating is 3 numeric characters, with the last two being decimal places
        # eg, to set 4.56 amps, give float input  4.56
        # characters  456
        # string passed  'CURR00456\r'
        sanitized_input = int(current * 100)
        # command = 'CURR00{:03d}\r'.format(sanitized_input)
        command = b'CURR00%(amps)03d\r' % {b'amps': sanitized_input}
        self._send_message(command)

        # clear buffer and check for errors
        self._receive_message()

    def get_settings(self):
        # NOTE: this has not been found in the tcl code
        raw_output_str = b''
        self._send_message(b'GETS00\r')
        # logging and error handling

        # returned string has the voltage and current information
        # eg, if set voltage = 12.3 V and set current = 4.56 A, the
        # return message string will be: '123456\rOK\r'
        reply = self._receive_message()

        # extract the info of interest: 6 digits followed by a \r
        raw_output_str = re.search(b'(\\d{6})\r', reply)[0]
        raw_voltage = raw_output_str[:3]
        raw_current = raw_output_str[3:6]

        voltage = float(raw_voltage)/10
        current = float(raw_current)/100

        return voltage, current

    def shutdown(self):
        # turn off the lamp power
        self.off()
        # return panel control
        self._send_message(b'ENDS00\r')
        self._receive_message()
        # last, close the socket
        self._lan_socket.close()

    # lamp_volts, lamp_current, on_off
    # keep track of how long the lamp is on for
    # set wval [SendCmd "SOUT001"]
    # work on figuring out what serial codes to send later

    # not sure what w_lamp() is, where it is defined
    # sqlset w_lamp(volt,value) $volt