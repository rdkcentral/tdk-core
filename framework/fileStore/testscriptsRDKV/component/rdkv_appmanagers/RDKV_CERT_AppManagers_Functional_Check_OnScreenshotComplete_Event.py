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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from tdkvScreenShotUtility import *
import time
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_appmanagers","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AppManagers_Functional_Check_OnScreenshotComplete_Event')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():
    # Step 1 : Get the device configuration values
    print("\n")
    configkeylist = ["SCREEN_CAPTURE_MECHANISM"]
    tdkTestObj = obj.createTestStep('appmanagers_getdeviceconfig')
    tdkTestObj.addParameter("configkeylist",configkeylist)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    result = ast.literal_eval(result)
    if "SUCCESS" in result[1]:
        tdkTestObj.setResultStatus("SUCCESS")

        # Step 2 : Check the status of the dependent plugin
        print("\n")
        pluginlist = ["org.rdk.RDKWindowManager"]
        tdkTestObj = obj.createTestStep('appmanagers_checkpluginstatus')
        tdkTestObj.addParameter("pluginlist",pluginlist)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")

            # Step 3 : Capture screenshot and check for onScreenshotComplete event
            time.sleep(3)
            print("\n")
            screenshot = getScreenShot(obj)
            print("Screenshot capture result : ", screenshot)
            if screenshot != "FAILURE":
                print("SUCCESS : Screenshot captured successfully")
            else:
                print("FAILURE : Failed to capture screenshot")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")
    obj.setLoadModuleStatus("FAILURE")

# Unload the module
print("\n")
obj.unloadModule("rdkv_appmanagers")