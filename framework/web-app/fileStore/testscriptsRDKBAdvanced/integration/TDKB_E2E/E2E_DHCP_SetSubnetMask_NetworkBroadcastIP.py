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
'''
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <id/>
  <version>1</version>
  <name>E2E_DHCP_SetSubnetMask_NetworkBroadcastIP</name>
  <primitive_test_id/>
  <primitive_test_name>tdkb_e2e_Set</primitive_test_name>
  <primitive_test_version>2</primitive_test_version>
  <status>FREE</status>
  <synopsis>Verify that subnet mask of DHCPv4 server pool cannot be set with Network broadcast IP address. (ex.10.0.0.255). Ensure that DHCP configuration on client is not affected</synopsis>
  <groups_id/>
  <execution_time>30</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Broadband</box_type>
    <box_type>Emulator</box_type>
    <box_type>RPI</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_268</test_case_id>
    <test_objective>Verify that subnet mask of DHCPv4 server pool cannot be set with Network broadcast IP address. (ex.10.0.0.255). Ensure that DHCP configuration on client is not affected</test_objective>
    <test_type>Negative</test_type>
    <test_setup>Broadband,Emulator,RPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress
Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanSubnetMask
Device.DHCPv4.Server.Pool.1.MinAddress
Device.DHCPv4.Server.Pool.1.MaxAddress</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save LanIP,SubnetMask,Maximum and minimum Address range
3. Set LanIP,SubnetMask,Maximum and minimum Address range as ClassA using tdkb_e2e_SetMultipleParams
4. Set subnetmask to network broadcast ip using tdkb_e2e_SetMultipleParams and it should fail
5.  Connect to the LAN client and check whether the subnetmask is changed or not
5. Revert the values to original value
6.Unload tdkb_e2e module</automation_approch>
    <except_output>DHCP configuration on client should not be affected by setting subnetmask as network broadcast ip</except_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_DHCP_SetSubnetMask_NetworkBroadcastIP</test_script>
    <skipped>No</skipped>
    <release_version>M55</release_version>
    <remarks>LAN</remarks>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
import tdkbE2EUtility
from tdkbE2EUtility import *;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1");

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_DHCP_SetSubnetMask_NetworkBroadcastIP');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        lanIPAddress = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        lanSubnetMask = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanSubnetMask"
        minAddress = "Device.DHCPv4.Server.Pool.1.MinAddress"
        maxAddress = "Device.DHCPv4.Server.Pool.1.MaxAddress"

        #Get the value of the wifi parameters that are currently set.
        paramList=[lanIPAddress,lanSubnetMask,minAddress,maxAddress]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS");
            print("TEST STEP 1: Get the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print("EXPECTED RESULT 1: Should retrieve the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : SUCCESS");

            # Set the lanIPAddress,lanSubnetMask,minAddress and maxAddress"
            setValuesList = ['10.0.0.1','255.255.255.0','10.0.0.2','10.0.0.253'];
            print("Parameter values that are set: %s" %setValuesList)


            list1 = [lanIPAddress,'10.0.0.1','string']
            list2 = [lanSubnetMask,'255.255.255.0','string']
            list3 = [minAddress,'10.0.0.2','string']
            list4 = [maxAddress,'10.0.0.253','string']

            #Concatenate the lists with the elements separated by pipe
            setParamList= list1 + list2 + list3 + list4
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS");
                print("TEST STEP 2: Set the lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                print("EXPECTED RESULT 2: Should set the lanIPAddress,lanSubnetMask,minAddress and maxAddress");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");

                #Retrieve the values after set and compare
                newParamList=[lanIPAddress,lanSubnetMask,minAddress,maxAddress]
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("TEST STEP 3: Get the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print("EXPECTED RESULT 3: Should retrieve the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : SUCCESS");

                    #Wait for the changes to reflect in client device
                    time.sleep(60);

                    # Set the LanIPAddress to network broadcast IP address"
                    subnetMask = "%s|10.0.0.255|string" %lanSubnetMask

                    tdkTestObj,status,details = setMultipleParameterValues(obj,subnetMask)
                    if expectedresult not in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("TEST STEP 4: Set the SubnetMask to network broadcast IP, 10.0.0.255")
                        print("EXPECTED RESULT 4: Should not set the SubnetMask");
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");

                        #Retrieve the values after set and compare
                        tdkTestObj,retStatus,newSubnetMask = getParameterValue(obj,lanSubnetMask)
                        print("LanSubnetMask: %s" %newSubnetMask);

                        if expectedresult in retStatus and newSubnetMask != "10.0.0.255":
                            tdkTestObj.setResultStatus("SUCCESS");
                            print("TEST STEP 5: Get the current subnetMask")
                            print("EXPECTED RESULT 5: Should retrieve the current subnetMask")
                            print("ACTUAL RESULT 5: %s " %newSubnetMask);
                            print("[TEST EXECUTION RESULT] : SUCCESS");

                            #Wait for the changes to reflect in client device
                            time.sleep(60);

                            #Connect to Lan Client and get the subnetMask
                            print("TEST STEP 6:Connect to LAN Client and get the subnetMask")
                            subnetMask = getLanSubnetMask(tdkbE2EUtility.lan_interface);
                            if subnetMask and "10.0.0.255" not in subnetMask:
                                tdkTestObj.setResultStatus("SUCCESS");
                                print(" subnet mask has not changed as network broadcast ip value")
                                finalStatus = "SUCCESS";
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("subnet mask has changed as network broadcast ip value")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 5: Get the current subnetmask")
                            print("EXPECTED RESULT 5: Should retrieve the current subnetmask")
                            print("ACTUAL RESULT 5: %s " %newSubnetMask);
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("TEST STEP 4: Set the subnetMask to a network broadcast IP, 10.0.0.255")
                        print("EXPECTED RESULT 4: Should not set the subnetMask");
                        print("ACTUAL RESULT 4: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("TEST STEP 3: Get the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print("EXPECTED RESULT 3: Should retrieve the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print("ACTUAL RESULT 3: %s" %newValues);
                    print("[TEST EXECUTION RESULT] : FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("TEST STEP 2: Set the lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                print("EXPECTED RESULT 2: Should set the lanIPAddress,lanSubnetMask,minAddress and maxAddress");
                print("ACTUAL RESULT 2: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");

            #Prepare the list of parameter values to be reverted

            list1 = [lanIPAddress,orgValue[0],'string']
            list2 = [lanSubnetMask,orgValue[1],'string']
            list3 = [minAddress,orgValue[2],'string']
            list4 = [maxAddress,orgValue[3],'string']

            #Concatenate the lists with the elements separated by pipe
            revertParamList = list1 + list2 + list3 +list4
            revertParamList = "|".join(map(str, revertParamList))

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS");
                print("EXPECTED RESULT 6: Should set the original lanIPAddress,lanSubnetMask,minAddress and maxAddress");
                print("ACTUAL RESULT 6: %s" %details);
                print("[TEST EXECUTION RESULT] : SUCCESS");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                details = tdkTestObj.getResultDetails();
                print("EXPECTED RESULT 6: Should set the original lanIPAddress,lanSubnetMask,minAddress and maxAddress");
                print("ACTUAL RESULT 6: %s" %details);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("TEST STEP 1: Get the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print("EXPECTED RESULT 1: Should retrieve the current lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print("ACTUAL RESULT 1: %s" %orgValue);
            print("[TEST EXECUTION RESULT] : FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");