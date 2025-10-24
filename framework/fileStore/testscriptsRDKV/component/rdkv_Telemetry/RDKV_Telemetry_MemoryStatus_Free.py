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
  <name>RDKV_Telemetry_MemoryStatus_Free</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>telemetry_deviceconfig_value</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To send device Memory_Free_Status report to telemetry server and verify output</synopsis>
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
    <test_case_id>rdkv_Telemetry_12</test_case_id>
    <test_objective>To send device Memory_Free_Status report to telemetry server and verify output</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator, RPI</test_setup>
    <pre_requisite>1. SSH_METHOD, SSH_USERNAME  and SSH_PASSWORD  must be configured in device config file
    2. Set dcm.properties with rdkcentral URL.
    3. Telemetry version
    4. Set Telemetry config URL.</pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch>1. Execute rbuscli command to set profile to report device Memory_Free_Status into server.
    2. Verify if rbuscli rules are set correctly.
    3. Verify if cJSON report is generated succcessfully from telemetry logs.
    4. Verify if report is sent to server successfully from telemetry logs.
    5. Verify if device Memory_Free_Status is updated in cJSON report. </automation_approch>
    <expected_output>1. rbuscli command must be executed successfully.
    2. rbuscli rules must be set successfully set with current profile.
    3. cJSON report must be present in telemetry logs.
    4. "Report Sent Successfully over HTTP : 200" must be present in telemetry logs.
    5. Device Memory_Free_Status must be successfully retrieved from cJSON report.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_Telemetry</test_stub_interface>
    <test_script>RDKV_Telemetry_MemoryStatus_Free</test_script>
    <skipped>No</skipped>
    <release_version>M141</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
import re
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_telemetry","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Telemetry_MemoryStatus_Free');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

obj.setLoadModuleStatus(result.upper());
expectedResult = "SUCCESS"

pre_requisite_set = False
if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('telemetry_deviceconfig_value')
    tdkTestObj.addParameter("basePath",obj.realpath)
    tdkTestObj.addParameter("configKey","Telemetry_Collector_URL")
    tdkTestObj.executeTestCase(expectedResult)
    details = tdkTestObj.getResultDetails()

    print("Details : ", details)
    details=details.replace("(","").replace(")","")
    details = details.split(",")
    Telemetry_Collector_URL = details[1]
    dummy_url = details[2]

    if "SUCCESS" in details:
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE");        

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('setPreRequisites');
    tdkTestObj.addParameter("Telemetry_Collector_URL",Telemetry_Collector_URL)
    tdkTestObj.executeTestCase(expectedResult);
    details = tdkTestObj.getResultDetails()
    if "SUCCESS" in details:
        print("PRE-REQUISITES SUCCESSFULLY SET")
        pre_requisite_set = True
        tdkTestObj.setResultStatus("SUCCESS");
    else:
        print("Unable to set PRE-REQUISITES successfully")
        tdkTestObj.setResultStatus("FAILURE");

