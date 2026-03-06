#!/usr/bin/env python3
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#########################################################################
"""
VTS Configuration File
Contains all configuration parameters for the VTS test framework.
"""

import os

# ============= DEVICE CONFIGURATION =============
# Rack Configuration Parameters
#Update device ip below inside quotes
DEVICE_IP = ""
#Update device SoC inside quotes ex : "Amlogic", "Realtek" , "Broadcom"
DEVICE_PLATFORM = ""
DEVICE_DESCRIPTION = "xxx"
SSH_USERNAME = "root"
SSH_PASSWORD = ""
SSH_PORT = 22
LOG_DIRECTORY = "./logs"

# Device Configuration Parameters
#Update device SoC inside quotes ex : "Amlogic", "Realtek" , "Broadcom"
CPE_PLATFORM = ""
CPE_MODEL = "test"
#Update device SoC inside quotes ex : "amlogic", "realtek", "broadcom"
SOC_VENDOR = ""
TARGET_DIRECTORY ="/VTS_Package/"

#=====================STREAM====================================
#Update stream server hosting streams
STREAM_DOWNLOAD_PATH = ""
