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
  <name>E2E_LAN_ConfigureStaticAddressSource</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_Get</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To check if configuring a Static IP is successful for the LAN client connected as reflected in the value of Address Source, and upon deleting the Static IP config, the Address Source changes back to DHCP.</synopsis>
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
    <test_case_id>TC_TDKB_E2E_654</test_case_id>
    <test_objective>Verify if configuring a Static IP is successful for the LAN client connected as reflected in the value of Address Source, and upon deleting the Static IP config, the Address Source changes back to DHCP.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>tdkb_e2e_Get</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
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
2.Connect the Lan client.
3.Get ip of lan client and store it.
4.Get the value of AddressSource paramenter value using Device.Hosts.Host.{i}.AddressSource and store it. It should be DHCP.
5.Store the Ip address, Mac address and Hostname of lan client using
Device.Hosts.Host.{i}.PhysAddress, Device.Hosts.Host.{i}.IPAddress,Device.Hosts.Host.{i}.HostName.
6.Now create a static table for Lan client using Device.DHCPv4.Server.Pool.1.StaticAddress.
7.Update IP address, Mac address and host name of lan client in static table.
8.Now verify the AddressSource parameter with Device.Hosts.Host.{i}.AddressSource. It should be Static.
9.Now delete the static table and verify the AddressSource parameter. It should be DHCP.
10.Unload the e2e module.</automation_approch>
    <expected_output>When Static IP is assigned to LAN client the AddressSource data model should return as static. When IP is assigned dynamically assigned the AddressSource should return as Dhcp.
</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdk_e2e</test_stub_interface>
    <test_script>E2E_LAN_ConfigureStaticAddressSource</test_script>
    <skipped>No</skipped>
    <release_version>M134</release_version>
    <remarks>Only 1 LAN client is allowed</remarks>
  </test_cases>
