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

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_SANITY_WIFI_CheckSSIDBroadcast')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"
    step = 1
    status = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        if tdkbE2EUtility.mlo_capability == "False":
            #Assign the WIFI parameters names to a variable
            ssidName_2g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
            keyPassPhrase_2g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
            ssidName_5g = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
            keyPassPhrase_5g = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index

            paramList = [ssidName_2g,keyPassPhrase_2g,ssidName_5g,keyPassPhrase_5g]
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd]
            ssidList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_5ghz_name]

            setList1 = [ssidName_2g,tdkbE2EUtility.ssid_2ghz_name,'string']
            setList2 = [keyPassPhrase_2g,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            setList3 = [ssidName_5g,tdkbE2EUtility.ssid_5ghz_name,'string']
            setList4 = [keyPassPhrase_5g,tdkbE2EUtility.ssid_5ghz_pwd,'string']
            setParamList = setList1 + setList2 + setList3 + setList4
        else:
            #Assign the MLO WIFI parameters names to a variable
            mloSsidIndex = tdkbE2EUtility.ssid_2ghz_index
            mloSsidName = "Device.WiFi.SSID.%s.SSID" %mloSsidIndex
            mloKeyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %mloSsidIndex

            paramList = [mloSsidName,mloKeyPassPhrase]
            setValuesList = [tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd]
            ssidList = [tdkbE2EUtility.ssid_name]

            setList1 = [mloSsidName,tdkbE2EUtility.ssid_name,'string']
            setList2 = [mloKeyPassPhrase,tdkbE2EUtility.ssid_pwd,'string']
            setParamList = setList1 + setList2

        #Get the value of the wifi parameters that are currently set.
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status and orgValue != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current WiFi SSID and keypassphrase values")
            print(f"EXPECTED RESULT {step}: Should retrieve the current WiFi SSID and keypassphrase values")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            print("WIFI parameter values that are set: %s" %setValuesList)

            #Concatenate the lists with the elements separated by pipe
            setParamList = "|".join(map(str, setParamList))

            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
            step = step + 1

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"\nTEST STEP {step}: Set the WiFi SSID and keypassphrase values")
                print(f"EXPECTED RESULT {step}: Should set the WiFi SSID and keypassphrase values")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                tdkTestObj,status,newValues = getMultipleParameterValues(obj,paramList)
                step = step + 1

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Get the updated WiFi SSID and keypassphrase values")
                    print(f"EXPECTED RESULT {step}: Should retrieve the updated WiFi SSID and keypassphrase values")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    #Check if the SSID name is listed in wifi client
                    step = step + 1
                    print(f"\nTEST STEP {step}: Check if the configured WiFi SSID names are listed in WiFi client")
                    print(f"EXPECTED RESULT {step}: Configured WiFi SSID names should be broadcasted on the network")

                    ssidBroadcastStatus = "SUCCESS"
                    for ssid in ssidList:
                        status = wlanIsSSIDAvailable(ssid)
                        if expectedresult in status:
                            print("Network name",ssid,"is broadcasted on the network")
                        else:
                            ssidBroadcastStatus = "FAILURE"
                            print("Network name",ssid,"is not broadcasted on the network")

                    if expectedresult in ssidBroadcastStatus:
                        tdkTestObj.setResultStatus("SUCCESS")
                        finalStatus = "SUCCESS"
                        print(f"ACTUAL RESULT {step}: Configured WiFi SSID names are broadcasted")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: One or more configured WiFi SSID names are not broadcasted")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nTEST STEP {step}: Get the updated WiFi SSID and keypassphrase values")
                    print(f"EXPECTED RESULT {step}: Should retrieve the updated WiFi SSID and keypassphrase values")
                    print(f"ACTUAL RESULT {step}: {newValues}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"\nTEST STEP {step}: Set the WiFi SSID and keypassphrase values")
                print(f"EXPECTED RESULT {step}: Should set the WiFi SSID and keypassphrase values")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")

            step = step + 1
            print(f"\nTEST STEP {step}: Revert the WiFi SSID and keypassphrase values to original")
            print(f"EXPECTED RESULT {step}: Should set the original WiFi SSID and keypassphrase values")

            if len(orgValue) == len(paramList):
                #Prepare the list of parameter values to be reverted
                revertParamList = []
                index = 0
                for param in paramList:
                    revertParamList = revertParamList + [param,orgValue[index],'string']
                    index = index + 1

                #Concatenate the lists with the elements separated by pipe
                revertParamList = "|".join(map(str, revertParamList))

                #Revert the values to original
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)

                if expectedresult in actualresult and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to revert because the retrieved original values are incomplete")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"\nTEST STEP {step}: Get the current WiFi SSID and keypassphrase values")
            print(f"EXPECTED RESULT {step}: Should retrieve the current WiFi SSID and keypassphrase values")
            print(f"ACTUAL RESULT {step}: {orgValue}")
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