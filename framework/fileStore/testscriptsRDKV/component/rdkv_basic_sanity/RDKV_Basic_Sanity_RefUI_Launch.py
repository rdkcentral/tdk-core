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
import ast
from rdkv_basic_sanitylib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_RefUI_Launch')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    print("\n Launching RefUI")
    
    # Get SSH configuration from device config file
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    configValues = {}
    
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath", obj.realpath)
        tdkTestObj.addParameter("configKey", configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print("SUCCESS: Retrieved %s from device config file" %(configKey))
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("FAILURE: Failed to retrieve %s from device config file" %(configKey))
            tdkTestObj.setResultStatus("FAILURE")
    
    # Check if RefUI is loaded using the library function
    print("\n Checking if RefUI is loaded")
    tdkTestObj = obj.createTestStep('rdkservice_get_loaded_apps')
    tdkTestObj.executeTestCase(expectedResult)
    loaded_apps = ast.literal_eval(str(tdkTestObj.getResultDetails()))
    
    if isinstance(loaded_apps, list) and any("refui" in str(app).lower() for app in loaded_apps):
        print("\n RefUI is loaded successfully")
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("\n RefUI is not loaded")
        tdkTestObj.setResultStatus("FAILURE")
        result = "FAILURE"
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
