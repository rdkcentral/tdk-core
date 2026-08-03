##########################################################################
# If not stated otherwise in this file or this component's LICENSE
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

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box IP and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_LAN_AccessInternet')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "True":
            print("MLO is enabled in the device configuration file.")

            #Get the Gateway LAN IP address from DUT first to obtain a valid tdkTestObj
            print(f"\nTEST STEP {step}: Get the Gateway LAN IP address from DUT")
            print(f"EXPECTED RESULT {step}: Should retrieve Gateway LAN IP address successfully")
            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
            tdkTestObj, status, curIPAddress = getParameterValue(obj, param)
            if expectedresult in status and curIPAddress:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Gateway LAN IP is {curIPAddress}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Get the LAN client IP address
                step += 1
                print(f"\nTEST STEP {step}: Get the IP address of the LAN client")
                print(f"EXPECTED RESULT {step}: Should retrieve LAN client IP address")
                lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface)
                if lanIP:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: LAN client IP is {lanIP}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Check LAN IP is in DHCP range
                    step += 1
                    print(f"\nTEST STEP {step}: Check whether LAN IP address is in the DHCP range")
                    print(f"EXPECTED RESULT {step}: LAN IP should be in the DHCP range")
                    status = checkIpRange(curIPAddress, lanIP)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: LAN IP is in the DHCP range")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Ping internet host from LAN client
                        step += 1
                        print(f"\nTEST STEP {step}: Verify LAN client has internet access by pinging {tdkbE2EUtility.network_ip}")
                        print(f"EXPECTED RESULT {step}: LAN client should successfully ping the internet host")
                        status = verifyNetworkConnectivity(tdkbE2EUtility.network_ip, "PING_TO_HOST", lanIP, curIPAddress, "LAN")
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            finalStatus = "SUCCESS"
                            print(f"ACTUAL RESULT {step}: Internet access verified successfully via ping")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: LAN client could not ping internet host")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: LAN IP is not in the DHCP range")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to get LAN client IP address")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to retrieve Gateway LAN IP address")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            print("MLO is disabled in the device configuration file.")
            obj.setLoadModuleStatus("FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")

else:
    print("Failed to load tdkb_e2e module")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed")

