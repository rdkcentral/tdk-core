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
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
sysobj = tdklib.TDKScriptingLibrary("sysutil","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_TCPFromLanToWan_GetThroughput')
sysobj.configureTestCase(ip,port,'E2E_TCPFromLanToWan_GetThroughput')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)
loadmodulestatus1 =sysobj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus1)
if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() :
    obj.setLoadModuleStatus("SUCCESS")
    sysobj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        step += 1
        print(f"\nTEST STEP {step}: Get the gateway IP of the DUT")
        print(f"EXPECTED RESULT {step}: Should get the gateway IP of the DUT")
        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        tdkTestObj,actualresult,curIPAddress = getParameterValue(obj,param)
        if expectedresult in actualresult and curIPAddress != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Got the gateway IP as {curIPAddress}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            step += 1
            #Connect to LAN client and obtain its IP
            print(f"\nTEST STEP {step}: Get the IP address of the lan client after connecting to it")
            print(f"EXPECTED RESULT {step}: Should get the IP address of the lan client after connecting to it")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface)
            if lanIP != "":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Got the IP address of the lan client as {lanIP}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                step += 1
                print(f"\nTEST STEP {step}: Check whether lan ip address is in same DHCP range")
                print(f"EXPECTED RESULT {step}: lan ip address should be in same DHCP range")
                status = checkIpRange(curIPAddress,lanIP)
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: lan ip address is in same DHCP range")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    step += 1
                    print(f"\nTEST STEP {step}: Add static route from lan client to wan via gateway")
                    print(f"EXPECTED RESULT {step}: Should add static route from lan client to wan via gateway")
                    status = addStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress,tdkbE2EUtility.lan_interface,"LAN")
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Successfully added the static add route from lan client to wan via gateway")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        step += 1
                        #Verify TCP from LAN to WAN
                        print(f"\nTEST STEP {step}: Check TCP from LAN to WAN")
                        print(f"EXPECTED RESULT {step}: Should check TCP from LAN to WAN")
                        status,serverOutput,clientOutput = tcp_udpInClients("LAN","WAN",tdkbE2EUtility.wan_ip,lanIP,"TCP_Throughput")
                        if expectedresult in status and serverOutput != "":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: TCP from LAN to WAN is successful")
                            print(f"Bandwidth recieved from server : {serverOutput}")
                            throughput = getThroughputInMbps(serverOutput)
                            print(f"Measured throughput: {throughput}")
                            raw_threshold = str(tdkbE2EUtility.lan_throughput_to_wan).strip()
                            if raw_threshold.isdigit():
                                threshold = int(raw_threshold)
                            perf_offset = 5
                            lowerBound = threshold - perf_offset
                            upperBound = threshold + perf_offset

                            step += 1
                            print(f"\nTEST STEP {step}: Check if the throughput is in desirable throughput  range.")
                            print(f"EXPECTED RESULT {step}: Throughput should be in desirable range.")
                            print(f"Actual Throughput(Mbps): {throughput}")
                            print(f"Desirable throughput range (Mbps): {lowerBound} - {upperBound}")
                            if  throughput >= lowerBound and throughput <= upperBound:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Throughput  is within desirable range.")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Throughput  is outside desirable range.")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to perform TCP from LAN to WAN.")
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        step += 1
                        #delete the added route
                        print(f"\nTEST STEP {step}: Delete the static route added from lan client to wan via gateway")
                        print(f"EXPECTED RESULT {step}: Should delete the static route added from lan client to wan via gateway successfully")
                        status = delStaticRoute(tdkbE2EUtility.wan_ip, curIPAddress,tdkbE2EUtility.lan_interface,"LAN")
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Successfully deleted the added route from lan client to wan via gateway")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to delete the added route from lan client to wan via gateway")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to add static route from lan client to wan via gateway")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: lan ip address is not in DHCP range")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to get the LAN client IP")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to get the gateway ip")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")
    clientDisconnect()
    obj.unloadModule("tdkb_e2e")
    sysobj.unloadModule("sysutil")
else:
    print("Failed to load tdkb_e2e and sysutil module")
    obj.setLoadModuleStatus("FAILURE")
    sysobj.setLoadModuleStatus("FAILURE")
    print("Modules loading failed")