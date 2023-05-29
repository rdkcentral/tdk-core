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
  <version>3</version>
  <name>RDKV_Container_HtmlApp_TimeTo_Destroy</name>
  <primitive_test_id/>
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate the time taken to destroy HtmlApp plugin in container mode</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>Containerization_24</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to destroy HtmlApp plugin in container mode</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/Containerization.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1.HTMLAPP_DESTROY_THRESHOLD_VALUE_IN_CONTAINER
 2.THRESHOLD_OFFSET_IN_CONTAINER
 3.HTMLAPP_DETAILS</input_parameters>
    <automation_approch>1.  After start on the device, ensure that Dobby is running
2. Enable datamodel values
3. Reboot the device or restart WPEFramework service
4. Verify datamodel values
5. Save current system time and destroy HtmlApp using RDKShell.
6. Get the time from triggered event
7. Validate the output with threshold value</automation_approch>
    <expected_output>HtmlApp should be destroyed and time taken to destroy HtmlApp should be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_HtmlApp_TimeTo_Destroy</test_script>
    <skipped>No</skipped>
    <release_version>M113</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
 # use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from containerizationlib import *
from web_socket_util import *
import rdkv_performancelib
from rdkv_performancelib import *
import re;
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("containerization","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Container_HtmlApp_TimeTo_Destroy');
#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "HTMLAPP_DETAILS","HTMLAPP_DESTROY_THRESHOLD_VALUE_IN_CONTAINER", "THRESHOLD_OFFSET_IN_CONTAINER"]
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
            htmlapp_destroy_threshold = configValues["HTMLAPP_DESTROY_THRESHOLD_VALUE_IN_CONTAINER"]
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
    tdkTestObj.addParameter("sshMethod", ssh_method);
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
        time.sleep(20)
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            print "Launching HtmlApp"
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            tdkTestObj.addParameter("launch",htmlapp_details)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print "Check container is running"
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",htmlapp_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    print "Destroying HtmlApp in container mode:"
                    tdkTestObj = obj.createTestStep('containerization_setPluginStatus')
                    tdkTestObj.addParameter("plugin","HtmlApp")
                    tdkTestObj.addParameter("status","deactivate")
                    destroy_start_time = str(datetime.utcnow()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                        tdkTestObj.addParameter("plugin","HtmlApp")
                        tdkTestObj.executeTestCase(expectedResult)
                        HtmlApp_status = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if HtmlApp_status == 'deactivated' and expectedResult in result:
                            print "HtmlApp has been destroyed successfully"
                            #Check for Container launch logs
                            command = 'cat /opt/logs/wpeframework.log | grep "onDestroyed event received for HtmlApp" | tail -1'
                            print "COMMAND : %s" %(command)
                            #Primitive test case which associated to this Script^M
                            tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                            #Add the parameters to ssh to the DUT and execute the command^M
                            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                            tdkTestObj.addParameter("credentials", credentials);
                            tdkTestObj.addParameter("command", command);
                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedResult);
                            output = tdkTestObj.getResultDetails()
                            pattern = r"\b\d{2}:\d{2}:\d{2}\.\d+\b"
                            matches = re.findall(pattern, output)
                            destroyed_time = matches[len(matches)-1]
                            if destroyed_time:
                                print "\n Validate the time taken to destroy HtmlApp in container mode"
                                if all(value != "" for value in (htmlapp_destroy_threshold,threshold_offset)):
                                    destroy_start_time_in_millisec = getTimeInMilliSec(destroy_start_time)
                                    destroyed_time_in_millisec = getTimeInMilliSec(destroyed_time)
                                    print "\n HtmlApp destroy initiated at: ",destroy_start_time
                                    Summ_list.append('HtmlApp destroy initiated at :{}'.format(destroy_start_time))
                                    print "\n HtmlApp destroyed at : ",destroyed_time
                                    Summ_list.append('HtmlApp destroyed at :{}'.format(destroyed_time))
                                    time_taken_for_destroy = destroyed_time_in_millisec - destroy_start_time_in_millisec
                                    print "\n Time taken to destroy HtmlApp: {}(ms)".format(time_taken_for_destroy)
                                    Summ_list.append('Time taken to destroy HtmlApp :{}'.format(time_taken_for_destroy))
                                    print "\n Threshold value for time taken to destroy HtmlApp after reboot: {}ms".format(htmlapp_destroy_threshold)
                                    if 0 < time_taken_for_destroy < (int(htmlapp_destroy_threshold) + int(threshold_offset)) :
                                        print "\n Time taken for destroying HtmlApp is within the expected range \n"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n Time taken for destroying HtmlApp is not within the expected range \n"
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Please configure the Threshold value in device configuration file \n"
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print "\n Error in gettin the status of the plugins"
                                tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Error in destroying HtmlApp in container mode"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "HtmlApp is not running in container mode"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "Failed to destroy HtmlApp"
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
            
