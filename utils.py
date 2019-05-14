import os
import json
import argparse

def create_config(name,chmod="r"):
    assert os.path.isfile(name),"Could not find config file"
    config_file = open(name,chmod)
    return json.loads(config_file.read())


def parse_arguments(description,config):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--pull',default="off",
                        help='pull from swarm triggers')
    return parser.parse_args()