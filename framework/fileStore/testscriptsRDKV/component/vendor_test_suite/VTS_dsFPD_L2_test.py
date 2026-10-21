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
import tdklib;
from VTSTestVariables import * 
from vendor_test_suitelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("vendor_test_suite","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'VTS_dsFPD_L2_test');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

try:
    tdkTestObj = obj.createTestStep('getDeviceConfigValues')
    tdkTestObj.addParameter("configKey","VTS_FRONT_PANEL_SUPPORT_ENABLED")
    tdkTestObj.executeTestCase("SUCCESS");
    actualresult = tdkTestObj.getResult();
    supported = tdkTestObj.getResultDetails();
except:
    supported = "no"

if supported == "no":
    print("Front panel testcases are not applicable for the device\n");
    print("Please set \"VTS_FRONT_PANEL_SUPPORT_ENABLED = yes\" in device specific config file to enable FPD execution for this device\n")
    obj.setAsNotApplicable();
    tdkTestObj = obj.createTestStep('setVTSResult')
    tdkTestObj.addParameter("failed_testCases", "ERROR")
    tdkTestObj.executeTestCase("SUCCESS")
    status = tdkTestObj.getResultDetails()
    tdkTestObj.setResultStatus("N/A")

if "SUCCESS" in result.upper() and supported == "yes":
    tdkTestObj = obj.createTestStep('getDeviceConfigValues')
    tdkTestObj.addParameter("configKey", "SSHParams")
    tdkTestObj.executeTestCase("SUCCESS")
    actualresult = tdkTestObj.getResult();
    ssh_params = tdkTestObj.getResultDetails().strip().split()
    tdkTestObj.setResultStatus("SUCCESS")
    username = ssh_params[0]
    password = ssh_params[1]

    #Set module
    module = "L2 dsFPD"
    #Set binary name
    binaryName = DeviceSettings_binaryName
    #Set TestCase Config
    binaryConfig = FPD_SOURCE_binaryConfig if "SOURCE" in DEVICE_TYPE.upper() else FPD_SINK_binaryConfig
    #Set Custom List of TestCases
    testCaseList = FPD_L2_List
    #Set basepath of test
    basePath =  DeviceSettings_basePath
    #SkipTestCaseList
    SkipTestCaseList = FPD_L2_SkipTestCaseList

    #Configuring plugin name
    words = module.split()
    words[0], words[-1] = words[-1], words[0]
    plugin_name = " ".join(words)
    testcaseID="dsFPD L1"

    testList = SetupPreRequisites(str(ip), username, password, basePath, binaryName, binaryConfig, module)

    try:
        if testList:
            print("\n####################################################################################")
            print("            PLUGIN NAME :  ",plugin_name)
            print("####################################################################################")

            binaryPath = "cd " + basePath + " ; ./" + binaryName + " -p " + binaryConfig
            executionSummary = runTest(binaryPath, module, testcaseID, testList, testCaseList, SkipTestCaseList, binaryConfig=binaryConfig)
    
            executePostRequisites()

            failed_testCases = printTestSummary(executionSummary, plugin_name)
        else:
            print("ERROR : NO TESTS FOUND")
            failed_testCases = "ERROR"
    except:
        failed_testCases = "ERROR"
    
    tdkTestObj = obj.createTestStep('setVTSResult')
    tdkTestObj.addParameter("failed_testCases", failed_testCases)
    tdkTestObj.executeTestCase("SUCCESS")
    status = tdkTestObj.getResultDetails()
    tdkTestObj.setResultStatus(status)

    obj.unloadModule("vendor_test_suite");
elif "SUCCESS" not in result.upper():
    print ("MODULE LOAD FAILURE")
else:
    print ("Test not applicable for device")
