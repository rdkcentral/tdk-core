# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time;
from tdkbE2EUtility import *;
import tdkbE2EUtility;
import ipaddress

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_IPV6_CheckInternetConnectivityFromWLANClient')

#Get the result of connection with test component
loadmodulestatus =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %loadmodulestatus)

if "SUCCESS" in loadmodulestatus.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedresult = "SUCCESS"

    #Parse the device configuration file
    status = parseDeviceConfig(obj)
    if expectedresult in status:
        obj.setLoadModuleStatus("SUCCESS")
        print("Parsed the device configuration file successfully")

        #Assign the WIFI parameters names to a variable
        ssidName = f"Device.WiFi.SSID.{tdkbE2EUtility.ssid_5ghz_index}.SSID"
        keyPassPhrase = f"Device.WiFi.AccessPoint.{tdkbE2EUtility.ssid_5ghz_index}.Security.KeyPassphrase"
        dnsServer = "Device.DNS.Client.Server.1.DNSServer"
        wan_ip_address = "Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6"

        #Get the WAN IPv6 address of the DUT
        step = 1
        print(f"\nTEST STEP {step}: Get the current WAN IPv6 address")
        print(f"EXPECTED RESULT {step}: Should retrieve the current WAN IPv6 address")
        tdkTestObj,status,wanIpv6Address = getParameterValue(obj,wan_ip_address)
        if expectedresult in status and wanIpv6Address != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {wanIpv6Address}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            step += 1

            #Get the value of the wifi parameters that are currently set.
            print(f"\nTEST STEP {step}: Get the current value of DNS Server")
            print(f"EXPECTED RESULT {step}: Should retrieve the current value of DNS Server")
            paramList=[ssidName,keyPassPhrase,dnsServer]
            tdkTestObj,status,orgValue = getMultipleParameterValues(obj,paramList)

            if expectedresult in status:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {orgValue[2]}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                setValuesList = [tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd]
                print("WIFI parameter values that are set: %s" %setValuesList)

                list1 = [ssidName,tdkbE2EUtility.ssid_5ghz_name,'string']
                list2 = [keyPassPhrase,tdkbE2EUtility.ssid_5ghz_pwd,'string']

                #Concatenate the lists with the elements separated by pipe
                setParamList = list1 + list2
                setParamList = "|".join(map(str, setParamList))
                step += 1
                print(f"\nTEST STEP {step}: Set the ssid,keypassphrase")
                print(f"EXPECTED RESULT {step}: Should set the ssid,keypassphrase")
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,setParamList)

                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: {details}")
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    #Retrieve the values after set and compare
                    newParamList=[ssidName,keyPassPhrase]
                    step += 1
                    print(f"\nTEST STEP {step}: Get the current ssid,keypassphrase")
                    print(f"EXPECTED RESULT {step}: Should retrieve the current ssid,keypassphrase")
                    tdkTestObj,status,newValues = getMultipleParameterValues(obj,newParamList)
                    if expectedresult in status and setValuesList == newValues:
                        tdkTestObj.setResultStatus("SUCCESS")
                        print(f"ACTUAL RESULT {step}: {newValues}")
                        print("[TEST EXECUTION RESULT] : SUCCESS")

                        #Wait for the changes to reflect in client device
                        time.sleep(60)

                        #Connect to the wifi ssid from wlan client
                        step += 1
                        print(f"\nTEST STEP {step}: From wlan client, Connect to the wifi ssid")
                        print(f"EXPECTED RESULT {step}: Should connect to the wifi ssid from wlan client")
                        status = wlanConnectWifiSsid(tdkbE2EUtility.ssid_5ghz_name,tdkbE2EUtility.ssid_5ghz_pwd,tdkbE2EUtility.wlan_5ghz_interface)
                        if expectedresult in status:
                            tdkTestObj.setResultStatus("SUCCESS")
                            print(f"ACTUAL RESULT {step}: Connected to the wifi ssid from wlan client")
                            print("[TEST EXECUTION RESULT] : SUCCESS")

                            # Get the IPv6 address of WLAN client interface
                            step += 1
                            print(f"\nTEST STEP {step}: Get the current IPV6 address of WLAN client interface")
                            print(f"EXPECTED RESULT {step}: Should retrieve the current IPV6 address of WLAN client interface")
                            wlanIPV6 = getWLANIPV6Address(tdkbE2EUtility.wlan_5ghz_interface)
                            print(f"ACTUAL RESULT {step}: The IPV6 address of wlan client is {wlanIPV6}")
                            if wlanIPV6:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                #Check whether the IPv6 Address obtained above is valid
                                step += 1
                                print(f"\nTEST STEP {step}: Check whether the IPv6 address obtained from WLAN client is valid")
                                print(f"EXPECTED RESULT {step}: The WLAN client should have a valid IPv6 address")
                                try:
                                    ipaddress.IPv6Address(wlanIPV6)
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    print(f"ACTUAL RESULT {step}: The IPv6 address {wlanIPV6} is valid")
                                    print(f"[TEST EXECUTION RESULT] : SUCCESS")

                                    #Check internet connectivity by pinging to an IPv6 host via wlan interface
                                    step += 1
                                    print(f"\nTEST STEP {step}: Check internet connectivity by pinging to an IPv6 host via wlan interface")
                                    print(f"EXPECTED RESULT {step}: Should ping to an IPv6 host via wlan interface")
                                    status = verifyIPv6NetworkConnectivity("IPV6_PING_TO_HOST", tdkbE2EUtility.ipv6_host_name, tdkbE2EUtility.wlan_5ghz_interface, "WLAN")
                                    if expectedresult in status:
                                        tdkTestObj.setResultStatus("SUCCESS")
                                        print(f"ACTUAL RESULT {step}: Successfully pinged to an IPv6 host via wlan interface")
                                        print(f"[TEST EXECUTION RESULT] : SUCCESS")
                                    else:
                                        print(f"ACTUAL RESULT {step}: Failed to ping to an IPv6 host via wlan interface")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        print(f"[TEST EXECUTION RESULT] : FAILURE")

                                except ValueError:
                                    tdkTestObj.setResultStatus("FAILURE")
                                    print(f"ACTUAL RESULT {step}: The IPv6 address {wlanIPV6} is invalid")
                                    print(f"[TEST EXECUTION RESULT] : FAILURE")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"[TEST EXECUTION RESULT] : FAILURE")

                            #Disconnect the wlan client
                            step += 1
                            print(f"\nTEST STEP {step}: From wlan client, Disconnect from the wifi ssid")
                            print(f"EXPECTED RESULT {step}: Should disconnect from the wifi ssid from wlan client")
                            status = wlanDisconnectWifiSsid(tdkbE2EUtility.wlan_5ghz_interface)
                            if expectedresult in status:
                                tdkTestObj.setResultStatus("SUCCESS")
                                print(f"ACTUAL RESULT {step}: WiFi disconnected successfully")
                                print("[TEST EXECUTION RESULT] : SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print(f"ACTUAL RESULT {step}: Wifi disconnect failed")
                                print("[TEST EXECUTION RESULT] : FAILURE")
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print(f"ACTUAL RESULT {step}: From wlan client, failed to connect to the wifi ssid")
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print(f"ACTUAL RESULT {step}: %s" %newValues)
                        print(f"[TEST EXECUTION RESULT] : FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: %s" %details)
                    print(f"[TEST EXECUTION RESULT] : FAILURE")

                #Prepare the list of parameter values to be reverted
                list1 = [ssidName,orgValue[0],'string']
                list2 = [keyPassPhrase,orgValue[1],'string']

                #Concatenate the lists with the elements separated by pipe
                revertParamList = list1 + list2
                revertParamList = "|".join(map(str, revertParamList))

                #Revert the values to original
                step += 1
                print(f"\nTEST STEP {step}: Set the original ssid,keypassphrase")
                print(f"EXPECTED RESULT {step}: Should set the original ssid,keypassphrase")
                tdkTestObj,actualresult,details = setMultipleParameterValues(obj,revertParamList)
                if expectedresult in actualresult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: %s" %details)
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    details = tdkTestObj.getResultDetails()
                    print(f"ACTUAL RESULT {step}: %s" %details)
                    print("[TEST EXECUTION RESULT] : FAILURE")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: %s" %orgValue)
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            print(f"ACTUAL RESULT {step}: Failed to get the current WAN IPv6 address. WAN IPv6 address is {wanIpv6Address}")
            print("[TEST EXECUTION RESULT] : FAILURE")
            tdkTestObj.setResultStatus("FAILURE")
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