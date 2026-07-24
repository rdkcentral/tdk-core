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
import random
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_PortTriggering_WANtoWLAN_UDP_TargetTFTPWithPTRuleDisabled')
obj1.configureTestCase(ip,port,'E2E_PortTriggering_WANtoWLAN_UDP_TargetTFTPWithPTRuleDisabled')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 =obj1.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1)

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)

    if expectedresult in status:
        print("Parsed the device configuration file successfully")

        #Check if Port Triggering is enabled, else enable the feature
        step = 1
        status, tdkTestObj, revertFlag, step = PTPreRequisite(obj, step)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")

            if tdkbE2EUtility.mlo_capability == "False":
                status = "FAILURE"

                #Assign the WIFI parameters names to a variable
                ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
                keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
                radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index

                #Get the value of the wifi parameters that are currently set.
                step = step + 1
                print("\nTEST STEP %d: Get the current ssid,keypassphrase,Radio enable status" %step)
                print("EXPECTED RESULT %d: Should retrieve the current ssid,keypassphrase,Radio enable status" %step)

                paramList=[ssidName,keyPassPhrase,radioEnable]
                tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("ACTUAL RESULT %d: Values retrieved: %s" %(step, orgValue))
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    # Set the SSID name, KeyPassphrase, Radio enable
                    step = step + 1
                    print("\nTEST STEP %d: Set the ssid, keypassphrase, radio enable" %step)
                    print("EXPECTED RESULT %d: Should set the ssid, keypassphrase, radio enable successfully" %step)
                    setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true']
                    print("Parameter values that are set: %s" %setValuesList)
                    list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                    list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
                    list3 = [radioEnable,'true','bool']

                    #Concatenate the lists with the elements separated by pipe
                    setParamList = list1 + list2 + list3
                    setParamList = "|".join(map(str, setParamList))
                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)

                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("ACTUAL RESULT %d: Details: %s" %(step, details))
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Retrieve the values after set and compare
                        step = step + 1
                        print("\nTEST STEP %d: Get the current ssid, keypassphrase, radio enable" %step)
                        print("EXPECTED RESULT %d: Should retrieve the current ssid, keypassphrase, radio enable" %step)
                        tdkTestObj,status,newValues = getMultipleParameterValues(obj, paramList)

                        if expectedresult in status and setValuesList == newValues:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("ACTUAL RESULT %d: GET values:  %s" %(step, newValues))
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Wait for the changes to reflect in client device
                            time.sleep(60)
                            status = "SUCCESS"
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("ACTUAL RESULT %d: GET values:  %s" %(step, newValues))
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("ACTUAL RESULT %d: Details: %s" %(step, details))
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("ACTUAL RESULT %d: Values not retrieved successfully" %step)
                    print("[TEST EXECUTION RESULT] : FAILURE")

                # Assign SSID, password and interface
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Cannot enable port triggering feature, not proceeding further...")

        if status == "SUCCESS":
            #Connect to the wifi ssid from wlan client
            step = step + 1
            print("\nTEST STEP %d: From wlan client, connect to the WiFi SSID" %step)
            print("EXPECTED RESULT %d: The wlan client should be successfully connected to the WiFi SSID" %step)
            status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print("ACTUAL RESULT %d: Wlan client successfully connected to WiFi SSID" %(step))
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Get the WLAN IP address of connected client
                step = step + 1
                print("\nTEST STEP %d: Get the WLAN IP address of the connected client" %step)
                print("EXPECTED RESULT %d: The current WLAN IP address of the connected client should be obtained" %step)
                wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)

                if wlanIP != "":
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("ACTUAL RESULT %d : Current WLAN IP address is obtained as %s" %(step, wlanIP))
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Check if the current Wlan IP is in the DHCP range
                    step = step + 1
                    print("\nTEST STEP %d: Check if the current WLAN IP address is in DHCP range" %step)
                    print("EXPECTED RESULT %d: The current WLAN IP address should be in DHCP range" %step)
                    param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                    tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                    print("WLAN IP Address: %s" %curIPAddress)

                    if expectedresult in status and curIPAddress:
                        tdkTestObj.setResultStatus("SUCCESS")
                        status = checkIpRange(curIPAddress,wlanIP)

                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("ACTUAL RESULT %d : Current WLAN IP address is in same DHCP range" %step)
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Set the Port Triggering rule and disable it:- Trigger Port(start:end) - 12345:12345, TargetPort(start:end) - 69:69 (for TFTP), Trigger Protocol - UDP, Target Protocol - UDP, Description - MyPTRule
                            step = step + 1
                            triggerStart = "12345"
                            triggerEnd = "12345"
                            targetStart = "69"
                            targetEnd = "69"
                            triggerProtocol = "UDP"
                            targetProtocol = "UDP"
                            description = "MyPTRule"
                            enablePTRule = "false"
                            status, tdkTestObj, instance, step = SetPTRule(obj, obj1, triggerStart, triggerEnd, targetStart, targetEnd, triggerProtocol, targetProtocol, description, enablePTRule, step)

                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")

                                #Set new static route in WLAN client
                                step = step + 1
                                print("\nTEST STEP %d: Add a new static route in WLAN client to route the trigger via DUT" %step)
                                print("EXPECTED RESULT %d: A new static route should be added in WLAN client to route the trigger via DUT" %step)
                                status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_interface, "WLAN")

                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print("ACTUAL RESULT %d: Static route added successfully" %step)
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #Trigger the port
                                    step = step + 1
                                    print("\nTEST STEP %d: Trigger the Port %s through a specified outbound packet from WLAN client" %(step, triggerStart))
                                    print("EXPECTED RESULT %d: Port should be triggered successfully" %step)
                                    status = triggerPort(tdkbE2EUtility.wan_ip, triggerStart, triggerProtocol, "WLAN")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("ACTUAL RESULT %d: Port Triggered successfully" %step)
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #Check if the specified inbound packets are NOT forwarded to the WLAN client that triggered it
                                        step = step + 1

                                        #Custom Message in file inside /tftpboot in server
                                        value = random.randint(0, 1000)
                                        message = "File under tftpboot in server " + str(value)
                                        print("\nTEST STEP %d: Check if the specified inbound packets are NOT forwarded to the WLAN client correctly triggered with PT rule disabled" %step)
                                        print("EXPECTED RESULT %d: TFTP from WAN to the WLAN should be failed with the GW WAN IP of DUT" %step)
                                        status = tftpToClient(tdkbE2EUtility.gw_wan_ip, "WLAN", tdkbE2EUtility.tftpfile, message, "WAN")

                                        if status == "FAILURE":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("ACTUAL RESULT %d: TFTP from WAN to the WLAN failed with the GW WAN IP of DUT" %step)
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print("ACTUAL RESULT %d: TFTP from WAN to the WLAN is success with the GW WAN IP of DUT" %step)
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("ACTUAL RESULT %d: Port not triggered successfully" %step)
                                        print("[TEST EXECUTION RESULT] : FAILURE")

                                    #Delete the newly added route in WLAN client
                                    step = step + 1
                                    print("\nTEST STEP %d: Delete the added static route in WLAN client" %step)
                                    print("EXPECTED RESULT %d: The added static route should be deleted successfully" %step)
                                    status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_interface, "WLAN")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print("ACTUAL RESULT %d: Added route is deleted successfully" %step)
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print("ACTUAL RESULT %d: Added route is not deleted successfully" %step)
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print("ACTUAL RESULT %d: Static route not added successfully" %step)
                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                #Delete the added PT rule
                                step = step + 1
                                DeletePTRule(obj1, instance, step)
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("\nPort triggering rule not set, not proceeding further...")

                            #Revert the PT enable if required
                            if revertFlag == 1:
                                step = step + 1
                                PTRevertPreRequisite(obj, step)
                            else:
                                print("\nReverting the Port Triggering Enable is not required")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("ACTUAL RESULT %d : Current WLAN IP address is not in same DHCP range" %step)
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("ACTUAL RESULT %d : Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress not retrieved" %step)
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("ACTUAL RESULT %d : Current WLAN IP address not obtained" %step)
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("ACTUAL RESULT %d: Wlan client not connected to WiFi SSID" %(step))
                print("[TEST EXECUTION RESULT] : FAILURE")

        if tdkbE2EUtility.mlo_capability == "False":
            #Prepare the list of parameter values to be reverted
            step = step + 1
            list1 = [ssidName,orgValue[0],'string']
            list2 = [keyPassPhrase,orgValue[1],'string']
            list3 = [radioEnable,orgValue[2],'bool']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            print("\nTEST STEP %d: Should set the original ssid, keypassphrase, radio enable" %step)
            print("EXPECTED RESULT %d: Should set the original ssid, keypassphrase, radio enable" %step)
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print("ACTUAL RESULT %d: Details: %s" %(step, details))
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("ACTUAL RESULT %d: Details : %s" %(step, details))
                print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    print("Failed to load tdkb_e2e module")
    print("Failed to load advanedconfig module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")