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
import tungsten_lamp


def _connect_ktl_service(service_config, verbose=True):
    # unpack the type of the service
    service_type = service_config['controller_type']

    if service_type == 'andorcam':
        # build and return an andorcam ktl service
        return controller.AndorCameraController(service_config['ktl_service_name'],
                                                service_config['startup_config'],
                                                verbose=verbose)

    if service_type == 'archon':
        # return an archon controller class
        pass
    else:
        # raise an error if no matching controller type is found
        # fill in the error type later
        raise


def open_config(config_filename, **kwargs):
    """
    Opens a yaml file, and returns it as a dictionary.

    This is a simple wrapper for yaml.load()

    Parameters
    ----------
    config_filename: string
        Name of the configuration file, typicall 'config.yaml'
    kwargs
        Keyword arguments for yaml.load.

    Returns
    -------
    config_dict: dictionary
        A dictionary containing the QE machine configuration
    """
    with open(config_filename) as file:
        config_dict = yaml.load(file, **kwargs)

    return config_dict


def start_controller(config_dict, config_key='ccd_controller0', verbose=True):
    """
    Constructs a CCD controller object, using the information in the
    configuration file.

    This function scans the section of a config dictionary under the
    given key. It determines what kind of controller object to build by
    examining key: value pairs, both what the key is, and what the key
    value contains. Currently, start_controller() only knows how to build
    ktl keyword controllers, but it is easily extendable by simply
    defining new keywords.

    For example, if the key named 'ktl_service_name' exists, then
    start_controller() will know to build a ktl service object. The value
    of 'ktl_service_name' is the specific ktl service to access. When
    loading ktl keyword services, start_controller() also needs to know
    what kind of ktl service this is, this information must be contained
    under a key named 'controller_type'. Start_controller() will also load
    any keywords defined under 'startup_config', treating keyword: value
    pairs as ktl keyword: value pairs. An example configuration would be:

    ccd_controller0:
        ktl_service_name : 'shanegcam'
        controller_type : 'andorcam'
        startup_config :
            # this section is interpreted as ktl keyword:value pairs
            # ktl keywords can be arbitrary, but must match actual keywords in the service
            EXPOSURE : 1.0
            GAINMODE : 0
            READSPEED : '1.0MHz'
            # put whatever keywords that have a controller function here
            OBSMODE : 'Other'



    Parameters
    ----------
    config_dict: dict
        A dictionary containing configuration information. Typically
        loaded from a config file.
    config_key: string, optional
        What key to look under for controller configuration info.
    verbose: bool, optional

    Returns
    -------

    """
    # I should figure out a way of parsing raw_config, and pulling
    # everything that matches the pattern 'ccd_controller\d'. Then each
    # matching instance will get it's own ktl service connection
    controller_config = config_dict[config_key]

    if controller_config['ktl_service_name']:
        ccd_controller = _connect_ktl_service(config_dict[config_key], verbose=verbose)

    # this can be easily extended by adding new keyword names and defining
    # corresponding constructor helper functions. For example
    #

    return ccd_controller


def start_w_lamp(config_dict, **kwargs):
    # carefully unpack the lan address into a tuple
    lan_address = (config_dict['lantronix']['w_lamp']['ip'],
                   config_dict['lantronix']['w_lamp']['port'])

    return tungsten_lamp.TungstenLamp(lan_address, **kwargs)

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





