##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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
import json
import rdkv_performancelib
from rdkv_performancelib import *
broker_port = 1883
#------------------------------------------------------------------------------------------------------------------------
#Mapping user-friendly operation names to their corresponding DAB API identifiers for enhanced code clarity and maintainability.
#------------------------------------------------------------------------------------------------------------------------
operation_name = {
    "dab_get_api": "system/settings/get",
    "dab_get_settings_list_api": "system/settings/list",
    "dab_set_api":"system/settings/set",
    "dab_device_info_api":"device/info",
    "dab_app_list":"applications/list",
    "dab_app_launch":"applications/launch",
    "dab_app_launch_with_content":"applications/launch-with-content",
    "dab_app_state":"applications/get-state",
    "dab_app_exit":"applications/exit",
    "dab_key_press":"input/key-press",
    "dab_screenshot":"output/image"
    # ... add more operations as needed
}

#--------------------------------------------------------------------------------------------------------------------------
#The `operations` dictionary defines all DAB-supported operations with their corresponding topics and message structures.
# This dictionary serves as a reference for constructing DAB API requests using the `perform_operation` function in `rdkv_dablib.py`.
# Each key in the dictionary represents a supported operation name.
# The corresponding value is a dictionary with two keys:
#   * `topic`: The MQTT topic to publish the request message to.
#   * `message` (optional): A dictionary containing the default message payload for the operation.
#       - If a message payload is not required for the operation, this key can be omitted or set to an empty dictionary (`{}`).
#       - If specific data needs to be included in the message, the keys and values within this dictionary define the structure.
# This dictionary provides a structured and centralized way to manage DAB operations and their message formats.
#--------------------------------------------------------------------------------------------------------------------------
operations = {
    "applications/list": {"topic": "applications/list", "message": {}},
    "applications/launch": {"topic": "applications/launch", "message": {"appId": "App_Name"}},
    "applications/launch-with-content": {"topic": "applications/launch-with-content", "message": {"appId": "App_Name", "contentId": "jfKfPfyJRdk"}},
    "applications/get-state": {"topic": "applications/get-state", "message": {"appId": "App_Name"}},
    "applications/exit": {"topic": "applications/exit", "message": {"appId": "App_Name"}},
    "device/info": {"topic": "device/info", "message": {}},
    "system/settings/list": {"topic": "system/settings/list", "message": {}},
    "system/settings/set": {"topic": "system/settings/set", "message": {"audioVolume": 00}},
    "system/settings/get": {"topic": "system/settings/get", "message": {}},
    "input/key/list": {"topic": "input/key/list", "message": {}},
    "input/key-press": {"topic": "input/key-press", "message": {"keyCode": "KEY_VOLUME_UP"}},
    "input/long-key-press": {"topic": "input/long-key-press", "message": {"keyCode": "KEY_VOLUME_UP", "durationMs": 3000}},
    "health-check/get": {"topic": "health-check/get", "message": {}}

    }
#--------------------------------------------------------------------------------------------------------------------------
# The special_case_mappings dictionary provides translation rules for specific DAB settings to their corresponding RDK equivalents.
# This is necessary due to inconsistencies or differences in terminology between the two systems.
# This dictionary is used to normalize values before comparison.
#--------------------------------------------------------------------------------------------------------------------------
special_case_mappings = {
    'audioOutputMode': {
        'passthrough': 'passthru',
        'auto': ['auto (dolby digital plus)', 'surround']
    },
    'hdrOutputMode': {
        'alwayshdr': True,
        'disablehdr': False,
    },
    'audioOutputSource': {
        'optical':'spdif0',
        'hdmi': 'hdmi0'
        # Add more mappings as needed
    }
}


#Define the validations to validate dab api's with corresponding rdk api's.

