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
  <name>RDKV_Container_Vimeo_ResourceUsage_VideoPlayBack</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_executeLifeCycle</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to calculate the resource usage during video playback in Vimeo app in container mode.</synopsis>
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
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>Containerization_17</test_case_id>
    <test_objective>The objective of this script is to calculate the resource usage during video playback in Vimeo app in containerization mode. </test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>vimeo_playback_url </input_parameters>
    <automation_approch>1.  After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Launch Vimeo
6. Verify that Vimeo is running in container mode
7. Check wpeframework.log
8. Start playback
9. Calculate resource usage</automation_approch>
    <expected_output>Resource usage while video playback in Vimeo app should not be higher than the threshold value.</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_Vimeo_ResourceUsage_VideoPlayBack</test_script>
    <skipped>No</skipped>
    <release_version>M112</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from containerizationlib import *
import PerformanceTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_Vimeo_ResourceUsage_VideoPlayBack');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "LIGHTNINGAPP_DETAILS", "VIMEO_PLAYBACK_URL"]
    configValues = {}
    webkit_instance = PerformanceTestVariables.webkit_instance
    set_method = webkit_instance+'.1.url'
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
            lightningApp_details = configValues["LIGHTNINGAPP_DETAILS"]
            vimeo_playback_url = configValues["VIMEO_PLAYBACK_URL"]
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
        #To enable datamodel
        datamodel=["Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Dobby.WPE.Enable"]
        tdkTestObj = obj.createTestStep('containerization_setPreRequisites')
        tdkTestObj.addParameter("datamodel",datamodel)
        tdkTestObj.executeTestCase(expectedResult)
        actualresult= tdkTestObj.getResultDetails()
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            print "Launch LightningApp"
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            tdkTestObj.addParameter("launch",lightningApp_details)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print "Check container is running"
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",lightningApp_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check for Container launch logs
                    command = 'cat /opt/logs/wpeframework.log | grep "launching LightningApp in container mode"'
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
                    if "launching LightningApp in container mode" in output:
                        print "LightningApp launched successfully in container mode"
                        print "\n Set the Vimeo URL"
                        tdkTestObj = obj.createTestStep('containerization_setValue')
                        tdkTestObj.addParameter("method",set_method)
                        tdkTestObj.addParameter("value",vimeo_playback_url)
                        tdkTestObj.executeTestCase(expectedResult)
                        cobalt_result = tdkTestObj.getResult()
                        time.sleep(10)
                        if(cobalt_result in expectedResult):
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "Clicking OK to play video"
                            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                            tdkTestObj = obj.createTestStep('containerization_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result1 = tdkTestObj.getResult()
                            time.sleep(50)
                            if "SUCCESS" == result1:
                                print "\n Check video is started \n"
                                tdkTestObj.setResultStatus("SUCCESS")
                                tdkTestObj = obj.createTestStep('containerization_getSSHParams')
                                tdkTestObj.addParameter("realpath",obj.realpath)
                                tdkTestObj.addParameter("deviceIP",obj.IP)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                                if ssh_param_dict != {} and expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    if validation_dict["validation_required"]:
                                        if validation_dict["password"] == "None":
                                            password = ""
                                    else:
                                        password = validation_dict["password"]
                                        tdkTestObj = obj.createTestStep('containerization_validateProcEntry')
                                        tdkTestObj.addParameter("ssh_method", ssh_param_dict["ssh_method"])
                                        tdkTestObj.addParameter("credentials", ssh_param_dict["credentials"])
                                        tdkTestObj.addParameter("video_validation_script", validation_dict["video_validation_script"])
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        output = tdkTestObj.getResultDetails()
                                else:
                                    print "\n Skipped the proc entry validation as this device is not configured for this validation"
                                print "\n Validate Resource Usage"
                                tdkTestObj = obj.createTestStep("containerization_validateResourceUsage")
                                tdkTestObj.executeTestCase(expectedResult)
                                resource_usage = tdkTestObj.getResultDetails()
                                result = tdkTestObj.getResult()
                                if expectedResult in result and resource_usage != "ERROR":
                                    print "\n Successfully validated Resource usage"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Error while validating Resource usage"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "Error while generating key code"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "Unable to launch the url"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Unable to get the required logs"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "LightningApp is not running in container mode"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Failed to launch LightningApp"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Failed to enable data model value"
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