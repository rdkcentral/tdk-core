# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import tdkbE2EUtility
from tdkbE2EUtility import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("tdkb_e2e","1")

#IP and Port of box, No need to change,
#This will be replaced with correspoing Box Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'E2E_IPV6_CheckDNSResolutionViaPrimaryDNSServerFromLANClient')

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
        step = 1

        wan_ip_address = "Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6"
        dnsServer = "Device.DNS.Client.Server.1.DNSServer"

        # Get the current WAN IPv6 address
        print(f"\nTEST STEP {step}: Get the current WAN IPv6 address")
        print(f"EXPECTED RESULT {step}: Should retrieve the current WAN IPv6 address")
        tdkTestObj,status,wanIpv6Address = getParameterValue(obj,wan_ip_address)
        if expectedresult in status and wanIpv6Address != "":
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {wanIpv6Address}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            step += 1
            # Get the DNS server value
            print(f"\nTEST STEP {step}: Get the current value of DNS Server")
            print(f"EXPECTED RESULT {step}: Should retrieve the current value of DNS Server")
            tdkTestObj,status,dnsServerValue = getParameterValue(obj,dnsServer)
            if expectedresult in status and dnsServerValue != "":
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: {dnsServerValue}")
                print("[TEST EXECUTION RESULT] : SUCCESS")

                #Connect to LAN Client Resolving domain name with nslookup in LAN Client
                step += 1
                print(f"\nTEST STEP {step}: Connect to LAN Client and resolve domain name with nslookup")
                print(f"EXPECTED RESULT {step}: DNS Primary Server should resolve the DNS query")
                status=nslookupInClient(tdkbE2EUtility.nslookup_domain_name,dnsServerValue,'LAN')
                if expectedresult in status:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print(f"ACTUAL RESULT {step}: DNS Primary Server successfully resolves the DNS query")
                    print("[TEST EXECUTION RESULT] : SUCCESS\n")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print(f"ACTUAL RESULT {step}: DNS Primary Server doesn't resolve the DNS query")
                    print("[TEST EXECUTION RESULT] : FAILURE\n")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: {dnsServerValue}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: {wanIpv6Address}")
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