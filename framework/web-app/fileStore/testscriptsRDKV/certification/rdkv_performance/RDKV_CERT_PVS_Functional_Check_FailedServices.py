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
  <name>RDKV_CERT_PVS_Functional_Check_FailedServices</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this script is to find the list of failed services in the device.</synopsis>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_139</test_case_id>
    <test_objective>The objective of this script is to find the list of failed services in the device.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>None</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. SSH the device
2. Run the command to check for the failed services.
3. Validate the number of failed services and print the services list. </automation_approch>
    <expected_output>The number of failed services and the list of services should be printed. </expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_Check_FailedServices</test_script>
    <skipped>No</skipped>
    <release_version>M111</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import json
from rdkv_performancelib import *
from StabilityTestUtility import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_Check_FailedServices');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        #command to check the failed services in the device
        command = 'systemctl --failed'
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        output = tdkTestObj.getResultDetails()
        if output != "EXCEPTION" and expectedResult in result:
            #command to get the number of failed services
            command = 'systemctl --failed | grep "loaded units listed"'
            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
            tdkTestObj.addParameter("command",command)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            output = tdkTestObj.getResultDetails()
            if output != "EXCEPTION" and expectedResult in result:
                print("Validate failed services:")
                services_count =int(output.split('\n')[1].split(' ')[0])
                #command to get the list of failed services
                command = 'systemctl --failed | cut -d " " -f2 | grep "service"'
                tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                tdkTestObj.addParameter("command",command)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                output = tdkTestObj.getResultDetails()
                services_list = output.replace(command,"")
                if services_count < 10:
                    print("The list of failed services are: {}".format(services_list))
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("The number of failed services in the device are: {} \n The list of failed services are: {} \n".format(services_count,services_list))
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Error in validating the failed services in the device")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Error occurred during SSH, please check ssh details in configuration file")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("Please configure the SSH details in configuration file")
        obj.setLoadModuleStatus("FAILURE")
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
