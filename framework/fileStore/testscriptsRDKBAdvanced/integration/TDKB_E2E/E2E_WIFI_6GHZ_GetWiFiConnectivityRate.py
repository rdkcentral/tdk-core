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
import tdkbVariables

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_GetWiFiConnectivityRate')
wifi_obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_GetWiFiConnectivityRate')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = wifi_obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    MAX_COUNT = 10
    count = 1
    numberOfSuccessConnections = 0
    exit_flag = 0
    sm_flag = 0
    step = 1

    # Parse the device config file
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)

    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Device configuration file parsed successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"

        print(f"\nTEST STEP {step}: Retrieve the current ssid, keypassphrase, and securityMode values")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase, and securityMode successfully")

        # Get the value of the wifi parameters that are currently set
        paramList = [ssidName, keyPassPhrase, securityMode]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Retrieved values are {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")

            initial_secMode = orgValue[2]

            # Check and change Security Mode to WPA3-Personal if not already
            if initial_secMode != "WPA3-Personal":
                step += 1
                print(f"\nTEST STEP {step}: Get the initial security configuration")
                print(f"EXPECTED RESULT {step}: Should successfully get initial security configuration")
                initial_config = {}
                tdkTestObj, actualresult, initial_config = tdkutility.getSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Initial security configuration retrieved successfully")
                    print("TEST EXECUTION RESULT : SUCCESS")

                    # Set the security mode to WPA3-Personal
                    step += 1
                    print(f"\nTEST STEP {step}: Set security mode to WPA3-Personal")
                    print(f"EXPECTED RESULT {step}: Should set security mode to WPA3-Personal")
                    config_SET = {
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.SAEPassphrase": tdkbVariables.SAE_PASS,
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.X_CISCO_COM_EncryptionMethod": tdkbVariables.ENCRYPTION_MODE
                    }
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, "WPA3-Personal", tdkbE2EUtility.ssid_6ghz_index, config_SET, initial_secMode)
                    details = tdkTestObj.getResultDetails()

                    if expectedresult in actualresult:
                        sm_flag = 1
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Security mode changed to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : SUCCESS")

                        time.sleep(2)
                        # Validate the security mode with get
                        step += 1
                        print(f"\nTEST STEP {step}: Get the Security Mode and check it is changed to WPA3-Personal")
                        print(f"EXPECTED RESULT {step}: Should successfully set security mode to WPA3-Personal")
                        paramName = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"
                        tdkTestObj,actualresult,sec_mode = tdkutility.wifi_GetParam(wifi_obj,paramName)

                        if expectedresult in actualresult and sec_mode == "WPA3-Personal":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Security Mode: {sec_mode}")
                            print("TEST EXECUTION RESULT : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Get operation failed or security mode is not reflected in GET.")
                            print("TEST EXECUTION RESULT : FAILURE")
                            exit_flag = 1
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to set security mode to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : FAILURE")
                        exit_flag = 1
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to retrieve Initial security configuration")
                    print("TEST EXECUTION RESULT : FAILURE")
                    exit_flag = 1
            else:
                print(f"\nChanging Security mode not required as Current security mode is {initial_secMode}")

            if exit_flag != 1:
                # Set ssid and keypassphrase for 6ghz
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

                # Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))

                step += 1
                print(f"\nTEST STEP {step}: Set the ssid and keypassphrase")
                print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase successfully")

                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                    step += 1

                    print(f"\nTEST STEP {step}: Retrieve and compare the ssid, keypassphrase after set")
                    print(f"EXPECTED RESULT {step}: Retrieved values should match the set values")

                    # Retrieve the values after set and compare
                    newParamList = [ssidName, keyPassPhrase]
                    tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Retrieved values after set are {newValues}")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                        step += 1


                        print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                        print(f"EXPECTED RESULT {step}: Should successfully retrieve the current LAN IP address")

                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                        tdkTestObj, status, curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)

                        if expectedresult in status and curIPAddress:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Successfully retrieved LAN IP Address {curIPAddress}")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            print("Waiting for the changes to reflect in client device...")
                            time.sleep(60)

                            #Check wifi connectivity
                            while count <= MAX_COUNT:
                                print(f"\n####################### COUNT NUMBER: {count} ###############################\n")

                                #connect to wlan client to wifi ssid
                                print(f"\nTEST STEP {count}: Connect to the wifi ssid from WLAN client")
                                print(f"EXPECTED RESULT {count}: Wlan client should connect to the wifi ssid")
                                status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {count}: WLAN client connected successfully")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    print(f"\nTEST STEP {count}: Get the IP address of the WLAN client after connecting to wifi")
                                    print(f"EXPECTED RESULT {count}: Should retrieve a valid IP address for the wlan client")
                                    wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                                    if wlanIP:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {count}: WLAN client IP is {wlanIP}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        print(f"\nTEST STEP {count}: Check whether WLAN IP address is in same DHCP range")
                                        print(f"EXPECTED RESULT {count}: WLAN IP should be in same DHCP range as LAN")
                                        status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {count}: WLAN IP is in same DHCP range")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            print(f"\nTEST STEP {count}: Disconnect from the wifi ssid from WLAN client")
                                            print(f"EXPECTED RESULT {count}: Wlan client should disconnect successfully")
                                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {count}: Disconnected from WIFI SSID successfully")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                numberOfSuccessConnections += 1
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {count}: Failed to disconnect from WIFI SSID")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {count}: WLAN IP is not in DHCP range")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {count}: Failed to get the WLAN IP")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {count}: Failed to connect WLAN client to SSID")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                count += 1

                            print(f"Number of successful connections: {numberOfSuccessConnections}")
                            if numberOfSuccessConnections == 10:
                                print("All connections were successful")
                                tdkTestObj.setResultStatus("SUCCESS")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                print("All connections were not successful")
                                tdkTestObj.setResultStatus("FAILURE")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to retrieve LAN IP Address")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: GET operation failed or parameter values are not updated after SET")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to set parameters. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")

                #Revert operation for security mode
                if sm_flag == 1:
                    print("Reverting to initial Security Mode...")
                    step += 1
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index, initial_config, sec_mode)
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
                else:
                    print("\nReverting Security Mode not required...")

                # Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']

                # Concatenate the lists with the elements separated by pipe
                if sm_flag == 1:
                    revertParamList = list1
                else:
                    revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                step += 1
                print(f"\nTEST STEP {step}: Revert the ssid, keypassphrase to original values")
                print(f"EXPECTED RESULT {step}: Should set the original ssid, keypassphrase successfully")

                # Revert the values to original
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Revert operation success. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Revert operation failed. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("Not proceeding further as SET operation for security mode failed")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to retrieve WiFi parameters")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print(f"[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    wifi_obj.unloadModule("wifiagent")

else:
    print("Failed to load tdkb_e2e/wifi module")
    obj.setLoadModuleStatus("FAILURE")
    wifi_obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
