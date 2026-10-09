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

# Use tdklib library, which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
# IP and Port of box, No need to change,
# This will be replaced with corresponding DUT IP and Port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_HTML_Play_Successive_SDR_TO_HDR')

webkit_console_socket = None

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions...")
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    setWebKitSocketPort(webinspect_port_html)
    # Setting the pre-requisites for media test. Launching the required test app via AppManager and
    # getting the details for proc validation from config file
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,MediaValidationVariables.html_player_app_id,MediaValidationVariables.html_player_app_download_url)
    if pre_requisite_status == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS");
        print("Pre conditions for the test are set successfully")

        print("\nSet Lightning video player test app url...")
        # Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)

        # Construct stream 1 URL
        appURL1    = MediaValidationVariables.html_video_test_app_url
        videoURL1  = MediaValidationVariables.video_src_url_mp4
        # Setting VideoPlayer Operations for Stream 1
        setOperation("close",MediaValidationVariables.close_interval)
        operations1 = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL1)
        setURLArgument("operations",operations1)
        setURLArgument("autotest","true")
        appArguments1 = getURLArguments()
        # Getting the complete test app URL for stream 1
        video_test_url1 = getTestURL(appURL1,appArguments1)

        # Construct stream 2 URL
        appURL2   = MediaValidationVariables.html_video_test_app_url
        videoURL2  = MediaValidationVariables.video_src_url_hevc_hdr
        # Setting VideoPlayer Operations for Stream 2
        operations2 = getOperations()
        # Setting VideoPlayer test app URL arguments
        setURLArgument("url",videoURL2)
        setURLArgument("operations",operations2)
        setURLArgument("autotest","true")
        appArguments2 = getURLArguments()
        # Getting the complete test app URL for stream 2
        video_test_url2 = getTestURL(appURL2,appArguments2)

        #Example video test url
        #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/htmlplayer.html?
        #url=<video_mp4_url>&operations=close(60)

        # Setting the list of video test url's for successive playback in PersistentStore and launching the html test app using AppManager
        setPS_value([video_test_url1,video_test_url2])
        launch_status = launchApp(obj,MediaValidationVariables.html_player_app_id)
        if "SUCCESS" in launch_status:
            # Monitoring the app progress, checking whether app plays the video properly or any hang detected in between,
            # performing proc entry check and getting the test result from the app
            test_result,proc_check_list = monitorVideoTest(obj,webkit_console_socket,validation_dict,"Video Player Playing");
            tdkTestObj = obj.createTestStep('rdkv_media_test');
            tdkTestObj.executeTestCase(expectedResult);
            if "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                print("Video is playing fine")
                print("[TEST EXECUTION RESULT]: SUCCESS")
                tdkTestObj.setResultStatus("SUCCESS");
            elif "SUCCESS" in test_result and "FAILURE" in proc_check_list:
                print("Decoder proc entry check returns failure. Video is not playing fine")
                print("[TEST EXECUTION RESULT]: FAILURE")
                tdkTestObj.setResultStatus("FAILURE");
            else:
                print("Video is not playing fine")
                print("[TEST EXECUTION RESULT]: FAILURE")
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Unable to load the Video Test URL in Webkit\n")

        print("\nSet post conditions...")
        tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
        tdkTestObj.executeTestCase(expectedResult);
        # Setting the post-requisites for media test. Terminating the bolt app & verifying the app unload event.
        post_requisite_status = setMediaTestPostRequisites(MediaValidationVariables.html_player_app_id)
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