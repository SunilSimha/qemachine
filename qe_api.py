"""
This is the function prototype code for the QE machine api.

In the future, this will develop into a full API

The goal is to keep the user interface the same, while allowing
        several different controller API's to run in the back end. The CCD
        controller will be handled by a KTL keyword server. There will be
        differences between controllers, at the very least in the available
        options.


All methods and functions should return an error code

The basic flow is for the user to enter keyword-value pairs via the terminal.
This keyword-value pair will be interpreted as a dictionary, which can then be
passed around to the various arguments. Since dictionaries have an arbitrary
number of keyword-value pairs, this effectively means the functions and classes
have an effectively arbitrary number of possible arguments. This enables an
enormous amount of flexibility: specifically, the user can write a script
for one CCD controller, and then be able to use that exact same script with
another totally different CCD controller without changing any arguments.

Another nice aspect of generating dictionaries from text is it lends itself
naturally to reading in config files.

"""


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


class AndorCameraController:
    """
    Class that takes an exposure using the
    """
    def __init__(self, config_dict):
        self.set_feature_1(config_dict['keyword1'])
        self.set_feature_2(config_dict['keyword2'])
        # etc

    def _set_exposure(self, new_exposure_time):
        """
        This is an internal routine that sets the exposure time of the camera
        being used with the QE machine. It is meant to be specific to the
        camera being used, covering all the warts of that camera's particular
        interface.

        Parameters
        ----------
        new_exposure_time: Float
            The exposure time in seconds that the camera will be set to

        Returns
        -------

        """
        # call some ktl service
        pass

    def _take_exposure(self):
        """
        This function is an internal routine that commands
        Returns
        -------

        """
        # call some ktl service
        pass

    def _set_feature_1(self, value):
        # call some api function here, prob a ktl keyword service
        pass

    def _set_feature_2(self, value):
        # call the second api function here
        pass

    def _set_feature_3(self, value):
        # call the second api function here
        pass

    def take_exposure(self, exposure_dict):
        self.set_exposure(exposure_dict['exposure_time'])

        if exposure_dict['keyword3']:
            self.set_feature3(exposure_dict['keyword3'])
        # etc....

        self.take_exposure(exposure_dict['target_file_directory'])


"""
Other QE machine functions
"""


def tungsten_lamp(lamp_volts, lamp_current, on_off):
    # keep track of how long the lamp is on for
    # set wval [SendCmd "SOUT001"]
    # work on figuring out what serial codes to send later

    # not sure what w_lamp() is, where it is defined
    # sqlset w_lamp(volt,value) $volt

    pass


def set_current():
    # control for the Keithley Model 6220 precision current source
    # not sure what the arguments for this need ot be
    # or what the current is going to. The tungsten lamp? Xenon lamp? Both?
    pass


def diode():
    # apparently, the diode controller also handles the light source mirror position
    # it seems the 'light source mirror' selects the XE or W lamp

    pass





