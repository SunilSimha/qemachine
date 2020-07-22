

import socket
import re
from time import sleep


class TungstenLamp:
    """
    A class for controlling the BK Precision 1697 power supply for the tungsten
    light source lamp. Only once instance of this class should run at a time.

    This class is meant to control the BK 1697 power supply for the CCD Lab QE
    machine. It functions by passing ASCII byte characters over an IP socket to
    a Lantronix device, which then passes the ASCII byte characters via serial
    port to the BK serial interface. The BK expects specific character strings,
    of varying lengths, and also replies with specific character strings. The
    BK will always end a reply with a 'OK\r'.

    When a class instance is created, it will automatically connect to the
    provided ip address and port. It will do this if the Lantronix is on,
    regardless if the BK power supply is powered on or not. Upon class instance
    creation, it disables the front panel control.

    Always invoke the shutdown method before finishing a script, program, or
    even discarding a class instance. This shuts off the lamp, re-enables the
    front panel, and correctly closes the connection to the Lantronix.

    Parameters
    ----------
    ip_port: tuple
        the ip address of the Lantronix, and the particular Lantronix port
        controlling the BK Precision 1697 power supply. This should have the
        format: (<ip address>, <port number>).
    timeout: non-negative float or None, optional
        The number of seconds the class will wait for a response from the
        Lantronix connection. If set to None, the connection will never time
        out. This last is not recommended, as it can lead to the program
        hanging while it waits for a reply that will never come.
    message_size: int, optional
        The number of characters the client-side socket will request from the
        server-side character buffer. Default is 1024, and represents a maximum
        number of characters to receive. The BK power supply always ends a
        reply with 'OK\r'. If the reply buffer does end with a 'OK\r', then
        TunstenLamp will repeat the request every 100ms up to 5 times until a
        'OK\r' is dectected at the buffer end. If after 5 times a 'OK\r' is not
        detected, it will raise an error.
    verbose: bool
        If True, TungstenLamp will print statements to help with debugging.
        Specifically, it will print every byte-string send to and received from
        the BK power supply.

    Methods
    -------
    off:
        Turns the power output to the lamp off
    on:
        Turns the power ouput to the lamp on
    set_volts:
        set the voltage of the power supply output
    set_curr:
        set the current of the power supply output
    get_outputs:
        Returns the voltage and current settings of the power supply output.
    shutdown:
        Turns off the output and shuts down the connection to the power supply

    Raises
    ------a
    BrokenPipeError:
        Occurs when the server side of the connection to the Lantronix is
        closed.
    RuntimeError:
        Occurs when a reply message that does not end with a 'OK\r' is found in
        the output buffer of the Lantronix connection. This generally means the
        BK power supply is not on.

    Notes
    -----
    This needs a way of tracking how long the lamp has been running.
    The tungsten lamp element has a limited life span, in that after a certain
    number of hours of runtime, the tungsten element needs to be replaced. The
    power supply does not track number of hours of runtime, so this needs to be
    tracked in software. This has not yet been implemented

    This needs some kind of logging. An obvious place is the _send_message and
    _receive_message helper methods. They already contain optional print
    statements of each byte-string send to and received from the BK, these seem
    like a good thing to also log.

    Currently, set commands return None.  They could be set to return the reply
    string, but that redundant with error checks, and inconsistent with the get
    functions. Every time the BK receives any command, it replies with a 'OK\r'
    to confirm the command was executed. The set functions checks if the 'OK\r'
    confirmation is received, and raises an exception if it does not. Also, the
    get functions return the requested values, NOT the reply string, so it
    makes more sense to either return a requested value(s), or, if there is no
    requested value, return a None.

    There are several functionalities that might be needed, that are not yet
    implemented. Possible candidates are setting and getting the upper voltage
    supply limit
    """
    # tcl version is tungstenlamp.tcl.sin
    # main control code in tcl version is the function SetWLamp
    # SetWLamp is about 200 lines long
    def __init__(self, ip_port, timeout=8, message_size=1024, verbose=False):
        self.verbose = verbose
        self.message_size = message_size

        # set up the communication here
        # record the ip address and port
        self.ip_address = ip_port[0]
        self.port_number = ip_port[1]
        # build the socket
        self._lan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._lan_socket.settimeout(timeout)

        # connect to the port and ip address.
        self._lan_socket.connect(ip_port)
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
            # to prevent a timeout, send a 'GETS00\r' to ensure something is in the buffer
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
        """
        Turns the power output of the BK Precision power supply off

        Effectively, this turns the lamp off.

        Returns
        -------
        None

        """
        self._send_message(output_string=b'SOUT001\r')

        self._receive_message()

    def on(self):
        """
        Turns the power outpu of the BK Prescision power supply on.

        Effectively, this turns the lamp on.

        Returns
        -------
        None
        """
        self._send_message(output_string=b'SOUT000\r')

    def set_volts(self, voltage):
        """
        Sets the voltage output of the BK power supply, in volts.

        Parameters
        ----------
        voltage: float
            This should be a 3 digit float, with one trailing decimal place.
            E.g., to set the BK to 12.3 volts, pass 12.3. Anything beyond those
            digits will simply be discarded, eg, passing 123.45 will result in
            the BK being set to 23.4 volts.

        Returns
        -------
        None

        """
        # formating is 3 numaric characters, with the last one being the decimal place
        # eg, float input  12.3
        # characters  123
        # string passed  'VOLT00123\r'

        # multiply float by ten, then truncate
        # % 1000 (modulus 1000) removes all digits above 3 places
        sanitized_input = int(voltage * 10 % 1000)
        command = b'VOLT00%(volts)03d\r' % {b'volts': sanitized_input}
        # command = b'VOLT00{:03d}\r'.format(sanitized_input)
        self._send_message(command)

        # pause while the command
        # clear the buffer.
        # This will raise an error if the most recent command did not execute
        # not sure if I should return this function
        self._receive_message()

    def set_curr(self, current):
        """
        Set the current output limit of the BK power supply, in amps.

        It's not clear if this sets the current output, or merely sets a
        current limit.

        Parameters
        ----------
        current: float
            This should be a 3 digit float, with 2 trailing decimal places.
            E.g., to set the BK current limit to 4.56 amps, pass 4.56. Any
            digits beyond those places will simply be discarded, e.g., passing
            456.789 will result in the BK being set to 6.78 amps.

        Returns
        -------
        None
        """
        # formating is 3 numeric characters, with the last two being decimal places
        # eg, to set 4.56 amps, give float input  4.56
        # then pass characters 456
        # string passed  'CURR00456\r'
        sanitized_input = int(current * 100 % 1000)
        # command = 'CURR00{:03d}\r'.format(sanitized_input)
        # %03d means: digits, if less than 3 pad with zeros out to 3 places
        command = b'CURR00%03d\r' % sanitized_input
        self._send_message(command)

        # clear buffer and check for errors
        self._receive_message()

    def get_outputs(self):
        """
        Query the BK Precision 1697 power supply for it's voltage and
        current output settings.

        Returns
        -------
        voltage: float
            The voltage output, in volts. This always be 3 digits, with a
            single decimal place. E.g., if the BK is set to 12.3 volts, this
            will be 12.3.
        current: float
            The current output, in amps. This will always be 3 digits, with two
            decimal places. E.g., if the BK is set to 4.56 amps, this will be
            4.56.

        Notes
        -----
        It's not clear if the current value returned is the actual current
        output, or the set limit on the current output.
        """
        # NOTE: this has not been found in the tcl code

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
        """
        Shuts down the connection to BK Precision 1697 power supply

        This turns off the power to the lamp, re-enables the front panel, and
        closes the connection socket to the Lantronics. This function needs to
        be called whenever a class instance is to be discarded, including when
        ending a program or script.

        When running a script, simply discarding or del'ing a class instance
        might leave the lamp on, will leave the front panel disabled, and might
        block future connections to the BK power supply through the Lantronics.

        Returns
        -------
        None
        """

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