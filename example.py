import atexit

from qe_api import *
from tungsten_lamp import TungstenLamp
config = open_config('config.yaml')

# start the camera controller
andorcam = start_controller(config)

# start the lamp
w_lamp = start_w_lamp(config, verbose=True)
# automatically call shutdown when the script ends
atexit.register(w_lamp.shutdown())

# main portion of script
w_lamp.set_volts(9.0)  # set to 9 volts

w_lamp.set_curr(4.56)  # set to limit of 4.56 amps

w_lamp.on()  # turn on the lamp
# the lamp has a warm-up period, unknown length

andorcam.set_exposure_time(0.5)  # set exposure time to .5 seconds

andorcam.set_shutter('shut')  # use 'open' for the real thing

andorcam.set_exposure_mode('single')


