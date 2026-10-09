##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2019 RDK Management
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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_DisablePF_FirewallLow_HTTPFromWanToWlan')
obj1.configureTestCase(ip,port,'E2E_DisablePF_FirewallLow_HTTPFromWanToWlan')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = obj1.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s " %loadmodulestatus)
print("[LIB LOAD STATUS]  :  %s " %loadmodulestatus1)

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_2ghz_index
        firewallLevel = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

        #Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, radioEnable]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)
        tdkTestObj1, retStatus, firewallValue = getParameterValue(obj, firewallLevel)
        print("Firewall Level: %s" %firewallValue)

        if expectedresult in status and expectedresult in retStatus:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"ACTUAL RESULT {step}: {orgValue} {firewallValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            if tdkbE2EUtility.mlo_capability == "False":
                #Set the SSID name,password,Radio enable status and firewall level
                setValuesList = [tdkbE2EUtility.ssid_2ghz_name, tdkbE2EUtility.ssid_2ghz_pwd, 'true']
                print("Parameter values that are set: %s" %setValuesList)

                list1 = [ssidName, tdkbE2EUtility.ssid_2ghz_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_2ghz_pwd, 'string']
                list3 = [radioEnable, 'true', 'bool']

                firewallParam = "%s|Low|string" %firewallLevel

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2 + list3
                setParamList = "|".join(map(str, setParamList))

                tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)
                tdkTestObj, firewallResult, details = setMultipleParameterValues(obj, firewallParam)

                step = step + 1
                if expectedresult in actualresult and expectedresult in firewallResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase,Radio enable status,firewall level")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,Radio enable status,firewall level")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    newParamList = [ssidName, keyPassPhrase, radioEnable]
                    tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)
                    tdkTestObj1, retStatus, newFirewallValue = getParameterValue(obj, firewallLevel)
                    print("Firewall Level: %s" %newFirewallValue)

                    step = step + 1
                    if expectedresult in status and expectedresult in retStatus and setValuesList == newValues and newFirewallValue == "Low":
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
                        print(f"ACTUAL RESULT {step}: {newValues} {newFirewallValue}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                        status = "SUCCESS"
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
                        print(f"ACTUAL RESULT {step}: {newValues} {newFirewallValue}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase,Radio enable status,firewall level")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,Radio enable status,firewall level")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                #Set the firewall level to Low using firewallSet function for MLO device
                level = "Low"
                step = step + 1
                status, step = firewallSet(obj, level, step)

            if tdkbE2EUtility.mlo_capability == "False":
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface

            if status == "SUCCESS":
                #Wait for the changes to reflect in client device
                time.sleep(60)

                #Connect to the wifi ssid from wlan client
                step = step + 1
                print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                print(f"EXPECTED RESULT {step}: The wlan client should connect to the WiFi SSID successfully")
                status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name, tdkbE2EUtility.ssid_pwd, tdkbE2EUtility.wlan_interface)

                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: WLAN client connected to WiFi SSID successfully")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    step = step + 1
                    print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                    print(f"EXPECTED RESULT {step}: Should get the IP address of the wlan client")
                    wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)

                    if wlanIP:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: WLAN IP Address is {wlanIP}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step = step + 1
                        print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                        print(f"EXPECTED RESULT {step}: Should get the current LAN IP address DHCP range")
                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                        tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
                        print("LAN IP Address: %s" %curIPAddress)

                        if expectedresult in status and curIPAddress:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: LAN IP Address retrieved as {curIPAddress}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            step = step + 1
                            print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                            print(f"EXPECTED RESULT {step}: WLAN IP address should be in same DHCP range")
                            status = "SUCCESS"
                            status = checkIpRange(curIPAddress, wlanIP)

                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WLAN IP address is in same DHCP range")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                step = step + 1
                                print(f"\nTEST STEP {step}: Add static route in WLAN client")
                                print(f"EXPECTED RESULT {step}: Static route should be added successfully")
                                status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_interface)

                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: Static route add success")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Saving the EnablePortMapping value")
                                    print(f"EXPECTED RESULT {step}: Should get the EnablePortMapping value successfully")
                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_Get")
                                    tdkTestObj.addParameter("paramName", "Device.NAT.X_Comcast_com_EnablePortMapping")
                                    expectedresult = "SUCCESS"
                                    tdkTestObj.executeTestCase(expectedresult)
                                    actualresult = tdkTestObj.getResult()
                                    details = tdkTestObj.getResultDetails()

                                    if expectedresult in actualresult:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        details = tdkTestObj.getResultDetails()
                                        print(f"ACTUAL RESULT {step}: {details}")
                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)

                                        if "true" in details:
                                            portMap = "true"
                                        else:
                                            portMap = "false"

                                        #Enabling port forwarding - setting the port mapping as true
                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Enabling Port Mapping")
                                        print(f"EXPECTED RESULT {step}: Should enable Port Mapping")
                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_Set")
                                        tdkTestObj.addParameter("paramName", "Device.NAT.X_Comcast_com_EnablePortMapping")
                                        tdkTestObj.addParameter("paramValue", "true")
                                        tdkTestObj.addParameter("paramType", "boolean")
                                        expectedresult = "SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult)
                                        actualresult = tdkTestObj.getResult()
                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)

                                        if expectedresult in actualresult:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            details = tdkTestObj.getResultDetails()
                                            print(f"ACTUAL RESULT {step}: {details}")
                                            print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                            print("Port Mapping is enabled\n")

                                            #Adding a new row to the port forwarding table
                                            step = step + 1
                                            print(f"\nTEST STEP {step}: Adding new rule to Port Mapping")
                                            print(f"EXPECTED RESULT {step}: Should add new rule to Port Mapping")
                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                            tdkTestObj.addParameter("paramName", "Device.NAT.PortMapping.")
                                            expectedresult = "SUCCESS"
                                            tdkTestObj.executeTestCase(expectedresult)
                                            actualresult = tdkTestObj.getResult()

                                            if expectedresult in actualresult:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                details = tdkTestObj.getResultDetails()
                                                print(f"ACTUAL RESULT {step}: {details}")
                                                print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                print("Add service option is selected and a new table is created\n")

                                                temp = details.split(':')
                                                instance1 = temp[1]

                                                if int(instance1) > 0:
                                                    #Setting the external port
                                                    step = step + 1
                                                    print(f"\nTEST STEP {step}: Setting external port")
                                                    print(f"EXPECTED RESULT {step}: Should set external port successfully")
                                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_SetMultiple")
                                                    tdkTestObj.addParameter("paramList", "Device.NAT.PortMapping.%s.Enable|true|bool|Device.NAT.PortMapping.%s.ExternalPort|%s|unsignedint|Device.NAT.PortMapping.%s.Protocol|BOTH|string|Device.NAT.PortMapping.%s.InternalClient|%s|string|Device.NAT.PortMapping.%s.Description|NEW_HTTP_RULE|string|Device.NAT.PortMapping.%s.ExternalPortEndRange|%s|unsignedint" %(instance1, instance1, tdkbE2EUtility.wlan_http_port, instance1, instance1, wlanIP, instance1, instance1, tdkbE2EUtility.wlan_http_port))
                                                    expectedresult = "SUCCESS"
                                                    tdkTestObj.executeTestCase(expectedresult)
                                                    actualresult = tdkTestObj.getResult()

                                                    if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        details = tdkTestObj.getResultDetails()
                                                        print(f"ACTUAL RESULT {step}: {details}")
                                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                        print("Added port mapping rule successfully\n")

                                                        time.sleep(60)

                                                        step = step + 1
                                                        print(f"\nTEST STEP {step}: Check the HTTP from WAN to WLAN after enabling port mapping")
                                                        print(f"EXPECTED RESULT {step}: HTTP from WAN to WLAN should be successful after enabling Port Mapping")
                                                        status = verifyNetworkConnectivity(tdkbE2EUtility.gw_wan_ip, "WGET_HTTP", tdkbE2EUtility.wan_ip, curIPAddress, "WAN")

                                                        if expectedresult in status:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: HTTP from WAN to WLAN is successful")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                            #Disabling port forwarding - setting the port mapping as false
                                                            step = step + 1
                                                            print(f"\nTEST STEP {step}: Disabling Port Mapping")
                                                            print(f"EXPECTED RESULT {step}: Should disable Port Mapping")
                                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_Set")
                                                            tdkTestObj.addParameter("paramName", "Device.NAT.X_Comcast_com_EnablePortMapping")
                                                            tdkTestObj.addParameter("paramValue", "false")
                                                            tdkTestObj.addParameter("paramType", "boolean")
                                                            expectedresult = "SUCCESS"
                                                            tdkTestObj.executeTestCase(expectedresult)
                                                            actualresult = tdkTestObj.getResult()
                                                            print("[TEST EXECUTION RESULT] : %s" %actualresult)

                                                            if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                details = tdkTestObj.getResultDetails()
                                                                print(f"ACTUAL RESULT {step}: {details}")
                                                                print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                                print("Port Mapping is disabled\n")

                                                                time.sleep(60)

                                                                step = step + 1
                                                                print(f"\nTEST STEP {step}: Check the HTTP from WAN to WLAN after disabling port mapping")
                                                                print(f"EXPECTED RESULT {step}: HTTP from WAN to WLAN should fail after disabling Port Mapping")
                                                                status = verifyNetworkConnectivity(tdkbE2EUtility.gw_wan_ip, "WGET_HTTP", tdkbE2EUtility.wan_ip, curIPAddress, "WAN")

                                                                if expectedresult not in status:
                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                    finalStatus = "SUCCESS"
                                                                    print(f"ACTUAL RESULT {step}: HTTP from WAN to WLAN failed as expected")
                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    print(f"ACTUAL RESULT {step}: HTTP from WAN to WLAN is successful after disabling Port Mapping")
                                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                details = tdkTestObj.getResultDetails()
                                                                print(f"ACTUAL RESULT {step}: {details}")
                                                                print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                                print("Failure in setting the port forwarding as false\n ")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            print(f"ACTUAL RESULT {step}: HTTP from WAN to WLAN failed")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        details = tdkTestObj.getResultDetails()
                                                        print(f"ACTUAL RESULT {step}: {details}")
                                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                        print("Failure in setting the start port\n")
                                                else:
                                                    print("Instance value should be greater than 0\n")
                                                    print("Wrong instance value\n")

                                                #To delete the added table
                                                if instance1:
                                                    step = step + 1
                                                    print(f"\nTEST STEP {step}: Deleting the added rule")
                                                    print(f"EXPECTED RESULT {step}: Should delete the added rule")
                                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                    tdkTestObj.addParameter("paramName", "Device.NAT.PortMapping.%s." %instance1)
                                                    expectedresult = "SUCCESS"
                                                    tdkTestObj.executeTestCase(expectedresult)
                                                    actualresult = tdkTestObj.getResult()
                                                    print("[TEST EXECUTION RESULT] : %s" %actualresult)

                                                    if expectedresult in actualresult:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        details = tdkTestObj.getResultDetails()
                                                        print(f"ACTUAL RESULT {step}: {details}")
                                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                        print("Added table is deleted successfully\n")
                                                    else:
                                                        details = tdkTestObj.getResultDetails()
                                                        print(f"ACTUAL RESULT {step}: {details}")
                                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                        print("Added table could not be deleted\n")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                details = tdkTestObj.getResultDetails()
                                                print(f"ACTUAL RESULT {step}: {details}")
                                                print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                                print("Failure in adding the new port forwarding row\n")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            details = tdkTestObj.getResultDetails()
                                            print(f"ACTUAL RESULT {step}: {details}")
                                            print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                            print("Failure in setting the port forwarding as true\n ")

                                        #Reverting port mapping status
                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Reverting Port Mapping")
                                        print(f"EXPECTED RESULT {step}: Should revert Port Mapping")
                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_Set")
                                        tdkTestObj.addParameter("paramName", "Device.NAT.X_Comcast_com_EnablePortMapping")
                                        tdkTestObj.addParameter("paramValue", portMap)
                                        tdkTestObj.addParameter("paramType", "boolean")
                                        expectedresult = "SUCCESS"
                                        tdkTestObj.executeTestCase(expectedresult)
                                        actualresult = tdkTestObj.getResult()
                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)

                                        if expectedresult in actualresult:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            details = tdkTestObj.getResultDetails()
                                            print(f"ACTUAL RESULT {step}: {details}")
                                            print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                            print("Port Mapping is reverted\n")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            details = tdkTestObj.getResultDetails()
                                            print(f"ACTUAL RESULT {step}: {details}")
                                            print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                            print("Port Mapping is not reverted\n")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: {details}")
                                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                                        print("Failure in getting EnablePortMapping value\n")

                                    #Delete the static route since it was added successfully
                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Delete the static route")
                                    print(f"EXPECTED RESULT {step}: Static route should be deleted successfully")
                                    status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress, tdkbE2EUtility.wlan_interface)

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Static route delete success")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Static route delete failed")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Static route add failed")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: WLAN Client IP address is not in the same Gateway DHCP range")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the Gateway IP address")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to get the WLAN Client IP address")
                        print("[TEST EXECUTION RESULT] : FAILURE")

                    #Disconnect WLAN client since it was connected successfully
                    step = step + 1
                    print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                    print(f"EXPECTED RESULT {step}: WLAN client should disconnect from WiFi SSID successfully")
                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID is successful")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID failed")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to connect to WIFI SSID")
                    print("[TEST EXECUTION RESULT] : FAILURE")

            if tdkbE2EUtility.mlo_capability == "False":
                #Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']
                list3 = [radioEnable, orgValue[2], 'bool']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2 + list3
                revertParamList = "|".join(map(str, revertParamList))

                firewallParam = "%s|%s|string" %(firewallLevel, firewallValue)

                #Revert the values to original
                step = step + 1
                print(f"\nTEST STEP {step}: Revert the values to original")
                print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,Radio enable status,firewall level")
                tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)
                tdkTestObj, firewallResult, details = setMultipleParameterValues(obj, firewallParam)

                if expectedresult in actualresult and expectedresult in firewallResult and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                #Revert the firewall level to original value using firewallSet function
                level = firewallValue
                step = step + 1
                _, _ = firewallSet(obj, level, step, revert="true")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,Radio enable status,firewall level")
            print(f"ACTUAL RESULT {step}: {orgValue} {firewallValue}")
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
    print("Failed to load advancedconfig module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")