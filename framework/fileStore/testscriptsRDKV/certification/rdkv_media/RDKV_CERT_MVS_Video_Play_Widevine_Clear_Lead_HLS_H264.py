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


# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_Play_Widevine_Clear_Lead_HLS_H264')

webkit_console_socket = None
expectedResult = "SUCCESS"

# ------------------------------------------------------------------------------
# LOAD MODULE
# ------------------------------------------------------------------------------
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  : ", result)

if expectedResult not in result.upper():
    obj.setLoadModuleStatus("FAILURE")
    raise SystemExit

# ------------------------------------------------------------------------------
# PRE-CONDITIONS
# ------------------------------------------------------------------------------
print("\nCheck Pre conditions...")
tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites')
tdkTestObj.executeTestCase(expectedResult)

drm_pre_requisite_status = checkDRMSupported(obj, "Widevine")

if drm_pre_requisite_status == "TRUE":
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,MediaValidationVariables.unified_player_app_id,MediaValidationVariables.unified_player_app_download_url)
elif drm_pre_requisite_status == "NA":
    pre_requisite_status = "NA"
else:
    pre_requisite_status = "FAILURE"

if pre_requisite_status != "SUCCESS":
    if pre_requisite_status == "NA":
        obj.setAsNotApplicable()
    else:
        tdkTestObj.setResultStatus("FAILURE")
    obj.unloadModule("rdkv_media")
    raise SystemExit

tdkTestObj.setResultStatus("SUCCESS")
print("Pre conditions for the test are set successfully")

# ------------------------------------------------------------------------------
# SET TEST URL
# ------------------------------------------------------------------------------
print("\nSet Lightning video player test app url...")

conf_file, result = getDeviceConfigFile(obj.realpath)
setDeviceConfigFile(conf_file)

videoURL = MediaValidationVariables.video_src_url_widevine_clear_lead_hls_h264_aac

setOperation("close", "150")
operations = getOperations()

setURLArgument("url", videoURL)
setURLArgument("operations", operations)
setURLArgument("autotest", "true")
setURLArgument("drmconfigs", MediaValidationVariables.video_src_url_widevine_clear_lead_hls_h264_aac_drmconfigs)
setURLArgument("type", "dash")

appArguments = getURLArguments()

players_list = str(MediaValidationVariables.codec_dash_aac).split(",")
print("SELECTED PLAYERS: ", players_list)

#Example video test url
#http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?
#url=<video_hls_h264_url>.mpd&drmconfigs=com.widevine(<license_url>)&operations=close(60)&autotest=true&type=dash
video_test_urls = getTestURLs(players_list, appArguments)

# ------------------------------------------------------------------------------
# LAUNCH & MONITOR
# ------------------------------------------------------------------------------
for video_test_url in video_test_urls:

    setPS_value(video_test_url)
    launch_status = launchApp(obj,MediaValidationVariables.unified_player_app_id)

    if "SUCCESS" not in launch_status:
        print("Unable to load the video Test URL in Webkit")
        tdkTestObj = obj.createTestStep('rdkv_media_test')
        tdkTestObj.executeTestCase(expectedResult)
        tdkTestObj.setResultStatus("FAILURE")
        continue

    # ----------------------------------------------------------
    # MONITOR VIDEO PLAYBACK
    # ----------------------------------------------------------
    test_result, proc_check_list = monitorVideoTest(obj, webkit_console_socket, validation_dict, "Video Player Playing")

    # ==========================================================
    # ### ADD: FAIL IF monitorVideoTest REPORTS FAILURE
    # ==========================================================
    if test_result == "SUCCESS":
        print("FAILURE: Encrypted video is playing fine")
        print("[TEST EXECUTION RESULT]: SUCCESS")
        tdkTestObj = obj.createTestStep('rdkv_media_test')
        tdkTestObj.executeTestCase(expectedResult)
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("FAILURE: Encrypted video is not playing fine")
        print("[TEST EXECUTION RESULT]: FAILURE")
        tdkTestObj = obj.createTestStep('rdkv_media_test')
        tdkTestObj.executeTestCase(expectedResult)
        tdkTestObj.setResultStatus("FAILURE")

    # ==========================================================
    # ADDED PRINTS DRM OBSERVATION
    # ==========================================================
    print("\n================ DRM OBSERVATION =================")
    print("NOTE:")
    print(" - 'Video Player Encrypted !!!' indicates DRM detection")
    print(" - It DOES NOT mean encrypted segments started playing")
    print(" - Widevine initializes during MPD parse in DASH streams")
    print(" - Initial clear segments are EXPECTED behavior")
    print("==================================================\n")
    # ==========================================================

# ------------------------------------------------------------------------------
# POST-CONDITIONS
# ------------------------------------------------------------------------------
print("\nSet post conditions...")
tdkTestObj = obj.createTestStep('rdkv_media_post_requisites')
tdkTestObj.executeTestCase(expectedResult)

post_requisite_status = setMediaTestPostRequisites(MediaValidationVariables.unified_player_app_id)

if post_requisite_status == "SUCCESS":
    print("Post conditions for the test are set successfully")
    tdkTestObj.setResultStatus("SUCCESS")
else:
    print("Post conditions are not met")
    tdkTestObj.setResultStatus("FAILURE")

obj.unloadModule("rdkv_media")