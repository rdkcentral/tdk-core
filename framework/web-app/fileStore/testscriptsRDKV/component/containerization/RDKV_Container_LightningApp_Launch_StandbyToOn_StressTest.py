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
  <name>RDKV_Container_LightningApp_Launch_StandbyToOn_StressTest</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>containerization_launchApplication</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate whether LightningApp is in contianer mode after changing Standby to On for 5 iterations</synopsis>
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
    <test_case_id>Containerization_60</test_case_id>
    <test_objective>The objective of this test is to validate whether LightningApp is in contianer mode after changing Standby to On for 5 iterations</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Configure the values SSH Method (variable $SSH_METHOD), DUT username (variable $SSH_USERNAME)and password of the DUT (variable $SSH_PASSWORD)  available in fileStore/device.config file</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>LIGHTNINGAPP_DETAILS=</input_parameters>
    <automation_approch>1. Launch LightningApp in contianer mode as pre condition.
2. Check and set the preferred standby mode as LIGHT_SLEEP.
3. Verify the power state and set it as STANDBY if it is ON.
4. In a loop of 5 times, Set the power state to ON and then to STANDBY.
5. At the end of 5th iteration, set the power  state to ON
6. Verify whether LightningApp is still running in container mode.</automation_approch>
    <expected_output>LightningApp should be in contianer mode after changing StandbyOn for 5 iterations</expected_output>
    <priority>High</priority>
    <test_stub_interface>containerization</test_stub_interface>
    <test_script>RDKV_Container_LightningApp_Launch_StandbyToOn_StressTest</test_script>
    <skipped>No</skipped>
    <release_version>M118</release_version>
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
obj.configureTestCase(ip,port,'RDKV_Container_LightningApp_Launch_StandbyToOn_StressTest');
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "LIGHTNINGAPP_DETAILS"]
    configValues = {}
    max_powerstate_changes = 5
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
            LightningApp_details = configValues["LIGHTNINGAPP_DETAILS"]
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
        if expectedResult in actualresult.upper():
            tdkTestObj.setResultStatus("SUCCESS")
            print "Launch LightningApp"
            tdkTestObj = obj.createTestStep('containerization_launchApplication')
            tdkTestObj.addParameter("launch",LightningApp_details)
            tdkTestObj.executeTestCase(expectedResult)
            actualresult = tdkTestObj.getResultDetails()
            if expectedResult in actualresult.upper():
                tdkTestObj.setResultStatus("SUCCESS")
                print "Check container is running"
                tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                tdkTestObj.addParameter("callsign",LightningApp_details)
                tdkTestObj.executeTestCase(expectedResult)
                actualresult = tdkTestObj.getResultDetails()
                if expectedResult in actualresult.upper():
                    tdkTestObj.setResultStatus("SUCCESS")
                    #Check for Container launch logs
                    command = 'cat /opt/logs/wpeframework.log | grep "launching LightningApp in container mode" | tail -1'
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
                        print "\nPre conditions for the test are set successfully"
                        print "\n Get the current StandByMode of the device:"
                        print "\n Invoke org.rdk.System.1.getPreferredStandbyMode \n"
                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                        tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                        tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult();
                        preferred_standby = tdkTestObj.getResultDetails()
                        if expectedResult in result and preferred_standby != "LIGHT_SLEEP":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print "\n Set standby mode as LIGHT_SLEEP \n"
                            params = '{"standbyMode":"LIGHT_SLEEP"}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue');
                            tdkTestObj.addParameter("method","org.rdk.System.1.setPreferredStandbyMode");
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult();
                            if expectedResult in result:
                                print "\n SetPreferredStandbyMode is success \n"
                                tdkTestObj.setResultStatus("SUCCESS")
                                print "\n Invoke org.rdk.System.1.getPreferredStandbyMode \n"
                                tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult');
                                tdkTestObj.addParameter("method","org.rdk.System.1.getPreferredStandbyMode");
                                tdkTestObj.addParameter("reqValue","preferredStandbyMode")
                                tdkTestObj.executeTestCase(expectedResult);
                                result = tdkTestObj.getResult();
                                preferred_standby = tdkTestObj.getResultDetails()
                                if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                                    print "\n Preferred standby mode is LIGHT_SLEEP \n"
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print "\n Error in setting up the stand by mode as LIGHT_SLEEP"
                                    tdkTestObj.setResultStatus("FAILURE")
                        if expectedResult in result and preferred_standby == "LIGHT_SLEEP":
                            print "Check the current power state"
                            tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                            tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                            tdkTestObj.addParameter("reqValue","powerState")
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            current_power_state = tdkTestObj.getResultDetails()
                            if expectedResult in result and current_power_state != "STANDBY":
                                print "\n The current power state is: ",current_power_state
                                print "\n Set the current power state mode to StandBy"
                                params = '{"powerState":"STANDBY", "standbyReason":"APIUnitTest"}'
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState")
                                tdkTestObj.addParameter("value",params)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                if expectedResult in result:
                                    print "\n Get the current power state: \n"
                                    tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                    tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                    tdkTestObj.addParameter("reqValue","powerState")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    current_power_state = tdkTestObj.getResultDetails()
                                else:
                                    print "\n Error in setting up the power state to standby"
                                    tdkTestObj.setResultStatus("FAILURE")
                            if expectedResult in result and current_power_state == "STANDBY":
                                for count in range(0,max_powerstate_changes):
                                    print "\n********************ITERATION: {} ********************\n".format(count+1)
                                    print "\n Set Preferred standby mode to ON"
                                    params = '{"powerState":"ON", "standbyReason":"APIUnitTest"}'
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState")
                                    tdkTestObj.addParameter("value",params)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResult()
                                    if expectedResult in result:
                                        print "\n Get the current power state: \n"
                                        tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                        tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                        tdkTestObj.addParameter("reqValue","powerState")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult()
                                        current_power_state = tdkTestObj.getResultDetails()
                                        if expectedResult in result and current_power_state == "ON":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print "\n Current power state : \n",current_power_state
                                            if count != 4:
                                                print "\n Change the power state to StandBy:"
                                                params = '{"powerState":"STANDBY", "standbyReason":"APIUnitTest"}'
                                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                tdkTestObj.addParameter("method","org.rdk.System.1.setPowerState")
                                                tdkTestObj.addParameter("value",params)
                                                tdkTestObj.executeTestCase(expectedResult)
                                                result = tdkTestObj.getResult()
                                                if expectedResult in result:
                                                    print "\n Get the current power state: \n"
                                                    tdkTestObj = obj.createTestStep('rdkservice_getReqValueFromResult')
                                                    tdkTestObj.addParameter("method","org.rdk.System.1.getPowerState")
                                                    tdkTestObj.addParameter("reqValue","powerState")
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResult()
                                                    current_power_state = tdkTestObj.getResultDetails()
                                                    if expectedResult in result and current_power_state == "STANDBY":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print "\n Current power state : \n",current_power_state
                                                    else:
                                                        print "\n Error in getting the current powerState"
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                else:
                                                    print "\n Error in setting the powerState to STANDBY"
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                            else:
                                                print "\n Completed setting the device powerstate to ON"
                                                tdkTestObj.setResultStatus("SUCCESS")
                                        else:
                                            print "\n Error in getting the current power state"
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        print "\n Error in setting the power state to ON"
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print "\n Successfully completed {} iterations \n".format(max_powerstate_changes)
                                    print "Check container is running"
                                    tdkTestObj = obj.createTestStep('containerization_checkContainerRunningState')
                                    tdkTestObj.addParameter("callsign",LightningApp_details)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    actualresult = tdkTestObj.getResultDetails()
                                    if expectedResult in actualresult.upper():
                                        print "\n LightningApp is running in container mode without any issues"
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print "\n LightningApp is not running in container mode"
                                        tdkTestObj.setResultStatus("FAILURE")                    
                            else:
                                print "\n Error in setting up the power state to standby"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "\n Error in setting up the stand by mode as LIGHT_SLEEP"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "\n Error in launching LightningApp in container mode"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "\n Error in checking the container running state"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "\n Unable to launch LightningApp in container mode"
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
