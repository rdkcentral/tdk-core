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
import sys
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_ACL_VerifyMacFilterDefaultValues_FactoryReset')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0
    # Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        #save device's current state before it goes for reboot
        obj.saveCurrentState()

        #Initiate Factory reset
        step +=1
        print(f"\nTEST STEP {step}: Initiate factory reset on DUT")
        print(f"EXPECTED RESULT {step}: Factory reset  should be initiated on DUT succesfully")
        tdkTestObj = obj.createTestStep('tdkb_e2e_Set')
        tdkTestObj.addParameter("paramName","Device.X_CISCO_COM_DeviceControl.FactoryReset")
        tdkTestObj.addParameter("paramValue","Router,Wifi,VoIP,Dect,MoCA")
        tdkTestObj.addParameter("paramType","string")
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Initiated factory reset on the DUT successfully")
            #Get the result of execution
            print("[TEST EXECUTION RESULT] : SUCCESS")

            #Restore the device state saved before reboot
            obj.restorePreviousStateAfterReboot()
            #Wait upto 5 min for DUT to come up
            print("Sleeping 5 min for DUT to come up")
            time.sleep(300)

            step+=1
            print(f"\nTEST STEP {step}: Verify that the last reboot reason is 'factory-reset'")
            print(f"EXPECTED RESULT {step}: The last reboot reason should be 'factory-reset'" )
            tdkTestObj,actualresult,rebootReason = getParameterValue(obj,"Device.DeviceInfo.X_RDKCENTRAL-COM_LastRebootReason")
            if expectedresult in actualresult and rebootReason == "factory-reset":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Got the last reboot reason as '{rebootReason}' confirmed the DUT's factory reset." )
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Get the number of radios
                step+=1
                print(f"\nTEST STEP {step} : Get the number of radio entries.")
                print(f"EXPECTED RESULT {step} : Should get the number of radio entries.")
                tdkTestObj,actualresult,radioCount = getParameterValue(obj,"Device.WiFi.RadioNumberOfEntries")
                if expectedresult in actualresult and radioCount != "" :
                    #Set the result of execution
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Got the number of radio entries as {radioCount} successfully.")
                    #Get the result of execution
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    radioCount = int(radioCount)
                    #Get the accesspoint indexes of Radios supported
                    if radioCount == 3:
                        ap_indices = [1,2,17]
                    elif radioCount == 2:
                        ap_indices = [1,2]
                    else:
                        print(f"Unknown radio count: {radioCount}")
                        obj.unloadModule("tdkb_e2e")
                        sys.exit(0)
                    flag =1
                    for index in ap_indices:
                        step+=1
                        print(f"\n***************For radio index : {index}*********************")
                        param1 = "Device.WiFi.AccessPoint." + str(index) + ".X_CISCO_COM_MACFilter.Enable"
                        print(f"\nTEST STEP {step}: Verify that Mac Filter Enable {param1} is 'false' as default value.")
                        print(f"EXPECTED RESULT {step}: Mac Filter Enable {param1} should be 'false' as default value.")
                        tdkTestObj,actualresult,macFilterEnable = getParameterValue(obj,param1)
                        if expectedresult in actualresult  and macFilterEnable == "false" :
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Mac Filter Enable {param1} is '{macFilterEnable}' as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Mac Filter Enable {param1} is '{macFilterEnable}' which is not expected as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        step+=1
                        param2 = "Device.WiFi.AccessPoint." + str(index) + ".X_CISCO_COM_MACFilter.FilterAsBlackList"
                        print(f"\nTEST STEP {step}: Verify that Mac FilterAsBlacklist {param2} is 'false' as default value.")
                        print(f"EXPECTED RESULT {step}: Mac FilterAsBlacklist {param2} should be 'false' as default value.")
                        tdkTestObj,actualresult,FilterAsBlackList = getParameterValue(obj,param2)
                        if expectedresult in actualresult  and FilterAsBlackList == "false" :
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Mac FilterAsBlacklist {param2} is '{FilterAsBlackList}' as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Mac FilterAsBlacklist {param2} is '{FilterAsBlackList}' which is not expected as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        step+=1
                        param3 = "Device.WiFi.AccessPoint." + str(index) + ".X_COMCAST-COM_MAC_FilteringMode"
                        print(f"\nTEST STEP {step}: Verify that Mac Filtering mode {param3} is 'Allow-ALL' as default value")
                        print(f"EXPECTED RESULT {step}: Mac Filtering mode {param3} should be 'Allow-ALL' as default value.")
                        tdkTestObj,actualresult,mode = getParameterValue(obj,param3)
                        if expectedresult in actualresult  and mode == "Allow-ALL" :
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Mac Filtering mode {param3} is '{mode}' as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            flag = 0
                            #Set the result status of execution
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Mac Filtering mode {param3} is '{mode}' which is not expected as default value.")
                            #Get the result of execution
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    if flag:
                        print("\n************************************")
                        print("\nCheck for a generic wifi connection")
                        #Assign the WIFI parameters names to a variable
                        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
                        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index

                        step+=1
                        #Get the value of the wifi parameters that are currently set.
                        paramList=[ssidName,keyPassPhrase]
                        print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase.")
                        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)
                        if expectedresult in status and orgValue != "":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Got the current ssid and keypassphrase as {orgValue}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd]
                            print("WIFI parameter values that are set: %s" %setValuesList)

                            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']

                            #Concatenate the lists with the elements separated by pipe
                            setParamList = list1 + list2
                            setParamList = "|".join(map(str, setParamList))

                            step+=1
                            print(f"\nTEST STEP {step}: Set the ssid and keypassphrase.")
                            print(f"EXPECTED RESULT {step}: Should set the ssid and keypassphrase.")
                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: {details}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                #Retrieve the values after set and compare
                                step+=1
                                newParamList=[ssidName,keyPassPhrase]
                                print(f"\nTEST STEP {step}: Get the current ssid and keypassphrase")
                                print(f"EXPECTED RESULT {step}: Should retrieve the current ssid and keypassphrase")
                                tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                                if expectedresult in status and setValuesList == newValues:
                                    tdkTestObj.setResultStatus("SUCCESS");
                                    print(f"ACTUAL RESULT {step}: Got the current ssid and keypassphrase as {newValues}");
                                    print("[TEST EXECUTION RESULT] : SUCCESS");

                                    #Wait for the changes to reflect in client device
                                    time.sleep(60);

                                    #Connect to the wifi ssid from wlan client
                                    step+=1
                                    print(f"\nTEST STEP {step} : From wlan client, Connect to the wifi ssid")
                                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface);
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print(f"ACTUAL RESULT {step} : Connection with client is success as expected  : {status}.")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                        #To get channel number to understand the radio Index
                                        channelno = 0
                                        channel = tdkbE2EUtility.getChannelNumberBssid()
                                        if channel !="":
                                            channelno = int(channel)
                                            print(f"Channel in-use : {channelno}")
                                        else:
                                            print(f"Channel is empty")
                                        step+=1
                                        print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                        status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_2ghz_interface);
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS");
                                            print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: SUCCESS")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE");
                                            print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: FAILED")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step} : Connection attempt failed which is not expected  : {status}.")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to get the current ssid and keypassphrase as {newValues}")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: {details}")
                                print("[TEST EXECUTION RESULT] : FAILURE")

                            #Prepare the list of parameter values to be reverted
                            list1 = [ssidName,orgValue[0],'string']
                            list2 = [keyPassPhrase,orgValue[1],'string']

                            #Concatenate the lists with the elements separated by pipe
                            revertParamList = list1 + list2
                            revertParamList = "|".join(map(str, revertParamList))

                            step+=1
                            #Revert the values to original
                            print(f"\nTEST STEP {step}: Set the original ssid and keypassphrase.")
                            print(f"EXPECTED RESULT {step}: Should set the original ssid and keypassphrase.")
                            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                            details = tdkTestObj.getResultDetails()
                            if expectedresult in actualresult:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: {details}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: {details}")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get the current ssid and keypassphrase.")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        print("\n Failed to get filtering mode as 'ALLOW-ALL'  after Factory reset.")
                else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to get the radio number of entries.")
                        print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Got the last reboot reason as '{rebootReason}', which does not match the expected value 'factory-reset'")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}:  Failed to factory reset the DUT")
            print("[TEST EXECUTION RESULT] : FAILURE")

    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f" ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load tdkb_e2e module")
    print("Module loading failed")
