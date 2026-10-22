##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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

import json
import re
import shlex

import tdklib;
from web_socket_util import *
import PerformanceTestVariables
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *
from urllib.parse import unquote, urlparse

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_HTML_Successive_Playback');

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
    
    appURL    = MediaValidationVariables.html_video_test_app_url
    videoURL  = MediaValidationVariables.video_src_url_mp4
    video_codec = "MP4"
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    setURLArgument("tmUrl",str(obj.url)+"/")
    setOperation("close",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    appArguments = getURLArguments()
    # Getting the complete test app URL for stream
    playback_iterations = PerformanceTestVariables.Succesive_playback_iterations
    video_test_urls = []
    for i in range(playback_iterations):
        video_test_url = getTestURL(appURL,appArguments)
        video_test_urls.append(video_test_url)

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
        #set the video test url to PersistanceStorage
        tdkTestObj = obj.createTestStep('setPS_value');
        tdkTestObj.addParameter("video_test_url",video_test_urls);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print("\n Video test URL is set successfully");
            app_bundle_name=MediaValidationVariables.html_player_app_download_url.split("/")[-1]
            print(f"\nApp bundle name: {app_bundle_name}")
            app_name = app_bundle_name.split("+")[0]
            print(f"\nApp name: {app_name}")
            app_download_url = MediaValidationVariables.html_player_app_download_url.split(app_bundle_name)[0]
            print("app_download_url", app_download_url)
            status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
            if status == "SUCCESS":
                if logging_method == "REST_API":
                    expected_streams = len(video_test_urls)
                    test_result,play_event_count,stream_results,playback_status = testSuccessivePlayback(obj,expected_streams)
                    if playback_status == "SUCCESS":
                        tdkTestObj.setResultStatus("SUCCESS")
                        # print("\n Observed play event: {}".format(str(observed_play_evt).strip()))
                        print("\n Test result: {}".format(str(test_result).strip()))
                        for stream_num in sorted(stream_results):
                            Summ_list.append("Stream {} playback result :{}".format(stream_num,stream_results[stream_num]))
                        Summ_list.append("Codec used :{}".format(video_codec))
                        Summ_list.append("Expected successive streams :{}".format(expected_streams))
                        Summ_list.append("Play events observed :{}".format(play_event_count))
                        successful_streams = list(stream_results.values()).count("SUCCESS")
                        Summ_list.append("Successful streams :{}".format(successful_streams))
                        Summ_list.append("Failed streams :{}".format(expected_streams - successful_streams))
                        # Validate resource usage after the successive playback
                        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                        tdkTestObj.executeTestCase(expectedResult)
                        resource_usage = tdkTestObj.getResultDetails()
                        if expectedResult in tdkTestObj.getResult() and resource_usage != "ERROR":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("\n Resource usage validated successfully and within expected limits")
                            resource_values = resource_usage.split(',')
                            Summ_list.append("CPU load :{}".format(resource_values[0]))
                            Summ_list.append("Memory usage :{}".format(resource_values[1]))
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("\n Resource usage validation failed")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("\n Successive playback is not happening")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("\n Error occured during video playback")

                print("\n Terminating the app")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id",app_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    print("App terminated successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to terminate the app")  
                      
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Failed to install or launch app")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Unable to set the video URL value in PersistentStorage")
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