if pre_requisite_set:
    param = "Device.DeviceInfo.MemoryStatus.Free"
    profile_name = "RDKV-Profile-9"
    description = "Report to check Memory Free status"
    name = "MemStatFree"

    tdkTestObj = obj.createTestStep('form_rbuscli_command');
    tdkTestObj.addParameter("param_name", param)
    tdkTestObj.addParameter("profile_name", profile_name)
    tdkTestObj.addParameter("description", description)
    tdkTestObj.addParameter("name", name)
    tdkTestObj.addParameter("Telemetry_Collector_URL",Telemetry_Collector_URL)
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    details = re.sub(r"\n", "", details)
    print("RBUS CLI COMMAND ", details)
    print("\n[TEST STEP 1] : Execute rbuscli command")
    tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT');
    command = str(details)
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    print (details)
    profile_set = False
    if "setvalues succeeded" in details:
        print("Successfully executed rbuscli command")
        print("\n[TEST STEP RESULT] : SUCCESS\n");
        tdkTestObj.setResultStatus("SUCCESS");

        print("\n[TEST STEP 2]: Verify if profile is successfully set in rbuscli rules")
        command = "rbuscli get Device.X_RDKCENTRAL-COM_T2.ReportProfiles"
        tdkTestObj.addParameter("command", command)
        tdkTestObj.executeTestCase("SUCCESS");
        details = tdkTestObj.getResultDetails()
        print (details)

        if profile_name in details:
            print("SUCCESS : Profile is successfully set in rbuscli rules")
            print("\n[TEST STEP RESULT] : SUCCESS")
            tdkTestObj.setResultStatus("SUCCESS");
            profile_set = True
        else:
            print("FAILURE : Profile is not set successfully in rbuscli rules")
            print("\n[TEST STEP RESULT] : FAILURE")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("\FAILURE observed during rbuscli command execution")
        print("\n[TEST STEP RESULT] : FAILURE\n")
        tdkTestObj.setResultStatus("FAILURE");

    if profile_set:
        print("Waiting for 60 seconds and collecting telemetry2_0 logs for current profile to get reflected\n")
        tdkTestObj = obj.createTestStep('telemetry_executeCmdInDUT')
        check_cmd = "sleep 60 ; journalctl -x -u telemetry2_0.service --since \"1 minute ago\""
        tdkTestObj.addParameter("command", check_cmd)
        tdkTestObj.executeTestCase("SUCCESS");
        details = tdkTestObj.getResultDetails()
        print (details)
        cJSON_line = ""
        HTTP_line = ""
        cJSON_found = False
        HTTP_found = False
        for line in details.splitlines():
            if "cJSON Report" in line:
                cJSON_line = line
                cJSON_found = True

            if "Report Sent Successfully over HTTP : 200" in line and not dummy_url:
                HTTP_line = line
                HTTP_found = True
            if dummy_url:
                HTTP_line = line
                HTTP_found = False

        print ("\n[TEST STEP 3]: Verify if cJSON Report is generated successfully")
        if not cJSON_found:
            print("FAILURE : Unable to find cJSON report")
            print("\n[TEST STEP RESULT] : FAILURE\n")
            tdkTestObj.setResultStatus("FAILURE")
        elif name not in cJSON_line:
            print("FAILURE : Unable to find device Memory_Free_Status in cJSON report")
            print("\n[TEST STEP RESULT] : FAILURE\n")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            print(cJSON_line)
            print("SUCCESS : cJSON report is generated successfully")
            print("\n[TEST STEP RESULT] : SUCCESS\n");
            tdkTestObj.setResultStatus("SUCCESS");
        print ("\n[TEST STEP 4] : Verify if report is sent successfully into server")
        if not HTTP_found and dummy_url:
            print("FAILURE : report not sent successfully to server")
            print("\n[TEST STEP RESULT] : FAILURE")
            print("EXPECTED RESULT AS DUMMY URL USED\n")
            tdkTestObj.setResultStatus("SUCCESS")
        elif not HTTP_found:
            print("FAILURE : report not sent successfully to server")
            print("\n[TEST STEP RESULT] : FAILURE\n")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            print(HTTP_line)
            print("SUCCESS : Report Sent Successfully")
            print("\n[TEST STEP RESULT] : SUCCESS\n");
            tdkTestObj.setResultStatus("SUCCESS");

        print ("\n[TEST STEP 5] : Verify if report is generated correctly")
        Memory_Free_Status = ""
        if cJSON_line and name in cJSON_line:
            try:
                match = re.search(r'(\{.*\})', cJSON_line)
                if match:
                    json_str = match.group(1)
                    data = json.loads(json_str)
                    Memory_Free_Status = data["Report"][0][name]
                    print("Memory_Free_Status:", Memory_Free_Status)
                    print("SUCCESS : Able to obtain  \"Memory_Free_Status\" from cJSON report")
                    print("\n[TEST STEP RESULT] : SUCCESS\n");
                    tdkTestObj.setResultStatus("SUCCESS");
            except:
                print("FAILURE : Unable to obtain \"Memory_Free_Status\" from cJSON report")
                print("\n[TEST STEP RESULT] : FAILURE\n")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("No JSON found in log line")
            print("Unable to get Memory_Free_Status from cJSON report")

obj.unloadModule("rdkv_telemetry");