# --------------------------------------------------------------------------------------------------------------------------
# Defining rdk_get_dab_validations dictionary to map DAB settings to RDK API calls for validation.
# Each DAB setting has a corresponding RDK API and parameter to retrieve the same information.
# This dictionary is used to compare DAB and RDK values for each setting and ensure consistency.
# --------------------------------------------------------------------------------------------------------------------------
rdk_get_dab_validations = {
    'audioVolume': {
        'rdk_api': 'org.rdk.DisplaySettings.getVolumeLevel',
        'rdk_param': 'volumeLevel'
    },
    'audioOutputMode': {
        'rdk_api': 'org.rdk.DisplaySettings.getSoundMode',
        'rdk_param': 'soundMode'
    },
    'cec': {
        'rdk_api': 'org.rdk.HdmiCec_2.getEnabled',
        'rdk_param': 'enabled'
    },
    'language': {
        'rdk_api': 'org.rdk.UserPreferences.getUILanguage',
        'rdk_param': 'ui_language'
    },
    'mute': {
        'rdk_api': 'org.rdk.DisplaySettings.getMuted',
        'rdk_param': 'muted'
    },
    'textToSpeech': {
        'rdk_api': 'org.rdk.TextToSpeech.isttsenabled',
        'rdk_param': 'isenabled'
    },
    'audioOutputSource': {
        'rdk_api': 'org.rdk.DisplaySettings.getConnectedAudioPorts',
        'rdk_param': 'connectedAudioPorts'
    },
    'hdrOutputMode': {
        'rdk_api': 'org.rdk.DisplaySettings.getSettopHDRSupport',
        'rdk_param': "supportsHDR"
    },
    'outputResolution': {
        'rdk_api': 'org.rdk.DisplaySettings.getCurrentResolution',
        'rdk_param': ('resolution', 'w', 'h')
    }
}
#--------------------------------------------------------------------------------------------------------------------------
# Defining rdk_devinfo_validations dictionary to map DAB settings to RDK API calls for validation.
# Each DAB setting has a corresponding RDK API and parameter to retrieve the same information.
# This dictionary is used to compare DAB and RDK values for each setting and ensure consistency.
#--------------------------------------------------------------------------------------------------------------------------
rdk_devinfo_validations = {
    'chipset': {
        'dab_param': 'chipset',
        'rdk_api': 'DeviceIdentification.deviceidentification',
        'rdk_param': 'chipset'
    },
    'deviceId': {
        'dab_param': 'deviceId',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'estb_mac'

    },
    'firmwareBuild': {
        'dab_param': 'firmwareBuild',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'imageVersion'
    },
    'firmwareVersion': {
        'dab_param': 'firmwareVersion',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'imageVersion'
    },
    'manufacturer': {
        'dab_param': 'manufacturer',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'make'
    },
    'model': {
        'dab_param': 'model',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'model_number'
    },
    'networkInterfaces_eth': {
        'dab_param': 'networkInterfaces',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'eth_mac',
    },
    'networkInterfaces_wifi': {
        'dab_param': 'networkInterfaces',
        'rdk_api': 'org.rdk.System.getDeviceInfo',
        'rdk_param': 'wifi_mac',
    },
    'screenHeightPixels': {
        'dab_param': 'screenHeightPixels',
        'rdk_api': 'DisplayInfo.height'
    },
    'screenWidthPixels': {
        'dab_param': 'screenWidthPixels',
        'rdk_api': 'DisplayInfo.width'
    },
    'serialNumber': {
        'dab_param': 'serialNumber',
        'rdk_api': 'DeviceInfo.serialnumber',
        'rdk_param': 'serialnumber'
    },
    'uptimeSince': {
        'dab_param': 'uptimeSince',
        'rdk_api': 'DeviceInfo.systeminfo',
        'rdk_param': 'time',
    }
}
#--------------------------------------------------------------------------------------------------------------------------
# Defining rdk_SettingsList_validations dictionary to map DAB settings to RDK API calls for validation.
# Each DAB setting has a corresponding RDK API and parameter to retrieve the same information.
# This dictionary is used to compare DAB and RDK values for each setting and ensure consistency.
#--------------------------------------------------------------------------------------------------------------------------
rdk_SettingsList_validations = {
    "audioOutputMode": {
        "dab_param": "audioOutputMode",
        "rdk_api": "org.rdk.DisplaySettings.getSupportedAudioModes",
        'rdk_param':'supportedAudioModes'
    },
    "audioOutputSource": {
        "dab_param": "audioOutputSource",
        "rdk_api": "org.rdk.DisplaySettings.getSupportedAudioPorts",
        'rdk_param':'supportedAudioPorts'
    },
    "outputResolution": {
        "dab_param": "outputResolution",
        "rdk_api": "org.rdk.DisplaySettings.getSupportedResolutions",
        'rdk_param':'supportedResolutions',
    },
    "textToSpeech": {
        "dab_param": "textToSpeech",
        "rdk_api": None,  # No corresponding RDK API
    },
    "videoInputSource": {
        "dab_param": "videoInputSource",
        "rdk_api": None,  # No corresponding RDK API
    },
    "lowLatencyMode": {
        "dab_param": "lowLatencyMode",
        "rdk_api": None,  # No corresponding RDK API
    },
    "matchContentFrameRate": {
        "dab_param": "matchContentFrameRate",
        "rdk_api": None,  # No corresponding RDK API
    },
    "memc": {
        "dab_param": "memc",
        "rdk_api": None,  # No corresponding RDK API
    },
    "pictureMode": {
        "dab_param": "pictureMode",
        "rdk_api": None,  # No corresponding RDK API
    },
    "audioVolume": {
        "dab_param": "audioVolume",
        "rdk_api": None,  # No corresponding RDK API
    },
    "hdrOutputMode": {
        "dab_param": "hdrOutputMode",
        "rdk_api": None,  # No corresponding RDK API
    },
}
#--------------------------------------------------------------------------------------------------------------------------
# Defining rdk_set_dab_validations dictionary to map DAB settings to RDK API calls for validation.
# Each DAB setting has a corresponding RDK API and parameter to retrieve the same information.
# This dictionary is used to compare DAB and RDK values for each setting and ensure consistency.
#--------------------------------------------------------------------------------------------------------------------------
rdk_set_dab_validations = {
    'audioVolume': {
        'rdk_api': 'org.rdk.DisplaySettings.getVolumeLevel',
        'rdk_param': 'volumeLevel'
    },
    'audioOutputMode': {
        'rdk_api': 'org.rdk.DisplaySettings.getSoundMode',
        'rdk_param': 'soundMode'
    },
    'cec': {
        'rdk_api': 'org.rdk.HdmiCec_2.getEnabled',
        'rdk_param': 'enabled'
    },
    'language': {
        'rdk_api': 'org.rdk.UserPreferences.getUILanguage',
        'rdk_param': 'ui_language'
    },
    'mute': {
        'rdk_api': 'org.rdk.DisplaySettings.getMuted',
        'rdk_param': 'muted'
    },
    'textToSpeech': {
        'rdk_api': 'org.rdk.TextToSpeech.isttsenabled',
        'rdk_param': 'isenabled'
    },
    'audioOutputSource': {
        'rdk_api': 'org.rdk.DisplaySettings.getConnectedAudioPorts',
        'rdk_param': 'connectedAudioPorts'
    },
    'hdrOutputMode': {
        'rdk_api': 'org.rdk.DisplaySettings.getSettopHDRSupport',
        'rdk_param': "supportsHDR"
    },
    'outputResolution': {
        'rdk_api': 'org.rdk.DisplaySettings.getCurrentResolution',
        'rdk_param': ('resolution', 'w', 'h')
    }
}
