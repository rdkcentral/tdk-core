##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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


#-----------------------------------------------------------------------------------------------
# module imports
#-----------------------------------------------------------------------------------------------
import inspect
import json , ast
import collections
from pexpect import pxssh
import configparser
from base64 import b64encode, b64decode
import base64
import codecs
from time import sleep
import re
import subprocess
import requests
import random
import string
import IPChangeDetectionVariables
import os
import datetime
import importlib 

timeZones = []

# To use the REST API variables
#import CertificationSuiteCommonVariables

#-----------------------------------------------------------------------------------------------
#               ***  RDK SERVICES VALIDATION FRAMEWORK SUPPORTING FUNCTIONS ***
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
# CheckAndGenerateTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues,otherInfo)
# Description : Method to parse the output JSON response and generate test result
# Parameter   : result - JSON response result value
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
#             : expectedValues - list of expected values
#             : otherInfo - list of other response messages like error/message etc
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateTestStepResult(result,methodTag,arguments,expectedValues,otherInfo={}):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. result - result from response JSON
    # b. methodTag - string
    # c. arguments - list
    # d. expectedValues - list
    # e. otherInfo - list

    # Output Variable:
    # a.info - dictionary
    #   1.info can have N different result key-value
    #    pairs based on user's need
    #   2.info must have "Test_Step_Status" key to
    #   update the status. By default its SUCCESS

    # DO NOT OVERRIDE THE RETURN VARIABLE "INFO" WITHIN
    # PARSER STEPS TO STORE SOME OTHER DATA. USER CAN
    # ONLY UPDATE "INFO" WITH RESULT DETAILS & STATUS
    info = {}
    info["Test_Step_Status"] = "SUCCESS"

    # USER CAN ADD N NUMBER OF RESPONSE RESULT PARSER
    # STES BELOW
    try:
        # Check whether the response result is empty
        if result == {} or result == [] or result == "":
            print("\n[INFO]: Received empty JSON response result")
            info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "exceptional_cases":
                info["Test_Step_Status"] = "SUCCESS"
                info["appStatus"] = "FALSE"
            elif len(arg) and arg[0] == "empty_result_validation":
                info["Test_Step_Status"] = "SUCCESS"
            # Ensure 'arg' is a list and has at least two elements
            elif isinstance(arg, list) and len(arg) > 1:
                if arg[1] == "no":
                    if not result:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

        # DeviceInfo Plugin Response result parser steps
        elif tag == "deviceinfo_get_system_info":

            if arg[0] == "check_cpu_load":
                info["cpu_load"] = result.get("cpuload")
                if int(info["cpu_load"]) < 90:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "get_all_info":
                if str(arg[1]).lower() == "yes":
                    info = checkAndGetAllResultInfo(result)
                elif str(arg[1]).lower() == "no":
                    info = result
                    newResult = result.copy()
                    if "esn" in newResult:
                        newResult.pop("esn")
                    status = checkNonEmptyResultData(newResult)
                    if status == "TRUE":
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "get_systeminfo_date":
                date = result.get("time")
                if date:
                    api_info = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
                    info["systeminfo_day"] = api_info.day
                    info["systeminfo_month"] = api_info.month
                    info["systeminfo_year"] = api_info.year
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_get_network_info":
            if arg[0] == "get_all_info":
                status = []
                network_info = []
                for interface in result:
                    interface_info = []
                    interface_info.append(interface.get("name"))
                    interface_info.append(interface.get("mac"))
                    interface_details  = "Name :" + interface.get("name") + " - "
                    interface_details += "MAC :"  + interface.get("mac")  + " - "
                    if interface.get("ip") is not None and len(interface.get("ip")):
                        ip_info = [ str(ip) for ip in interface.get("ip") ]
                        interface_info.extend(ip_info)
                        interface_details += "IP :" + str(ip_info)
                    else:
                        interface_details += "IP:"  + str(interface.get("ip"))
                    network_info.append(interface_details)
                    status.append(checkNonEmptyResultData(interface_info))
                info["network_info"] = network_info
                if "FALSE" not in status and len(network_info) != 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_get_socket_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        elif tag == "deviceinfo_get_api_info":
            info = checkAndGetAllResultInfo(result)

        elif tag == "deviceinfo_check_expected_result":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info[arg[0]] = result.get(arg[0])
                if str(result.get(arg[0])).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_firmware_version":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["imagename"] = result.get("imagename")
                info["yocto"] = result.get("yocto")
                if str(result.get("imagename")).lower() == str(expectedValues[0].strip()).lower() and str(result.get("yocto")).lower() == str(expectedValues[1].strip()).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_supported_audio_and_video_ports":
            info[arg[0]] = result.get(arg[0])
            if collections.Counter(result.get(arg[0])) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_supported_resolutions":
            info["supportedResolutions"] = result.get('supportedResolutions')
            if result.get('supportedResolutions'):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_default_resolution" :
            info["defaultResolution"] = result.get('defaultResolution')
            if str(result.get('defaultResolution')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_validate_firmware_version":
            imagename = result.get('imagename')
            info["imagename"] = imagename
            if imagename:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # LocationSync Plugin Response result parser steps
        elif tag == "locationsync_get_location_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        # OCDM Plugin Response result parser steps
        elif tag == "ocdm_get_drm_info":
            if arg[0] == "get_all_info":
                status = []
                supportedDRMStatus = []
                drms_name = []
                drm_info = []
                for drm in result:
                    drm_details = []
                    drm = eval(json.dumps(drm))
                    drm_details.append(drm.get("name"))
                    drms_name.append(drm.get("name"))
                    if drm.get("keysystems") is not None and len(drm.get("keysystems")):
                        key_info = [ str(key) for key in drm.get("keysystems") ]
                        drm_details.extend(key_info)
                    else:
                        status.append("FALSE")
                    drm_info.append(drm)
                    status.append(checkNonEmptyResultData(drm_details))
                info["drm_info"] = drm_info
                if expectedValues:
                    drms_name = [ value.lower() for value in drms_name ]
                    expectedValues = [ value.lower() for value in expectedValues ]
                    for value in expectedValues:
                        if value not in drms_name:
                            supportedDRMStatus.append("FALSE")
                if "FALSE" not in status and len(drm_info) != 0 and "FALSE" not in supportedDRMStatus:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "ocdm_get_drm_key_info":
            if arg[0] == "check_drm_key":
                key_info = []
                key_valid_status = "TRUE"
                for key in result:
                    key_info.append(str(key))
                    if key not in expectedValues:
                        key_valid_status = "FALSE"
                info["keysystems"] = key_info
                if key_valid_status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # DeviceIdentification Plugin Response result parser steps
        elif tag == "deviceidentification_get_platform_info":
            info = result.copy()
            status = checkNonEmptyResultData(list(info.values()))
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # TraceControl Plugin Response result parser steps
        elif tag == "tracecontrol_get_state":

            info["state"]    = result.get("settings")[0].get("state")
            info["module"]   = result.get("settings")[0].get("module")
            info["category"] = result.get("settings")[0].get("category")
            if arg[0] == "check_state":
                if info["state"] in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # MessageControl Plugin Response result parser steps
        elif tag == "messagecontrol_get_controls":
            for value in result:
                if str(value.get("module")).lower() == arg[1] and str(value.get("type")).lower() == arg[2] and str(value.get("category")).lower() == arg[3].lower():
                    info["enabled"] = value.get("enabled")
                    info["module"]   = value.get("module")
                    info["category"] = value.get("category")
                    break;
            if arg[0] == "check_state":
                if str(value.get("enabled")) == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # Network Plugin Response result parser steps
        elif tag == "network_get_interface_info":
            status,macAddressStatus=[],[]
            interfaces_info = result.get("interfaces")
            for interface in interfaces_info:
                status.append(checkNonEmptyResultData(list(interface.values())))
                macAddress = interface.get("macAddress")
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is None:
                macAddressStatus.append("False")
            if "FALSE" not in status and len(interfaces_info) != 0 and "FALSE" not in macAddressStatus:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

            info["interfaces"] = interfaces_info
            if arg[0] == "get_all_info":
                info["interfaces"] = interfaces_info
            elif arg[0] == "get_interface_names":
                interface_names = []
                for interface in interfaces_info:
                    interface_names.append(interface.get("interface"))
                interface_names = [ str(name) for name in interface_names if str(name).strip() ]
                info["interface_names"] = interface_names
            elif arg[0] == "check_interfaces_state":
                interface_names = []
                for interface in interfaces_info:
                    interface_names.append(interface.get("interface"))
                if "WIFI" and "ETHERNET" in interface_names:
                    info["Test_Step_Status"] = "SUCCESS"
                    for interface in interfaces_info:
                        if interface.get("interface") == "ETHERNET":
                            if str(interface.get("connected")).lower() == expectedValues[0]:
                                info["Test_Step_Status"] = "SUCCESS"
                            else:
                                info["Test_Step_Status"] = "FAILURE"
                        elif interface.get("interface") == "WIFI":
                            if str(interface.get("connected")).lower() == expectedValues[1]:
                                info["Test_Step_Status"] = "SUCCESS"
                            else:
                                info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_interfaces_enabled_state":
                interface_names = []
                for interface in interfaces_info:
                    interface_names.append(interface.get("interface"))
                if "WIFI" and "ETHERNET" in interface_names:
                    info["Test_Step_Status"] = "SUCCESS"
                    for interface in interfaces_info:
                        if interface.get("interface") == "ETHERNET":
                            if str(interface.get("enabled")).lower() != str(expectedValues[0]).lower():
                                info["Test_Step_Status"] = "FAILURE"
                        elif interface.get("interface") == "WIFI":
                            if str(interface.get("enabled")).lower() != str(expectedValues[1]).lower():
                                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_get_default_interface":
            default_interface = result.get("interface")
            info["default_interface"] = default_interface
            if len(arg) and arg[0] == "check_interface":
                if default_interface in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
                
        elif tag == "network_negative_error_message_validation":
            success = result.get("success")
            info["success"] = success
            message = str(result.get("error")).strip()
            info["error"] = message
            if str(success).lower() =="false" and any(value in message for value in expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_results":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "network_get_named_endpoints":
            result = result.get("endpoints")
            endpoints = [ str(name) for name in result if str(name).strip() ]
            info["endpoints"] = endpoints
            if len(endpoints):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_get_ping_response":
            info = checkAndGetAllResultInfo(result)
            if len(arg) and arg[0] == "validate_error_message":
                if str(result.get("success")).lower() == "false" and str(result.get('error')).lower() == str(expectedValues[1]).lower() and result.get("target") == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info = result.copy()
                target = result.get("target")
                tx_packets = int(result.get("packetsTransmitted"))
                rx_packets = int(result.get("packetsReceived"))
                packets_loss = result.get("packetLoss")
                if "duplicates" in packets_loss:
                    packets_loss = packets_loss.split("duplicates")[0]
                success = str(result.get("success")).lower() == "true"
                if len(arg) and arg[0] == "check_target":
                    packets = int(expectedValues[0])
                    host_ip = expectedValues[1]
                    if success and target == host_ip and tx_packets == packets and rx_packets == packets and int(packets_loss) == 0:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    packets = int(expectedValues[0])
                    if success and target.strip() and tx_packets == packets and rx_packets == packets and int(packets_loss) == 0:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_get_trace_response":
            info = result.copy()
            result_data = result.get("results")
            success = str(result.get("success")).lower() == "true"
            error_status = "FALSE"
            for data in result_data:
                if "ERROR" in data or "error" in data:
                    error_status = "TRUE"
            if len(arg) and arg[0] == "check_target":
                host_ip = expectedValues[0]
                if success and result.get("target") == host_ip and error_status == "FALSE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and error_status == "FALSE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_get_ip_settings":
            info = result.copy()
            if result.get("interface") == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "validate_ip_address":
                status = checkNonEmptyResultData(result)
                success = str(result.get("success")).lower() == "true"
                if success and status == "TRUE":
                    if str(result.get("autoconfig")).lower() == "true":
                        if re.match("^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$",str(result.get("dhcpserver")).lower()) is None:
                            info["Test_Step_Status"] = "FAILURE"
                        else:
                            info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_get_interface_status":
            info["enabled"] = result.get("enabled")
            if str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_check_interface_enable_set_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_connectedto_internet":
            info["ConnectedToInternet"] = result.get("connectedToInternet")
            status = checkNonEmptyResultData(result)
            if status and str(result.get("connectedToInternet")).lower() == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "network_check_device_ip_changed":
            info["Device_IP"] = result.get("ip")
            if str(result.get("ip")) != str(expectedValues):
                message = "Internally received onIPAddressStatusChanged event and default interface changed"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_validate_public_ip_address":
            success = str(result.get("success")).lower() == "true"
            info["public_ip"] = result.get("public_ip")
            if str(result.get("public_ip")).lower() == str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "network_check_internet_connection_state":
            info = result
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if success and status == "TRUE" and int(result.get("state")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Front Panel Response result parser steps
        elif tag == "frontpanel_get_led_info":
            supported_leds = result.get("supportedLights")
            supported_leds_info = []
            for led in supported_leds:
                led_info = result.get("supportedLightsInfo").get(led).copy()
                led_info["index"] = led
                supported_leds_info.append(led_info)
            status = []
            status.append(checkNonEmptyResultData(supported_leds))
            success = str(result.get("success")).lower() == "true"
            for led_info in supported_leds_info:
                status.append(checkNonEmptyResultData(list(led_info.values())))
            if arg[0] == "get_all_info":
                info["supported_leds"] = supported_leds
                info["supported_leds_info"] = supported_leds_info
            elif arg[0] == "get_power_led_info":
                info = result.get("supportedLightsInfo").get("power_led").copy()
                info["index"] = "power_led"
            elif arg[0] == "get_data_led_info":
                info = result.get("supportedLightsInfo").get("data_led").copy()
                info["index"] = "data_led"
            elif arg[0] == "get_record_led_info":
                info = result.get("supportedLightsInfo").get("record_led").copy()
                info["index"] = "record_led"

            if success and "FALSE" not in status and len(supported_leds):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_fp_or_clock_brightness":
            brightness = result.get("brightness")
            status = checkNonEmptyResultData(brightness)
            success = str(result.get("success")).lower() == "true"
            info["brightness"] = brightness
            if len(arg) and arg[0] == "check_brightness_level":
                if success and status == "TRUE" and int(brightness) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_led_brightness":
            brightness = result.get("brightness")
            status = checkNonEmptyResultData(brightness)
            success = str(result.get("success")).lower() == "true"
            info["brightness"] = brightness
            if len(expectedValues) == 1:
                if success and status == "TRUE" and int(brightness) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE" and int(brightness) >= int(expectedValues[0]) and int(brightness) <= int(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_clock_mode":
            info["is24Hour"] = result.get("is24Hour")
            success = str(result.get("success")).lower() == "true"
            expectedValues = [str(value).lower() for value in expectedValues]
            if success and str(result.get("is24Hour")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_set_operation_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "frontpanel_get_preferences":
            info["preferences"] = result.get("preferences")
            success = str(result.get("success")).lower() == "true"
            expectedValues = ",".join(expectedValues)
            expectedValues = json.loads(str(expectedValues))
            if success and expectedValues == result.get("preferences"):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # WebKitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_get_state":
            info["state"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_visibility":
            info["visibility"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "webkitbrowser_check_fps":
            if int(result) >= 0:
                info["fps"] = result
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "webkitbrowser_get_cookie_policy":
            info["cookie_accept_policy"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_local_storage_availability":
            info["enabled"] = result
            if str(result) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_languages":
            info["languages"] = result
            status = [ "FALSE" for lang in result if lang not in expectedValues ]
            if "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_useragent":
            info["useragent"] = result
            status = checkNonEmptyResultData(result)
            if len(arg) and arg[0] == "check_useragent":
                if status == "TRUE" and result in ",".join(expectedValues):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_headers":
            info["headers"] = result
            if len(result) > 0:
                status = []
                for data in result:
                    status.append(checkNonEmptyResultData(list(data.values())))
                if len(arg) and arg[0] == "check_header":
                    if "FAILURE" not in status and data.get("name") in expectedValues and data.get("value") in expectedValues:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    if "FAILURE" not in status:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_check_url":
            info["url"] = result
            if len(arg) and arg[0] == "check_loaded_url":
                status = checkNonEmptyResultData(result)
            else:
                status = compareURLs(result,expectedValues[0])
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # Cobalt Plugin Response result parser steps
        elif tag == "cobalt_get_state":
            info["state"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "cobalt_validate_accessibility_settings":
            status = checkNonEmptyResultData(result)
            closedcaptions = result.get("closedcaptions")
            textdisplay = result.get("textdisplay")
            for key,value in list(closedcaptions.items()):
                info[key] = value
            info["ishighcontrasttextenabled"] = textdisplay.get("ishighcontrasttextenabled")
            if status and str(closedcaptions.get("isenabled")).lower() == str(expectedValues[0]).lower() and closedcaptions.get("backgroundcolor") == expectedValues[1] and closedcaptions.get("backgroundopacity") == expectedValues[2] and closedcaptions.get("characteredgestyle") == expectedValues[3] and closedcaptions.get("fontcolor") == expectedValues[4] and closedcaptions.get("fontfamily") == expectedValues[5] and closedcaptions.get("fontopacity") == expectedValues[6] and closedcaptions.get("fontsize") == expectedValues[7] and closedcaptions.get("windowcolor") == expectedValues[8] and closedcaptions.get("windowopacity") == expectedValues[9] and str(textdisplay.get("ishighcontrasttextenabled")).lower() == str(expectedValues[10]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Device Diagnostics Plugin Response parser steps
        elif tag == "devicediagnostics_get_configurations":
            params_info = result.get("paramList")
            status = []
            params_detail = []
            success = str(result.get("success")).lower() == "true"
            for param in params_info:
                detail = []
                detail.append(param.get("name"))
                detail.append(param.get("value"))
                status.append(checkNonEmptyResultData(detail))
                params_detail.append(str(detail[0]) + " - " + str(detail[1]))
            info["param_list"] = params_detail
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "devicediagnostics_get_avdecoder_status":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("avDecoderStatus")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # HDCP Profile Plugin Response result parser steps
        elif tag == "hdcpprofile_get_general_info":
            if arg[0] == "get_stb_hdcp_info":
                info = checkAndGetAllResultInfo(result,result.get("success"))
            elif arg[0] == "get_hdcp_status":
                info = checkAndGetAllResultInfo(result.get("HDCPStatus"),result.get("success"))
                if str(info["isConnected"]).lower() == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                    if str(info["isConnected"]).lower() == "false" and str(info["isHDCPCompliant"]).lower() != "false":
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "get_hdcp_status_without_tv":
                info = checkAndGetAllResultInfo(result.get("HDCPStatus"),result.get("success"))
                if str(info["isConnected"]).lower() == expectedValues[0] and str(info["isHDCPCompliant"]).lower() == expectedValues[0] and str(info["isHDCPEnabled"]).lower() == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # System Plugin Response result parser steps
        elif tag =="system_check_mfg_serial_number":    
            info["mfgSerialNumber"] = result.get('mfgSerialNumber')
            info["success"] = result.get('success')
            if str(result.get('success')).lower() == "true" and len(result.get('mfgSerialNumber')) != 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"    
        
        elif tag == "system_validate_territory_region":
            info["territory"] = result.get('territory')
            info["region"] = result.get('region')
            info["success"] = result.get('success')
            if len(arg) and arg[0] == "checksystem":
                if str(result.get('success')).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get('success')).lower() == "true" and len(result.get('territory')) != 0 and len(result.get('region')) != 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_set_territory":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_api_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "system_get_xconf_info":
            info = checkAndGetAllResultInfo(result.get("xconfParams"),result.get("success"))

        elif tag == "system_check_uptime":
            info["systemUptime"] = result.get("systemUptime")
            success = str(result.get("success")).lower() == "true"
            if success and int(float(result.get("systemUptime"))) <= int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_rfc_info":
            info = checkAndGetAllResultInfo(result.get("RFCConfig"),result.get("success"))
            if len(arg) and arg[0] == "check_expected_value":
                rfc_value = list(result.get("RFCConfig").values())[0]
                if str(rfc_value).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                rfc_values = list(result.get("RFCConfig").values())
                for rfc_data in rfc_values:
                    if "ERROR" in rfc_data or "error" in rfc_data:
                        info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_validate_empty_rfclist":
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_gz_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_cache":
            if str(result.get("success")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_cache_key":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if result.get(expectedValues[0]) == str(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_power_state":
            powerState = result.get("powerState")
            info["powerState"] = powerState
            success = str(result.get("success")).lower() == "true"
            if success and powerState in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_available_standby_modes":
            supportedStandbyModes = result.get("supportedStandbyModes")
            status = checkNonEmptyResultData(supportedStandbyModes)
            success = str(result.get("success")).lower() == "true"
            info["supportedStandbyModes"] = supportedStandbyModes
            if len(arg) and arg[0] == "check_mode":
                if success and status == "TRUE" and all( mode in supportedStandbyModes for mode in expectedValues ):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_preferred_standby_mode":
            preferredStandbyMode = result.get("preferredStandbyMode")
            success = str(result.get("success")).lower() == "true"
            info["standbyMode"] = preferredStandbyMode
            if success and preferredStandbyMode in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_timezone_dst":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_timezone":
                if info.get("timeZone") in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_state_info":
            if len(arg):
                info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            else:
                info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "system_validate_core_temperature":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(float(result.get("temperature"))) > 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_validate_modes":
            mode_info = result.get("modeInfo")
            info = checkAndGetAllResultInfo(mode_info,result.get("success"))
            if str(mode_info.get("mode")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_validate_bool_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            status = str(result.get(arg[0])).lower()
            if status in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_verify_thresholds_params":
            success = str(result.get("success")).lower() == "true"
            result = result.get("temperatureThresholds")
            info["WARN"] = result.get("WARN")
            info["MAX"] =  result.get("MAX")
            if len(arg) and arg[0] == "validate_threshold_params":
                if success and float(result.get("WARN")) == float(expectedValues[0]) and float(result.get("MAX")) == float(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag== "system_check_mac_address":
            if arg[0] == "bluetooth_mac":
                info["bluetooth_mac"] = result.get("bluetooth_mac")
                macAddress = result.get("bluetooth_mac")
                success = str(result.get("success")).lower() == "true"
                status = checkNonEmptyResultData(result.get("bluetooth_mac"))
            elif arg[0] == "wifi_mac":
                info["wifi_mac"] = result.get("wifi_mac")
                macAddress = result.get("wifi_mac")
                success = str(result.get("success")).lower() == "true"
                status = checkNonEmptyResultData(result.get("wifi_mac"))
            if success and status == "TRUE":
                if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is None:
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_validate_powerstate_before_reboot":
            powerState = result.get("state")
            info["powerState"] = powerState
            success = str(result.get("success")).lower() == "true"
            if success:
                if "STANDBY" in expectedValues or "LIGHT_SLEEP" in expectedValues:
                    if powerState in ["STANDBY","LIGHT_SLEEP"]:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif powerState in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_telemetry_optout_status":
            success = str(result.get("success")).lower() == "true"
            info["Opt-Out"] = result.get("Opt-Out")
            if success and str(result.get("Opt-Out")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_get_downloaded_firmware_info":
            currentFWVersion = result.get("currentFWVersion")
            info["current_FW_version"] = currentFWVersion
            status = checkNonEmptyResultData(result.get("currentFWVersion"))
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_image":
                if success and status == "TRUE" and currentFWVersion in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if  success and status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_custom_reboot_reason":
            info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            result = result.get(arg[0])
            if result.get("customReason") in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_get_moca_enabled_status":
            info["mocaEnabled"] = result.get("mocaEnabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("mocaEnabled")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_verify_interval_value":
            info["graceInterval"] = result.get("graceInterval")
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_expected_interval":
                if success and str(result.get("graceInterval")).lower() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and str(result.get("graceInterval")):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_platform_configurations":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            if status == "TRUE" and success:
                if len(arg) and arg[0] == "check_model_number":
                    deviceInfo = result.get("DeviceInfo")
                    info["MODEL_NUMBER"] = deviceInfo.get("model")
                    deviceDetail = deviceInfo.get("model")
                elif len(arg) and arg[0] == "check_devicetype":
                    deviceInfo = result.get("DeviceInfo")
                    info["deviceType"] = deviceInfo.get("deviceType")
                    deviceDetail = deviceInfo.get("deviceType")
                elif len(arg) and arg[0] == "check_device_mac_address":
                    accountInfo = result.get("AccountInfo")
                    info["deviceMACAddress"] = accountInfo.get("deviceMACAddress")
                    deviceDetail = accountInfo.get("deviceMACAddress")
                elif len(arg) and arg[0] == "check_webbrowser_details":
                    deviceInfo = result.get("DeviceInfo")
                    webBrowser = deviceInfo.get("webBrowser")
                    deviceDetail = webBrowser.get("userAgent")
                    expectedValues[0] = ",".join(expectedValues)
                    info["userAgent"] = webBrowser.get("userAgent")
                    info["browserType"] = webBrowser.get("browserType")
                    info["version"] = webBrowser.get("version")
                elif len(arg) and arg[0] == "check_firmware_upgrade_status":
                    accountInfo = result.get("AccountInfo")
                    info["firmwareUpdateDisabled"] = accountInfo.get("firmwareUpdateDisabled")
                    deviceDetail = accountInfo.get("firmwareUpdateDisabled")
                elif len(arg) and arg[0] == "check_public_ip_address":
                    deviceInfo = result.get("DeviceInfo")
                    info["publicIP"] = deviceInfo.get("publicIP")
                    deviceDetail = deviceInfo.get("publicIP")
                if str(deviceDetail).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_check_hdr_capabilities":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            if status == "TRUE" and success:
                deviceInfo = result.get("DeviceInfo")
                info["HdrCapability"] = deviceInfo.get("HdrCapability")
                deviceDetail = deviceInfo.get("HdrCapability")
                HdrCapability = str(deviceDetail).lower().split(",")
                result_status = [ "FALSE" for value in expectedValues if value.lower()  not in HdrCapability ]
                if "FALSE" not in result_status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_get_network_standby_mode_status":
            info["nwStandby"] = result.get("nwStandby")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("nwStandby")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_get_time_zones_list":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
                getcountofelements(result.get("zoneinfo"))
                message = "Selecting 5 timezones out of %d zone info" %(len(timeZones))
                info["Test_Step_Message"] = message
                info["zoneinfo"] = random.sample(timeZones,5)
                del timeZones[:]
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_negative_scenario":
            info = result
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "system_check_friendly_name":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_name":
                if result.get("friendlyName") in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
 
        elif tag == "system_check_error_message":
            success = str(result.get("success")).lower() == "false"
            info["success"] = result.get("success")
            if len(arg) and arg[0] == "errorMessage":
                if "errorMessage" in result:
                    output = str(result.get("errorMessage")).strip()
                    info["errorMessage"] = output
                    if success and expectedValues[0].lower() in output.lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    output = str(result.get("message")).strip()
                    info["message"] = output
                    if success and expectedValues[0].lower() in output.lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                result = result.get("error")
                info["message"] = result.get("message")
                if success and str(result.get("message")).lower() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "system_validate_image_version":
            imageVersion = result.get('imageVersion')
            success = result.get('success')
            info["imageVersion"] = imageVersion
            info["success"] = success
            if imageVersion and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # User Preferces Plugin Response result parser steps
        elif tag == "userpreferences_get_ui_language":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_language":
                if result.get("ui_language") == expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "userpreferences_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        #Code for RDK Shell plugin
        elif tag =="rdkshell_get_cursor_size":
            #Check result value empty or not
            info = checkAndGetAllResultInfo(result)
            #Check cursor width and height not equal to zero
            if result.get('width') and result.get('height') != 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            #Validate cursor size
            if len(arg) and arg[0] == "check_cursor_size":
                integer_list = []
                for x in expectedValues:
                    #Remove unwanted symbols in expectedvalues
                    x = x.replace("[","").replace("]","").replace(" ","")
                    integer_list.append(int(x))
                if str(result.get("success")).lower() == "true" and int(result.get('width')) in integer_list and int(result.get('height')) in integer_list:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "rdkshell_get_connected_client_list":
            result = result.get("clients")
            clients = [ str(name) for name in result if str(name).strip() ]
            info["clients"] = clients
            #Minimum two clients have to be running to effectivly perform RDK Shell test cases
            if len(clients) >= 2:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_result_status":
            success = result.get("success")
            info["success"] = success
            if str(success).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_for_results":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "rdkshell_check_for_visibility_result":
            if len(expectedValues) > 1 :
                if str(result.get("visible")).lower() in str(expectedValues[0]).lower() or str(result.get("visible")).lower() in str(expectedValues[1]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif str(result.get("visible")).lower() in str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # read previously set resolution and compare it
        elif tag == "rdkshell_check_for_resolution_set":
            w = int(result.get("w"))
            h = int(result.get("h"))
            expectedw = int(expectedValues[0])
            expectedh = int(expectedValues[1])
            if w == expectedw and h == expectedh:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_for_bounds":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            result=result.get("bounds")
            info["x"]=str(result.get("x"))
            info["y"]=str(result.get("y"))
            info["w"]=str(result.get("w"))
            info["h"]=str(result.get("h"))
            if len(expectedValues)>0:
                x = str(result.get("x"))
                y = str(result.get("y"))
                w = str(result.get("w"))
                h = str(result.get("h"))
                expectedx = expectedValues[0]
                expectedy = expectedValues[1]
                expectedw = expectedValues[2]
                expectedh = expectedValues[3]
                if x == expectedx and  y == expectedy and  w == expectedw and  h == expectedh:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_validate_opacity":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            status = result.get("opacity")
            if len(expectedValues)>0:
                if int(expectedValues[0]) == int(status):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif int(status) >= 0 and int(status) <=100 :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_verify_scale_params":
            if float(result.get("sx")) == float(expectedValues[0]) and float(result.get("sy")) == float(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_application":
            result = result.get("clients")
            clients = [ str(name) for name in result if str(name).strip() ]
            info["clients"] = clients
            if arg[0] == "check_not_exists" or arg[0] == "check_if_not_exists":
                if expectedValues[0] not in clients:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "check_if_exists":
                if expectedValues[0] in clients:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_multiple_application":
            info["clients"] = result.get("clients")
            clients = result.get("clients")
            appStatus = 0
            if len(arg) and arg[0] == "check_if_exists":
                for app in expectedValues:
                    if app not in clients:
                        appStatus = 1
                if appStatus == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_state":
            success = str(result.get("success")).lower() == "true"
            result = result.get("state")
            for data in result:
                if(data.get("callsign")) == str(arg[0]):
                    break;
            if success and data.get("callsign") ==  str(arg[0]) and str(data.get("state")) in expectedValues:
                info["callsign"] = data.get("callsign")
                info["state"] = data.get("state")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_log_level":
            success = str(result.get("success")).lower() == "true"
            info["LogLevel"] = result.get("logLevel")
            if success and str(result.get("logLevel")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_hole_punch":
            success = str(result.get("success")).lower() == "true"
            info["holePunch"] = result.get("holePunch")
            if success and str(result.get("holePunch")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_validate_topmost_client":
            success = str(result.get("success")).lower() == "true"
            TopMostClient = result.get("clients")[0]
            info["TopMostClient"] = result.get("clients")[0]
            if success and TopMostClient in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_key_repeats_status":
            success = str(result.get("success")).lower() == "true"
            info["enable"] = result.get("keyRepeat")
            if success and str(result.get("keyRepeat")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_enabled_status":
            success = str(result.get("success")).lower() == "true"
            info["enabled"] = result.get("enabled")
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_get_virtual_resolution":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            info["width"] = result.get("width")
            info["height"] = result.get("height")
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and  arg[0] == "check_virtual_resolutions":
                if success and str(result.get("width")) == str(expectedValues[0]) and  str(result.get("height")) == str(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_error_message":
            success = str(result.get("success")).lower() == "false"
            info["message"] = result.get("message")
            if success and str(result.get("message")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_zorder":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if success and status == "TRUE":
                result = result.get("clients")
                clients = [ str(name) for name in result if str(name).strip() ]
                info["Excluded_Process_List"] = arg
                clients = [ element for element in clients if element not in arg ]
                info["clients"] = clients
                #Minimum two clients have to be running to effectivly perform RDK Shell test cases
                if len(clients) >= 2:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_validate_zorder":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if success and status == "TRUE":
                result = result.get("clients")
                clients = [ str(name) for name in result if str(name).strip() ]
                processList = list(arg)
                processList.pop(0)
                clients = [ element for element in clients if element not in processList ]
                info["clients"] = clients
                if len(arg) and arg[0] == "validate_move_to_front":
                    if str(clients[0]).lower() == str(expectedValues[0]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif len(arg) and arg[0] == "validate_move_to_back":
                    index = (len(clients)-1)
                    if str(clients[index]).lower() == str(expectedValues[0]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif len(arg) and arg[0] == "validate_move_to_behind":
                    if str(clients[1]).lower() == str(expectedValues[0]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif len(arg) and arg[0] == "validate_front_app_order":
                    if str(clients[0]).lower() != str(expectedValues[0]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_graphics_framerate":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            info["framerate"] = result.get("framerate")
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_expected_framerate":
                if int(result.get("framerate")) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "rdkshell_check_launchtype":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("launchType")).lower() == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DisplayInfo Plugin Response result parser steps
        elif tag == "displayinfo_get_general_info":
            if arg[0] == "get_all_info":
                info = checkAndGetAllResultInfo(result)

        elif tag == "displayinfo_check_for_nonempty_result":
            info["Result"] = result
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_results":
            info["Result"] = result
            if len(arg) and arg[0] == "check_width_height_in_centimeters":
                if result >= 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if result > 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_boolean_result":
            if str(result) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_width_or_height":
            if arg[0] == "width":
                index = 0
            elif arg[0] == "height":
                index = 1
            SupportingRes=expectedValues
            Resolution_Details = {}
            for values in range(1,len(arg)):
                mapping_details = arg[values].split(":")
                resolution = mapping_details[0]
                width = mapping_details[1].split('|')[0].strip('[]')
                height = mapping_details[1].split('|')[1].strip('[]')
                Resolution_Details[resolution] = [int(width),int(height)]
            search_key = int(result)
            #Create a sub dictionary of width and height pair from the SupportingRes keys.
            subdict=dict([(x,Resolution_Details[x]) for x in SupportingRes])

            #Get matching width_height pair for given width from the SupportingRes.
            width_height_pair = [val for key, val in list(subdict.items()) if search_key in val]
            #List of matching width/height list based on index
            sub_list = [item[index] for item in width_height_pair]
            if search_key in sub_list :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_hdr_formats":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Result"] = result
                status = [ "FALSE" for form in result if form not in expectedValues ]
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_validate_expected_results":
            status = checkNonEmptyResultData(result)
            if status == "TRUE":
                info["Result"] = result
                expectedValues = [ value.lower() for value in expectedValues]
                if len(arg) and arg[0] == "check_colorimetry":
                    result = [ value.lower() for value in result]
                    colorimetry_status = [ "FALSE" for value in result if value not in expectedValues ]
                    if "FALSE" not in colorimetry_status:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    if str(result).lower() in expectedValues:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displayinfo_check_edid_result":
            info = checkAndGetAllResultInfo(result)
            EDID = result.get("data")
            if str(EDID) == str(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        # Parser Code for ActivityMonitor plugin
        elif tag == "activitymonitor_check_applications_memory":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            app_list=result.get("applicationMemory")
            status = []
            if len(app_list) > 0:
                for app_info in app_list:
                    status.append(checkNonEmptyResultData(app_info.values))
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "activitymonitor_validate_result":
            if len(arg) > 0:
                info = checkAndGetAllResultInfo(result.get(arg[0]),result.get("success"))
            else:
                info = checkAndGetAllResultInfo(result,result.get("success"))

        # Parser Code for HDMICEC plugin
        elif tag == "hdmicec_get_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "hdmicec_validate_boolean_result":
            if str(result.get("status")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec_get_cec_addresses":
            cec_addresses = result.get("CECAddresses")
            if arg[0] == "get_logical_address":
                success = str(result.get("success")).lower() == "true"
                info["logicalAddress"] =  cec_addresses.get("logicalAddress")
                info["deviceType"] =  cec_addresses.get("deviceType")
                if len(cec_addresses) > 0:
                    logical_Address_value = cec_addresses.get("logicalAddress")
                    Device_Type_value = cec_addresses.get("deviceType")
                    if logical_Address_value  not in [15,255] and logical_Address_value == int(expectedValues[0]) and  Device_Type_value == expectedValues[1] and  success:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["logicalAddresses"] = cec_addresses
                    info["Test_Step_Status"] = "FAILURE"

            elif arg[0] == "get_physical_address":
                physical_address = cec_addresses.get("physicalAddress")
                status = checkNonEmptyResultData(cec_addresses.get("physicalAddress"))
                physical_address_hex_format = hex(physical_address)
                info["physicalAddress"] = physical_address
                info["physical_address_hex_format"] = physical_address_hex_format
                physical_address_hex_format = physical_address_hex_format[2:]
                if status == "TRUE" and str(result.get("success")).lower() == "true":
                    if expectedValues[0] == "true" and  str(physical_address_hex_format) != "ffff":
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        #Parser code for HdmiCecSink plugin
        elif tag == "hdmicecsink_check_active_source_and_route_details":
            info["AVAILABLE"] = result.get("available")
            success = str(result.get("success")).lower() == "true"
            if str(result.get("available")).lower() == "true" and success:
                if arg[0] == "get_logical_address":
                    if len(arg) > 1 and arg[1] == "active_route":
                        values = result.get("pathList")
                        logicalAddress = values[0].get("logicalAddress")
                        deviceType = values[0].get("deviceType")
                    else:
                        logicalAddress = result.get("logicalAddress")
                        deviceType = result.get("deviceType")
                    info["logicalAddress"] = logicalAddress
                    info["deviceType"] =  deviceType
                    if logicalAddress  not in [15,255] and logicalAddress == int(expectedValues[0]) and deviceType.lower() == expectedValues[1].lower() and  success:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif arg[0] == "get_physical_address":
                    if len(arg) > 1 and arg[1] == "active_route":
                        hdmiPort = str(result.get("ActiveRoute"))
                        physical_address = result.get("pathList")
                        physical_address = physical_address[0].get("physicalAddress")
                    else:
                        physical_address = result.get("physicalAddress")
                        hdmiPort = str(result.get("port"))
                    hdmiPort = int(hdmiPort[len(hdmiPort)-1])
                    hdmiPort += 1
                    status = checkNonEmptyResultData(result)
                    info["physicalAddress"] = physical_address
                    expectedAddress = str(hdmiPort)+'.0.0.0'
                    if status == "TRUE":
                        if  physical_address == expectedAddress and physical_address != "15.15.15.15":
                            info["Test_Step_Status"] = "SUCCESS"
                        else:
                            info["Test_Step_Status"] = "FAILURE"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif arg[0] == "get_cec_version":
                    cecVersion = result.get("cecVersion")
                    info["cecVersion"] = cecVersion
                    status = checkNonEmptyResultData(cecVersion)
                    if status == "TRUE" and str(cecVersion).lower() != "unknown":
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif arg[0] == "get_vendor_id":
                    if len(arg) > 1 and arg[1] == "active_route":
                        vendorID = result.get("pathList")
                        vendorID  = vendorID[0].get("vendorID")
                    else:
                        vendorID = result.get("vendorID")
                    info["vendorID"] = vendorID
                    status = checkNonEmptyResultData(vendorID)
                    if status == "TRUE" and str(vendorID).lower() != "000":
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif arg[0] == "get_power_status":
                    info["powerStatus"] = result.get("powerStatus")
                    if str(result.get("powerStatus")).lower() == expectedValues[0].lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif arg[0] == "get_osd_name":
                    if len(arg) > 1 and arg[1] == "active_route":
                        osdName = result.get("pathList")
                        osdName = osdName[0].get("osdName")
                    else:
                        osdName = result.get("osdName")
                    info["osdname"] = osdName
                    if str(osdName).lower() == expectedValues[0].lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "hdmicecsink_get_vendor_id":
            success = str(result.get("success")).lower() == "true"
            vendorID = result.get("vendorid")
            info["vendorID"] = vendorID
            status = checkNonEmptyResultData(vendorID)
            if status == "TRUE" and str(vendorID).lower() != "000":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "hdmicecsink_get_osd_name":
            success = str(result.get("success")).lower() == "true"
            info["OSDNAME"] = result.get("name")
            status = checkNonEmptyResultData(result.get("name"))
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "hdmicecsink_check_audio_connected_status":
            success = str(result.get("success")).lower() == "true"
            info["connected"] = result.get("connected")
            if str(result.get("connected")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "hdmicecsink_check_device_list":
            info["devicelist"] = result.get("deviceList")
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if len(arg) and arg[0] == "empty_check":
                if success and status == "TRUE" and int(result.get("numberofdevices")) == 0 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and status == "TRUE" and int(result.get("numberofdevices")) > 0 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "hdmicecsink_set_operation_status":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        #Parser code for State Observer plugin
        elif tag == "StateObserver_validate_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "StateObserver_validate_version":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            version=result.get("version")
            if len(arg) and arg[0] == "check_version":
                if int(float(version)) > 0 and int(float(version)) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if int(float(version)) > 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "StateObserver_validate_name":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            name=result.get("Name")
            if str(expectedValues[0]).lower() in str(name).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "StateObserver_get_property_info":
            property_info = result.get("properties")
            status = []
            success = str(result.get("success")).lower() == "true"
            for property_data in property_info:
                status.append(checkNonEmptyResultData(list(property_data.values())))
            info["properties"] = property_info
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "stateobserver_check_registered_property_names":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            property_info = result.get("properties")
            success = str(result.get("success")).lower() == "true"
            status = "TRUE"
            for property_data in property_info:
                if property_data not in expectedValues:
                    status = "FALSE"
            info["properties"] = property_info
            if success and "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Display Settings Plugin Response result parser steps
        elif tag == "displaysettings_get_associated_audio_mixing":
            info["mixing"] = result.get('mixing')
            info["success"] = result.get('success')
            if len(arg) and arg[0] == "check_audio_mixing":
                if str(result.get("success")).lower() == "true" and str(result.get('mixing')).lower() == str(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and result.get("mixing") is not None:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "displaysettings_set_associated_audio_mixing":
            info["success"] = result.get('success')
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "displaysettings_get_fader_control":
            info["mixerBalance"] = result.get('mixerBalance')
            info["success"] = result.get('success')
            if len(arg) and arg[0] == "check_fader_control":
                if str(result.get("success")).lower() == "true" and int(result.get('mixerBalance')) == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and -32 <= int(result.get('mixerBalance')) <= 32:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "displaysettings_set_fader_control":
            info["success"] = result.get('success')
            if len(arg) and arg[0] == "check_negative_fader_control":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_is_connected":
            info["video_display"] = result.get('connectedVideoDisplays')
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('connectedVideoDisplays'))
            if success and status == "TRUE":
                info["is_connected"] = "true"
                info["Test_Step_Status"] = "SUCCESS"
            elif success and status == "FALSE":
                info["is_connected"] = "false"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_tv_connected":
                if "true" in info["is_connected"]:
                    info["Test_Step_Status"] = "FAILURE"
                    message = "Please test after disconnecting the TV"
                    info["Test_Step_Message"] = message
                else:
                    info["Test_Step_Status"] = "SUCCESS"
            elif len(arg) and arg[0] == "check_tv_not_connected":
                if "true" in info["is_connected"]:
                    info["Test_Step_Status"] = "FAILURE"
                    message = "Connected video displays list should be empty when TV is not connected"
                    info["Test_Step_Message"] = message
                else:
                    info["Test_Step_Status"] = "SUCCESS"

        elif tag == "display_settings_check_set_operation":
            info["success"] = result.get("success")
            if len(arg) and arg[0] == "check_set_failed":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            else:
                if str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_connected_status":
            info["video_display"] = result.get('connectedVideoDisplays')
            if len(arg):
                if arg[0].lower() != "true":
                    if json.dumps(result.get('success')) == "true" and result.get('connectedVideoDisplays'):
                        info["Test_Step_Status"] = "FAILURE"
                    else:
                        info["Test_Step_Status"] = "SUCCESS"
                else:
                    if json.dumps(result.get('success')) == "true" and result.get('connectedVideoDisplays'):
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                if json.dumps(result.get('success')) == "true" and  result.get('connectedVideoDisplays'):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_resolutions":
            info["supportedSettopResolutions"] = result.get('supportedSettopResolutions')
            if collections.Counter(result.get('supportedSettopResolutions')) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_tv_resolutions":
            info["supportedTvResolutions"] = result.get('supportedTvResolutions')
            if json.dumps(result.get("success")) == "true" and any(item not in result.get('supportedTvResolutions') for item in ["none"]) :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "display_supported_resolutions":
            info["supportedResolutions"] = result.get('supportedResolutions')
            if json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_current_resolution":
            info["resolution"] = result.get('resolution')
            if json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_expected_resolution":
                if result.get('resolution') in expectedValues and json.dumps(result.get("success")) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_resolution_not_persisted":
                defaultResolution = str(expectedValues[0])
                info["defaultResolution"] = defaultResolution
                if defaultResolution == str(expectedValues[1]):
                    if str(result.get('resolution')) and json.dumps(result.get("success")) == "true":
                        info["Test_Step_Status"] = "SUCCESS"
                elif result.get('resolution') != str(expectedValues[1]) and json.dumps(result.get("success")) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_video_displays":
            info["supportedVideoDisplays"] = result.get('supportedVideoDisplays')
            if json.dumps(result.get('success')) == "true" and collections.Counter((result.get('supportedVideoDisplays'))) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_audio_ports":
            info["audio_port"] = result.get('supportedAudioPorts')
            if collections.Counter(result.get('supportedAudioPorts')) == collections.Counter(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_empty_audio_ports":
            connectedAudioPorts = result.get('connectedAudioPorts')
            success = result.get('success')
            info["supportedAudioPorts"] = connectedAudioPorts
            info["success"] = success
            if str(success).lower() == "true" and arg[0] not in connectedAudioPorts:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "Please test after disconnecting the TV"
                info["message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_HDR_support":
            info["supportsHDR"] = result.get('supportsHDR')
            if json.dumps(result.get('supportsHDR')).upper()in json.dumps(expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_TV_HDR_support":
            info["TVsupportsHDR"] = result.get('supportsHDR')
            if json.dumps(result.get('supportsHDR')) == "true" and any(item not in result.get('standards') for item in ["none"]) :
                info["Test_Step_Status"] = "SUCCESS"
            elif json.dumps(result.get('supportsHDR')) == "false" and any(item in result.get('standards') for item in ["none"]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_host_edid":
            info["host_edid"] = result.get('EDID')
            if json.dumps(result.get('EDID')) and json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_connected_device_edid":
            if len(arg) and arg[0] == "check_edid_status_for_disconnected_device":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["connected_device_edid"] = result.get('EDID')
                if json.dumps(result.get('EDID')) and json.dumps(result.get("success")) == "true" :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_connected_audio_ports":
            if len(arg) and arg[0] == "check_value":
                info["connected_audio_port"] = result.get('connectedAudioPorts')
                status = checkNonEmptyResultData(result)
                if "FALSE" not in status and json.dumps(result.get('success')) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["connected_audio_port"] = result.get('connectedAudioPorts')
                if json.dumps(result.get('success')) == "true" and str(expectedValues[0]) in result.get('connectedAudioPorts'):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_audio_modes":
            info["supported_audio_modes"] = result.get('supportedAudioModes');
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('supportedAudioModes'))
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_hdmi0_audio_modes":
                status = "TRUE"
                expectedValues = [ str(mode).lower() for mode in expectedValues ]
                for soundMode in  result.get('supportedAudioModes'):
                    if "AUTO" in soundMode:
                        soundMode = re.search(r"\((.*?)\)",soundMode).group(1)
                    if str(soundMode).lower() not in expectedValues:
                        status = "FALSE"
                        break
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_sound_mode":
            soundMode = result.get('soundMode')
            info["soundMode"] = soundMode
            if len(arg) and arg[0] == "check_expected_sound_mode":
                if "AUTO" in expectedValues:
                    for Mode in arg:
                        if "AUTO" in Mode:
                            expectedMode = Mode.lower()
                            break
                else:
                    expectedMode = str(expectedValues[0]).lower()
                if result.get('soundMode').lower() == expectedMode or expectedMode in result.get('soundMode').lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and result.get('soundMode') in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_zoom_settings":
            info["zoomSetting"] = result.get('zoomSetting');
            if str(result.get("success")).lower() == "true" and result.get('zoomSetting') in expectedValues :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_current_output_settings":
            info["colorSpace"] = result.get('colorSpace')
            info["colorDepth"] = result.get('colorDepth')
            info["matrixCoefficients"] = result.get('matrixCoefficients')
            info["videoEOTF"] = result.get('videoEOTF')
            if str(result.get("success")).lower() == "true" and result.get('colorSpace') in [0,1,2,3,4,5] and result.get('matrixCoefficients') in [0,1,2,3,4,5,6,7] :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_active_input":
            info ["activeInput"] = result.get('activeInput')
            info ["success"] = result.get('success')
            if len(arg) and arg[0] == "check_for_invalid_port":
                if str(result.get("success")).lower() == "false" and str(result.get('activeInput')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('activeInput')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_MS12_audio_compression":
            info["compresionLevel"] = result.get('compressionlevel');
            if str(result.get("success")).lower() == "true" and str(result.get('compressionlevel')) in expectedValues :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_video_port_status_standby":
            if len(arg) and arg[0] == "check_for_invalid_port":
                info = checkAndGetAllResultInfo(result)
                if str(result.get("success")).lower() == "false" and result.get('error_message').lower() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["enabled"] = result.get('videoPortStatusInStandby');
                if str(result.get("success")).lower() == "true" and str(result.get('videoPortStatusInStandby')) in expectedValues :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_dolby_volume_mode":
            info["dolbyVolumeMode"] = result.get('dolbyVolumeMode');
            if str(result.get("success")).lower() == "true" and str(result.get('dolbyVolumeMode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_dialog_enhancement":
            info["enhancerlevel"] = result.get('enhancerlevel');
            if str(result.get("success")).lower() == "true" and str(result.get('enhancerlevel')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_intelligent_equalizer_mode":
            info["intelligentEqualizerMode"] = result.get('mode');
            if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_volume_leveller":
            info["level"] = result.get('level')
            info["mode"] = result.get('mode')
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_expected_values":
                if success and str(result.get('mode')) in expectedValues[0] and str(result.get('level')) in expectedValues[1]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_volume_leveller_mode":
                if success and str(result.get('mode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and str(result.get('level')) in expectedValues and int(result.get('mode')) in [0,1,2]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_bass_enhancer":
            info["bassBoost"] = result.get('bassBoost');
            if len(arg) and arg[0] == "check_bass_range":
                if 0 <= int(result.get('bassBoost')) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('bassBoost')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_surround_virtualizer":
            info["boost"] = result.get('boost')
            info["mode"] = result.get('mode')
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_surround_virtualizer_range":
                if success and 0 <= int(result.get('boost')) <= 96 and int(result.get('mode')) in [0,1,2]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_surround_virtualizer_mode":
                if success and str(result.get('mode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and str(result.get('boost')) in expectedValues[1] and str(result.get('mode')) in expectedValues[0]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_mi_steering":
            info["MISteeringEnable"] = result.get('MISteeringEnable');
            if str(result.get("success")).lower() == "true" and str(result.get('MISteeringEnable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_surround_decoder":
            info["surroundDecoderEnable"] = result.get('surroundDecoderEnable');
            if str(result.get("success")).lower() == "true" and str(result.get('surroundDecoderEnable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_drc_mode":
            if result.get('DRCMode').lower() == "line":
                DRCMode = 0
                message = "DRCMode => line-0"
            elif result.get('DRCMode').lower() == "rf":
                DRCMode = 1
                message = "DRCMode => RF-1"
            info["DRCMode"] = DRCMode
            info["Test_Step_Message"] = message
            if len(arg) and arg[0] == "validate_drc_mode":
                if str(result.get("success")).lower() == "true" and DRCMode == int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('DRCMode')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_volume_level":
            info["volumeLevel"] = result.get('volumeLevel');
            if len(arg) and arg[0] == "check_volume_level_range":
                if 0 <= int(float(result.get('volumeLevel'))) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(int(float(result.get('volumeLevel')))) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_gain":
            info["gain"] = result.get('gain');
            if len(arg) and arg[0] == "check_gain_range":
                if 0 <= float(result.get('gain')) <= 100 :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if int(expectedValues[0])== 0 and int(float(result.get('gain')))== 2 and str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"

                elif str(result.get("success")).lower() == "true" and str(int(float(result.get('gain')))) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_muted":
            info["muted"] = str(result.get('muted'));
            if str(result.get("success")).lower() == "true" and str(result.get('muted')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_delay":
            info["audioDelay"] = result.get('audioDelay');
            if len(arg) and arg[0] == "check_audio_delay_range":
                if 0 <= int(result.get('audioDelay')):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('audioDelay')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_delay_offset":
            info["audioDelayOffset"] = result.get('audioDelayOffset');
            if len(arg) and arg[0] == "check_audio_delay_offset_range":
                if 0 <= int(result.get('audioDelayOffset')):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('audioDelayOffset')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_sink_atmos_capability":
            info["atmos_capability"] = result.get('atmos_capability');
            if str(result.get("success")).lower() == "true" and str(result.get('atmos_capability')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_tv_hdr_capabilities":
            info["capabilities"] = result.get('capabilities')
            if str(result.get("success")).lower() == "true" and int(result.get('capabilities')) >= 0:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_device_repeater":
            info["HdcpRepeater"] = result.get('HdcpRepeater')
            if str(result.get("success")).lower() == "true" and str(result.get('HdcpRepeater')).lower() == expectedValues[0].lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_default_resolution" :
            info["defaultResolution"] = result.get('defaultResolution')
            if str(result.get("success")).lower() == "true" and str(result.get('defaultResolution')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_MS12_Audio_Profiles":
            info["supportedMS12AudioProfiles"] = result.get('supportedMS12AudioProfiles')
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get('supportedMS12AudioProfiles'))
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_profile":
            info["ms12AudioProfile"] = result.get('ms12AudioProfile')
            if str(result.get("success")).lower() == "true" and str(result.get('ms12AudioProfile')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "check_audio_port_status":
            info["enable"] = result.get('enable')
            if str(result.get("success")).lower() == "true" and str(result.get('enable')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_graphic_equalizer_mode":
            info["graphicEqualizerMode"] = result.get('mode')
            if str(result.get("success")).lower() == "true" and str(result.get('mode')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_audio_capabilities":
            info["audioCapabilities"] = result.get('AudioCapabilities')
            status = checkNonEmptyResultData(result)
            audioCapabilities = [value.lower() for value in result.get('AudioCapabilities')]
            audioCapabilities_status = [ "FALSE" for value in expectedValues if value.lower() not in audioCapabilities ]
            if status == "TRUE" and "FALSE" not in  audioCapabilities_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_settop_supported_ms12_capabilities":
            info["ms12Capabilities"] = result.get('MS12Capabilities')
            status = checkNonEmptyResultData(result)
            ms12Capabilities = [value.lower() for value in result.get('MS12Capabilities')]
            ms12Capabilities_status = [ "FALSE" for value in expectedValues if value.lower() not in ms12Capabilities ]
            if status == "TRUE" and "FALSE" not in  ms12Capabilities_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_supported_resolutions":
            supportedResolutions = result.get('supportedResolutions')
            info["supportedResolutions"] = supportedResolutions
            status = all(item in expectedValues for item in supportedResolutions)
            if status is True:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_audio_video_formats":
            if len(arg) and arg[0] == "get_video_format":
                info["supportedVideoFormat"] = supportedFormats = result.get("supportedVideoFormat")
                info["currentVideoFormat"] = currentFormat = result.get("currentVideoFormat")
            elif len(arg) and arg[0] == "get_audio_format":
                info["supportedAudioFormat"] = supportedFormats = result.get("supportedAudioFormat")
                info["currentAudioFormat"] = currentFormat = result.get("currentAudioFormat")
            status = checkNonEmptyResultData(result)
            if status == "TRUE" and currentFormat in supportedFormats:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_supported_color_depth_capabilities":
            status = checkNonEmptyResultData(result)
            supportedColorDepth = result.get('capabilities')
            info["supportedColorDepth"] = supportedColorDepth
            success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_color_depth":
            info["colorDepth"] = result.get('colorDepth')
            if json.dumps(result.get("success")) == "true" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_expected_color_depth":
                if result.get('colorDepth') in expectedValues and json.dumps(result.get("success")) == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_check_adapter_state":
            info = result.copy()
            state = int(result.get("state"))
            state_names = ["UNINSTALLED","DISABLED","DISCONNECTED","PAIRING","CONNECTING","CONNECTED","FAILED"]
            success = str(result.get("success")).lower() == "true"
            info["state_name"] = state_names[state]
            info["enable"] = "True" if state not in [0,6,1] else "False"
            if str(result.get("state")) in expectedValues:
                info["Test_Step_Status"] = "FAILURE"
                if arg[0] == "check_state_valid" and state not in [0,6]:
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "check_state_enabled" and state not in [0,6,1]:
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "check_connection_status" and state == 5:
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "check_state_disabled" and state == 1:
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_set_operation":
            if str(result.get("success")).lower() == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_save_clear_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(result.get("result")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "wifi_check_signal_threshold_change_status":
            if result.get('result') == 0:
                Enabled = True
                message = "Enabled => True-0"
            elif result.get('result') == 1:
                Enabled = False
                message = "Enabled => False-1"
            info["enabled"] = Enabled
            info["Test_Step_Message"] = message
            if len(arg) and arg[0] == "validate_signal_threshold":
                if str(result.get("success")).lower() == "true" and str(Enabled).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(result.get('result')) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_get_connected_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if arg[0] == "check_ssid":
                if str(result.get("success")).lower() == "true" and str(result.get("ssid")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_no_ssid":
                if str(result.get("success")).lower() == "true" and str(result.get("ssid"))=="":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_ssid_pairing":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if int(result.get("result")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_get_paired_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("success")).lower() == "true" and str(result.get("ssid")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "wifi_check_supported_security_modes":
            info["supported_security_modes"] = result.get("security_modes")
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
                
        # Bluetooth Plugin Response result parser steps
        elif tag == "bluetooth_validate_startscan":
            info["status"] = result.get("status")
            if str(result.get("success")).lower() == "true" and str(result.get("status")).lower() == "available":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_discoverable_status":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("discoverable")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_name":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_name":
                if result.get("name") in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_device_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            success = str(result.get("success")).lower() == "true"
            deviceInfo = result.get("deviceInfo")
            info["deviceInfo"] = deviceInfo
            status = checkNonEmptyResultData(deviceInfo)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_discovered_devices":
            discoveredDevices = result.get("discoveredDevices")
            info["discoveredDevices"] = discoveredDevices
            status = []
            devices = []
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "get_devices_info":
                for device_info in discoveredDevices:
                    status.append(checkNonEmptyResultData(device_info))
                    device_data = {}
                    device_data["deviceID"] = str(device_info.get("deviceID"))
                    device_data["name"] = str(device_info.get("name"))
                    device_data["deviceType"] = str(device_info.get("deviceType"))
                    devices.append(device_data)
                info["devices"] = devices
            elif len(arg) and arg[0] == "get_device_id":
                checkStatus = "FALSE"
                for device_info in discoveredDevices:
                    if str(device_info.get("name")) in expectedValues[0]:
                        info["deviceID"] = str(device_info.get("deviceID"))
                        checkStatus = "TRUE"
                        break
                status.append(checkStatus)
            elif len(arg) and arg[0] == "check_device_not_discovered":
                checkStatus = "TRUE"
                if len(arg) > 1:
                    for device_info in discoveredDevices:
                        if str(device_info.get("name")) in expectedValues[0] and str(device_info.get("deviceID")) in arg[1]:
                            checkStatus = "FALSE"
                            break
                else:
                    for device_info in discoveredDevices:
                        if str(device_info.get("name")) in expectedValues[0]:
                            checkStatus = "FALSE"
                            break
                status.append(checkStatus)
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "bluetooth_get_paired_devices":
            if arg[0] == "check_device_paired":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                status = False
                pairedDevices = result.get("pairedDevices")
                success = str(result.get("success")).lower() == "true"
                for pairedDevice in pairedDevices:
                    if str(pairedDevice.get("name")) in expectedValues[0]:
                        status = True
                        state = pairedDevice.get("connected")
                        info = pairedDevice
                if success and status:
                    info["Test_Step_Status"] = "SUCCESS"
                    if len(arg) >=2 and arg[1] == "check_connected_state":
                        if str(state).lower() == str(arg[2]).lower():
                            info["Test_Step_Status"] = "SUCCESS"
                        else:
                            info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_paired_device_list_empty":
                if len(result.get("pairedDevices")) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_bt_emu_connected":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                pairedDevices = result.get("pairedDevices")
                success = str(result.get("success")).lower() == "true"
                for pairedDevice in pairedDevices:
                    if pairedDevice.get("name") and str(pairedDevice.get("name")) in expectedValues[0]:
                        info = pairedDevice
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "bluetooth_get_connected_devices":
            if arg[0] == "check_device_connected":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                status = False
                connectedDevices = result.get("connectedDevices")
                success = str(result.get("success")).lower() == "true"
                for connectedDevice in connectedDevices:
                    if str(connectedDevice.get("name")) in expectedValues[0]:
                        status = True
                        info = connectedDevice
                        break
                if len(arg) > 1 and arg[1] == "check_active_state":
                    if int(connectedDevice.get("activeState")) in [0,1,2]:
                        status = True
                    else:
                        status = False

                if success and status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_connected_device_list_empty":
                if len(result.get("connectedDevices")) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "get_connected_bt_emu_details":
                info = checkAndGetAllResultInfo(result,result.get("success"))
                connectedDevices= result.get("connectedDevices")
                success = str(result.get("success")).lower() == "true"
                for connectedDevice in connectedDevices:
                    if connectedDevice.get("name") and str(connectedDevice.get("name")) in expectedValues[0]:
                        info = connectedDevice
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_api_version_number":
            info = result
            success = str(result.get("success")).lower() == "true"
            if success and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FirmwareCotrol Plugin Response result parser steps
        elif tag == "fwc_get_status":
            expectedStatuses = ["none", "upgradestarted", "downloadstarted", "downloadaborted", "downloadcompleted", "installinitiated", "installnotstarted", "installaborted", "installstarted", "upgradecompleted", "upgradecancelled"]
            info["status"] = result
            if result in expectedStatuses:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "fwc_get_download_size":
            info["downloadsize"] = int(result)
            if info["downloadsize"] > 200000000:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # FrameRate Plugin Response result parser steps
        elif tag == "framerate_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "framerate_check_auto_framerate_mode":
            success = str(result.get("success")).lower() == "true"
            info["frmmode"] = result.get("auto-frm-mode")
            if success and str(result.get("auto-frm-mode")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "framerate_check_negative_scenario":
            info = result
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "framerate_check_display_framerate":
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get("framerate"))
            info["framerate"] = result.get("framerate")
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and  arg[0] == "check_framerate_values":
                if success and str(result.get("framerate")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        # Warehouse Plugin Response result parser steps

        elif tag == "warehouse_get_device_info":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "warehouse_set_operation":
            info = result.copy()
            if len(arg) and arg[0] == "invalid":
                if str(result.get("success")).lower() == "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "warehouse_check_isclean":
            info = result.copy()
            isclean = str(result.get("clean")).lower()
            success = str(result.get("success")).lower() == "true"
            if success and len(result.get("files")) > 0 and isclean == "false":
                info["Test_Step_Status"] = "SUCCESS"
            elif success and ( len(result.get("files")) == 0 or result.get("files") is None ) and isclean == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "warehouse_negative_error_message_validation":
            success = result.get("success")
            info["success"] = success
            message = str(result.get("error")).strip()
            info["error"] = message
            if str(success).lower() == "false" and any(value in message for value in expectedValues):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "warehouse_validate_reset":
            info["success"] = result.get("success")
            success = str(result.get("success")).lower() == "true"
            if "error" in result and len(result.get("error")) > 0:
                info["error"] = result.get("error")
                info["Test_Step_Status"] = "FAILURE"
            else:
                if success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # LoggingPreferences Plugin Response result parser steps
        elif tag == "loggingpreferences_check_keystroke_mask_state":
            info["keystrokeMaskEnabled"] = result.get("keystrokeMaskEnabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("keystrokeMaskEnabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "loggingpreferences_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        # DataCapture Plugin Response result parser steps
        elif tag == "datacapture_enable_audio_capture":
            info =  checkAndGetAllResultInfo (result,result.get("success"))

        elif tag == "datacapture_get_audio_clip":
            info = checkAndGetAllResultInfo (result,result.get("success"))

        # Timer Plugin Response result parser steps
        elif tag == "timer_check_results":
            info = result
            status = checkNonEmptyResultData(result)
            if len(arg) and arg[0] == "check_negative_scenario":
                success = str(result.get("success")).lower() == "false"
            else:
                success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "timer_check_timer_status":
            info["state"] = result.get("state")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("state")) in expectedValues:
                 info["Test_Step_Status"] = "SUCCESS"
            else:
                 info["Test_Step_Status"] = "FAILURE"

        elif tag == "timer_check_negative_scenario":
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Messenger Plugin Response result parser steps
        elif tag == "messenger_join_room":
            info["roomid"] = result.get("roomid")
            if not str(result.get("roomid")):
                info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "Messenger_check_leave_response":
            if result== None:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag =="messenger_check_error_message":
            info = otherInfo.get("error")
            error = otherInfo.get("error")
            message = error.get("message")
            code = error.get("code")
            if message.lower() == str(expectedValues[0]).lower() and int(code) == int(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Monitor Plugin Response result parser steps
        elif tag == "monitor_get_result_data":
            if arg[1] =="yes":
                if arg[0] == "get_status":
                    measurements =  result[0].get("measurements")
                    info["observable"] = result[0].get("observable")
                    info["restart_limit"] = result[0].get("restart").get("limit")
                    info["restart_window"] = result[0].get("restart").get("window")
                elif arg[0] == "get_reset_statistics":
                    measurements =  result.get("measurements")
                    info["observable"] = result.get("observable")
                    info["restart_limit"] = result.get("restart").get("limit")
                    info["restart_window"] = result.get("restart").get("window")
                status = []
                measurement_detail = []
                for key in measurements:
                    detail_Values=[]
                    detail_Values.append(measurements.get(key))
                    status.append(checkNonEmptyResultData(detail_Values))
                    measurement_detail.append(str(key)+": "+str(measurements.get(key)))
                info["measurements"] =  measurement_detail
                if "FALSE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        # ScreenCapture Plugin Response result parser steps
        elif tag == "screencapture_upload_screen":
            if str(result.get("success")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        #AVInput Plugin Response result parser
        elif tag == "avinput_check_inputs":
            info["numberOfInputs"] = result.get("numberOfInputs")
            success = str(result.get("success")).lower() == "true"
            if success and int(result.get("numberOfInputs")) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "avinput_get_currentvideomode":
            info["currentVideoMode"] = result.get("currentVideoMode")
            currentVideoMode =  result.get("currentVideoMode")
            status = checkNonEmptyResultData(currentVideoMode)
            if status == "TRUE":
                if str(currentVideoMode).lower() == "unknown":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    VideoMode = re.split('(p|i)',currentVideoMode)
                    Resolution = VideoMode[0]
                    Framerate = VideoMode[2]
                    if Resolution == "unknown" and  len(Framerate) == 0 or Resolution in ["480", "576", "720", "1080", "3840x2160", "4096x2160"] and Framerate in ["24", "25", "30", "60", "23.98", "29.97", "50", "59.94"]:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "avinput_is_contentprotected":
            info["isContentProtected"] = result.get("isContentProtected")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("isContentProtected")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # HdmiInput Response result parser steps
        elif tag == "get_hdmiinput_devices":
            success = str(result.get("success")).lower() == "true"
            devices = result.get("devices")
            status = []
            device_details = []
            if len(arg) and arg[0] == "get_data":
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    device_data = {}
                    device_data["id"] = int(device_info.get("id"))
                    device_data["locator"] = str(device_info.get("locator"))
                    device_details.append(device_data)
                info["devices"] = device_details
            else:
                port_id_list = []
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    port_id_list.append(str(device_info.get("id")))
                info["portIds"] = port_id_list
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmiinput_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmiinput_read_edid_value":
            info["EDID"]  = str(result.get("EDID"))
            if str(result.get("success")).lower() == "true" and info["EDID"]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmiinput_check_spd_packet_information":
            packetInfo = str(result.get(arg[0])).split(',')
            status = []
            for key in packetInfo:
                key,value = str(key).split(':')
                info[key] = value
                if str(value) == "":
                    status.append("FALSE")
                elif int(value) == 0:
                    status.append("FALSE")
            if "FALSE" not in status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        # CompositeInput Response result parser steps
        elif tag == "get_compositeinput_devices":
            success = str(result.get("success")).lower() == "true"
            devices = result.get("devices")
            status = []
            device_details = []
            if len(arg) and arg[0] == "get_data":
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    device_data = {}
                    device_data["id"] = int(device_info.get("id"))
                    device_data["locator"] = str(device_info.get("locator"))
                    device_data["connected"] = str(device_info.get("connected"))
                    device_details.append(device_data)
                info["devices"] = device_details
            else:
                port_id_list = []
                for device_info in devices:
                    status.append(checkNonEmptyResultData(device_info))
                    port_id_list.append(str(device_info.get("id")))
                info["portIds"] = port_id_list
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "compositeinput_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        # PlayerInfo Plugin Response result parser steps
        elif tag == "playerinfo_check_audio_video_codecs":
            info["RESULT"] = result
            status = checkNonEmptyResultData(result)
            codec_status = [ "FALSE" for codec in expectedValues if codec  not in result ]
            if status == "TRUE" and "FALSE" not in codec_status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_validate_boolean_result":
            info["RESULT"] = result
            if str(result).lower() == "true" or str(result).lower() == "false" :
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_check_results":
            info["RESULT"] = result
            if result in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "playerinfo_check_resolution":
            info["resolution"]= result
            fps_data = ""
            resolution = result.replace("Resolution","")
            fps_data = re.split('(p|i)',str(expectedValues[0]))[2]
            if fps_data == "60":
                if str(resolution).lower() != "2160p60":
                   expectedValues = str(expectedValues[0])[0:-2]
            if str(resolution).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # PersistentStore Plugin Response result parser steps
        elif tag == "persistentstore_check_set_operation":
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_check_value":
            info["value"] = result.get("value")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("value")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_keys":
            keys = result.get("keys")
            info["Keys"] = keys
            if arg[0] == "check_not_exists":
                if expectedValues[0] not in keys:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_if_exists":
                if expectedValues[0] in keys:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_namespaces":
            Namespaces = result.get("namespaces")
            info["Namespaces"] = Namespaces
            if arg[0] == "check_not_exists":
                if expectedValues[0] not in Namespaces:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_if_exists":
                if expectedValues[0] in Namespaces:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "persistentstore_get_storage_size":
            status = checkNonEmptyResultData(result)
            if "FALSE" not in status:
                storage_size = []
                for key,value in list(result.get("namespaceSizes").items()):
                    storage_size.append(str(key)+": "+str(value))
                    info["storage_size"] =  storage_size
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["storage_size"] = result
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "persistentstore_get_namespace_storagelimit":
            output = result.get("storageLimit")
            if int(output) == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # TextToSpeech Plugin Response result parser steps
        elif tag == "texttospeech_get_enabled_status":
            info["enabletts"] = result.get("isenabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("isenabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "texttospeech_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "texttospeech_check_api_version":
            info["version"] = result.get("version")
            success = str(result.get("success")).lower() == "true"
            if success and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # XCast Plugin Response result parser steps
        elif tag == "xcast_get_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "xcast_check_version":
            success = str(result.get("success")).lower() == "true"
            info["version"] = result.get("version")
            if success and str(result.get("version")) == str(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_set_operation":
            info["success"] = result.get("success")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_friendly_name":
            info["friendlyname"] = result.get("friendlyname")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("friendlyname")).lower() in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_negative_scenario":
            info = result
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "xcast_check_standby_behavior":
            info["standbybehavior"] = result.get("standbybehavior")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("standbybehavior")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # DTV Plugin Response result parser steps
        elif tag == "dtv_validate_service_search":
            if str(result).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "dtv_check_result_list":
            if len(arg) and arg[0] == "service_list":
                info["Service_List"] = result
            elif len(arg) and arg[0] == "country_list":
                info["Country_List"] = result
            if len(result) > 0:
                status = []
                for data in result:
                    status.append(checkNonEmptyResultData(list(data.values())))
                if "FAILURE" not in status:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "dtv_check_result":
            info["result"] = result
            if len(arg) and arg[0] == "check_play_handle":
                if int(result) >= 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_services":
                if int(result) > 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "dtv_check_play_handle_status":
            info = checkAndGetAllResultInfo(result)
            if str(result.get("dvburi")).lower() == str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "dtv_check_country_configuration":
            info["result"] = result
            if str(result) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "dtv_validate_now_next_events":
            info = checkAndGetAllResultInfo(result)

        elif tag == "dtv_validate_schedule_events":
            status = checkNonEmptyResultData(result)
            info["SCHEDULED_EVENTS"] = result
            if status == "TRUE":
                nowEvent_EventID = int(expectedValues[1])
                if len(arg) and arg[0] == "validate_now_event":
                    if len(result) == 1 and int(result[0].get("eventid")) == nowEvent_EventID:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

                elif len(arg) and arg[0] == "validate_now_next_event":
                    nextEvent_EventID = int(expectedValues[0])
                    if len(result) == 2 and int(result[0].get("eventid")) == nowEvent_EventID and int(result[1].get("eventid")) == nextEvent_EventID:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # TVControlSettings Plugin Response result parser steps
        elif tag == "tvcontrolsettings_check_value":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                valueDetails = result.get(arg[1])
                if len(arg) and arg[0] == "version1":
                    info[arg[1]] = valueDetails
                    if len(arg) > 2 and arg[2] == "check_expected_value":
                        if str(valueDetails).lower() == str(expectedValues[0]).lower():
                            info["Test_Step_Status"] = "SUCCESS"
                        else:
                            info["Test_Step_Status"] = "FAILURE"
                elif len(arg) and arg[0] == "version2":
                    selectedValue = valueDetails.get("Selected")
                    info[arg[2]] = valueDetails.get("Selected")
                    info["Options"] = valueDetails.get("Options")
                    if len(arg) > 3 and arg[3] == "check_expected_value":
                        if str(selectedValue).lower() == str(expectedValues[0]).lower():
                            info["Test_Step_Status"] = "SUCCESS"
                        else:
                            info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_set_operation":
            info["success"] = result.get("success")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_dynamic_contrast":
            info["DynamicContrast"] = result.get('DynamicContrast');
            if str(result.get("success")).lower() == "true" and str(result.get('DynamicContrast')) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_supported_modes":
            info[arg[0]] = result.get(arg[0]);
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get(arg[0]))
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_modes":
            info[arg[0]] = result.get(arg[0])
            if len(arg) > 1 and arg[1] == "check_expected_mode":
                if str(result.get(arg[0])).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and result.get(arg[0]) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_auto_backlight_control":
            status = checkNonEmptyResultData(result)
            info["supportedModes"] = result.get("supportedModes")
            info["mode"] = result.get("mode")
            success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            if len(arg) and arg[0] == "check_expected_mode":
                if str(result.get("mode")).lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "tvcontrolsettings_validate_range":
            if arg[0] == "version1":
                resultValue = result.get(arg[1])
                info[arg[1]] = resultValue
            elif arg[0] == "version2":
                resultDetails = result.get(arg[1])
                info[arg[2]] = resultDetails.get('Setting')
                resultValue = resultDetails.get('Setting')
                info["Range"] = resultDetails.get('Range')
            if len(arg) > 2 and "check_range" in arg:
                if 0 <= int(resultValue) <= 100 and str(result.get("success")).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result.get("success")).lower() == "true" and str(resultValue) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "tvcontrolsettings_check_video_formats":
            info[arg[0]] = supportedFormats = result.get(arg[0])
            info[arg[1]] = result.get(arg[1])
            status = checkNonEmptyResultData(result)
            supportedFormats = [ value.lower() for value in supportedFormats ]
            if status == "TRUE" and str(result.get(arg[1])).lower() in supportedFormats:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # SecurityAgent Plugin Response result parser steps
        elif tag == "securityagent_validate_token":
            status = checkNonEmptyResultData(result)
            info["valid"] = result.get("valid")
            valid = result.get("valid")
            if str(valid).lower() == str(expectedValues[0]).lower() and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # LISA Plugin Response result parser steps
        elif tag == "lisa_check_status":
            info["Result"] = result
            status = checkNonEmptyResultData(result)
            if status == "TRUE" and result.isdigit():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "lisa_check_application_list":
            status = checkNonEmptyResultData(result)
            if not result:
                appStatus = "FALSE"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                appStatus = "FALSE"
                for app in result.get("apps"):
                    if str(app.get("id")).lower() == str(expectedValues[0]).lower():
                        appName = app.get("installed")[0]
                        if str(appName.get("appName")).lower() == str(expectedValues[0]).lower():
                            appStatus = "TRUE"
                            break;
            info["appStatus"] = appStatus
            if len(arg) > 2 and arg[1] == "check_app_exist":
                if status == "TRUE" and appStatus == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) > 2 and arg[1] == "check_app_not_exists":
                if status == "TRUE" and appStatus == "TRUE":
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "SUCCESS"
        elif tag == "lisa_check_error_message":
            info = result
            if len(arg) and arg[0] == "check_error_message":
                status = checkNonEmptyResultData(result)
                if status == "TRUE" and str(expectedValues[0]) in str(result.get("message")).lower() and str(result.get("success")).lower() == str(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info = checkAndGetAllResultInfo(otherInfo)
                error = otherInfo.get("error")
                if str(expectedValues[0]) in str(otherInfo.get("message")).lower() and error.get("code") == int(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "lisa_check_multiple_request_error_message":
            info = result
            sleep(1)
            info = checkAndGetAllResultInfo(otherInfo)
            error = otherInfo.get("error")
            if str(expectedValues[0]) in str(otherInfo.get("message")).lower() and error.get("code") == int(expectedValues[1]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "lisa_check_storage_info":
            info = result
            apps = result.get("apps")
            persistent = result.get("persistent")
            status1 = checkNonEmptyResultData(list(apps.values()))
            status2 = checkNonEmptyResultData(list(persistent.values()))
            if status1 == "TRUE" and status2 == "TRUE":
                if str(expectedValues[0]).lower() in str(apps.get("path")).lower() and str(expectedValues[0]).lower() in str(persistent.get("path")).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"
        # OCIContainer Plugin Response result parser steps
        elif tag == "ocicontainer_list_container":
            info = result
            containers = result.get("containers")
            success = str(result.get("success")).lower() == "true"
            expectedResult = 0
            for app in containers:
                if str(app.get("Id")).lower() == expectedValues[0]:
                    descriptor = app.get("Descriptor")
                    expectedResult = 1
                    break;
            if success:
                if len(arg) and arg[0] == "check_if_exists":
                    if expectedResult == 1:
                        info["Test_Step_Status"] = "SUCCESS"
                        if len(arg) > 2 and arg[1] == "check_container_info":
                            if descriptor == arg[2]:
                                info["Test_Step_Status"] = "SUCCESS"
                            else:
                                info["Test_Step_Status"] = "FAILURE"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

                elif len(arg) and arg[0] == "check_not_exists":
                    if expectedResult == 0:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "ocicontainer_check_container_status":
            info = result
            success = str(result.get("success")).lower() == "true"
            if success and result.get("state").lower() == expectedValues[0] and result.get("containerId").lower() == expectedValues[1]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "ocicontainer_check_for_results":
            info = result
            status = checkNonEmptyResultData(result)
            if len(arg) and arg[0] == "check_negative_scenario":
                success = str(result.get("success")).lower() == "false"
            else:
                success = str(result.get("success")).lower() == "true"
            if success and status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "ocicontainer_check_container_info":
            info = result
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            containerInfo = result.get("info")
            if success and status == "TRUE" and containerInfo.get("id").lower() == expectedValues[1] and containerInfo.get("state").lower() == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"


        elif tag == "ocicontainer_check_process_id":
            status = checkNonEmptyResultData(result)
            success = str(result.get("success")).lower() == "true"
            result = result.get("info")
            pids = result.get("pids")
            info["pids"] = pids
            if success and status == "TRUE" and int(expectedValues[0]) in pids:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # Parser Code for HdmiCec2 plugin
        elif tag == "hdmicec2_get_enabled_status":
            info["enabled"] = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            if success and str(result.get("enabled")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec2_validate_boolean_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("status")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec2_check_result":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "hdmicec2_get_osd_name":
            success = str(result.get("success")).lower() == "true"
            info["name"] = result.get("name")
            if len(arg) and arg[0] == "osd_name":
                if success and str(result.get("name")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                status = checkNonEmptyResultData(result.get("name"))
                if status == "TRUE":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "hdmicec2_get_vendor_id":
            success = str(result.get("success")).lower() == "true"
            vendorID = result.get("vendorid")
            info["vendorID"] = vendorID
            if len(arg) and arg[0] == "vendor_id":
                if success and str(vendorID) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                status = checkNonEmptyResultData(vendorID)
                if status == "TRUE" and str(vendorID).lower() != "000":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # Controller Plugin Response result parser steps
        elif tag == "controller_get_plugin_state":
            if arg[0] == "check_status":
                state = ""
                callsign = ""
                for plugin in result:
                    if plugin.get("callsign") == arg[1]:
                        state = plugin.get("state")
                        callsign = plugin.get("callsign")
                        break
                info["state"] = state
                info["callsign"] = callsign

                if info["state"] in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        
        #Fetch the complete configuration and save it
        elif tag == "controller_get_configuration":
            status = checkNonEmptyResultData(result)
            info["configuration"] = result
            info["url"] = expectedValues[0]
            if status:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_discovery_result":
            info = checkAndGetAllResultInfo (result[0])

        elif tag == "controller_check_environment_variable_value":
            status = checkNonEmptyResultData(result)
            info["RESULT"] = result
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_get_configuration_url":
            info["url"] = result.get("url")
            status = compareURLs(str(result.get("url")),expectedValues[0])
            if status == "TRUE":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_processinfo":
            info = checkAndGetAllResultInfo (result)

        elif tag == "controller_check_active_connection":
            info = result[0]
            status = checkNonEmptyResultData(result[0])
            if status == "TRUE" and str(result[0].get("state")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_subsystems_status":
            info = result[0]
            status = checkNonEmptyResultData(result[0])
            if status == "TRUE" and str(result[0].get("subsystem")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag =="controller_check_error_message":
            info = otherInfo.get("error")
            error = otherInfo.get("error")
            message = error.get("message")
            if len(arg) and arg[0] == "check_message":
                if message.lower() == str(expectedValues[0]).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "deactivate_check_error_message":
                if message.lower() in str(expectedValues).lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                code = error.get("code")
                if message.lower() == str(expectedValues[0]).lower() and int(code) == int(expectedValues[1]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "controller_check_default_plugin_state":
            if arg[0] == "check_default_state":
                state = ""
                callsign = ""
                for plugin in result:
                    if plugin.get("callsign") == arg[1]:
                        state = plugin.get("state")
                        callsign = plugin.get("callsign")
                        autostart = plugin.get("autostart")
                        break
                info["state"] = state
                info["callsign"] = callsign
                info["autostart"] = autostart
                if autostart == True:
                    expectedState = "activated,activation"
                    if state in expectedState:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
        #Validate_http Response result parser steps
        elif tag == "validate_http_exit_code":
            if arg[0] == "check_status":
                for plugin in result:
                    status_code = plugin.get("HttpStatusCode")
                    if status_code is not None:
                        info["HttpStatusCode"] = status_code
                        break
                if status_code == 200:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        # UsbAccess Plugin Response result parser steps
        elif tag == "check_mount_device_path":
            mounted = result.get('mounted')
            success = result.get('success')
            info["mounted"] = mounted
            info["success"] = success
            #Check result value empty or not
            if mounted and success:
                #Check success value not equal false
                if str(success).lower() != "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if expectedValues and str(success).lower() != "false":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_mount_device_path_after_reboot":
            mounted = result.get('mounted')
            success = result.get('success')
            info["mounted"] = mounted
            info["success"] = success
            if mounted and success:
                if str(success).lower() != "false" and expectedValues[0] in mounted:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_get_link":
            links = result.get('links')
            success = result.get('success')
            if links:
                path = links[0].get('path')
                baseURL = links[0].get('baseURL')
                info["path"] = path
                info["baseURL"] = baseURL
                info["success"] = success
                if expectedValues:
                    if expectedValues[0] in baseURL and str(success).lower() == "true":
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif str(success).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["links"] = links
                info["success"] = success
                if expectedValues and str(success).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                elif str(success).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_create_link":
            baseURL = result.get('baseURL')
            success = result.get('success')
            error = result.get("error")
            #Check result value empty or not
            if baseURL and success:
                info["baseURL"] = baseURL
                info["success"] = success
                if str(success).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["success"] = success
                if error:
                    info["error"] = error
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["baseURL"] = baseURL
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_clear_link":
            success = result.get('success')
            error = result.get("error")
            if str(success).lower() == "true":
                info["success"] = success
                info["Test_Step_Status"] = "SUCCESS"
            else:
                if error:
                    info["error"] = error
                    info["success"] = success
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["success"] = success
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_negative_scenario":
            success = result.get('success')
            error = str(result.get("error")).strip()
            info["error"] = error
            info["success"] = success
            if str(success).lower() == "false" and expectedValues[0] in error:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_get_file_list":
            success = result.get('success')
            contents = result.get('contents')
            info["contents"] = contents
            info["success"] = success
            if str(success).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_archive_logs":
            success = result.get('success')
            info["success"] = success
            if str(success).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_get_power_state":
            powerState = result.get("powerState")
            success = result.get('success')
            info["powerState"] = powerState
            info["success"] = success
            if powerState and success:
                if expectedValues:
                    if str(success).lower() == "true" and powerState in expectedValues:
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                elif str(success).lower() == "true":
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag =="usbaccess_check_available_Firmware_file":
            availableFirmwareFiles = result.get("availableFirmwareFiles")
            success = result.get('success')
            info["availableFirmwareFiles"] = availableFirmwareFiles
            info["success"] = success
            if availableFirmwareFiles and success:
                for files in availableFirmwareFiles:
                    if str(success).lower() == "true" and expectedValues[0] in files:
                        info["Test_Step_Status"] = "SUCCESS"
                        break
                    else:
                        info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_check_available_Firmware_file_negative_scenario":
            availableFirmwareFiles = result.get("availableFirmwareFiles")
            success = result.get('success')
            info["availableFirmwareFiles"] = availableFirmwareFiles
            info["success"] = success
            for files in availableFirmwareFiles:
                if str(success).lower() == "true" and arg[0] not in files:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
                    break

        # Combinational Plugin Response result parser steps
        elif tag == "validate_audio_ports":
            supportedAudioPorts = result.get("supportedAudioPorts")
            success = result.get('success')
            info["supportedAudioPorts"] = supportedAudioPorts
            info["success"] = success
            #Removing unwanted quotes
            expectedValues = [elem.strip("[]' ") for item in expectedValues for elem in item.split(', ')]
            if set(supportedAudioPorts) == set(expectedValues):
                message = "DisplaySettings and DeviceInfo API's are returning same audio ports"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "DisplaySettings and DeviceInfo API's are not returning same audio ports"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_video_ports":
            supportedVideoDisplays = result.get("supportedVideoDisplays")
            success = result.get('success')
            info["supportedVideoDisplays"] = supportedVideoDisplays
            info["success"] = success
            #Removing unwanted quotes
            expectedValues = [elem.strip("[]' ") for item in expectedValues for elem in item.split(', ')]
            if set(supportedVideoDisplays) == set(expectedValues):
                message = "DisplaySettings and DeviceInfo API's are returning same video ports"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "DisplaySettings and DeviceInfo API's are not returning same video ports"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_audio_ports":
            supportedAudioPorts = result.get("supportedAudioPorts")
            info["supportedAudioPorts"] = supportedAudioPorts
            if supportedAudioPorts:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "deviceinfo_check_video_ports":
            supportedVideoDisplays = result.get("supportedVideoDisplays")
            info["supportedVideoDisplays"] = supportedVideoDisplays
            if supportedVideoDisplays:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_hdcp_version":
            output = result.get("supportedHDCPVersion")
            success = result.get('success')
            info["supportedHDCPVersion"] = output
            info["success"] = success
            if  str(success).lower() == "true" and float(output) == float(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # NetworkManager Plugin Response result parser steps
        elif tag == "networkmanager_get_interface_info":
            status,macAddressStatus = [],[]
            interfaces_info = result.get("interfaces")
            success = str(result.get("success")).lower() == "true"
            info["success"] = success
            for interface in interfaces_info:
                status.append(checkNonEmptyResultData(list(interface.values())))
                macAddress = interface.get("mac")
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is None:
                macAddressStatus.append("False")
            if success and "FALSE" not in status and len(interfaces_info) != 0 and "FALSE" not in macAddressStatus:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
            
            if arg[0] == "get_all_info":
                info["interfaces"] = interfaces_info

            elif arg[0] == "get_interface_names":
                interface_names = []
                for interface in interfaces_info:
                    interface_names.append(interface.get("name"))
                interface_names = [ str(name) for name in interface_names if str(name).strip() ]
                info["interface_names"] = interface_names

        elif tag == "networkmanager_get_primary_interface":
            default_interface = result.get("interface")
            success = str(result.get("success")).lower() == "true"
            info["default_interface"] = default_interface
            info["success"] = success
            if len(arg) and arg[0] == "check_interface":
                if success and default_interface in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_publicip":
            ipaddress = result.get("ipaddress")
            success = str(result.get("success")).lower() == "true"
            info["ipaddress"] = ipaddress
            info["success"] = success
            if arg[0] == "check_ipv4":
                # Validate IPv4 IP address using regex
                pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                status = bool(re.match(pattern, ipaddress))
                if success and status and str(ipaddress) == str(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif arg[0] == "check_ipv6": 
                # Validate IPv6 IP address using regex
                pattern = r"^([0-9a-fA-F]{1,4}:){7}([0-9a-fA-F]{1,4}|:)$"
                status = bool(re.match(pattern, ipaddress))
                if status and success:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_ping_response":
            if len(arg) and arg[0] == "validate_error_message":
                if str(result.get("success")).lower() == "false" and str(result.get('error')).lower() == str(expectedValues[0]).lower() and result.get("endpoint") == expectedValues[1]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "validate_ipversion_error_message":
                if otherInfo:
                    error = otherInfo.get("error")
                    if str(error.get("message")).lower() == str(expectedValues[0]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:        
                endpoint = result.get("endpoint")
                tx_packets = int(result.get("packetsTransmitted"))
                rx_packets = int(result.get("packetsReceived"))
                packets_loss = result.get("packetLoss")
                success = str(result.get("success")).lower() == "true"
                info["endpoint"] = endpoint
                info["packetsTransmitted"] = tx_packets
                info["packetsReceived"] = rx_packets
                info["packetsloss"] = packets_loss
                info["success"] = success
                if success and endpoint == expectedValues[1] and tx_packets == int(expectedValues[0]) and rx_packets == int(expectedValues[0]) and int(packets_loss) == 0:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_trace_response":
            endpoint = result.get("endpoint")
            traceroute = result.get("results")
            success = str(result.get("success")).lower() == "true"
            info["endpoint"] = endpoint
            info["traceroute"] = traceroute
            info["success"] = success
            if success and endpoint == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_check_networkconnectivity":
            connected = str(result.get("connected")).lower()
            success = str(result.get("success")).lower() == "true"
            info["connected"] = connected
            info["success"] = success
            if success and connected == expectedValues[0]:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_check_interface_status":
            status,macAddressStatus = [],[]
            isenabled_status = None
            interfaces_info = result.get("interfaces")
            success = str(result.get("success")).lower() == "true"
            info["success"] = success
            info["interfaces"] = interfaces_info
            # Loop through the interfaces to find and get configured isEnabled status
            for interface in interfaces_info:
                status.append(checkNonEmptyResultData(list(interface.values())))
                macAddress = interface.get("mac")
                if interface["name"] == arg[0]:
                    isenabled_status = interface["enabled"]
            if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is None:
                macAddressStatus.append("False")
            if success and "FALSE" not in status and len(interfaces_info) != 0 and "FALSE" not in macAddressStatus and str(isenabled_status).lower() in str(expectedValues[0]).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_connected_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if len(arg) and arg[0] == "check_ssid":
                if str(result.get("success")).lower() == "true" and str(result.get("ssid")) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_known_ssid":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("success")).lower() == "true" and str(expectedValues[0]) in result.get("ssids"):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_check_supported_security_modes":
            info["security"] = result.get("security")
            success = str(result.get("success")).lower() == "true"
            status = checkNonEmptyResultData(result.get("security"))
            if "FALSE" not in status and success:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_stun_endpoint":
            endpoint = result.get("endpoint")
            port = result.get("port")
            success = str(result.get("success")).lower() == "true"
            info["endpoint"] = endpoint
            info["port"] = port
            info["success"] = success
            if len(arg) and arg[0] == "check_endpoint":
                if success and endpoint in expectedValues and str(port) in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and endpoint and port:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
       
        elif tag == "networkmanager_check_log_level":
            success = str(result.get("success")).lower() == "true"
            info["level"] = result.get("level")
            if success and str(result.get("level")) in expectedValues:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_check_wifi_state":
            info = checkAndGetAllResultInfo(result)
            state = result.get("state")
            status = str(result.get("status")).lower()
            success = str(result.get("success")).lower() == "true"
            if len(arg) and arg[0] == "check_wifi_state":
                  expectedValues = [ value.lower() for value in expectedValues ]
                  if success:
                       for index, value in enumerate(expectedValues):
                            if index == state and value == status:
                                info["Test_Step_Status"] = "SUCCESS"
                                break
                            else:
                                info["Test_Step_Status"] = "FAILURE"
                  else:
                      info["Test_Step_Status"] = "FAILURE"
        
            elif len(arg) and arg[0] == "check_wifi_expected_state":
                if success:
                    if state == int(expectedValues[0]) and status == str(expectedValues[1]).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                else: 
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_get_connectivity_test_endpoint":
            endpoints = result.get("endpoints")
            success = str(result.get("success")).lower() == "true"
            info["endpoints"] = ",".join(endpoints)
            info["success"] = success
            if len(arg) and arg[0] == "check_endpoints":
                endpointStatus = endpoints == expectedValues
                if success and endpointStatus:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if success and endpoints:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "networkmanager_check_ssid_list":
            info["success"] = result.get("success")
            info["ssids"] = result.get("ssids")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
                if arg[0] in result.get("ssids"):
                    info["configured_ssid_presence"] = "yes"
                else:
                    info["configured_ssid_presence"] = "no"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "networkmanager_check_empty_ssid_list":
            info["success"] = result.get("success")
            info["ssids"] = result.get("ssids")
            if str(result.get("success")).lower() == "true":
                if arg[0] in result.get("ssids"):
                    info["Test_Step_Status"] = "FAILURE"
                else:
                    info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        # Common Response result parser steps
        elif tag == "check_result_values":
            info = checkAndGetAllResultInfo(result,result.get("success"))

        elif tag == "success_status_validation":
            info["success"] = result.get("success")
            if str(result.get("success")).lower() == "true":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "get_enabled_status_validation":
            enabled = result.get("enabled")
            success = str(result.get("success")).lower() == "true"
            info["enabled"] = enabled
            info["success"] = success
            if success and (str(enabled).lower()) in (str(expectedValues).lower()):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "success_negative_status_validation":
            info = result
            if str(result.get("success")).lower() == "false":
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "error_negative_scenario_validation":
            try:
                info["otherInfo"] = otherInfo
                message = otherInfo.get("error").get("message")
                if str(message).lower() in [str(val).lower() for val in expectedValues]:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            except Exception as e:
                info["error"] = str(e)
                info["Test_Step_Status"] = "FAILURE"

        # RemoteControl Response result parser steps
        elif tag == "check_api_version":
            info = checkAndGetAllResultInfo(result,result.get("success"))
            if str(result.get("success")).lower() == "true" and result.get("version") == int(expectedValues[0]):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"
        
        # DWTV Response result parser steps
        elif tag == "empty_result_validation":
            if result:
                info["Test_Step_Status"] = "FAILURE"
            else:
                info["Test_Step_Status"] = "SUCCESS"

        # Maintenance Manager Response result parser steps
        elif tag == "check_maintenance_activity_status":
            info = result
            if str(result.get("success")).lower() == "true" and result.get("maintenanceStatus").lower() == expectedValues[0].lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "get_maintenance_optout_mode":
            info = result
            if str(result.get("success")).lower() == "true" and result.get("maintenanceMode").strip().lower() == expectedValues[0].lower() and result.get("optOut").strip().lower() == expectedValues[1].lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        # UserSettings Response result parser steps
        elif tag == "usersettings_get_status":
            info[arg[0]] = result
            if len(arg) > 1 and arg[1] == "negative":
                if str(result).strip().lower() in expectedValues[0].lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_api_info":
            info[arg[0]] = result
            if result:
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_enabled_status":
            info["enabled"] = result
            if arg and arg[0] == "negative":
                if str(result).strip().lower() in expectedValues[0].lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_pinControl_status":
            info["pinControl"] = result
            if arg and arg[0] == "negative":
                if str(result).strip().lower() in expectedValues[0].lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_liveWatershed_status":
            info["liveWatershed"] = result
            if arg and arg[0] == "negative":
                if str(result).strip().lower() in expectedValues[0].lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_playbackWatershed_status":
            info["playbackWatershed"] = result
            if arg and arg[0] == "negative":
                if str(result).strip().lower() in expectedValues[0].lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "usersettings_get_contentpin_status":
            info["contentPin"] = result
            if expectedValues:
                if str(result).strip() in expectedValues:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            else:
                if result:
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

        else:
            print("\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag))
            info["Test_Step_Status"] = "FAILURE"

    except Exception as e:
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))
        info["Test_Step_Status"] = "FAILURE"

    return info



#-----------------------------------------------------------------------------------------------
# CheckAndGenerateConditionalExecStatus
#-----------------------------------------------------------------------------------------------
# Syntax      : CheckAndGenerateConditionalExecStatus(testStepResults,methodTag,arguments)
# Description : Method to parse the previous test step result to check whether required
#               condition is satisfied to execute the current test step
# Parameter   : testStepResults - list of previous test step results
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Condition status (TRUE/FALSE)
#-----------------------------------------------------------------------------------------------
def CheckAndGenerateConditionalExecStatus(testStepResults,methodTag,arguments):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. testStepResults - list of dictionaries
    #    Eg [ {1: [{"brightness":100}]} ] // 1-testCaseId
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, if any exception occurs
    #   while parsing then status will be FAILURE
    # b.result - (TRUE/FALSE)
    #   1.It is the actual variable which indicates
    #   whether required condition is met or not

    # User can also use testStepId to refer the result
    # data present in testStepResults

    # DO NOT OVERRIDE THE RETURN VARIABLES "RESULT" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "RESULT" WITH (TRUE/FALSE)
    result = ""
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:

        # Controller Plugin Response result parser steps
        if tag == "controller_get_plugin_state":
            state = ""
            testStepResults = list(testStepResults[0].values())[0]
            for result in testStepResults:
                if result.get("callsign") == arg[1]:
                    state = result.get("state")
                    break;
            if arg[0] == "isDeactivated":
                if state == "deactivated":
                    result = "TRUE"
                elif state == "activated":
                    result = "FALSE"
                elif state == "resumed":
                    result = "FALSE"
                else:
                    result = "TRUE"
            elif arg[0] == "isActivated":
                if state == "activated":
                    result = "TRUE"
                elif state == "resumed":
                    result = "TRUE"
                elif state == "deactivated":
                    result = "FALSE"
                else:
                    result = "FALSE"
            elif arg[0] == "isUnavailable":
                if state == "activated":
                    result = "FALSE"
                elif state == "resumed":
                    result = "FALSE"
                elif state == "deactivated":
                    result = "FALSE"
                elif state == "unavailable":
                    result = "TRUE"
                else:
                    result = "TRUE"

        elif tag =="controller_check_plugin_state_applicability":
            testStepResults = list(testStepResults[0].values())[0]
            status_value = testStepResults[0].get("plugin_status_value")
            if status_value == "yes":
                result = "TRUE"
            else:
                result = "FALSE"

        # TraceControl Plugin Response result parser steps
        elif tag == "tracecontrol_get_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isDisabled":
                if state == "disabled":
                    result = "TRUE"
                else:
                    result = "FALSE"
            if arg[0] == "isEnabled":
                if state == "enabled":
                    result = "TRUE"
                else:
                    result = "FALSE"


        # Front Panel Plugin Response result parser steps
        elif tag == "frontpanel_check_led_brightness":
            testStepResults = list(testStepResults[0].values())[0]
            brightness = testStepResults[0].get("brightness")
            if arg[0] == "isBrigtnessZero":
                if str(brightness) == "0":
                    result = "TRUE"
                else:
                    result = "FALSE"


        # WebKitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_check_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isSuspended":
                if state == "suspended":
                    result = "TRUE"
                else:
                    result = "FALSE"

        #network plugin
        elif tag =="check_test_status":
            testStepResults = list(testStepResults[0].values())[0]
            configValue = testStepResults[0].get("configvalue")
            if configValue == "yes":
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "get_previous_wifi_enabled_status":
            testStepResults1 = list(testStepResults[0].values())[0]
            result1 = testStepResults1[0].get("enabled")
            result2 = testStepResults1[1].get("enabled")
            if len(arg) and arg[0] == "check_empty_wifi_event":
                if result1 == result2:
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if result1 == result2:
                    result = "FALSE"
                else:
                    result = "TRUE"
                    
        elif tag == "network_check_wifi_interface_status":
            testStepResults = list(testStepResults[0].values())[0]
            wifi_enabled_status = testStepResults[0].get("enabled")
            if str(wifi_enabled_status).strip().lower() == "true":
                result = "FALSE"
            else:
                result = "TRUE"

        # Cobalt Plugin Response result parser steps
        elif tag == "cobalt_check_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = testStepResults[0].get("state")
            if arg[0] == "isSuspended":
                if state == "suspended":
                    result = "TRUE"
                else:
                    result = "FALSE"

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_check_adapter_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = str(testStepResults[0].get("state"))
            if arg[0] == "isDisabled":
                if state == "1":
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "wifi_check_interface_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = str(testStepResults[0].get("enabled"))
            if str(state).lower() == "false":
                result = "TRUE"
            else:
                result = "FALSE"

        # RDKShell Plugin Response result parser steps
        elif tag == "rdkshell_check_application_state":
            testStepResults = list(testStepResults[0].values())[0]
            clients = testStepResults[0].get("clients")
            if len(arg) and arg[0] == "check_app_not_exists":
                if str(arg[1]).lower() in clients:
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if arg[0] not in clients:
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "rdkshell_get_previous_app_state":
            testStepResults1 = list(testStepResults[0].values())[0]
            clients = testStepResults1[0].get("clients")
            if str(arg[0]).lower() in clients:
                testStepResults2 = list(testStepResults[1].values())[0]
                apps = testStepResults2[0].get("state")
                #Iterate through the list to find the youtube app state
                for app in apps:
                    if app["callsign"] == "Cobalt":
                        appstate = app["state"]
                if str(appstate).lower() == "hibernated":
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                result = "FALSE"

        # XCast Plugin Response result parser steps
        elif tag == "xcast_get_xdial_status":
            if len(arg) and arg[0] == "dynamic_app_list":
                testStepResults1 = list(testStepResults[0].values())[0]
                testStepResults2 = list(testStepResults[1].values())[0]
                status1 = testStepResults1[0].get("status")
                status2 = testStepResults2[0].get("status")
                if str(status1).lower() == "true" and str(status2).lower() == "true":
                    result = "FALSE"
                else:
                    result = "TRUE"
            else:
                testStepResults = list(testStepResults[0].values())[0]
                status = testStepResults[0].get("status")
                if str(status).lower() == "true":
                    result = "FALSE"
                else:
                    result = "TRUE"

        elif tag == "xcast_get_enable_status":
            testStepResults = list(testStepResults[0].values())[0]
            xcast_enabled = testStepResults[0].get("enabled")
            if "false" in str(xcast_enabled).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        # HdmiCecSink Plugin Response result parser steps
        elif tag == "hdmicecsink_check_cec_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            if str(testStepResults[0].get("enabled")).lower() != "true":
                result = "TRUE"
            else:
                result = "FALSE"

        # System Plugin Response result parser steps
        elif tag == "system_check_preferred_standby_mode":
            testStepResults = list(testStepResults[0].values())[0]
            mode = testStepResults[0].get("preferredStandbyMode")
            if arg[0] == "isNotEqual":
                if mode != arg[1]:
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "system_check_disk_partition":
            testStepResults = list(testStepResults[0].values())[0]
            partition_count = testStepResults[0].get("partition_count")
            if int(partition_count) < int(arg[0]):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "system_check_power_state_status":
            testStepResults = list(testStepResults[0].values())[0]
            powerState = testStepResults[0].get("powerState")
            if powerState in ("STANDBY","DEEP_SLEEP","LIGHT_SLEEP"):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "system_check_existing_rule":
            testStepResults = list(testStepResults[0].values())[0]
            message = testStepResults[0].get(arg[0])
            if arg[0] == "existing_model_id":
                if "not found" in message:
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if not message:
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "lisa_check_app_status":
            testStepResults = list(testStepResults[0].values())[0]
            appStatus = testStepResults[0].get("appStatus")
            if len(arg) and arg[0] == "check_app_exists":
                if appStatus == "TRUE":
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if appStatus == "TRUE":
                    result = "FALSE"
                else:
                    result = "TRUE"

        # OCI Container Plugin Response result parser steps
        elif tag == "get_data_model_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("status")
            if str(status).lower() == "true":
                result = "FALSE"
            else:
                result = "TRUE"

        # Bluetooth Plugin Response result parser steps
        elif tag == "bluetooth_check_device_pair_status":
            testStepResults = list(testStepResults[0].values())[0]
            if testStepResults[0].get("name"):
                result = "TRUE"
            else:
                result = "FALSE"

        # UsbAccess Plugin Response result parser steps
        elif tag == "usbaccess_clear_link":
            testStepResults = list(testStepResults[0].values())[0]
            baseURL = testStepResults[0].get("baseURL")
            if baseURL:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "usbaccess_set_power_state":
            testStepResults = list(testStepResults[0].values())[0]
            powerState = testStepResults[0].get("powerState")
            if powerState in "ON":
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "usbaccess_check_parameter":
            testStepResults = list(testStepResults[0].values())[0]
            tr181parametervalue = testStepResults[0].get("tr181parametervalue")
            if "true" not in tr181parametervalue:
                result = "TRUE"
            else:
                result = "FALSE"

        # DisplaySettings Plugin Response result parser steps
        elif tag == "displaysettings_mute_status":
            testStepResults = list(testStepResults[0].values())[0]
            muted_status = testStepResults[0].get("muted")
            if len(arg) and arg[0] == "muted_status":
                if "true" in muted_status.lower():
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if "false" in muted_status.lower():
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "displaysettings_volume_level":
            testStepResults = list(testStepResults[0].values())[0]
            volume_Level = testStepResults[0].get("volumeLevel")
            volume_Level_float = float(volume_Level)
            volume_Level_int = int(volume_Level_float)
            if len(arg) and arg[0] == "volume_status":
                if volume_Level_int == 0:
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if volume_Level_int == 100:
                    result = "TRUE"
                else:
                    result = "FALSE"

        elif tag == "displaysettings_volume_level_for_hundred":
            testStepResults = list(testStepResults[0].values())[0]
            volume_Level = testStepResults[0].get("volumeLevel")
            volume_Level_float = float(volume_Level)
            volume_Level_int = int(volume_Level_float)
            if volume_Level_int != 100:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "displaysettings_keycode_decrease_volume_level":
            testStepResults = list(testStepResults[0].values())[0]
            volume_Level = testStepResults[0].get("volumeLevel")
            volume_Level_float = float(volume_Level)
            volume_Level_int = int(volume_Level_float)
            if volume_Level_int > 90:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "displaysettings_keycode_increase_volume_level":
            testStepResults = list(testStepResults[0].values())[0]
            volume_Level = testStepResults[0].get("volumeLevel")
            volume_Level_float = float(volume_Level)
            volume_Level_int = int(volume_Level_float)
            if volume_Level_int < 10:
                result = "TRUE"
            else:
                result = "FALSE"
                
        elif tag == "get_previous_resolution":
            testStepResults1 = list(testStepResults[0].values())[0]
            resolution1 = testStepResults1[0].get("resolution")
            resolution2 = testStepResults1[1].get("resolution")
            if len(arg) and arg[0] == "check_resolution":
                if resolution1 == resolution2:
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if resolution1 == resolution2:
                    result = "FALSE"
                else:
                    result = "TRUE"

        # PersistentStore Plugin Response result parser steps
        elif tag == "persistentstore_get_previous_namespace":
            testStepResults = list(testStepResults[0].values())[0]
            namespaces = testStepResults[0].get("Namespaces")
            if namespaces is None:
                result = "FALSE"
            else:
                if "username" in namespaces:
                    result = "TRUE"
                else:
                    result = "FALSE"

        # HdmiCecSource Plugin Response result parser steps
        elif tag == "hdmicecsource_check_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if len(arg) and arg[0] == "empty_check":
                if str(enabled).lower() == "true":
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if str(enabled).lower() == "true":
                    result = "FALSE"
                else:
                    result = "TRUE"

        elif tag == "hdmicecsource_check_active_source_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("status")
            if len(arg) and arg[0] =="standby":
                if "true" in str(status).lower():
                    result = "TRUE"
                else:
                    result = "FALSE"
            else:
                if "false" in str(status).lower():
                    result = "TRUE"
                else:
                    result = "FALSE"

        # NetworkMnager Plugin Response result parser steps
        elif tag == "networkmanager_get_wifi_state":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "false":
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "networkmanage_check_primary_interface":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("default_interface")
            if str(default_interface).lower() != "eth0":
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "networkmanager_get_ssid_presence_value":
            testStepResults = list(testStepResults[0].values())[0]
            configured_ssid_presence = testStepResults[0].get("configured_ssid_presence")
            if str(configured_ssid_presence).lower() == "yes":
                result = "TRUE"
            else:
                result = "FALSE"

        # MaintenanceMnager Plugin Response result parser steps
        elif tag == "maintenancemanager_get_maintenance_status":
            testStepResults = list(testStepResults[0].values())[0]
            maintenance_status = testStepResults[0].get("maintenanceStatus")
            if arg[0].lower() == maintenance_status.lower():
                result = "TRUE"
            else:
                result = "FALSE"

        # Miracast Plugin Response result parser steps
        elif tag == "miracast_getpreviousenable":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "false":
                result = "TRUE"
            else:
                result = "FALSE"

        else:
            print("\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag))
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))
        print("Result: %s" %(result))

    return status,result



#-----------------------------------------------------------------------------------------------
# parsePreviousTestStepResult
#-----------------------------------------------------------------------------------------------
# Syntax      : parsePreviousTestStepResult(testStepResults,methodTag,arguments)
# Description : Method to parse the previous test step results to get the certain
#               required key-value pair(s) based on user's need
# Parameter   : testStepResults - list of previous test step results
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def parsePreviousTestStepResult(testStepResults,methodTag,arguments):
    tag  = methodTag
    arg  = arguments

    # Input Variables:
    # a. testStepResults - list of dictionaries
    #    Eg [ {1: [{"brightness":100}]} ] // 1-testCaseId
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.Info - dictionary
    #   1.It should be updated with the required
    #   key-value pair(s) based on user's need

    # User can also use testStepId to refer the result
    # data present in testStepResults

    # DO NOT OVERRIDE THE RETURN VARIABLES "INFO" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "INFO" WITH REQUIRED
    # RESULT DETAILS

    info = {}
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:
        # TraceControl Plugin Response result parser steps
        if tag == "tracecontrol_toggle_state":
            state = ""
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) != 0:
                for result in testStepResults:
                    if arg[0] == result.get("category"):
                        state = result.get("state")
                        break;
            else:
                state = testStepResults[0].get("state")

            if state == "enabled":
                info["state"] = "disabled"
            elif state == "disabled":
                info["state"] = "enabled"

        elif tag == "tracecontrol_get_category":
            testStepResults = list(testStepResults[0].values())[0]
            info["category"] = testStepResults[0].get("category")
 
        # MessageControl Plugin Response result parser steps
        elif tag == "messagecontrol_toggle_state":
            state = ""
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) != 0:
                for result in testStepResults:
                    if arg[0] == result.get("category"):
                        state = result.get("enabled")
                        break;
            else:
                state = testStepResults[0].get("enabled")
            if str(state).lower() == "true":
                info["enabled"] = False
            elif str(state ).lower() == "false":
                info["enabled"] = True
 
        # MessageControl Plugin Response result parser steps
        elif tag == "messagecontrol_get_original_state":
            state = ""
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) != 0:
                for result in testStepResults:
                    if arg[0] == result.get("category"):
                        state = result.get("enabled")
                        break;
            else:
                state = testStepResults[0].get("enabled")
            info["enabled"] = state

        # DeviceInfo Plugin Response result parser steps
        elif tag == "deviceinfo_get_firmware_version_details":
            testStepResults = list(testStepResults[0].values())[0]
            info["imagename"] = testStepResults[0].get("image")
            info["yocto"] = testStepResults[0].get("yocto")

        elif tag =="get_previous_dates":
            api_date_list = [] 
            dut_date_list = []
            testStepResults1 = list(testStepResults[0].values())[0]
            api_date_list.append(testStepResults1[0].get("systeminfo_day"))
            api_date_list.append(testStepResults1[0].get("systeminfo_month"))
            api_date_list.append(testStepResults1[0].get("systeminfo_year"))
            info["api_date_list"] = api_date_list
            
            testStepResults2 = list(testStepResults[1].values())[0]
            dut_date_list.append(testStepResults2[0].get("dut_day"))
            dut_date_list.append(testStepResults2[0].get("dut_month"))
            dut_date_list.append(testStepResults2[0].get("dut_year"))
            info["dut_date_list"] = dut_date_list

        # OCDM Plugin Response result parser steps
        elif tag == "ocdm_get_all_drms":
            testStepResults = list(testStepResults[0].values())[0]
            drm_info = testStepResults[0].get("drm_info")
            drms = []
            for drm in drm_info:
                drms.append(drm.get("name"))
            info["drm"] = ",".join(drms)

        elif tag == "ocdm_get_drm_key":
            testStepResults = list(testStepResults[0].values())[0]
            drm_info = testStepResults[0].get("drm_info")
            drm_key = ""
            for drm in drm_info:
                if arg[0] == drm.get("name"):
                    drm_key = ",".join(drm.get("keysystems"))
                    break;
            info["drm_key"] = drm_key


        # Network Plugin Response result parser steps
        elif tag == "network_get_interface_names":
            testStepResults = list(testStepResults[0].values())[0]
            interface_names = testStepResults[0].get("interface_names")
            interface_names = [ name for name in interface_names if name.strip() ]
            info["interface_names"] = ",".join(interface_names)

        elif tag == "network_get_endpoint_name":
            testStepResults = list(testStepResults[0].values())[0]
            endpoints = testStepResults[0].get("endpoints")
            if len(endpoints):
                info["endpointName"] = endpoints[0]
            else:
                info["endpointName"] = ""

        elif tag == "network_get_default_interface_name":
            testStepResults = list(testStepResults[0].values())[0]
            info["interface"] =  testStepResults[0].get("default_interface")

        elif tag == "network_toggle_interface_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("enabled")
            if str(status).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        #Parse the previous results and update only URL value
        elif tag == "controller_parse_configuration_values":
            testStepResults = list(testStepResults[0].values())[0]
            updatedConfiguration = testStepResults[0].get("configuration")
            updatedConfiguration['url'] = testStepResults[0].get("url")
            info["configuration"] = updatedConfiguration

        elif tag == "network_get_stb_ip":
            testStepResults = list(testStepResults[0].values())[0]
            info["Device_IP"] = testStepResults[0].get("ip")


        # Front Panel Plugin Response result parser steps
        elif tag == "frontpanel_get_brightness_levels":
            testStepResults = list(testStepResults[0].values())[0]
            range_type = testStepResults[0].get("range")
            step_value = str(testStepResults[0].get("step"))
            min_value  = str(testStepResults[0].get("min"))
            max_value  = str(testStepResults[0].get("max"))
            if len(arg) and arg[0] == "get_min_max":
                info["brightness"] = min_value + "," + max_value
            elif len(arg) and arg[0] == "get_max":
                info["brightness"] = max_value
            else:
                if range_type == "boolean":
                    info["brightness"] = min_value + "," + max_value
                else:
                    if step_value == "10":
                        mid_value = "50"
                    elif step_value == "20":
                        mid_value = "60"
                    else:
                        mid_value = step_value
                    info["brightness"] = min_value + "," + mid_value + "," + max_value

        elif tag == "frontpanel_get_clock_brightness":
            testStepResults = list(testStepResults[0].values())[0]
            brightness = testStepResults[0].get("brightness")
            if str(brightness) == "100":
                info["brightness"] = "50"
            else:
                info["brightness"] = "100"

        elif tag == "frontpanel_toggle_clock_mode":
            testStepResults = list(testStepResults[0].values())[0]
            hr24clock_mode = testStepResults[0].get("is24Hour")
            if str(hr24clock_mode).lower() == "false":
                info["is24Hour"] = True
            else:
                info["is24Hour"] = False

        elif tag == "frontpanel_set_led_info":
            testStepResults = list(testStepResults[0].values())[0]
            info["preferences"] = json.dumps(testStepResults[0].get("supported_leds_info")[0])

        # FrameRate Plugin Response result parser steps
        elif tag == "framerate_set_display_framerate":
            FramerateList = []
            testStepResults = list(testStepResults[0].values())[0]
            test_list = testStepResults[0].get("DisplayFrameRate")
            for value in test_list:
                if value not in FramerateList:
                    FramerateList.append(value)
            info["framerate"] = FramerateList

        # WebkitBrowser Plugin Response result parser steps
        elif tag == "webkitbrowser_toggle_visibility":
            testStepResults = list(testStepResults[0].values())[0]
            visibility = testStepResults[0].get("visibility")
            if visibility == "visible":
                info["visibility"] = "hidden"
            else:
                info["visibility"] = "visible"

        elif tag == "webkitbrowser_toggle_local_storage_availability":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "false":
                info["enabled"] = True
            else:
                info["enabled"] = False

        elif tag == "webkitbrowser_change_cookie_policy":
            testStepResults = list(testStepResults[0].values())[0]
            cookie_accept_policy = testStepResults[0].get("cookie_accept_policy")
            if cookie_accept_policy  == "always":
                info["cookie_accept_policy"] = "never"
            else:
                info["cookie_accept_policy"] = "always"

        elif tag == "webkitbrowser_get_useragent_string":
            testStepResults = list(testStepResults[0].values())[0]
            info["useragent"] = testStepResults[0].get("useragent")

        elif tag == "webkitbrowser_get_header":
            testStepResults = list(testStepResults[0].values())[0]
            header = testStepResults[0].get("headers")[0]
            if len(arg) and arg[0] == "get_name":
                info["name"] = header.get("name")
            elif len(arg) and arg[0] == "get_value":
                info["value"] = header.get("value")
            else:
                info = header

        elif tag == "webkitbrowser_check_average_fps":
            testStepResults = list(testStepResults[0].values())[0]
            fpsValues = 0;count = 0
            for result in testStepResults:
                count += 1
                fpsValues += int(result.get("fps"))
            average= fpsValues//count
            info["Average"] = average

        elif tag == "webkitbrowser_get_loaded_url":
            testStepResults = list(testStepResults[0].values())[0]
            info["url"] = testStepResults[0].get("url")

        elif tag == "webkitbrowser_lightningapp_get_loaded_url":
            testStepResults = list(testStepResults[0].values())[0]
            info["url"] = testStepResults[0].get("url")

        elif tag == "webkitbrowser_get_fps":
            testStepResults = list(testStepResults[0].values())[0]
            info["newFpsValue"] = int(testStepResults[0].get("fps"))

        # System plugin result parser steps
        elif tag == "system_get_previous_territory_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["territory"] = testStepResults[0].get("territory")

        elif tag == "system_get_previous_region_result":
            testStepResults = list(testStepResults[0].values())[0]
            territorys = testStepResults[0].get("territory")
            territoryAndregion = testStepResults[0].get("territoryAndregion")
            for territory in territorys:
                if arg[0] == territory:
                    info["region"] = str(territoryAndregion.get(territory))
                    break

        elif tag == "system_get_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            territory = testStepResults[0].get("territory")
            region = testStepResults[0].get("region")
            info["territoryAndregion"] = territory + region

        elif tag == "system_toggle_gz_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "system_switch_power_state":
            testStepResults = list(testStepResults[0].values())[0]
            powerState = testStepResults[0].get("powerState")
            if powerState in ("STANDBY","DEEP_SLEEP","LIGHT_SLEEP"):
                info["powerState"] = "ON"
            else:
                info["powerState"] = "STANDBY"

        elif tag == "system_get_available_standby_modes":
            testStepResults = list(testStepResults[0].values())[0]
            info["standbyMode"] = testStepResults[0].get("supportedStandbyModes")

        elif tag == "system_generate_new_temperature_thresholds":
            testStepResults = list(testStepResults[0].values())[0]
            if str(arg[0]) == "warn":
                info["WARN"] = float(testStepResults[0].get("temperature")) - 10
            if str(arg[1]) == "max":
                info["MAX"] = float(testStepResults[0].get("temperature")) + 10

        elif tag == "system_get_bluetooth_mac":
            testStepResults = list(testStepResults[0].values())[0]
            info["bluetooth_mac"] = testStepResults[0].get("bluetooth_mac")

        elif tag == "system_get_powerstate_before_reboot":
            testStepResults = list(testStepResults[0].values())[0]
            info["powerState"] = testStepResults[0].get("powerState")

        elif tag == "system_get_estb_mac":
            testStepResults = list(testStepResults[0].values())[0]
            info["estb_mac"] = testStepResults[0].get("estb_mac")

        elif tag == "system_get_core_temperature":
            testStepResults = list(testStepResults[0].values())[0]
            info["temperature"] = testStepResults[0].get("temperature")

        elif tag == "system_get_current_image_name":
            testStepResults = list(testStepResults[0].values())[0]
            info["image_name"] = testStepResults[0].get("current_FW_version")

        elif tag == "system_toggle_moca_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            value = testStepResults[0].get("mocaEnabled")
            if str(value).lower() == "true":
                info["value"] = False
            else:
                info["value"] = True

        elif tag == "system_generate_new_temperature_grace_interval":
            testStepResults = list(testStepResults[0].values())[0]
            info["graceInterval"] = int(testStepResults[0].get("graceInterval")) + 10

        elif tag == "system_get_device_details":
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) and arg[0] == "get_swupdate_file_status":
                info["FIRMWARE_UPGRADE_STATUS"] = testStepResults[0].get("FIRMWARE_UPGRADE_STATUS")
            elif len(arg) and arg[0] == "get_public_ip_address":
                info["PUBLIC_IP"] = testStepResults[0].get("PUBLIC_IP")
            else:
                info["value"] = testStepResults[0].get("details")

        elif tag == "system_get_time_zone":
            testStepResults = list(testStepResults[0].values())[0]
            info["timeZone"] = testStepResults[0].get("timeZone")

        elif tag == "system_get_formatted_time_zones":
            testStepResults = list(testStepResults[0].values())[0]
            zoneInfo = testStepResults[0].get("zoneinfo")
            info["timeZone"] = ",".join(zoneInfo)

        elif tag == "system_toggle_network_standby_mode_status":
            testStepResults = list(testStepResults[0].values())[0]
            nwStandby = testStepResults[0].get("nwStandby")
            if str(nwStandby).lower() == "true":
                info["nwStandby"] = False
            else:
                info["nwStandby"] = True

        elif tag == "system_get_firmware_rule_parameters":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["model"] = testStepResults1[0].get("details")
            testStepResults2 = list(testStepResults[len(testStepResults)-1].values())[0]
            info["estb_mac"] = testStepResults2[0].get("estb_mac")
            if len(testStepResults) == 4:
                firmwareConfig = list(testStepResults[2].values())[0]
                firmwareConfig = json.dumps(firmwareConfig[0])
                firmwareConfig = json.loads(firmwareConfig)
                firmwareConfig = firmwareConfig.get("new_firmware_configuration")
                info["configId"] = firmwareConfig.get("id")
            else:
                firmwareConfig = list(testStepResults[1].values())[0]
                firmwareConfig = json.dumps(firmwareConfig[0])
                firmwareConfig = json.loads(firmwareConfig)
                firmwareConfig = firmwareConfig.get("existing_firmware_configuration")
                info["configId"] = firmwareConfig[0].get("id")

        # user Preferences result parser steps
        elif tag == "userpreferences_switch_ui_language":
            testStepResults = list(testStepResults[0].values())[0]
            language = testStepResults[0].get("language")
            if "en" in str(language):
                info["language"] = "es"
            else:
                info["language"] = "en"

        # HdmiCecSink plugin result parser steps
        elif tag =="hdmicecsink_get_physical_logical_address":
            testStepResults1 = list(testStepResults[0].values())[0]
            testStepResults2 = list(testStepResults[1].values())[0]
            info["logicalAddress"] = testStepResults1[0].get("logicalAddress")
            info["physicalAddress"] = testStepResults2[0].get("physicalAddress")

        # RDK Shell plugin result parser steps
        elif tag =="rdkshell_revert_get_cursor_size":
            testStepResults = list(testStepResults[0].values())[0]
            info["width"] = testStepResults[0].get("width")
            info["height"] = testStepResults[0].get("height")

        elif tag =="rdkshell_get_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["configvalue"] = testStepResults[0].get("configvalue")

        elif tag == "rdkshell_get_cursor_width":
            testStepResults = list(testStepResults[0].values())[0]
            info["width"] = testStepResults[0].get("width")

        elif tag =="rdkshell_get_cursor_height":
            testStepResults = list(testStepResults[0].values())[0]
            widths = testStepResults[0].get("width")
            cursor_dict=testStepResults[0].get("cursor_dict")
            for width in widths:
                if arg[0] == width:
                    info["height"]=cursor_dict.get(width)
                    break
        
        elif tag == "rdkshell_get_connected_client":
            testStepResults = list(testStepResults[0].values())[0]
            clients = testStepResults[0].get("clients")
            if len(arg) and arg[0] == "get_all_clients":
                info["client"] = ",".join(clients)
            else:
                index = int(arg[0])
                if len(clients):
                    if len(arg) > 1:
                        if arg[1] == "target":
                            info["target"] = clients[index]

                    else:
                        info["client"] = clients[index]
                else:
                    info["client"] = ""
                    info["target"] = ""

        elif tag == "rdkshell_get_clients_state":
            testStepResults = list(testStepResults[0].values())[0]
            result = testStepResults[0].get("state")
            print(result)
            info["callsign"] = result[int(arg[0])].get("callsign")

        elif tag =="visibility_toggle_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("visible")
            if str(status).lower() == "true":
                info["visible"] = False
            else:
                info["visible"] = True

        elif tag =="rdkshell_generate_new_opacity_value":
            testStepResults = list(testStepResults[0].values())[0]
            opacity = str(testStepResults[0].get("opacity"))
            #Check if the current opacity is set to 75 if not set it to 75 for testing.
            #If curretnt value is 75 then set to 50 for testing.
            if int(opacity) != 75:
                info["opacity"] = 75
            else:
                info["opacity"] = 50

        elif tag =="rdkshell_generate_new_scale_value":
            testStepResults = list(testStepResults[0].values())[0]
            #Generate a new scaling values by incrementing 1 to the given value
            if len(arg) > 0:
                if str(arg[0]) == "sx":
                    info["sx"] = float(testStepResults[0].get("sx")) + 1
                if str(arg[0]) == "sy":
                    info["sy"] = float(testStepResults[0].get("sy")) + 1
            else:
                info["sx"] = float(testStepResults[0].get("sx")) + 1
                info["sy"] = float(testStepResults[0].get("sy")) + 1

        elif tag =="rdkshell_get_last_client_zorder":
            testStepResults = list(testStepResults[0].values())[0]
            clients = testStepResults[0].get("clients")
            info["client"] = str(clients[(len(clients)-1)])

        elif tag == "rdkshell_get_zorder":
            testStepResults = list(testStepResults[0].values())[0]
            clients = testStepResults[0].get("clients")
            if len(clients):
                index = int(arg[0])
                if len(arg) > 1 and arg[1] == "target":
                    info["target"] = clients[index]
                elif len(arg)> 1 and arg[1] == "behind":
                    info["behind"] = clients[index]
                else:
                    info["client"] = clients[index]
            else:
                info["client"] = ""
                info["target"] = ""
        
        elif tag == "rdkshell_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enable"] = False
            else:
                info["enable"] = True

        elif tag == "rdkshell_set_virtual_resolution":
            testStepResults = list(testStepResults[0].values())[0]
            width = testStepResults[0].get("width")
            height = testStepResults[0].get("height")
            if len(arg) and arg[0] == "set_screen_resolution":
                info["w"] = width
                info["h"] = height
            else:
                info["width"] = width
                info["height"] = height

        elif tag == "rdkshell_get_image_path":
            testStepResults = list(testStepResults[0].values())[0]
            imagePath = testStepResults[0].get("imagepath")
            info["path"] = imagePath

        #Display info plugin result parser steps
        elif tag == "display_info_get_supported_resolution_list":
            testStepResults = list(testStepResults[0].values())[0]
            SupportingRes = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(SupportingRes)

        elif tag == "displayinfo_get_connected_device_edid":
            testStepResults = list(testStepResults[0].values())[0]
            info["connected_device_edid"] = testStepResults[0].get('connected_device_edid')

        # Parser Code for ActivityMonitor plugin
        elif tag == "activitymonitor_get_appPid":
            testStepResults = list(testStepResults[0].values())[0]
            app_list=testStepResults[0].get("applicationMemory")
            if len(app_list) > 0:
                pid=app_list[0].get("appPid")
                if pid and int(pid) > 0:
                    info["pid"] = pid
                else:
                    info["pid"] = ""
            else:
                info["pid"] = ""

        # HDMI CEC plugin result parser steps
        elif tag == "hdmicec_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "hdmicec_get_base64_data":
            testStepResults = list(testStepResults[0].values())[0]
            message  = testStepResults[0].get("message")
            info["message"] = message


        #Parser code for State Observer plugin
        elif tag == "StateObserver_change_version":
            testStepResults = list(testStepResults[0].values())[0]
            version = testStepResults[0].get("version")
            if int(float(version)) == 1:
                info["version"] = 2
            else:
                info["version"] = 1

        #Parser code for FirmwareController plugin
        elif tag == "change_image_version":
            testStepResults = list(testStepResults[0].values())[0]
            info["image"] = testStepResults[0].get("image")

        # Display Settings Plugin result parser steps
        elif tag == "display_get_isconnected_status":
            testStepResults = list(testStepResults[0].values())[0]
            is_connected = testStepResults[0].get("is_connected")
            info["is_connected"] = is_connected

        elif tag =="set_video_display":
            testStepResults = list(testStepResults[0].values())[0]
            video_display = testStepResults[0].get("video_display")
            info["videoDisplay"] = video_display[0]
            info["portName"] = video_display[0]

        elif tag =="get_supported_sound_modes":
            testStepResults = list(testStepResults[0].values())[0]
            supported_sound_modes = testStepResults[0].get("supported_audio_modes")
            info["soundMode"] = ",".join(supported_sound_modes)

        elif tag =="get_supported_resolutions":
            testStepResults = list(testStepResults[0].values())[0]
            supportedResolutions = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(supportedResolutions)

        elif tag =="get_supported_audio_profiles":
            testStepResults = list(testStepResults[0].values())[0]
            audioProfiles = testStepResults[0].get("supportedMS12AudioProfiles")
            if len(arg) and arg[0] == "get_profiles_without_off":
                if "Off" in audioProfiles:
                    audioProfiles.remove("Off")
                    info["ms12AudioProfile"] = ",".join(audioProfiles)
                    info["profileName"] = ",".join(audioProfiles)
                else:
                    info["profileName"] = ",".join(audioProfiles)
                    info["ms12AudioProfile"] = ",".join(audioProfiles)
            else:
                info["profileName"] = ",".join(audioProfiles)
                info["ms12AudioProfile"] = ",".join(audioProfiles)

        elif tag == "set_profile_name":
            info["profileName"] = arg[0]

        elif tag == "get_connected_audio_port":
            testStepResults = list(testStepResults[0].values())[0]
            audioPorts = testStepResults[0].get("connected_audio_port")
            if "HDMI0" in audioPorts:
                info["audioPort"] = "HDMI0"
            elif "SPEAKER0" in audioPorts:
                info["audioPort"] = "SPEAKER0"
            else:
                info["audioPort"] = audioPorts[0]

        elif tag =="get_formatted_sound_modes":
            testStepResults = list(testStepResults[0].values())[0]
            supported_sound_modes = testStepResults[0].get("supported_audio_modes")
            soundModes = []
            for mode in supported_sound_modes:
                if "AUTO" in mode:
                    soundModes.append("AUTO")
                else:
                    soundModes.append(mode)
            info["soundMode"] = ",".join(soundModes)

        elif tag =="get_settop_and_tv_resolutions":
            testStepResults1 = list(testStepResults[0].values())[0]
            testStepResults2 = list(testStepResults[1].values())[0]
            supportedTvResolutions = testStepResults1[0].get("supportedTvResolutions")
            supportedSettopResolutions = testStepResults2[0].get("supportedSettopResolutions")
            commonResolutions = list(set(supportedTvResolutions) & set(supportedSettopResolutions))
            info["commonResolutions"] = ",".join(commonResolutions)

        elif tag =="get_selected_resolutions":
            resolutionsList = []
            testStepResults1 = list(testStepResults[0].values())[0]
            testStepResults2 = list(testStepResults[1].values())[0]
            supportedResolutions = testStepResults1[0].get("supportedResolutions")
            currentResolution = testStepResults2[0].get("resolution")
            supportedResolutions.remove(currentResolution)
            resolutionsList.append(supportedResolutions[0])
            resolutionsList.append(supportedResolutions[len(supportedResolutions)//2])
            resolutionsList.append(supportedResolutions[len(supportedResolutions)-1])
            info["resolution"] = resolutionsList

        elif tag == "get_default_resolution":
            testStepResults = list(testStepResults[0].values())[0]
            info["defaultResolution"] = testStepResults[0].get("defaultResolution")

        elif tag == "get_audio_delay":
            testStepResults = list(testStepResults[0].values())[0]
            info["audioDelay"] = testStepResults[0].get("audioDelay")

        elif tag == "displaysettings_get_default_values":
            testStepResults = list(testStepResults[0].values())[0]
            info["defaultValue"] = testStepResults[0].get("defaultValue")
            if len(arg) and arg[0] == "get_default_mode":
                info["defaultMode"] = testStepResults[0].get("defaultMode")

        elif tag == "displaysettings_generate_new_value":
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) and arg[0] == "bass_enhancer":
                bassBoost = testStepResults[0].get("bassBoost")
                if bassBoost != 75:
                    info["ms12SettingsValue"] = "75"
                else:
                    info["ms12SettingsValue"] = "50"
            elif len(arg) and arg[0] == "dialog_enhancement":
                enhancerLevel = testStepResults[0].get('enhancerlevel')
                if enhancerLevel != 12:
                    info["ms12SettingsValue"] = "12"
                else:
                    info["ms12SettingsValue"] = "8"
            elif len(arg) and arg[0] == "volume_leveller":
                VolumeLeveller = testStepResults[0].get('level')
                if VolumeLeveller != 10:
                    info["ms12SettingsValue"] = "10"
                else:
                    info["ms12SettingsValue"] = "1"

        elif tag =="get_supported_color_depth_capabilities":
            testStepResults = list(testStepResults[0].values())[0]
            supportedColorDepth = testStepResults[0].get("supportedColorDepth")
            info["colorDepth"] = ",".join(supportedColorDepth)

        elif tag =="get_previous_volume_level":
            testStepResults1 = list(testStepResults[0].values())[0]
            volumeLevel = testStepResults1[0].get("volumeLevel")
            volumeLevel_float = float(volumeLevel)
            volumeLevel_int = int(volumeLevel_float)
            info["volumeLevel"] = volumeLevel_int+1

        elif tag =="get_previous_volume_level_for_decrease":
            testStepResults1 = list(testStepResults[0].values())[0]
            volumeLevel = testStepResults1[0].get("volumeLevel")
            volumeLevel_float = float(volumeLevel)
            volumeLevel_int = int(volumeLevel_float)
            info["volumeLevel"] = volumeLevel_int-1

        elif tag =="get_previous_increase_keycode_volume_level":
            testStepResults1 = list(testStepResults[0].values())[0]
            volumeLevel = testStepResults1[0].get("volumeLevel")
            volumeLevel_float = float(volumeLevel)
            volumeLevel_int = int(volumeLevel_float)
            info["volumeLevel"] = volumeLevel_int+5

        elif tag =="get_previous_decrease_keycode_volume_level":
            testStepResults1 = list(testStepResults[0].values())[0]
            volumeLevel = testStepResults1[0].get("volumeLevel")
            volumeLevel_float = float(volumeLevel)
            volumeLevel_int = int(volumeLevel_float)
            info["volumeLevel"] = volumeLevel_int-5

        elif tag =="get_keycode_mute_status":
            testStepResults1 = list(testStepResults[0].values())[0]
            mutedStatus = testStepResults1[0].get("muted")
            if mutedStatus.lower() == "true":
                info["mutedStatus"] = "False"
            else:
                info["mutedStatus"] = "True"

        # Wifi Plugin Response result parser steps
        elif tag == "wifi_toggle_adapter_state":
            testStepResults = list(testStepResults[0].values())[0]
            state = str(testStepResults[0].get("state"))
            if len(arg) and arg[0] == "get_state_no":
                if state == "1":
                    info["state"] = "2"
                else:
                    info["state"] = "1"
            else:
                if state == "1":
                    info["enable"] = True
                else:
                    info["enable"] = False

        elif tag == "wifi_toggle_signal_threshold_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("enabled")
            if len(arg) and arg[0] == "get_toggle_value":
                if str(status).lower() == "false":
                    info["enabled"] = True
                else:
                    info["enabled"] = False

        # Bluetooth Plugin Response result parser steps
        elif tag == "bluetooth_toggle_discoverable_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("discoverable")
            if str(status).lower() == "true":
                info["discoverable"] = False
            else:
                info["discoverable"] = True

        elif tag == "bluetooth_get_device_id":
            testStepResults = list(testStepResults[0].values())[0]
            info["deviceID"] = testStepResults[0].get("deviceID")

        # Logging Preferences Plugin Response result parser steps
        elif tag == "loggingpreferences_toggle_keystroke_mask_state":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get("keystrokeMaskEnabled")
            if str(status).lower()== "false":
                info["keystrokeMaskEnabled"] = True
            else:
                info["keystrokeMaskEnabled"] = False

        #Timer Plugin Response result parser steps
        elif tag == "timer_start_timer_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["timerId"] = testStepResults[0].get("timerId")


        # Messenger Plugin Response result parser steps
        elif tag == "messenger_get_roomid":
            testStepResults = list(testStepResults[0].values())[0]
            info["roomid"] = testStepResults[0].get("roomid")

        # HdmiInput plugin result parser steps
        elif tag == "hdmiinput_get_portids":
            testStepResults = list(testStepResults[0].values())[0]
            port_id_list = testStepResults[0].get("portIds")
            if len(arg) and arg[0] == "deviceid":
                info["deviceId"] = ",".join(port_id_list)
            else:
                info["portId"] = ",".join(port_id_list)

        #CompositeInput plugin result parser steps
        elif tag == "compositeinput_get_portids":
            testStepResults = list(testStepResults[0].values())[0]
            port_id_list = testStepResults[0].get("portIds")
            info["portId"] = ",".join(port_id_list)

        #PlayerInfo Plugin Response result parser steps
        elif tag == "player_info_get_resolutions":
            testStepResults = list(testStepResults[0].values())[0]
            SupportingRes = testStepResults[0].get("supportedResolutions")
            info["resolution"] = ",".join(SupportingRes)

        # TextToSpeech Plugin Response result parser steps
        elif tag == "texttospeech_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled_status = testStepResults[0].get("enabletts")
            if str(enabled_status).lower() == "true":
                info["enabletts"] = False
            else:
                info["enabletts"] = True

        # XCast Plugin Response result parser steps
        elif tag == "xcast_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled_status = testStepResults[0].get("enabled")
            if str(enabled_status).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True
        elif tag == "xcast_toggle_standby_behavior_status":
            testStepResults = list(testStepResults[0].values())[0]
            standbyBehavior = testStepResults[0].get("standbybehavior")
            if str(standbyBehavior).lower() == "active":
                info["standbybehavior"] = "inactive"
            else:
                info["standbybehavior"] = "active"

        # DTV Plugin Response result parser steps
        elif tag == "dtv_get_service_info":
            testStepResults = list(testStepResults[0].values())[0]
            if len(arg) and arg[0] == "get_first_service":
                service = testStepResults[0].get("Service_List")[0]
                info["dvburi"] = service.get("dvburi")
                info["lcn"] = service.get("lcn")

        elif tag == "dtv_get_play_handle":
            testStepResults = list(testStepResults[0].values())[0]
            info["value"] = testStepResults[0].get("result")

        elif tag == "dtv_get_country_list":
            testStepResults = list(testStepResults[0].values())[0]
            country_list  = testStepResults[0].get("Country_List")
            if len(arg) and arg[0] == "get_country_code":
                country_code = []
                for country in country_list:
                    code = country.get("code")
                    country_code.append(code)
                country_code = [ str(code) for code in country_code ]
                info["country_code"] = ",".join(country_code)
            elif len(arg) and arg[0] == "get_no_of_countries":
                info["no_of_countries"] = len(country_list)
            else:
                info["Country_List"] = country_list

        elif tag == "dtv_get_events_params":
            testStepResults1 = list(testStepResults[0].values())[0]
            testStepResults2 = list(testStepResults[1].values())[0]
            service = testStepResults1[0].get("Service_List")
            nowEvent = testStepResults2[0].get("now")
            nextEvent = testStepResults2[0].get("next")
            dvburi = service[0].get("dvburi")
            nowEvent_startTime = nowEvent.get("starttime")
            nextEvent_startTime = nextEvent.get("starttime")
            if len(arg) and arg[0] == "get_now_event_params":
                nowEvent_duration = nowEvent.get("duration")
                nowEvent_endTime = (int(nowEvent_startTime) + int(nowEvent_duration)- 100)
                value = dvburi+":"+str(nowEvent_startTime)+","+str(nowEvent_endTime)
                info["dvburi"] = value
            elif len(arg) and arg[0] == "get_now_next_event_params":
                nextEvent_duration = nextEvent.get("duration")
                nextEvent_endTime = (int(nextEvent_startTime)+int(nextEvent_duration) - 100)
                value = dvburi+":"+str(nowEvent_startTime)+","+str(nextEvent_endTime)
                info["dvburi"] = value

        elif tag == "dtv_get_events_expected_values":
            testStepResults = list(testStepResults[0].values())[0]
            nowEvent = testStepResults[0].get("now")
            nextEvent = testStepResults[0].get("next")
            info["nowEvent_EventID"] = nowEvent.get("eventid")
            info["nextEvent_EventID"] = nextEvent.get("eventid")

        elif tag == "dtv_get_random_services_dvburi":
            dvburi = []
            service_list = []
            testStepResults = list(testStepResults[0].values())[0]
            services = testStepResults[0].get("Service_List")
            if len(services) >= 3:
                for value in range(3):
                    service_list.append(services[random.randrange(0,(len(services)-1))])
            else:
                service_list = services

            for value in service_list:
                dvburi.append(str(value.get("dvburi")))
            info["dvburi"] = ",".join(dvburi)

        elif tag == "dtv_get_random_services_lcn":
            testStepResults = list(testStepResults[0].values())[0]
            services = testStepResults[0].get("Service_List")
            for service in services:
                if arg[0] == service.get("dvburi"):
                    info["lcn"] = service.get("lcn")
                    break
        # TVControlSettings Plugin Response result parser steps
        elif tag == "tvcontrolsettings_get_aspect_ratio":
            testStepResults = list(testStepResults[0].values())[0]
            info["aspectRatio"] = testStepResults[0].get("aspectRatio")

        elif tag == "tvcontrolsettings_get_supported_modes":
            Modes = []
            testStepResults = list(testStepResults[0].values())[0]
            supportedModes = testStepResults[0].get(arg[0])
            for value in supportedModes:
                Modes.append(str(value))
            info[arg[1]] = ",".join(Modes)

        elif tag == "tvcontrolsettings_get_saved_data":
            testStepResults = list(testStepResults[0].values())[0]
            info[arg[0]] = testStepResults[0].get(arg[0])

        elif tag == "tvcontrolsettings_get_selected_mode":
            testStepResults = list(testStepResults[0].values())[0]
            info[arg[0]] = testStepResults[0].get("randomnumber")

        elif tag == "tvcontrolsettings_get_default_values":
            testStepResults = list(testStepResults[0].values())[0]
            info["defaultValue"] = testStepResults[0].get("defaultValue")

        # Security Agent Plugin Response result parser steps
        elif tag == "securityagent_get_token":
            testStepResults = list(testStepResults[0].values())[0]
            info["token"] = testStepResults[0].get("securityToken")

        # LISA Plugin Response result parser steps
        elif tag == "lisa_get_handle":
            testStepResults = list(testStepResults[0].values())[0]
            info["handle"] = testStepResults[0].get("Result")

        # OCIContainer Plugin Response result parser steps
        elif tag == "ocicontainer_get_process_id":
            testStepResults = list(testStepResults[0].values())[0]
            info["processID"] = testStepResults[0].get("processID")

        elif tag == "ocicontainer_get_container_details":
            testStepResults = list(testStepResults[0].values())[0]
            info["descriptor"] = testStepResults[0].get("descriptor")

        # HdmiCec2 Plugin Response result parser steps
        elif tag == "hdmicec2_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        # Controller Plugin Response result parser steps
        elif tag == "controller_get_plugin_name":
            testStepResults = list(testStepResults[0].values())[0]
            info["callsign"] = testStepResults[0].get("callsign")

        elif tag == "controller_get_plugin_state":
            testStepResults = list(testStepResults[0].values())[0]
            info["state"] = testStepResults[0].get("state")

        # Usb Access Plugin Response result parser steps
        elif tag =="usbaccess_getlink_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            links = testStepResults[0].get("links")
            info["baseURL"] = links.get("baseURL")

        elif tag =="usbaccess_get_mountdevice_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["path"] = testStepResults[0]['mounted'][0]

        elif tag =="usbaccess_get_createlink_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["baseURL"] = testStepResults[0].get("baseURL")

        elif tag =="usbaccess_get_logfilepath_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["path"] = testStepResults[0].get("path")

        elif tag =="usbaccess_get_firmwarefile_previous_result":
            testStepResults = list(testStepResults[0].values())[0]
            info["path"] = testStepResults[0].get("dummyfirmwarefile")
        
        # Combinatinal Plugin Response result parser steps
        elif tag =="get_previous_firmware_version":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["imagename"] = testStepResults1[0].get("imagename")
            testStepResults2 = list(testStepResults[1].values())[0]
            info["imageVersion"] = testStepResults2[0].get("imageVersion")
        
        elif tag =="get_previous_Serial_Number":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["serialnumber"] = testStepResults1[0].get("serialnumber")
            testStepResults2 = list(testStepResults[1].values())[0]
            info["serialNumber"] = testStepResults2[0].get("serialNumber")

        elif tag =="get_previous_audio_ports":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["supportedAudioPorts"] = testStepResults1[0].get("supportedAudioPorts")

        elif tag =="get_previous_video_ports":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["supportedVideoDisplays"] = testStepResults1[0].get("supportedVideoDisplays")

        elif tag =="get_previous_host_EDID":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["EDID"] = testStepResults1[0].get("EDID")
            testStepResults2 = list(testStepResults[1].values())[0]
            info["host_edid"] = testStepResults2[0].get("host_edid")

        elif tag =="get_previous_hdcp_version":
            testStepResults = list(testStepResults[0].values())[0]
            info["hdcp_version"] = testStepResults[0].get("supportedHDCPVersion")

        elif tag =="get_previous_default_resolution":
            testStepResults = list(testStepResults[0].values())[0]
            info["defaultResolution"] = testStepResults[0].get("defaultResolution")

        # HdmiCecSource Plugin Response result parser steps
        elif tag =="hdmicecsource_get_previous_vendor_id":
            testStepResults = list(testStepResults[0].values())[0]
            info["vendorid"] = testStepResults[0].get("vendorID")

        # NetworkManager Plugin Response result parser steps
        elif tag == "networkmanager_get_interface_names":
            testStepResults = list(testStepResults[0].values())[0]
            interface_names = testStepResults[0].get("interface_names")
            interface_names = [ name for name in interface_names if name.strip() ]
            info["interface_names"] = ",".join(interface_names)
        
        elif tag == "networkmanager_get_previous_public_ip":
            testStepResults = list(testStepResults[0].values())[0]
            info["PUBLIC_IP"] = testStepResults[0].get("PUBLIC_IP")

        elif tag == "networkmanager_get_previous_primary_interface":
            testStepResults = list(testStepResults[0].values())[0]
            info["interface"] = testStepResults[0].get("default_interface")

        elif tag == "networkmanager_get_previous_stun_endpoint":
            testStepResults1 = list(testStepResults[0].values())[0]
            info["endpoint"] = testStepResults1[0].get("endpoint")
            testStepResults2 = list(testStepResults[0].values())[0]
            info["port"] = testStepResults2[0].get("port")

        elif tag == "networkmanager_get_previous_connectivity_test_endpoint":
            testStepResults = list(testStepResults[0].values())[0]
            info["endpoints"] = testStepResults[0].get("endpoints")

        # Monitor Plugin Response result parser steps
        elif tag =="monitor_get_webkit_presence":
            testStepResults = list(testStepResults[0].values())[0]
            info["webkit_presence"] = testStepResults[0].get("webkitbrowser_details_presence")

        # Miracast Response result parser steps
        elif tag =="miracast_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        # UserSettings Response result parser steps
        elif tag == "usersettings_toggle_status":
            testStepResults = list(testStepResults[0].values())[0]
            status = testStepResults[0].get(arg[0])
            if str(status).lower().strip() == "true":
                info[arg[0]] = False
            else:
                info[arg[0]] = True

        elif tag == "usersettings_toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower().strip() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        elif tag == "usersettings_toggle_pinControl_status":
            testStepResults = list(testStepResults[0].values())[0]
            pinControl = testStepResults[0].get("pinControl")
            if str(pinControl).lower().strip() == "true":
                info["pinControl"] = False
            else:
                info["pinControl"] = True

        elif tag == "usersettings_toggle_liveWatershed_status":
            testStepResults = list(testStepResults[0].values())[0]
            liveWatershed = testStepResults[0].get("liveWatershed")
            if str(liveWatershed).lower().strip() == "true":
                info["liveWatershed"] = False
            else:
                info["liveWatershed"] = True

        elif tag == "usersettings_toggle_playbackWatershed_status":
            testStepResults = list(testStepResults[0].values())[0]
            playbackWatershed = testStepResults[0].get("playbackWatershed")
            if str(playbackWatershed).lower().strip() == "true":
                info["playbackWatershed"] = False
            else:
                info["playbackWatershed"] = True

        # Common Response result parser steps
        elif tag =="toggle_enabled_status":
            testStepResults = list(testStepResults[0].values())[0]
            enabled = testStepResults[0].get("enabled")
            if str(enabled).lower() == "true":
                info["enabled"] = False
            else:
                info["enabled"] = True

        else:
            print("\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag))
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))

    return status,info



#-----------------------------------------------------------------------------------------------
# checkTestCaseApplicability
#-----------------------------------------------------------------------------------------------
# Syntax      : checkTestCaseApplicability(methodTag,configKeyData,arguments)
# Description : Method to check whether the current test is applicable for the device or not
# Parameter   : configKeyData - Key data from the device/platform config file
#             : methodTag - tag used to identify the parser step
#             : arguments - list of arguments used for parsing
# Return Value: Function execution status & Applicability Status (TRUE/FALSE)
#-----------------------------------------------------------------------------------------------

def checkTestCaseApplicability(methodTag,configKeyData,arguments):
    tag  = methodTag
    arg  = arguments
    keyData  = configKeyData

    # Input Variables:
    # a. configKeyData - list
    # b. methodTag - string
    # c. arguments - list

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.result - (TRUE/FALSE)
    #   1.It is the actual variable which indicates
    #   test case applicability

    # DO NOT OVERRIDE THE RETURN VARIABLES "RESULT" &
    # "STATUS" WITHIN PARSER STEPS TO STORE SOME OTHER
    # DATA. USER CAN ONLY UPDATE "RESULT" WITH (TRUE/FALSE)

    result = "TRUE"
    status = "SUCCESS"

    # USER CAN ADD N NUMBER OF PREVIOUS RESULT PARSER
    # STES BELOW
    try:
        if tag == "is_plugin_applicable":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "frontpanel_check_feature_applicability":
            if all(item in keyData for item in arg):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "displaysetting_check_feature_applicability":
            if all(item in keyData for item in arg):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "is_led_supported":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "warehouse_na_tests":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "deviceinfo_na_tests":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "displayinfo_na_tests":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "playerinfo_na_tests":
            if arg[0] not in keyData:
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "bt_na_tests":
            if arg[0] not in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "network_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "wifi_check_feature_applicability":
            if arg[0] in keyData:
                result = "TRUE"
            else:
                result = "FALSE"
        elif tag == "controller_check_feature_applicability":
            if arg[0] in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "rdkshell_check_feature_applicability":
            if arg[0] in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "firmwarecontrol_check_feature_applicability":
            if all(item in keyData for item in arg):
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "system_check_feature_applicability":
            if str(arg[0]).lower() in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        elif tag == "networkmanager_check_feature_applicability":
            if str(arg[0]).lower() in str(keyData).lower():
                result = "TRUE"
            else:
                result = "FALSE"

        else:
            print("\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag))
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))

    return status,result


#-----------------------------------------------------------------------------------------------
# generateComplexTestInputParam
#-----------------------------------------------------------------------------------------------
# Syntax      : generateComplexTestInputParam(methodTag,testParams)
# Description : Method to generate complex test input parameters which cannot be generated
#               by the framework
# Parameter   : testParams - test params collected by the framework
#             : methodTag - tag used to identify the parser step
# Return Value: Function execution status & User Generated param Dictionary
#-----------------------------------------------------------------------------------------------
def generateComplexTestInputParam(methodTag,testParams):
    tag = methodTag

    # Input Variables:
    # a. testParams - test params to be re-formed
    # b. methodTag - string

    # Output variables:
    # a.status - (SUCCESS/FAILURE)
    #   1.It means the status of the parsing action
    #   By default is SUCCESS, it any exception occurs
    #   while parsing then status will be FAILURE
    # b.userGeneratedParam - dictionary/str/list
    #   1.Test params can be reformed in anyway
    #   and any data type.By default its dict

    # DO NOT OVERRIDE THE RETURN VARIABLE "STATUS"
    # WITHIN PARSER STEPS TO STORE SOME OTHER DATA.
    # USER CAN OVERRIDE "USERGENERATEDPARAM" WITH
    # RE-FORMED TEST INPUT PARAM

    status = "SUCCESS"
    userGeneratedParam = {}

    # USER CAN ADD N NUMBER OF PARAM REFORMING
    # STES BELOW
    try:

        if tag == "get_same_param":
            userGeneratedParam = testParams
        elif tag == "webkitbrowser_get_header_params":
            userGeneratedParam = [testParams]
        elif tag == "monitor_get_restart_params":
            userGeneratedParam = { "callsign": testParams.get("callsign"), "restart": { "limit": testParams.get("limit") ,  "window": testParams.get("window") }}
        elif tag == "rdkshell_set_keys_params":
            newtestParams = []
            for value in testParams.get("keyCode"):
                if "callsign" in testParams and len(testParams.get("callsign")) > 0:
                    keysValue = {"callsign": testParams.get("callsign"),"keyCode" : int(value),"modifiers": testParams.get("modifiers"),"delay": testParams.get("delay")}
                else:
                    keysValue = {"keyCode" : int(value),"modifiers": testParams.get("modifiers"),"delay": testParams.get("delay")}
                newtestParams.append(keysValue)
            userGeneratedParam = {"keys":newtestParams}
        elif tag == "rdkshell_set_launch_params":
            userGeneratedParam = { "callsign": testParams.get("callsign"), "configuration": { "closurepolicy": testParams.get("closurepolicy") } }
        elif tag == "rdkshell_set_launch_app_params":
            userGeneratedParam = { "callsign": testParams.get("callsign"),"type": testParams.get("type"),"visible": testParams.get("visible"),"configuration": { "url": testParams.get("url") } }
        elif tag == "rdkshell_set_keylistener_params":
            newtestParams = testParams.copy()
            newtestParams.pop("client")
            userGeneratedParam = {"keys": [newtestParams],"client": testParams.get("client") }
        elif tag == "rdkshell_set_animations_params":
            userGeneratedParam = {"animations":[testParams]}
        elif tag == "rdkshell_add_key_intercepts":
            print(testParams,"testParams")
            userGeneratedParam = {"intercepts": [{"client":testParams.get("client1"),"keys":[{"keyCode":int(testParams.get("keyCode1")),"modifiers": testParams.get("modifiers")}]},{"client":testParams.get("client2"),"keys":[{"keyCode":int(testParams.get("keyCode2")),"modifiers": testParams.get("modifiers")}]}]}
        elif tag == "cobalt_set_accessibility_params":
            newtestParams = testParams.copy()
            newtestParams.pop("ishighcontrasttextenabled")
            userGeneratedParam = {"closedcaptions": newtestParams, "textdisplay": { "ishighcontrasttextenabled": testParams.get("ishighcontrasttextenabled") } }
        elif tag == "dtv_set_service_search_params":
            newtestParams = testParams.copy()
            newtestParams.pop("tunertype")
            newtestParams.pop("searchtype")
            newtestParams.pop("retune")
            newtestParams.pop("usetuningparams")
            userGeneratedParam = { "tunertype":testParams.get("tunertype"),"searchtype":testParams.get("searchtype"),"retune":testParams.get("retune"),"usetuningparams":testParams.get("usetuningparams"),"dvbctuningparams":newtestParams}
        elif tag == "system_set_thresholds_params":
            userGeneratedParam = {"thresholds":testParams}
        elif tag == "webkit_browser_configuration":
            userGeneratedParam = testParams.get("configuration")

        else:
            print("\nError Occurred: [%s] No Parser steps available for %s" %(inspect.stack()[0][3],methodTag))
            status = "FAILURE"

    except Exception as e:
        status = "FAILURE"
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))

    return status,userGeneratedParam


#-----------------------------------------------------------------------------------------------
# ExecExternalFnAndGenerateResult
#-----------------------------------------------------------------------------------------------
# Syntax      : ExecExternalFnAndGenerateResult(methodTag,arguments,expectedValues,execInfo)
# Description : Method to execute other user defined functions by the framework
# Parameter   : methodTag - tag used to identify the function ti be called
#             : arguments - arguments to be passed to the function
#             : expectedValues - expected values to be checked
#             : execInfo - list of execution details like TM path, device IP, MAC, exec method
# Return Value: Result Info Dictionary
#-----------------------------------------------------------------------------------------------
def ExecExternalFnAndGenerateResult(methodTag,arguments,expectedValues,execInfo):
    tag  = methodTag
    arg  = arguments
    basePath = execInfo[0]
    deviceConfigFile = execInfo[1]
    deviceIP = execInfo[2]
    tm_url = execInfo[5]
    deviceName = execInfo[6]
    deviceType=execInfo[7]

    # Input Variables:
    # a. methodTag - string
    # b. arguments - list
    # c. expectedValues - list
    # d. execInfo - list

    # Output Variable:
    # a.info - dictionary
    #   1.info can have N different result key-value
    #    pairs based on user's need
    #   2.info must have "Test_Step_Status" key to
    #   update the status. By default its SUCCESS

    # USER MUST GENERATE THE TEST STEP RESULT FROM THE
    # EXTERNAL FUNCTION TO BE INVOKED AND UPDATE INFO
    # WITH THOSE RESULTS

    info = {}
    info["Test_Step_Status"] = "SUCCESS"

    # USER CAN ADD N NUMBER OF FUNCTION CALL STEPS BELOW

    try:
        print("\n\n---------- Executing Function ------------")
        print("FUNCTION TAG     :", tag)
        if tag == "executeBluetoothCtl":
            info["Test_Step_Status"] = executeBluetoothCtl(deviceConfigFile,arg)
        elif tag == "broadcastIARMEventTuneReady":
            command = "IARM_event_sender TuneReadyEvent 1"
            info["details"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "broadcastIARMEventChannelMap":
            command = "IARM_event_sender ChannelMapEvent 1"
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "Trust_MAC":
            deviceType = arguments[0]
            command = "bluetoothctl <<< 'trust "+arguments[1]+"'"
            executeCommand(execInfo, command, deviceType)
        elif tag == "Enable_TR181_Parameter":
            command = arguments[0]
            output = executeCommand(execInfo, command)
            if "set operation success" in output.lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag =="get_configfile_value":
            info["configvalue"] = arg[0]

        elif tag =="validate_config_file_value":
            if len(arg) != 0:
                message ="RDKSHELL_WPEFRAMEWORK_SERVICE_FILEPATH configured value in device config file : "+arg[0]
                info["Test_Step_Message"] = message
                info["configvalue"] = arg[0]
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message ="RDKSHELL_WPEFRAMEWORK_SERVICE_FILEPATH configured empty value in device config file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "webkitbrowser_get_url":
            #Get Values from IPChangeDetectionVariables file
            ip_change_app_url = IPChangeDetectionVariables.ip_change_app_url
            user_name = IPChangeDetectionVariables.tm_username
            password = IPChangeDetectionVariables.tm_password
            #Remove the extra slash from basepath at the end
            if basePath.endswith('/'):
                basePath = basePath[:-1]
            ip_address_type = getDeviceConfig(basePath,'DEVICE_IP_ADDRESS_TYPE',deviceName,deviceType)
            #Lightningapp url formation
            if ip_change_app_url and tm_url and deviceName and user_name and password and ip_address_type:
                url = ip_change_app_url+'?tmURL='+tm_url+'&deviceName='+deviceName+'&tmUserName='+user_name+'&tmPassword='+password+'&ipAddressType='+ip_address_type
                print(url)
                info["url"] = url
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "Please configure values in IPChangeDetectionVariables and device specific configuration file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_device_ssh_state":
            #Get the MAC Address from the box below command
            command = "ifconfig | awk '/eth0/ {print $5}'"
            deviceMAC = executeCommand(execInfo,command)
            deviceMAC = str(deviceMAC).split("\n")[1]
            deviceMAC = deviceMAC.strip()
            #Validate MAC Address
            if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",str(deviceMAC).lower()):
                print("\nSUCCESS : Successfully get the MAC address of the box")
                print("SUCCESS : Box is SSH able")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\nFAILURE : Failed to get the MAC address")
                print("Able to SSH the box, failed in get the MAC address of the box")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Get_territory_And_region_Config_File":
            territorylist = []
            regionlist = []
            territoryAndregion = {}
            systemlist = arg
            for item in systemlist:
                key, value = item.split(":")
                territoryAndregion[key] = value
            info["territoryAndregion"] = territoryAndregion
            if arg:
                for value in arg:
                    territory,region = value.split(":")
                    territorylist.append(territory)
                    regionlist.append(region)
                info["territory"] = territorylist
                info["region"] = regionlist
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "Please configure system territorys values in device specific configuration file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag =="rdkshell_cursor_size_value":
            cursor_dict={}
            width_list = []
            height_list = []
            #cursor width and height value
            cursor_size_list = [(38,38),(48,48),(58,58),(68,68),(78,78),(88,88)]
            for key,value in cursor_size_list:
                cursor_dict[key] = value
                width_list.append(value)
                height_list.append(value)
            info["width"] = width_list
            info["height"] = height_list
            info["cursor_dict"] = cursor_dict
            info["Test_Step_Status"] = "SUCCESS"

        elif tag == "check_environment_variable":
            #check environment variable present or not in wpeframework.service file
            command = 'grep -q '+expectedValues[0]+' '+arg[0]+' && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = output.split("\n")
            if int(output[1]) == 1:
                print(expectedValues[0]+" Environment variable is present in the wpeframework.service file")
                #check  environment variable have value or not in wpeframework.service file
                command = 'sed \'s/"//g\' '+arg[0]+' | awk -F \'=\' \'/'+expectedValues[0]+'/ {if ($3 == "") print("0") ; else print("1")}\''
                output = executeCommand(execInfo, command)
                output = output.split("\n")
                if int(output[1]) == 1:
                    message = expectedValues[0]+" Environment variable has a non-empty value"
                    info["Test_Step_Message"] = message
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    message = expectedValues[0]+" Environment variable has an empty value"
                    info["Test_Step_Message"] = message
                    info["Test_Step_Status"] = "FAILURE"
            else:
                message = expectedValues[0]+" Environment variable is not present in the wpeframework.service file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_log_file":
            #Check whether log file present or not inside USB
            command ="[ -f "+arg[0]+" ] && echo 1 || echo 0"
            output = executeCommand(execInfo, command)
            output = output.split("\n")
            if int(output[1]) == 1:
                print("\n"+arg[0]+" file present")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\n"+arg[0]+" file not present")
                info["Test_Step_Status"] = "FAILURE"
            
        elif tag == "check_log_file_format":
            #Check whether log file name comprises of Mac of the device,date and time in a tgz format or not
            command ='[[ -f "'+arg[0]+'" && "'+arg[0]+'" =~ ^/[a-zA-Z0-9_/.-]+/[0-9A-F]{12}_Logs_[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}(AM|PM)\.tgz$ ]] && echo "1" || echo "0"'
            output = executeCommand(execInfo, command)
            output = output.split("\n")
            if int(output[1]) == 1:
                print("\n"+arg[0]+" file name format is correct")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\n"+arg[0]+" file name format is incorrect")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "unmount_usb_drive":
            #Command for unmount USB drive from device
            command ="umount "+arg[0]+" && echo 1 || echo 0"
            output = executeCommand(execInfo, command)
            output = output.split("\n")
            if int(output[1]) == 1:
                print("\n"+arg[0]+" SUCCESS : Unmount USB drive successfully")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\n"+arg[0]+" FAILURE : Unmount USB drive failed")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "mount_usb_drive":
            #Command for mount USB drive
            command ="mount "+expectedValues[0]+" "+arg[0]+" && echo 1 || echo 0"
            output = executeCommand(execInfo, command)
            output = output.split("\n")
            if int(output[1]) == 1: 
                print("\n"+arg[0]+" SUCCESS : Mount USB drive successfully")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\n"+arg[0]+" FAILURE : Mount USB drive failed")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "enable_tr181_parameter":
            #Command for enable tr181 parameter
            command ="tr181 -d -s -v true "+arg[0]
            output = executeCommand(execInfo, command)
            if "set operation success" in output.lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "disable_tr181_parameter":
            #Command for disable tr181 parameter
            command ="tr181 -d -s -v false "+arg[0]
            output = executeCommand(execInfo, command)
            if "set operation success" in output.lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_tr181_parameter":
            #Command for check tr181 parameter value
            command ="tr181 "+arg[0]
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            output = output[1]
            if expectedValues:
                if str(expectedValues[0]) in output.lower():
                    info["tr181parametervalue"] = output
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["tr181parametervalue"] = output
                    info["Test_Step_Status"] = "FAILURE"
            else:
                info["tr181parametervalue"] = output
                info["Test_Step_Status"] = "SUCCESS"

        elif tag == "usbaccess_create_directory":
            command ="mkdir "+arg[1]+"/Test_Directory && echo 1 || echo 0"
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            output = int(output[1])
            if output == 1:
                print("\nTest_Directory created successfully inside USB")
                if arg[0] == "directoryonly":
                    info["dummyfirmwarefile"] = arg[1]+"/Test_Directory"
                    info["Test_Step_Status"] = "SUCCESS"
                elif arg[0] == "subdirectoryonly":
                    command ="touch "+arg[1]+"/Test_Directory/"+expectedValues[0]+"_Dummy_SubDir_Firmware_File.bin && echo 1 || echo 0"
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    output = int(output[1])
                    if output == 1:
                        print("\n"+expectedValues[0]+"_Dummy_SubDir_Firmware_File.bin file created successfully inside USB")
                        info["dummyfirmwarefile"] = expectedValues[0]+"_Dummy_SubDir_Firmware_File.bin"
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print("\nFailed to create"+expectedValues[0]+"_Dummy_SubDir_Firmware_File.bin file inside USB")
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    command ="touch "+arg[1]+"/"+expectedValues[0]+"_Dummy_Firmware_File.bin && echo 1 || echo 0"
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    output = int(output[1])
                    if output == 1:
                        print("\n"+expectedValues[0]+"_Dummy_Firmware_File.bin file created successfully inside USB")
                        info["dummyfirmwarefile"] = expectedValues[0]+"_Dummy_Firmware_File.bin"
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print("\nFailed to create"+expectedValues[0]+"_Dummy_Firmware_File.bin file inside USB")
                        info["Test_Step_Status"] = "FAILURE"
            else:
                print("\nFailed to create Test_Directory inside USB")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "usbaccess_delete_directory":
            if arg[0] == "directoryonly":
                command ="rm -rf "+arg[1]+"/Test_Directory && echo 1 || echo 0"
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                output = int(output[1])
                if output == 1:
                    print("\nTest_Directory deleted successfully inside USB")
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print("\nFailed to delete Test_Directory inside USB")
                    info["Test_Step_Status"] = "FAILURE"
            else:
                command ="rm -rf "+arg[1]+"/"+expectedValues[0]+"_Dummy_Firmware_File.bin && echo 1 || echo 0"
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                output = int(output[1])
                if output == 1:
                    print("\v"+expectedValues[0]+"_Dummy_Firmware_File.bin file deleted successfully inside USB")
                    command ="rm -rf "+arg[1]+"/Test_Directory && echo 1 || echo 0"
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    output = int(output[1])
                    if output == 1:
                        print("\nTest_Directory deleted successfully inside USB")
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print("\nFailed to delete Test_Directory inside USB")
                        info["Test_Step_Status"] = "FAILURE"
                else:
                    print("\nFailed to delete "+expectedValues[0]+"_Dummy_Firmware_File.bin file inside USB")
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_log_file_present_or_not":
            command ="tar -tzf "+arg[0]+" > /dev/null 2>&1 && echo 1 || echo 0"
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            output = int(output[1])
            if output == 1:
                print("\n"+arg[0]+" contains device logs file")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("\n"+arg[0]+" does not contain device logs file")
                info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "validate_image_version":
            if arg[0].strip().lower() == arg[1].strip().lower():
                message = "System and DeviceInfo API's are returning same firmware version"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "System and DeviceInfo API's are not returning same firmware version"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_Serial_Number":
            if arg[0].strip().lower() == arg[1].strip().lower():
                message = "System and DeviceInfo API's are returning same serial number"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "System and DeviceInfo API's are not returning same serial number"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "validate_host_EDID":
            if arg[0].strip().lower() == arg[1].strip().lower():
                message = "DisplaySettings and DeviceInfo API's are returning same EDID details"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "DisplaySettings and DeviceInfo API's are not returning same EDID details"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"
                
        elif tag == "disable_ethernet_interface":
            command = "ifconfig eth0 down"
            output = executeCommand(execInfo, command)
            message = "Successfully executed "+command+" command"
            info["Test_Step_Message"] = message
            info["Test_Step_Status"] = "SUCCESS"

        elif tag == "check_memcr_service_status":
            command="systemctl status memcr | grep running"
            result = executeCommand(execInfo, command)
            if "active (running)" in result:
                print(result)
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print(result)
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_service_status":
            command="systemctl status "+arg[0]+" | grep running"
            result = executeCommand(execInfo, command)
            if "active (running)" in result:
                print(result)
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print(result)
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_device_active_status":
            message = "Device came online after a reset, waited for 120 seconds"
            info["Test_Step_Message"] = message

        elif tag == "initialize_pre-requisite":
            message = "Starting the pre-requisite initialization"
            info["Test_Step_Message"] = message

        elif tag == "Check_And_Enable_XDial":
            if len(arg) and arg[0] == "enable_xdial":
                command = 'tr181 -d -s -v 1 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.XDial.Enable'
                output = executeCommand(execInfo, command)
                if "set operation success" in output.lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "disable_xdial":
                command = 'tr181 -d -s -v 0 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.XDial.Enable'
                output = executeCommand(execInfo, command)
                if "set operation success" in output.lower():
                    info["Test_Step_Status"] = "SUCCESS"
            elif len(arg) and arg[0] == "check_status":
                command = 'tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.XDial.Enable'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")[1]
                info["status"] = output.strip()

        elif tag == "Check_And_Enable_Dynamic_App_List":
            if len(arg) and arg[0] == "enable_dynamic_app_list":
                command = 'tr181 -d -s -v true Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.XDial.DynamicAppList'
                output = executeCommand(execInfo, command)
                if "set operation success" in output.lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "check_status":
                command = 'tr181 Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.XDial.DynamicAppList'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")[1]
                info["status"] = output.strip()

        elif tag == "check_and_enable_data_model":
            if len(arg) and arg[1] == "enable_data_model":
                command = "tr181 -d -s -v true "+arg[0]
                output = executeCommand(execInfo,command)
                if "set operation success" in output.lower():
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"

            elif len(arg) and arg[1] == "check_status":
                command = "tr181 "+arg[0]
                output = executeCommand(execInfo,command)
                output = str(output).split("\n")[1]
                info["status"] = output.strip()

        elif tag == "network_check_stb_ip_family":
            info["STB_IP_Family"] = expectedValues
            if str(expectedValues[0]) == str(deviceIP):
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "EncodeHexToBase64":
            arguments[1] = arguments[1]+"0"
            hex_code  = "".join((arguments[1],arguments[0]))
            decoded_bytes = bytes.fromhex(hex_code)
            base64_data = base64.b64encode(decoded_bytes).decode('utf-8')
            info["Hex_Data"] = hex_code
            info["message"] = base64_data.strip()

        elif tag == "Check_Version_File":
            command = '[ -f "/version.txt" ] && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print("Version.txt File Exists")
                command = '[ -s "/version.txt" ] && echo 1 ||  echo 0'
                output = executeCommand(execInfo, command)
                output = output.split("\n")
                if int(output[1]) == 1:
                    print("Version.txt File Is not Empty")
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print("Version.txt File Is Empty")
                    info["Test_Step_Status"] = "FAILURE"
            else:
                print("Version.txt File doesn't Exists")
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_include.properties_file":
            xconfurl = arg[0]
            print("include.properties file exist,checking whether xconf url is updated")
            command = 'grep -q '+xconfurl+' /etc/include.properties  && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print("File is updated with xconf url")
                info["Test_Step_Status"] = "SUCCESS"
            else:
                print("File is not updated with xconf url,Updating file with xconf url")
                command = 'sed -i \'s~^CLOUDURL=.*$~CLOUDURL='+xconfurl+'~g\' /etc/include.properties;grep -q '+xconfurl+' /etc/include.properties  && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print("Successfully updated file with xconf url")
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print("File is not updated with xconf url")
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_swupdate_file":
            xconfurl = arg[0]
            command = '[ -f "/opt/swupdate.conf" ] && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print("swupdate.conf file exist,checking whether xconf url is updated")
                command = 'grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print("File is updated with xconf url")
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    print("File is not updated with xconf url,Updating file with xconf url")
                    command = 'echo '+xconfurl+' >> /opt/swupdate.conf;grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    if int(output[1]) == 1:
                        print("Successfully updated file with xconf url")
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print("File is not updated with xconf url")
                        info["Test_Step_Status"] = "FAILURE"
            else:
                print("swupdate.conf file does not exist. Creating the file....")
                command = 'touch /opt/swupdate.conf;[ -f "/opt/swupdate.conf" ] && echo 1 || echo 0'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")
                if int(output[1]) == 1:
                    print("File created")
                    command = 'echo '+xconfurl+' >> /opt/swupdate.conf;grep -q '+xconfurl+' /opt/swupdate.conf  && echo 1 || echo 0'
                    output = executeCommand(execInfo, command)
                    output = str(output).split("\n")
                    if int(output[1]) == 1:
                        print("Successfully updated file with xconf url")
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        print("File is not updated with xconf url")
                        info["Test_Step_Status"] = "FAILURE"

                else:
                    print("File doesn't created")
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "Check_disk_partition":
            command = 'ls /dev/mmcblk0* | wc -l'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            info["partition_count"] = int(output[1])
            if len(arg) and arg[0] == "after_reboot":
                if int(info["partition_count"]) >= int(expectedValues[0]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"


        elif tag == "system_check_and_create_configuration_rule":
            configParser = configparser.ConfigParser()
            configParser.read(r'%s' % deviceConfigFile)
            xconfurl = configParser.get('device.config', 'XCONF_SERVER_URL')

            # Method to check and create model id
            if len(arg) and arg[0] == "system_check_model_id":
                ruleId = 'TDK_'+str(arg[3]).upper()+'_TEST_MODEL'
                if len(arg) and arg[1] == "existing_rule":
                    command = 'curl -sX GET '+xconfurl+arg[2]+ruleId+' -H \'Content-Type: application/json\' -H \'Accept: application/json\''
                    output = executeCommandInTM(command)
                    output = json.loads(output)
                    if output.get('message'):
                        ruleStatus = output["message"]
                        print("message from output",output["message"])
                    elif output.get('id'):
                        ruleStatus = output["id"]
                    info["existing_model_id"] = ruleStatus
                    if "not found" in ruleStatus:
                        info["Test_Step_Message"] = "NO EXISTING MODEL ID"
                    else:
                        if str(output.get("id")).lower() == str(ruleId).lower():
                            info["Test_Step_Status"] = "SUCCESS"
                        else:
                            info["Test_Step_Status"] = "FAILURE"

                elif len(arg) and arg[1] == "new_rule":
                    command = 'curl -sX POST '+xconfurl+arg[2]+' -H \'Content-Type: application/json\' -H \'Accept: application/json\' -d \'{"id":"'+ruleId+'","description":"TDK '+arg[3]+' test model"}\''
                    output = executeCommandInTM(command)
                    output = json.loads(output)
                    ruleStatus = output["id"]
                    info["new_model_id"] = output["id"]
                    if str(output.get("id")).lower() == str(ruleId).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

            # Method to check and create firmware configuration
            elif len(arg) and arg[0] == "system_check_firmware_configuration":
                #Getting firmware configurations from config file
                firmwareFilename = configParser.get('device.config', 'FIRMWARE_FILENAME')
                firmwareVersion = configParser.get('device.config', 'FIRMWARE_VERSION')
                firmwareDownloadProtocol = configParser.get('device.config', 'FIRMWARE_DOWNLOAD_PROTOCOL')
                if len(expectedValues) and expectedValues[0] == "update_existing_rule":
                    firmwareFilename = configParser.get('device.config', 'EXISTING_FIRMWARE_FILENAME')
                    firmwareVersion = expectedValues[1]

                ruleId = 'TDK_'+str(arg[3]).upper()+'_TEST_FIRMWARE_CONFIGURATION'
                modelId = 'TDK_'+str(arg[3]).upper()+'_TEST_MODEL'
                if len(arg) and arg[1] == "existing_rule":
                    command = 'curl -sX GET '+xconfurl+arg[2]+modelId+'?applicationType=stb -H \'Content-Type: application/json\' -H \'Accept: application/json\''
                    output = executeCommandInTM(command)
                    content = json.loads(output)
                    info["existing_firmware_configuration"] = content
                    if len(content) == 0:
                        info["Test_Step_Message"] = "NO EXISTING FIRMWARE CONFIGURATION"
                    else:
                        firmwareConfigs = json.loads(output)
                        info["Test_Step_Status"] = "FAILURE"
                        for output in firmwareConfigs:
                            if str(output.get("description")).lower() == str(ruleId).lower():
                                info["Test_Step_Status"] = "SUCCESS"
                                if str(output.get("firmwareFilename")).lower() != firmwareFilename.lower():
                                    firmwareConfigId = output.get("id")
                                    command = 'curl -sX PUT '+xconfurl+'updates/firmwares?applicationType=stb -H \'Content-Type: application/json\' -H \'Accept: application/json\' -d \'{"id":"'+firmwareConfigId+'" ,"updated": 144757585,"supportedModelIds": ["TDK_'+str(arg[3]).upper()+'_TEST_MODEL"],"firmwareDownloadProtocol": "'+firmwareDownloadProtocol+'","firmwareFilename": "'+firmwareFilename+'","firmwareVersion": "'+firmwareVersion+'","description":"'+ruleId+'","rebootImmediately": true}\''
                                    output = executeCommandInTM(command)
                                    info["new_firmware_configuration"] = output
                                    output = json.loads(output)
                                    if str(output.get("description")).lower() == str(ruleId).lower():
                                        info["Test_Step_Status"] = "SUCCESS"
                                    else:
                                        info["Test_Step_Status"] = "FAILURE"
                                    break;

                elif len(arg) and arg[1] == "new_rule":
                    command = 'curl -sX POST '+xconfurl+arg[2]+'?applicationType=stb -H \'Content-Type: application/json\' -H \'Accept: application/json\' -d \'{"description":"'+ruleId+'","supportedModelIds": [ "TDK_'+str(arg[3]).upper()+'_TEST_MODEL" ], "firmwareDownloadProtocol": "'+firmwareDownloadProtocol+'", "firmwareFilename": "'+firmwareFilename+'", "firmwareVersion": "'+firmwareVersion+'", "rebootImmediately": true}\''
                    output = executeCommandInTM(command)
                    output = json.loads(output)
                    info["new_firmware_configuration"] = output
                    if str(output.get("description")).lower() == str(ruleId).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

            # Method to check and create firmware rule
            elif len(arg) and arg[0] == "system_check_firmware_rule":
                print("arg",arg)
                ruleId = 'TDK_'+str(arg[2]).upper()+'_TEST_FIRMWARE_RULE'
                modelId = 'TDK_'+str(arg[2]).upper()+'_TEST_MODEL'
                firmwareconfigId = arg[4]
                deviceMAC = arg[3]
                if len(arg) and arg[1] == "existing_rule":
                    command = 'curl -sX --location --request GET \''+xconfurl+'firmwarerule/filtered?name='+ruleId+'&applicationType=stb&templateId=MAC_RULE\''
                    output = executeCommandInTM(command)
                    content = json.loads(output)
                    info["existing_firmware_rule"] = content
                    if content is None:
                        info["Test_Step_Message"] = "NO EXISTING FIRMWARE RULE"
                    else:
                        firmwareRule = content
                        info["Test_Step_Status"] = "FAILURE"
                        for output in firmwareRule:
                            firmwareruleconfigId = output['applicableAction']['configId']
                            firmwarerulename = output['name']
                            if str(firmwarerulename).lower() == str(ruleId).lower() and str(firmwareruleconfigId).lower() == str(firmwareconfigId).lower():
                                info["Test_Step_Status"] = "SUCCESS"
                                firmwarerulemacaddress = output["rule"]["condition"]["fixedArg"]["bean"]["value"]["java.lang.String"]
                                if str(firmwarerulemacaddress).lower() != str(deviceMAC).lower():
                                    firmwareruleId = output['id']
                                    command = 'curl -sX POST '+xconfurl+'firmwarerule/importAll?applicationType=stb -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id": "'+firmwareruleId+'","name":"'+firmwarerulename+'","rule":{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}}},"applicableAction":{"type":".RuleAction","actionType":"RULE","configId":"'+firmwareconfigId+'","configEntries":[],"active":true,"useAccountPercentage":false,"firmwareCheckRequired":false,"rebootImmediately":true},"type":"MAC_RULE","active":true,"applicationType":"stb"}]\''
                                    output = executeCommandInTM(command)
                                    info["new_firmware_rule_status"] = output
                                    output = json.loads(output)
                                    if str(output.get("IMPORTED")[0]).lower() == str(ruleId).lower():
                                        info["Test_Step_Status"] = "SUCCESS"
                                    else:
                                        info["Test_Step_Status"] = "FAILURE"
                elif len(arg) and arg[1] == "new_rule":
                    command = 'curl -sX POST '+xconfurl+'firmwarerule/importAll?applicationType=stb -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"name":"'+ruleId+'","rule":{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}}},"applicableAction":{"type":".RuleAction","actionType":"RULE","configId":"'+firmwareconfigId+'","configEntries":[],"active":true,"useAccountPercentage":false,"firmwareCheckRequired":false,"rebootImmediately":true},"type":"MAC_RULE","active":true,"applicationType":"stb"}]\''
                    output = executeCommandInTM(command)
                    info["new_firmware_rule_status"] = output
                    output = json.loads(output)
                    if str(output.get("IMPORTED")[0]).lower() == str(ruleId).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

            # Method to check and create firmware local server rule
            elif len(arg) and arg[0] == "system_check_firmware_local_server_rule":
                firmwareLocation = configParser.get('device.config','FIRMWARE_LOCATION')
                firmwareDownloadProtocol = configParser.get('device.config', 'FIRMWARE_DOWNLOAD_PROTOCOL')
                ruleId = 'TDK_'+str(arg[2]).upper()+'_TEST_FIRMWARE_LOCAL_SERVER_RULE'
                modelId = 'TDK_'+str(arg[2]).upper()+'_TEST_MODEL'
                firmwareConfigId = arg[4]
                deviceMAC = arg[3]
                if len(arg) and arg[1] == "existing_rule":
                    command = 'curl -sX --location --request GET \''+xconfurl+'firmwarerule/filtered?name='+ruleId+'&applicationType=stb&templateId=DOWNLOAD_LOCATION_FILTER\''
                    output = executeCommandInTM(command)
                    firmwareRule = json.loads(output)
                    info["existing_firmware_local_server_rule"] = firmwareRule
                    if firmwareRule is None:
                        info["Test_Step_Message"] = "NO EXISTING FIRMWARE LOCAL SERVER RULE"
                    else:
                        info["Test_Step_Status"] = "FAILURE"
                        for output in firmwareRule:
                            firmwareRuleName = output['name']
                            if str(firmwareRuleName).lower() == str(ruleId).lower():
                                info["Test_Step_Status"] = "SUCCESS"
                                firmwareRuleMacAddress = output["rule"]["compoundParts"][0]["condition"]["fixedArg"]["bean"]["value"]["java.lang.String"]
                                firmwareRuleLocation = output['applicableAction']['properties']["firmwareLocation"]
                                firmwareRuleDownloadLocation = output['applicableAction']['properties']["firmwareDownloadProtocol"]
                                if str(firmwareRuleMacAddress).lower() != str(deviceMAC).lower() or str(firmwareRuleLocation).lower() != str(firmwareLocation).lower() or str(firmwareRuleDownloadLocation).lower() != str(firmwareDownloadProtocol).lower():
                                    firmwareRuleId = output['id']
                                    command = 'curl -sX POST '+xconfurl+'firmwarerule/importAll?applicationType=stb -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"id":"'+firmwareRuleId+'","name":"'+firmwareRuleName+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"AA:BB:CC:DD:EE:FF"}}}},"compoundParts":[]}]},"applicableAction":{"type":".DefinePropertiesAction","actionType":"DEFINE_PROPERTIES","configId":"'+firmwareConfigId+'","properties":{"ipv6FirmwareLocation":"","firmwareLocation":"'+firmwareLocation+'","firmwareDownloadProtocol":"'+firmwareDownloadProtocol+'"},"byPassFilters":[],"activationFirmwareVersions":{}},"type":"DOWNLOAD_LOCATION_FILTER","active":true,"applicationType":"stb"}]\''
                                    output = executeCommandInTM(command)
                                    info["new_firmware_local_server_rule_status"] = output
                                    output = json.loads(output)
                                    if str(output.get("IMPORTED")[0]).lower() == str(ruleId).lower():
                                        info["Test_Step_Status"] = "SUCCESS"
                                    else:
                                        info["Test_Step_Status"] = "FAILURE"

                elif len(arg) and arg[1] == "new_rule":
                    command = 'curl -sX POST '+xconfurl+'firmwarerule/importAll?applicationType=stb -H "Content-Type: application/json" -H "Accept: application/json" -d \'[{"name":"'+ruleId+'","rule":{"negated":false,"compoundParts":[{"negated":false,"condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"'+deviceMAC+'"}}}},"compoundParts":[]},{"negated":false,"relation":"OR","condition":{"freeArg":{"type":"STRING","name":"eStbMac"},"operation":"IS","fixedArg":{"bean":{"value":{"java.lang.String":"AA:BB:CC:DD:EE:FF"}}}},"compoundParts":[]}]},"applicableAction":{"type":".DefinePropertiesAction","actionType":"DEFINE_PROPERTIES","configId":"'+firmwareConfigId+'","properties":{"ipv6FirmwareLocation":"","firmwareLocation":"'+firmwareLocation+'","firmwareDownloadProtocol":"'+firmwareDownloadProtocol+'"},"byPassFilters":[],"activationFirmwareVersions":{}},"type":"DOWNLOAD_LOCATION_FILTER","active":true,"applicationType":"stb"}]\''
                    output = executeCommandInTM(command)
                    info["new_firmware_rule_status"] = output
                    output = json.loads(output)
                    if str(output.get("IMPORTED")[0]).lower() == str(ruleId).lower():
                        info["Test_Step_Status"] = "SUCCESS"
                    else:
                        info["Test_Step_Status"] = "FAILURE"

        elif tag == "Create_File":
            command = "mkdir "+arguments[0]+"/Controller;[ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            result = 1
            if int(status[1]) == result:
                info["RESULT"] = "Controller directory created"
                command = "touch "+arguments[0]+"/Controller/TDK_TEST_FILE.txt;[ -f "+arguments[0]+"/Controller/TDK_TEST_FILE.txt ] && echo 1 || echo 0"
                status = executeCommand(execInfo, command)
                status = str(status).split("\n")
                result = 1
                if int(status[1]) == result:
                    info["RESULT"] = "File created"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["RESULT"] = "File not created"
                    info["Test_Step_Status"] = "FAILURE"

            else:
                info["RESULT"] = "Controller directory not created"
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Check_WPE_Process":
            processesRunning = []
            processesNotRunning = []
            command = "ps -ef | awk '{print $8}' ; ps -eo comm"
            output = executeCommand(execInfo, command)
            for value in expectedValues:
                if ":" in str(value):
                    value = value.split(":")[1]
                if value.lower() in str(output).lower():
                    status = True
                    processesRunning.append(value)
                else:
                    status = False
                    processesNotRunning.append(value)
            if status:
                info["Running_Processes"] = processesRunning
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Running_Processes"] = processesRunning
                info["processes_Not_Running"] = processesNotRunning
                info["Test_Step_Status"] = "FAILURE"
        elif tag == "check_fps_value":
            expectedFPS = (int(expectedValues[0])-int(expectedValues[1]))
            info["AVERAGE_FPS"] = arguments[0]
            if int(arguments[0]) >= expectedFPS:
                message = "FPS should be >= %d & it is as expected" %(expectedFPS)
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "FPS should be >= %d & it is not as expected" %(expectedFPS)
                info["Test_Step_Status"] = "FAILURE"
            info["Test_Step_Message"] = message

        elif tag == "Check_If_File_Exists":
            command = "[ -f "+arguments[0]+"/Controller/TDK_TEST_FILE.txt ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            result = 0
            if int(status[1]) == result:
                info["RESULT"] = "File does not exist"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["RESULT"] = "File exist"
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "Delete_Test_File":
            command = "[ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
            status = executeCommand(execInfo, command)
            status = str(status).split("\n")
            if int(status[1]) == 0:
                info["RESULT"] = "File does not exist"
                info["Test_Step_Status"] = "SUCCESS"
            else:
                command = "rm -rf "+arguments[0]+"/Controller ; [ -d "+arguments[0]+"/Controller ] && echo 1 || echo 0"
                status = executeCommand(execInfo, command)
                status = str(status).split("\n")
                if int(status[1]) == 0:
                    info["Message"] = "Test file deleted"
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Message"] = "Test file not deleted"
                    info["Test_Step_Status"] = "FAILURE"

        elif tag == "Framerate_Get_Width_And_Height":
            DisplayFrameRate_values = []
            for values in range(1,len(arg)):
                mapping_details = arg[values].split(":")
                width = mapping_details[1].split('|')[0].strip('[]')
                height = mapping_details[1].split('|')[1].strip('[]')
                DisplayFrameRate = width+'x'+height+'x60'
                DisplayFrameRate_values.append(DisplayFrameRate)
            info["DisplayFrameRate"] = DisplayFrameRate_values

        elif tag == "Get_Default_Values":
            profile = arg[len(arg)-1]
            arg[0] = profile+'.'+arg[0]
            command = 'grep -F '+arg[0]+' /etc/hostDataDefault'
            output = executeCommand(execInfo, command)
            output = str(output).split()
            output = output[1]
            info["defaultValue"] = int(output,16)
            if len(arg) > 3 and arg[2] == "get_audio_profiles_default_modes":
                arg[1] = profile+'.'+arg[1]
                command =  'grep -F '+arg[1]+' /etc/hostDataDefault'
                output = executeCommand(execInfo, command)
                output = str(output).split()
                output = output[1]
                info["defaultMode"] = int(output)

        elif tag == "TV_ControlSettings_Get_Default_Values":
            command = 'grep -F '+arg[0]+' ' +arg[1]+''
            output = executeCommand(execInfo, command)
            output = str(output).split("=")[1]
            info["defaultValue"] = output.strip()

        elif tag == "TV_ControlSettings_Get_Random_Number":
            if len(arg) and arg[0] == "fixed_length_list":
                arg.pop(0)
                randomnumber = random.choice(arg)
            else:
                randomnumber = random.randint(int(arg[0]),int(arg[1]))
            info["randomnumber"] = randomnumber

        elif tag == "RDKShell_Get_Width_And_Height":
            mapping_details = arg[len(arg)//2].split(":")
            info["width"] = mapping_details[1].split('|')[0].strip('[]')
            info["height"] = mapping_details[1].split('|')[1].strip('[]')

        elif tag == "Get_Image_Name":
            command = 'find / -name *.png'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            for lines in output:
                if command not in lines and "no such file or directory" not in lines.lower():
                    imagePath = lines
                    break;
            info["imagepath"] = imagePath

        elif tag == "get_process_id":
            command = 'ps -ef | grep DobbyInit | grep '+arg[0]+' | awk \'NR==1 {print $2}\''
            output = executeCommand(execInfo, command)
            info["processID"] = output.split("\n")[1].strip()

        elif tag == "securityagent_get_security_token":
            command = "WPEFrameworkSecurityUtility |  cut -d '\"' -f 4"
            output = executeCommand(execInfo, command)
            print(output)
            output = str(output).split("\n")[1]
            output =  output.strip()
            if len(arg) and arg[0] == "get_modified_token":
                letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
                invalidToken = ''.join(random.choice(letters) for i in range(10))
                info["securityToken"] = output + invalidToken
            else:
                info["securityToken"] = output

        elif tag == "securityagent_get_invalid_security_token":
            letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
            info["securityToken"] = ''.join(random.choice(letters) for i in range(90))

        elif tag == "check_required_logs":
            command = 'cat /opt/logs/wpeframework.log | grep -inr \"'+expectedValues[0]+'\"'
            output = executeCommand(execInfo, command)
            output = output.split('\n',1)[-1]
            if str(expectedValues[0]).lower() in str(output).lower():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "check_container_status":
            container_status = "FAILURE"
            command = 'DobbyTool list'
            print("COMMAND : %s" %(command))
            output = executeCommand(execInfo, command)
            print(output)
            result = output.splitlines()
            if len(arg) and arg[0] == "check_empty_container":
                container_status = "SUCCESS"
                for line in result:
                    if str(expectedValues[0]) in line.lower():
                        container_status = "FAILURE"
                        info["Test_Step_Message"] = expectedValues[0]+' container is running'
                        info["Test_Step_Status"] =  "FAILURE"
                        break;
                print("container_status",container_status)
                if "SUCCESS" in container_status:
                    info["Test_Step_Message"] = expectedValues[0]+' container is not running'
                    info["Test_Step_Status"] =  "SUCCESS"
            else:
                container_status = "FAILURE"
                for line in result:
                    if str(expectedValues[0]) in line.lower() and str(expectedValues[1]).lower() in line.lower():
                        container_status = "SUCCESS"
                        info["Test_Step_Message"] = expectedValues[1]+' container is '+expectedValues[0]
                        break;
                print("container_status",container_status)
                if "FAILURE" in container_status:
                    info["Test_Step_Message"] = expectedValues[1]+' container is not '+expectedValues[0]
                    info["Test_Step_Status"] =  "FAILURE"

        elif tag == "Check_Environment_Variable_In_Service_File":
            command = 'grep -q '+str(expectedValues[0])+' /lib/systemd/system/wpeframework.service && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                message = "\"RDKSHELL_SPLASH_IMAGE_JPEG\" Environment variable is present in the  wpeframework.service file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "\"RDKSHELL_SPLASH_IMAGE_JPEG\" Environment variable is not present in the wpeframework.service file but \"Splash Screen\" feature configured as supported feature in config file"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "get_dut_date":
            try:
                command = 'date'
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")[1].strip()
                if output:
                    dut_info = datetime.datetime.strptime(output, "%a %b %d %H:%M:%S %Z %Y")
                    info["dut_day"] = dut_info.day
                    info["dut_month"] = dut_info.month
                    info["dut_year"] = dut_info.year
                else:
                    print("Empty output from command execution")
                    info["Test_Step_Status"] = "FAILURE"
            except Exception as e:
                info["Test_Step_Status"] = "FAILURE"
                print(e)

        elif tag == "validate_dates":
            data = arg
            list1 = [int(item.strip("[] ")) for item in data[:3]]
            list2 = [int(item.strip("[] ")) for item in data[3:]]
            if list1 == list2:
                message = "The dates from systeminfo API and DUT are same"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "SUCCESS"
            else:
                message = "The dates from systeminfo API and DUT are different"
                info["Test_Step_Message"] = message
                info["Test_Step_Status"] = "FAILURE"
        
        elif tag == "get_plugin_status_value":
            if arg[0] == "activated":
                info["plugin_status_value"] = "no"
            else:
                info["plugin_status_value"] = "yes"

        elif tag == "check_webkit_presence":
            try:
                command = "grep -iq '"+'"callsign":\s*"WebKitBrowser"'+"' "+arg[0]+" && echo 1 || echo 0"
                output = executeCommand(execInfo, command)
                output = str(output).split("\n")[1].strip()
                if int(output) == 1:
                    info["webkitbrowser_details_presence"] = "yes"
                elif int(output) == 0:
                    info["webkitbrowser_details_presence"] = "no"
                else:
                    print(output)
                    info["Test_Step_Status"] = "FAILURE"
            except Exception as e:
                info["Test_Step_Status"] = "FAILURE"
                print(e)

        elif tag == "check_time_sync":
            command = 'date'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")[1].strip()
            current_utc_time_DUT = datetime.datetime.strptime(output, "%a %b %d %H:%M:%S %Z %Y")
            current_utc_time_DUT = current_utc_time_DUT.replace(second=0)
            current_utc_time_DUT = current_utc_time_DUT.strftime("%Y-%m-%d %H:%M")
            info["current_utc_time_DUT"] = current_utc_time_DUT
            current_utc_time = datetime.datetime.utcnow()
            current_utc_time = current_utc_time.replace(second=0)
            current_utc_time = current_utc_time.strftime("%Y-%m-%d %H:%M")
            info["current_utc_time"] = current_utc_time
            if current_utc_time_DUT.strip() == current_utc_time.strip():
                info["Test_Step_Status"] = "SUCCESS"
            else:
                info["Test_Step_Status"] = "FAILURE"

        elif tag == "system_get_device_details_from_file":
            command = 'grep '+str(arg[0])+' '+str(arg[1])+' | cut -d\'=\' -f2- | xargs'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")[1]
            info["details"] = output.replace('"','').strip()
            info["Test_Step_Status"] =  "SUCCESS"

        elif tag == "system_check_swupdate_file_status":
            command = '[ -f "/opt/swupdate.conf" ] && echo 1 || echo 0'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if int(output[1]) == 1:
                print("SWUpdate file exist")
                info["FIRMWARE_UPGRADE_STATUS"] = "true"
            else:
                print("SWUpdate file not exist")
                info["FIRMWARE_UPGRADE_STATUS"] = "false"

        elif tag == "system_check_public_ip_address":
            command = 'curl -s ifconfig.me'
            output = executeCommand(execInfo, command)
            output = str(output).split("\n")
            if output[1]:
                info["PUBLIC_IP"] = str(output[1])
                info["Test_Step_Status"] =  "SUCCESS"
            else:
                info["Test_Step_Status"] =  "FAILURE"

        elif tag == "executeRebootCmd":
            command = "reboot"
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"
        elif tag == "getImageVersion":
            command = "cat /version.txt | grep imagename | cut -d ':' -f2"
            details = executeCommand(execInfo, command)
            info["image"] = str(details).split("\n")[1]
            if len(arg) and arg[0] == "get":
                if str(info["image"]):
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
            elif len(arg) and arg[0] == "get_image_and_yocto_version":
                command = "grep -i 'YOCTO_VERSION' /version.txt | cut -d '=' -f2"
                details = executeCommand(execInfo, command)
                info["yocto"] = str(details).split("\n")[1]
            else:
                if expectedValues[0] in info["image"] :
                    info["Test_Step_Status"] = "SUCCESS"
                else:
                    info["Test_Step_Status"] = "FAILURE"
        elif tag == "toggleMemoryBank":
            command = '/bin/sh '+arg[0]
            info["deatils"] = executeCommand(execInfo, command)
            info["Test_Step_Status"] =  "SUCCESS"

        else:
            print("\nError Occurred: [%s] No function call available for %s" %(inspect.stack()[0][3],methodTag))
            info["Test_Step_Status"] = "FAILURE"

    except Exception as e:
        print("\nException Occurred: [%s] %s" %(inspect.stack()[0][3],e))
        info["Test_Step_Status"] = "FAILURE"
    return info


#-----------------------------------------------------------------------------------------------
#                    ***  USER CAN ADD SUPPORTING FUNCTIONS BELOW ***
#-----------------------------------------------------------------------------------------------
def checkAndGetAllResultInfo(result,success="null"):
    info = {}
    info = result.copy()
    status = checkNonEmptyResultData(list(info.values()))
    success = str(success).lower() == "true" if success != "null" else True
    if success and status == "TRUE":
        info["Test_Step_Status"] = "SUCCESS"
    else:
        info["Test_Step_Status"] = "FAILURE"

    return info


def checkNonEmptyResultData(resultData):
    status = "TRUE"
    if resultData is None:
        status = "FALSE"
    elif type(resultData) is list:
        for data in resultData:
            if str(data).strip() == "":
                status = "FALSE"
                break;
        if len(resultData) == 0:
            status = "FALSE"
    elif str(resultData).strip() == "":
        status = "FALSE"

    return status

def compareURLs(actualURL,expectedURL):
    if expectedURL in actualURL:
        status = "TRUE"
    else:
        url_data = []
        url_data_split = [ data for data in expectedURL.split("/") if data.strip() ]
        for data in url_data_split:
            if "?" in data:
                url_data.extend(data.split("?"))
            else:
                url_data.append(data)
        status = "TRUE"
        for data in url_data:
            if data not in actualURL:
                status = "FALSE"

    return status

def DecodeBase64ToHex(base64):
    if len(base64) % 4 != 0:
        while len(base64) % 4 != 0:
            base64 = base64 + "="
    decoded = b64decode(base64)
    hex_code = codecs.encode(decoded, 'hex').decode("utf-8")
    return hex_code

def getcountofelements(dictionary):
    global timeZones
    for key,value in list(dictionary.items()):
        if isinstance(value, dict):
            for continent,country in list(value.items()):
                zoneinfo = key+"/"+continent
                timeZones.append(str(zoneinfo))
            getcountofelements(value)
    return timeZones



# Other External Functions can be added below

def executeBluetoothCtl(deviceConfigFile,commands):
    try :
        #Get Bluetooth configuration file
        configParser = configparser.ConfigParser()
        configParser.read(r'%s' % deviceConfigFile)
        ip = configParser.get('device.config', 'BT_EMU_IP')
        username = configParser.get('device.config', 'BT_EMU_USER_NAME')
        password = configParser.get('device.config', 'BT_EMU_PWD')
        deviceName = configParser.get('device.config','BT_EMU_DEVICE_NAME')
        #Executing the commands in device
        print('Number of commands:', len(commands))
        print('Commands List:', commands)
        print("Connecting to client device")
        global session
        session = pxssh.pxssh(options={
                            "StrictHostKeyChecking": "no",
                            "UserKnownHostsFile": "/dev/null"})
        session.login(ip,username,password,sync_multiplier=5)
        print("Executing the bluetoothctl commands")
        for parameters in range(0,len(commands)):
            session.sendline(commands[parameters])
        session.prompt()
        status=session.before
        status=status.strip()
        #session.logout()
        status = "SUCCESS"
        #session.close()
        print("Successfully Executed bluetoothctl commands in client device")
    except Exception as e:
        print(e);
        status = "FAILURE"

    return status

def executeCommand(execInfo, command, device="test-device"):
    deviceConfigFile = execInfo[1]
    deviceIP         = execInfo[2]
    deviceMAC        = execInfo[3]
    execMethod       = execInfo[4]

    configParser = configparser.ConfigParser()
    configParser.read(r'%s' % deviceConfigFile)
    sshMethod = configParser.get('device.config', 'SSH_METHOD')
    if device == "test-device":
        username = configParser.get('device.config', 'SSH_USERNAME')
        password = configParser.get('device.config', 'SSH_PASSWORD')
    elif device == "bt-emu":
        deviceIP = configParser.get('device.config', 'BT_EMU_IP')
        username = configParser.get('device.config', 'BT_EMU_USER_NAME')
        password = configParser.get('device.config', 'BT_EMU_PWD')
        deviceName = configParser.get('device.config','BT_EMU_DEVICE_NAME')
    if password == "None":
        password = ''

    output = ""
    if sshMethod.upper() == "DIRECTSSH":
        try:
            session = pxssh.pxssh(options={
                                "StrictHostKeyChecking": "no",
                                "UserKnownHostsFile": "/dev/null"})
            print("\nCreating ssh session")
            session.login(deviceIP,username,password,sync_multiplier=5)
            sleep(2)
            print("Executing command: ",command)
            session.sendline(command)
            if command == "reboot":
                sleep(2);
                output = "reboot"
            elif command == "ifconfig eth0 down":
                sleep(2);
                output = "eth0 down"
            else:
                session.prompt()
                output = str(session.before, 'utf-8')
                print("Closing session")
                session.logout()
        except pxssh.ExceptionPxssh as e:
            print("Login to device failed")
            print(e)
    else:
        try:
            ssh_util = configParser.get('device.config', 'SSH_UTIL')
            lib = importlib.import_module("SSHUtility")
            method = "ssh_and_execute_" + sshMethod
            method_to_call = getattr(lib, method)
            output = method_to_call(command,deviceMAC,ssh_util)
            print(output)
        except Exception as e:
            output = "EXCEPTION"
            print("Exception Occurred: ",e)

    return output


def executeCommandInTM(command):
    output = ""
    try:
        if "" == command:
            status = "FAILURE"
            print("[ERROR]: Command to be executed cannot be empty")
        else:
            print("Going to execute %s..." %(command))
            output = subprocess.check_output (command, shell=True)
    except Exception as e:
        print(e)
        status = "FAILURE"
        print("Unable to execute %s successfully" %(command))
    return output

#Get value from device config file
def getDeviceConfig (basePath, configKey,deviceName,deviceType):
    deviceConfigFile=""
    configValue = ""
    output = ""
    configPath = basePath + "/"   + "fileStore/tdkvRDKServiceConfig"
    deviceNameConfigFile = configPath + "/" + deviceName + ".config"
    deviceTypeConfigFile = configPath + "/" + deviceType + ".config"
    # Check whether device / platform config files required for
    # executing the test are present
    if os.path.exists (deviceNameConfigFile) == True:
        deviceConfigFile = deviceNameConfigFile
    elif os.path.exists (deviceTypeConfigFile) == True:
        deviceConfigFile = deviceTypeConfigFile
    else:
        output = "FAILURE : No Device config file found : " + deviceNameConfigFile + " or " + deviceTypeConfigFile
        print(output)
    try:
        if (len (deviceConfigFile) != 0) and (len (configKey) != 0):
            config = configparser.ConfigParser ()
            config.read (deviceConfigFile)
            deviceConfig = config.sections ()[0]
            configValue =  config.get (deviceConfig, configKey)
            output = configValue
        else:
            output = "FAILURE : DeviceConfig file or key cannot be empty"
            print(output)
    except Exception as e:
        output = "FAILURE : Exception Occurred: [" + inspect.stack()[0][3] + "] " + e.message
        print(output)
    return output
