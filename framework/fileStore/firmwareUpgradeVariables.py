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
##########################################################################
#

# This file contains the variables used for firmware upgrade operations.
# The user can populate the values as per requirement.

import time

#Target Firmware Names for RPI and BPI
#For other platforms, the same variable naming convention can be followed: FIRMWARE_UPGRADE_<PLATFORM>
FIRMWARE_UPGRADE_RPI=""
FIRMWARE_UPGRADE_BPI=""

#Target Firmware location and Protocol
#Target and Initial Firmware is placed in the http server location mentioned below
FIRMWARE_LOCATION=""
Protocol="http"

#XCONF Server URL
XCONF_URL = "https://xconf.rdkcentral.com/xconfAdminService/xconfAdminService"

# The firmware upgrade rule setting IDs - Dynamically generated with timestamp for uniqueness
timestamp = str(int(time.time()))

FWCONFIG_ID = f"TDKB_CURL_Firmware_CONFIG_{timestamp}"

MAC_RULE_ID = f"TDKB_CURL_MACRULE_{timestamp}"

MAC_LIST_ID = f"TDKB_CURL_MACLIST_{timestamp}"

SUPPORTED_MODEL_ID = f"RPI_TDKB_TEST_{timestamp}"

#Username of DUT
username = "root"

#Standalone TDK-B Package Installation Files and Path to enable TDK-B in RDK-B Builds
#Please ensure that the TDK-B package installation files are present in the source path mentioned below

#Source path of TDK Package Installation Files in the Host Machine[TM]
source_path = ""
#Name of the TDK-B Installation Script
install_script = ""
#Name of the TDK-B Package to be deployed
tdk_package = ""

#Destination of Package Installation Files in DUT
dest_path = "/rdklogs"

# Xconf Server Firmware Download Location
xconf_firmware_location = "/extblock/httpimage/imagedwnld"

# Partition path for getting partition count
PARTITION_PATH = "/dev/mmcblk0p*"

