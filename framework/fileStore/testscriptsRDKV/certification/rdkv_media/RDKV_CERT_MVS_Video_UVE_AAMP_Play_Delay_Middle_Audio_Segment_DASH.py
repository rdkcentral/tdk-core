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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>11</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_MVS_Video_UVE_AAMP_Play_Delay_Middle_Audio_Segment_DASH</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_media_test</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Test script to initiate the TDK Lightning UVE AAMP Player application through a Webkit instance. The objective is to assess the Player's response when delays are intentionally introduced for audio segment files during the middle part of stream, served via the Nginx streaming server with an intentional delay configuration.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <test_case_id>RDKV_Media_Validation_607</test_case_id>
    <test_objective>Test script to initiate the TDK Lightning UVE AAMP Player application through a Webkit instance. The objective is to assess the Player's response when delays are intentionally introduced for audio segment files during the middle part of stream, served via the Nginx streaming server with an intentional delay configuration.</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Accelerator,RPI</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device. 
2.Lightning Player app should be hosted.
3.Streaming server should be up and running in the docker.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Lightning UVE AAMP player App URL: string   webkit_instance:string webinspect_port: string  audio_src_url_middle_dash: string</input_parameters>
    <automation_approch>1. As pre requisite, launch webkit instance via RDKShell, open websocket connection to webinspect page
2. Store the details of other launched apps. Move the webkit instance to front, if its z-order is low. 
3. Transfer the relevant Nginx delay configuration file to the Nginx build directory.
4. Streaming server should be up and running in the docker.
5. Launch webkit instance with video test app with the live dash url.
6. App should play the live dash content and event video playing should occur.
7. If expected event video playing is observed then update the result as SUCCESS or else FAILURE.
8. Update the test script result as SUCCESS/FAILURE based on event validation result and proc check status (if applicable). 
9. Revert all values.
10. Streaming server should be stopped.</automation_approch>
    <expected_output>The player should handle delays in video and audio segments without crashing or exiting the 'playing' state. For short delays, playback should continue smoothly after buffering. For longer delays, the player may pause to buffer but must resume playback from the delayed segments without skipping or freezing.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_media</test_stub_interface>
    <test_script>RDKV_CERT_MVS_Video_UVE_AAMP_Play_Delay_Middle_Audio_Segment_DASH</test_script>
    <skipped>No</skipped>
    <release_version>M143</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_medialib import *
import MediaValidationVariables
from MediaValidationUtility import * 
from MediaValidationUtility import generate_nginx_config

obj = tdklib.TDKScriptingLibrary("rdkv_media","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_MVS_Video_UVE_AAMP_Play_Delay_Middle_Audio_Segment_DASH')
webkit_console_socket = None 
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print ("[LIB LOAD STATUS]  :  %s" %result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print ("\nCheck Pre conditions...")
    tdkTestObj = obj.createTestStep('rdkv_media_pre_requisites');
    tdkTestObj.executeTestCase(expectedResult);
    # Setting the pre-requites for media test. Launching the wekit instance via RDKShell and
    # moving it to the front, openning a socket connection to the webkit inspect page and
    # getting the details for proc validation from config file
    pre_requisite_status,webkit_console_socket,validation_dict = setMediaTestPreRequisites(obj,webkit_instance)
    # Path to the template file
    template_path = MediaValidationVariables.NGINX_TEMPLATE_PATH
    local_destination = MediaValidationVariables.NGINX_LOCAL_DESTINATION
    remote_destination = MediaValidationVariables.NGINX_REMOTE_DESTINATION
    nginx_container_ip = MediaValidationVariables.NGINX_CONTAINER_IP

    # Values for placeholders
    chunk_pattern = "chunk-stream1-00005"  # Example chunk pattern
    # Update the Nginx configuration
    generate_nginx_config(template_path, local_destination, remote_destination, nginx_container_ip, chunk_pattern, delay_value)
    # Check and start Nginx if necessary
    check_and_start_nginx() 
    videoURL  = MediaValidationVariables. video_src_url_delay_dash
    delay = MediaValidationVariables.delay_value 
    if pre_requisite_status == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS");
            print ("Pre conditions for the test are set successfully")
            print ("\nSet Lightning video player test app url...")
            #Setting device config file
            conf_file,result = getDeviceConfigFile(obj.realpath)
            setDeviceConfigFile(conf_file)
            appURL    = MediaValidationVariables.lightning_uve_test_app_url
            # Setting VideoPlayer Operations
            setOperation("close","100")   
            operations = getOperations()
            # Setting VideoPlayer test app URL arguments
            setURLArgument("url",videoURL)
            setURLArgument("operations",operations)
            setURLArgument("autotest","true")
            setURLArgument("delaytest","true")
            setURLArgument("expectedStart", "0")
            setURLArgument("expectedEnd", "89")
            appArguments = getURLArguments()
            # Getting the complete test app URL for selected players
            test_counter = 0
            players_list = str(MediaValidationVariables.codec_dash_h264).split(",")
            print ("SELECTED PLAYERS: ", appURL)
            video_test_url = getTestURL(appURL,appArguments)

            # Example video test url
            #http://*testManagerIP*/rdk-test-tool/fileStore/lightning-apps/unifiedplayer/build/index.html?
            #url=<video_h264_url>.mpd&operations=playtillend(0)&autotest=true&type=mp4

            # Setting the video test url in webkit instance using RDKShell
            launch_status = launchPlugin(obj,webkit_instance,video_test_url)
            if "SUCCESS" in launch_status:
                # Monitoring the app progress, checking whether app plays the video properly or any hang detected in between,
                # performing proc entry check and getting the test result from the app
                test_counter += 1
                test_result,proc_check_list = monitorVideoTest(obj,webkit_console_socket,validation_dict,"Video Player Playing",180);
                tdkTestObj = obj.createTestStep('rdkv_media_test');
                tdkTestObj.executeTestCase(expectedResult);
                if "SUCCESS" in test_result and "FAILURE" not in proc_check_list:
                    print ("Video play is fine")
                    print("[TEST EXECUTION RESULT]: SUCCESS")
                    tdkTestObj.setResultStatus("SUCCESS");
                elif "SUCCESS" in test_result and "FAILURE" in proc_check_list:
                    print ("Decoder proc entry check returns failure.Video not playing fine")
                    print ("[TEST EXECUTION RESULT]: FAILURE")
                    tdkTestObj.setResultStatus("FAILURE");
                else:
                    print ("Video not playing fine")
                    print ("[TEST EXECUTION RESULT]: FAILURE")
                    tdkTestObj.setResultStatus("FAILURE"); 
            print ("\nSet post conditions...")
            tdkTestObj = obj.createTestStep('rdkv_media_post_requisites');
            tdkTestObj.executeTestCase(expectedResult);
            # Setting the post-requites for media test.Removing app url from webkit instance and
            # moving next high z-order app to front (residentApp if its active)
            post_requisite_status = setMediaTestPostRequisites(obj,webkit_instance,webkit_console_socket)
            if post_requisite_status == "SUCCESS":
                print ("Post conditions for the test are set successfully\n")
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print ("Post conditions are not met\n")
                tdkTestObj.setResultStatus("FAILURE");
    else:
        print ("Pre conditions are not met\n")
        tdkTestObj.setResultStatus("FAILURE");
        obj.unloadModule("rdkv_media");
else:
    obj.setLoadModuleStatus("FAILURE");
    print ("Failed to load module")

#function to stop nginx
stop_nginx()
