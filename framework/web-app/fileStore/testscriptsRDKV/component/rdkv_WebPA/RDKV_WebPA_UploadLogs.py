##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
  <name>RDKV_WebPA_UploadLogs</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>webpa_deviceconfig_value</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To trigger and validate immediate log upload on the device using the WebPA server</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>3</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>rdkvWebPA_19</test_case_id>
    <test_objective>To trigger and validate immediate log upload on the device using the WebPA server</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>WEBPA_URL and Authoraization Key should be configured in the device config file</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <expected_output>RFC parmeter should return logs are uploaded in the device</expected_output>
    <priority>High</priority>
    <test_stub_interface></test_stub_interface>
    <test_script>RDKV_WebPA_UploadLogs</test_script>
    <skipped>No</skipped>
    <release_version>M139</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;

# Create TDK scripting object with rdkv_WebPAlib (used as utility module)
obj = tdklib.TDKScriptingLibrary("rdkv_WebPAlib","1",standAlone=True)

# Configure test case
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_WebPA_UploadLogs')

# Get the result of connection with test component
result = obj.getLoadModuleResult()
print("[MODULE LOAD] Status : %s" % result)

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

if "SUCCESS" in result.upper():

    # Define the parameter and value to test
    paramName = "Device.DeviceInfo.X_RDKCENTRAL-COM_xOpsDeviceMgmt.Logging.xOpsDMUploadLogsNow"
    testValue = "1"

    print("\n")
    tdkTestObj = obj.createTestStep('webpa_deviceconfig_value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","WEBPA_URL")
    tdkTestObj.addParameter("configKey2","AUTH_TOKEN")
    tdkTestObj.executeTestCase(expectedResult)
    detail = tdkTestObj.getResultDetails()

    ##remove special characters by replace command
    detail=detail.replace("(","").replace("'","").replace(")","")
    detail = detail.split(",")
    WEBPA_URL = detail[1]
    AUTH_TOKEN = detail[2]
    if "SUCCESS" in detail:
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n")
        tdkTestObj = obj.createTestStep('webpa_get')
        tdkTestObj.addParameter("paramName",paramName)
        tdkTestObj.addParameter("WEBPA_URL",WEBPA_URL)
        tdkTestObj.addParameter("AUTH_TOKEN",AUTH_TOKEN)
        tdkTestObj.executeTestCase(expectedResult)
        detail = tdkTestObj.getResultDetails()
        print("\nDETAILS : ", detail)

        detail=detail.replace("(","").replace("'","").replace(")","")
        detail = detail.split(",")
        original_value = detail[1]
        data_type = detail[2]
        if "SUCCESS" in detail:
            tdkTestObj.setResultStatus("SUCCESS")

            print("\n")
            tdkTestObj = obj.createTestStep('webpa_set')
            tdkTestObj.addParameter("paramName",paramName)
            tdkTestObj.addParameter("testValue",testValue)
            tdkTestObj.addParameter("WEBPA_URL",WEBPA_URL)
            tdkTestObj.addParameter("AUTH_TOKEN",AUTH_TOKEN)
            tdkTestObj.addParameter("dataType", data_type)
            tdkTestObj.executeTestCase(expectedResult)
            detail = tdkTestObj.getResultDetails()
            if "SUCCESS" in detail:
                tdkTestObj.setResultStatus("SUCCESS")

                print("\n")
                tdkTestObj = obj.createTestStep('webpa_validate_set')
                tdkTestObj.addParameter("paramName",paramName)
                tdkTestObj.addParameter("testValue",testValue)
                tdkTestObj.addParameter("WEBPA_URL",WEBPA_URL)
                tdkTestObj.addParameter("AUTH_TOKEN",AUTH_TOKEN)
                tdkTestObj.executeTestCase(expectedResult)
                detail = tdkTestObj.getResultDetails()
                if "SUCCESS" in detail:
                    tdkTestObj.setResultStatus("SUCCESS")
                    
                    print("\nNeed to revert the Values into actualvalue\n")
                    tdkTestObj = obj.createTestStep('webpa_set')
                    tdkTestObj.addParameter("paramName",paramName)
                    tdkTestObj.addParameter("testValue",original_value)
                    tdkTestObj.addParameter("WEBPA_URL",WEBPA_URL)
                    tdkTestObj.addParameter("AUTH_TOKEN",AUTH_TOKEN)
                    tdkTestObj.addParameter("dataType", data_type)
                    tdkTestObj.executeTestCase(expectedResult)
                    detail = tdkTestObj.getResultDetails()
                    if "SUCCESS" in detail:
                        tdkTestObj.setResultStatus("SUCCESS")

                        print("\n")
                        tdkTestObj = obj.createTestStep('webpa_get')
                        tdkTestObj.addParameter("paramName",paramName)
                        tdkTestObj.addParameter("WEBPA_URL",WEBPA_URL)
                        tdkTestObj.addParameter("AUTH_TOKEN",AUTH_TOKEN)
                        tdkTestObj.executeTestCase(expectedResult)
                        detail = tdkTestObj.getResultDetails()
                        if "SUCCESS" in detail:
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")

                else:
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("\nFAILURE : Module Loading Status Failure\n")
#unload module
obj.unloadModule('rdkv_WebPA');
