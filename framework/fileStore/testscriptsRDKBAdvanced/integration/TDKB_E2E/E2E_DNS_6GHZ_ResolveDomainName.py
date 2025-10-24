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
  <name>E2E_DNS_6GHZ_ResolveDomainName</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>tdkb_e2e_SetMultipleParams</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>Verify that the DNS server of WG successfully resolves the DNS queries in 6GHz WLAN client</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>BPI</box_type>
    <!--  -->
    <box_type>Broadband</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDKB</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>TC_TDKB_E2E_652</test_case_id>
    <test_objective>Verify that the DNS server of WG successfully resolves the DNS queries in 6GHz WLAN client</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Broadband,BPI</test_setup>
    <pre_requisite>Ensure the client setup is up with the IP address assigned by the gateway</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>Device.WiFi.SSID.{i}.SSID
    Device.WiFi.AccessPoint.{i}.Security.KeyPassphrase
    Device.DNS.Client.Server.1.DNSServer</input_parameters>
    <automation_approch>1. Load tdkb_e2e module
2. Using tdkb_e2e_Get, get and save Primary DNS Server IP
3. Connect the WiFi client to the 6GHz SSID  of gateway
4. Check if the WiFi client's ip received from gateway is in valid range
5. Try to resolve the domain name from WLAN Client using nslookup with server as DNS server
6. Disconnect WiFi client
7. Unload tdkb_e2e module</automation_approch>
    <expected_output>WLAN client should be able to resolve the domain name with Primary DNS Server</expected_output>
    <priority>High</priority>
    <test_stub_interface>tdkb_e2e</test_stub_interface>
    <test_script>E2E_DNS_6GHZ_ResolveDomainName</test_script>
    <skipped></skipped>
    <release_version>M140</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''

# use tdklib library, which provides a wrapper for tdk testcase script
import tdklib
import time
from tdkbE2EUtility import *
import tdkbE2EUtility

# Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e", "1")

# IP and Port of box, No need to change,
# This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_DNS_6GHZ_ResolveDomainName')

# Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    # Parse the device configuration file
    print(f"TEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = parseDeviceConfig(obj)

    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")

        # Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        dnsServer = "Device.DNS.Client.Server.1.DNSServer"

        # Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, dnsServer]
        tdkTestObj, status, orgValue = getMultipleParameterValues(obj, paramList)

        step += 1
        print(f"TEST STEP {step}: Get the current value of ssid, Keypassphrase and DNS Server")
        print(f"EXPECTED RESULT {step}: Should retrieve the current values")

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")

            setValuesList = [tdkbE2EUtility.ssid_6ghz_name, tdkbE2EUtility.ssid_6ghz_pwd]
            print(f"WIFI parameter values that are set: {setValuesList}")

            list1 = [ssidName, tdkbE2EUtility.ssid_6ghz_name, 'string']
            list2 = [keyPassPhrase, tdkbE2EUtility.ssid_6ghz_pwd, 'string']

            # Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2
            setParamList = "|".join(map(str, setParamList))

            step += 1
            print(f"TEST STEP {step}: Set the ssid, keypassphrase")
            print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, setParamList)

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                # Retrieve the values after set and compare
                newParamList = [ssidName, keyPassPhrase]
                tdkTestObj, status, newValues = getMultipleParameterValues(obj, newParamList)

                step += 1
                print(f"TEST STEP {step}: Get the current ssid, keypassphrase")
                print(f"EXPECTED RESULT {step}: Should retrieve the ssid, keypassphrase")

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    # Wait for the changes to reflect in client device
                    time.sleep(60)

                    # Connect to the wifi ssid from wlan client
                    step += 1
                    print(f"TEST STEP {step}: From wlan client, Connect to the wifi ssid")
                    print(f"EXPECTED RESULT {step}: Should connect successfully")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Successfully connected to the wifi ssid")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        print(f"TEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                        print(f"EXPECTED RESULT {step}: Should retrieve a wlan client IP")
                        wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)

                        if wlanIP:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: wlan IP is {wlanIP}")
                            print(f"[TEST EXECUTION RESULT] : SUCCESS")

                            step += 1
                            print(f"TEST STEP {step}: Get the current LAN IP address DHCP range")
                            print(f"EXPECTED RESULT {step}: Should retrieve the LAN IP")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: LAN IP Address: {curIPAddress}")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                step += 1
                                print(f"TEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                print(f"EXPECTED RESULT {step}: WLAN IP should be in DHCP range")
                                status = checkIpRange(curIPAddress, wlanIP)

                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN IP is in DHCP range")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                    step += 1
                                    print(f"TEST STEP {step}: Connect to WLAN Client and do NSLookup")
                                    print(f"EXPECTED RESULT {step}: DNS should resolve domain name")
                                    status = nslookupInClient(tdkbE2EUtility.nslookup_domain_name, orgValue[2], 'WLAN')

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        finalStatus = "SUCCESS"
                                        print(f"ACTUAL RESULT {step}: DNS Primary Server successfully resolves the query")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                        #Disconnect wifi
                                        step += 1
                                        print(f"TEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                        print(f"EXPECTED RESULT {step}: Should disconnect successfully")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)

                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: WiFi disconnected successfully")
                                            print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Wifi disconnect failed")
                                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: DNS Primary Server failed to resolve query")
                                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: WLAN IP not in DHCP range")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Failed to get LAN IP range")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get WLAN IP")
                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to connect to wifi ssid")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {details}")
                print(f"[TEST EXECUTION RESULT] : FAILURE")

            # Prepare the list of parameter values to be reverted
            list1 = [ssidName, orgValue[0], 'string']
            list2 = [keyPassPhrase, orgValue[1], 'string']
            revertParamList = list1 + list2
            revertParamList = "|".join(map(str, revertParamList))

            step += 1
            print(f"TEST STEP {step}: Revert ssid,keypassphrase to original values")
            print(f"EXPECTED RESULT {step}: Should set original values")
            tdkTestObj, actualresult, details = setMultipleParameterValues(obj, revertParamList)

            if expectedresult in actualresult and expectedresult in finalStatus:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {details}")
                print(f"[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {tdkTestObj.getResultDetails()}")
                print(f"[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print(f"[TEST EXECUTION RESULT] : FAILURE")

    # Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")


