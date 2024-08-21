##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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
  <name>RDKV_Memcr_Check_AppHibernate_RFCParameter_Status</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>memcr_datamodelcheck</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Memcr feature validation</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>4</execution_time>
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
    <test_case_id>rdkvmemcr_08</test_case_id>
    <test_objective>Verify that the value of the apphibernate RFC parameter is always set to enabled</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator and RPI</test_setup>
    <pre_requisite>MEMCR_APPHIBERNATE_PARAMETER needs to be configured in the device configuration file</pre_requisite>
    <api_or_interface_used>Nil</api_or_interface_used>
    <input_parameters>MEMCR_APPHIBERNATE_PARAMETER</input_parameters>
    <automation_approch>1. Retrieve the AppHibernate RFC parameter from the device configuration 2. Check the status of the Memcr service 3. To ensure that the apphibernate RFC parameter is consistently set to enabled</automation_approch>
    <expected_output>All the steps should execute successfully</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>Nil</test_stub_interface>
    <test_script>RDKV_Memcr_Check_AppHibernate_RFCParameter_Status</test_script>
    <skipped>Nil</skipped>
    <release_version>M128</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvmemcr","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Memcr_Check_AppHibernate_RFCParameter_Status');

#Get the result of connection with test component and DUTV
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('memcr_getTR181Value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","MEMCR_APPHIBERNATE_PARAMETER")
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    if "SUCCESS" in result:
        tdkTestObj.setResultStatus("SUCCESS")
        ##remove special characters by replace command
        result = ast.literal_eval(result)
        tr181_parameter = list(result)[0].strip()

        tdkTestObj = obj.createTestStep('memcr_statuscheck')
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")

            tdkTestObj = obj.createTestStep('memcr_checkAppHibernateRFC')
            tdkTestObj.addParameter("datamodel",tr181_parameter)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if "SUCCESS" in result:
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")

obj.unloadModule("rdkvmemcr");
