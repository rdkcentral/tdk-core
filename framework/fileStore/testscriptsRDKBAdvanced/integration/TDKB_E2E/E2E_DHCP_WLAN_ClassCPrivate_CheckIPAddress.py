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
obj.configureTestCase(ip,port,'E2E_DHCP_WLAN_ClassCPrivate_CheckIPAddress')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        step = 1
        status = "SUCCESS"

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" %tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" %tdkbE2EUtility.ssid_2ghz_index
        lanIPAddress = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
        lanSubnetMask = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanSubnetMask"
        minAddress = "Device.DHCPv4.Server.Pool.1.MinAddress"
        maxAddress = "Device.DHCPv4.Server.Pool.1.MaxAddress"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,lanIPAddress,lanSubnetMask,minAddress,maxAddress]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            if tdkbE2EUtility.mlo_capability == "False":
                # Set the SSID name,password,lanIPAddress,lanSubnetMask,minAddress and maxAddress
                step = step + 1
                setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'192.168.0.1','255.255.255.0','192.168.0.2','192.168.0.253']
                print("Parameter values that are set: %s" %setValuesList)

                list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']

                list3 = [lanIPAddress,'192.168.0.1','string']
                list4 = [lanSubnetMask,'255.255.255.0','string']
                list5 = [minAddress,'192.168.0.2','string']
                list6 = [maxAddress,'192.168.0.253','string']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))
                setParamList1= list3 + list4 + list5 + list6
                setParamList1 = "|".join(map(str, setParamList1))

                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,setParamList1)
                if expectedresult in actualresult and expectedresult in actualresult1:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    step = step + 1
                    newParamList=[ssidName,keyPassPhrase,lanIPAddress,lanSubnetMask,minAddress,maxAddress]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Wait for the changes to reflect in client device
                        time.sleep(60)
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                        status = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    status = "FAILURE"

                # Assign global values
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface
            else:
                #Set the Lan IP Address, Lan Subnet Mask, Min and Max address
                step = step + 1
                setList = ['192.168.0.1','255.255.255.0','192.168.0.2','192.168.0.253']
                status, step, newValues = lanManagementSet(obj,setList,step,revert="false")

            if status == "SUCCESS":
                #Connect to the wifi ssid from wlan client
                step = step + 1
                print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name,tdkbE2EUtility.ssid_pwd,tdkbE2EUtility.wlan_interface)
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("wlanConnectWifiSsid: SUCCESS")

                    step = step + 1
                    print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                    wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)
                    if wlanIP:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("getWlanIPAddress: SUCCESS")

                        step = step + 1
                        print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                        opstatus = "SUCCESS"
                        LanIP = newValues[0]
                        opstatus = checkIpRange(LanIP,wlanIP)
                        if expectedresult in opstatus:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("checkIpRange: SUCCESS")

                            step = step + 1
                            print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                            status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface)
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                finalStatus = "SUCCESS"
                                print("Disconnect from WIFI SSID: SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"\nTEST STEP {step}:Disconnect from WIFI SSID: FAILED")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"\nTEST STEP {step}:WLAN Client IP address is not in the same Gateway DHCP range")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}:Failed to get the WLAN Client IP address")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"\nTEST STEP {step}:Failed to connect to WIFI SSID")

            if tdkbE2EUtility.mlo_capability == "False":
                #Prepare the list of parameter values to be reverted
                list1 = [ssidName,orgValue[0],'string']
                list2 = [keyPassPhrase,orgValue[1],'string']

                list3 = [lanIPAddress,orgValue[2],'string']
                list4 = [lanSubnetMask,orgValue[3],'string']
                list5 = [minAddress,orgValue[4],'string']
                list6 = [maxAddress,orgValue[5],'string']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                revertParamList1 = list3 + list4 + list5 + list6
                revertParamList1 = "|".join(map(str, revertParamList1))

                #Revert the values to original
                step = step + 1
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj,revertParamList1)
                print(f"\nTEST STEP {step}: Revert the values to original")
                if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                #Revert the Lan IP Address, Lan Subnet Mask, Min and Max address
                step = step + 1
                setList = [orgValue[2], orgValue[3], orgValue[4], orgValue[5]]
                _, _, _ = lanManagementSet(obj,setList,step,revert="true")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"TEST STEP {step}: Get the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,lanIPAddress,lanSubnetMask,minAddress and maxAddress")
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
