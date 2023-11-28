#!/usr/bin/env python3
"""
    Name:
        parse_metrics.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        Minifies the full metrics.json file
"""
import json
import argparse
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

types = {
    "bool": 0,
    "int": 1,
    "float": 2
}


parser = argparse.ArgumentParser(description='Minify the full metrics.json file. Prints output to STDOUT')
parser.add_argument('file', type=argparse.FileType('r'), help='Source metrics file in JSON format')

args = parser.parse_args()


metrics_in = None
with args.file as file:
    metrics_in = json.load(file)


index = 0
metrics_out = []
for metric, config in metrics_in.items():
    metrics_out.append(metric)
    # logger.info("Handling config for {}: {}".format(metric, config))
    # out = []
    # out.append(types[config['type']])
    # out.append(config.get("address", 0))
    # bytes = []
    # for byte in config.get("byte_list", []):
    #     byte_config = []
    #     byte_config.append(byte['byte_num'])
    #     byte_config.append(byte['start_bit'])
    #     byte_config.append(byte['num_bits'])
    #     bytes.append(byte_config)
    # out.append(bytes)
    # metrics_out.append(out)
    # metrics_out[metric] = out

# print(json.dumps(metrics_out))
# print("{}".format(metrics_out.sort()))
metrics_out.sort()
for line in metrics_out:
    print(line)
