"""
NOTES:

KTL keyword values should be whatever the keyword type is.

I don't know how to handle enums. Python doesn't have native enums

Keywords can be array-likes, such as for binning.

"""


import sys
# start by adding the ktl python module path
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

    def set_exposure_mode(self, expmode):
        # set the exposure mode, e.g., single or continuous
        pass

    def get_exposure_mode(self):
        # retrieve the exposure mode setting
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
    Wrapper class for the iXon 888 ktl keyword service.

    Notes
    -----
    The behavior of taking an exposure with ktl keywords needs to be tested.
    """
    def __init__(self, service_name, service_config_dict, verbose=True):

        self.andor_service = ktl.Service(service_name)
        # _write_keywords(self.andor_service, service_config_dict)
        _write_keywords(self.andor_service, service_config_dict, verbose=verbose)

    def expose(self, command):
        # start an exposure
        # keyword calls for enums. Possible values
        # None, Abort, Stop, Start
        # python doesn't have enums in the C sense. Instead, pass matching strings
        # alternetely, passing the enum value is possible, enable this
        # casefold generates all lowercase, useful for case insensitive validation
        valid = {string.casefold() for string in {'None', 'Abort', 'Stop', 'Start'}}
        if command.casefold() not in valid:
            raise ValueError('expose: command must be one of %s' % valid)
        self.andor_service['EXPOSE'].write(command)

    def set_exposure_mode(self, expmode):
        # set the exposure mode, e.g., single or continuous
        # use matching strings instead of enum
        valid = {string.casefold() for string in {'Single', 'Continuous'}}
        if expmode.casefold() not in valid:
            raise ValueError('set_exposure_mode: expmode must be one of %s' % valid)
        self.andor_service['EXPMODE'].write(expmode)

    def get_exposure_mode(self):
        # retrieve the exposure mode setting
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
        cooler_on: bool
            True turns the cooler on, False turns it off.

        Returns
        -------

        """
        self.andor_service['COOLING'].write(cooler_on)
        # cooler_on possibly needs to be stringified

    def get_cooler(self):
        # retrieve the current cooler setting
        return self.andor_service['COOLING'].read()

    def set_temp(self, target_temp):
        # set the target temperature of the cooler

        # pass the target temperature to the ktl service
        ktl_function_code = self.andor_service['COOLTARG'].write(target_temp)

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
        # currently not defined for Andorcam
        pass

    def set_gain(self, gainmode):
        # select the gain
        # use matching strings to replace enums
        valid = {string.casefold() for string in {'Gain1', 'Gain2'}}
        if gainmode.casefold() not in valid:
            raise ValueError('set_gain: gainmode must be one of %s' % valid)
        self.andor_service['GAINMODE'].write(gainmode)

    def get_gain(self):
        # retrieve the current gain
        return self.andor_service['GAINMODE'].read()

    def set_read_speed(self, readmode):
        # select the readout speed
        # use matching strings to replace enums
        valid = {string.casefold() for string in {'1.0MHz', '0.1MHz'}}
        if readmode.casefold() not in valid:
            raise ValueError('set_read_speed: readmode must be one of %s' % valid)
        self.andor_service['READMODE'].write(readmode)

    def get_read_speed(self):
        # retrieve the current readout speed
        return self.andor_service['READSPEED'].read()

    def set_binning(self, new_bins):
        # use matching strings to replace enums
        valid = {string.casefold() for string in {'1,1', '2,2', '4,4'}}
        if new_bins.casefold() not in valid:
            raise ValueError('set_binning: new_bins must be one of %s' % valid)
        self.andor_service['BINNING'].write(new_bins)

    def get_binning(self):
        # retrieve the current pixel binning
        return self.andor_service['BINNING'].read()

    def set_window(self, window_array):
        # define a window, i.e., a region of interest or subsection of the CCD
        """
        define a window, i.e., a region of interest or subsection of the CCD

        The KEYWORD format is
        WINDOW =
            hbeg:	136
            hend:	850
            vbeg:	220
            vend:	850


        Parameters
        ----------
        window_array: array-like
            This needs to formatted as an array-like python object, like a list
            or tuple. The array-like needs to have exactly 4 entries,
            corresponding to the format given above. If it doesn't have exactly
            4 entries, it will raise an error.

        Returns
        -------

        """
        self.andor_service['WINDOW'].write(window_array)

    def get_window(self):
        # retrieve the current image window
        return self.andor_service['WINDOW'].read()

    def set_shutter(self, shuttermode):
        # open or close the camera shutter
        # possible values
        # 'auto', 'open', 'shut'
        # use matching strings instead of enums
        valid = {string.casefold() for string in {'auto', 'open', 'shut'}}
        if shuttermode.casefold() not in valid:
            raise ValueError('set_shutter: shuttermode must be one of %s' % valid)
        self.andor_service['SHUTTERMODE'].write(shuttermode)

    def get_shutter(self):
        # retrieve the current shutter mode
        return self.andor_service['SHUTTERMODE'].read()




def _read_keywords(ktl_service, keyword_dict):
    # reads multiple ktl keywords
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        value = ktl_keyword.read()
        print(keyword, ':', value)
        keyword_dict[keyword] = value


def _write_keywords(ktl_service, keyword_dict, verbose=False):
    # writes multiple ktl keywords
    if verbose:
        print('Setting up initial configuration \n'
              'Writing keywords...')
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        seq_number = ktl_keyword.write(value)  # value possibly requires a string
        if verbose:
            # print the keyword value pairs
            print(keyword, value)
