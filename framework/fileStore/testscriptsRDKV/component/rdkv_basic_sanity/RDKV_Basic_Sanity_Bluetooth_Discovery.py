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

#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import ast

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Bluetooth_Discovery')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions")
    status = "SUCCESS"
    
    print("\n[STEP 1] Enabling Bluetooth")
    tdkTestObj = obj.createTestStep('rdkservice_getValue')
    tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.enable")
    tdkTestObj.executeTestCase(expectedResult)
    enable_result = tdkTestObj.getResult()
    
    if enable_result == "SUCCESS":
        print("Bluetooth enabled successfully")
        tdkTestObj.setResultStatus("SUCCESS")
        time.sleep(3)
        
        # Step 2: Start Scan
        print("\n[STEP 2] Starting Bluetooth Scan")
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.startScan")
        tdkTestObj.addParameter("value", '{"timeout": "30", "profile": "DEFAULT"}')
        tdkTestObj.executeTestCase(expectedResult)
        start_scan_result = tdkTestObj.getResult()
        
        if start_scan_result == "SUCCESS":
            print("Bluetooth scan started successfully")
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(30)
            
            # Step 3: Stop Scan
            print("\n[STEP 3] Stopping Bluetooth Scan")
            tdkTestObj = obj.createTestStep('rdkservice_getValue')
            tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.stopScan")
            tdkTestObj.executeTestCase(expectedResult)
            stop_scan_result = tdkTestObj.getResult()
            
            if stop_scan_result == "SUCCESS":
                print("Bluetooth scan stopped successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(2)
                
                # Step 4: Get Discovered Devices
                print("\n[STEP 4] Getting Discovered Devices")
                tdkTestObj = obj.createTestStep('rdkservice_getValue')
                tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.getDiscoveredDevices")
                tdkTestObj.executeTestCase(expectedResult)
                discover_result = tdkTestObj.getResult()
                discover_details = tdkTestObj.getResultDetails()
                
                if discover_result == "SUCCESS" and discover_details:
                    print("Discovered devices retrieved successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    
                    try:
                        devices_list = ast.literal_eval(discover_details)["discoveredDevices"]
                        if devices_list:
                            print("Number of devices discovered: %d" %len(devices_list))
                        else:
                            print("No devices discovered")
                            tdkTestObj.setResultStatus("FAILURE")
                    except Exception as e:
                        print("Error parsing discovered devices: %s" %str(e))
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Failed to get discovered devices")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Failed to stop scan")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to start scan")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("Failed to enable Bluetooth")
        tdkTestObj.setResultStatus("FAILURE")
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
