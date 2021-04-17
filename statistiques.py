import os
import json

import numpy as np


def active_time(filename, debug=False):
    """Returns a list with dicts for every trial.

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
            0. x -array of Gaze x positions,
            1. y -array of Gaze y positions,

            A COMPLETER
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

    # est-ce qu'il faut le fermer ?
    with open("F:/PII/GazePlay/2021-01-12-22-43-15-replayData.json") as f:
        file_data = json.load(f)

    # close file
    message("closing file '%s'" % filename)
    f.close()

    stopTime = file_data['lifeCycle']['stopTime']
    startTime = file_data['lifeCycle']['startTime']

    activeTime = stopTime - startTime

    def convertMillis(millis):
        seconds = (millis/1000) % 60
        minutes = (millis/(1000*60)) % 60
        hours = (millis/(1000*60*60)) % 24
        return seconds, minutes, hours

    return convertMillis(int(activeTime))
