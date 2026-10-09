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

ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_ConnectWithInvalidKey');

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

            paramList = [ssidName, keyPassPhrase]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print("TEST STEP 1: Get the current ssid and keypassphrase")
                print("EXPECTED RESULT 1: Should retrieve the current ssid and keypassphrase")
                print("ACTUAL RESULT 1: %s" %orgValue)
                print("[TEST EXECUTION RESULT] : SUCCESS")

                if tdkbE2EUtility.ssid_name == orgValue[0] and tdkbE2EUtility.ssid_pwd == orgValue[1]:
                    print("The current ssid and keypassphrase are same as configured in the device configuration file")
                    tdkTestObj.setResultStatus("SUCCESS")

                    #Try to connect with invalid passphrase - connection should fail
                    print("TEST STEP 2: From wlan client, try to connect to the wifi ssid using invalid passphrase")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_invalid_pwd,tdkbE2EUtility.wlan_interface);
                    if "SUCCESS" not in status:
                        tdkTestObj.setResultStatus("SUCCESS");
                        finalStatus = "SUCCESS";
                        print("EXPECTED RESULT 2: WLAN client should not connect using invalid passphrase")
                        print("ACTUAL RESULT 2: Connection with invalid passphrase failed as expected")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("EXPECTED RESULT 2: WLAN client should not connect using invalid passphrase")
                        print("ACTUAL RESULT 2: Connection with invalid passphrase unexpectedly succeeded")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("The current ssid and keypassphrase are not same as configured in the device configuration file")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("TEST STEP 1: Get the current ssid and keypassphrase")
                print("EXPECTED RESULT 1: Should retrieve the current ssid and keypassphrase")
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
