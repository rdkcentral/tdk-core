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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_LANtoWLAN_Telnet_OpenSecurity')
wifi_obj.configureTestCase(ip,port,'E2E_WIFI_6GHZ_LANtoWLAN_Telnet_OpenSecurity')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 = wifi_obj.getLoadModuleResult()

print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 1

    #Parse the device configuration file
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")

    status = tdkbE2EUtility.parseDeviceConfig(obj)

    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")
        step += 1

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"
        radioEnable = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_6ghz_index}.Enable"
        ssidEnable = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.Enable"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,securityMode,radioEnable,ssidEnable]

        print(f"\nTEST STEP {step}: Get the current ssid,securityMode,radioEnable and ssidEnable")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,securityMode,radioEnable and ssidEnable")

        tdkTestObj,status,orgValue = tdkbE2EUtility.getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Retrived current values. The values: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")
            initial_secMode = orgValue[1]

            #Get the initial security configuration
            step += 1
            print(f"\nTEST STEP {step}: Get the initial security configuration")
            print(f"EXPECTED RESULT {step}: Should successfully get initial security configuration")
            initial_config = {}
            tdkTestObj,actualresult,initial_config = tdkutility.getSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index)

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Initial security configuration reterived successfully. Initial config values: {initial_config}")
                print("TEST EXECUTION RESULT :SUCCESS")

                step += 1
                # Set ssid,securityMode, radioEnable and ssidEnable for 2.4ghz"
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name,'Enhanced-Open','true','true']
                print(f"WIFI parameter values that are set: {setValuesList}")

                list1 = [ssidName,tdkbE2EUtility.ssid_6ghz_name,'string']
                list2 = [securityMode, 'Enhanced-Open', 'string']
                list3 = [radioEnable,'true','bool']
                list4 = [ssidEnable,'true','bool']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2 + list3 + list4
                setParamList = "|".join(map(str, setParamList))

                print(f"\nTEST STEP {step}: Set the ssid, securityMode, radioEnable and ssidEnable")
                print(f"EXPECTED RESULT {step}: Should set the ssid,securityMode,radioEnable and ssidEnable")

                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                    step += 1

                    #Retrieve the values after set and compare
                    newParamList=[ssidName,securityMode,radioEnable,ssidEnable]

                    print(f"\nTEST STEP {step}: Get the current ssid,securityMode,radioEnable and ssidEnable after setting")
                    print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,securityMode,radioEnable and ssidEnable and match with set values")

                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: The parameter values after SET :{newValues}")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                        step += 1

                        #Wait for the changes to reflect in client device
                        time.sleep(60)

                        # Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"\nTEST STEP {step}: From wlan client, connect to the wifi ssid")
                        print(f"EXPECTED RESULT {step}: Wlan client should connect successfully")
                        status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd, tdkbE2EUtility.wlan_6ghz_interface,"Open")

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: {status}")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"\nTEST STEP {step}: Get the IP address of the wlan client")
                            print(f"EXPECTED RESULT {step}: Should retrieve the wlan IP")
                            wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)

                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN IP Address: {wlanIP}")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                                print(f"EXPECTED RESULT {step}: Should retrieve the LAN IP address")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = tdkbE2EUtility.getParameterValue(obj, param)

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"LAN IP Address: {curIPAddress}")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"\nTEST STEP {step}: Check whether wlan ip is in the same DHCP range")
                                    print(f"EXPECTED RESULT {step}: Wlan IP should be in the DHCP range")
                                    status = tdkbE2EUtility.checkIpRange(curIPAddress, wlanIP)

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: {status}")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                        step += 1
                                        print(f"\nTEST STEP {step}: Get the IP address of the lan client")
                                        print(f"EXPECTED RESULT {step}: Should retrieve the lan client IP")
                                        lanIP = tdkbE2EUtility.getLanIPAddress(tdkbE2EUtility.lan_interface)

                                        if lanIP:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: LAN Client IP Address: {lanIP}")
                                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                            step += 1
                                            print(f"\nTEST STEP {step}: Check whether lan ip is in the same DHCP range")
                                            print(f"EXPECTED RESULT {step}: Lan IP should be in the DHCP range")
                                            status = tdkbE2EUtility.checkIpRange(curIPAddress, lanIP)

                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: {status}")
                                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                                step += 1
                                                print(f"\nTEST STEP {step}: Check Telnet traffic between wired and wireless clients")
                                                print(f"EXPECTED RESULT {step}: Telnet traffic should be success")
                                                status = tdkbE2EUtility.telnetToClient("WLAN", wlanIP)
                                                if "SUCCESS" in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: Telnet traffic successful between wired and wireless clients")
                                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                                    # Disconnect WLAN
                                                    step += 1
                                                    print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                                    print(f"EXPECTED RESULT {step}: WLAN client should disconnect successfully")
                                                    status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: WLAN disconnected successfully")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: WLAN disconnect failed")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: Telnet status:{status}")
                                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                                                    print("FAILURE: Telnet traffic not successful between wired and wireless clients")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Lan IP not in DHCP range")
                                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to get lan IP")
                                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Wlan IP not in DHCP range")
                                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get LAN IP address")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get wlan IP")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Wlan client connection failed")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: GET operation failed or Parameter values are not updated after SET ")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")

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


                #Prepare the list of parameter values to be reverted
                list1 = [ssidName,orgValue[0],'string']
                list3 = [radioEnable,orgValue[2],'bool']
                list4 = [ssidEnable,orgValue[3],'bool']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list3 + list4
                revertParamList = "|".join(map(str, revertParamList))

                step += 1
                print(f"\nTEST STEP {step}: Revert to original WiFi parameter values")
                print(f"EXPECTED RESULT {step}: Should successfully revert to original ssid,radioEnable and ssidEnable")

                #Revert the values to original
                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,revertParamList)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to retrive Initial security configuration")
                print("TEST EXECUTION RESULT :FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to retrive current values")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"[TEST EXECUTION RESULT] : FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    wifi_obj.unloadModule("wifiagent")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    wifi_obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")
