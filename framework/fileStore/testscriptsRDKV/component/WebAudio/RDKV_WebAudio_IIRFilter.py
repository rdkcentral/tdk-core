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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>RDKV_WebAudio_IIRFilter</name>
  <primitive_test_id/>
  <primitive_test_name>webaudio_prerequisite</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Validates IIR filter behavior for various pole configurations including 1-pole, 2 real poles, 2 complex poles, repeated poles, and 4th-order cascaded filters</synopsis>
  <groups_id/>
  <execution_time>20</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>WebAudio_148</test_case_id>
    <test_objective>ensure filters produce non-zero outputs during active intervals, correctly decay to zero at the tail, and maintain numerical stability across all pole configurations including unstable cases</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Video Accelerators</test_setup>
    <pre_requisite>The device must be online with wpeframework service running.
All the variables in WebAudioVariables.py must be filled.</pre_requisite>
    <api_or_interface_used>WebAudio</api_or_interface_used>
    <input_parameters>iir-tail-time.html,iir-unstable.html,unstable-filter-warning.html</input_parameters>
    <automation_approch>1. Launch the html test app in browser
2. Check for the required logs in wpeframework log or in the webinspect page</automation_approch>
    <expected_output>Outputs are non-zero during active intervals and zero afterward, tail frames are within limits, explicit comparison with expected results passes, unstable filters produce warnings or non-finite values as expected, all assertions pass</expected_output>
    <priority>High</priority>
    <test_stub_interface>WebAudio</test_stub_interface>
    <test_script>RDKV_WebAudio_IIRFilter</test_script>
    <skipped>No</skipped>
    <release_version>M143</release_version>
    <remarks>None</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import WebAudioVariables;
import WebAudiolib

