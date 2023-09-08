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
##########################################################################
'''
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>RDKV_Basic_Sanity_Lightsleep_Service_Status</name>
  <primitive_test_id/>
  <primitive_test_name>rdkv_basic_sanity_executeInDUT</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To validate the status of services running before and after lightsleep</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_Basic_Sanity_06</test_case_id>
    <test_objective>To Initiate the shell scripts which check status of service before and after lightsleep.If status vary reboot the dut and check the status.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-HYB,RPI-Client,Video_Accelerator</test_setup>
    <pre_requisite>1. Configure the location of shell scripts in SANITY_SCRIPT_PATH available in fileStore/Basic_Sanity_Config.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>SANITY_SCRIPT_PATH</input_parameters>
    <automation_approch>1. Check the status of services before lighstsleep.
    2.If services are not same after lightsleep reboot</automation_approch>
    <expected_output>Respective Scripts are executed and Validating status of services before and after lightsleep</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_basic_sanity</test_stub_interface>
    <test_script>RDKV_Basic_Sanity_Lightsleep_Service_Status</test_script>
    <skipped>No</skipped>
    <release_version>M113</release_version>
    <remarks/>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_basic_sanitylib import *
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Lightsleep_Service_Status');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result.upper());

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    configKeyList = ["SANITY_SCRIPT_PATH","SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    configValues={}
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configValues[configKey] == "":
                print "\n Please configure the %s key in the device config file" %(configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"] :
            if configValues["SSH_PASSWORD"] == "None":
                configValues["SSH_PASSWORD"] = ""
            credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
            command = "sh " + configValues["SANITY_SCRIPT_PATH"] + "/system_sanity_lightsleep_service_status.sh"
            #Primitive test case associated with this Script
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_rebootexecution');
            #Add the parameters to ssh to the DUT and execute the command
            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
            tdkTestObj.addParameter("credentials", credentials);
            tdkTestObj.addParameter("command", command);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            output = tdkTestObj.getResultDetails();
            # View log file after 300 seconds
            print("Waiting for 300 seconds before checking log file to finish reboot process...")
            time.sleep(300)
            command = "cat $(find / -name 'system_sanity_lightsleep_service_status.log' 2>/dev/null | head -n1)"
            print("COMMAND: %s" % command)
            # Primitive test case which associated to this Script
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_executeInDUT');
            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
            tdkTestObj.addParameter("credentials", credentials);
            tdkTestObj.addParameter("command", command);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult()
            # Get the result of execution
            output = tdkTestObj.getResultDetails();
            output = str(output)
            print("[RESPONSE FROM DEVICE]: %s" % output)
            if "FAILURE" in output or expectedResult not in output:
                #Check if the file exists or not
                if "No such file or directory" in output:
                  print "FAILURE: File not found"
                  tdkTestObj.setResultStatus("FAILURE")
                else:
                  print "FAILURE: Script Execution was not Successful"
                  tdkTestObj.setResultStatus("FAILURE")
            elif "FAILURE" not in output and expectedResult in output:
                print "SUCCESS: Script Execution Successful"
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print "Error: Error in the Script Execution"
                tdkTestObj.setResultStatus("FAILURE")           
        else:
            print "FAILURE: Currently only supports directSSH ssh method"
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print "FAILURE: Failed to get configuration values"
        tdkTestObj.setResultStatus("FAILURE");
    #Unload the module
    obj.unloadModule("rdkv_basic_sanity_executeInDUT");

else:
    #Set load module status
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"

