

class TungstenLamp:
    # tcl version is tungstenlamp.tcl.sin
    # main control code in tcl version is the function SetWLamp
    # SetWLamp is about 200 lines long
    def __init__(self, ip_address, port):
        # set up the communication here

        # I haven't found the initialization commands in the tcl code
        # possible initialization calls
        # 'SESS00\r' disables the front keypad and puts ps in remote mode
        # 'SVOP00{volts}\r' sets the upper voltage limit
        pass

    # methods for controlling the current

    # prototypes for sending and recieving communications from the current controller.
    # these will probably be wrappers for a generic communication class
    def _send_message(self, output_string):
        pass

    def _recieve_message(self, input_string):
        pass

    def off(self):
        self._send_message(output_string='SOUT001\r')
        # some kind of error case handling here

    def on(self):
        self._send_message(output_string='SOUT000\r')

    def volt(self, voltage):
        # formating is 3 numaric characters, with the last one being the decimal place
        # eg, float input  12.3
        # characters  123
        # string passed  'VOLT00123\r'

        # multiply float by ten, then truncate
        sanitized_input = int(voltage * 10)
        command = 'VOLT00{:03d}\r'.format(sanitized_input)
        self._send_message(command)
        # some kind of error handling and logging here

    def current(self, current):
        # formating is 3 numeric characters, with the last two being decimal places
        # eg, float input  4.56
        # characters  456
        # string passed  'CURR00456\r'
        sanitized_input = int(current)
        command = 'CURR00{:03d}\r'.format(sanitized_input)
        self._send_message(command)
        # error handling and logging here

    def get_settings(self):
        # NOTE: this has not been found in the tcl code
        raw_output_str = ''
        self._send_message('GETS00\r')
        # logging and error handling

        # returned string has the voltage and current information
        # eg, if set voltage = 12.3 V and set current = 4.56 A, the
        # return message string will be: '123456\rOK\r'
        self._recieve_message(raw_output_str)
        # logging and error handling

        # decode the return message here


    # lamp_volts, lamp_current, on_off
    # keep track of how long the lamp is on for
    # set wval [SendCmd "SOUT001"]
    # work on figuring out what serial codes to send later

    # not sure what w_lamp() is, where it is defined
    # sqlset w_lamp(volt,value) $volt