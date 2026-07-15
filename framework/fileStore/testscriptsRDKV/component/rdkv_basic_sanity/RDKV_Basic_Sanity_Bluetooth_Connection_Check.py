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
import time
import ast
import os
import configparser
from rdkv_basic_sanitylib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Bluetooth_Connection_Check')

#Execution summary variable
Summ_list=[]

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions")
    status = "SUCCESS"
    
    # Fetch Bluetooth device name from config file
    print("\n[CONFIG] Fetching Bluetooth device configuration")
    bt_device_name = ""
    
    # Get config file path from basePath
    config_path = obj.realpath.rstrip('/') + "/fileStore/tdkvRDKServiceConfig"
    
    if os.path.exists(config_path):
        # List all .config files in the directory
        config_files = [f for f in os.listdir(config_path) if f.endswith('.config')]
        
        if config_files:
            # Try each config file to find one with BT_EMU_DEVICE_NAME
            for config_filename in config_files:
                # Skip sample files
                if 'sample' in config_filename.lower() or 'ci_exec' in config_filename.lower():
                    continue
                    
                config_file = os.path.join(config_path, config_filename)
                print("Trying config file: %s" %config_file)
                
                try:
                    # Read config file as properties file (key = value format)
                    with open(config_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            # Skip empty lines and comments
                            if not line or line.startswith('#'):
                                continue
                            # Parse key=value pairs
                            if '=' in line:
                                key, value = line.split('=', 1)
                                key = key.strip().lower()
                                value = value.strip()
                                
                                if key == 'bt_emu_device_name':
                                    bt_device_name = value
                                    print("Found Bluetooth Device Name: %s in file: %s" %(bt_device_name, config_filename))
                                    Summ_list.append('Config Fetch : SUCCESS')
                                    break
                    
                    if bt_device_name:
                        break
                        
                except Exception as e:
                    print("Error reading %s: %s" %(config_filename, str(e)))
                    continue
            
            if not bt_device_name:
                print("BT_EMU_DEVICE_NAME not found in any config file")
                Summ_list.append('Config Fetch : FAILURE')
                status = "FAILURE"
        else:
            print("No config files found in %s" %config_path)
            Summ_list.append('Config Fetch : FAILURE')
            status = "FAILURE"
    else:
        print("Config path does not exist: %s" %config_path)
        Summ_list.append('Config Fetch : FAILURE')
        status = "FAILURE"
    
    if status == "SUCCESS":
        print("\n[STEP 1] Enabling Bluetooth")
        tdkTestObj = obj.createTestStep('rdkservice_getValue')
        tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.enable")
        tdkTestObj.executeTestCase(expectedResult)
        enable_result = tdkTestObj.getResult()
        
        if enable_result == "SUCCESS":
            print("Bluetooth enabled successfully")
            Summ_list.append('Bluetooth Enable : SUCCESS')
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
                Summ_list.append('Bluetooth StartScan : SUCCESS')
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
                    Summ_list.append('Bluetooth StopScan : SUCCESS')
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
                        Summ_list.append('Bluetooth GetDiscoveredDevices : SUCCESS')
                        tdkTestObj.setResultStatus("SUCCESS")
                        
                        try:
                            devices_list = ast.literal_eval(discover_details)["discoveredDevices"]
                            if devices_list:
                                print("Number of devices discovered: %d" %len(devices_list))
                                
                                # Search for the specific device from config
                                device_id = ""
                                device_name = ""
                                device_type = ""
                                for device in devices_list:
                                    if device["name"] == bt_device_name:
                                        device_id = device["deviceID"]
                                        device_name = device["name"]
                                        device_type = device["deviceType"]
                                        break
                                
                                if device_id != "":
                                    print("Found configured device: %s" %device_name)
                                    
                                    # Step 5: Pair Device
                                    print("\n[STEP 5] Pairing with Device: %s" %device_name)
                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                    tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.pair")
                                    tdkTestObj.addParameter("value", '{"deviceID": "' + device_id + '"}')
                                    tdkTestObj.executeTestCase(expectedResult)
                                    pair_result = tdkTestObj.getResult()
                                    
                                    if pair_result == "SUCCESS":
                                        print("Device paired successfully")
                                        Summ_list.append('Bluetooth Pair : SUCCESS')
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        time.sleep(3)
                                        
                                        # Step 6: Connect Device
                                        print("\n[STEP 6] Connecting to Device: %s" %device_name)
                                        tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                        tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.connect")
                                        tdkTestObj.addParameter("value", '{"deviceID": "' + device_id + '","deviceType":"' + device_type + '","profile": "DEFAULT"}')
                                        tdkTestObj.executeTestCase(expectedResult)
                                        connect_result = tdkTestObj.getResult()
                                        
                                        if connect_result == "SUCCESS":
                                            print("Device connected successfully")
                                            Summ_list.append('Bluetooth Connect : SUCCESS')
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            time.sleep(5)
                                            
                                            # Step 7: Get Connected Devices
                                            print("\n[STEP 7] Verifying Connected Devices")
                                            tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                            tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.getConnectedDevices")
                                            tdkTestObj.executeTestCase(expectedResult)
                                            connected_result = tdkTestObj.getResult()
                                            connected_details = tdkTestObj.getResultDetails()
                                            
                                            if connected_result == "SUCCESS":
                                                connected_list = ast.literal_eval(connected_details)["connectedDevices"]
                                                if connected_list and any(device["name"] == device_name for device in connected_list):
                                                    print("Device is in connected list")
                                                    Summ_list.append('Bluetooth GetConnectedDevices : SUCCESS')
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    print("Device not in connected list")
                                                    Summ_list.append('Bluetooth GetConnectedDevices : FAILURE')
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print("Failed to get connected devices")
                                                Summ_list.append('Bluetooth GetConnectedDevices : FAILURE')
                                                tdkTestObj.setResultStatus("FAILURE")
                                            
                                            # Step 8: Disconnect Device
                                            print("\n[STEP 8] Disconnecting Device: %s" %device_name)
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.disconnect")
                                            tdkTestObj.addParameter("value", '{"deviceID": "' + device_id + '","deviceType":"' + device_type + '"}')
                                            tdkTestObj.executeTestCase(expectedResult)
                                            disconnect_result = tdkTestObj.getResult()
                                            
                                            if disconnect_result == "SUCCESS":
                                                print("Device disconnected successfully")
                                                Summ_list.append('Bluetooth Disconnect : SUCCESS')
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                time.sleep(2)
                                            else:
                                                print("Failed to disconnect device")
                                                Summ_list.append('Bluetooth Disconnect : FAILURE')
                                                tdkTestObj.setResultStatus("FAILURE")
                                            
                                            # Step 9: Unpair Device
                                            print("\n[STEP 9] Unpairing Device: %s" %device_name)
                                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                            tdkTestObj.addParameter("method", "org.rdk.Bluetooth.1.unpair")
                                            tdkTestObj.addParameter("value", '{"deviceID": "' + device_id + '"}')
                                            tdkTestObj.executeTestCase(expectedResult)
                                            unpair_result = tdkTestObj.getResult()
                                            
                                            if unpair_result == "SUCCESS":
                                                print("Device unpaired successfully")
                                                Summ_list.append('Bluetooth Unpair : SUCCESS')
                                                tdkTestObj.setResultStatus("SUCCESS")
                                            else:
                                                print("Failed to unpair device")
                                                Summ_list.append('Bluetooth Unpair : FAILURE')
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            print("Failed to connect device")
                                            Summ_list.append('Bluetooth Connect : FAILURE')
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print("Failed to pair device")
                                        Summ_list.append('Bluetooth Pair : FAILURE')
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("Configured device not found in discovered list")
                                    Summ_list.append('Bluetooth Device Discovery : Device Not Found')
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("No devices discovered")
                                Summ_list.append('Bluetooth GetDiscoveredDevices : No Devices')
                                tdkTestObj.setResultStatus("FAILURE")
                        except Exception as e:
                            print("Error parsing discovered devices: %s" %str(e))
                            Summ_list.append('Bluetooth GetDiscoveredDevices : FAILURE')
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("Failed to get discovered devices")
                        Summ_list.append('Bluetooth GetDiscoveredDevices : FAILURE')
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Failed to stop scan")
                    Summ_list.append('Bluetooth StopScan : FAILURE')
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("Failed to start scan")
                Summ_list.append('Bluetooth StartScan : FAILURE')
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to enable Bluetooth")
            Summ_list.append('Bluetooth Enable : FAILURE')
            tdkTestObj.setResultStatus("FAILURE")
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
