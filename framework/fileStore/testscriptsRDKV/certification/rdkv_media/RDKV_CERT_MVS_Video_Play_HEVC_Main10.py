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

# use tdklib library, which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
# IP and port of box, No need to change,
# This will be replaced with corresponding DUT IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_Play_HEVC_Main10')

webkit_console_socket = None

# Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions...")
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    # Setting the pre-requisites for media test. Launching the webkit instance via RDKShell and
    # moving it to the front, opening a socket connection to the webkit inspect page and
    # getting the details for proc validation from config file
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,webkit_instance)
    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print("Pre conditions for the test are set successfully")

        print("\nSet Lightning video player test app url...")
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)
        #appURL    = MediaValidationVariables.lightning_video_test_app_url
        videoURL  = MediaValidationVariables.video_src_url_hevc_main10
        # Setting VideoPlayer Operations
        setOperation("close",MediaValidationVariables.close_interval)
        operations = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL)
        setURLArgument("operations",operations)
        setURLArgument("autotest","true")
        setURLArgument("type","dash")
        appArguments = getURLArguments()

        # Getting the complete test app URL for selected players
        video_test_urls = []
        test_counter = 0
        players_list = str(MediaValidationVariables.codec_dash_h264).split(",")
        print("SELECTED PLAYERS: ", players_list)
        video_test_urls = getTestURLs(players_list,appArguments)

        #Example video test url
        #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?
        #url=<video_src_url_hevc_main10>.mpd&operations=close(60)&autotest=true&type=dash

        # Setting the video test url in webkit instance using RDKShell
        for video_test_url in video_test_urls:
            launch_status = launchPlugin(obj,webkit_instance,video_test_url)
            if "SUCCESS" in launch_status:
                # Monitoring the app progress, checking whether app plays the video properly or any hang detected in between,
                # performing proc entry check and getting the test result from the app
                test_counter += 1
                test_result,proc_check_list = monitorVideoTest(obj,webkit_console_socket,validation_dict,"Video Player Playing");
                tdkTestObj = obj.createTestStep('rdkv_media_test');
                tdkTestObj.executeTestCase(expectedResult);
                if "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                    print("Video play is fine")
                    print("[TEST EXECUTION RESULT]: SUCCESS")
                    tdkTestObj.setResultStatus("SUCCESS");
                elif "SUCCESS" in test_result and "FAILURE" in proc_check_list:
                    print("Decoder proc entry check returns failure.Video not playing fine")
                    print("[TEST EXECUTION RESULT]: FAILURE")
                    tdkTestObj.setResultStatus("FAILURE");
                else:
                    print("Video not playing fine")
                    print("[TEST EXECUTION RESULT]: FAILURE")
                    tdkTestObj.setResultStatus("FAILURE");

                if test_counter < len(video_test_urls):
                    launch_status = launchPlugin(obj,webkit_instance,"about:blank")
                    time.sleep(3)
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("Unable to load the Video Test URL in Webkit\n")

        print("\nSet post conditions...")
        tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
        tdkTestObj.executeTestCase(expectedResult);
        # Setting the post-requisites for media test. Removing app url from webkit instance and
        # moving next high z-order app to front (residentApp if its active)
        post_requisite_status = setMediaTestPostRequisites(obj,webkit_instance,webkit_console_socket)
        if post_requisite_status == "SUCCESS":
            print("Post conditions for the test are set successfully\n")
            tdkTestObj.setResultStatus("SUCCESS");
        else:
            print("Post conditions are not met\n")
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print("Pre conditions are not met\n")
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")