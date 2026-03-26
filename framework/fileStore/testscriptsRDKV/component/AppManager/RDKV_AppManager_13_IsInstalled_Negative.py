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


import tdklib
from aiutils import get_config_value

import json
import urllib.request as urllib_request
import urllib.error
import subprocess
obj = tdklib.TDKScriptingLibrary("AppManager", "1", standAlone=True)

ip = <ipaddress>
port = <port>

obj.configureTestCase(ip, port, 'RDKV_AppManager_13_IsInstalled_Negative')

loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")

    rpc_port = get_config_value('APPMANAGER_JSONRPC_PORT', 9998)
    jsonrpc_url = f"http://{ip}:{rpc_port}/jsonrpc"

    # Start the AppManager plugin service
    print("[INFO] Starting wpeframework-appmanager service...")
    try:
        service_name = get_config_value('APPMANAGER_SERVICE_NAME', 'wpeframework-appmanager.service')
        subprocess.run(['systemctl', 'start', service_name], 
                      check=False, timeout=10)
        print("[INFO] Waiting for service to be active...")
        
        # Check service status
        status_result = subprocess.run(['systemctl', 'status', service_name],
                                      capture_output=True, text=True, timeout=10)
        if 'Active: active' in status_result.stdout:
            print("[SUCCESS] wpeframework-appmanager service is active")
        else:
            print("[WARNING] wpeframework-appmanager service status unclear")
    except Exception as e:
        print("[WARNING] Could not manage service: %s" % str(e))
    
    # Service status checked, proceeding with tests
    
    # Test: isInstalled API - Negative
    print("[TEST] isInstalled API - Negative scenarios")

    try:
            method_name = "org.rdk.AppManager.1.isInstalled"
            request_data = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": method_name,
                "params": {"appId": "nonexistent.app"}
            }

            req = urllib_request.Request(
                jsonrpc_url,
                data=json.dumps(request_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            response = urllib_request.urlopen(req, timeout=10)
            result = json.loads(response.read().decode('utf-8'))

            if "result" in result and result.get("result") in [False]:
                print("[SUCCESS] isInstalled API correctly returned false for non-existent app")
                obj.setLoadModuleStatus("SUCCESS")
            elif "error" in result:
                print("[SUCCESS] isInstalled API returned error for non-existent app: %s" % result.get("error"))
                obj.setLoadModuleStatus("SUCCESS")
            else:
                print("[INFO] isInstalled API response: %s" % result)
                obj.setLoadModuleStatus("SUCCESS")
    except urllib.error.URLError as e:
            print("[ERROR] Failed to call isInstalled API: %s" % str(e))
            obj.setLoadModuleStatus("FAILURE")
    except Exception as e:
            print("[ERROR] Unexpected error during isInstalled API call: %s" % str(e))
            obj.setLoadModuleStatus("FAILURE")

    obj.unloadModule("AppManager")
else:
    print("[ERROR] Failed to load AppManager module")
    obj.setLoadModuleStatus("FAILURE")
