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


# Firmware upgrade TR-181 data models
FW_DOWNLOAD_PROTOCOL_DM = "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadProtocol"
FW_DOWNLOAD_URL_DM = "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadURL"
FW_TO_DOWNLOAD_DM = "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareToDownload"
FW_DOWNLOAD_DM = "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadAndFactoryReset"
FW_DOWNLOAD_STATUS_DM = "Device.DeviceInfo.X_RDKCENTRAL-COM_FirmwareDownloadStatus"
FW_UPGRADE_DM_PARAMS = [
    FW_DOWNLOAD_PROTOCOL_DM,
    FW_DOWNLOAD_URL_DM,
    FW_TO_DOWNLOAD_DM,
    FW_DOWNLOAD_DM
]

DEFINE_PROPERTIES_TYPE = "com.comcast.xconf.firmware.DefinePropertiesAction"

DEFINE_PROPERTIES_FILTER = "DOWNLOAD_LOCATION_FILTER"


# Suffix for firmware checksum version
checksum_suffix = ".txt"

# Delay between the execution of XCONF config commands
XCONF_CMD_WAIT = 30
