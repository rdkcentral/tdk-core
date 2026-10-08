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
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_TimeTo_Video_Playback_4K_HLS');

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
    videoURL  = MediaValidationVariables.video_src_url_4k_hls
    videoURL_type = "hls"
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
    players_list = str(MediaValidationVariables.codec_hls_hevc).split(",")
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
        #set the video test url to PersistanceStorage
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
                if logging_method == "REST_API":
                    load_video, playback_started = getPlaybackTimestamps(obj, app_name)
                    if load_video and playback_started:
                        load_time = re.sub(r"(\d{2}:\d{2}:\d{2}):(\d+)", r"\1.\2", load_video)
                        playback_time = re.sub(r"(\d{2}:\d{2}:\d{2}):(\d+)", r"\1.\2", playback_started)
                        load_time_ms = getTimeInMilliSec(load_time if "." in load_time else load_time + ".000")
                        playback_time_ms = getTimeInMilliSec(playback_time if "." in playback_time else playback_time + ".000")
                        elapsed_time_ms = playback_time_ms - load_time_ms
                        if elapsed_time_ms < 0:
                            elapsed_time_ms += 24 * 60 * 60 * 1000
                        print("\nTime from WPE load committed to Video Player Playing: {} ms".format(elapsed_time_ms))
                        result1, video_playback_threshold_value = getDeviceConfigKeyValue(conf_file,"VIDEO_PLAYBACK_THRESHOLD_VALUE")
                        Summ_list.append('VIDEO_PLAYBACK_THRESHOLD_VALUE :{}ms'.format(video_playback_threshold_value))
                        result2, offset = getDeviceConfigKeyValue(conf_file,"THRESHOLD_OFFSET")
                        Summ_list.append('THRESHOLD_OFFSET :{}ms'.format(offset))
                        Summ_list.append('WPE load committed at :{}'.format(load_video))
                        Summ_list.append('Video Player Playing at :{}'.format(playback_started))
                        Summ_list.append('Time to video playback :{}ms'.format(elapsed_time_ms))
                        if all(value != "" for value in (video_playback_threshold_value,offset)):
                            print("\n The threshold value for time to video playback: {} ms".format(video_playback_threshold_value))
                            if 0 < int(elapsed_time_ms) < (int(video_playback_threshold_value) + int(offset)):
                                print("\n Time to video playback is within the expected limit \n")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("\n Time to video playback is not within the expected limit \n")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("\n Failed to get the threshold value for time to video playback from config file \n")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Failed to capture WPE load committed or Video Player Playing timestamp")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("\n Error occured during video playback")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Failed to install or launch app")
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
