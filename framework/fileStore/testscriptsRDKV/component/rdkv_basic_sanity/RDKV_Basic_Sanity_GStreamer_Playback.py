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
import urllib.request, urllib.parse, urllib.error
import MediaValidationVariables
import json
import re

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

thunderPort=None
#Get the thunder port from REST API
url = obj.url + '/deviceGroup/getThunderDevicePorts?stbIp='+ip
try:
     data = urllib.request.urlopen(url).read()
     thunderPortDetails = json.loads(data)
     thunderPort= thunderPortDetails['thunderPort']
     print("THUNDER PORT : ", thunderPort)
except Exception as e:
     print("Unable to obtain Thunder Port from REST!!!")
     print("Error message received :\n",e);
     result = "FAILURE"

expectedResult = "SUCCESS"
DISPLAY_NAME = "testdisplay"

if expectedResult in result.upper() and thunderPort is not None:
    # Primitive test case which associated to this Script
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_createAndVerifyDisplay')
    tdkTestObj.addParameter("deviceIP", ip)
    tdkTestObj.addParameter("THUNDER_PORT", thunderPort)
    tdkTestObj.addParameter("DISPLAY_NAME", DISPLAY_NAME)
    tdkTestObj.executeTestCase(expectedResult)

    result = tdkTestObj.getResult()
    output = str(tdkTestObj.getResultDetails()).strip()

    if expectedResult in result.upper() and "SUCCESS" in output:
        print("SUCCESS: testdisplay was created and verified in getApps")
        tdkTestObj.setResultStatus("SUCCESS")

        # Fetch SSH credentials from device config file
        configKeyList = ["SSH_PORT", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
        configValues = {}
        tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
        for configKey in configKeyList:
            tdkTestObj.addParameter("basePath", obj.realpath)
            tdkTestObj.addParameter("configKey", configKey)
            tdkTestObj.executeTestCase(expectedResult)
            configValues[configKey] = tdkTestObj.getResultDetails()
            if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
                print("SUCCESS: Successfully retrieved %s configuration from device config file" % configKey)
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("FAILURE: Failed to retrieve %s configuration from device config file" % configKey)
                if configValues[configKey] == "":
                    print("\n Please configure the %s key in the device config file" % configKey)
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"
                break

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

                env_set = "WAYLAND_DISPLAY={} XDG_RUNTIME_DIR=/tmp".format(DISPLAY_NAME)
                playback_stream = MediaValidationVariables.video_src_url_short_duration_mp4

                # Optionally override base path if TEST_STREAMS_BASE_PATH is configured
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
                tdkTestObj.addParameter("basePath", obj.realpath)
                tdkTestObj.addParameter("configKey", "TEST_STREAMS_BASE_PATH")
                tdkTestObj.executeTestCase(expectedResult)
                test_streams_base_path = tdkTestObj.getResultDetails()
                if "FAILURE" not in test_streams_base_path and test_streams_base_path.strip():
                    test_streams_base_path = test_streams_base_path.strip()
                    if hasattr(MediaValidationVariables, 'test_streams_base_path') and MediaValidationVariables.test_streams_base_path:
                        playback_stream = playback_stream.replace(MediaValidationVariables.test_streams_base_path, test_streams_base_path)
                    else:
                        playback_stream = test_streams_base_path + playback_stream
                    print("INFO: TEST_STREAMS_BASE_PATH applied, playback_stream: {}".format(playback_stream))

                # Verify playback stream is accessible before launching GStreamer
                if playback_stream.startswith("file:/"):
                    # Local file on DUT — check via SSH
                    local_path = playback_stream[len("file:"):]
                    try:
                        file_check_obj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
                        file_check_obj.addParameter("sshMethod", configValues["SSH_METHOD"])
                        file_check_obj.addParameter("sshPort", configValues["SSH_PORT"])
                        file_check_obj.addParameter("credentials", credentials)
                        file_check_obj.addParameter("command", '[ -f "{}" ] && echo "exists" || echo "not found"'.format(local_path))
                        file_check_obj.executeTestCase(expectedResult)
                        file_check_output = str(file_check_obj.getResultDetails()).strip()
                        last_line = file_check_output.splitlines()[-1].strip()
                        if last_line == "exists":
                            print("INFO: Playback file found on DUT: {}".format(local_path))
                        else:
                            print("FAILURE: Playback file not found on DUT: {}".format(local_path))
                            result = "FAILURE"
                    except Exception as e:
                        print("FAILURE: Could not verify playback file on DUT: {}".format(e))
                        result = "FAILURE"
                else:
                    # Remote URL — check via HTTP HEAD request
                    try:
                        req = urllib.request.Request(playback_stream, method="HEAD")
                        urllib.request.urlopen(req, timeout=10)
                        print("INFO: Playback stream is accessible: {}".format(playback_stream))
                    except Exception as e:
                        print("FAILURE: Playback stream is not accessible: {}".format(e))
                        result = "FAILURE"

                if "FAILURE" != result:
                    gst_launch_command = "gst-launch-1.0 -v playbin uri={} flags={}".format(playback_stream, gst_play_flags)
                    command = env_set + " " + gst_launch_command
                    print("Executing command in DUT: {}".format(command))
                    # Primitive test case to execute the command in DUT
                    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
                    tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"])
                    tdkTestObj.addParameter("sshPort", configValues["SSH_PORT"])
                    tdkTestObj.addParameter("credentials", credentials)
                    tdkTestObj.addParameter("command", command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = str(tdkTestObj.getResultDetails()).strip()
                    print("[TEST EXECUTION RESULT] : %s" % result)
                    print("[RESPONSE FROM DEVICE]  : %s" % output)
                    if expectedResult in result.upper():
                        # Check playback reached >= 99.5% completion
                        percentages = [float(m) for m in re.findall(r'\(([0-9]+(?:\.[0-9]+)?)\s*%\)', output)]
                        max_percent = max(percentages) if percentages else 0.0
                        print("INFO: Maximum playback progress detected: {:.1f}%".format(max_percent))
                        reached_end = max_percent >= 99.5
                        # Check EOS
                        eos_detected = "Got EOS" in output
                        if eos_detected and reached_end:
                            print("SUCCESS: GStreamer playback completed - Got EOS detected and {:.1f}% reached".format(max_percent))
                            tdkTestObj.setResultStatus("SUCCESS")
                        elif not eos_detected:
                            print("FAILURE: 'Got EOS' was not detected in output")
                            tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("FAILURE: Playback reached only {:.1f}%, expected >= 99.5%".format(max_percent))
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("FAILURE: Failed to execute command in DUT")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE: Playback stream is not accessible, skipping GStreamer execution")
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
    print("FAILURE: Failed to load module or obtain Thunder port")
