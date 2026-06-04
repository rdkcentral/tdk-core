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
import tdklib
import ast
import time
import os
from urllib.parse import urlparse
import web_socket_util
from web_socket_util import *
import rdkv_appmanagerslib
from rdkv_appmanagerslib import wait_for_event
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkvxconfrfc","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AppManagers_Functional_WayLand_OnReady_Event')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

# Predefined variables which will be used in the script
event_listener = None
event_status = "FALSE"

if "SUCCESS" in result.upper():
    # Step 1 : Get the device configuration values
    print("\n")
    configkeylist = ["SSH_METHOD","SSH_USERNAME","SSH_PASSWORD","WAYLAND_DISPLAY_NAME","WAYLAND_MP4_HOSTED_URL","WAYLAND_MP4_MD5SUM_VALUE"]
    tdkTestObj = obj.createTestStep('appmanagers_getdeviceconfig')
    tdkTestObj.addParameter("configkeylist",configkeylist)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    result = ast.literal_eval(result)
    wayland_display_name = result[0]["WAYLAND_DISPLAY_NAME"]
    wayland_mp4_hosted_url = result[0]["WAYLAND_MP4_HOSTED_URL"]
    wayland_mp4_md5sum_value = result[0]["WAYLAND_MP4_MD5SUM_VALUE"]
    if "SUCCESS" in result[1]:
        tdkTestObj.setResultStatus("SUCCESS")

        # Step 2 : Check the status of the dependent plugin
        print("\n")
        pluginlist = ["org.rdk.RDKWindowManager"]
        tdkTestObj = obj.createTestStep('appmanagers_checkpluginstatus')
        tdkTestObj.addParameter("pluginlist",pluginlist)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")

            # Register and Listen the events
            print("\nRegistering and Listening to the events")
            thunder_port = rdkv_appmanagerslib.devicePort
            deviceToken = rdkv_appmanagerslib.deviceToken
            web_socket_util.deviceToken = deviceToken
            payloads = []
            # Format of events list is : '{"callsign": "eventname"}'
            events = ['{"org.rdk.RDKWindowManager": "onReady"}']
            for item in events:
                parsed_item = json.loads(item)
                for callsign, event_name in parsed_item.items():
                    payload = '{"jsonrpc": "2.0","id": 1,"method": "'+callsign+'.1.register","params": {"event": "'+event_name+'", "id": "client.events.1" }}'
                    payloads.append(payload)
            print("Event Registration List : ", payloads)
            event_listener = createEventListener(ip,thunder_port,payloads,"/jsonrpc",False)

            time.sleep(10)
            # Step 3 : Create display
            print("\n")
            method = "org.rdk.RDKWindowManager.1.createDisplay"
            value = '{"displayParams" : {"client": "'+wayland_display_name+'", "displayName": "'+wayland_display_name+'", "displayWidth": 1920, "displayHeight": 1080, "virtualWidth": 1920, "virtualHeight": 1080} }'
            #value = '{"displayParams" : {"client": "'+wayland_display_name+'", "displayName": "'+wayland_display_name+'"} }'
            tdkTestObj = obj.createTestStep('appmanagers_setvalue')
            tdkTestObj.addParameter("method",method)
            tdkTestObj.addParameter("value",value)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            result = ast.literal_eval(result)
            if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                print("SUCCESS : Display created successfully")
                tdkTestObj.setResultStatus("SUCCESS")

                # Step 4 : Check whether the display created or not
                print("\n")
                time.sleep(5)
                method = "org.rdk.RDKWindowManager.1.getApps"
                tdkTestObj = obj.createTestStep('appmanagers_getvalue')
                tdkTestObj.addParameter("method", method)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                # Convert string to list
                if "error" not in result and "result" in result:
                    result_list = json.loads(result['result'])
                    if wayland_display_name in result_list:
                        print("SUCCESS : Cretaed display is present in the list")
                        tdkTestObj.setResultStatus("SUCCESS")

                        # step 5 : Download the mp4 file
                        print("\n")
                        time.sleep(5)
                        command = "cd /tmp ; curl -O " + wayland_mp4_hosted_url + " && echo 'SUCCESS'"
                        tdkTestObj = obj.createTestStep('appmanagers_executeInDUT')
                        tdkTestObj.addParameter("command", command)
                        tdkTestObj.executeTestCase(expectedResult)
                        result = tdkTestObj.getResultDetails()
                        print("\nExecuting Command : %s" %command)
                        print("Output of executing command : %s" %result)
                        if "SUCCESS" in result:
                            print("SUCCESS : MP4 file download initiated successfully")
                            tdkTestObj.setResultStatus("SUCCESS")

                            # Step 6 : Check md5sum of the downloaded file
                            print("\n")
                            time.sleep(5)
                            filename = os.path.basename(urlparse(wayland_mp4_hosted_url).path)
                            print("MP4 file name : ", filename)
                            command = "cd /tmp ; md5sum " + filename + " | awk '{print $1}'"
                            tdkTestObj = obj.createTestStep('appmanagers_executeInDUT')
                            tdkTestObj.addParameter("command", command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            print("\nExecuting Command : %s" %command)
                            print("Output of executing command : %s" %result)
                            if wayland_mp4_md5sum_value in result:
                                print("SUCCESS : MD5 checksum of the downloaded file is correct")
                                tdkTestObj.setResultStatus("SUCCESS")

                                # Clear the event buffer before waiting for events to avoid processing old events
                                event_listener.clearEventsBuffer()
                                # Step 7 : Play the video using gst-launch
                                print("\n")
                                time.sleep(5)
                                command = 'export WAYLAND_DISPLAY=' + wayland_display_name + ' ; export XDG_RUNTIME_DIR=/tmp ; gst-launch-1.0 playbin uri="file:/tmp/'+filename+'" && echo "SUCCESS" || echo "FAILED"'
                                tdkTestObj = obj.createTestStep('appmanagers_executeInDUT')
                                tdkTestObj.addParameter("command", command)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                print("\nExecuting Command : %s" %command)
                                print("Output of executing command : %s" %result)
                                if "SUCCESS" in result:
                                    print("SUCCESS : Video played successfully")

                                    # Wait for the onReady event
                                    event_log = wait_for_event(event_listener)
                                    if len(event_log) > 0:
                                        for entry in event_log:
                                            _, json_part = entry.split("$$$", 1)
                                            json_part = json_part.encode().decode("unicode_escape")
                                            outer = json.loads(json_part)
                                            inner = outer["params"]
                                            #print("\nParsed Event : ", inner)
                                            client = inner["client"]
                                            if client == wayland_display_name:
                                                print("SUCCESS : Received onReady event for the created display : ", client)
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                event_status = "TRUE"
                                                break
                                    
                                        if event_status == "TRUE":
                                            # Step 8 : Check created display should not present in the list of apps after receiving onReady event
                                            print("\n")
                                            time.sleep(5)
                                            method = "org.rdk.RDKWindowManager.1.getApps"
                                            tdkTestObj = obj.createTestStep('appmanagers_getvalue')
                                            tdkTestObj.addParameter("method", method)
                                            tdkTestObj.executeTestCase(expectedResult)
                                            result = tdkTestObj.getResultDetails()
                                            result = ast.literal_eval(result)
                                            # Convert string to list
                                            if "error" not in result and "result" in result:
                                                result_list = json.loads(result['result'])
                                                if wayland_display_name not in result_list:
                                                    print("SUCCESS : Created display is not present in the list")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    print("FAILURE : Created display is still present in the list")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print("FAILURE : Failed to get the list of apps or created display")
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print("FAILURE : onReady event received but for different display or not received at all : ", client)
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("FAILURE : Video playback failed")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("FAILURE : MD5 checksum of the downloaded file is incorrect")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("FAILURE : MP4 file download failed")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("FAILURE : Created display is not present in the list")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE : Failed to get the list of apps or created display")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("FAILURE : Display creation failed")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")

        if event_listener:
            # Closing the websocket connection
            print("\nUnregistering the events and closing the websocket connection")
            event_listener.disconnect()
            time.sleep(10)

    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")
    obj.setLoadModuleStatus("FAILURE")

# Unload the module
print("\n")
obj.unloadModule("rdkv_appmanagers")
