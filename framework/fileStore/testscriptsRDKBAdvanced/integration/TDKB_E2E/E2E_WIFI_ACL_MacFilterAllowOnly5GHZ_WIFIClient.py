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
import re
import time
import tdkutility
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WIFI_ACL_MacFilterAllowOnly5GHZ_WIFIClient')
obj1.configureTestCase(ip,port,'E2E_WIFI_ACL_MacFilterAllowOnly5GHZ_WIFIClient')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 =obj1.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    step = 0

    #Check for ACL test prerequisites
    tdkTestObj,preRequisiteStatus, step = tdkutility.set_ACLprerequisites_allRadios(obj,step)
    if "SUCCESS" in preRequisiteStatus:
        print("\n*******************ACL test prerequisites are SUCCESS************************")

        # Parse the device configuration file
        step+=1
        print(f"\nTEST STEP {step}: Parse the device configuration file.")
        print(f"EXPECTED RESULT {step}: Device configuration file should be parsed successfully.")
        status = tdkbE2EUtility.parseDeviceConfig(obj)
        if expectedresult in status:
            obj.setLoadModuleStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Parsed the device configuration file successfully.")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Get the MacAddress of wlan client
            step+=1
            print(f"\nTEST STEP {step}: Get MAC address of WLAN client.")
            print(f"EXPECTED RESULT {step}: Should get MAC address of WLAN client.")
            macAddress = tdkbE2EUtility.getWlanMACAddress_SSH(tdkbE2EUtility.wlan_5ghz_interface)
            if macAddress and (re.match("^[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macAddress.lower()) is not None):
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: MAC address of WLAN client is {macAddress}.")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                # Adding a new MACFilter rule for 5 GHz
                step+=1
                tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable." %tdkbE2EUtility.ssid_5ghz_index)
                print(f"\nTEST STEP {step}: Adding new Mac filter rule for 5GHz.")
                print(f"EXPECTED RESULT {step}: Should add new rule for 5GHz.")
                tdkTestObj.executeTestCase(expectedresult)
                actualresult = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()
                if expectedresult in actualresult:
                    #Set the result status of execution
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    instance = details.split(':')[1]
                    print(f"INSTANCE VALUE of 5Ghz : {instance}")

                    # Set  MAC of the device to be allowed
                    deviceMAC = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_5ghz_index}.X_CISCO_COM_MacFilterTable.{instance}.MACAddress"
                    step += 1
                    print(f"\nTEST STEP {step}: Set MAC of client device as in the filter for 5Ghz.")
                    print(f"EXPECTED RESULT {step}: Should set MAC of client device in the filter for 5Ghz.")
                    tdkTestObj = obj.createTestStep('tdkb_e2e_Set')
                    tdkTestObj.addParameter("paramName",deviceMAC)
                    tdkTestObj.addParameter("paramValue",macAddress)
                    tdkTestObj.addParameter("paramType","string")
                    tdkTestObj.executeTestCase(expectedresult)
                    actualresult = tdkTestObj.getResult()
                    details = tdkTestObj.getResultDetails()
                    if expectedresult in actualresult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Set Mac Filter MacAddress Entry for 5Ghz successfully.")
                        #Get the result of execution
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Get the BSSID of 5GHz
                        step+=1
                        bssidName = "Device.WiFi.SSID.%s.BSSID" %tdkbE2EUtility.ssid_5ghz_index
                        print(f"\nTEST STEP {step} : Get the bssid of 5GHz.")
                        print(f"EXPECTED RESULT {step} : Should get the bssid of 5GHz.")
                        tdkTestObj,actualresult,bssid = tdkbE2EUtility.getParameterValue(obj,bssidName)
                        if expectedresult in actualresult and bssid and (re.match("^[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", bssid.lower()) is not None):
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: BSSID of 5Ghz is {bssid}.")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Assign the WIFI parameters names to a variable
                            ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_5ghz_index
                            keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_5ghz_index
                            radioEnable = "Device.WiFi.Radio.%s.Enable" %tdkbE2EUtility.radio_5ghz_index
                            securityMode = "Device.WiFi.AccessPoint.%s.Security.ModeEnabled" %tdkbE2EUtility.ssid_5ghz_index

                            step+=1
                            #Get the value of the wifi parameters that are currently set.
                            paramList=[ssidName,keyPassPhrase,securityMode]
                            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and securityMode.")
                            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and securityMode.")
                            tdkTestObj,status,orgValue = tdkbE2EUtility.getMultipleParameterValues(obj,paramList)
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: Got the current ssid,keypassphrase and securityMode as {orgValue}.")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                # Set securityMode for 5ghz
                                setValuesList = [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,'WPA2-Personal']
                                print("\nWIFI parameter values that are set: %s" %setValuesList)

                                list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
                                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']
                                list3 = [securityMode,'WPA2-Personal','string']

                                #Concatenate the lists with the elements separated by pipe
                                setParamList = list1 + list2 + list3
                                setParamList = "|".join(map(str, setParamList))

                                step+=1
                                print(f"\nTEST STEP {step}: Set the ssid,keypassphrase and securityMode.")
                                print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase and securityMode.")
                                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: {details}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #Retrieve the values after set and compare
                                    step+=1
                                    newParamList=[ssidName,keyPassPhrase,securityMode]
                                    print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and securityMode.")
                                    print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and securityMode.")
                                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)
                                    if expectedresult in status and setValuesList == newValues:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Got the current ssid,keypassphrase and securityMode as {newValues}.")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #Wait for the changes to reflect in client device
                                        time.sleep(60);

                                        #Connect to the wifi ssid from wlan client
                                        step+=1
                                        print(f"\nTEST STEP {step} : From wlan client, Connect to the  wifi ssid via 5Ghz.")
                                        status = tdkbE2EUtility.wlanConnectWifiSsidBssid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,bssid,tdkbE2EUtility.wlan_5ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step} : Connected to wifi ssid via 5Ghz successfully : {status}.")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            step+=1
                                            print(f"\nTEST STEP {step}: Get the possible channels of 5GHz.")
                                            print(f"EXPECTED RESULT {step} : Should get the possible channels of 5GHz.")
                                            tdkTestObj,actualresult,details =  tdkbE2EUtility.getParameterValue(obj,"Device.WiFi.Radio.2.PossibleChannels")
                                            if expectedresult in actualresult and details != "":
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                possibleChannels = [int(x) for x in details.split(",")]
                                                print(f"ACTUAL RESULT{step} : Got the possible channels of 5Ghz as {possibleChannels}.")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                step+=1
                                                print(f"\nTEST STEP {step}: Verify if the channel belongs to 5Ghz supported channels which confirms the connection with 5GHz.")
                                                print(f"EXPECTED RESULT {step}: The channel should in the 5Ghz supported channels.")
                                                channel5 = 0
                                                channel = tdkbE2EUtility.getChannelNumberBssid()
                                                if channel !="":
                                                    channel5 = int(channel)
                                                    print(f"Channel in-use : {channel5}")
                                                else:
                                                    print(f"Channel is empty")
                                                if channel5 in possibleChannels:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f" ACTUAL RESULT {step} : The channel {channel5} is in possible channels of 5GHz .")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                    step+=1
                                                    print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid.")
                                                    status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: SUCCESS")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: FAILED")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f" ACTUAL RESULT {step} : The channel {channel5} is not in possible channels of 5Ghz.")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step} : Failed to get the possible channels of 5Ghz.")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step} : Failed to connect to wifi ssid.")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Failed to get the current ssid,keypassphrase and securityMode as {newValues}.")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: {details}")
                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                #Prepare the list of parameter values to be reverted
                                list1 = [ssidName,orgValue[0],'string']
                                list2 = [keyPassPhrase,orgValue[1],'string']
                                list3 = [securityMode,orgValue[2],'string']

                                #Concatenate the lists with the elements separated by pipe
                                revertParamList = list1 + list2 + list3
                                revertParamList = "|".join(map(str, revertParamList))

                                step+=1
                                #Revert the values to original
                                print(f"\nTEST STEP {step}: Set the original ssid,keypassphrase,securityMode.")
                                print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,securityMode.")
                                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,revertParamList)
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
                                print(f"ACTUAL RESULT {step}: Failed to get the current ssid,keypassphrase and securityMode.")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to get BSSID of 5Ghz : {bssid}")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to Set Mac Filter MacAddress Entry for 5Ghz.")
                        print("[TEST EXECUTION RESULT] : FAILURE")

                    #Delete the created table entry
                    step+=1
                    tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                    tdkTestObj.addParameter("paramName","Device.WiFi.AccessPoint.%s.X_CISCO_COM_MacFilterTable.%s." %(tdkbE2EUtility.ssid_5ghz_index,instance))
                    expectedresult = "SUCCESS"
                    print(f"\nTEST STEP {step}:  Delete the added rule for 5Ghz.")
                    print(f"EXPECTED RESULT {step} : Should delete the added rule for 5Ghz.")
                    tdkTestObj.executeTestCase(expectedresult)
                    actualresult = tdkTestObj.getResult()
                    details = tdkTestObj.getResultDetails()
                    if expectedresult in actualresult:
                        #Set the result status of execution
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Added table entry for 5Ghz deleted successfully :{details}")
                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to delete the table entry for 5Ghz: {details}")
                        print("[TEST EXECUTION RESULT] : %s" %actualresult)
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to add new rule for 5GHz.")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to get MAC address of WLAN client : {macAddress}.")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            obj.setLoadModuleStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file.")
            print("[TEST EXECUTION RESULT] : FAILURE")
        #Handle any post execution cleanup required
        print("\nPerforming the post wifi E2E execution cleanup.")
        tdkbE2EUtility.postExecutionCleanup()
        tdkutility.revert_ACLprerequisites_allRadios(obj,step)
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print("\nFailed to set ACL test prerequisites. Please check.")
        print("[TEST EXECUTION RESULT] : FAILURE")

    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    print("Failed to load tdkb_e2e and advancedconfig module.")
    obj.setLoadModuleStatus("FAILURE")
    print("Module loading failed.")