import time;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("WebAudio","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_WebAudio_IIRFilter');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
browser = WebAudioVariables.browser_instance
webaudio_test_url = obj.url+WebAudioVariables.wpe_webkit_testcases_path+'/IIRFilter/iir-tail-time.html'
webaudio_test_url2 = obj.url+WebAudioVariables.wpe_webkit_testcases_path+'/IIRFilter/iir-unstable.html'
webaudio_test_url3 = obj.url+WebAudioVariables.wpe_webkit_testcases_path+'/IIRFilter/unstable-filter-warning.html'
browser_method = browser+".1.url"
log_check_method = WebAudioVariables.log_check_method
current_url=''
webinspect_logs =''
status_dict = {}

# Function for processing the logs from the HTML Files
def process_webinspect_logs(log_filename, webinspect_logs,status_dict):
    print(f"Processing logs from file: {log_filename}")
    if "TDK_LOGS" in webinspect_logs and log_filename in webinspect_logs:
        print("\nSUCCESS: Successfully fetched the logs from the Html test App")
        tdkTestObj.setResultStatus("SUCCESS")
        if "TDK_LOGS : PASS" in webinspect_logs and "TDK_LOGS : FAIL" in webinspect_logs:
            print("Both PASS and FAIL patterns are present in the output.")
            print("\n", webinspect_logs, "\n")
            print("Test step result: FAILURE")
            tdkTestObj.setResultStatus("FAILURE")
            status_dict[log_filename] = "FAILURE"
        elif "TDK_LOGS : PASS" in webinspect_logs:
            print("Pattern TDK_LOGS : PASS is present in the output.")
            print("\n", webinspect_logs, "\n")
            print("Test step result: SUCCESS")
            tdkTestObj.setResultStatus("SUCCESS")
            status_dict[log_filename] = "SUCCESS"
        elif "TDK_LOGS : FAIL" in webinspect_logs:
            print("Pattern TDK_LOGS : FAIL is present in the output")
            print("\n", webinspect_logs, "\n")
            print("Test step result: FAILURE")
            tdkTestObj.setResultStatus("FAILURE")
            status_dict[log_filename] = "FAILURE"
    else:
        print("FAILURE: Failed to fetch the logs from Html test App \n")
        tdkTestObj.setResultStatus("FAILURE")
        status_dict[log_filename] = "FAILURE"

#Function for parsing the logs
def get_webinspect_logs(test_url, log_check_method, grep_line, log_filename,status_dict):
    if log_check_method == "WebinspectPageLogs":
        print("\n Script is directly taking the browser webinspect page console logs to validate the webaudio")
        webinspect_logs = WebAudiolib.webaudio_getLogs_webinspectpage(obj, test_url, browser)
        webinspect_logs = ', '.join(webinspect_logs)
    else:
        print("\n Script is using wpeframework log to validate the webaudio test")
        webinspect_logs = WebAudiolib.webaudio_getLogs_fromDevicelogs(obj, test_url, browser, grep_line)
    
    if webinspect_logs != "":
        process_webinspect_logs(log_filename, webinspect_logs,status_dict)
    else:
        print("FAILURE: Failed to fetch the logs from Html test App \n")
        tdkTestObj.setResultStatus("FAILURE")
        status_dict[log_filename] = "FAILURE"

if expectedResult in result.upper():
    print("\nCheck prerequisites")
    tdkTestObj = obj.createTestStep('webaudio_prerequisite')
    tdkTestObj.addParameter("VariableList","browser_instance,webinspect_port,chromedriver_path,log_check_method,wpe_webkit_testcases_path")
    tdkTestObj.executeTestCase(expectedResult)
    pre_req_status=tdkTestObj.getResultDetails()
    if expectedResult in pre_req_status:
        print("SUCCESS: All the prerequisites are completed")
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n Check current status of browser instance")
        tdkTestObj = obj.createTestStep('webaudio_getPluginStatus')
        tdkTestObj.addParameter("plugin", browser)
        tdkTestObj.executeTestCase(expectedResult)
        browser_status = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if expectedResult in result:
            if browser_status == "resumed":
                print("SUCCESS: ", browser," is already in resumed state")
                tdkTestObj.setResultStatus("SUCCESS")

                print("Get the current URL loaded in ",browser)
                tdkTestObj = obj.createTestStep('webaudio_getValue')
                tdkTestObj.addParameter("method",browser_method)
                tdkTestObj.executeTestCase(expectedResult)
                current_url=tdkTestObj.getResultDetails()
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print("SUCCESS: Current URL in ", browser, " is ",current_url)
                    tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("SUCCESS: ", browser," is in deactivated state")
                
                print ("\n Launching ", browser)
                tdkTestObj = obj.createTestStep('webaudio_setPluginStatus')
                tdkTestObj.addParameter("plugin",browser)
                tdkTestObj.addParameter("status","activate")
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if expectedResult in result:
                    print("SUCCESS: ", browser ," has launched successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    print("FAILURE : Failed to launch ", browser, " in device \n")
                    tdkTestObj.setResultStatus("FAILURE")
                    obj.unloadModule("webaudio");
                    exit()

            files_info = [
                {"tail_num": 5,"url": webaudio_test_url},
                {"tail_num": 5,"url": webaudio_test_url2},
                {"tail_num": 5,"url": webaudio_test_url3}
            ]

            for file_info in files_info:
                filename =file_info["url"].split("/")[-1]
                tail_num = file_info["tail_num"]
                log_filename = filename.replace(".html","")
                url = file_info["url"]
                print(f"Processing {filename} file")
                grep_line = f"{filename} | tail -{tail_num} | tr -d '\\n'"
                try:
                    get_webinspect_logs(url, log_check_method, grep_line, log_filename,status_dict)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    status_dict[log_filename] = "FAILURE"
       
            print("\n Revert everything before exiting the script")
            if current_url !='':
                tdkTestObj = obj.createTestStep('webaudio_setPluginStatus')
                tdkTestObj.addParameter("plugin",browser)
                tdkTestObj.addParameter("status","activate")
                tdkTestObj.addParameter("uri",current_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
            else:
                tdkTestObj = obj.createTestStep('webaudio_setPluginStatus')
                tdkTestObj.addParameter("plugin",browser)
                tdkTestObj.addParameter("status","deactivate")
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print("SUCCESS: Successfully reverted everything")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("FAILURE: Failed to revert the status of ", browser)

        else:
            print("FAILURE: Failed to get the status of ", browser)
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Pre-requsites are not met")
        tdkTestObj.setResultStatus("FAILURE")

print("############## Execution Summary #######################")
for log_filename, status in status_dict.items():
    print(f"{log_filename}: {status}")
    
obj.unloadModule("WebAudio");

