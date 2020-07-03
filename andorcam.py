import sys


# okay, this works:
sys.path.extend(['/opt/kroot/rel/default/lib/python',
                 '/opt/kroot/rel/default/lib',
                 '/usr/local/lick/lib/python',
                 '/usr/local/lick/lib'])

import ktl


class AndorCameraController:
    """
    Class that takes an exposure using the
    """
    def __init__(self, config_dict):

        self._intialize_iXon(config_dict['use_syslog'])

        andor_service = ktl.Service(config_dict['service_name'])
        # general template given below
        self.set_feature_1(config_dict['keyword1'])
        self.set_feature_2(config_dict['keyword2'])
        # etc

    def _intialize_iXon(self, use_syslog):
        # this is an alias for booting up the andor
        # currently, not going to be used

        pass

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

    def _set_cooler_temp(self, target_temp):
        # pass the target temperature to the ktl service
        pass

    def _take_exposure(self):
        """
        This function is an internal routine that commands the Andor
        camera to take an exposure

        Returns
        -------

        """
        # call some ktl service
        pass

    def _set_(self, value):
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
