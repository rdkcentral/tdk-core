# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")
sysobj = tdklib.TDKScriptingLibrary("sysutil","RDKB")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_Stability_2.4GHz_WLANClientToServer_UDPDownlink_ThroughputMeasurement')
sysobj.configureTestCase(ip,port,'E2E_Stability_2.4GHz_WLANClientToServer_UDPDownlink_ThroughputMeasurement')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
loadmodulestatus_sys =sysobj.getLoadModuleResult()

expectedresult = "SUCCESS"

if expectedresult in loadmodulestatus.upper() and expectedresult in loadmodulestatus_sys.upper():
    obj.setLoadModuleStatus("SUCCESS")
    sysobj.setLoadModuleStatus("SUCCESS")

    status = "FAILURE"
    wifi_band = "2.4GHz"

    #Parse the device configuration file
    step = 1
    print(f"\nTEST STEP {step}: Parse the device configuration file")
    print(f"EXPECTED RESULT {step}: Should parse the device configuration file successfully")
    status = tdkbE2EUtility.parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Device configuration parsed successfully")
        print(f"[TEST EXECUTION RESULT] : SUCCESS")

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_2ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_2ghz_index}.Security.KeyPassphrase"
        radioEnable = f"Device.WiFi.Radio.{tdkbE2EUtility.radio_2ghz_index}.Enable"

        #Get the value of the wifi parameters that are currently set.
        step += 1
        print(f"\nTEST STEP {step}: Get the current {wifi_band} ssid,keypassphrase,Radio enable status")
        print(f"EXPECTED RESULT {step}: Should retrieve the current {wifi_band} ssid,keypassphrase,Radio enable status")

        paramList=[ssidName,keyPassPhrase,radioEnable]
        tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

        if expectedresult in status:
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Values retrieved: {orgValue}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Set the SSID name, KeyPassphrase, Radio enable
            step += 1
            print(f"\nTEST STEP {step}: Set the {wifi_band} ssid, keypassphrase, radio enable")
            print(f"EXPECTED RESULT {step}: Should set the {wifi_band} ssid, keypassphrase, radio enable successfully")
            setValuesList = [tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,'true']
            print(f"Parameter values that are set: {setValuesList}")
            list1 = [ssidName,tdkbE2EUtility.ssid_2ghz_name,'string']
            list2 = [keyPassPhrase,tdkbE2EUtility.ssid_2ghz_pwd,'string']
            list3 = [radioEnable,'true','bool']

            #Concatenate the lists with the elements separated by pipe
            setParamList = list1 + list2 + list3
            setParamList = "|".join(map(str, setParamList))
            tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)

            if expectedresult in actualresult:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Details: {details}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Retrieve the values after set and compare
                step += 1
                print(f"\nTEST STEP {step}: Get the current {wifi_band} ssid, keypassphrase, radio enable")
                print(f"EXPECTED RESULT {step}: Should retrieve the current {wifi_band} ssid, keypassphrase, radio enable")
                tdkTestObj,status,newValues = getMultipleParameterValues(obj, paramList)

                if expectedresult in status and setValuesList == newValues:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: GET values:  {newValues}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Wait for the changes to reflect in client device
                    time.sleep(60)

                    #Connect the first wlan client to the WiFi SSID
                    step += 1
                    print(f"\nTEST STEP {step}: Connect the first wlan client to the {wifi_band} WiFi SSID")
                    print(f"EXPECTED RESULT {step}: The first wlan client should be successfully connected to the {wifi_band} WiFi SSID")
                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan_2ghz_interface)

                    if expectedresult in status:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: The first wlan client successfully connected to the {wifi_band} WiFi SSID")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Get the WLAN IP address of connected client
                        step += 1
                        print(f"\nTEST STEP {step}: Get the WLAN IP address of the first wlan client connected.")
                        print(f"EXPECTED RESULT {step}: The current WLAN IP address of the first wlan client should be obtained")
                        wlanInterfaceIP = getWlanIPAddress(tdkbE2EUtility.wlan_2ghz_interface)

                        if wlanInterfaceIP != "":
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step} : Current WLAN IP address is obtained as {wlanInterfaceIP}")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            #Check if the current Wlan IP is in the DHCP range
                            step += 1
                            curIPAddress = ""
                            print(f"\nTEST STEP {step}: Check if the current WLAN IP address of the first wlan client is in DHCP range")
                            print(f"EXPECTED RESULT {step}: The current WLAN IP address of the first wlan client should be in DHCP range")
                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                            print(f"WLAN IP Address: {curIPAddress}")

                            if expectedresult in status and curIPAddress:
                                tdkTestObj.setResultStatus("SUCCESS")
                                status = checkIpRange(curIPAddress,wlanInterfaceIP)

                                if expectedresult in status:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step} : Current WLAN IP address of the first wlan client is in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                    #Connect the second wlan client to the WiFi SSID
                                    step += 1
                                    print(f"\nTEST STEP {step}: Connect the second wlan client to the {wifi_band} WiFi SSID")
                                    print(f"EXPECTED RESULT {step}: The second wlan client should be successfully connected to the {wifi_band} WiFi SSID")
                                    status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_2ghz_name,tdkbE2EUtility.ssid_2ghz_pwd,tdkbE2EUtility.wlan2_2ghz_interface,clientType = "WLAN_2")

                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        client2_status = "CONNECTED"
                                        print(f"ACTUAL RESULT {step}: The second wlan client successfully connected to the {wifi_band} WiFi SSID")
                                        print("[TEST EXECUTION RESULT] : SUCCESS")

                                        #Get the WLAN IP address of connected client
                                        step += 1
                                        print(f"\nTEST STEP {step}: Get the WLAN IP address of the second wlan client connected.")
                                        print(f"EXPECTED RESULT {step}: The current WLAN IP address of the second wlan client should be obtained")
                                        wlan2_InterfaceIP = getWlanIPAddress(tdkbE2EUtility.wlan2_2ghz_interface)

                                        if wlan2_InterfaceIP != "":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print(f"ACTUAL RESULT {step} : Current WLAN IP address is obtained as {wlan2_InterfaceIP}")
                                            print("[TEST EXECUTION RESULT] : SUCCESS")

                                            #Check if the current Wlan IP is in the DHCP range
                                            step += 1
                                            print(f"\nTEST STEP {step}: Check if the current WLAN IP address of the second wlan client is in DHCP range")
                                            print(f"EXPECTED RESULT {step}: The current WLAN IP address of the second wlan client should be in DHCP range")
                                            param = "Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress"
                                            tdkTestObj,status,curIPAddress = getParameterValue(obj,param)
                                            print(f"WLAN IP Address: {curIPAddress}")

                                            if expectedresult in status and curIPAddress:
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                status = checkIpRange(curIPAddress,wlan2_InterfaceIP)

                                                if expectedresult in status:
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    print(f"ACTUAL RESULT {step} : Current WLAN IP address of the second wlan client is in same DHCP range")
                                                    print("[TEST EXECUTION RESULT] : SUCCESS")

                                                    #Wait for 60s for the connection to stabilize before throughput measurement
                                                    time.sleep(60)

                                                    # Determine the operating standard of the wifi connection and set the Operating Standard in DUT
                                                    step += 1
                                                    #For 802.11n, the operating standard is set as 'n'.
                                                    operating_standard = 'n'
                                                    print(f"Setting the Operating Standard in DUT to the current Operating Standard of the wifi connection")
                                                    set_flag, initial_operating_std, final_operating_std, step = setOperatingStandard(obj, tdkbE2EUtility.ssid_2ghz_name, wifi_band, operating_standard, step)

                                                    if set_flag:
                                                        print(f"Operating Standard set successfully in DUT and verified. Initial Operating Standard: {initial_operating_std} and Final Operating Standard: {final_operating_std}")
                                                        #Measure the UDP downlink throughput from server to first wlan client and toggle the wifi connection of second wlan client during each iteration for 4 hours and validate the throughput
                                                        step += 1
                                                        duration = 900
                                                        bitrate = "50M"
                                                        iter_count = 16 
                                                        dut_server_log_file = "/rdklogs/udp_downlink_iperf3.log"
                                                        print(f"Measuring the UDP downlink throughput from server to first wlan client and toggling the wifi connection of second wlan client during each iteration for 4 hours with a time interval of 15 minutes.")
                                                        downlink_flag, step = downlinkUDPThroughputTest(sysobj, step, wlanInterfaceIP, duration, bitrate, iter_count, dut_server_log_file, client2_status, tdkbE2EUtility.wlan2_2ghz_interface, client2_ssid = tdkbE2EUtility.ssid_2ghz_name, client2_password = tdkbE2EUtility.ssid_2ghz_pwd)
                                                        if downlink_flag:
                                                            print(f"UDP downlink throughput test successful for 4 hours with toggling the wifi connection of second wlan client during each iteration")
                                                            print("[TEST EXECUTION RESULT] : SUCCESS")
                                                        else:
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            print(f"ACTUAL RESULT {step} : UDP downlink throughput test failed")
                                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                                        #Revert the Operating Standard to initial value if it was changed
                                                        step += 1
                                                        if initial_operating_std != final_operating_std:
                                                            print(f"Reverting the Operating Standard in DUT to initial Operating Standard: {initial_operating_std}")
                                                            set_flag, initial_op_std, final_op_std, step = setOperatingStandard(obj, tdkbE2EUtility.ssid_2ghz_name, wifi_band, initial_operating_std, step)
                                                            if set_flag:
                                                                print(f"Operating Standard reverted successfully in DUT and verified. Current Operating Standard: {final_op_std}.")
                                                                print("[TEST EXECUTION RESULT] : SUCCESS")
                                                            else:
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                print(f"ACTUAL RESULT {step} : Failed to revert the Operating Standard in DUT to initial Operating Standard: {initial_operating_std}. Current Operating Standard: {final_op_std}")
                                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                                    else:
                                                        print(f"Failed to set the Operating Standard in DUT to the current Operating Standard of the wifi connection. Initial Operating Standard: {initial_operating_std} and Final Operating Standard: {final_operating_std}")
                                                else:
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    print(f"ACTUAL RESULT {step} : Current WLAN IP address of the second wlan client is not in same DHCP range")
                                                    print("[TEST EXECUTION RESULT] : FAILURE")
                                            else:
                                                tdkTestObj.setResultStatus("FAILURE")
                                                print(f"ACTUAL RESULT {step} : Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress not retrieved")
                                                print("[TEST EXECUTION RESULT] : FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                            print(f"ACTUAL RESULT {step} : Current WLAN IP address of the second wlan client not obtained")
                                            print("[TEST EXECUTION RESULT] : FAILURE")
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"ACTUAL RESULT {step}: The second wlan client not connected to WiFi SSID")
                                        print("[TEST EXECUTION RESULT] : FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step} : Current WLAN IP address of the first wlan client is not in same DHCP range")
                                    print("[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step} : Device.X_CISCO_COM_DeviceControl.LanManagementEntry.1.LanIPAddress not retrieved")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step} : Current WLAN IP address of the first wlan client not obtained")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: The first wlan client not connected to WiFi SSID")
                        print("[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Value not retrieved successfully")
                    print("[TEST EXECUTION RESULT] : FAILURE")

                #Prepare the list of parameter values to be reverted
                step = step + 1
                list1 = [ssidName,orgValue[0],'string']
                list2 = [keyPassPhrase,orgValue[1],'string']
                list3 = [radioEnable,orgValue[2],'bool']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2 + list3
                revertParamList = "|".join(map(str, revertParamList))

                #Revert the values to original
                print(f"\nTEST STEP {step}: Should set the original ssid, keypassphrase, radio enable")
                print(f"EXPECTED RESULT {step}: Should set the original ssid, keypassphrase, radio enable")
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: Details: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: Details : {details}")
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Details: {details}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Values not retrieved successfully")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        obj.setLoadModuleStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to parse the device configuration file")
        print("[TEST EXECUTION RESULT] : FAILURE")

    #Handle any post execution cleanup required
    postExecutionCleanup("WLAN")
    postExecutionCleanup("WLAN_2")
    obj.unloadModule("tdkb_e2e")
    sysobj.unloadModule("sysutil")
else:
    print("Failed to load the modules")
    obj.setLoadModuleStatus("FAILURE")
    sysobj.setLoadModuleStatus("FAILURE")
