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

import tdklib
import re
import json
from rdkv_performancelib import *

obj = tdklib.TDKScriptingLibrary("rdkv_telemetry","1",standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'RDKV_Telemetry_AppLaunch_ErrorValidation')
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % result)

obj.setLoadModuleStatus(result.upper())
expectedResult = "SUCCESS"

event_name = "RDKAMAppLaunchError_split"
component_name = "AppManager"
profile_name = "RDKV-AppLaunchErrorProfile"
description = "Report to validate App Launch Error"

app_bundle_name = PerformanceTestVariables.google_bundle
app_name = app_bundle_name.split("+")[0]
app_download_url = PerformanceTestVariables.app_download_url

pre_requisite_set = False
profile_set = False

if "SUCCESS" in result.upper():

    tdkTestObj = obj.createTestStep('telemetry_deviceconfig_value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","Telemetry_Collector_URL")
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    details = details.replace("(","").replace(")","")
    details = details.split(",")

    Telemetry_Collector_URL = details[1]

if "SUCCESS" in result.upper():

    tdkTestObj = obj.createTestStep('setPreRequisites')
    tdkTestObj.addParameter("Telemetry_Collector_URL",Telemetry_Collector_URL)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()

    if "SUCCESS" in details:
        pre_requisite_set = True

if pre_requisite_set:

    print("\n[TEST STEP 1] : Create Telemetry Event Profile")

    tdkTestObj = obj.createTestStep('form_rbuscli_event_command')
    tdkTestObj.addParameter("event_name",event_name)
    tdkTestObj.addParameter("Telemetry_Collector_URL",Telemetry_Collector_URL)
    tdkTestObj.addParameter("profile_name",profile_name)
    tdkTestObj.addParameter("description",description)
    tdkTestObj.addParameter("component_name",component_name)
    tdkTestObj.executeTestCase(expectedResult)
    command = tdkTestObj.getResultDetails()
    command = re.sub(r"\n", "", command)
    print(command)
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    print(details)

    if "setvalues succeeded" in details:
        profile_set = True
        print("SUCCESS : Profile configured")

if profile_set:
    print("\n[TEST STEP 2] : Verify Profile")
    command = \
        "rbuscli get Device.X_RDKCENTRAL-COM_T2.ReportProfiles"
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    print(details)

    if profile_name in details:
        print("SUCCESS : Profile found")
    else:
        print("FAILURE : Profile not found")

if profile_set:
    print("\nCapturing current WPEFramework log position")
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
    command = "wc -l /opt/logs/wpeframework.log | awk '{print $1}'"
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult)
    start_line = tdkTestObj.getResultDetails().strip()
    print("Current Log Line :", start_line)

    print("\n[TEST STEP 3] : Launch Application")
    status = rdkservice_install_launch_app(obj,app_bundle_name,app_name,app_download_url,launch=True)

    if status == "SUCCESS":
        print("SUCCESS : Application launched")
        print("\n[TEST STEP 3A] : Verify Launch Marker Generation")
        command = "grep OverallLaunchError_split /opt/logs/wpeframework.log | tail -20"
        tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        marker_details = tdkTestObj.getResultDetails()

        print(marker_details)
        if "OverallLaunchError_split" in marker_details:
            print("SUCCESS : Launch marker generated")
        else:
            print("FAILURE : Launch marker not found")
    else:
        print("FAILURE : Application launch failed")

if profile_set:

    print("\nWaiting for telemetry collection")
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')

    check_cmd = \
        'sleep 60 ; journalctl -x -u telemetry2_0.service --since "1 minute ago"'

    tdkTestObj.addParameter("command",check_cmd)
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()
    print(details)
    print("\n[TEST STEP 4] : Verify cJSON Report")
    cJSON_line = ""

    for line in details.splitlines():
        if "cJSON Report" in line:
            cJSON_line = line
            break
    if cJSON_line:
        print(cJSON_line)
        print("SUCCESS : cJSON Report found")

        print("\n[TEST STEP 5] : Parse Launch Telemetry Report")
        launch_data = ""
        if cJSON_line:
            try:
                match = re.search(r'(\{.*\})', cJSON_line)
                if match:
    
                    json_str = match.group(1)
                    data = json.loads(json_str)
                    print("\nParsed JSON Report :")
                    print(data)
                    report = data.get("Report", [])
                    if len(report) == 0:
                        print("FAILURE : Telemetry report is empty")
                        print("\n[TEST STEP RESULT] : FAILURE\n")
                        tdkTestObj.setResultStatus("FAILURE")
                    else:
                        launch_data = report[0]
                        print("\nLaunch Telemetry Data :")
                        print(launch_data)
                        print("SUCCESS : Launch telemetry data found")
                        print("\n[TEST STEP RESULT] : SUCCESS\n")
                        tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("FAILURE : Unable to extract JSON from cJSON report")
                    print("\n[TEST STEP RESULT] : FAILURE\n")
                    tdkTestObj.setResultStatus("FAILURE")

            except Exception as e:
                print("FAILURE : Unable to obtain launch telemetry data")
                print(e)
                print("\n[TEST STEP RESULT] : FAILURE\n")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE : No cJSON report found")
            print("\n[TEST STEP RESULT] : FAILURE\n")            
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE : cJSON Report not found")

obj.unloadModule("rdkv_telemetry")
