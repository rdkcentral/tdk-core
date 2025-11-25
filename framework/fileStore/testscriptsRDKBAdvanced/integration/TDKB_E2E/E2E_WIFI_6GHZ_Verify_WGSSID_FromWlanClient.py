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

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_Verify_WGSSID_FromWlanClient')


# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0

    # Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        step += 1
        print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase")
        print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current values: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")

            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            # Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)

            step += 1
            print(f"\nTEST STEP {step}: Set the SSID, KeyPassphrase")
            print(f"EXPECTED RESULT {step}: Should set the SSID, KeyPassphrase")

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : {actualresult}")

                # Retrieve the values after set and compare
                newParamList = [ssidName, keyPassPhrase]
                tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                step += 1
                print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase")
                print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Current values after SET: {newValues}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    step += 1
                    print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid ")
                    print(f"EXPECTED RESULT {step}: Should connect to the wifi ssid")

                    status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Connected to SSID {tdkbE2EUtility.ssid_6ghz_name}")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should get the IP address of the wlan client after connecting to wifi")

                        wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: wlanIP: {wlanIP}")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve the current LAN IP address DHCP range")

                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP address DHCP range: {curIPAddress}")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: wlan ip address should be in same DHCP range")

                                status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    print(f"ACTUAL RESULT {step}: SUCCESS, wlan ip address is in same DHCP range")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                    tdkTestObj.setResultStatus("SUCCESS")

                                    # Get the connected Gateway's SSID from client
                                    step += 1
                                    print(f"\nTEST STEP {step}: Get the SSID of the connected gateway")
                                    print(f"EXPECTED RESULT {step}: Should get the SSID of the connected gateway")
                                    SSID1 = tdkbE2EUtility.getConnectedSsidName(tdkbE2EUtility.wlan_6ghz_interface)

                                    if SSID1:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: SSID of the connected gateway is {SSID1}")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                        # Get the gateway SSID using tr-181 param
                                        step += 1
                                        print(f"\nTEST STEP {step}: Get the SSID of gateway using tr-181")
                                        print(f"EXPECTED RESULT {step}: Should get the SSID of gateway using tr-181")
                                        getSSID = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"

                                        tdkTestObj, status, SSID2 = tdkbE2EUtility.getParameterValue(obj, getSSID)

                                        if expectedresult in status and SSID2:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: {SSID2}")
                                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                            step += 1
                                            print(f"\nTEST STEP {step}: Compare the SSID values")
                                            print(f"EXPECTED RESULT {step}: Both SSID values should be same")

                                            if SSID1.strip() == SSID2.strip():
                                                print(f"ACTUAL RESULT {step}: Both SSID values are same. SSID1: {SSID1},SSID2: {SSID2}")
                                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                                step += 1
                                                print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                                print(f"EXPECTED RESULT {step}: Should disconnect from the wifi ssid from wlan client")

                                                status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: Connection successfully disconnected")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: Failed to Disconnect")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                            else:
                                                print(f"ACTUAL RESULT {step}: Both SSID values are not same. SSID1: {SSID1},SSID2: {SSID2}")
                                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to get gateway ssid through tr-181")
                                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: FAILURE, wlan ip address is not in the same DHCP range")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get the current LAN IP address DHCP range")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the IP address of the wlan client after connecting to wifi")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect from wlan client, to the wifi ssid using valid wifi password")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: GET operation failed/parameter are not updated after SET")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : FAILURE")

            # Prepare the list of parameter values to be reverted
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']

            # Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            # Revert the values to original
            tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)

            step += 1
            print(f"\nTEST STEP {step}: Revert the SSID, KeyPassphrase to original values")
            print(f"EXPECTED RESULT {step}: Should set the original SSID, KeyPassphrase")

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Revert operation success. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Revert operation failed. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: GET operation failed")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")
        print(f"[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

