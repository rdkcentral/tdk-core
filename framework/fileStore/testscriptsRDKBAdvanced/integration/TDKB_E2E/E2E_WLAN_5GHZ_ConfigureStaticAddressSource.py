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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>E2E_WLAN_5GHZ_ConfigureStaticAddressSource</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if configuring a Static IP is successful for the WLAN client(5ghz) connected as reflected in the value of Address Source, and upon deleting the Static IP config, the Address Source changes back to DHCP.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>15</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>Broadband</box_type>
    <!--  -->
    <box_type>RPI</box_type>
    <!--  -->
  <box_type>BPI</box_type></box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_653</test_case_id>
    <test_objective>Verify if configuring a Static IP is successful for the WLAN client(5ghz) connected as reflected in the value of Address Source, and upon deleting the Static IP config, the Address Source changes back to DHCP.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Get</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
Device.WiFi.SSID.{i}.Enable
Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.WiFi.AccessPoint.{i}.AssociatedDeviceNumberOfEntries
Device.Hosts.HostNumberOfEntries
Device.Hosts.Host.{i}.Layer1Interface
Device.Hosts.Host.{i}.PhysAddress
Device.Hosts.Host.{i}.HostName
Device.Hosts.Host.{i}.AddressSource
Device.DHCPv4.Server.Pool.1.StaticAddress.
Device.DHCPv4.Server.Pool.1.StaticAddress.{i}.Chaddr
Device.DHCPv4.Server.Pool.1.StaticAddress.{i}.Yiaddr
Device.DHCPv4.Server.Pool.1.StaticAddress.{i}.X_CISCO_COM_DeviceName</input_parameters>
    <automation_approch>1.Load the e2e module.
2.Connect the wlan client.
3.Get ip of wlan client and store it.
4.Get the value of AddressSource paramenter value using Device.Hosts.Host.{i}.AddressSource and store it. It should be DHCP.
5.Store the Ip address, Mac address and Hostname of wlan client using
Device.Hosts.Host.{i}.PhysAddress, Device.Hosts.Host.{i}.IPAddress,Device.Hosts.Host.{i}.HostName.
6.Now create a static table for wlan client using Device.DHCPv4.Server.Pool.1.StaticAddress.
7.Update IP address, Mac address and host name of wlan client in static table.
8.Now verify the AddressSource parameter Device.Hosts.Host.{i}.AddressSource. It should be Static.
9.Now delete the static table and verify the AddressSource parameter. It should be DHCP.
10.Unload the e2e module.</automation_approch>
    <expected_output>When Static IP is assigned to WLAN client the AddressSource data model should return as static. When IP is assigned dynamically assigned the AddressSource should return as Dhcp.</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdk_e2e</test_stub_interface>
    <test_script>E2E_WLAN_5GHZ_ConfigureStaticAddressSource</test_script>
    <skipped>No</skipped>
    <release_version>M134</release_version>
    <remarks>Only 1 wlan client is allowed in the setup</remarks>
  </test_cases>
