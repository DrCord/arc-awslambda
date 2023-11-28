#! /usr/bin/env python
"""
    Name:
        telemetry_to_csv.py
    Category:
        This file is part of AWSLambda.
    Purpose:
        for loading json formatted telemetry data and exporting it as csv
"""
import json
import csv
import sys
import logging

# for file manipulation
from os import listdir
from os import mkdir
from os.path import isfile, join

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def append_header(header, new_field):
    if new_field not in header:
        header.append(new_field)
    return header


def make_csv(input_filename, output_filename):
    # build header
    header = ['timestamp']
    with open(input_filename) as input_file:
        for line in input_file:
            quantum = json.loads(line[:-1])  # remove \n
            for key in quantum:
                header = append_header(header, key)

    # build csv
    with open(output_filename, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        with open(input_filename) as input_file:
            for line in input_file:
                quantum = json.loads(line[:-1])  # remove \n
                writer.writerow(quantum)


def dir_to_csv(load_directory, save_directory=None):
    """
    Purpose:
        Read a directory of json telemetry data files, and reformat each one as a .csv file
    Inputs:
        load_directory: the name of the directory to read .json files from
        save_directory: the name of the directory to save .csv files to
            Default: None.  Will write to the load_directory.
    """
    if save_directory is None:
        save_directory = load_directory
    try:
        mkdir(save_directory)
    except OSError:
        logger.error("Creation of the directory %s failed" % save_directory)
    else:
        logger.info("Successfully created the directory %s " % save_directory)

    file_list = [f for f in listdir(load_directory) if isfile(join(load_directory, f))]
    file_list.sort()

    for telemetry_file in file_list:
        logger.info("Opening file {}".format(telemetry_file))
        save_file = telemetry_file[:-4] + '.csv'
        make_csv(join(load_directory, telemetry_file), join(save_directory, save_file))

    logger.info("Done.")


###############################################################################
# testing

def test():
    # pick a ringbuffer file
    # telemetry_file = '2019-09-23_yellow.txt'  # 318 KB
    telemetry_file = '2019-09-24_yellow.txt'  # 6.4 MB
    # telemetry_file = '2019-09-26_Mark.txt'  # 340 KB

    save_file = telemetry_file[:-4] + '.csv'
    make_csv(telemetry_file, save_file)
    logger.info("Done.")


###############################################################################
# main

if __name__ == '__main__':
    num_args = len(sys.argv)
    if num_args < 3:
        logger.info("Example usage: telemetry_to_csv.py json_directory csv_directory")
        sys.exit()

    dir_to_csv(sys.argv[1], sys.argv[2])
