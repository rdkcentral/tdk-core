##########################################################################
# If not stated otherwise in this file or this component's LICENSE
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
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_WLAN_AccessInternet')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "True":
            print("MLO is enabled in the device configuration file.")

            #Assign the WIFI parameter names to variables
            ssidName = "Device.WiFi.SSID.%s.SSID" % tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" % tdkbE2EUtility.ssid_2ghz_index

            #Get the current SSID and keypassphrase from DUT
            paramList = [ssidName, keyPassPhrase]
            print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase from DUT")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
            tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {orgValue}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Verify DUT SSID and password match what is configured in the device config file
                if tdkbE2EUtility.ssid_name == orgValue[0] and tdkbE2EUtility.ssid_pwd == orgValue[1]:
                    print("SSID and keypassphrase match the device configuration file")
                    tdkTestObj.setResultStatus("SUCCESS")

                    #Connect WLAN client to the MLO SSID
                    step += 1
                    print(f"\nTEST STEP {step}: Connect WLAN client to the MLO SSID")
                    print(f"EXPECTED RESULT {step}: WLAN client should connect to the SSID successfully")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name, tdkbE2EUtility.ssid_pwd, tdkbE2EUtility.wlan_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Get WLAN client IP address after connecting
                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve WLAN client IP address")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client IP is {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Get the Gateway LAN IP address from DUT
                            step += 1
                            print(f"\nTEST STEP {step}: Get the Gateway LAN IP address from DUT")
                            print(f"EXPECTED RESULT {step}: Should retrieve Gateway LAN IP address successfully")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Gateway LAN IP is {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                #Check WLAN IP is in DHCP range
                                step += 1
                                print(f"\nTEST STEP {step}: Check whether WLAN IP address is in the DHCP range")
                                print(f"EXPECTED RESULT {step}: WLAN IP should be in the DHCP range")
                                status = checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is in the DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #Ping internet host from WLAN client
                                    step += 1
                                    print(f"\nTEST STEP {step}: Verify WLAN client has internet access by pinging {tdkbE2EUtility.network_ip}")
                                    print(f"EXPECTED RESULT {step}: WLAN client should successfully ping the internet host")
                                    status = verifyNetworkConnectivity(tdkbE2EUtility.network_ip, "PING_TO_HOST", wlanIP, curIPAddress, "WLAN")
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Internet access verified successfully via ping")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #Disconnect WLAN client from the SSID
                                        step += 1
                                        print(f"\nTEST STEP {step}: Disconnect WLAN client from the wifi SSID")
                                        print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            finalStatus = "SUCCESS"
                                            print(f"ACTUAL RESULT {step}: WLAN client disconnected successfully")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to disconnect WLAN client from SSID")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: WLAN client could not ping internet host")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is not in the DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to retrieve Gateway LAN IP address")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get WLAN client IP address")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to the SSID")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("SSID and keypassphrase in DUT do not match the device configuration file")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to retrieve current ssid and keypassphrase")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            print("MLO is disabled in the device configuration file.")
            obj.setLoadModuleStatus("FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
