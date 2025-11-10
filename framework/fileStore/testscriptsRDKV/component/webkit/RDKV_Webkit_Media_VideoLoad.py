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
  <version>2</version>
  <name>RDKV_Webkit_Media_VideoLoad</name>
  <primitive_test_id/>
  <primitive_test_name>webkit_prerequisite</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test validates media loading behavior, preload settings, and network state transitions</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
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
    <test_case_id>Media_131</test_case_id>
    <test_objective>To verify that invalid and valid sources, preload metadata and none, and explicit load calls trigger correct networkState readyState and natural size while respecting user gesture restrictions</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Video Accelerators</test_setup>
    <pre_requisite>The device must be online with wpeframework service running.
All the variables in WebkitVariables.py must be filled.</pre_requisite>
    <api_or_interface_used>webkit</api_or_interface_used>
    <input_parameters>video-load-networkState.html, video-load-preload-metadata.html, video-load-preload-metadata-naturalsize.html, video-load-preload-none.html, video-load-readyState.html, video-load-require-user-gesture.html</input_parameters>
    <automation_approch>1. Launch the html test app in browser
2. Check for the required logs in wpeframework log or in the webinspect page</automation_approch>
    <expected_output>The video should transition to correct networkState and readyState, preload metadata should prevent buffering until playback, preload none should still load with explicit load, and user gesture requirements should block automatic loading</expected_output>
    <priority>High</priority>
    <test_stub_interface>webkit</test_stub_interface>
    <test_script>RDKV_Webkit_Media_VideoLoad</test_script>
    <skipped>No</skipped>
    <release_version>M143</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import WebkitVariables;
import webkitlib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("webkit","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Webkit_Media_VideoLoad');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
browser = WebkitVariables.browser_instance
webkit_test_url = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-networkState.html'
webkit_test_url2 = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-preload-metadata.html'
webkit_test_url3 = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-preload-metadata-naturalsize.html'
webkit_test_url4 = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-preload-none.html'
webkit_test_url5 = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-readyState.html'
webkit_test_url6 = obj.url+WebkitVariables.wpe_webkit_testcases_path+'/media/video-load-require-user-gesture.html'
browser_method = browser+".1.url"
log_check_method = WebkitVariables.log_check_method
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
        print("\n Script is directly taking the browser webinspect page console logs to validate the webkit")
        webinspect_logs = webkitlib.webkit_getLogs_webinspectpage(obj, test_url, browser)
        webinspect_logs = ', '.join(webinspect_logs)
    else:
        print("\n Script is using wpeframework log to validate the webkit test")
        webinspect_logs = webkitlib.webkit_getLogs_fromDevicelogs(obj, test_url, browser, grep_line)
    
    if webinspect_logs != "":
        process_webinspect_logs(log_filename, webinspect_logs,status_dict)
    else:
        print("FAILURE: Failed to fetch the logs from Html test App \n")
        tdkTestObj.setResultStatus("FAILURE")
        status_dict[log_filename] = "FAILURE"

if expectedResult in result.upper():
    print("\nCheck prerequisites")
    tdkTestObj = obj.createTestStep('webkit_prerequisite')
    tdkTestObj.addParameter("VariableList","browser_instance,webinspect_port,chromedriver_path,log_check_method,wpe_webkit_testcases_path")
    tdkTestObj.executeTestCase(expectedResult)
    pre_req_status=tdkTestObj.getResultDetails()
    if expectedResult in pre_req_status:
        print("SUCCESS: All the prerequisites are completed")
        tdkTestObj.setResultStatus("SUCCESS")

        print("\n Check current status of browser instance")
        tdkTestObj = obj.createTestStep('webkit_getPluginStatus')
        tdkTestObj.addParameter("plugin", browser)
        tdkTestObj.executeTestCase(expectedResult)
        browser_status = tdkTestObj.getResultDetails()
        result = tdkTestObj.getResult()
        if expectedResult in result:
            if browser_status == "resumed":
                print("SUCCESS: ", browser," is already in resumed state")
                tdkTestObj.setResultStatus("SUCCESS")

                print("Get the current URL loaded in ",browser)
                tdkTestObj = obj.createTestStep('webkit_getValue')
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
                tdkTestObj = obj.createTestStep('webkit_setPluginStatus')
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
                    obj.unloadModule("webkit");
                    exit()

            files_info = [
                {"tail_num": 3,"url": webkit_test_url},
                {"tail_num": 3,"url": webkit_test_url2},
                {"tail_num": 3,"url": webkit_test_url3},
                {"tail_num": 3,"url": webkit_test_url4},
                {"tail_num": 3,"url": webkit_test_url5},
                {"tail_num": 3,"url": webkit_test_url6}
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
                tdkTestObj = obj.createTestStep('webkit_setPluginStatus')
                tdkTestObj.addParameter("plugin",browser)
                tdkTestObj.addParameter("status","activate")
                tdkTestObj.addParameter("uri",current_url)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
            else:
                tdkTestObj = obj.createTestStep('webkit_setPluginStatus')
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

obj.unloadModule("webkit");

