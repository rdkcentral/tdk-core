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
obj.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Block6_Allow2.4_WIFIClient')
obj1.configureTestCase(ip,port,'E2E_WIFI_MACFilter_Block6_Allow2.4_WIFIClient')

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

        # Assign the WIFI parameters names to a variables
        ssidName2_g = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_2ghz_index}.SSID"
        keyPassPhrase2_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.Security.KeyPassphrase"
        radioEnable2_g = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_2ghz_index}.Enable"
        macFilterEnable2_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MACFilter.Enable"
        macFilterBlackList2_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MACFilter.FilterAsBlackList"

        ssidName6_g = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase6_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        radioEnable6_g = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Enable"
        macFilterEnable6_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MACFilter.Enable"
        macFilterBlackList6_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MACFilter.FilterAsBlackList"

        # Get the value of the wifi parameters that are currently set.
        paramList = [
            ssidName2_g, keyPassPhrase2_g, radioEnable2_g, macFilterEnable2_g, macFilterBlackList2_g,
            ssidName6_g, keyPassPhrase6_g, radioEnable6_g, macFilterEnable6_g, macFilterBlackList6_g
        ]
        tdkTestObj, status, orgValue = tdkbE2EUtility.getMultipleParameterValues(obj, paramList)
        step += 1
        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase, Radio enable status, macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set the SSID name,Keypassphrase,Radio enable status for 2.4 ghz and 6ghz
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true',tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,'true']
            print(f"Parameter values that are set: {setValuesList}" )

            list1 = [ssidName2_g,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase2_g,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [radioEnable2_g,'true','bool']

            list4 = [ssidName6_g,tdkbE2EUtility.ssid_6ghz_name,'string']
            list5 = [keyPassPhrase6_g,tdkbE2EUtility.ssid_6ghz_pwd,'string']
            list6 = [radioEnable6_g,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList2_g = list1 + list2 + list3
            setParamList6_g = list4 + list5 + list6
            setParamList2_g = "|".join(map(str, setParamList2_g))
            setParamList6_g = "|".join(map(str, setParamList6_g))

            tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList2_g)
            tdkTestObj,actualresult1,details1 = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList6_g)

            step += 1
            print(f"\nTEST STEP {step}: Set the ssid, keypassphrase, Radio enable status for 2.4ghz and 6ghz")
            print(f"EXPECTED RESULT {step}: Should set the ssid, keypassphrase, Radio enable status for 2.4ghz and 6ghz")

            if expectedresult in actualresult and expectedresult in actualresult1:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                newParamList=[ssidName2_g,keyPassPhrase2_g,radioEnable2_g,ssidName6_g,keyPassPhrase6_g,radioEnable6_g]
                tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                step += 1
                print(f"\nTEST STEP {step}: Get the current ssid, keypassphrase, Radio enable status for 2.4ghz and 6ghz")
                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keypassphrase, Radio enable status for 2.4ghz and 6ghz")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Current values: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Connect to the 2.4ghz wifi ssid from wlan client
                    step += 1
                    print(f"\nTEST STEP {step}: Connect to the 2.4ghz wifi ssid from WLAN client")
                    print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                    status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve a valid IP address for the wlan client")
                        wlanIP_2ghz = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface)
                        if wlanIP_2ghz:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: WLAN client IP is {wlanIP_2ghz}")
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
                                status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP_2ghz)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #From the client, get its MAC
                                    step += 1
                                    print(f"\nTEST STEP {step}: Get MAC address of WLAN client")
                                    print(f"EXPECTED RESULT {step}: Should get MAC address of WLAN client ")
                                    MAC_2GHZ = tdkbE2EUtility.getWlanMACAddress(tdkbE2EUtility.wlan_2ghz_interface)

                                    if MAC_2GHZ:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: MAC address of 2ghz WLAN client is {MAC_2GHZ}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        print(f"\nTEST STEP {step}: Disconnect WLAN client from the 2.4ghz wifi ssid")
                                        print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                        status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            # Connect to the 6ghz wifi ssid from wlan client
                                            step += 1
                                            print(f"\nTEST STEP {step}: Connect to the 6ghz wifi ssid from WLAN client")
                                            print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                                            status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)

                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                step += 1
                                                print(f"\nTEST STEP {step}: Get the IP address of the WLAN client after connecting to wifi")
                                                print(f"EXPECTED RESULT {step}: Should retrieve a valid IP address for the wlan client")
                                                wlanIP_6ghz = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                                                if wlanIP_6ghz:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: WLAN client IP is {wlanIP_6ghz}")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                    step += 1
                                                    print(f"\nTEST STEP {step}: Check whether WLAN IP address is in same DHCP range")
                                                    print(f"EXPECTED RESULT {step}: WLAN IP should be in same DHCP range as LAN")
                                                    status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP_6ghz)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: WLAN IP is in same DHCP range")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                        #From the client, get its MAC
                                                        step += 1
                                                        print(f"\nTEST STEP {step}: Get MAC address of WLAN client")
                                                        print(f"EXPECTED RESULT {step}: Should get MAC address of WLAN client ")
                                                        MAC_6GHZ = tdkbE2EUtility.getWlanMACAddress(tdkbE2EUtility.wlan_6ghz_interface)

                                                        if MAC_6GHZ:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: MAC address of 6ghz WLAN client is {MAC_6GHZ}")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                            step += 1
                                                            print(f"\nTEST STEP {step}: Disconnect WLAN client from the 6ghz wifi ssid")
                                                            print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                # Set macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz
                                                                setValuesList = ['true','false','true','true']
                                                                print(f"Parameter values that are set: {setValuesList}")

                                                                list1 = [macFilterEnable2_g,'true','bool']
                                                                list2 = [macFilterBlackList2_g,'false','bool']

                                                                list3 = [macFilterEnable6_g,'true','bool']
                                                                list4 = [macFilterBlackList6_g,'true','bool']

                                                                #Concatenate the lists with the elements separated by pipe
                                                                setParamList2_g = list1 + list2
                                                                setParamList6_g = list3 + list4
                                                                setParamList2_g = "|".join(map(str, setParamList2_g))
                                                                setParamList6_g = "|".join(map(str, setParamList6_g))

                                                                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList2_g)
                                                                tdkTestObj,actualresult1,details1= tdkbE2EUtility.setMultipleParameterValues(obj,setParamList6_g)

                                                                step += 1
                                                                print(f"\nTEST STEP {step}: Set macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")
                                                                print(f"EXPECTED RESULT {step}: Should set the macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")

                                                                if expectedresult in actualresult and expectedresult in actualresult1:
                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                    print(f"ACTUAL RESULT {step}: SET operation success")
                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                    #Retrieve the values after set and compare
                                                                    newParamList=[macFilterEnable2_g,macFilterBlackList2_g,macFilterEnable6_g,macFilterBlackList6_g]
                                                                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                                                                    step += 1
                                                                    print(f"\nTEST STEP {step}: Get the current macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")
                                                                    print(f"EXPECTED RESULT {step}: Should Get the macFilterEnable, macFilterBlackList for 2.4ghz and 6ghz")

                                                                    if expectedresult in status and setValuesList == newValues:
                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                        print(f"ACTUAL RESULT {step}: The parameter values after set :{newValues}")
                                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                        # Adding a new MACFilter rule for 2.4 GHz
                                                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                                                        tdkTestObj.addParameter("paramName",f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MacFilterTable.")
                                                                        tdkTestObj.executeTestCase(expectedresult)
                                                                        actualresult = tdkTestObj.getResult()
                                                                        details = tdkTestObj.getResultDetails()

                                                                        step += 1
                                                                        print(f"\nTEST STEP {step}: Add a new MACFilter rule for 2.4 GHz")
                                                                        print(f"EXPECTED RESULT {step}: Should add new rule")
                                                                        if expectedresult in actualresult:
                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                            print(f"ACTUAL RESULT {step}: Added new rule. Details: {details}")
                                                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                            temp = details.split(':')
                                                                            instance2_g= temp[1]
                                                                            print(f"2.4ghz INSTANCE VALUE: {instance2_g}")

                                                                            if (int(instance2_g) > 0):
                                                                                #Adding a new MACFilter rule for 6GHz
                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                                                                tdkTestObj.addParameter("paramName",f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.")
                                                                                tdkTestObj.executeTestCase(expectedresult)
                                                                                actualresult = tdkTestObj.getResult()
                                                                                details = tdkTestObj.getResultDetails()
                                                                                step += 1
                                                                                print(f"\nTEST STEP {step}: Add a new MACFilter rule for 6GHz")
                                                                                print(f"EXPECTED RESULT {step}: Should add new rule")
                                                                                if expectedresult in actualresult:
                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                    print(f"ACTUAL RESULT {step}: Added new rule. Details: {details}")
                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                    temp = details.split(':')
                                                                                    instance6_g= temp[1]
                                                                                    print(f"6ghz INSTANCE VALUE: {instance6_g}")

                                                                                    if (int(instance6_g) > 0):
                                                                                        #Set the name and MAC of the device name to be blocked
                                                                                        deviceName2_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MacFilterTable.{instance2_g}.DeviceName"
                                                                                        deviceMAC2_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MacFilterTable.{instance2_g}.MACAddress"
                                                                                        deviceName6_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance6_g}.DeviceName"
                                                                                        deviceMAC6_g = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance6_g}.MACAddress"

                                                                                        setValuesList = [tdkbE2EUtility.ssid_2ghz_name, MAC_2GHZ, tdkbE2EUtility.ssid_6ghz_name, MAC_6GHZ]

                                                                                        # Print parameter values using f-string
                                                                                        print(f"Parameter values that are set: {setValuesList}")

                                                                                        list1 = [deviceName2_g, tdkbE2EUtility.ssid_2ghz_name, 'string']
                                                                                        list2 = [deviceMAC2_g, MAC_2GHZ, 'string']
                                                                                        list3 = [deviceName6_g, tdkbE2EUtility.ssid_6ghz_name, 'string']
                                                                                        list4 = [deviceMAC6_g, MAC_6GHZ, 'string']

                                                                                        # Concatenate the lists with elements separated by pipe
                                                                                        setParamList2_g = "|".join(map(str, list1 + list2))
                                                                                        setParamList6_g = "|".join(map(str, list3 + list4))

                                                                                        step += 1
                                                                                        print(f"\nTEST STEP {step}: Set the name and MAC of client device in the filter")
                                                                                        print(f"EXPECTED RESULT {step}: Should set the name and MAC of client device in the filter")

                                                                                        tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList2_g)
                                                                                        tdkTestObj,actualresult1,details1 = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList6_g)

                                                                                        if expectedresult in actualresult and expectedresult in actualresult1:
                                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                                            print(f"ACTUAL RESULT {step}: SET operation success")
                                                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                            #Retrieve the values after set and compare
                                                                                            newParamList=[deviceName2_g,deviceMAC2_g,deviceName6_g,deviceMAC6_g]

                                                                                            step += 1
                                                                                            print(f"\nTEST STEP {step}: Get the current value of name and MAC of client device in the filter")
                                                                                            print(f"EXPECTED RESULT {step}: Should retrieve the current name and mac of client device in the filter")

                                                                                            tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)
                                                                                            print(f"Debug_NewValues {newValues}")
                                                                                            newValues[1] = newValues[1].lower()
                                                                                            newValues[3] = newValues[3].lower()
                                                                                            if expectedresult in status and setValuesList == newValues:
                                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                                print(f"ACTUAL RESULT {step}: The parameter values after set :{newValues}")
                                                                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                                #Wait for the changes to reflect in client device
                                                                                                time.sleep(60)

                                                                                                # Connect to the 2.4ghz wifi ssid from wlan client
                                                                                                step += 1
                                                                                                print(f"\nTEST STEP {step}: Connect to the 2.4ghz wifi ssid from WLAN client")
                                                                                                print(f"EXPECTED RESULT {step}: Wlan client should connect to the wifi ssid")
                                                                                                status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface)

                                                                                                if expectedresult in status:
                                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                                    print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                                    step += 1
                                                                                                    print(f"\nTEST STEP {step}: Disconnect WLAN client from the 2.4ghz wifi ssid")
                                                                                                    print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                                                                                    status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface)
                                                                                                    if expectedresult in status:
                                                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                                                        print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                                                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                                        # Connect to the 6ghz wifi ssid from wlan client
                                                                                                        step += 1
                                                                                                        print(f"\nTEST STEP {step}: Connect to the 6ghz wifi ssid from WLAN client")
                                                                                                        print(f"EXPECTED RESULT {step}: Wlan client should not connect to the wifi ssid")
                                                                                                        status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)

                                                                                                        if expectedresult not in status:
                                                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                                                            print(f"ACTUAL RESULT {step}: Connection attempt for 6ghz ssid should fail after enabling the MAC filter")
                                                                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                                            step += 1
                                                                                                            print(f"\nTEST STEP {step}: Disconnect WLAN client from the 6ghz wifi ssid")
                                                                                                            print(f"EXPECTED RESULT {step}: Wlan client should disconnect successfully")
                                                                                                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                                                                            if expectedresult in status:
                                                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                                                print(f"ACTUAL RESULT {step}: Disconnected from WIFI SSID successfully")
                                                                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                                            else:
                                                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                                                print(f"ACTUAL RESULT {step}: Failed to disconnect from 6ghz WIFI SSID")
                                                                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                                        else:
                                                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                                                            print(f"ACTUAL RESULT {step}: Connection from wlan client to 6ghz ssid is success even after enabling the MAC filter")
                                                                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                                    else:
                                                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                                                        print(f"ACTUAL RESULT {step}: Failed to disconnect from 2.4ghz WIFI SSID")
                                                                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                                else:
                                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                                    print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to 2.4ghz SSID")
                                                                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                            else:
                                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                                print(f"ACTUAL RESULT {step}: Failed to get the current values")
                                                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                        else:
                                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                                            print(f"ACTUAL RESULT {step}: SET operation failed")
                                                                                            print("[TEST EXECUTION RESULT] : FAILURE")

                                                                                        #Delete the created table entry
                                                                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                                                        tdkTestObj.addParameter("paramName",f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.X_CISCO_COM_MacFilterTable.{instance6_g}." )
                                                                                        tdkTestObj.executeTestCase(expectedresult)
                                                                                        actualresult = tdkTestObj.getResult()
                                                                                        details = tdkTestObj.getResultDetails()

                                                                                        step += 1
                                                                                        print(f"\nTEST STEP {step}: Delete the added rule for 6ghz")
                                                                                        print(f"EXPECTED RESULT {step}: Should delete the added rule")

                                                                                        if expectedresult in actualresult:
                                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                                            print(f"ACTUAL RESULT {step}: Deleted the added rule successfully ")
                                                                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                        else:
                                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                                            print(f"ACTUAL RESULT {step}: Failed to delete the added rule. Details: {details}")
                                                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                    else:
                                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                                        print(f"Invalid INSTANCE VALUE returned for 6ghz: {instance6_g}")
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                    print(f"ACTUAL RESULT {step}: Failed to add new rule")
                                                                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                                                                #Delete the created table entry
                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                                                tdkTestObj.addParameter("paramName",f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.X_CISCO_COM_MacFilterTable.{instance2_g}." )
                                                                                tdkTestObj.executeTestCase(expectedresult)
                                                                                actualresult = tdkTestObj.getResult()
                                                                                details = tdkTestObj.getResultDetails()

                                                                                step += 1
                                                                                print(f"\nTEST STEP {step}: Delete the added rule for 2.4ghz")
                                                                                print(f"EXPECTED RESULT {step}: Should delete the added rule")

                                                                                if expectedresult in actualresult:
                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                    print(f"ACTUAL RESULT {step}: Deleted the added rule successfully ")
                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                    print(f"ACTUAL RESULT {step}: Failed to delete the added rule. Details: {details}")
                                                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                                            else:
                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                print(f"Invalid INSTANCE VALUE returned for 2.4ghz: {instance2_g}")
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            print(f"ACTUAL RESULT {step}: Failed to add new rule")
                                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                        print(f"ACTUAL RESULT {step}: GET operation failed/parameter values are not reflected in GET")
                                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    print(f"ACTUAL RESULT {step}: SET operation failed")
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
                                                    print(f"ACTUAL RESULT {step}: Failed to get the WLAN IP")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to  6ghz SSID")
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
                        print(f"ACTUAL RESULT {step}: Failed to connect WLAN client to 2.4 ghz SSID")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: GET operation failed/ parameter values are not updated after SET")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            #Prepare the list of parameter values to be reverted
            list1 = [ssidName2_g,orgValue[0],'string']
            list2 = [keyPassPhrase2_g,orgValue[1],'string']
            list3 = [radioEnable2_g,orgValue[2],'bool']
            list4 = [macFilterEnable2_g,orgValue[3],'bool']
            list5 = [macFilterBlackList2_g,orgValue[4],'bool']

            list6 = [ssidName6_g,orgValue[5],'string']
            list7 = [keyPassPhrase6_g,orgValue[6],'string']
            list8 = [radioEnable6_g,orgValue[7],'bool']
            list9 = [macFilterEnable6_g,orgValue[8],'bool']
            list10 = [macFilterBlackList6_g,orgValue[9],'bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList2_g = list1 + list2 + list3 + list4 + list5
            setParamList6_g = list6 + list7 + list8 + list9 + list10
            setParamList2_g = "|".join(map(str, setParamList2_g))
            setParamList6_g = "|".join(map(str, setParamList6_g))

            step += 1
            print(f"\nTEST STEP {step}: Revert the parameter values to original values")
            print(f"EXPECTED RESULT {step}: Should revert the parameter values to original values")
            tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList2_g)
            tdkTestObj,actualresult1,details1 = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList6_g)

            if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Reverted the parameter values to original values")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to revert the parameter values to original values.Details: {details}, Details1:{details1}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to retrieve the current values")
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
    print("Failed to load tdkb_e2e/advancedconfig module")
    print("Module loading failed")
