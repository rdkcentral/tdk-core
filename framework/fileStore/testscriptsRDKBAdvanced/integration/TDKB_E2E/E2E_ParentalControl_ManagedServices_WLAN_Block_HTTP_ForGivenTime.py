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
from datetime import datetime
import calendar

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_WLAN_Block_HTTP_ForGivenTime')
obj1.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_WLAN_Block_HTTP_ForGivenTime')

#Get the result of connection with test component
loadmodulestatus = obj.getLoadModuleResult()
loadmodulestatus1 = obj1.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus)
print("[LIB LOAD STATUS]  :  %s" % loadmodulestatus1)

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    finalStatus = "FAILURE"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        print("Parsed the device configuration file successfully")

        step = 1
        status = "SUCCESS"

        #Assign the WIFI parameters names to a variable
        ssidName = "Device.WiFi.SSID.%s.SSID" % tdkbE2EUtility.ssid_2ghz_index
        keyPassPhrase = "Device.WiFi.AccessPoint.%s.Security.KeyPassphrase" % tdkbE2EUtility.ssid_2ghz_index
        managedServiceEnable = "Device.X_Comcast_com_ParentalControl.ManagedServices.Enable"

        #Get the value of the wifi parameters that are currently set.
        paramList = [ssidName, keyPassPhrase, managedServiceEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj, paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and managedServiceEnable")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and managedServiceEnable")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            if tdkbE2EUtility.mlo_capability == "False":
                # Set the SSID name,password and managedServiceEnable
                step = step + 1
                setValuesList = [tdkbE2EUtility.ssid_2ghz_name, tdkbE2EUtility.ssid_2ghz_pwd, 'true']
                print("Parameter values that are set: %s" % setValuesList)

                list1 = [ssidName, tdkbE2EUtility.ssid_2ghz_name, 'string']
                list2 = [keyPassPhrase, tdkbE2EUtility.ssid_2ghz_pwd, 'string']
                list3 = [managedServiceEnable, 'true', 'bool']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))
                managedServiceEnableStatus = "|".join(map(str, list3))

                tdkTestObj,actualresult,details = setMultipleParameterValues(obj, setParamList)
                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj, managedServiceEnableStatus)

                if expectedresult in actualresult and expectedresult in actualresult1:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase and managedServiceEnable")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase and managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    step = step + 1
                    newParamList = [ssidName, keyPassPhrase, managedServiceEnable]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and managedServiceEnable")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and managedServiceEnable")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and managedServiceEnable")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and managedServiceEnable")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                        status = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"\nTEST STEP {step}: Set the ssid,keypassphrase and managedServiceEnable")
                    print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase and managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    status = "FAILURE"

                # Assign global values
                tdkbE2EUtility.ssid_name = tdkbE2EUtility.ssid_2ghz_name
                tdkbE2EUtility.ssid_pwd = tdkbE2EUtility.ssid_2ghz_pwd
                tdkbE2EUtility.wlan_interface = tdkbE2EUtility.wlan_2ghz_interface
            else:
                # MLO=True: Set managedServiceEnable only
                step = step + 1
                setValuesList = ['true']
                print("Parameter values that are set: %s" % setValuesList)

                list1 = [managedServiceEnable, 'true', 'bool']

                #Concatenate the list with the elements separated by pipe
                setParamList = "|".join(map(str, list1))

                tdkTestObj,actualresult,details = setMultipleParameterValues(obj, setParamList)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the managedServiceEnable")
                    print(f"EXPECTED RESULT {step}: Should set the managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    step = step + 1
                    newParamList = [managedServiceEnable]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj, newParamList)

                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current managedServiceEnable")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current managedServiceEnable")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Get the current managedServiceEnable")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current managedServiceEnable")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                        status = "FAILURE"
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"\nTEST STEP {step}: Set the managedServiceEnable")
                    print(f"EXPECTED RESULT {step}: Should set the managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    status = "FAILURE"

            if status == "SUCCESS":
                #Get the current UTC Time
                utcTime = datetime.utcnow()
                start_Time = utcTime.strftime('%H:%M')
                print("current UTC time is : %s" % utcTime)
                start = start_Time.split(":")
                start_Time = str(int(start[0])) + ":00"
                end_Time = str(int(start[0]) + 3) + ":15"
                day = calendar.day_name[utcTime.weekday()]
                day = day[:3]
                print("Start time is : %s, End time is : %s, day is : %s" % (start_Time, end_Time, day))

                # Adding a new row to BlockedService
                tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedServices.Service.")
                tdkTestObj.executeTestCase(expectedresult)
                actualresult = tdkTestObj.getResult()
                details = tdkTestObj.getResultDetails()

                step = step + 1
                print(f"\nTEST STEP {step}: Adding new rule for service blocking")
                print(f"EXPECTED RESULT {step}: Should add new rule")
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Added new rule. Details: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    temp = details.split(':')
                    instance = temp[1]

                    if int(instance) > 0:
                        print(f"INSTANCE VALUE: {instance}")
                        description = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.Description"
                        protocol = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.Protocol"
                        startport = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.StartPort"
                        endPort = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.EndPort"
                        alwaysBlock = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.AlwaysBlock"
                        startTime = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.StartTime"
                        endTime = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.EndTime"
                        blockdays = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.BlockDays"

                        setValuesList = ['http', 'BOTH', '80', '8080', 'false', start_Time, end_Time, day]
                        print("Parameter values that are set: %s" % setValuesList)

                        list1 = [description, 'http', 'string']
                        list2 = [protocol, 'BOTH', 'string']
                        list3 = [startport, '80', 'unsignedInt']
                        list4 = [endPort, '8080', 'unsignedInt']
                        list5 = [alwaysBlock, 'false', 'bool']
                        list6 = [startTime, start_Time, 'string']
                        list7 = [endTime, end_Time, 'string']
                        list8 = [blockdays, day, 'string']

                        #Concatenate the lists with the elements separated by pipe
                        setParamList = list1 + list2 + list3 + list4 + list5 + list6 + list7 + list8
                        setParamList = "|".join(map(str, setParamList))

                        tdkTestObj,actualresult,details = setMultipleParameterValues(obj, setParamList)

                        step = step + 1
                        print(f"\nTEST STEP {step}: Set all fields in added rule")
                        print(f"EXPECTED RESULT {step}: Should set all fields in added rule")
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: {details}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Retrieve the values after set and compare
                            newParamList = [description, protocol, startport, endPort, alwaysBlock, startTime, endTime, blockdays]
                            tdkTestObj,status,newValues = getMultipleParameterValues(obj, newParamList)

                            step = step + 1
                            print(f"\nTEST STEP {step}: Get all fields of added rule")
                            print(f"EXPECTED RESULT {step}: Should retrieve all fields of added rule")
                            if expectedresult in status and setValuesList == newValues:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: {newValues}")
                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                #Wait for the changes to reflect in client device
                                time.sleep(60)

                                #Connect to the wifi ssid from wlan client
                                step = step + 1
                                print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                                print(f"EXPECTED RESULT {step}: WLAN client should connect to wifi successfully")
                                status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_name, tdkbE2EUtility.ssid_pwd, tdkbE2EUtility.wlan_interface)

                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    step = step + 1
                                    print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                                    print(f"EXPECTED RESULT {step}: Should retrieve the WLAN client IP")
                                    wlanIP = getWlanIPAddress(tdkbE2EUtility.wlan_interface)

                                    if wlanIP:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: WLAN IP: {wlanIP}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        step = step + 1
                                        print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                                        print(f"EXPECTED RESULT {step}: Should retrieve the LAN IP address")
                                        param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                        tdkTestObj,status,curIPAddress = getParameterValue(obj, param)

                                        if expectedresult in status and curIPAddress:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: LAN IP Address: {curIPAddress}")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            step = step + 1
                                            print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                            print(f"EXPECTED RESULT {step}: WLAN IP should be in LAN DHCP range")
                                            status = checkIpRange(curIPAddress, wlanIP)

                                            if expectedresult in status:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: WLAN IP address is in same DHCP range")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                #Refresh wifi network before adding static route
                                                wlanIsSSIDAvailable(tdkbE2EUtility.ssid_name)

                                                step = step + 1
                                                print(f"\nTEST STEP {step}: Add static route to reach HTTP WAN client from WLAN client")
                                                print(f"EXPECTED RESULT {step}: Static route should be added successfully")
                                                status = addStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.wlan_interface)

                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: Static route added successfully")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                    step = step + 1
                                                    print(f"\nTEST STEP {step}: Check the HTTP connectivity from WLAN to WAN")
                                                    print(f"EXPECTED RESULT {step}: Blocked service HTTP should not be reachable during configured time")
                                                    status = wgetToWAN("WGET_HTTP", wlanIP, curIPAddress)

                                                    if expectedresult not in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: The blocked service 'HTTP' cannot be reached")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")
                                                        finalStatus = "SUCCESS"
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: The blocked service 'HTTP' can be reached")
                                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: Static route add failed")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                                #delete the added route
                                                step = step + 1
                                                print(f"\nTEST STEP {step}: Delete the static route")
                                                print(f"EXPECTED RESULT {step}: Static route should be deleted successfully")
                                                status = delStaticRoute(tdkbE2EUtility.wan_http_ip, curIPAddress, tdkbE2EUtility.wlan_interface)

                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: Static route deleted successfully")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: Static route delete failed")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                                step = step + 1
                                                print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                                print(f"EXPECTED RESULT {step}: WLAN client should disconnect from SSID")
                                                status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_interface)

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
                                                print(f"ACTUAL RESULT {step}: WLAN Client IP address is not in the same Gateway DHCP range")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to get the Gateway IP address")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Failed to get the WLAN Client IP address")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Failed to connect to WIFI SSID")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: GET operation failed or values mismatch: {newValues}")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                            print("[TEST EXECUTION RESULT] : FAILURE")

                        #Delete the created table entry
                        tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                        tdkTestObj.addParameter("paramName", f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.")
                        expectedresult = "SUCCESS"
                        tdkTestObj.executeTestCase(expectedresult)
                        actualresult = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()

                        step = step + 1
                        print(f"\nTEST STEP {step}: Deleting the added service blocking rule")
                        print(f"EXPECTED RESULT {step}: Should delete the added rule")

                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Added rule deleted successfully. Details: {details}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Added rule could not be deleted. Details: {details}")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Table add returned invalid instance")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to add new service blocking rule. Details: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")

            #Revert the values to original
            if tdkbE2EUtility.mlo_capability == "False":
                #Prepare the list of parameter values to be reverted
                list1 = [ssidName, orgValue[0], 'string']
                list2 = [keyPassPhrase, orgValue[1], 'string']
                list3 = [managedServiceEnable, orgValue[2], 'bool']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))
                managedServiceEnableStatus = "|".join(map(str, list3))

                #Revert the values to original
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj, revertParamList)
                tdkTestObj,actualresult1,details = setMultipleParameterValues(obj, managedServiceEnableStatus)

                step = step + 1
                print(f"\nTEST STEP {step}: Revert the values to original")
                if expectedresult in actualresult and expectedresult in actualresult1 and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase and managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase and managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                #MLO=True: Revert managedServiceEnable only
                list1 = [managedServiceEnable, orgValue[2], 'bool']

                #Concatenate the list with the elements separated by pipe
                revertParamList = "|".join(map(str, list1))

                #Revert the value to original
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj, revertParamList)

                step = step + 1
                print(f"\nTEST STEP {step}: Revert the values to original")
                if expectedresult in actualresult and expectedresult in finalStatus:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"EXPECTED RESULT {step}: Should set the original managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"EXPECTED RESULT {step}: Should set the original managedServiceEnable")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"TEST STEP {step}: Get the current ssid,keypassphrase and managedServiceEnable")
            print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and managedServiceEnable")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print("Failed to parse the device configuration file")

    #Handle any post execution cleanup required
    postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
else:
    print("Failed to load the module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")
    print("Module loading failed")