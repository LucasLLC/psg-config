import os
from copy import deepcopy
from collections import OrderedDict


url = "https://psg.gsfc.nasa.gov/api.php"
default_config_fn = "default_config.txt"
output_dir = "output"

default_config = None

def read_config(config_fn = default_config_fn):
    """

    :param config_fn: location of default config
    :param ignore_these: Iterable of strings, will not read these from config
    :return: OrderedDict representing one config
    """

    with open(config_fn) as fp:
        config_lines = fp.readlines()

    config = OrderedDict()

    # read through every line in the config
    done = False
    for line in config_lines:

        # find out the field name
        for i in range(len(line)):

             if line[i] == ">":
                field_name = line[:i+1]

                # this is the name of the last field we want to read
                if "GENERATOR-RADUNITS" in field_name:

                    # now we are done processing the file
                    done = True

                config[field_name] = line[i+1:-1]
                break

        if done:
            # we are done processing the file, exit the loop
            break

    return config

def generate_config(**kwargs):
    """ Takes all keys in kwargs, and substitutes those keys in the default config

    :param kwargs: Any keys to be substituted in default config file
    :return:
    """

    # grab a default config
    config = get_default_config()

    for kwarg in kwargs:
        field_name = "<" + kwarg.replace("_", "-") + ">"
        config[field_name] = kwargs[kwarg]

    return config

def get_default_config():

    global default_config
    if not default_config:
        default_config = read_config()

    return deepcopy(default_config)

def config_to_file(config,
                   atmosphere_fn,
                   output_fn):
    """

    :param config:
    :param atmosphere_fn:
    :param config_fn:
    :return:
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(atmosphere_fn, "r") as fp:
        atmosphere_data = fp.read()

    with open(os.path.join(output_dir, output_fn), "w") as fp:
        for config_line in config:

            str_line = config_line + str(config[config_line]) + "\n"
            fp.write(str_line)
        fp.write(atmosphere_data)



if __name__ == '__main__':

    # generate a config
    config = generate_config(OBJECT="Michael's Ass",
                             OBJECT_DIAMETER=2)

    # write that config to a file, appending the context of sample_atmosphere
    config_to_file(config,
                   "sample_atmosphere.txt",
                   "michael_config.txt")
