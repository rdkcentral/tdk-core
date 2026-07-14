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
import urllib.request, urllib.parse, urllib.error
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Wifi_Connect_Disconnect');
# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

thunderPort = None
# Get the thunder port from REST API
url = obj.url + '/deviceGroup/getThunderDevicePorts?stbIp=' + ip
try:
    data = urllib.request.urlopen(url).read()
    thunderPortDetails = json.loads(data)
    thunderPort = thunderPortDetails['thunderPort']
    print("THUNDER PORT : ", thunderPort)
except Exception as e:
    print("Unable to obtain Thunder Port from REST!!!")
    print("Error message received :\n", e)
    result = "FAILURE"

expectedResult = "SUCCESS"

if expectedResult in result.upper() and thunderPort is not None:

    # ------------------------------------------------------------------
    # Read WiFi config from device config file
    # ------------------------------------------------------------------
    configKeyList = ["WIFI_SSID_NAME", "WIFI_PASSPHRASE", "WIFI_SECURITY_MODE", "WIFI_SSID_NAME_5GHZ", "WIFI_PASSPHRASE_5GHZ", "WIFI_SECURITY_MODE_5GHZ"]
    configValues  = {}
    tdkTestObj    = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')

    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath",  obj.realpath)
        tdkTestObj.addParameter("configKey", configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print("SUCCESS: Retrieved %s from device config" % configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("FAILURE: Could not retrieve %s from device config" % configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break

    if "FAILURE" != result:
        VERIFY_WAIT = 10  # seconds to wait before second connection check

        # List of (label, ssid, passphrase, security) to iterate over
        wifi_profiles = [
            ("2.4GHz", configValues["WIFI_SSID_NAME"],      configValues["WIFI_PASSPHRASE"],      int(configValues["WIFI_SECURITY_MODE"])),
            ("5GHz",   configValues["WIFI_SSID_NAME_5GHZ"], configValues["WIFI_PASSPHRASE_5GHZ"], int(configValues["WIFI_SECURITY_MODE_5GHZ"])),
        ]

        for (band_label, WIFI_SSID, PASSPHRASE, SECURITY) in wifi_profiles:
            if "FAILURE" == result:
                break

            print("\n" + "="*60)
            print("INFO: Starting WiFi validation for %s band - SSID: %s" % (band_label, WIFI_SSID))
            print("="*60)

            # ==============================================================
            # STEP 1: WiFi Scan - start, wait for event, verify SSID, stop
            # ==============================================================
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_wifiStartScanAndVerify')
            tdkTestObj.addParameter("deviceIP",    ip)
            tdkTestObj.addParameter("thunderPort", thunderPort)
            tdkTestObj.addParameter("targetSSID",  WIFI_SSID)
            tdkTestObj.executeTestCase(expectedResult)
            result  = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails()
            print("[%s - STEP 1 - WiFi Scan] : %s | %s" % (band_label, result, details))
            print("")
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"

            # ==============================================================
            # STEP 2: WiFi Connect - trigger connect, wait for state event
            # ==============================================================
            if "FAILURE" != result:
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_wifiConnect')
                tdkTestObj.addParameter("deviceIP",    ip)
                tdkTestObj.addParameter("thunderPort", thunderPort)
                tdkTestObj.addParameter("ssid",        WIFI_SSID)
                tdkTestObj.addParameter("passphrase",  PASSPHRASE)
                tdkTestObj.addParameter("security",    SECURITY)
                tdkTestObj.executeTestCase(expectedResult)
                result  = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print("[%s - STEP 2 - WiFi Connect] : %s | %s" % (band_label, result, details))
                print("")
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    result = "FAILURE"

            # ==============================================================
            # STEP 3: Verify GetConnectedSSID - first check
            # ==============================================================
            if "FAILURE" != result:
                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_wifiVerifyConnectedSSID')
                tdkTestObj.addParameter("deviceIP",     ip)
                tdkTestObj.addParameter("thunderPort",  thunderPort)
                tdkTestObj.addParameter("expectedSSID", WIFI_SSID)
                tdkTestObj.executeTestCase(expectedResult)
                result  = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print("[%s - STEP 3 - GetConnectedSSID (first check)] : %s | %s" % (band_label, result, details))
                print("")
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    result = "FAILURE"

            # ==============================================================
            # STEP 4: Wait then re-verify GetConnectedSSID
            # ==============================================================
            if "FAILURE" != result:
                print("INFO: Waiting %ds before re-checking connection..." % VERIFY_WAIT)
                time.sleep(VERIFY_WAIT)

                tdkTestObj = obj.createTestStep('rdkv_basic_sanity_wifiVerifyConnectedSSID')
                tdkTestObj.addParameter("deviceIP",     ip)
                tdkTestObj.addParameter("thunderPort",  thunderPort)
                tdkTestObj.addParameter("expectedSSID", WIFI_SSID)
                tdkTestObj.executeTestCase(expectedResult)
                result  = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                print("[%s - STEP 4 - GetConnectedSSID (re-check)] : %s | %s" % (band_label, result, details))
                print("")
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    result = "FAILURE"

            # ==============================================================
            # STEP 5: WiFi Disconnect (always run per band)
            # ==============================================================
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_wifiDisconnect')
            tdkTestObj.addParameter("deviceIP",    ip)
            tdkTestObj.addParameter("thunderPort", thunderPort)
            tdkTestObj.executeTestCase(expectedResult)
            disc_result  = tdkTestObj.getResult()
            disc_details = tdkTestObj.getResultDetails()
            print("[%s - STEP 5 - WiFi Disconnect] : %s | %s" % (band_label, disc_result, disc_details))
            print("")
            if disc_result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"

    else:
        print("FAILURE: Failed to get configuration values from device config")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")

else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")