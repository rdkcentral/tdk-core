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
  <name>RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The Objective of the test is to check for any crashes for the WebkitBrowser application by keeping the web inspect port open for play and pause operations of mp4 video</synopsis>
  <groups_id/>
  <execution_time>100</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_163</test_case_id>
    <test_objective>The Objective of the test is to check for any crashes for the WebkitBrowser application by keeping the web inspect port open for play and pause operations of mp4 video</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. As a prerequisite disable all other plugins and enable web kit instance plugin.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1.Open WebkitBrowser app web inspect port
2. Set the application URL in WebkitBrowser app
3. Play and pause the video from the application
4.Check for any crashes during playback</automation_approch>
    <expected_output>video playback should happen with out crash</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect</test_script>
    <skipped>No</skipped>
    <release_version>M132</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from web_socket_util import *
import PerformanceTestVariables
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_WebKitBrowser_Video_Playback_Without_Crash_WithWebinspect');
deviceIP =str(ip)
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
webkit_console_socket = None
driver = None
crash_Validation = False
crash_iteration = -1
memory_usage = []
result_dict_list =[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    conf_file, status = get_configfile_name(obj);
    result, logging_method = getDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
    setDeviceConfigFile(conf_file)
    videoURL  = MediaValidationVariables.video_src_url_mp4
    videoURL_type = "mp4"
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    setURLArgument("tmUrl",str(obj.url)+"/")  
    test_duration_in_seconds = 60
    setOperation("close",test_duration_in_seconds)    
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("options","looptest")
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    video_test_urls = []
    players_list = str(MediaValidationVariables.codec_mp4).split(",")
    print("SELECTED PLAYERS: ", players_list)
    # Getting the complete test app URL
    video_test_urls = getTestURLs(players_list,appArguments)
    print("\n Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"    
    
    plugins_list = ["DeviceInfo","org.rdk.PersistentStore"]
    plugin_status_needed = {"org.rdk.PersistentStore":"activated","DeviceInfo":"activated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\n Error while getting plugin status")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print("\n Pre conditions for the test are set successfully");
        time.sleep(10)
        tdkTestObj = obj.createTestStep('setPS_value');
        tdkTestObj.addParameter("video_test_url",video_test_urls[0]);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print("\n Video test URL is set successfully");
            app_bundle_name=MediaValidationVariables.unified_player_app_download_url.split("/")[-1]
            print(f"\nApp bundle name: {app_bundle_name}")
            app_name = app_bundle_name.split("+")[0]
            print(f"\nApp name: {app_name}")
            app_download_url = MediaValidationVariables.unified_player_app_download_url.split(app_bundle_name)[0]
            print("app_download_url", app_download_url)
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
            if status == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
                print("\n App is installed and launched successfully")
                tdkTestObj.setResultStatus("SUCCESS")

                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())

                webinspect_launched = False
                webinspect_port = None
                webinspectURL = None

                try:
                    webinspect_port = str(get_webinspect_port()).strip()
                except Exception as error:
                    print(f"Unable to get WebInspect port: {error}")
                    tdkTestObj.setResultStatus("FAILURE")

                if webinspect_port and webinspect_port.lower() not in ["none", "null", "error", "exception"]:
                    webinspectURL = 'http://' + deviceIP + ':' + webinspect_port + '/Main.html?ws=' + deviceIP + ':' + webinspect_port + '/socket/1/1/WebPage'
                    print(webinspectURL)

                    try:
                        driver = openChromeBrowser(webinspectURL)
                        if driver != "EXCEPTION OCCURRED":
                            time.sleep(20)
                            print("Webinspect page in device launched successfully")
                            webinspect_launched = True
                            webkit_console_socket = driver
                        else:
                            raise RuntimeError("failed to launch webinspect page")

                    except Exception as error:
                        print("Got exception while opening the browser")
                        tdkTestObj.setResultStatus("FAILURE")
                        print(error)
                else:
                    print(f"Invalid WebInspect port received: {webinspect_port}")
                    tdkTestObj.setResultStatus("FAILURE")

                if webinspect_launched:
                    test_time_in_sec = 60
                    test_time_in_millisec = test_time_in_sec * 1000
                    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                    iteration = 0
                    if ssh_param_dict != {}:
                        print("Checking for any crash during video playback\n")
                        command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                        print("COMMAND : %s" %(command))
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                        #Add the parameters to ssh to the DUT and execute the command
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                        tdkTestObj.addParameter("command",command)
                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult)
                        output = tdkTestObj.getResultDetails()
                        output = tdkTestObj.getResultDetails().replace(r'\n', '\n')
                        output = output[output.find('\n')]
                        if ("crash" or "CRASH" or "Crash") in output:
                            print("\nCrash observed during Video playback\n")
                            print("\n Validate the status of the app to confirm the crash:\n")
                            app_ids = rdkservice_get_loaded_apps()
                            if app_name in app_ids:
                                print(f"\n Crash is not observed and {app_name} is still running")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"Crash is observed during video playback and {app_name} is not listed as loadedapps")
                                crash_Validation = True
                                obj.unloadModule("rdkv_performance")
                        else:
                            print(f"No crash observed during video playback \n")
                            tdkTestObj.setResultStatus("SUCCESS")
                    if logging_method == "REST_API":
                        expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingRestAPI(obj)
                        evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                    elif logging_method == "WEB_INSPECT":
                        if current_url != None and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS")
                            expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingWebInspect(obj,webkit_console_socket)
                            evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                    if ("SUCCESS" in test_result) and crash_Validation == False:
                        print("\nVideo playback is happening successfully with out any crash")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("\n Error occured during video playback")
                else:
                    print("WebInspect page was not launched. Skipping playback and crash validation")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Unable to set the video url value in PersistanceStorage")
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
        print("\n Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print("\n Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    if driver and webinspect_launched :
       print("################TEST SUMMARY################\n")
       if crash_Validation == False:
          print("No crash is observed during the execution\n")
       else:
           print(f"Crash observed during execution \n")
       driver.quit()
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("\n Failed to load module")
