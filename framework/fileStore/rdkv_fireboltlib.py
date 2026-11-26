##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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

import requests
import FireboltTestVariables

deviceIP=""
devicePort=""
deviceName=""
deviceType=""
realpath=""
securityEnabled=False
deviceToken=""
logged_config_files = set()

def get_step_description(method, params):
    return "Install, run and collect Firebolt certification reports"

#---------------------------------------------------------------
#INITIALIZE THE MODULE
#---------------------------------------------------------------
def init_module(libobj,port,deviceInfo):
    global deviceIP
    global devicePort
    global deviceName
    global deviceType
    global libObj
    global realpath
    global deviceMac
    deviceIP = libobj.ip;
    devicePort = port
    deviceName = deviceInfo["devicename"]
    deviceType = deviceInfo["boxtype"]
    libObj = libobj
    try:
        deviceMac = deviceInfo["mac"]
    except Exception as e:
        print("\nException Occurred while getting MAC \n")
        print(e)

def firebolt_execute():
    reporting_id = "tdk_%s" % (libObj.execID)
    report_server_url=FireboltTestVariables.report_server_url
    response = requests.post(report_server_url + "automation/runs", json={
            "deviceIp": libObj.ip, "reportingId": reporting_id,
            "timeout": 4500
        }, timeout=20)
    response.raise_for_status()
    print("[INFO] Execution reportingId: " + reporting_id)