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
obj.configureTestCase(ip,port,'E2E_WIFI_FirewallHigh_TCPFromWlanToLan');

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus) ;

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS");
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    status = parseDeviceConfig(obj);
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS");
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "True":
            print("MLO is enabled in the device configuration file.")

            ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            firewallLevel = "Device.X_CISCO_COM_Security.Firewall.FirewallLevel"

            paramList = [ssidName, keyPassPhrase, firewallLevel]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print("TEST STEP 1: Get the current ssid, keypassphrase and firewallLevel")
                print("EXPECTED RESULT 1: Should retrieve the current ssid, keypassphrase and firewallLevel")
                print("ACTUAL RESULT 1: %s" %orgValue)
                print("[TEST EXECUTION RESULT] : SUCCESS")

                if tdkbE2EUtility.ssid_name == orgValue[0] and tdkbE2EUtility.ssid_pwd == orgValue[1]:
                    print("The current ssid and keypassphrase are same as configured in the device configuration file")
                    tdkTestObj.setResultStatus("SUCCESS")

                    firewallParam = "%s|High|string" %firewallLevel
                    tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
                    if expectedresult in firewallResult:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("TEST STEP 2: Set firewallLevel to High")
                        print("EXPECTED RESULT 2: Should set firewallLevel to High")
                        print("ACTUAL RESULT 2: %s" %details)
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        time.sleep(60);

                        print("TEST STEP 3: From wlan client, Connect to the wifi ssid")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface);
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS");

                            print("TEST STEP 4: Get the IP address of the wlan client after connecting to wifi")
                            wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface);
                            if wlanIP:
                                tdkTestObj.setResultStatus("SUCCESS");

                                print("TEST STEP 5: Get the current LAN IP address DHCP range")
                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                print("LAN IP Address: %s" %curIPAddress);

                                if expectedresult in status and curIPAddress:
                                    tdkTestObj.setResultStatus("SUCCESS");

                                    print("TEST STEP 6: Check whether wlan ip address is in same DHCP range")
                                    status = "SUCCESS"
                                    status = checkIpRange(curIPAddress,wlanIP);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");

                                        print("TEST STEP 7: Get the IP address of the lan client after connecting to it")
                                        lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface);
                                        if lanIP:
                                            tdkTestObj.setResultStatus("SUCCESS");

                                            print("TEST STEP 8: Check whether lan ip address is in same DHCP range")
                                            status = "SUCCESS"
                                            status = checkIpRange(curIPAddress,lanIP);
                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS");

                                                print("TEST STEP 9: Check TCP from WLAN to LAN");
                                                status,serverOutput,clientOutput = tcp_udpInClients("WLAN","LAN",lanIP,wlanIP);
                                                print("Bandwidth recieved from server : %s" %serverOutput);
                                                print("Bandwidth recieved from client : %s" %clientOutput);
                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS");
                                                    print("Bandwidth recieved from server is greater than that from client")
                                                    print("TCP from WLAN to LAN : SUCCESS")

                                                    print("TEST STEP 10: From wlan client, Disconnect from the wifi ssid")
                                                    status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface);
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS");
                                                        finalStatus = "SUCCESS";
                                                        print("Disconnect from WIFI SSID: SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE");
                                                        print("TEST STEP 10: Disconnect from WIFI SSID: FAILED")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE");
                                                    print("TEST STEP 9: TCP from WLAN to LAN failed")
                                                    print("Bandwidth recieved from server is not greater than that from client")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE");
                                                print("TEST STEP 8: checkIpRange:lan ip address is not in DHCP range")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print("TEST STEP 7: getLanIPAddress:Failed to get the LAN client IP")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE");
                                        print("TEST STEP 6: checkIpRange:wlan ip address is not in DHCP range")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE");
                                    print("TEST STEP 5: getParameterValue : Failed to get gateway lan ip")
                            else:
                                tdkTestObj.setResultStatus("FAILURE");
                                print("TEST STEP 4: getWlanIPAddress:Failed to get the wlan ip address")
                        else:
                            tdkTestObj.setResultStatus("FAILURE");
                            print("TEST STEP 3: wlanConnectWifiSsid: Failed to connect to the wifi ssid")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("TEST STEP 2: Set firewallLevel to High: FAILED")
                        print("[TEST EXECUTION RESULT] : FAILURE")

                    firewallParam = "%s|%s|string" %(firewallLevel,orgValue[2])
                    tdkTestObj,firewallResult,details = setMultipleParameterValues(obj,firewallParam)
                    if expectedresult in firewallResult and expectedresult in finalStatus:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print("EXPECTED RESULT 15: Should revert the firewallLevel to original value");
                        print("ACTUAL RESULT 15: %s" %details);
                        print("[TEST EXECUTION RESULT] : SUCCESS");
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        details = tdkTestObj.getResultDetails();
                        print("EXPECTED RESULT 15: Should revert the firewallLevel to original value");
                        print("ACTUAL RESULT 15: %s" %details);
                        print("[TEST EXECUTION RESULT] : FAILURE");
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("The current ssid and keypassphrase are not same as configured in the device configuration file")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 1: Get the current ssid, keypassphrase and firewallLevel")
                print("EXPECTED RESULT 1: Should retrieve the current ssid, keypassphrase and firewallLevel")
                print("ACTUAL RESULT 1: %s" %orgValue);
                print("[TEST EXECUTION RESULT] : FAILURE");
        else:
            print("MLO is disabled in the device configuration file.")
            obj.setLoadModuleStatus("FAILURE");
    else:
        obj.setLoadModuleStatus("FAILURE");
        print("Failed to parse the device configuration file")

    postExecutionCleanup();
    obj.unloadModule("tdkb_e2e");

else:
    print("Failed to load tdkb_e2e module");
    obj.setLoadModuleStatus("FAILURE");
    print("Module loading failed");
