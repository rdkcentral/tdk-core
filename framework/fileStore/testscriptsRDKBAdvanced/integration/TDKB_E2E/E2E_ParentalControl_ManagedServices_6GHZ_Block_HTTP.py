##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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

##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
import tdkutility
import tdkbVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
obj1 = tdklib.TDKScriptingLibrary("advancedconfig","RDKB")
wifi_obj = tdklib.TDKScriptingLibrary("wifiagent","1")

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_6GHZ_Block_HTTP')
obj1.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_6GHZ_Block_HTTP')
wifi_obj.configureTestCase(ip,port,'E2E_ParentalControl_ManagedServices_6GHZ_Block_HTTP')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus1 =obj1.getLoadModuleResult()
loadmodulestatus2 = wifi_obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus1}")
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus2}")

if "SUCCESS" in loadmodulestatus.upper() and "SUCCESS" in loadmodulestatus1.upper() and "SUCCESS" in loadmodulestatus2.upper():
    obj.setLoadModuleStatus("SUCCESS")
    obj1.setLoadModuleStatus("SUCCESS")
    wifi_obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"
    exit_flag = 0
    sm_flag = 0
    step = 0

    #Parse the device configuration file
    step += 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Device configuration parsed successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_6ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.KeyPassphrase"
        managedServiceEnable = "Device.X_Comcast_com_ParentalControl.ManagedServices.Enable"
        securityMode = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"

        #Get the value of the wifi parameters that are currently set.
        paramList=[ssidName,keyPassPhrase,managedServiceEnable,securityMode]
        tdkTestObj,status,orgValue = tdkbE2EUtility.getMultipleParameterValues(obj,paramList)

        step += 1
        print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase,managedServiceEnable and securityMode")
        print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase,managedServiceEnable and securityMode")
        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: The values retrived: {orgValue}")
            print(f"[TEST EXECUTION RESULT] : SUCCESS")

            initial_secMode = orgValue[3]

            # Check and change Security Mode to WPA3-Personal if not already
            if initial_secMode != "WPA3-Personal":
                step += 1
                print(f"\nTEST STEP {step}: Get the initial security configuration")
                print(f"EXPECTED RESULT {step}: Should successfully get initial security configuration")
                initial_config = {}
                tdkTestObj, actualresult, initial_config = tdkutility.getSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Initial security configuration retrieved successfully")
                    print("TEST EXECUTION RESULT : SUCCESS")

                    # Set the security mode to WPA3-Personal
                    step += 1
                    print(f"\nTEST STEP {step}: Set security mode to WPA3-Personal")
                    print(f"EXPECTED RESULT {step}: Should set security mode to WPA3-Personal")
                    config_SET = {
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.SAEPassphrase": tdkbVariables.SAE_PASS,
                        f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.X_CISCO_COM_EncryptionMethod": tdkbVariables.ENCRYPTION_MODE
                    }
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, "WPA3-Personal", tdkbE2EUtility.ssid_6ghz_index, config_SET, initial_secMode)
                    details = tdkTestObj.getResultDetails()

                    if expectedresult in actualresult:
                        sm_flag = 1
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: Security mode changed to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : SUCCESS")

                        time.sleep(2)
                        # Validate the security mode with get
                        step += 1
                        print(f"\nTEST STEP {step}: Get the Security Mode and check it is changed to WPA3-Personal")
                        print(f"EXPECTED RESULT {step}: Should successfully set security mode to WPA3-Personal")
                        paramName = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_6ghz_index}.Security.ModeEnabled"
                        tdkTestObj,actualresult,sec_mode = tdkutility.wifi_GetParam(wifi_obj,paramName)

                        if expectedresult in actualresult and sec_mode == "WPA3-Personal":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Security Mode: {sec_mode}")
                            print("TEST EXECUTION RESULT : SUCCESS")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Get operation failed or security mode is not reflected in GET.")
                            print("TEST EXECUTION RESULT : FAILURE")
                            exit_flag = 1
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: Failed to set security mode to WPA3-Personal. Details: {details}")
                        print("TEST EXECUTION RESULT : FAILURE")
                        exit_flag = 1
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Failed to retrieve Initial security configuration")
                    print("TEST EXECUTION RESULT : FAILURE")
                    exit_flag = 1
            else:
                print(f"\nChanging Security mode not required as Current security mode is {initial_secMode}")

            if exit_flag != 1:
                # Set the SSID name, KeyPassphrase,managedServiceEnable"
                setValuesList = [tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,'true']
                print(f"Parameter values that are set: {setValuesList}")

                list1 = [ssidName,tdkbE2EUtility.ssid_6ghz_name,'string']
                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_6ghz_pwd,'string']
                list3 = [managedServiceEnable,'true','bool']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))

                setParamList1 = list3
                setParamList1 = "|".join(map(str, setParamList1))

                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
                tdkTestObj,actualresult1,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList1)

                step += 1
                print(f"\nTEST STEP {step}: Set the ssid,keypassphrase and managedServiceEnable")
                print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase and managedServiceEnable")
                if expectedresult in actualresult and expectedresult in actualresult1:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}:SET operation success.")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    newParamList=[ssidName,keyPassPhrase,managedServiceEnable]
                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)

                    step += 1
                    print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase and managedServiceEnable")
                    print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase and managedServiceEnable")
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: The parameter values after SET opetation: {newValues}")
                        print(f"[TEST EXECUTION RESULT] : SUCCESS")

                        # Adding a new row to BlockedService
                        tdkTestObj = obj1.createTestStep("AdvancedConfig_AddObject")
                        tdkTestObj.addParameter("paramName","Device.X_Comcast_com_ParentalControl.ManagedServices.Service.")
                        tdkTestObj.executeTestCase(expectedresult)
                        actualresult = tdkTestObj.getResult()
                        details = tdkTestObj.getResultDetails()

                        step += 1
                        print(f"\nTEST STEP {step}: Add new rule for service blocking")
                        print(f"EXPECTED RESULT {step}: Should add new rule")
                        if expectedresult in actualresult:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Added new rule. Details: {details}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            temp = details.split(':')
                            instance = temp[1]

                            if int(instance) > 0:
                                print(f"INSTANCE VALUE: {instance}")
                                #SET the parameters to block the HTTP Service
                                description = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.Description"
                                protocol = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.Protocol"
                                startport = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.StartPort"
                                endPort = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.EndPort"
                                alwaysBlock = f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.AlwaysBlock"

                                setValuesList = ['http','BOTH','80','8080','true']
                                print(f"Parameter values that are set: {setValuesList}")

                                list1 = [description,'http','string']
                                list2 = [protocol,'BOTH','string']
                                list3 = [startport,'80','unsignedInt']
                                list4 = [endPort,'8080','unsignedInt']
                                list5 = [alwaysBlock,'true','bool']

                                #Concatenate the lists with the elements separated by pipe
                                setParamList= list1 + list2 + list3 + list4 + list5
                                setParamList = "|".join(map(str, setParamList))

                                step += 1
                                print(f"\nTEST STEP {step}: Set all fields in added rule")
                                print(f"EXPECTED RESULT {step}: Should set all fields in added rule")

                                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,setParamList)
                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: SET operation successfull. Details: {details}")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #Retrieve the values after set and compare
                                    step +=1
                                    print(f"\nTEST STEP {step}: Get all fields of added rule")
                                    print(f"EXPECTED RESULT {step}: Should retrieve all fields of added rule and all the fields should update in GET")
                                    newParamList=[description,protocol,startport,endPort,alwaysBlock]
                                    tdkTestObj,status,newValues = tdkbE2EUtility.getMultipleParameterValues(obj,newParamList)
                                    if expectedresult in status and setValuesList == newValues:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Parameter values after SET: {newValues}")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #Wait for the changes to reflect
                                        time.sleep(60)
                                        #Connect to the wifi ssid from wlan client
                                        step += 1
                                        print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                                        print(f"EXPECTED RESULT {step}: Wlan client should connect to wifi successfully")
                                        status = tdkbE2EUtility.wlanConnectWifiSsid(tdkbE2EUtility.ssid_6ghz_name,tdkbE2EUtility.ssid_6ghz_pwd,tdkbE2EUtility.wlan_6ghz_interface)
                                        if expectedresult in status:
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step}: WLAN client connected successfully")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            #Get WLAN client IP after connecting
                                            step += 1
                                            print(f"\nTEST STEP {step}: Get the IP address of the wlan client after connecting to wifi")
                                            print(f"EXPECTED RESULT {step}: Should retrieve the wlan client IP")
                                            wlanIP = tdkbE2EUtility.getWlanIPAddress(tdkbE2EUtility.wlan_6ghz_interface)
                                            if wlanIP:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                print(f"ACTUAL RESULT {step}: {wlanIP}")
                                                print("[TEST EXECUTION RESULT] : SUCCESS")

                                                # Get the current LAN IP address DHCP range
                                                step += 1
                                                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                                                print(f"EXPECTED RESULT {step}: Should retrieve LAN IP range")
                                                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                                tdkTestObj,status,curIPAddress = tdkbE2EUtility.getParameterValue(obj,param)

                                                if expectedresult in status and curIPAddress:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step}: {curIPAddress}")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                    # Check whether wlan ip address is in same DHCP range
                                                    step += 1
                                                    print(f"\nTEST STEP {step}: Check whether wlan ip address is in same DHCP range")
                                                    print(f"EXPECTED RESULT {step}: wlan IP should be in LAN DHCP range")
                                                    status = tdkbE2EUtility.checkIpRange(curIPAddress,wlanIP)
                                                    if expectedresult in status:
                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                        print(f"ACTUAL RESULT {step}: wlan ip address {wlanIP} is in same DHCP range {curIPAddress}")
                                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                                        #set new static route to wan client
                                                        step += 1
                                                        print(f"\nTEST STEP {step}: Add static route to reach WAN from WLAN client")
                                                        print(f"EXPECTED RESULT {step}: Should add static route successfully")
                                                        status = tdkbE2EUtility.addStaticRoute(tdkbE2EUtility.wan_https_ip, curIPAddress,tdkbE2EUtility.wlan_6ghz_interface)
                                                        if expectedresult in status:
                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                            print(f"ACTUAL RESULT {step}: Static route added successfully")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                                            #Check HTTP connectivity from WLAN to WAN
                                                            step += 1
                                                            print(f"\nTEST STEP {step}:Check the Http connectivity from WLAN to WAN")
                                                            print(f"EXPECTED RESULT {step}: Http connection should be blocked")
                                                            status = tdkbE2EUtility.wgetToWAN("WGET_HTTP", wlanIP, curIPAddress)

                                                            if expectedresult not in status:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print("ACTUAL RESULT: Http connection from WLAN to WAN is blocked")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                print("ACTUAL RESULT: Http connection from WLAN to WAN is success")
                                                                print("[TEST EXECUTION RESULT] : FAILURE")

                                                            #delete the added route
                                                            step += 1
                                                            print(f"\nTEST STEP {step}: Delete the static route")
                                                            print(f"EXPECTED RESULT {step}: Should delete the static route")
                                                            status = tdkbE2EUtility.delStaticRoute(tdkbE2EUtility.wan_https_ip, curIPAddress,tdkbE2EUtility.wlan_6ghz_interface)
                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print("ACTUAL RESULT: Static route deleted successfully")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                print("ACTUAL RESULT: Failed to delete the static route")
                                                                print("[TEST EXECUTION RESULT] : FAILURE")

                                                            #Disconnect wifi client
                                                            step += 1
                                                            print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                                                            print(f"EXPECTED RESULT {step}: WLAN client should disconnect from SSID")
                                                            status = tdkbE2EUtility.wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_6ghz_interface)
                                                            if expectedresult in status:
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: SUCCESS")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                print(f"ACTUAL RESULT {step}: Disconnect from WIFI SSID: FAILED")
                                                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            print(f"ACTUAL RESULT {step}:Static route add failed")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        print(f"ACTUAL RESULT {step}: wlan ip address is not in same DHCP range")
                                                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step}: Failed to get the current LAN IP address DHCP range")
                                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step}: Failed to get the wlan address")
                                                print(f"[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step}: Failed to connect to wlan client")
                                            print(f"[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: Failed to retrieve all fields of added rule or parameter are not reflected in GET")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: SET operation failed. Details: {details}")
                                    print("[TEST EXECUTION RESULT] : FAILURE")

                                # Delete the created table entry
                                tdkTestObj = obj1.createTestStep("AdvancedConfig_DelObject")
                                tdkTestObj.addParameter("paramName", f"Device.X_Comcast_com_ParentalControl.ManagedServices.Service.{instance}.")
                                tdkTestObj.executeTestCase(expectedresult)
                                actualresult = tdkTestObj.getResult()
                                details = tdkTestObj.getResultDetails()

                                step += 1
                                print(f"\nTEST STEP {step}: Delete the added rule")
                                print(f"EXPECTED RESULT {step}: Should delete the added rule")

                                if expectedresult in actualresult:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: Details: {details}")
                                    print(f"TEST EXECUTION RESULT : SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: Details: {details}")
                                    print(f"TEST EXECUTION RESULT : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"Invalid instance returned : {instance}")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: Failed to add new rule. Details: {details}")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: GET operation failed or the parameter values are not updated after SET")
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: SET operation failed")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")

                #Revert operation for security mode
                if sm_flag == 1:
                    print("Reverting to initial Security Mode...")
                    step += 1
                    tdkTestObj, actualresult = tdkutility.setSecurityModeEnabledConfig(wifi_obj, initial_secMode, tdkbE2EUtility.ssid_6ghz_index, initial_config, sec_mode)
                    details = tdkTestObj.getResultDetails()

                    print(f"\nTEST STEP {step} : Revert Security Mode to initial security mode : {initial_secMode}")
                    print(f"EXPECTED RESULT {step} : Reverting to initial security mode should be success")

                    if expectedresult in actualresult:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was successful Details : {details}")
                        print("TEST EXECUTION RESULT : SUCCESS")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step} : Reverting Mode to initial value was NOT successful Details : {details}")
                        print("TEST EXECUTION RESULT : FAILURE")
                else:
                    print("\nReverting Security Mode not required...")

                #Prepare the list of parameter values to be reverted
                list1 = [ssidName,orgValue[0],'string']
                list2 = [keyPassPhrase,orgValue[1],'string']

                list3 = [managedServiceEnable,orgValue[2],'bool']

                #Concatenate the lists with the elements separated by pipe
                if sm_flag == 1:
                    revertParamList = list1
                else:
                    revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                revertParamList1 = list3
                revertParamList1 = "|".join(map(str, revertParamList1))

                #Revert the values to original
                tdkTestObj,actualresult,details = tdkbE2EUtility.setMultipleParameterValues(obj,revertParamList)
                tdkTestObj,actualresult1,details = tdkbE2EUtility.setMultipleParameterValues(obj,revertParamList1)

                step += 1
                print(f"\nTEST STEP {step}: Revert wifi parameters to original values")
                print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase and managedServiceEnable")
                if expectedresult in actualresult and expectedresult in actualresult1:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Revert operation success. Details:{details}")
                    print(f"[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: Revert operation failed. Details: {details}")
                    print(f"[TEST EXECUTION RESULT] : FAILURE")
            else:
                print("Not proceeding further due to security mode change failure")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to retrive the values")
            print(f"[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    tdkbE2EUtility.postExecutionCleanup()
    obj.unloadModule("tdkb_e2e")
    obj1.unloadModule("advancedconfig")
    wifi_obj.unloadModule("wifiagent")
else:
    print(f"ACTUAL RESULT: Failed to load tdkb_e2e/advancedconfig/wifiagent module")
    obj.setLoadModuleStatus("FAILURE")
    obj1.setLoadModuleStatus("FAILURE")
    wifi_obj.setLoadModuleStatus("FAILURE")
    print(f"ACTUAL RESULT: Module loading failed")
