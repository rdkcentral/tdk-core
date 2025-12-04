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
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Allow_6GHZ_WIFIClient')
obj1.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Allow_6GHZ_WIFIClient')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 =obj1.getLoadModuleResult()

print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0

    # Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable using f-strings
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        radioEnable = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Enable"
        macFilterEnable = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MACFilter.Enable"
        macFilterBlackList = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MACFilter.FilterAsBlackList"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, radioEnable, macFilterEnable, macFilterBlackList]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)

        step += 1
        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set the SSID name,password,Radio enable status ,macFilterEnable, macFilterBlackList
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,'true','true','false']
            print(f"Parameter values that are set: {setValuesList}")

            list1 = [ssidName,tdkbE2EUtility.ssid_6ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_6ghz_pwd,'string']
            list3 = [radioEnable,'true','bool']
            list4 = [macFilterEnable,'true','bool']
            list5 = [macFilterBlackList,'false','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3 + list4 + list5
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)

            step += 1
            print(f"\nTEST STEP {step}: Set the ssid,keypassphrase,Radio enable status,macFilterEnable and macFilterBlackList")
            print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,Radio enable status, macFilterEnable and macFilterBlackList")

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: SET operation success. Details:{details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                newParamList=[ssidName,keyPassPhrase,radioEnable,macFilterEnable,macFilterBlackList]
                tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                step += 1
                print(f"\nTEST STEP {step}:  Get the current SSID, KeyPassphrase, radioEnable, macFilterEnable and macFilterBlackList")
                print(f"EXPECTED RESULT {step}: Should Get the ssid,keypassphrase,Radio enable status ,macFilterEnable and macFilterBlackList")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: The parameter values after set :{newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Connect to the wifi ssid from wlan client
                    step += 1
                    print(f"\nTEST STEP {step}: Connect to the wifi ssid from WLAN client")
                    print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                    status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)

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

                                    #From the client, get its MAC
                                    step += 1
                                    print(f"\nTEST STEP {step}: Get MAC address of WLAN client")
                                    print(f"EXPECTED RESULT {step}: Should get MAC address of WLAN client ")
                                    MAC = tdkbE2EUtility.getWlanMACAddress(tdkbE2EUtility.wlan_6ghz_interface)

                                    if MAC:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: MAC address of WLAN client is {MAC}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        print(f"\nTEST STEP {step}: Disconnect from the wifi ssid from WLAN client")
                                        print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                        status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            # Add a new row to BlockedSite
                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                            tdkTestObj.addParameter("paramName",f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.")
                                            tdkTestObj.executeTestCase(expectedresult)
                                            actualresult = tdkTestObj.getResult()
                                            details = tdkTestObj.getResultDetails()

                                            step += 1
                                            print(f"\nTEST STEP {step}: Add new Mac filter rule")
                                            print(f"EXPECTED RESULT {step}: Should add new rule")

                                            if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: Added new rule. Details: {details}")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                temp = details.split(':')
                                                instance = temp[1]

                                                if (int(instance) > 0):
                                                    # Print instance value using f-string
                                                    print(f"INSTANCE VALUE: {instance}")

                                                    # Set the name and MAC of the device to be blocked using f-strings
                                                    deviceName = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance}.DeviceName"
                                                    deviceMAC = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance}.MACAddress"

                                                    setValuesList = [tdkbE2EUtility.ssid_6ghz_name, MAC]

                                                    # Print parameter values using f-string
                                                    print(f"Parameter values that are set: {setValuesList}")

                                                    list1 = [deviceName, tdkbE2EUtility.ssid_6ghz_name, 'string']
                                                    list2 = [deviceMAC, MAC, 'string']

                                                    # Concatenate the lists with elements separated by pipe
                                                    setParamList = list1 + list2
                                                    setParamList = "|".join(map(str, setParamList))

                                                    tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)

                                                    step += 1
                                                    print(f"\nTEST STEP {step}: Set the name and MAC of client device in the filter")
                                                    print(f"EXPECTED RESULT {step}: Should set the name and MAC of client device in the filter")

                                                    if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: SET operation success. Details:{details}")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                        #Retrieve the values after set and compare
                                                        newParamList=[deviceName,deviceMAC]
                                                        tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj, newParamList)
                                                        newValues[1] = newValues[1].lower()

                                                        step += 1
                                                        print(f"\nTEST STEP {step}: Get the current value of name and MAC of client device in the filter")
                                                        print(f"EXPECTED RESULT {step}: Should retrieve the current name and mac of client device in the filter")

                                                        if expectedresult in status and setValuesList == newValues:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: The parameter values after set :{newValues}")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                            #Wait for the changes to reflect in client device
                                                            time.sleep(60)

                                                            # Connect to the wifi ssid from wlan client
                                                            step += 1
                                                            print(f"\nTEST STEP {step}: Connect to the wifi ssid from WLAN client")
                                                            print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                                                            status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface)

                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
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
                                                                print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to SSID")
                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            print(f"ACTUAL RESULT {step}: Failed to get the current values/current values are not updated after SET: {newValues}")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: Failed to set the name and MAC of client device in the filter. Details: {details}")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")

                                                    # Delete the created table entry
                                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                    tdkTestObj.addParameter("paramName", f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance}.")
                                                    expectedresult = "SUCCESS"
                                                    tdkTestObj.executeTestCase(expectedresult)
                                                    actualresult = tdkTestObj.getResult()
                                                    details = tdkTestObj.getResultDetails()

                                                    step += 1
                                                    print(f"\nTEST STEP {step}: Delete the added rule")
                                                    print(f"EXPECTED RESULT {step}: Should delete the added rule")

                                                    if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: Deleted the added rule. Details: {details}")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: Failed to delete the added rule. Details: {details}")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"Invalid INSTANCE VALUE: {instance}")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to add new rule. Details: {details}")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to disconnect from WIFI SSID")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Failed to get MAC address of WLAN client")
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
                    print(f"ACTUAL RESULT {step}: Get operation failed or parameter values not reflected in GET.")
                    print("TEST EXECUTION RESULT : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: SET operation failed. Details:{details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            #Revert operation for parameters
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [radioEnable,orgValue[2],'bool']
            list4 = [macFilterEnable,orgValue[3],'bool']
            list5 = [macFilterBlackList,orgValue[4],'bool']

            #Concatenate the lists with the elements separated by pipe

            setParamList = list1 + list2 + list3 + list4 + list5
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
            step += 1
            print(f"\nTEST STEP {step} : Set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            print(f"EXPECTED RESULT {step} : Should set the ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList")
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step} : Set operation success. Details : {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step} : Set operation failed. Details : {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to get the current values")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f" ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")
    print("Failed to load tdkb_e2e and advancedconfig module")
    print("Module loading failed")

