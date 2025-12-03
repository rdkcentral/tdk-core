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

def find_wlan_client(host_entries_count):

    host_entries_count = int(host_entries_count)
    for i in range(1, host_entries_count + 1):
        layer1_interface_param = f"Device.Hosts.Host.{i}.Layer1Interface"

        # Fetch Layer1Interface for the current host entry
        tdkTestObj,layer1_interface_result, layer1_interface_value = tdkbE2EUtility.getParameterValue(obj, layer1_interface_param)

        if "SUCCESS" in layer1_interface_result and layer1_interface_value:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"Checking Layer1Interface for Device.Hosts.Host.{i}: {layer1_interface_value}")

            # Check if the interface is Wifi
            if "Device.WiFi.SSID.1" in layer1_interface_value:
                print(f"WLAN connection found with Wifi interface for Device.Hosts.Host.{i}")
                return i
            else:
                print(f"Device.Hosts.Host.{i} is not using Wifi, continuing to check other devices.")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print("Failed to fetch Layer1Interface for the current host entry")

    print("No WLAN connection found.")
    return -1



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
obj.configureTestCase(ip,port,'E2E_WLAN_6GHZ_ConfigureStaticAddressSource')
obj1.configureTestCase(ip,port, 'E2E_WLAN_6GHZ_ConfigureStaticAddressSource')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 = obj1.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus} [LIB1 LOAD STATUS] : {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 1
    table_flag = 0

    #Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable using f-strings
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        ssidEnable = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.Enable"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,ssidEnable,keyPassPhrase]
        tdkTestObj,status,orgValue = tdkbE2EUtility.getMultipleParameterValues(obj,paramList)

        print(f"TEST STEP {step}: Get the current ssid, ssidEnable and Keypassphrase")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid ,ssidEnable and Keypassphrase")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Current values: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set ssid, Keypassphrase and ssidEnable for 6ghz"
            setValuesList = [tdkbE2EUtility.ssid_6ghz_name,'true', tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName,tdkbE2EUtility.ssid_6ghz_name,'string']
            list2 = [ssidEnable,'true','bool']
            list3 = [keyPassPhrase,tdkbE2EUtility.ssid_6ghz_pwd,'string']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            step  += 1
            print(f"TEST STEP {step}: Set the ssid ssidEnable and keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the ssid ,ssidEnable and keypassphrase")

            tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: SET operation success. Details: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                newParamList=[ssidName,ssidEnable,keyPassPhrase]
                tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                step  += 1
                print(f"TEST STEP {step}: Get the current ssid ssidEnable and keypassphrase")
                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid ssidEnable and keypassphrase")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Current values after SET :{newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    #Connect to the wifi ssid from wlan client
                    step  += 1
                    print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: wlan client should connect to wifi ssid")
                    status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {status}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step  += 1
                        print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should fetch the IP address of wlan client after connecting to ssid")
                        wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: SUCCESS")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            step  += 1
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should get current LAN IP address DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj,status,curIPAddress = tdkbE2EUtility.getParameterValue(obj,param)

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP Address: {curIPAddress}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                step  += 1
                                print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: wlan IP should be in same DHCP range")
                                status = tdkbE2EUtility.checkIpRange(curIPAddress,wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: wlan ip address is in DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    param = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.AssociatedDeviceNumberOfEntries"
                                    tdkTestObj,status,AssociatedDevices = tdkbE2EUtility.getParameterValue(obj,param)
                                    step  += 1
                                    print(f"TEST STEP {step} : Get the current Associated number of entries after connecting to WIFI")
                                    print(f"EXPECTED RESULT {step} : Should get the current Associated number of entries after connecting to WIFI")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step} : AssociatedDeviceNumberOfEntries : {AssociatedDevices}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        if int(AssociatedDevices) == 1:
                                            #Get the number of connected clients
                                            step  += 1
                                            print(f"TEST STEP {step} : Get the Host number of entries")
                                            print(f"EXPECTED RESULT {step}: Should get host number of entries")
                                            param = "Device.Hosts.HostNumberOfEntries"
                                            tdkTestObj,status,host_entries_count = tdkbE2EUtility.getParameterValue(obj,param)

                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: Host number of entries are {host_entries_count}")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                # Get index of WLan client from host table
                                                index = find_wlan_client(host_entries_count)

                                                if int(index) >0:
                                                    # Get the value of AddressSource value
                                                    step  += 1
                                                    print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                    print(f"EXPECTED RESULT {step} : Should get value of AddressSource")
                                                    param = f"Device.Hosts.Host.{index}.AddressSource"
                                                    tdkTestObj,status,Address_Source = tdkbE2EUtility.getParameterValue(obj,param)

                                                    if expectedresult in status and Address_Source == "DHCP":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: AddressSource of WLAN client: {Address_Source}")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                        # Get Mac address and HostName of Wlan client
                                                        step  += 1
                                                        print(f"TEST STEP {step} : Get Mac address and Host name of WLAN client")
                                                        print(f"EXPECTED RESULT {step}: should get mac address and host name of WLAN client")
                                                        param_mac = f"Device.Hosts.Host.{index}.PhysAddress"
                                                        param_host = f"Device.Hosts.Host.{index}.HostName"

                                                        tdkTestObj,status_MAC,wlanMAC = tdkbE2EUtility.getParameterValue(obj,param_mac)
                                                        tdkTestObj,status_Host,wlanHOST = tdkbE2EUtility.getParameterValue(obj,param_host)

                                                        if expectedresult in status_MAC and expectedresult in status_Host:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: Mac Address : {wlanMAC} and Host Name : {wlanHOST}")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                            # Add static table
                                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                                            tdkTestObj.addParameter("paramName","Device.DHCPv4.Server.Pool.1.StaticAddress.")
                                                            tdkTestObj.executeTestCase(expectedresult)
                                                            actualresult = tdkTestObj.getResult()
                                                            details = tdkTestObj.getResultDetails()
                                                            step  += 1
                                                            print(f"TEST STEP {step} : Create a static table for WLAN client")
                                                            print(f"EXPECTED RESULT {step} : Should create static table for WLAN client")
                                                            if expectedresult in actualresult:
                                                                table_flag = 1
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print(f"ACTUAL RESULT {step}: Addedd new static rule {details}")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                instance = details.split(':')[1]

                                                                if int(instance)>0:
                                                                    print(f"INSTANCE VALUE : {instance}")

                                                                    Chaddr = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.Chaddr"
                                                                    Yiaddr = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.Yiaddr"
                                                                    DeviceName = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.X_CISCO_COM_DeviceName"

                                                                    list1 = [Chaddr,wlanMAC,'string']
                                                                    list2 = [Yiaddr,wlanIP,'string']
                                                                    list3 = [DeviceName,wlanHOST,'string']

                                                                    setParamList= list1 + list2 + list3
                                                                    setParamList = "|".join(map(str, setParamList))
                                                                    step = step+1
                                                                    print(f"TEST STEP {step}: Set Chaddr, Yiaddr and DeviceName")
                                                                    print(f"EXPECTED RESULT {step} : Should set Chaddr, Yiaddr and DeviceName")
                                                                    setValuesList = [wlanMAC,wlanIP,wlanHOST]
                                                                    print(f"parameter values are set {setValuesList}")

                                                                    tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
                                                                    if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                        print(f"ACTUAL RESULT {step}: {details}")
                                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                        #Retrieve the values after set and compare
                                                                        newParamList=[Chaddr,Yiaddr,DeviceName]
                                                                        step  += 1
                                                                        print(f"TEST STEP {step} : Get the current values of Chaddr,Yiaddr and DeviceName and compare ")
                                                                        print(f"EXPECTED RESULT {step} : Should retrive current values of Chaddr,Yiaddr and DeviceName")
                                                                        tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)
                                                                        if expectedresult in status and setValuesList == newValues:
                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                            print(f"ACTUAL RESULT {step}: new values : {newValues}")
                                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                            # Get the AddressSource of WLan client
                                                                            step  += 1
                                                                            print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                                            print(f"EXPECTED RESULT {step} : Should get the value of AddressSource and value should be changed to static ")
                                                                            param = f"Device.Hosts.Host.{index}.AddressSource"
                                                                            tdkTestObj,status,Address_Source = tdkbE2EUtility.getParameterValue(obj,param)

                                                                            if expectedresult in status and Address_Source == "Static":
                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                print(f"ACTUAL RESULT {step}: AddressSource : {Address_Source}")
                                                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                                                #delete the static table
                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                                                tdkTestObj.addParameter("paramName",f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.")
                                                                                tdkTestObj.executeTestCase(expectedresult)
                                                                                actualresult = tdkTestObj.getResult()
                                                                                details = tdkTestObj.getResultDetails()
                                                                                step  += 1
                                                                                print(f"TEST STEP {step}: Delete the static table")
                                                                                print(f"EXPECTED RESULT {step} : Should delete static table")

                                                                                if expectedresult in actualresult:
                                                                                    table_flag = 0
                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                    print(f"ACTUAL RESULT {step} : {details}")
                                                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                    time.sleep(2)

                                                                                    #check AddressSource
                                                                                    step  += 1
                                                                                    print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                                                    print(f"EXPECTED RESULT {step} : should retrive the AddressSource and value should be changed to DHCP")
                                                                                    param = f"Device.Hosts.Host.{index}.AddressSource"
                                                                                    tdkTestObj,status,Address_Source = tdkbE2EUtility.getParameterValue(obj,param)

                                                                                    if expectedresult in status and Address_Source == "DHCP":
                                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                                        print(f"ACTUAL RESULT {step}: AddressSource :{Address_Source}")
                                                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                                                    else:
                                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                                        print(f"ACTUAL RESULT {step}: AddressSource :{Address_Source}")
                                                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                    print(f"ACTUAL RESULT {step}: Failed to delete static table :{details}")
                                                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                                                            else:
                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                print(f"ACTUAL RESULT {step} : AddressSource not changed. AddressSource:{Address_Source}")
                                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            print(f"ACTUAL RESULT {step}: Failed GET operation failed/values do not reflect in get :{newValues}")
                                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                        print(f"ACTUAL RESULT {step}: Failed to set Chaddr, Yiaddr and DeviceName :{details}")
                                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    print(f"Invalid instance returned : {instance} ")
                                                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                                                    if(table_flag == 1):
                                                                        tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                                        tdkTestObj.addParameter("paramName",f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.")
                                                                        tdkTestObj.executeTestCase(expectedresult)
                                                                        actualresult = tdkTestObj.getResult()
                                                                        details = tdkTestObj.getResultDetails()
                                                                        step  += 1
                                                                        print(f"TEST STEP {step}: Delete the static table")
                                                                        print(f"EXPECTED RESULT {step}: Should delete static table")

                                                                        if expectedresult in actualresult:
                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                            print(f"ACTUAL RESULT {step}: Static table deleted :{details}")
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            print(f"ACTUAL RESULT {step}: Failed to delete static table :{details}")
                                                            else:
                                                                tdkTestObj.setResultStatus ("FAILURE")
                                                                print(f"ACTUAL RESULT {step} : Failed to add static table for WLAN client")
                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                        else:
                                                            tdkTestObj.setResultStatus ("FAILURE")
                                                            print(f"ACTUAL RESULT {step}: Mac Address : {wlanMAC} and Host Name : {wlanHOST}")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus ("FAILURE")
                                                        print(f"ACTUAL RESULT {step} Value of AddressSource for WLAN client is not changed. AddressSource:{Address_Source}")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus ("FAILURE")
                                                    print("No WLAN entries found in host table")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus ("FAILURE")
                                                print(f"ACTUAL RESULT {step} Failed to get Host number of entries")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print("AssociatedDeviceNumberOfEntries is greater than 1 not procceding further")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step} : AssociatedDeviceNumberOfEntries :{AssociatedDevices}")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: wlan ip address is not in DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get current gateway ip address. LAN IP Address:{curIPAddress}")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the wlan ip address")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect to the wifi ssid")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: GET operation failed/parameter values not reflected in GET")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: GET operation failure")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    print("Failed to load tdkb_e2e module")
    print("Failed to load advancedconfig module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")
    print("Module loading failed")