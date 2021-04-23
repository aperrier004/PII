###
# Fichier comportant des fonctions pour lire un fichier .JSON
#

import os
import json

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def read_json(filename, debug=False):
    """Returns a list with the data of the json file.

    Parameters
    ----------
    filename : str
            Path to the file that has to be read
    debug : bool
            Indicating if DEBUG mode should be on or off; if DEBUG mode is on, information on what the script currently is doing will be printed to the console (default = False)

    Returns
    -------
    data : list
            With a dict for every trial. Following is the dictionary
            0. timestamp of the gaze
            1. name of the trial
            2. x -array of Gaze left positions,
            3. x -array of Gaze right positions,
            4. y -array of Gaze left positions,
            5. y -array of Gaze right positions
    """

    if debug:
        def message(msg):
            print(msg)
    else:
        def message(msg):
            pass

    # # # # #
    # file handling

    # check if the file exists
    if os.path.isfile(filename):
        # open file
        message("opening file '%s'" % filename)
        f = open(filename, 'r')
    # raise exception if the file does not exist
    else:
        raise Exception(
            "Error in read_json: file '%s' does not exist" % filename)

    # read file contents
    message("reading file '%s'" % filename)

    with open(filename) as f:
        file_data = json.load(f)

    # close file
    message("closing file '%s'" % filename)
    f.close()

    # # # # #
    # parse lines

    # variables
    data = []
    trackertime = []  # =
    name = []  # =
    x_l = []  # =
    y_l = []  # =
    x_r = []  # =
    y_r = []  # =

    gameName = file_data['gameName']

    lenghtPoints = len(file_data['coordinatesAndTimeStamp'])

    # Screen ratio 16:9
    real_x = 1920
    real_y = 1080

    # if it's 4:3
    if file_data['screenAspectRatio'] == "4:3":
        real_x = 1280
        real_y = 960

    # loop through all data of "coordinatesAndTimeStamp" --> used data
    for i in range(lenghtPoints):
        trackertime.append(file_data['coordinatesAndTimeStamp'][i]['time'])
        name.append(gameName)
        x_l.append(file_data['coordinatesAndTimeStamp'][i]['X'] * real_x)
        x_r.append(file_data['coordinatesAndTimeStamp'][i]['X'] * real_x)
        y_l.append(file_data['coordinatesAndTimeStamp'][i]['Y'] * real_y)
        y_r.append(file_data['coordinatesAndTimeStamp'][i]['Y'] * real_y)

        trial = {}
        trial['trackertime'] = np.array(trackertime)
        trial['name'] = np.array(name)
        trial['x_l'] = np.array(x_l)
        trial['x_r'] = np.array(x_r)
        trial['y_l'] = np.array(y_l)
        trial['y_r'] = np.array(y_r)

        # add trial to data
        data.append(trial)

        # reset stuff
        trackertime = []
        name = []
        x_l = []
        y_l = []
        x_r = []
        y_r = []

    # # # # #
    # return

    return data
