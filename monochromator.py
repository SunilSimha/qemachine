"""
Developer notes:


The monochromator consists of both a diffraction grating monochromator,
and a 6-position filter wheel accessory, with both controlled through the
same serial port interface. For simplicity's sake, both should be wrapped
in a single class, with possible subclasses if appropriate. The
monochromator may also have a shutter, whether or not it does should be
confirmed.

The monochromator can use either the IEEE-488 or RS-232 standard. This doc
assumes RS-232 serial port communication is being used. This interface is
similar to the tungsten lamp serial interface. Refer to tungsten_lamp for
an example of serial port interface control in python.

All messages sent to the monochromator must end in a linefeed character,
'\n'. Responses from the monochromater end with carriage return and
newline characters, '\r\n' in python.


"""


class Monochromator:
    """
    Class for controlling the Newport Cornerstone 130 model 70000 monochromator.


    """
    def __init__(self):
        """
        read in config file


        Stub, too tired to think
        """
        pass

    def filter_wheel(self, filter_index):
        # sent a rotate command to the filter wheel
        pass

    def select_wavelength(self, center_wavelength):
        # there are two ways of selecting the wavelength:
        # center wavelength
        # or the upper and lower wavelength on a bandpass
        # the bandpass is so narrow it's effectively monochromatic

        # there are two diffraction gratings, for red or blue regimes
        # Not sure if grating selection should be automatic, based on the
        # current wavelength, or user controlled
        pass

    def set_slit_width(self, input_width, output_width, some_middle_slit):
        # the width of the monochromator slits
        # there are three slits:
        # one on the input to the monochromator
        # another on the output of the monochromator
        # I don't know what the 3rd, internal slit does
        # block higher order refractions? But that's what the filter wheel is for
        # I want an optical diagram of the monochromator

        pass