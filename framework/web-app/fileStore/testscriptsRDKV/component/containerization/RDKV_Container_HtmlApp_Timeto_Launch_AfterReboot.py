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
  <version>6</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Container_HtmlApp_Timeto_Launch_AfterReboot</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate time taken to launch HtmlApp after reboot.</synopsis>
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
    <box_type>RDKTV</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>Containerization_50</test_case_id>
    <test_objective>Validate time to launch HtmlApp after reboot</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/Containerization.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>HTMLAPP_DETAILS=
HTMLAPP_PLAYBACK_URL=</input_parameters>
    <automation_approch>1.  After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Launch HtmlApp
6. Verify that HtmlApp is running in container mode
7. Check wpeframework.log
9.Reboot the device
10. Launch HtmlApp
11. Verify that HtmlApp is running in container mode.</automation_approch>
    <expected_output>Time taken to launch HtmlApp after reboot</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_HtmlApp_Timeto_Launch_AfterReboot</test_script>
    <skipped>No</skipped>
    <release_version>M116</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from containerizationlib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_HtmlApp_Timeto_Launch_AfterReboot');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "HTMLAPP_DETAILS","HTMLAPP_LAUNCH_THRESHOLD_VALUE_IN_CONTAINER", "THRESHOLD_OFFSET_IN_CONTAINER"]
    configValues = {}
    #Get each configuration from device config file
    for configKey in configKeyList:
        tdkTestObj = obj.createTestStep('containerization_getDeviceConfig')
        tdkTestObj.addParameter("basePath",obj.realpath)
        tdkTestObj.addParameter("configKey",configKey)
        tdkTestObj.executeTestCase("SUCCESS")
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print "SUCCESS: Successfully retrieved %s configuration from device config file" %(configKey)
        else:
            print "FAILURE: Failed to retrieve %s configuration from device config file" %(configKey)
            if configValues[configKey] == "":
                print "\n [INFO] Please configure the %s key in the device config file" %(configKey)
                result = "FAILURE"
                break
    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"]:
            ssh_method = configValues["SSH_METHOD"]
            user_name = configValues["SSH_USERNAME"]
            htmlapp_details = configValues["HTMLAPP_DETAILS"]
            htmlapp_launch_threshold = configValues["HTMLAPP_LAUNCH_THRESHOLD_VALUE_IN_CONTAINER"]
            threshold_offset = configValues["THRESHOLD_OFFSET_IN_CONTAINER"]
            if configValues["SSH_PASSWORD"] == "None":
                password = ""
            else:
                password = configValues["SSH_PASSWORD"]
        else:
            print "FAILURE: Currently only supports directSSH ssh method"
            config_status = "FAILURE"
    else:
        config_status = "FAILURE"

    credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
    print "\nTo Ensure Dobby service is running"
    command = 'systemctl status dobby | grep active | grep -v inactive'
    print "COMMAND : %s" %(command)

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
    #Add the parameters to ssh to the DUT and execute the command
    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
    tdkTestObj.addParameter("credentials", credentials);
    tdkTestObj.addParameter("command", command);

    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedResult);
    result = tdkTestObj.getResult()

    #Get the result of execution
    output = tdkTestObj.getResultDetails();
    if "Active: active" in output and expectedResult in result:
        print "Dobby is running %s" %(output)
        print "Reboot Device"
        tdkTestObj = obj.createTestStep('containerization_rebootDevice')
        tdkTestObj.addParameter("waitTime",60)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS")
            #To enable datamodel
            datamodel=["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.WPE.Enable"]
            tdkTestObj = obj.createTestStep('containerization_setPreRequisites')
            tdkTestObj.addParameter("datamodel",datamodel)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult= tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print "Launch HtmlApp"
                tdkTestObj = obj.createTestStep('containerization_launchApplication')
                tdkTestObj.addParameter("launch",htmlapp_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                launch_start_time = actualresult.split(",")[1][2:17]
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "Check container is running"
                    tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                    tdkTestObj.addParameter("callsign",htmlapp_details)
                    tdkTestObj.executeTestCase(expectedResult)
                    actualresult = tdkTestObj.getResultDetails()
                    if expectedResult in actualresult.upper():
                        tdkTestObj.setResultStatus("SUCCESS")
                        #Check for Container launch logs
                        command = 'cat /opt/logs/wpeframework.log | grep "launching HtmlApp in container mode"| tail -1'
                        print "COMMAND : %s" %(command)
                        #Primitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                        #Add the parameters to ssh to the DUT and execute the command
                        tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                        tdkTestObj.addParameter("credentials", credentials);
                        tdkTestObj.addParameter("command", command);

                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult);
                        output = tdkTestObj.getResultDetails()
                        if "launching HtmlApp in container mode" in output:
                            print "HtmlApp launched successfully in container mode"
                            pattern = r"\b\d{2}:\d{2}:\d{2}\.\d+\b"
                            matches = re.findall(pattern, output)
                            launched_time = matches[len(matches)-1]
                            print "\nlaunched time", launched_time  
                            if launched_time:
                                print "\n Validating the time taken to launch HtmlApp in container mode"
                                if all(value != "" for value in (htmlapp_launch_threshold,threshold_offset)):
                                    launch_start_time_in_millisec = getTimeInMilliSec(launch_start_time)
                                    launched_time_in_millisec = getTimeInMilliSec(launched_time)
                                    print "\n HtmlApp launch initiated at: ",launch_start_time
                                    print "\n HtmlApp launched at : ",launched_time
                                    time_taken_for_launch = launched_time_in_millisec - launch_start_time_in_millisec
                                    print "\n Time taken to launch HtmlApp: {}(ms)".format(time_taken_for_launch)
                                    print "\n Threshold value for time taken to launch HtmlApp after reboot: {}ms".format(htmlapp_launch_threshold)
                                    if 0 < time_taken_for_launch < (int(htmlapp_launch_threshold) + int(threshold_offset)) :
                                        print "\n Time taken for launching HtmlApp is within the expected range \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for launching HtmlApp is not within the expected range \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Please configure the Threshold value in device configuration file \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Not able to get the launch time"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Unable to get the required logs"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "HtmlApp is not running in container mode"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Failed to launch HtmlApp"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Failed to enable data model value"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Reboot device failed"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "Dobby service is not running"
        tdkTestObj.setResultStatus("FAILURE")

tdkTestObj = obj.createTestStep('containerization_setPostRequisites')
tdkTestObj.addParameter("datamodel",datamodel)
tdkTestObj.executeTestCase(expectedResult)
actualresult = tdkTestObj.getResultDetails()
if expectedResult in actualresult.upper():
    tdkTestObj.setResultStatus("SUCCESS")
else:
    print "Set Post Requisites Failed"
    tdkTestObj.setResultStatus("FAILURE")

obj.unloadModule("containerization");