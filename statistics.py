###
# Functions for the statistics
###
import os
import json


def active_time(filename, debug=False):
    """Returns a conversion of ms to s, min and hour

    Parameters
    ----------
    filename : str
            Path to the file that has to be read
    debug : bool
            Indicating if DEBUG mode should be on or off; if DEBUG mode is on, information on what the script currently is doing will be printed to the console (default = False)

    Returns
    -------
    seconds, minutes, hours

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

    stopTime = file_data['lifeCycle']['stopTime']
    startTime = file_data['lifeCycle']['startTime']

    activeTime = stopTime - startTime

    def convertMillis(millis):
        seconds = (millis/1000) % 60
        minutes = (millis/(1000*60)) % 60
        hours = (millis/(1000*60*60)) % 24
        return seconds, minutes, hours

    return convertMillis(int(activeTime))


def gameName(filename, debug=False):
    """Returns the name of the game

    Parameters
    ----------
    filename : str
            Path to the file that has to be read
    debug : bool
            Indicating if DEBUG mode should be on or off; if DEBUG mode is on, information on what the script currently is doing will be printed to the console (default = False)

    Returns
    -------
    gameName : str
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

    gameName = file_data['gameName']

    return gameName


def goal(filename, debug=False):
    """Returns the number of goals

    Parameters
    ----------
    filename : str
            Path to the file that has to be read
    debug : bool
            Indicating if DEBUG mode should be on or off; if DEBUG mode is on, information on what the script currently is doing will be printed to the console (default = False)

    Returns
    -------
    goals : int
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

    goal = file_data['statsNbGoalsReached']

    return goal


def goalToReach(filename, debug=False):
    """Returns the number of goals to reach

    Parameters
    ----------
    filename : str
            Path to the file that has to be read
    debug : bool
            Indicating if DEBUG mode should be on or off; if DEBUG mode is on, information on what the script currently is doing will be printed to the console (default = False)

    Returns
    -------
    goalToReach : int
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

    goalToReach = file_data['statsNbGoalsToReach']

    if(goalToReach == 0):
        goalToReach = file_data['statsNbGoalsReached']

    return goalToReach
