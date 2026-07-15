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
import MediaValidationVariables
import json
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_GStreamer_Playback');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);

expectedResult = "SUCCESS"
DISPLAY_NAME = "testdisplay"

if expectedResult in result.upper():
    # Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_createAndVerifyDisplay')
    tdkTestObj.addParameter("DISPLAY_NAME", DISPLAY_NAME)
    tdkTestObj.executeTestCase(expectedResult)

    result = tdkTestObj.getResult()
    output = str(tdkTestObj.getResultDetails()).strip()

    if expectedResult in result.upper() and "SUCCESS" in output:
        print("SUCCESS: testdisplay was created and verified in getApps")
        tdkTestObj.setResultStatus("SUCCESS")

        # Fetch all device config values in a single call using a JSON-encoded key list
        configKeyList = ["SSH_PORT", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD", "TEST_STREAMS_BASE_PATH"]
        tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
        tdkTestObj.addParameter("basePath", obj.realpath)
        tdkTestObj.addParameter("configKey", json.dumps(configKeyList))
        tdkTestObj.executeTestCase(expectedResult)
        configRaw = str(tdkTestObj.getResultDetails()).strip()
        configValues = {}
        try:
            configValues = ast.literal_eval(configRaw)
            failed_keys = [k for k, v in configValues.items() if "FAILURE" in str(v) or str(v).strip() == ""]
            # TEST_STREAMS_BASE_PATH is optional — do not treat as failure
            failed_keys = [k for k in failed_keys if k != "TEST_STREAMS_BASE_PATH"]
            for k, v in configValues.items():
                if k == "TEST_STREAMS_BASE_PATH" and not str(v).strip():
                    continue
                print("{} : {}".format(k, v))
            if failed_keys:
                for k in failed_keys:
                    print("FAILURE: Failed to retrieve %s configuration from device config file" % k)
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"
            else:
                print("SUCCESS: Successfully retrieved all device config values")
                tdkTestObj.setResultStatus("SUCCESS")
        except Exception as e:
            print("FAILURE: Could not parse device config response: {}".format(e))
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"

        if "FAILURE" != result:
            if "directSSH" == configValues["SSH_METHOD"]:
                if configValues["SSH_PASSWORD"] == "None":
                    configValues["SSH_PASSWORD"] = ""
                credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]

                # Detect SoC capabilities by checking /proc/brcm on the DUT
                gst_play_flags = "audio+video"
                try:
                    brcm_check_obj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
                    brcm_check_obj.addParameter("sshMethod", configValues["SSH_METHOD"])
                    brcm_check_obj.addParameter("sshPort", configValues["SSH_PORT"])
                    brcm_check_obj.addParameter("credentials", credentials)
                    brcm_check_obj.addParameter("command", '[ -d /proc/brcm ] && echo "exists" || echo "not found"')
                    brcm_check_obj.executeTestCase(expectedResult)
                    brcm_check_output = str(brcm_check_obj.getResultDetails()).strip()
                    output = brcm_check_output.splitlines()[-1].strip()
                    if output == "exists":
                        gst_play_flags = gst_play_flags + "+native-audio+native-video"
                except Exception as e:
                    print("Defaulting to audio+video: {}".format(e))
                print("INFO: gst_play_flags set to: {}".format(gst_play_flags))

                playback_stream = MediaValidationVariables.video_src_url_short_duration_mp4

                # Optionally override base path if TEST_STREAMS_BASE_PATH is configured
                test_streams_base_path = configValues.get("TEST_STREAMS_BASE_PATH", "")
                if "FAILURE" not in test_streams_base_path and test_streams_base_path.strip():
                    test_streams_base_path = test_streams_base_path.strip()
                    if hasattr(MediaValidationVariables, 'test_streams_base_path') and MediaValidationVariables.test_streams_base_path:
                        playback_stream = playback_stream.replace(MediaValidationVariables.test_streams_base_path, test_streams_base_path)
                    else:
                        playback_stream = test_streams_base_path + playback_stream
                    print("INFO: TEST_STREAMS_BASE_PATH applied, playback_stream: {}".format(playback_stream))

                # Launch GStreamer playback — stream check, command formation and execution
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_launchPlayback')
                tdkTestObj.addParameter("playback_stream", playback_stream)
                tdkTestObj.addParameter("gst_play_flags",  gst_play_flags)
                tdkTestObj.addParameter("DISPLAY_NAME",    DISPLAY_NAME)
                tdkTestObj.addParameter("sshMethod",       configValues["SSH_METHOD"])
                tdkTestObj.addParameter("credentials",     credentials)
                tdkTestObj.addParameter("sshPort",         configValues["SSH_PORT"])
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                output = str(tdkTestObj.getResultDetails()).strip()
                print("[LAUNCH PLAYBACK RESULT] : %s" % result)
                print("[RESPONSE FROM DEVICE]   : \n%s" % output)
                if expectedResult in result.upper() and output:
                    tdkTestObj.setResultStatus("SUCCESS")
                    # Check EOS
                    eosTestObj = obj.createTestStep('rdkv_basic_sanity_verifyEOS')
                    eosTestObj.addParameter("gst_output", output)
                    eosTestObj.executeTestCase(expectedResult)
                    eos_result = eosTestObj.getResult()
                    eos_details = str(eosTestObj.getResultDetails()).strip()
                    print("[EOS CHECK RESULT] : %s" % eos_details)

                    # Check progress
                    progressTestObj = obj.createTestStep('rdkv_basic_sanity_checkPlaybackProgress')
                    progressTestObj.addParameter("gst_output", output)
                    progressTestObj.executeTestCase(expectedResult)
                    progress_result = progressTestObj.getResult()
                    progress_details = str(progressTestObj.getResultDetails()).strip()
                    print("[PROGRESS CHECK RESULT] : %s" % progress_details)

                    if expectedResult in eos_result.upper() and expectedResult in progress_result.upper():
                        print("SUCCESS: GStreamer playback completed - EOS detected and progress threshold met")
                        eosTestObj.setResultStatus("SUCCESS")
                        progressTestObj.setResultStatus("SUCCESS")
                    else:
                        if expectedResult not in eos_details.upper():
                            print("FAILURE: EOS check failed - {}".format(eos_details))
                            eosTestObj.setResultStatus("FAILURE")
                        if expectedResult not in progress_details.upper():
                            print("FAILURE: Progress check failed - {}".format(progress_details))
                            progressTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE: GStreamer playback launch failed")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("FAILURE: Currently only supports directSSH ssh method")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Failed to get SSH configuration values")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: testdisplay was not found in getApps result")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
