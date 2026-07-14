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
import json
import requests
import urllib.request, urllib.parse, urllib.error
import tdklib
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_HDMI_Connection_Check');

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

thunderPort = None
# Get the thunder port from REST API
url = obj.url + '/deviceGroup/getThunderDevicePorts?stbIp=' + ip
try:
    data = urllib.request.urlopen(url).read()
    thunderPortDetails = json.loads(data)
    thunderPort = thunderPortDetails['thunderPort']
    print("THUNDER PORT : ", thunderPort)
except Exception as e:
    print("Unable to obtain Thunder Port from REST!!!")
    print("Error message received :\n", e)
    result = "FAILURE"

expectedResult = "SUCCESS"

if expectedResult in result.upper() and thunderPort is not None:

    # Call org.rdk.DisplaySettings.getConnectedVideoDisplays via Thunder JSON-RPC
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    tdkTestObj.addParameter("basePath",  obj.realpath)
    tdkTestObj.addParameter("configKey", "SSH_METHOD")
    tdkTestObj.executeTestCase(expectedResult)
    print("")

    jsonrpc_url = "http://{}:{}/jsonrpc".format(ip, thunderPort)
    payload = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "org.rdk.DisplaySettings.getConnectedVideoDisplays"
    }

    try:
        response = requests.post(jsonrpc_url, json=payload, timeout=10)
        response_json = response.json()
        print("INFO: getConnectedVideoDisplays response: %s" % json.dumps(response_json))

        result_obj         = response_json.get("result", {})
        connected_displays = result_obj.get("connectedVideoDisplays", [])
        success            = result_obj.get("success", False)

        print("INFO: connectedVideoDisplays: %s" % connected_displays)

        if not success:
            print("FAILURE: getConnectedVideoDisplays did not return success=true")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            hdmi_connected = any(str(d).upper().startswith("HDMI") for d in connected_displays)
            if hdmi_connected:
                print("SUCCESS: HDMI is connected")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("FAILURE: HDMI is not connected. Connected displays: %s" % connected_displays)
                tdkTestObj.setResultStatus("FAILURE")

    except Exception as e:
        print("FAILURE: Exception during getConnectedVideoDisplays request: %s" % str(e))
        tdkTestObj.setResultStatus("FAILURE")

    # Unload the module
    obj.unloadModule("rdkv_basic_sanity")

else:
    # Set load module status
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
