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

# start by adding the ktl python module path
import sys
import yaml

# sys.path.append('/home/Lee/svn/kroot')
# okay, this works:
sys.path.extend(['/opt/kroot/rel/default/lib/python',
                 '/opt/kroot/rel/default/lib',
                 '/usr/local/lick/lib/python',
                 '/usr/local/lick/lib'])
import ktl


def _connect_ktl_service(service_config):

    pass


def _open_config(config_filename):
    with open('scratch.yaml') as file:
        config_dict = yaml.load(file, Loader=yaml.FullLoader)

    return config_dict


def _read_keywords(ktl_service, keyword_dict):
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        value = ktl_keyword.read()
        print(keyword, ':', value)
        keyword_dict[keyword] = value


def _write_keywords(ktl_service, keyword_dict):
    for keyword, value in keyword_dict.items():
        ktl_keyword = ktl_service[keyword]
        seq_number = ktl_keyword.write(value) # value possibly requires a string


def load_config(config_filename):

    raw_config = _open_config(config_filename)

    _connect_ktl_service(raw_config[service])


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





