##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2022 RDK Management
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
  <name>RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations of mp4 video.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>6</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_119</test_case_id>
    <test_objective>This script is to get the performance of the Lightning application by calculating the time taken for play and pause operations of mp4 video.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1. As a pre requisite disable all other plugins and enable webkitinstance plugin.
2. Set the application URL
3. Play and pause the video from the application
3. Get the time taken to play/pause the video</automation_approch>
    <expected_output>The video must play and pause within expected range of ms.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4</test_script>
    <skipped>No</skipped>
    <release_version>M99</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_TimeTo_Video_PlayPause_MP4');

webkit_console_socket = None

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
    setOperation("pause",10)
    setOperation("play",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
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
    status = "SUCCESS"
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
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
        # rdkv_performancelib.setPS_value(video_test_urls[0])
            app_bundle_name=MediaValidationVariables.unified_player_app_download_url.split("/")[-1]
            print(f"\nApp bundle name: {app_bundle_name}")
            app_name = app_bundle_name.split("+")[0]
            print(f"\nApp name: {app_name}")
            app_download_url = MediaValidationVariables.unified_player_app_download_url.split(app_bundle_name)[0]
            print("app_download_url", app_download_url)
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
            if status == "SUCCESS":
                if logging_method == "REST_API":
                    expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingRestAPI(obj);
                    evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                elif logging_method == "WEB_INSPECT":
                    webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
                    if current_url != None and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingWebInspect(obj,webkit_console_socket);
                        evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                if ("SUCCESS" in test_result) and (not any(value == "" for value in evt_list)):
                    print("\n Validating resource usage:")
                    tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                    tdkTestObj.executeTestCase(expectedResult)
                    resource_usage = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if expectedResult in result and resource_usage != "ERROR":
                        print("\n Resource usage is within the expected limit")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("\n Error while validating resource usage")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("\n Error occured during video playback")
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
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print("\n Failed to load module")
