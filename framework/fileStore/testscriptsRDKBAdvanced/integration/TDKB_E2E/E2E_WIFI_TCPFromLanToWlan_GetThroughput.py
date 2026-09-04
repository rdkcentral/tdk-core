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
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_WIFI_TCPFromLanToWlan_GetThroughput')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" %loadmodulestatus)
if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "True":
            print("MLO is enabled in the device configuration file.")

            #Assign the WIFI parameters names to a variable
            ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            #Get the value of the wifi parameters that are currently set.
            step += 1
            paramList=[ssidName,keyPassPhrase]
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase")
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Got current ssid,keypassphrase as {orgValue}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Check if same values are configured in the device configuration file
                if tdkbE2EUtility.ssid_name == orgValue[0] and tdkbE2EUtility.ssid_pwd == orgValue[1]:
                    print("The current ssid and keypassphrase are same as configured in the device configuration file")
                    tdkTestObj.setResultStatus("SUCCESS")

                    #Connect to the wifi ssid from WLAN client
                    step += 1
                    print(f"\nTEST STEP {step}: From WLAN client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: WLAN client should connect to the wifi ssid")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN client connected to wifi ssid successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should get the IP address of the WLAN client after connecting to wifi")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)
                        if wlanIP != "":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Got the IP address of the WLAN client as {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            step += 1
                            print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should get the current LAN IP address DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                            if expectedresult in status and curIPAddress != "":
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Got the LAN IP Address: {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                step += 1
                                print(f"\nTEST STEP {step}: Check whether WLAN IP address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: WLAN IP address should be in same DHCP range")
                                status = checkIpRange(curIPAddress,wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP address is in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                    #Connect to LAN client and obtain its IP
                                    step += 1
                                    print(f"\nTEST STEP {step}: Get the IP address of the LAN client after connecting to it")
                                    print(f"EXPECTED RESULT {step}: Should get the IP address of the LAN client after connecting to it")
                                    lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface)
                                    if lanIP != "":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Got IP address of the LAN client as {lanIP}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                        step += 1
                                        print(f"\nTEST STEP {step}: Check whether LAN IP address is in same DHCP range")
                                        print(f"EXPECTED RESULT {step}: LAN IP address should be in same DHCP range")
                                        status = checkIpRange(curIPAddress,lanIP)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: LAN IP address is in same DHCP range")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                            step += 1
                                            #Verify TCP from LAN to WLAN
                                            print(f"\nTEST STEP {step}: Check TCP from LAN to WLAN")
                                            print(f"EXPECTED RESULT {step}: Should check TCP from LAN to WLAN")
                                            status,serverOutput,clientOutput = tcp_udpInClients("LAN","WLAN",wlanIP,lanIP,"TCP_Throughput")
                                            if expectedresult in status and serverOutput != "":
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: TCP from LAN to WLAN is successful")
                                                print(f"Bandwidth received from server : {serverOutput}")
                                                throughput = getThroughputInMbps(serverOutput)
                                                print(f"Measured throughput: {throughput}")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                raw_threshold = str(tdkbE2EUtility.lan_throughput_to_wlan).strip()
                                                if raw_threshold.isdigit():
                                                    threshold = int(raw_threshold)
                                                    raw_offset = str(tdkbE2EUtility.perf_test_offset).strip()
                                                    if raw_offset.isdigit():
                                                        perf_offset = int(raw_offset)
                                                        lowerBound = threshold - perf_offset
                                                        upperBound = threshold + perf_offset

                                                        step += 1
                                                        print(f"\nTEST STEP {step}: Check if the throughput is in desirable throughput range.")
                                                        print(f"EXPECTED RESULT {step}: Throughput should be in desirable range.")
                                                        print(f"Actual Throughput (Mbps): {throughput}")
                                                        print(f"Desirable throughput range (Mbps): {lowerBound} - {upperBound}")
                                                        if throughput >= lowerBound and throughput <= upperBound:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: Throughput is within desirable range.")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            print(f"ACTUAL RESULT {step}: Throughput is outside desirable range.")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"Invalid or non-integer offset value: '{raw_offset}'")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"Invalid or non-integer threshold value: '{raw_threshold}'. Cannot evaluate throughput range.")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to perform TCP from LAN to WLAN.")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL STEP {step}: LAN IP address is not in DHCP range")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL STEP {step}: Failed to get the LAN client IP")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL STEP {step}: WLAN IP address is not in DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL STEP {step}: Failed to get gateway LAN IP")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL STEP {step}: Failed to get the WLAN IP address")
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        step += 1
                        print(f"\nTEST STEP {step}: From WLAN client, Disconnect from the wifi ssid")
                        print(f"EXPECTED RESULT {step}: WLAN client should be disconnected from wifi ssid")
                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL STEP {step}: Disconnect from WIFI SSID: SUCCESS")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL STEP {step}:Disconnect from WIFI SSID: FAILED")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL STEP {step}: Failed to connect to the wifi ssid")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("The current ssid and keypassphrase are not same as configured in the device configuration file")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step} : {orgValue}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            print("MLO is disabled in the device configuration file.")
            obj.setLoadModuleStatus("FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