</xml>
'''
def find_wlan_client(tdkTestObj, host_entries_count):

    host_entries_count = int(host_entries_count)
    for i in range(1, host_entries_count + 1):
        layer1_interface_param = f"Device.Hosts.Host.{i}.Layer1Interface"

        # Fetch Layer1Interface for the current host entry
        tdkTestObj,layer1_interface_result, layer1_interface_value = getParameterValue(obj, layer1_interface_param)

        if "SUCCESS" in layer1_interface_result and layer1_interface_value:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"Checking Layer1Interface for Device.Hosts.Host.{i}: {layer1_interface_value}")

            # Check if the interface is Wifi
            if "Device.WiFi.SSID.2" in layer1_interface_value:
                print(f"WLAN connection found with Wifi interface for Device.Hosts.Host.{i}")
                return i
            else:
                print(f"Device.Hosts.Host.{i} is not using Wifi, continuing to check other devices.")
        else:
            tdkTestObj.setResultStatus("SUCCESS")
            print("Failed to fetch Layer1Interface for the current host entry")

    print("No WLAN connection found.")
    return -1



# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WLAN_5GHZ_ConfigureStaticAddressSource')
obj1.configureTestCase(ip,port, 'E2E_WLAN_5GHZ_ConfigureStaticAddressSource')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 = obj1.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus} [LIB1 LOAD STATUS] : {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 1
    table_flag = 0

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
        ssidEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_5ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,ssidEnable,keyPassPhrase]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        print(f"TEST STEP {step}: Get the current ssid, keyPassPhrase and ssidEnable")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keyPassPhrase and ssidEnable")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: %s" %orgValue)
            print("[TEST EXECUTION RESULT] : SUCCESS")

            setValuesList = [tdkbE2EUtility.ssid_5ghz_name,'true',tdkbE2EUtility.ssid_5ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
            list2 = [ssidEnable,'true','bool']
            list3 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))

            step = step + 1
            print(f"TEST STEP {step}: Set the ssid, keyPassPhrase and ssidEnable")
            print(f"EXPECTED RESULT {step}: Should set the ssid, keyPassPhrase and ssidEnable")

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                newParamList=[ssidName,ssidEnable,keyPassPhrase]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                step = step + 1
                print(f"TEST STEP {step}: Get the current ssid, keyPassPhrase and ssidEnable")
                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid, keyPassPhrase and ssidEnable")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    #Connect to the wifi ssid from wlan client
                    step = step + 1
                    print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: wlan client should connect to wifi ssid")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {status}")

                        step = step + 1
                        print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should fetch the IP address of wlan client after connecting to ssid")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_5ghz_interface)
                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: SUCCESS")
                            step = step + 1
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should get current LAN IP address DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP Address: {curIPAddress}")
                                step = step + 1
                                print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: wlan IP should be in same DHCP range")
                                status = "SUCCESS"
                                status = checkIpRange(curIPAddress,wlanIP)
                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: wlan ip address is in DHCP range")

                                    param = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_5ghz_index}.AssociatedDeviceNumberOfEntries"
                                    tdkTestObj,status,AssociatedDevices = getParameterValue(obj,param)
                                    step = step + 1
                                    print(f"TEST STEP {step} : Get the current Associated number of entries after connecting to WIFI")
                                    print(f"EXPECTED RESULT {step} : Should get the current Associated number of entries after connecting to WIFI")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step} : AssociatedDeviceNumberOfEntries : {AssociatedDevices}")

                                        if int(AssociatedDevices) == 1:

                                            #Get the number of connected clients
                                            step = step + 1
                                            print(f"TEST STEP {step} : Get the Host number of entries")
                                            print(f"EXPECTED RESULT {step}: Should get host number of entries")
                                            param = "Device.Hosts.HostNumberOfEntries"
                                            tdkTestObj,status,host_entries_count = getParameterValue(obj,param)

                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: Host number of entries are {host_entries_count}")

                                                # Get index of WLan client from host table
                                                index = find_wlan_client(obj,host_entries_count)

                                                if int(index) >0:
                                                    # Get the value of AddressSource value
                                                    step = step + 1
                                                    print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                    print(f"EXPECTED RESULT {step} : Should get value of AddressSource")
                                                    param = f"Device.Hosts.Host.{index}.AddressSource"
                                                    tdkTestObj,status,Address_Source = getParameterValue(obj,param)

                                                    if expectedresult in status and Address_Source == "DHCP":
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: AddressSource of WLAN client: {Address_Source}")

                                                        # Get Mac address and HostName of Wlan client
                                                        step = step + 1
                                                        print(f"TEST STEP {step} : Get Mac address and Host name of WLAN client")
                                                        print(f"EXPECTED RESULT {step}: should get mac address and host name of WLAN client")
                                                        status_MAC = "SUCCESS"
                                                        status_Host = "SUCCESS"
                                                        param_mac = f"Device.Hosts.Host.{index}.PhysAddress"
                                                        param_host = f"Device.Hosts.Host.{index}.HostName"

                                                        tdkTestObj,status_MAC,wlanMAC = getParameterValue(obj,param_mac)
                                                        tdkTestObj,status_Host,wlanHOST = getParameterValue(obj,param_host)

                                                        if "SUCCESS" in status_MAC and "SUCCESS" in status_Host:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: Mac Address : {wlanMAC} and Host Name : {wlanHOST}")

                                                            # Add static table
                                                            tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                                            tdkTestObj.addParameter("paramName","Device.DHCPv4.Server.Pool.1.StaticAddress.")
                                                            tdkTestObj.executeTestCase(expectedresult)
                                                            actualresult = tdkTestObj.getResult()
                                                            details = tdkTestObj.getResultDetails()
                                                            step = step + 1
                                                            print(f"TEST STEP {step} : Create a static table for WLAN client")
                                                            print(f"EXPECTED RESULT {step} : Should create static table for WLAN client")
                                                            if expectedresult in actualresult:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print(f"ACTUAL RESULT {step}: Addedd new static rule {details}")
                                                                table_flag = 1
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

                                                                    tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                                                                    if expectedresult in actualresult:
                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                        print(f"ACTUAL RESULT {step}: {details}")

                                                                        #Retrieve the values after set and compare
                                                                        newParamList=[Chaddr,Yiaddr,DeviceName]
                                                                        step = step + 1
                                                                        print(f"TEST STEP {step} : Get the current values of Chaddr,Yiaddr and DeviceName and compare ")
                                                                        print(f"EXPECTED RESULT {step} : Should retrive current values of Chaddr,Yiaddr and DeviceName")
                                                                        tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                                                        if expectedresult in status and setValuesList == newValues:
                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                            print(f"ACTUAL RESULT {step}: new values : {newValues}")

                                                                            # Get the AddressSOurce of WLan client
                                                                            step = step + 1
                                                                            print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                                            print(f"EXPECTED RESULT {step} : Should get the value of AddressSource and value should be changed to static ")
                                                                            param = f"Device.Hosts.Host.{index}.AddressSource"
                                                                            tdkTestObj,status,Address_Source = getParameterValue(obj,param)

                                                                            if expectedresult in status and Address_Source == "Static":
                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                print(f"ACTUAL RESULT {step}: AddressSource : {Address_Source}")

                                                                                #delete the static table

                                                                                tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                                                                tdkTestObj.addParameter("paramName",f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.")
                                                                                tdkTestObj.executeTestCase(expectedresult)
                                                                                actualresult = tdkTestObj.getResult()
                                                                                details = tdkTestObj.getResultDetails()
                                                                                step = step + 1
                                                                                print(f"TEST STEP {step}: Delete the static table")
                                                                                print(f"EXPECTED RESULT {step} : Should delete static table")

                                                                                if expectedresult in actualresult:
                                                                                    table_flag = 0
                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                    print(f"ACTUAL RESULT {step} : {details}")
                                                                                    time.sleep(2)

                                                                                    #check AddressSource
                                                                                    step = step + 1
                                                                                    print(f"TEST STEP {step} : Get the value of AddressSource for WLAN client")
                                                                                    print(f"EXPECTED RESULT {step} : should retrive the AddressSource and value should be changed to DHCP")
                                                                                    param = f"Device.Hosts.Host.{index}.AddressSource"
                                                                                    tdkTestObj,status,Address_Source = getParameterValue(obj,param)

                                                                                    if expectedresult in status and Address_Source == "DHCP":
                                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                                        print(f"ACTUAL RESULT {step}: AddressSource :{Address_Source}")
                                                                                    else:
                                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                                        print(f"ACTUAL RESULT {step}: AddressSource :{Address_Source}")
                                                                                else:
                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                    print(f"ACTUAL RESULT {step}: Failed to delete static table :{details}")
                                                                            else:
                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                print(f"ACTUAL RESULT {step} : AddressSource not changed. AddressSource:{Address_Source}")
                                                                        else:
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            print(f"ACTUAL RESULT {step} : Failed GET operation failed/values do not reflect in get. Current values:{newValues}")
                                                                    else:
                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                        print(f"ACTUAL RESULT {step}: Failed to set Chaddr, Yiaddr and DeviceName :{details}")
                                                                else:
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    print(f"Invalid instance returned : {instance} ")
                                                            else:
                                                                tdkTestObj.setResultStatus ("FAILURE")
                                                                print(f"ACTUAL RESULT {step} : Failed to add static table for WLAN client")
                                                        else:
                                                            tdkTestObj.setResultStatus ("FAILURE")
                                                            print(f"ACTUAL RESULT {step}: Mac Address : {wlanMAC} and Host Name : {wlanHOST}")
                                                    else:
                                                        tdkTestObj.setResultStatus ("FAILURE")
                                                        print(f"ACTUAL RESULT {step} Value of AddressSource not changed. AddressSource:{Address_Source}")
                                                else:
                                                    tdkTestObj.setResultStatus ("FAILURE")
                                                    print("No WLAN entries found in host table")
                                            else:
                                                tdkTestObj.setResultStatus ("FAILURE")
                                                print(f"ACTUAL RESULT {step} Failed to get Host number of entries")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print("AssociatedDeviceNumberOfEntries is greater than 1 not procceding further")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step} : AssociatedDeviceNumberOfEntries : {AssociatedDevices}")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: wlan ip address is not in DHCP range")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get current gateway ip address. LAN IP Address{curIPAddress}")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the wlan ip address")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect to the wifi ssid")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    if(table_flag == 1):
        tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
        tdkTestObj.addParameter("paramName",f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.")
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        step = step + 1
        print(f"TEST STEP {step}: Delete the static table")
        print(f"EXPECTED RESULT {step}: Should delete static table")

        if expectedresult in actualresult:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Static table deleted :{details}")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to delete static table :{details}")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    print("Failed to load tdkb_e2e module")
    print("Failed to load advancedconfig module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

