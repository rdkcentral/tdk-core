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


# use tdklib library, which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
import tdkutility

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_OpenSecurity_Custom_TCPFromWlanToLan')
wifi_obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_OpenSecurity_Custom_TCPFromWlanToLan')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = wifi_obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    index = 17
    step = 1

    # Parse the device configuration file
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Device configuration parsed successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"
        firewallLevel = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

        # Get the value of the wifi parameters that are currently set
        paramList = [ssidName, securityMode, firewallLevel]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)
        initial_secMode = orgValue[1]

        print(f"\nTEST STEP {step}: Get the current ssid, securityMode and firewallLevel")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, securityMode and firewallLevel")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Retrived current ssid, securityMode and firewallLevel. Current values:{orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            #Get the initial security configuration
            step += 1
            print(f"\nTEST STEP {step}: Get the initial security configuration")
            print(f"EXPECTED RESULT {step}: Should successfully get initial security configuration")
            initial_config = {}
            tdkTestObj,actualresult,initial_config = tdkutility.getSecurityModeEnabledConfig(wifi_obj, initial_secMode, index)

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Initial security configuration reterived successfully. Initial config values: {initial_config}")
                print("TEST EXECUTION RESULT :SUCCESS")

                # Set ssid, security mode, firewalllevel
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name, 'Enhanced-Open', 'Custom']
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                list2 = [securityMode, 'Enhanced-Open', 'string']
                firewallParam = f"{firewallLevel}|Custom|string"

                # Concatenate the lists with the elements separated by pipe
                setParamList = "|".join(map(str, list1 + list2))

                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)
                tdkTestObj, firewallResult, details = tdkbE2EUtility.setMultipleParameterValues(obj, firewallParam)

                step += 1
                print(f"\nTEST STEP {step}: Set the ssid, security mode and firewallLevel")
                print(f"EXPECTED RESULT {step}: Should set the ssid, security mode and firewallLevel")

                if expectedresult in actualresult and expectedresult in firewallResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: SET operation success. Details:{details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Retrieve the values after set and compare
                    newParamList = [ssidName, securityMode, firewallLevel]
                    tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                    step += 1
                    print(f"\nTEST STEP {step}: Get the current ssid, security mode and firewallLevel after setting new values")
                    print(f"EXPECTED RESULT {step}: Should retrieve the updated ssid, security mode and firewallLevel")

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: The parameter values after SET: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        # Wait for the changes to reflect in client device
                        time.sleep(60)

                        # Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"\nTEST STEP {step}: Connect to the wifi ssid from WLAN client")
                        print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                        status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface,"Open")

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            step += 1

                            print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to wifi")
                            print(f"EXPECTED RESULT {step}: Should retrieve a valid IP address for the wlan client")
                            wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN client IP is {wlanIP}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should retrieve the current LAN IP address")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj, status, curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: LAN IP Address is {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"\nTEST STEP {step}: Check whether WLAN IP address is in same DHCP range")
                                    print(f"EXPECTED RESULT {step}: WLAN IP should be in same DHCP range as LAN")
                                    status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: WLAN IP is in same DHCP range")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                        step += 1

                                        print(f"\nTEST STEP {step}: Get the IP address of the LAN client after connecting to it")
                                        print(f"EXPECTED RESULT {step}: Should retrieve IP address for the LAN client")
                                        lanIP = tdkbE2EUtility.getLanIPAddress(tdkbE2EUtility.lan_interface)
                                        if lanIP:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: LAN client IP is {lanIP}")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                            step += 1

                                            print(f"\nTEST STEP {step}: Check whether LAN IP address is in same DHCP range")
                                            print(f"EXPECTED RESULT {step}: LAN IP should be in same DHCP range as gateway")
                                            status = tdkbE2EUtility.checkIpRange(curIPAddress, lanIP)
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: LAN IP is in same DHCP range")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                step += 1

                                                print(f"\nTEST STEP {step}: Verify TCP from WLAN to LAN")
                                                print(f"EXPECTED RESULT {step}: TCP between WLAN and LAN should be success")
                                                status, serverOutput, clientOutput = tdkbE2EUtility.tcp_udpInClients("WLAN","LAN",lanIP,wlanIP)
                                                print(f"Bandwidth received from server: {serverOutput}")
                                                print(f"Bandwidth received from client: {clientOutput}")
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: TCP from WLAN to LAN is Success")
                                                    print("Bandwidth recieved from server is greater than that from client")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    step += 1

                                                    print(f"\nTEST STEP {step}: Disconnect from the wifi ssid from WLAN client")
                                                    print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                                    status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: Failed to disconnect from WIFI SSID")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: TCP from WLAN to LAN failed")
                                                    print("Bandwidth recieved from server is not greater than that from client")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: LAN IP is not in DHCP range")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to get the LAN client IP")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: WLAN IP is not in DHCP range")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get gateway LAN IP")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get the WLAN IP")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to SSID")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: GET operation failed or the parameter values which are SET are not updated")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")

                #Revert operation for security mode
                print("Reverting to initial Security Mode...")
                step += 1
                tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index, initial_config, "Enhanced-Open")
                details = tdkTestObj.getResultDetails()

                print(f"\nTEST STEP {step} : Revert Security Mode to initial security mode : {initial_secMode}")
                print(f"EXPECTED RESULT {step} : Reverting to initial security mode should be success")

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was successful Details : {details}")
                    print("TEST EXECUTION RESULT : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was NOT successful Details : {details}")
                    print("TEST EXECUTION RESULT : FAILURE")

                # Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']

                revertParamList = list1

                revertParamList = "|".join(map(str, revertParamList))
                firewallParam = f"{firewallLevel}|{orgValue[2]}|string"

                # Revert the values to original
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)
                tdkTestObj, firewallResult, details = tdkbE2EUtility.setMultipleParameterValues(obj, firewallParam)
                step += 1

                print(f"\nTEST STEP {step}: Revert ssid and firewall to original values")
                print(f"EXPECTED RESULT {step}: Should set the original ssid and firewallLevel")

                if expectedresult in actualresult and expectedresult in firewallResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Revert operation success. Details: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Revert operation failed. Details: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to retrive Initial security configuration")
                print("TEST EXECUTION RESULT :FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to retrive current ssid, securityMode and firewallLevel")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    wifi_obj.unloadModule("wifiagent")

else:
    print("Failed to load tdkb_e2e/wifi module")
    obj.setLoadModuleStatus("FAILURE")
    wifi_obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
