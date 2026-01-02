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

# Use tdklib library, which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import *


obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
# IP and port of box, no need to change,
# This will be replaced with corresponding DUT IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_SHAKA_Seek_Pos_DASH_H264_Main')

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

        print("\nSet Lightning Shaka player test app url...")
        #Setting device config file
        conf_file,result = getDeviceConfigFile(obj.realpath)
        setDeviceConfigFile(conf_file)
        appURL    = MediaValidationVariables.lightning_shaka_test_app_url
        videoURL  = MediaValidationVariables.video_src_url_dash_h264_main
        checkInterval = str(MediaValidationVariables.seekpos_check_interval)
        seekfwd_pos  = str(MediaValidationVariables.seekfwd_position)
        seekbwd_pos = str(MediaValidationVariables.seekbwd_position)
        # Setting VideoPlayer Operations
        # Video plays for 30 seconds, seek/jump to given position and continue playback for 30 seconds, then jump
        # to new position and plays for 30 seconds and close
        # Eg. opeartion=seekpos(30,85). Initial playback for 30 sec & jumps to pos 85
        setOperation("seekpos","30:"+ seekfwd_pos)
        setOperation("seekpos","30:"+ seekbwd_pos)
        setOperation("close","30")
        operations = getOperations()
        # Setting Shaka Player test app URL arguments
        setURLArgument("url",videoURL)
        setURLArgument("operations",operations)
        setURLArgument("options","checkInterval("+checkInterval+"),loop")
        setURLArgument("autotest","true")
        appArguments = getURLArguments()
        # Getting the complete test app URL
        video_test_url = getTestURL(appURL,appArguments)

        #Example video test url
        #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?
        #url=<video_src_url_dash_h264_main>.mpd&operations=seekpos(30:120),seekpos(30:75),close(30)&options=checkInterval(10),loop&autotest=true

        # Setting the video test url in webkit instance using RDKShell
        launch_status = launchPlugin(obj,webkit_instance,video_test_url)
        if "SUCCESS" in launch_status:
            # Monitoring the app progress, checking whether app plays the video properly or any hang detected in between,
            # performing proc entry check and getting the test result from the app
            test_result,proc_check_list = monitorVideoTest(obj,webkit_console_socket,validation_dict,"Observed Event: ");
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
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Unable to load the video Test URL in Webkit\n")

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