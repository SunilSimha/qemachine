"""
This is the function prototype code for the QE machine api.

In the future, this will develop into a full API

The goal is to keep the user interface the same, while allowing
        several different controller API's to run in the back end. The CCD
        controller will be handled by a KTL keyword server. There will be
        differences between controllers, at the very least in the available
        options.


All methods and functions should return an error code.
Scratch the above: all methods and functions returning an error code does not
mesh well with python. Python does not do pass-by-reference, so if I want a
value from a function, I need to return that value(s). Alternatively, python
will do pass-by-reference for lists and dicts, I could leverage that. But that
is not in accordance with standard python practice. Standard python practice is
to return a value, and deal with errors by raising interrupts.

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


Notes
-----
I need a way of turning dictionary-style keyword-value pairs into ktl keywords


Setting up path variables

export KROOT=/opt/kroot
export RELDIR=$KROOT/rel/default
export LROOT=/usr/local/lick

run exec bash to restart shell

workaroud for gshow not known:
export PATH=/opt/kroot/bin:$PATH
"""


# import sys
import yaml


# sys.path.append('/home/Lee/svn/kroot')
# okay, this works:
# sys.path.extend(['/opt/kroot/rel/default/lib/python',
#                  '/opt/kroot/rel/default/lib',
#                  '/usr/local/lick/lib/python',
#                  '/usr/local/lick/lib'])
# import ktl

# local imports
import controller


def _connect_ktl_service(service_config):
    # unpack the type of the service
    service_type = service_config['controller_type']

    if service_type == 'andorcam':
        return controller.AndorCameraController(service_config['ktl_service_name'], service_config['startup_config'])

    if service_type == 'archon':
        # return an archon controller class
        pass
    else:
        # raise an error if no matching controller type is found
        # fill in the error type later
        raise


def _open_config(config_filename, **kwargs):
    with open(config_filename) as file:
        config_dict = yaml.load(file, **kwargs)

    return config_dict


def load_config(config_filename, **kwargs):
    # load_config(config_filename, Loader=yaml.FullLoader)
    config_dict = _open_config(config_filename, **kwargs)

    # I should figure out a way of parsing raw_config, and pulling
    # everything that matches the pattern 'ccd_controller\d'. Then each
    # matching instance will get it's own ktl service connection
    controller_config = config_dict['ccd_controller0']

    if controller_config['ktl_service_name']:
        ktl_service = _connect_ktl_service(config_dict['ccd_controller0'])

    # add more stuff that needs to be initialized
    # e.g., possibly make network connections

    return ktl_service


"""
Other QE machine functions
"""


def set_current():
    # control for the Keithley Model 6220 precision current source
    # not sure what the arguments for this need ot be
    # or what the current is going to. The tungsten lamp? Xenon lamp? Both?
    # def not the tungsten lamp, that uses the BK 1696 current source

    pass


def diode():
    # apparently, the diode controller also handles the light source mirror position
    # it seems the 'light source mirror' selects the XE or W lamp

    pass





