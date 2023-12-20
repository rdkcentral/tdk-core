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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Container_Cobalt_TimeTo_SuspendResume</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to suspend resume in Cobalt plugin in container mode</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RDKTV</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>Containerization_45</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to suspend and resume Cobalt plugin in container mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/Containerization.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. COBALT_DETAILS
2. COBALT_SUSPEND_THRESHOLD_VALUE_CONTAINER
3. THRESHOLD_OFFSET_IN_CONTAINER
4. COBALT_RESUME_THRESHOLD_VALUE_CONTAINER</input_parameters>
    <automation_approch>1.  After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Save current system time and suspend Cobalt using RDKShell.
6. Launch Cobalt using RDKShell
7. Suspend the plugin and get the time from triggered event.
8. After suspending successfully, resume the plugin by launching it and get the time from triggered event.
9. Validate the output with threshold value</automation_approch>
    <expected_output>The time taken to suspend and resume Cobalt plugin in container mode should be within the expected limit. </expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_Cobalt_TimeTo_SuspendResume</test_script>
    <skipped>No</skipped>
    <release_version>M117</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from containerizationlib import *
import re;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_Cobalt_TimeTo_SuspendResume');
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("Retrieving Configuration values from config file.......")
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "COBALT_DETAILS","COBALT_SUSPEND_THRESHOLD_VALUE_CONTAINER", "THRESHOLD_OFFSET_IN_CONTAINER","COBALT_RESUME_THRESHOLD_VALUE_CONTAINER"]
    configValues = {}
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj = obj.createTestStep('containerization_getDeviceConfig')
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase("SUCCESS")
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print("SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey))
        else:
            print("FAILURE: Failed to retrieve %s configuration from device config file" %(configKey))
            if configValues[configKey] == "":
                print("\n [INFO] Please configure the %s key in the device config file" %(configKey))
                result = "FAILURE"
                break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"]:
            ssh_method = configValues["SSH_METHOD"]
            user_name = configValues["SSH_USERNAME"]
            cobalt_details = configValues["COBALT_DETAILS"]
            cobalt_resume_threshold = configValues["COBALT_RESUME_THRESHOLD_VALUE_CONTAINER"]
            cobalt_suspend_threshold = configValues["COBALT_SUSPEND_THRESHOLD_VALUE_CONTAINER"]
            threshold_offset = configValues["THRESHOLD_OFFSET_IN_CONTAINER"]
            if configValues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configValues["SSH_PASSWORD"]
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            config_status = "FAILURE"
    else:
        config_status = "FAILURE"
    credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
    print("\nTo Ensure Dobby service is running")
    command = 'systemctl status dobby | grep active | grep -v inactive'
    print("COMMAND : %s" %(command))
    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
    #Add the parameters to ssh to the DUT and execute the command
    tdkTestObj.addParameter("sshMethod", ssh_method);
    tdkTestObj.addParameter("credentials", credentials);
    tdkTestObj.addParameter("command", command);
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult()
    #Get the result of execution
    output = tdkTestObj.getResultDetails();
    if "Active: active" in output and expectedResult in result:
        print("Dobby is running %s" %(output))
        #To enable datamodel
        datamodel=["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.Cobalt.Enable"]
        tdkTestObj = obj.createTestStep('containerization_setPreRequisites')
        tdkTestObj.addParameter("datamodel",datamodel)
        tdkTestObj.executeTestCase(expectedResult)
        actualresult= tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(15)
            print("Launch Cobalt")
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            tdkTestObj.addParameter("launch",cobalt_details)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print("Check container is running")
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",cobalt_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check for Container launch logs
                    command = 'cat /opt/logs/wpeframework.log | grep "launching cobalt in container mode" | tail -1'
                    print("COMMAND : %s" %(command))
                    #Primitive test case which associated to this Script
                    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                    #Add the parameters to ssh to the DUT and execute the command
                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                    tdkTestObj.addParameter("credentials", credentials);
                    tdkTestObj.addParameter("command", command);
                    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedResult);
                    output = tdkTestObj.getResultDetails()
                    if "launching cobalt in container mode" in output:
                        print("cobalt launched successfully in container mode")
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("Suspend Cobalt")
                        suspend_status,start_suspend = containerization_suspend_plugin(obj,"Cobalt")
                        time.sleep(10)
                        if suspend_status == expectedResult:
                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                            tdkTestObj.addParameter("plugin","Cobalt")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            Cobalt_status = tdkTestObj.getResultDetails()
                            if Cobalt_status == 'suspended' and expectedResult in result:
                                print("\n Cobalt suspended successfully")
                                print("\n Check for onSuspended event from wpeframework logs")
                                command = 'cat /opt/logs/wpeframework.log | grep "RDKShell onSuspended event received for Cobalt" | tail -1'
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                print("COMMAND : %s" %(command))
                                #Primitive test case which associated to this Script
                                tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                                #Add the parameters to ssh to the DUT and execute the command
                                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                tdkTestObj.addParameter("credentials", credentials);
                                tdkTestObj.addParameter("command", command);
                                #Execute the test case in DUT
                                tdkTestObj.executeTestCase(expectedResult);
                                output = tdkTestObj.getResultDetails()
                                print (output)
                                suspended_time = output.split("tail -1")[1].split(" ")[2]
                                print (suspended_time)
                                if "RDKShell onSuspended event received for Cobalt" in output:
                                    print("\n cobalt suspended successfully and event recieved from wpeframework logs")
                                    print("\n Resume Cobalt")
                                    tdkTestObj = obj.createTestStep('containerization_launchApplication')
                                    tdkTestObj.addParameter("launch",cobalt_details)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    output = tdkTestObj.getResultDetails()
                                    time_pattern = r"\d{2}:\d{2}:\d{2}\.\d+"
                                    match = re.search(time_pattern, output)
                                    start_resume = match.group()
                                    if expectedResult in output:
                                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                        tdkTestObj.addParameter("plugin","Cobalt")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        Cobalt_status = tdkTestObj.getResultDetails()
                                        if Cobalt_status == 'resumed' and expectedResult in result:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("\n The plugin status is received as 'resumed' successfully")
                                            print("Check container is running")
                                            tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                                            tdkTestObj.addParameter("callsign",cobalt_details)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            actualresult = tdkTestObj.getResultDetails()
                                            if expectedResult in actualresult.upper():
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                #Check for Container launch logs
                                                command = 'cat /opt/logs/wpeframework.log | grep "launching cobalt in container mode" | tail -1'
                                                print("COMMAND : %s" %(command))
                                                #Primitive test case which associated to this Script
                                                tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                                                #Add the parameters to ssh to the DUT and execute the command
                                                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                                tdkTestObj.addParameter("credentials", credentials);
                                                tdkTestObj.addParameter("command", command);
                                                #Execute the test case in DUT
                                                tdkTestObj.executeTestCase(expectedResult);
                                                output = tdkTestObj.getResultDetails()
                                                resumed_time = output.split("tail -1")[1].split(" ")[2]
                                                if "launching cobalt in container mode" in output:
                                                    print("Cobalt resumed successfully in container mode")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    if suspended_time and resumed_time:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        start_suspend_in_millisec = getTimeInMilliSec(start_suspend)
                                                        suspended_time_in_millisec = getTimeInMilliSec(suspended_time)
                                                        print("\n Suspended initiated at: ",start_suspend)
                                                        print("\n Suspended at : ",suspended_time)
                                                        time_taken_for_suspend = suspended_time_in_millisec - start_suspend_in_millisec
                                                        print("\n Time taken to suspend Cobalt Plugin: " + str(time_taken_for_suspend) + "(ms)")
                                                        print("\n Threshold value for time taken to suspend Cobalt plugin : {} ms".format(cobalt_suspend_threshold))
                                                        print("\n Validate the time taken for suspending the plugin")
                                                        if 0 < time_taken_for_suspend < (int(cobalt_suspend_threshold) + int(threshold_offset)) :
                                                            print("\n Time taken for suspending Cobalt plugin is within the expected range")
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            print("\n Time taken for suspending Cobalt plugin is greater than the expected range")
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                        start_resume_in_millisec = getTimeInMilliSec(start_resume)
                                                        resumed_time_in_millisec =  getTimeInMilliSec(resumed_time)
                                                        print("\n Resume initiated at: ",start_resume)
                                                        print("\n Resumed at: ",resumed_time)
                                                        time_taken_for_resume = resumed_time_in_millisec - start_resume_in_millisec
                                                        print("\n Time taken to resume Cobalt Plugin: " + str(time_taken_for_resume) + "(ms)")
                                                        print("\n Threshold value for time taken to resume Cobalt plugin : {} ms".format(cobalt_resume_threshold))
                                                        print("\n Validate the time taken for resuming the plugin ")
                                                        if 0 < time_taken_for_resume < (int(cobalt_resume_threshold) + int(threshold_offset)) :
                                                            print("\n Time taken for resuming Cobalt plugin is within the expected range")
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                        else:
                                                            print("\n Time taken for resuming Cobalt plugin is greater than the expected range")
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                    else:
                                                        print("\n Error in suspend and resume events")
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                else:
                                                    print("\n Unable to get required logs")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print("\n Cobalt is not running in container mode")
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print("Error in getting the status of plugin")
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print("Failed to launch Cobalt")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("\n RDKShell onSuspended event not recieved in wpeframework logs")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("\n Error in getting the status if plugin")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("\n Unable to suspend the plugin")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("\n Unable to get the required logs")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\n Cobalt is not running in container mode")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Failed to launch Cobalt")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to enable data model value")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("Dobby service is not running")
        tdkTestObj.setResultStatus("FAILURE")
tdkTestObj = obj.createTestStep('containerization_setPostRequisites')
tdkTestObj.addParameter("datamodel",datamodel)
tdkTestObj.executeTestCase(expectedResult)
actualresult = tdkTestObj.getResultDetails()
if expectedResult in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS")
else:
    print("Set Post Requisites Failed")
    tdkTestObj.setResultStatus("FAILURE")
obj.unloadModule("containerization");
