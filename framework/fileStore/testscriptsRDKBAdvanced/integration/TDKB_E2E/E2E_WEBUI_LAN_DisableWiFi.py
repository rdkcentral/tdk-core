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
import tdkbWEBUIUtility
from tdkbWEBUIUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_WEBUI_LAN_DisableWiFi')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print(f"[LIB LOAD STATUS]  :  {loadmodulestatus}")

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

        # Check if the device is MLO capable and get the SSID name accordingly
        if tdkbE2EUtility.mlo_capability == "True":
            ssidName = tdkbE2EUtility.ssid_name
        else:
            ssidName = tdkbE2EUtility.ssid_2ghz_name

        wifiEnable = "Device.WiFi.SSID.%s.Enable" %tdkbE2EUtility.ssid_2ghz_index
        #Get the value of the wifi parameters that are currently set.
        paramList=[wifiEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status and orgValue != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"\nTEST STEP {step}: Get the current wifienable status")
            print(f"EXPECTED RESULT {step}: Should retrieve the current wifienable status")
            print(f"ACTUAL RESULT {step}: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            if orgValue[0] == "false":
                step += 1
                setValuesList = ['true']
                print(f"WIFI parameter values that are set: {setValuesList}")
                setParamList = "%s|true|bool" %(wifiEnable)
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"\nTEST STEP {step}: Set the wifi enable status to true")
                    print(f"EXPECTED RESULT {step}: Should set the wifi enable status to true")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    #Retrieve the values after set and compare
                    newParamList=[wifiEnable]
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)

                    step += 1
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"\nTEST STEP {step}: Get the current wifi enable status")
                        print(f"EXPECTED RESULT {step}: Should retrieve the current wifi enable status")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Wait for the changes to reflect in client device
                        time.sleep(60)
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"\nTEST STEP {step}: Failed to set the wifi enable status to true")
                        print(f"EXPECTED RESULT {step}: Should retrieve the wifi enable status as true")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                        obj.unloadModule("tdkb_e2e")
                        exit()

            #Connect to LAN client and obtain its IP
            step += 1
            print(f"\nTEST STEP {step}: Get the IP address of the lan client after connecting to it")
            lanIP = getLanIPAddress(tdkbE2EUtility.lan_interface)
            if lanIP != "":
                tdkTestObj.setResultStatus("SUCCESS")
                step += 1
                print(f"\nTEST STEP {step}: Get the current LAN IP address DHCP range")
                param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                print(f"LAN IP Address: {curIPAddress}")

                if expectedresult in status and curIPAddress != "":
                    tdkTestObj.setResultStatus("SUCCESS")
                    step += 1
                    print(f"\nTEST STEP {step}: Check whether lan ip address is in same DHCP range")
                    status = "SUCCESS"
                    status = checkIpRange(curIPAddress,lanIP)
                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        #Set Selenium grid
                        driver,status = startSeleniumGrid(tdkTestObj,"LAN",tdkbE2EUtility.grid_url)
                        if status == "SUCCESS":
                            try:
                                time.sleep(10)
                                #To click on option "Connection" in UI
                                driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/a').click()
                                #To click on WiFi option under connection
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/ul/li[1]/ul/li[2]/ul/li[4]/a").click()
                                time.sleep(10)
                                # To click on edit option for 2.4GHz wifi
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/table/tbody/tr[2]/td[5]/a").click()
                                # To Disable 2.4Ghz WiFi
                                driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[3]/div[2]/form/div[1]/span[2]/ul/a[2]/li/label").click()
                                #To save the settings
                                driver.find_element_by_id("save_settings").submit()
                                time.sleep(60)
                                driver.quit()

                                #Check if 2.4GHz wifi broadcasting is stopped to validate the disabling of wifi
                                step += 1
                                print(f"\nTEST STEP {step}: Check if the SSID name is listed in wifi client")
                                time.sleep(30)
                                status = wlanIsSSIDAvailable(ssidName)
                                if expectedresult not in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"Network name {ssidName} is not broadcasted on the network")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"Network name {ssidName} is broadcasted on the network")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            except Exception as error:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(error)
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("Failed to set selenium grid")
                        #Kill selenium hub and node
                        status = tdkbWEBUIUtility.kill_hub_node("LAN")
                        if status == "SUCCESS":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("Post-requisite success")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("Couldnt kill node and hub")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("checkIpRange:lan ip address is not in DHCP range")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("getParameterValue : Failed to get gateway lan ip")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("getLanIPAddress:Failed to get the LAN client IP")

            #Prepare the list of parameter values to be reverted
            revertParamList = "%s|%s|bool" %(wifiEnable,orgValue[0])

            #Revert the values to original
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
            step += 1
            print(f"\nTEST STEP {step}: Revert the wifi enable status to original")
            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"EXPECTED RESULT {step}: Should set the original wifi enable status")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"EXPECTED RESULT {step}: Should set the original wifi enable status")
                print(f"ACTUAL RESULT {step}: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"\nTEST STEP {step}: Get the current wifi enable status")
            print(f"EXPECTED RESULT {step}: Should retrieve the current wifi enable status")
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