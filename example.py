from qe_api import *
from tungsten_lamp import TungstenLamp
config = open_config('config.yaml')

andorcam = start_controller(config)

w_lamp = start_w_lamp(config, verbose=True)

w_lamp.set_volts(9.0)  # set to 9 volts

w_lamp.set_curr(4.56)  # set to limit of 4.56 amps

w_lamp.on()  # turn on the lamp
# the lamp has a warm-up period, unknown length

andorcam.set_exposure_time(1.0)  # set exposure time to 1 second

andorcam.set_shutter()
