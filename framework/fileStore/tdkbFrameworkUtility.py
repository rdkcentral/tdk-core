#!/usr/bin/env python3

# Broadband-specific framework utility functions.

import os
import sys


def readtdkbConfigFile(obj):
    """
    Read HOST_NAME from framework/fileStore/tdkb.config.
    """

    configFile = obj.realpath + "fileStore/" + "tdkb.config"
    print("Configuration File Found : ", configFile)
    sys.stdout.flush()
    HostName = ""

    # Checking if file exists
    fileCheck = os.path.isfile(configFile)
    if fileCheck:
        for line in open(configFile).readlines():
            if "HOST_NAME" in line:
                HostName = line.split("=")[1].strip()
                print("Host name is %s" % HostName)

        if HostName == "":
            return "NULL"
    else:
        print("Configuration File does not exist.")
        sys.stdout.flush()
        exit()

    return HostName
