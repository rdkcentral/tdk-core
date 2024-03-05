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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>2</version>
  <name>RDKV_CERT_WebAudio_AudioPlayback</name>
  <primitive_test_id/>
  <primitive_test_name>webaudio_prerequisite</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>To test if the audio playback is working fine in device browser</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RDKTV</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>WebAudio_04</test_case_id>
    <test_objective>To test if the audio playback is working fine in device browser</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Video Accelerators</test_setup>
    <pre_requisite>The device must be online with wpeframework service running.
All the variables in WebAudioVariables.py must be filled.</pre_requisite>
    <api_or_interface_used>WebAudio</api_or_interface_used>
    <input_parameters>AudioPlaybackTest.html</input_parameters>
    <automation_approch>1. Launch the html test app in browser
2. Check for the required logs in wpeframework log or in the webinspect page</automation_approch>
    <expected_output>The browser should play the given content using WebAudio apis</expected_output>
    <priority>High</priority>
    <test_stub_interface>WebAudio</test_stub_interface>
    <test_script>RDKV_CERT_WebAudio_AudioPlayback</test_script>
    <skipped>No</skipped>
    <release_version>M122</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags/>
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
obj.configureTestCase(ip,port,'RDKV_CERT_WebAudio_AudioPlayback');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
browser = WebAudioVariables.browser_instance
stream_url= WebAudioVariables.mp3_audio_url
webaudio_test_url = obj.url+"/fileStore/lightning-apps/webaudio/AudioPlaybackTest.html?streamUrl="+stream_url
browser_method = browser+".1.url"
log_check_method = WebAudioVariables.log_check_method
current_url=''

if expectedResult in result.upper():
    print("\nCheck prerequisites")
    tdkTestObj = obj.createTestStep('webaudio_prerequisite')
    tdkTestObj.addParameter("VariableList","browser_instance,webinspect_port,chromedriver_path,log_check_method,mp3_audio_url")
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
                    obj.unloadModule("webaudio_test");
                    exit()
            if log_check_method == "WebinspectPageLogs":
                print("\n Script is directly taking the browser webinspect page console logs to validate the webaudio")
                webinspect_logs=WebAudiolib.webaudio_getLogs_webinspectpage(obj,webaudio_test_url,browser,["9","13"])
                webinspect_logs = ', '.join(webinspect_logs)
            else:
                print("\n Script is using wpeframework log to validate the webaudio test")
                grep_line="'AudioPlaybackTest' | tail -4 | tr -d '\\n'"
                webinspect_logs = WebAudiolib.webaudio_getLogs_fromDevicelogs(obj,webaudio_test_url,browser,grep_line,["9","13"])
            if webinspect_logs != "":
                if "TDK_LOGS" in webinspect_logs and "AudioPlaybackTest" in webinspect_logs:
                    print("\n ", webinspect_logs)
                    print("\nSUCCESS: Successfully fetched the logs from the Html test App")
                    tdkTestObj.setResultStatus("SUCCESS")

                    success_logs=["AudioContext created","AudioContext created successfully","Audio file loaded successfully","Audio playback started"]
                    for log in success_logs:
                        if log in webinspect_logs: 
                            print("SUCCESS : ",log)
                            result = "SUCCESS"
                        else:
                            print("FAILURE : Failed to get the log '", log, "' from the test")
                            result = "FAILURE"
                            break;
                    if expectedResult in result:
                        print("\nSUCCESS: Successfully played the audio in the device browser\n")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("\nFAILURE: Failed to playback the audio in the device browser\n")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE: Failed to fetch the logs from Html test App \n")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("FAILURE: The logs from the browser came as empty")
                tdkTestObj.setResultStatus("FAILURE")
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
obj.unloadModule("WebAudio");
