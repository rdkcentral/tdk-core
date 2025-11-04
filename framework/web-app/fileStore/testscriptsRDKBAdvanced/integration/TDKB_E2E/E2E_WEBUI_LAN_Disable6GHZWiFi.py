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
import tdkbWEBUIUtility

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_Disable6GHZWiFi')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 1
    exit_flag = 0

    # Parse the device configuration file
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)

    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        wifiEnable = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.Enable"
        paramList = [wifiEnable]

        print(f"\nTEST STEP {step}: Get the current WiFi enable status for 6GHz")
        print(f"EXPECTED RESULT {step}: Should retrieve the current WiFi enable status")
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current WiFi enable status is {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")

            if orgValue[0] == "false":
                setValuesList = ['true']
                print(f"WIFI parameter values to be set: {setValuesList}")
                setParamList = f"{wifiEnable}|true|bool"

                step += 1
                print(f"\nTEST STEP {step}: Set the WiFi enable status to true")
                print(f"EXPECTED RESULT {step}: Should set the WiFi enable status to true")

                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: SET operation success{details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    newParamList = [wifiEnable]
                    step += 1
                    print(f"\nTEST STEP {step}: Verify if the WiFi enable status is updated to true")
                    print(f"EXPECTED RESULT {step}: The WiFi enable status should be true")

                    tdkTestObj, status, newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WiFi enable status is {newValues}")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                        time.sleep(60)
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to set WiFi enable status to true")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                        exit_flag = 1
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: SET operation failed")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                    exit_flag = 1
            else:
                print("Changing wifi enable is not required")

            if exit_flag != 1:
                step += 1
                print(f"\nTEST STEP {step}: Get the IP address of the LAN client after connecting to it")
                print(f"EXPECTED RESULT {step}: Should retrieve valid LAN client IP address")
                lanIP = tdkbE2EUtility.getLanIPAddress(tdkbE2EUtility.lan_interface)

                if lanIP:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: LAN Client IP Address is {lanIP}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    step += 1
                    print(f"\nTEST STEP {step}: Get the current LAN IP address (gateway) DHCP range")
                    print(f"EXPECTED RESULT {step}: Should retrieve valid LAN gateway IP address")

                    param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                    tdkTestObj, status, curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)
                    print(f"ACTUAL RESULT {step}: Current LAN Gateway IP is {curIPAddress}")

                    if expectedresult in status and curIPAddress:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Check if LAN IP is in the same DHCP range")
                        print(f"EXPECTED RESULT {step}: LAN client IP should be in same DHCP range")

                        status = tdkbE2EUtility.checkIpRange(curIPAddress, lanIP)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: LAN IP is in the same DHCP range")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"\nTEST STEP {step}: Start Selenium Grid and perform WiFi disable operation in Web UI")
                            print(f"EXPECTED RESULT {step}: Selenium grid should start and WiFi should be disabled successfully in UI")

                            driver, status = tdkbWEBUIUtility.startSeleniumGrid(tdkTestObj, "LAN", tdkbE2EUtility.grid_url)
                            if status == "SUCCESS":
                                try:
                                    time.sleep(10)
                                    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/a').click()
                                    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/ul/li[4]").click()
                                    time.sleep(10)
                                    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/table/tbody/tr[4]/td[5]/a").click()
                                    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/form/div[1]/span[2]/ul/a[2]/li/label").click()
                                    driver.find_element_by_id("save_settings").submit()
                                    time.sleep(10)
                                    driver.quit()
                                    print(f"ACTUAL RESULT {step}: WiFi disable action performed in Web UI")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"\nTEST STEP {step}: Check if 6GHz SSID is visible in WiFi client list")
                                    print(f"EXPECTED RESULT {step}: SSID should not be broadcasted after disabling 6GHz WiFi")

                                    status = tdkbE2EUtility.wlanIsSSIDAvailable(tdkbE2EUtility.ssid_6ghz_name)
                                    if expectedresult not in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: SSID {tdkbE2EUtility.ssid_6ghz_name} is not broadcasted")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: SSID {tdkbE2EUtility.ssid_6ghz_name} is still broadcasted")
                                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                                except Exception as error:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Exception occurred{error}")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to start Selenium Grid")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")

                            step += 1
                            print(f"\nTEST STEP {step}: Kill Selenium Hub and Node post execution")
                            print(f"EXPECTED RESULT {step}: Selenium Hub and Node should stop successfully")

                            status = tdkbWEBUIUtility.kill_hub_node("LAN")
                            if status == "SUCCESS":
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Post-requisite cleanup success")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Could not kill node and hub")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: LAN IP address not in DHCP range")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to get gateway LAN IP")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to get LAN client IP")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")

                step += 1
                print(f"\nTEST STEP {step}: Revert WiFi enable status to original value")
                print(f"EXPECTED RESULT {step}: Should revert WiFi enable status to {orgValue[0]}")

                revertParamList = f"{wifiEnable}|{orgValue[0]}|bool"
                tdkTestObj, actualresult, details = tdkbE2EUtility.setMultipleParameterValues(obj, revertParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("Not proceeding further")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to get current WiFi enable status")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print(f"[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
