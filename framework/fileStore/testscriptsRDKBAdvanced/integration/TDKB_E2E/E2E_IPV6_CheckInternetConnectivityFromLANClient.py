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
import tdkbE2EUtility
from tdkbE2EUtility import *
import ipaddress

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_IPV6_CheckInternetConnectivityFromLANClient')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  : {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")
        step = 1

        wan_ip_address = "Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6"

        #Get the current WAN IPv6 address of the DUT
        print(f"\nTEST STEP {step}: Get the current WAN IPv6 address")
        print(f"EXPECTED RESULT {step}: Should retrieve the current WAN IPv6 address")
        tdkTestObj,status,wanIpv6Address = getParameterValue(obj,wan_ip_address)
        if expectedresult in status and wanIpv6Address != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {wanIpv6Address}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Connect to LAN client and get the IPv6 address of LAN client interface
            step += 1
            lanIPV6 = getLanIPV6Address(tdkbE2EUtility.lan_interface)
            print(f"\nTEST STEP {step}: Get the current IPV6 address of LAN client interface")
            print(f"EXPECTED RESULT {step}: The IPV6 address of lan client should be obtained")
            if lanIPV6:
                print(f"ACTUAL RESULT {step}: The IPV6 address of lan client is {lanIPV6}")
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                #Check whether the IPv6 Address obtained above is valid
                step += 1
                print(f"\nTEST STEP {step}: Check whether the IPv6 address obtained from LAN client is valid")
                print(f"EXPECTED RESULT {step}: The LAN client should have a valid IPv6 address")
                try:
                    ipaddress.IPv6Address(lanIPV6)
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: The IPv6 address {lanIPV6} is valid")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    #Check internet connectivity by pinging to an IPv6 host via lan interface
                    step += 1
                    print(f"\nTEST STEP {step}: Check internet connectivity by pinging to an IPv6 host via lan interface")
                    print(f"EXPECTED RESULT {step}: Should ping to an IPv6 host via lan interface")
                    status = verifyIPv6NetworkConnectivity("IPV6_PING_TO_HOST", tdkbE2EUtility.ipv6_host_name, tdkbE2EUtility.lan_interface, "LAN")
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Successfully pinged to an IPv6 host via lan interface")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS\n")
                    else:
                        print(f"ACTUAL RESULT {step}: Failed to ping to an IPv6 host via lan interface")
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"[TEST EXECUTION RESULT] : FAILURE\n")

                except ValueError:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: The IPv6 address {lanIPV6} is invalid")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to get the IPV6 address of lan client")
                print(f"[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {wanIpv6Address}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")