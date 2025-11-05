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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
import tdkutility
import tdkbVariables

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_ConnectWiFi_GetAssociatedDeviceNumberOfEntries')
wifi_obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_ConnectWiFi_GetAssociatedDeviceNumberOfEntries')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = wifi_obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  : {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    exit_flag = 0
    sm_flag = 0
    step = 1

    # Parse the device configuration file
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        radioEnable = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Enable"
        encryptionMethod = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.X_CISCO_COM_EncryptionMethod"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, radioEnable, encryptionMethod, securityMode]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase, Radio status, encryption method, security mode")
        print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase, Radio status, encryption method, security mode")
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: The current values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            initial_secMode = orgValue[4]

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
                # Set the security mode as WPA3-Personal and encryption method as "AES"
                step += 1
                setValuesList = ['true', tdkbE2EUtility.ssid_6ghz_name, 'AES', tdkbE2EUtility.ssid_6ghz_pwd]
                print(f"\nWIFI parameter values that are set: {setValuesList}")

                list1 = [radioEnable, 'true', 'boolean']
                list2 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                list3 = [encryptionMethod, 'AES', 'string']
                list4 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

                # Concatenate the lists with the elements separated by pipe
                #if initial security mode is not WPA3-Personal no need to change Encryption mode it be changed in above security mode SET operation
                if initial_secMode != "WPA3-Personal":
                    setParamList = "|".join(map(str, list1 + list2 + list4))
                else:
                    setParamList = "|".join(map(str, list1 + list2 + list3 + list4))

                print(f"\nTEST STEP {step}: Set the SSID, KeyPassphrase, Radio status, encryption method")
                print(f"EXPECTED RESULT {step}: Should set the SSID, KeyPassphrase, Radio status, encryption method")
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                    step += 1

                    # Retrieve the values after set and compare
                    newParamList = [radioEnable, ssidName, encryptionMethod, keyPassPhrase]
                    tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                    print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase, Radio status, encryption method after set")
                    print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase, Radio status, encryption method")
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}:The parameter values after SET : {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                        step += 1

                        # Wait for the changes to reflect in client device
                        time.sleep(60)

                        # Get current AssociatedDeviceNumberOfEntries before connecting to WIFI
                        print(f"\nTEST STEP {step}: Get the current Associated number of entries before connecting to WIFI")
                        print(f"EXPECTED RESULT {step}: Should get the Associated number of entries before connecting")
                        param = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.AssociatedDeviceNumberOfEntries"
                        tdkTestObj, status, associatedNumberOfEntries = tdkbE2EUtility.getParameterValue(obj, param)

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Current Associated number of entries: {associatedNumberOfEntries}")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            # Connect to the wifi ssid from wlan client using valid wifi password
                            step += 1
                            print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid using valid wifi password")
                            print(f"EXPECTED RESULT {step}: WLAN client should connect successfully")
                            status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                step += 1

                                # Get the IP address of the wlan client
                                print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                                print(f"EXPECTED RESULT {step}: Should retrieve WLAN IP address")
                                wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                                if wlanIP:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP: {wlanIP}")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                    step += 1

                                    # Get AssociatedDeviceNumberOfEntries after connecting
                                    print(f"\nTEST STEP {step}: Get the current Associated number of entries after connecting to WIFI")
                                    print(f"EXPECTED RESULT {step}: Should get the Associated number of entries after connecting")
                                    param = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.AssociatedDeviceNumberOfEntries"
                                    tdkTestObj, status, associatedNumberOfEntriesAfterWiFiConnect = tdkbE2EUtility.getParameterValue(obj, param)

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Current Associated number of entries: {associatedNumberOfEntriesAfterWiFiConnect}")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        # Check AssociatedDeviceNumberOfEntries incremented or not
                                        print(f"\nTEST STEP {step}: Verify Associated number of entries incremented by 1")
                                        print(f"EXPECTED RESULT {step}: Associated number of entries should increment by 1 after wifi connect")
                                        if expectedresult in status and (int(associatedNumberOfEntries) + 1) == int(associatedNumberOfEntriesAfterWiFiConnect):
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Associated number of entries incremented after wifi connect")
                                            print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                            step += 1

                                            # Disconnect WLAN client
                                            print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                            print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: WLAN client disconnected successfully")
                                                print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to Disconnect from the wifi ssid")
                                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Associated number of entries not incremented / Failed to verify")
                                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Failed to get current Associated number of entries")
                                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get WLAN IP address")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: WLAN client failed to connect")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get Associated number of entries before connecting")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: GET opertaion failed or current values after set do not match expected")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to set parameters: {details}")
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

                # Revert values to original
                step += 1
                print(f"\nTEST STEP {step}: Revert the values of SSID, KeyPassphrase, Radio status, encryption method to original")
                print(f"EXPECTED RESULT {step}: Should set the original SSID, KeyPassphrase, Radio status, encryption method")
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']
                list3 = [radioEnable, orgValue[2], 'boolean']
                list4 = [encryptionMethod, orgValue[3], 'string']
                if sm_flag == 1:
                    revertParamList = "|".join(map(str, list1 + list3))
                else:
                    revertParamList = "|".join(map(str, list1 + list2 + list3 + list4))
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Revert operation success. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to revert values. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("Not proceeding further as SET operation for security mode failed")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: GET operation failed")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")
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


