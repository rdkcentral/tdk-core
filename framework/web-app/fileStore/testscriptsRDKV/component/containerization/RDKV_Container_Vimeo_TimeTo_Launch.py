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
  <version>4</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_Container_Vimeo_TimeTo_Launch</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_executeLifeCycle</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to calculate the time taken to launch Vimeo app in container mode.</synopsis>
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
    <test_case_id>Containerization_35</test_case_id>
    <test_objective>The objective of this script is to calculate the resource usage while launching in Vimeo app in containerization mode. </test_objective>
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
9. Calculate the time taken to launch Vimeo app in container mode</automation_approch>
    <expected_output>Time taken to launch Vimeo app in container mode should not be higher than the threshold value.</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_Vimeo_TimeTo_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M114</release_version>
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
obj.configureTestCase(ip,port,'RDKV_Container_Vimeo_TimeTo_Launch');
#Execution summary variable 
Summ_list=[]
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
                        vimeo_result = tdkTestObj.getResult()
                        start_time = str(datetime.utcnow()).split()[1]
                        time.sleep(10)
                        if(vimeo_result in expectedResult):
                                tdkTestObj.setResultStatus("SUCCESS");
                                print "\n URL is set successfully"
                                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                                tdkTestObj.addParameter("realpath",obj.realpath)
                                tdkTestObj.addParameter("deviceIP",obj.IP)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                                if ssh_param_dict != {} and expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    command = 'cat /opt/logs/wpeframework.log | grep -inr URLChanged.*url.*'+vimeo_playback_url+'| tail -1'
                                    #Primitive test case which associated to this Script
                                    tdkTestObj = obj.createTestStep('containerization_executeInDUT');
                                    #Add the parameters to ssh to the DUT and execute the command
                                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                                    tdkTestObj.addParameter("credentials", credentials);
                                    tdkTestObj.addParameter("command", command);
                                    #Execute the test case in DUT
                                    tdkTestObj.executeTestCase(expectedResult);
                                    output = tdkTestObj.getResultDetails()
                                    if output != "EXCEPTION" and expectedResult in result:
                                        url_changed_line = output.split('\n')[1]
                                        if url_changed_line != "":
                                            url_changed_time = getTimeStampFromString(url_changed_line)
                                            print "\n Vimeo URL set at :{}".format(start_time)
                                            print "\n Vimeo launched at: {} (UTC)".format(url_changed_time)
                                            start_time_millisec = getTimeInMilliSec(start_time)
                                            url_changed_time_millisec = getTimeInMilliSec(url_changed_time)
                                            launch_time = url_changed_time_millisec - start_time_millisec
                                            print "\n Time taken to launch the application: {} milliseconds \n".format(launch_time)
                                            conf_file,result = getConfigFileName(tdkTestObj.realpath)
                                            result1, vimeo_launch_threshold_value = getDeviceConfigKeyValue(conf_file,"VIMEO_LAUNCH_THRESHOLD_VALUE")
                                            Summ_list.append('VIMEO_LAUNCH_THRESHOLD_VALUE :{}ms'.format(vimeo_launch_threshold_value))
                                            result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                                            Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                                            Summ_list.append('Application Initiated  at :{}'.format(start_time))
                                            Summ_list.append('Application launched at :{}'.format(url_changed_time))
                                            Summ_list.append('Time taken to launch the application :{}ms'.format(launch_time))
                                            if all (value != "" for value in (vimeo_launch_threshold_value,offset)):
                                                print "\n Threshold value for time taken to launch the vimeo: {} ms".format(vimeo_launch_threshold_value)
                                                if 0 < int(launch_time) < (int(vimeo_launch_threshold_value) + int(offset)):
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print "\n The time taken to launch the vimeo is within the expected limit\n"
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print "\n The time taken to launch the vimeo is not within the expected limit \n"
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print "\n Failed to get the threshold value from config file"
                                        else:
                                            print "\n URL is not loaded in DUT"
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print "\n Error occurred while executing the command:{} in DUT,\n Please check the SSH details".format(command)
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print "\n Error in setting up the url"
                                    tdkTestObj.setResultStatus("FAILURE")
                        else:
                            "\n Error in setting up the vimeo url"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error while launching lightningApp in container"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Unable to check the container running state"
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
    getSummary(Summ_list,obj)
else:
    print "Set Post Requisites Failed"
    tdkTestObj.setResultStatus("FAILURE")
obj.unloadModule("containerization");                         
                            
