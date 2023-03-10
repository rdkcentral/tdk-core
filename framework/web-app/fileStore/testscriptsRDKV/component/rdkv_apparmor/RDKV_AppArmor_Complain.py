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
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_AppArmor_Complain</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkvapparmor_executeInDUT</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To test if apparmor is in complain mode for the given profiles</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <test_case_id>RDKV_APPARMOR_02</test_case_id>
    <test_objective>To test if apparmor is in complain mode for the given profiles</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI</test_setup>
    <pre_requisite>1. Configure the values AppArmor_Profiles available in fileStore/ApparmorConfig.config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters>AppArmor_Profiles</input_parameters>
    <automation_approch>
1. Check if AppArmor is supported in device
2. Complain AppArmor to the given profiles using tr181 command
3. Validate if the AppArmor is complain to the given profiles</automation_approch>
    <expected_output>AppArmor should be in complained mode in the given profiles</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_apparmor</test_stub_interface>
    <test_script>RDKV_AppArmor_Complain</test_script>
    <skipped>No</skipped>
    <release_version>M109</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
from rdkv_apparmorlib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_apparmor","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_AppArmor_Complain');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print "[LIB LOAD STATUS]  :  %s" %result;
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print "Retrieving Configuration values from config file......."
    configKeyList = ["AppArmor_Profiles", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    configValues = obtainCredentials(obj,configKeyList)
    AppArmor_Profiles = configValues["AppArmor_Profiles"]
    credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
    print "\nTo Ensure Apparmor service is running"
    command = 'systemctl status apparmor.service | grep active | grep -v inactive'
    print "COMMAND : %s" %(command)

    #Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
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
        print "Apparmor is running %s" %(output)
        
        #To check Apparmor is enabled
        command = 'aa-enabled'
        print "COMMAND : %s" %(command)
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
        #Add the parameters to ssh to the DUT and execute the command
        tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
        tdkTestObj.addParameter("credentials", credentials);
        tdkTestObj.addParameter("command", command);

        #Execute the test case in DUT
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult()

        #Get the result of execution
        output = tdkTestObj.getResultDetails();
        if 'Yes' in output and expectedResult in result:
            print "Apparmor is enabled"
            
            #Set Apparmor profile mode into complain mode with tr181 command
            print (AppArmor_Profiles)
            AppArmor_Profiles=AppArmor_Profiles.split(',')
            count = len(AppArmor_Profiles)
            print(count)
            for i in range(count):
                command = 'tr181 -s -v "'+AppArmor_Profiles[i]+':complain" Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.NonRootSupport.ApparmorBlocklist'
                print "COMMAND : %s" %(command)
                #Primitive test case which associated to this Script
                tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
                #Add the parameters to ssh to the DUT and execute the command
                tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                tdkTestObj.addParameter("credentials", credentials);
                tdkTestObj.addParameter("command", command);

                #Execute the test case in DUT
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
            if expectedResult in result:
                print "tr181 is set"
                #Reboot the device
                tdkTestObj = obj.createTestStep('rdkvapparmor_rebootDevice')
                tdkTestObj.addParameter("waitTime",50)
                #Execute the test case in DUT
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print "Device is rebooted"
                    
                    #check status from /opt/secure/Apparmor_blocklist
                    command = 'cat /opt/secure/Apparmor_blocklist'
                    print "COMMAND : %s" %(command)
                    #Primitive test case which associated to this Script
                    tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
                    #Add the parameters to ssh to the DUT and execute the command
                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                    tdkTestObj.addParameter("credentials", credentials);
                    tdkTestObj.addParameter("command", command);

                    #Execute the test case in DUT
                    tdkTestObj.executeTestCase(expectedResult);
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    for i in range(count):
                        if ''+AppArmor_Profiles[i]+':complain' in output:
                            complain = "Success"
                        else:
                            complain = "Failure"
                    if complain == "Success":
                        print "Status is valid in Apparmor_blocklist"

                        #To check if profiles are loaded into kernel
                        command = 'cat /sys/kernel/security/apparmor/profiles'
                        print "COMMAND : %s" %(command)
                        #Primitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
                        #Add the parameters to ssh to the DUT and execute the command
                        tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                        tdkTestObj.addParameter("credentials", credentials);
                        tdkTestObj.addParameter("command", command);

                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult()
                        output = tdkTestObj.getResultDetails()
                        for i in range(count):
                            if ''+AppArmor_Profiles[i]+' (complain)' in output:
                                kernel = "Success"
                            else:
                                kernel = "Failure"
                        if kernel == "Success":
                            print "apparmor profiles are loaded in to kernel space"

                            #Check for AppArmor initialization logs
                            command = 'cat /opt/logs/startup_stdout_log.txt | grep "Starting AppArmor initialization"'
                            print "COMMAND : %s" %(command)
                            #Primitive test case which associated to this Script
                            tdkTestObj = obj.createTestStep('rdkvapparmor_executeInDUT');
                            #Add the parameters to ssh to the DUT and execute the command
                            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"]);
                            tdkTestObj.addParameter("credentials", credentials);
                            tdkTestObj.addParameter("command", command);

                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedResult);
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()
                            if "Starting AppArmor initialization" in output:
                                print "AppArmor initialized successfully"
                            else:
                                print "Unable to get the required logs"
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print "apparmor profiles are not loaded in to kernel space"
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print "Status is invalid in Apparmor_blocklist"
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print "Device is not rebooted"
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print "tr181 is not set"
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print "Apparmor is not enabled"
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print "AppArmor is not supported"
        tdkTestObj.setResultStatus("FAILURE")

    #Unload the module
    obj.unloadModule("rdkv_apparmor");
else:
    #Set load module status
    obj.setLoadModuleStatus("FAILURE");
    print "FAILURE: Failed to load module"

