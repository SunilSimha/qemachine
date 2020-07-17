"""
NOTES:

I don't know if ktl KEYWORD values need to be strings.
I also need to know what format is required for non-obvious values,
such as binning.

"""


import sys


# okay, this works:
sys.path.extend(['/opt/kroot/rel/default/lib/python',
                 '/opt/kroot/rel/default/lib',
                 '/usr/local/lick/lib/python',
                 '/usr/local/lick/lib'])

import ktl


class Controller:
    """
    This is a template controller interface class

    Populate all these functions, and you will have a working controller
    class for the QE machine. Each function has expected arguments and
    return values. It may be possible to leave some functions unpopulated,
    in which case the function will simply return a None value. The QE
    machine software will attempt to handle None values gracefully, but is
    not guaranteed to work.
    """
    # I need to carefully define the arguments for these functions.
    # I also need to add a way of handling multiple amps in the future
    def expose(self):
        # start an exposure
        pass

    def set_cooler(self, cooler_on):
        # turn the cooler on or off
        pass

    def get_cooler(self):
        # retrieve the current cooler setting
        pass

    def set_temp(self, target_temp):
        # set the target temperature of the cooler
        pass

    def get_targ_temp(self):
        # retrieve the target temperature of the cooler
        pass

    def get_curr_temp(self):
        # retrieve the current temperature of the cooler
        pass

    def set_exposure_time(self, new_exposure_time):
        # set the exposure time
        pass

    def get_exposure_time(self):
        # retrieve the current exposure time setting
        pass

    def set_amp(self):
        # select the readout amplifier
        pass

    def get_amp(self):
        # retrieve the current selected amp
        pass

    def set_gain(self):
        # select the gain
        pass

    def get_gain(self):
        # retrieve the current gain
        pass

    def set_read_speed(self):
        # select the readout speed
        pass

    def get_read_speed(self):
        # retrieve the current readout speed
        pass

    def set_binning(self):
        # set the pixel binning
        pass

    def get_binning(self):
        # retrieve the current pixel binning
        pass

    def set_window(self):
        # define a window, i.e., a region of interest or subsection of the CCD
        pass

    def get_window(self):
        # retrieve the current image window
        pass

    def set_shutter(self):
        # open or close the camera shutter
        pass

    def get_shutter(self):
        # retrieve the current shutter mode
        pass


class AndorCameraController(Controller):
    """
    Wrapper class for the iXon 888 ktl keyword service
    """
    def __init__(self, service_name, service_config_dict):

        self.andor_service = ktl.Service(service_name)
        # _write_keywords(self.andor_service, service_config_dict)
        _read_keywords(self.andor_service, service_config_dict)

    def expose(self):
        # start an exposure
        pass

    def set_exposure_time(self, new_exposure_time):
        # set the exposure time
        self.andor_service['EXPOSURE'].write(new_exposure_time)

    def get_exposure_time(self):
        # retrieve the current exposure time setting
        return self.andor_service['EXPOSURE'].read()

    def set_cooler(self, cooler_on):
        # turn the cooler on or off
        """

                Parameters
                ----------
                cooler_on: boolean
                    If True, turns the cooler on. If False, turns the cooler off
                """
        self.andor_service['COOLING'].write(cooler_on)
        # cooler_on possibly needs to be stringified

    def get_cooler(self):
        # retrieve the current cooler setting
        return self.andor_service['COOLING'].read()

    def set_temp(self, target_temp):
        # set the target temperature of the cooler

        # pass the target temperature to the ktl service
        keyword = self.andor_service['COOLTARG']
        ktl_function_code = keyword.write(target_temp)

        # to check what the current target temp is
        # current_target = keyword.read()

    def get_targ_temp(self):
        # retrieve the target temperature of the cooler
        return self.andor_service['COOLTARG'].read()

    def get_curr_temp(self):
        # retrieve the current temperature of the cooler
        return self.andor_service['CURRTEMP'].read()

    def set_amp(self):
        # select the readout amplifier
        pass

    def get_amp(self):
        # retrieve the current selected amp
        pass

    def set_gain(self):
        # select the gain
        pass

    def get_gain(self):
        # retrieve the current gain
        return self.andor_service['GAINMODE'].read()

    def set_read_speed(self):
        # select the readout speed
        pass

    def get_read_speed(self):
        # retrieve the current readout speed
        return self.andor_service['READSPEED'].read()

    def set_binning(self):
        # set the pixel binning
        pass

    def get_binning(self):
        # retrieve the current pixel binning
        return self.andor_service['BINNING'].read()

    def set_window(self):
        # define a window, i.e., a region of interest or subsection of the CCD
        """
        The KEYWORD format is
        WINDOW =
            hbeg:	136
            hend:	850
            vbeg:	220
            vend:	850

        I'm not sure what format is expected here.
        """
        pass

    def get_window(self):
        # retrieve the current image window
        return self.andor_service['WINDOW'].read()

    def set_shutter(self):
        # open or close the camera shutter
        pass

    def get_shutter(self):
        # retrieve the current shutter mode
        return self.andor_service['SHUTTERMODE'].read()

    def _set_expos_mode(self, new_mode):
        self.andor_service['EXPMODE'].write(new_mode)

    def _take_exposure(self):
        """
        This function is an internal routine that commands the Andor
        camera to take an exposure
        """
        self.andor_service['EXPOSE'].write('')
        # I have no idea what value to pass to trigger a write

    def _set_binning(self, new_bins):

        self.andor_service['BINNING'].write(new_bins)

    def _set_window(self, hsize, vsize):
        """
        The KEYWORD format is
        WINDOW =
            hbeg:	136
            hend:	850
            vbeg:	220
            vend:	850

        I'm not sure what format is expected here.
        """

    def _expose(self, exposure_dict):
        self.set_exposure(exposure_dict['exposure_time'])

        if exposure_dict['keyword3']:
            self.set_feature3(exposure_dict['keyword3'])
        # etc....

        self.take_exposure(exposure_dict['target_file_directory'])


def _read_keywords(ktl_service, keyword_dict):
    # reads multiple ktl keywords
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        value = ktl_keyword.read()
        print(keyword, ':', value)
        keyword_dict[keyword] = value


def _write_keywords(ktl_service, keyword_dict):
    # writes multiple ktl keywords
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        seq_number = ktl_keyword.write(value)  # value possibly requires a string

