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
  <version>5</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_Functional_TimeTo_GetKeys</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The objective of this test is to validate the time taken to get Keys from RDK Shell</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>7</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_108</test_case_id>
    <test_objective>The objective of this test is to validate the time taken to get Keys from RDK Shell</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>1. Enable WebKitInstance plugin.
2. Set URL for keytest in WebKitInstance.
3. In a loop of minimum 15 iterations send a key using generatekey method of RDKShell to the system.
4. Validate the key press using logs from wpeframework logs.
5. Validate the time taken to get keys from RDK Shell.
6. Revert plugins status after completing the test</automation_approch>
    <expected_output>The time taken to get keys from RDK Shell must be within the expected limit</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_TimeTo_GetKeys</test_script>
    <skipped>No</skipped>
    <release_version>M98</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from StabilityTestUtility import *
from web_socket_util import *
from rdkv_performancelib import *
import ast
import PerformanceTestVariables
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_TimeTo_GetKeys');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if expectedResult in result and ssh_param_dict != {}:
        print("\nPre conditions for the test are set successfully")
        app_bundle_name=PerformanceTestVariables.keytest_bundle
        app_name="com.rdkcentral.keytest"
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name)
        if status == "SUCCESS":
            end_get_key_time = ""
            total_time = 0
            count = 0
            print(f"Getting the app instance id of {app_name}")
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method","org.rdk.AppManager.getLoadedApps")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            status = tdkTestObj.getResult()
            if status == expectedResult and app_name in result:
                appinstanceid=""
                result = ast.literal_eval(result)
                for item in result:
                    if isinstance(item, dict) and item.get("appId") == app_name:
                        appinstanceid = item.get("appInstanceId")
                for i in range(0,15):
                    params = '{"client":"'+appinstanceid + '","keys":"{\\"keys\\":[{\\"keyCode\\":50,\\"modifiers\\":[],\\"delay\\":0}]}"}'
                    # params = '{"keys":[ {"keyCode": 50,"modifiers": [],"delay":1.0,"client":'+appinstanceid+'}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKWindowManager.generateKey")
                    tdkTestObj.addParameter("value",params)
                    start_get_key_time = str(datetime.now()).split()[1]
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(10)
                        print("checking for Keycode log")
                        command = 'cat /opt/logs/dacapp.log | grep -inr KeyCode | tail -1'
                        print("COMMAND : %s" %(command))
                        #Primitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                        #Add the parameters to ssh to the DUT and execute the command
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                        tdkTestObj.addParameter("command",command)
                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult);
                        result = tdkTestObj.getResult()
                        output = tdkTestObj.getResultDetails()
                        output = output[output.find('\n'):]
                        if "KeyCode" in output:
                            print("\n Keycode logs are present in logs")
                            log_line = output.split('\n')[1]
                            end_get_key_time = getTimeStampFromString(log_line)
                            if result in expectedResult and end_get_key_time != {}:
                                print("\n key codes are received successfully \n")
                                print("end time",end_get_key_time)
                                start_get_key_time_in_millisec = getTimeInMilliSec(start_get_key_time)
                                end_get_key_time_in_millisec = getTimeInMilliSec(end_get_key_time)
                                time_taken = end_get_key_time_in_millisec - start_get_key_time_in_millisec
                                print("time taken",time_taken)
                                total_time = total_time + time_taken
                                count = count + 1
                            else:
                                print("\n Error in getting the keycode time")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print("\n Keycode logs are not present in logs")
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        print("\nError while executing generate key method\n")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
            else:
                print(f"Failed to get the app instanceid for {app_name}")
                tdkTestObj.setResultStatus("FAILURE")
            if end_get_key_time:
                conf_file,file_status = getConfigFileName(obj.realpath)
                config_status,get_key_threshold = getDeviceConfigKeyValue(conf_file,"GET_KEY_THRESHOLD_VALUE")
                Summ_list.append('GET_KEY_THRESHOLD_VALUE :{}ms'.format(get_key_threshold))
                if count == 15:
                    avg_get_key_time = total_time/15
                else:
                    print("\n 15 Iterations for receiving the keys is not successful")
                    tdkTestObj.setResultStatus("FAILURE")
                print("\n Time taken to get keys : {}(ms)".format(avg_get_key_time))
                Summ_list.append('Time taken to get keys :{}ms'.format(avg_get_key_time))
                print("\n Threshold value to get keys: {}(ms)".format(get_key_threshold))
                print("\n Validate the time:")
                if int(avg_get_key_time) < int(get_key_threshold):
                    print("\n Time taken for getting the keys is within the expected range \n")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("\n Time taken for getting keys is not within the expected range \n")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("All keys not received successfully")
                tdkTestObj.setResultStatus("FAILURE")
            print("\n Terminating the app")
            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id",app_name)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Unable to terminate the app")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to install or launch app")
    else:
        print("Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE");
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