</xml>
'''

def find_lan_client(tdkTestObj, host_entries_count):

    host_entries_count = int(host_entries_count)
    for i in range(1, host_entries_count + 1):
        layer1_interface_param = f"Device.Hosts.Host.{i}.Layer1Interface"

        # Fetch Layer1Interface for the current host entry
        tdkTestObj,layer1_interface_result, layer1_interface_value = getParameterValue(obj, layer1_interface_param)

        if "SUCCESS" in layer1_interface_result and layer1_interface_value:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"Checking Layer1Interface for Device.Hosts.Host.{i}: {layer1_interface_value}")

            # Check if the interface is Ethernet
            if "Ethernet" in layer1_interface_value:
                print(f"LAN connection found with Ethernet interface for Device.Hosts.Host.{i}")
                return i
            else:
                print(f"Device.Hosts.Host.{i} is not using Ethernet, continuing to check other devices.")
        else:
            tdkTestObj.setResultStatus("SUCCESS")
            print("Failed to fetch Layer1Interface for the current host entry")

    print("No LAN connection found.")
    return -1

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_LAN_ConfigureStaticAddressSource')
obj1.configureTestCase(ip,port,'E2E_LAN_ConfigureStaticAddressSource')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 = obj1.getLoadModuleResult()
print(f"[LIB LOAD STATUS] : {loadmodulestatus}")
print(f"[LIB LOAD STATUS1] : {loadmodulestatus1}")


if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    status = "SUCCESS"
    step = 1
    table_flag = 0

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        print(f"TEST STEP {step}: Get the current Gateway IP")
        print(f"EXPECTED RESULT {step}: Should get the current Gateway IP")
        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        tdkTestObj,status,curIPAddress = getParameterValue(obj,param)

        if expectedresult in status and curIPAddress:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: CurrentIP : {curIPAddress}")
            step = step + 1

            print(f"TEST STEP {step}: Get the IP address of LAN clinet")
            print(f"EXPECTED RESULT {step}: Should fetch LAN client IP address")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface)
            if lanIP:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: LAN client IP: {lanIP}")

                step = step + 1
                print(f"TEST STEP {step}: Check whether lan ip address is in same DHCP range")
                print(f"EXPECTED RESULT {step} lan ip address should be in same DHCP range")
                status = "SUCCESS"
                status = checkIpRange(curIPAddress,lanIP)
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step} lan ip address is in same DHCP range")

                    #Get the number of connected clients
                    step = step + 1
                    print(f"TEST STEP {step} : Get the Host number of entries")
                    print(f"EXPECTED RESULT {step}: Should get host number of entries")
                    param = "Device.Hosts.HostNumberOfEntries"
                    tdkTestObj,status,host_entries_count = getParameterValue(obj,param)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Host number of entries are {host_entries_count}")

                        # Get index of Lan client from host table
                        index = find_lan_client(obj,host_entries_count)

                        if int(index) >0:
                            # Get the value of AddressSource value
                            step = step + 1
                            print(f"TEST STEP {step} : Get the value of AddressSource for LAN client")
                            print(f"EXPECTED RESULT {step} : should get value of AddressSource")
                            param = f"Device.Hosts.Host.{index}.AddressSource"
                            tdkTestObj,status,Address_Source = getParameterValue(obj,param)

                            if expectedresult in status and Address_Source == "DHCP":
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: AddressSource of LAN client: {Address_Source}")

                                # Get Mac address and HostName of lan client
                                step = step + 1
                                print(f"TEST STEP {step} : Get Mac address and Host name of LAN client")
                                print(f"EXPECTED RESULT {step}: should get mac address and host name of LAN client")
                                status_MAC = "SUCCESS"
                                status_Host = "SUCCESS"
                                param_mac = f"Device.Hosts.Host.{index}.PhysAddress"
                                param_host = f"Device.Hosts.Host.{index}.HostName"

                                tdkTestObj,status_MAC,lanMAC = getParameterValue(obj,param_mac)
                                tdkTestObj,status_Host,lanHOST = getParameterValue(obj,param_host)

                                if "SUCCESS" in status_MAC and "SUCCESS" in status_Host:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: Mac Address : {lanMAC} and Host Name : {lanHOST}")

                                    # Add static table
                                    tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                                    tdkTestObj.addParameter("paramName","Device.DHCPv4.Server.Pool.1.StaticAddress.")
                                    tdkTestObj.executeTestCase(expectedresult)
                                    actualresult = tdkTestObj.getResult()
                                    details = tdkTestObj.getResultDetails()
                                    step = step + 1
                                    print(f"TEST STEP {step} : Create a static table for LAN client")
                                    print(f"EXPECTED RESULT {step} : Should create static table for LAN client")
                                    if expectedresult in actualresult:
                                        table_flag = 1
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Added new static rule {details}")
                                        instance = details.split(':')[1]

                                        if int(instance)>0:
                                            print(f"INSTANCE VALUE : {instance}")

                                            Chaddr = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.Chaddr"
                                            Yiaddr = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.Yiaddr"
                                            DeviceName = f"Device.DHCPv4.Server.Pool.1.StaticAddress.{instance}.X_CISCO_COM_DeviceName"

                                            list1 = [Chaddr,lanMAC,'string']
                                            list2 = [Yiaddr,lanIP,'string']
                                            list3 = [DeviceName,lanHOST,'string']

                                            setParamList= list1 + list2 + list3
                                            setParamList = "|".join(map(str, setParamList))
                                            step = step+1
                                            print(f"TEST STEP {step}: Set Chaddr, Yiaddr and DeviceName")
                                            print(f"EXPECTED RESULT {step} : Should set Chaddr, Yiaddr and DeviceName")

                                            setValuesList = [lanMAC,lanIP,lanHOST]
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

                                                    # Get the AddressSource of Lan client
                                                    step = step + 1
                                                    print(f"TEST STEP {step} : Get the value of AddressSource for LAN client")
                                                    print(f"EXPECTED RESULT {step} : Should get the value of AddressSource and AddressSource value should change to 'Static' ")
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

                                                            #check AddressSource
                                                            step = step + 1
                                                            print(f"TEST STEP {step} : Get the value of AddressSource for LAN client")
                                                            print(f"EXPECTED RESULT {step} : should retrive the AddressSource and AddressSource value should change to 'DHCP' ")
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
                                                    print(f"ACTUAL RESULT {step} : Failed GET operation failed/values do not reflect in get. Current values {newValues}")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to set Chaddr, Yiaddr and DeviceName :{details}")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Invalid instance returned :{instance} ")
                                    else:
                                        tdkTestObj.setResultStatus ("FAILURE")
                                        print(f"ACTUAL RESULT {step} : Failed to add static table for LAN client")
                                else:
                                    tdkTestObj.setResultStatus ("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Mac Address :{lanMAC} and Host Name :{lanHOST}")
                            else:
                                tdkTestObj.setResultStatus ("FAILURE")
                                print(f"ACTUAL RESULT {step} Value of AddressSource for LAN client is not changed. AddressSource:{Address_Source}")
                        else:
                            tdkTestObj.setResultStatus ("FAILURE")
                            print("No LAN entries found in the host table")
                    else:
                        tdkTestObj.setResultStatus ("FAILURE")
                        print(f"ACTUAL RESULT {step} Failed to get Host number of entries")
                else:
                    tdkTestObj.setResultStatus ("FAILURE")
                    print(f"ACTUAL RESULT {step} : Lan client ip is not in same DHCP range")
            else:
                tdkTestObj.setResultStatus ("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to get LAN client IP")
        else:
            tdkTestObj.setResultStatus ("FAILURE")
            print(f"ACTUAL RESULT {step} : Failed to get the current Gateway IP ")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device config file")

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