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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>

obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_ChannelNumber_ManualMode')
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0
    ch_num = '5'

    #Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        channelMode = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.AutoChannelEnable"
        channelNumber = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Channel"

        #Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, channelMode, channelNumber]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        step += 1
        print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase, channel mode, channel number")
        print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase, channel mode, channel number")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current values: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : {status}")

            # Set the ssid, Keypassphrase,auto channel mode and channel number
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, 'false', ch_num]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']
            list3 = [channelMode, 'false', 'boolean']
            list4 = [channelNumber, ch_num, 'unsignedint']

            # Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3 + list4
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)

            step += 1
            print(f"\nTEST STEP {step}: Set the SSID, KeyPassphrase, channel mode, channel number")
            print(f"EXPECTED RESULT {step}: Should set the SSID, KeyPassphrase, channel mode, channel number")

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                newParamList = [ssidName, keyPassPhrase, channelMode, channelNumber]
                tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                step += 1
                print(f"\nTEST STEP {step}: Get the current SSID, KeyPassphrase, channel mode, channel number")
                print(f"EXPECTED RESULT {step}: Should retrieve the current SSID, KeyPassphrase, channel mode, channel number")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Current values after SET: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    step += 1
                    print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: Should connect to the wifi ssid from wlan client")

                    status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Connected to SSID {tdkbE2EUtility.ssid_6ghz_name}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should get the IP address of the wlan client after connecting to wifi")

                        wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Wlan IP: {wlanIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve the current LAN IP address")

                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)
                            print(f"LAN IP Address: {curIPAddress}")

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Current LAN IP address DHCP range: {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: Wlan IP should be in the same DHCP range as LAN IP")

                                status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: Wlan IP {wlanIP} is in the DHCP range of LAN IP {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"\nTEST STEP {step}: Check whether wlan client connected with channel number {ch_num}")
                                    print(f"EXPECTED RESULT {step}: Client should be connected on channel {ch_num}")

                                    channel_number = tdkbE2EUtility.getChannelNumber(tdkbE2EUtility.ssid_6ghz_name)
                                    if channel_number == ch_num:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Client channel: {channel_number}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                        print(f"EXPECTED RESULT {step}: Should disconnect from the wifi ssid from wlan client")

                                        status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Disconnected from SSID {tdkbE2EUtility.ssid_6ghz_name}")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to disconnect from SSID {tdkbE2EUtility.ssid_6ghz_name}")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Client channel: {channel_number}, expected {ch_num}")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Wlan IP {wlanIP} is NOT in DHCP range of LAN IP {curIPAddress}")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to retrieve LAN IP or LAN IP not present: {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get wlan IP after connection")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect to SSID {tdkbE2EUtility.ssid_6ghz_name}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Retrieved values {newValues} do not match set values {setValuesList}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : {actualresult}")

            # Prepare the list of parameter values to be reverted
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']
            list3 = [channelMode, orgValue[2], 'boolean']
            list4 = [channelNumber, orgValue[3], 'unsignedint']

            # Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3 + list4
            revertParamList = "|".join(map(str, revertParamList))

            tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)

            step += 1
            print(f"\nTEST STEP {step}: Revert the SSID, KeyPassphrase, channel mode, channel number to original values")
            print(f"EXPECTED RESULT {step}: Should set the original SSID, KeyPassphrase, channel mode, channel number")

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Revert operation success. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : {actualresult}")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Revert operation failed. Details: {details}")
                print(f"[TEST EXECUTION RESULT] : {actualresult}")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: GET operation failed")
            print(f"[TEST EXECUTION RESULT] : {status}")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

