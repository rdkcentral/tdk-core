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
import tdkbE2EUtility
from tdkbE2EUtility import *
import tdkbWEBUIUtility
from tdkbWEBUIUtility import *

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_WLAN_LoginToUI')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1
    status = "SUCCESS"

    # Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        # Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" % tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" % tdkbE2EUtility.ssid_2ghz_index

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            if tdkbE2EUtility.mlo_capability == "False":
                step += 1
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface

                setValuesList = [tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd]
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName, tdkbE2EUtility.ssid_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_pwd, 'string']

                # Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))

                tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the ssid and keypassphrase")
                    print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Retrieve the values after set and compare
                    newParamList = [ssidName, keyPassPhrase]
                    tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                    step += 1
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                        status = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nTEST STEP {step}: Set the ssid and keypassphrase")
                    print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    status = "FAILURE"
            else:
                print("MLO is enabled in the device configuration file.")

            if status == "SUCCESS":
                # Wait for the changes to reflect in client device
                time.sleep(60)

                # Set Selenium grid
                driver, status = startSeleniumGrid(tdkTestObj, "WLAN", tdkbE2EUtility.grid_url)
                if status == "SUCCESS":

                    # Connect to the wifi ssid from wlan client
                    step += 1
                    print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    status = wlanConnectWifiSsid(
                        tdkbE2EUtility.ssid_name, tdkbE2EUtility.ssid_pwd, tdkbE2EUtility.wlan_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")

                            step += 1
                            print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                            print(f"LAN IP Address: {curIPAddress}")

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")

                                step += 1
                                print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                status = "SUCCESS"
                                status = checkIpRange(curIPAddress, wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    status, driver = openLocalWebUI(
                                        tdkbE2EUtility.grid_url, tdkTestObj, "LocalLogin")
                                    if status == "SUCCESS":
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        finalStatus = "SUCCESS"
                                        time.sleep(10)
                                        driver.quit()
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print("checkIpRange:wlan ip address is not in DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("getParameterValue : Failed to get gateway lan ip")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("getWlanIPAddress:Failed to get the wlan ip address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("wlanConnectWifiSsid: Failed to connect to the wifi ssid")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Failed to set the selenium grid")

                # Kill selenium hub and node
                status = tdkbWEBUIUtility.kill_hub_node("WLAN")
                if status == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("Post-requisite success")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Couldnt kill node and hub")

            if tdkbE2EUtility.mlo_capability == "False":
                # Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']

                # Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                # Revert the values to original
                tdkTestObj, actualresult, details = setMultipleParameterValues(
                    obj, revertParamList)
                step += 1
                if expectedresult in actualresult and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"EXPECTED RESULT {step}: Should set the original ssid and keypassphrase")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"EXPECTED RESULT {step}: Should set the original ssid and keypassphrase")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("MLO is enabled; no SSID/keypassphrase revert is required.")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    # Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")