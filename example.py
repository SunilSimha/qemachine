import atexit

from qe_api import *
from tungsten_lamp import TungstenLamp
config = open_config('config.yaml')

# start the camera controller
andorcam = start_controller(config, verbose=True)

# start the lamp
w_lamp = start_w_lamp(config, verbose=True)

# automatically call shutdown when the script ends
# needs the function pointer, not the function invocation
atexit.register(w_lamp.shutdown)

# main portion of script
w_lamp.set_volts(9.0)  # set to 9 volts

w_lamp.set_curr(4.56)  # set to limit of 4.56 amps

w_lamp.on()  # turn on the lamp
# the lamp has a warm-up period, unknown length

andorcam.set_exposure_time(0.5)  # set exposure time to .5 seconds

andorcam.set_shutter('shut')  # use 'open' for the real thing

andorcam.set_exposure_mode('single')

andorcam.expose('Start')

'''
Example of what this looks like at runtime

>>> from qe_api import *
>>> 
>>> config = open_config('config.yaml')
>>> 
>>> andorcam = start_controller(config, verbose=True)
Setting up initial configuration 
Writing keywords...
EXPOSURE 1.0
GAINMODE 0
READSPEED 1.0MHz
>>> andorcam.set_exposure_time(0.5)
>>> andorcam.get_exposure_time()
'0.500'
>>> andorcam.set_exposure_time(1.0)
>>> andorcam.get_exposure_time()
'1.000'
>>> andorcam.set_exposure_mode('single')
>>> andorcam.expose('start')
>>> 
>>> w_lamp = start_w_lamp(config, verbose=True)
Command sent: b'SESS00\r'
Reply received: b'OK\r'
>>> # accessing a keyword directly
>>> keyword = andorcam.andor_service['kinTimE']
>>> keyword.read()
'2.119'
>>> andorcam.set_exposure_time(.2)
>>> keyword.read()
'1.319'
>>> 

'''
