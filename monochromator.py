
class Monochromator:
    """
    Class for controlling the monochromator.

    The monochomator has several individually controlled parts. For
    simplicity's sake, they are all to be wrapped in a class

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