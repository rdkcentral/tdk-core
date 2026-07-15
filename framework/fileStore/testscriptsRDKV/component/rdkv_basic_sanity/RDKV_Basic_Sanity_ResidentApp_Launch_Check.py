##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
from rdkv_basic_sanitylib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_ResidentApp_Launch_Check')

#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    print("\n Launching ResidentApp")
    
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
    
    result = "SUCCESS"
    
    # Check if ResidentApp (refui) is loaded using curl command
    print("\n Checking if ResidentApp is loaded")
    if "directSSH" == configValues["SSH_METHOD"]:
        if configValues["SSH_PASSWORD"] == "None":
            configValues["SSH_PASSWORD"] = ""
        
        credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
        curl_command = 'curl -d \'{ "jsonrpc": 2.0, "id": 8, "method": "org.rdk.AppManager.getLoadedApps" }\' http://127.0.0.1:9998/jsonrpc'
        
        tdkTestObj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
        tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"])
        tdkTestObj.addParameter("credentials", credentials)
        tdkTestObj.addParameter("command", curl_command)
        tdkTestObj.executeTestCase(expectedResult)
        
        output = tdkTestObj.getResultDetails()
        output = str(output)
        print("\n[RESPONSE FROM DEVICE]: %s"%(output))
        
        if "refui" in output and expectedResult in tdkTestObj.getResult():
            print("\n ResidentApp (refui) is loaded successfully")
            Summ_list.append('\nResidentApp Status : Launched')
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("\n ResidentApp (refui) is not loaded")
            Summ_list.append('ResidentApp Status : Not Loaded')
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Currently only supports directSSH method")
        Summ_list.append('ResidentApp Status Check : FAILURE')
        result = "FAILURE"
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
