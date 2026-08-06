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
import json
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Vulkaninfo')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    # Fetch SSH config values in a single batch call
    configKeyList = ["SSH_PORT", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    tdkTestObj.addParameter("basePath", obj.realpath)
    tdkTestObj.addParameter("configKey", json.dumps(configKeyList))
    tdkTestObj.executeTestCase(expectedResult)
    configRaw = str(tdkTestObj.getResultDetails()).strip()
    configValues = {}
    try:
        configValues = ast.literal_eval(configRaw)
        failed_keys = [k for k, v in configValues.items() if "FAILURE" in str(v) or str(v).strip() == ""]
        for k, v in configValues.items():
            print("{} : {}".format(k, v))
        if failed_keys:
            for k in failed_keys:
                print("FAILURE: Failed to retrieve %s from device config" % k)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
        else:
            print("SUCCESS: Successfully retrieved all device config values")
            tdkTestObj.setResultStatus("SUCCESS")
    except Exception as e:
        print("FAILURE: Could not parse device config response: {}".format(e))
        tdkTestObj.setResultStatus("FAILURE")
        result = "FAILURE"

    if "FAILURE" != result:
        if configValues["SSH_METHOD"] == "directSSH":
            if configValues["SSH_PASSWORD"] == "None":
                configValues["SSH_PASSWORD"] = ""
            credentials = obj.IP + "," + configValues["SSH_USERNAME"] + "," + configValues["SSH_PASSWORD"]
            vulkan_output = ""

            # ==============================================================
            # STEP 1: Run vulkaninfo on DUT
            # ==============================================================
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_runVulkaninfo')
            tdkTestObj.addParameter("sshMethod",   configValues["SSH_METHOD"])
            tdkTestObj.addParameter("credentials", credentials)
            tdkTestObj.addParameter("sshPort",     configValues["SSH_PORT"])
            tdkTestObj.executeTestCase(expectedResult)
            result  = tdkTestObj.getResult()
            details = str(tdkTestObj.getResultDetails()).strip()
            if "FAILURE" not in details and "error" not in details.lower():
                print("[STEP 1 - Run Vulkaninfo] : SUCCESS")
                vulkan_output = details
                print("INFO: vulkaninfo output:\n%s" % vulkan_output)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("[STEP 1 - Run Vulkaninfo] : %s" % details)
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"

            # ==============================================================
            # STEP 2: Verify mandatory Vulkan property strings
            # ==============================================================
            if "FAILURE" != result:
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_verifyVulkanProperties')
                tdkTestObj.addParameter("vulkan_output", vulkan_output)
                tdkTestObj.executeTestCase(expectedResult)
                result  = tdkTestObj.getResult()
                details = str(tdkTestObj.getResultDetails()).strip()
                print("[STEP 2 - Verify Vulkan Properties] : %s" % details)
                if "FAILURE" not in details:
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    result = "FAILURE"

            # ==============================================================
            # STEP 3: Verify Vulkan API version >= 1.1.0
            # ==============================================================
            if "FAILURE" != result:
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_verifyVulkanVersion')
                tdkTestObj.addParameter("vulkan_output", vulkan_output)
                tdkTestObj.executeTestCase(expectedResult)
                result  = tdkTestObj.getResult()
                details = str(tdkTestObj.getResultDetails()).strip()
                print("[STEP 3 - Verify Vulkan Version] : %s" % details)
                if "FAILURE" not in details:
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Failed to get SSH configuration values")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
