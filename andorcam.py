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


def _read_keywords(ktl_service, keyword_dict):
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        value = ktl_keyword.read()
        print(keyword, ':', value)
        keyword_dict[keyword] = value


def _write_keywords(ktl_service, keyword_dict):
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        seq_number = ktl_keyword.write(value)  # value possibly requires a string


class AndorCameraController:
    """
    Class that takes an exposure using the
    """
    def __init__(self, service_name, service_config_dict):

        self.andor_service = ktl.Service(service_name)
        _write_keywords(self.andor_service, service_config_dict)


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
        self.andor_service['EXPOSURE'].write(new_exposure_time)

    def _set_expos_mode(self, new_mode):
        self.andor_service['EXPMODE'].write(new_mode)

    def _set_cooler_temp(self, target_temp):
        # pass the target temperature to the ktl service
        self.andor_service['COOLTARG'].write(target_temp)

    def _take_exposure(self):
        """
        This function is an internal routine that commands the Andor
        camera to take an exposure
        """
        self.andor_service['EXPOSE'].write('')
        # I have no idea what value to pass to trigger a write

    def _set_cooler(self, cooler_on):
        """

        Parameters
        ----------
        cooler_on: boolean
            If True, turns the cooler on. If False, turns the cooler off
        """
        self.andor_service['COOLING'].write(cooler_on)
        # cooler_on possibly needs to be stringified

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

    def take_exposure(self, exposure_dict):
        self.set_exposure(exposure_dict['exposure_time'])

        if exposure_dict['keyword3']:
            self.set_feature3(exposure_dict['keyword3'])
        # etc....

        self.take_exposure(exposure_dict['target_file_directory'])
