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

from tdkutility import *
from tdkbIPv6Variables import *

import ipaddress


# getWAN_Interface
# Syntax      : getWAN_Interface(tr181obj, step)
# Description : Gets the WAN interface name.
# Parameters  : tr181obj - TR-181 object
#               step - test step number
# Return Value: interface - WAN interface name or empty string
def getWAN_Interface(tr181obj, step):
    expectedresult = "SUCCESS"
    interface = ""
    print(f"\nTEST STEP {step} : Get the WAN interface using Device.DHCPv6.Client.1.Interface")
    print(f"EXPECTED RESULT {step} : Should get the WAN interface using Device.DHCPv6.Client.1.Interface")
    tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
    actualresult, interface = getTR181Value(tdkTestObj, "Device.DHCPv6.Client.1.Interface")
    if expectedresult in actualresult and interface != "":
        print(f"ACTUAL RESULT {step} : Successfully got the WAN interface using Device.DHCPv6.Client.1.Interface. Interface is {interface}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the WAN interface using Device.DHCPv6.Client.1.Interface")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return interface

########## End of function ##########


# VerifyIPv6Address
# Syntax      : verifyIPv6Address(sysobj, interface, step, scope="global")
# Description : Verifies IPv6 address scope on an interface.
# Parameters  : sysobj - sysutil object
#               interface - interface name
#               step - test step number
#               scope - IPv6 scope to verify
# Return Value: flag - True if scope is present else False
def verifyIPv6Address(sysobj, interface, step, scope="global"):
    expectedresult = "SUCCESS"
    flag = False
    # Check whether the provided interface has inet6 address with the specified scope
    command = f"ip -6 addr show {interface} | grep 'inet6' | grep 'scope {scope}'"
    scope = "link local" if scope == "link" else scope
    print(f"TEST STEP {step} : Check whether the {interface} interface has inet6 address with {scope} scope")
    print(f"EXPECTED RESULT {step} : Should check whether the {interface} interface has inet6 address with {scope} scope")
    print(f"Command: {command}")
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command output: {details}")

    if expectedresult in actualresult and details != "":
        flag = True
        print(f"ACTUAL RESULT {step} : Successfully verified that the {interface} interface has inet6 address with {scope} scope")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to verify that the {interface} interface has inet6 address with {scope} scope")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return flag

########## End of function ##########

# ExtractIPv6PrefixandAddress
# Syntax      : extractIPv6PrefixandAddress(sysobj, interface, step, scope="global")
# Description : Extracts IPv6 address and prefix from an interface.
# Parameters  : sysobj - sysutil object
#               interface - interface name
#               step - test step number
#               scope - IPv6 scope to extract, default is "global", can be "link" for link-local
# Return Value: tdkTestObj - executed test object
#               ipv6_addr - IPv6 address
#               ipv6_prefix - IPv6 prefix length
#               flag - True if extraction succeeds else False


def extractIPv6PrefixandAddress(sysobj, interface, step, scope="global"):
    expectedresult = "SUCCESS"
    ipv6_addr = ""
    ipv6_prefix = None
    flag = False
    print(f"TEST STEP {step} : Get the IP address and prefix of the {interface} interface with {scope} scope")
    print(f"EXPECTED RESULT {step} : Should get the IP address and prefix of the {interface} interface with {scope} scope")
    command = f"ip -6 addr show {interface} | grep 'inet6' | grep 'scope {scope}' | awk '{{print$2}}'"
    print(f"Command: {command}")
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command output: {details}")

    print("Checking if the output is a valid IPv6 address")
    if expectedresult in actualresult and details != "":
        try:
            ipv6_interface = ipaddress.ip_interface(details.strip())
            ipv6_addr = str(ipv6_interface.ip)
            ipv6_prefix = ipv6_interface.network.prefixlen
            print("The output is a valid IPv6 address.")
        except ValueError:
            ipv6_addr = ""
            ipv6_prefix = None
            print("The output is NOT a valid IPv6 address.")

    if expectedresult in actualresult and ipv6_prefix is not None:
        flag = True
        print(f"ACTUAL RESULT {step} : Successfully got the IP address and prefix of the {interface} interface with {scope} scope. IP address is {ipv6_addr}, Prefix is {ipv6_prefix}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the IP address and prefix of the {interface} interface with {scope} scope. IP address is {ipv6_addr}, Prefix is {ipv6_prefix}")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return tdkTestObj, ipv6_addr, ipv6_prefix, flag

########## End of function ##########


# GetWANIPv6Address
# Syntax      : getWANIPv6Address(tr181obj, step, validity_check=False)
# Description : Gets WAN IPv6 address and optionally validates it.
# Parameters  : tr181obj - TR-181 object
#               step - test step number
#               validity_check - validate address format when True
# Return Value: tdkTestObj - executed test object
#               ipv6 - WAN IPv6 address or empty string
#               flag - True if retrieval succeeds else False
#               step - updated test step number
def getWANIPv6Address(tr181obj, step, validity_check=False):
    expectedresult = "SUCCESS"
    ipv6 = ""
    flag = True
    tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
    print(f"\nTEST STEP {step} : Get the IPv6 address using Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6")
    print(f"EXPECTED RESULT {step} : Should get the IPv6 address using Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6")
    actualresult, details = getTR181Value(tdkTestObj, "Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6")
    if expectedresult in actualresult and details != "":
        print(f"ACTUAL RESULT {step} : Successfully got the IPv6 address using Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6. IPv6 address is {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")

        if validity_check:
            step += 1
            # Verify whether the IPv6 address is valid or not
            print(f"TEST STEP {step} : Verify whether the IPv6 address is valid or not")
            print(f"EXPECTED RESULT {step} : Should verify whether the IPv6 address is valid or not")
            try:
                ipv6 = str(ipaddress.IPv6Address(details.strip()))
                print(f"ACTUAL RESULT {step} : Successfully verified that the IPv6 address is valid")
                tdkTestObj.setResultStatus("SUCCESS")
                print("[TEST EXECUTION RESULT] : SUCCESS\n")
            except ipaddress.AddressValueError:
                flag = False
                print(f"ACTUAL RESULT {step} : Failed to verify that the IPv6 address is valid")
                tdkTestObj.setResultStatus("FAILURE")
                print("[TEST EXECUTION RESULT] : FAILURE\n")
        else:
            ipv6 = details.strip()
    else:
        flag = False
        print(f"ACTUAL RESULT {step} : Failed to get the IPv6 address using Device.DeviceInfo.X_COMCAST-COM_WAN_IPv6")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")

    return tdkTestObj, ipv6, flag, step

########## End of function ##########


# GetActiveClientIndex
# Syntax      : getActiveClientIndex(tr181obj, expected_value, step)
# Description : Finds the active client index for a given interface type.
# Parameters  : tr181obj - TR-181 object
#               expected_value - Layer1Interface value
#               step - test step number
# Return Value: index - active host index or None
#               step - updated test step number
def getActiveClientIndex(tr181obj, expected_value, step):
    expectedresult = "SUCCESS"
    if expected_value == "Ethernet":
        client_type = "LAN"
    else:
        client_type = "WLAN"
    index = None
    # Get the number of hosts in Device.Hosts
    print(f"\nTEST STEP {step} : Get the number of hosts in Device.Hosts using Device.Hosts.HostNumberOfEntries")
    print(f"EXPECTED RESULT {step} : Should get the number of hosts in Device.Hosts using Device.Hosts.HostNumberOfEntries")
    tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
    actualresult, host_number = getTR181Value(tdkTestObj, "Device.Hosts.HostNumberOfEntries")
    host_number = int(host_number) if host_number.isdigit() else 0
    if expectedresult in actualresult and host_number > 0:
        print(f"ACTUAL RESULT {step} : Successfully got the number of hosts in Device.Hosts using Device.Hosts.HostNumberOfEntries. Number of hosts is {host_number}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")


        # Loop through the number of hosts and find the expected value in Device.Hosts.Host.{i}.Layer1Interface
        step += 1
        print(f"\nTEST STEP {step} : Loop through the number of hosts and find an active client with Layer1Interface value {expected_value}")
        print(f"EXPECTED RESULT {step} : Should find an active client with Layer1Interface value {expected_value}")
        for i in range(1, host_number + 1):
            print(f"\nGet the Layer1Interface of the host using Device.Hosts.Host.{i}.Layer1Interface")
            tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
            actualresult, layer1_interface = getTR181Value(tdkTestObj, f"Device.Hosts.Host.{i}.Layer1Interface")
            if expectedresult in actualresult and expected_value in layer1_interface:
                print(f"Successfully got the Layer1Interface of the host using Device.Hosts.Host.{i}.Layer1Interface. Layer1Interface is {layer1_interface}")

                # Check whether the LAN client is active
                print(f"\nCheck whether the client is active using Device.Hosts.Host.{i}.Active")
                tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
                actualresult, active_status = getTR181Value(tdkTestObj, f"Device.Hosts.Host.{i}.Active")
                if expectedresult in actualresult and active_status == "true":
                    index = i
                    print(f"Successfully verified that the client is active using Device.Hosts.Host.{i}.Active. Active status is {active_status}\n")

                    print(f"ACTUAL RESULT {step} : Found an active {client_type} client with Layer1Interface value {expected_value} at Device.Hosts.Host.{i}")
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("[TEST EXECUTION RESULT] : SUCCESS\n")
                    return index, step
                else:
                    print(f"The client is not active using Device.Hosts.Host.{i}.Active. Active status is {active_status}. Continuing to check the next host if available.")
            else:
                print(f"Failed to get the Layer1Interface of the host using Device.Hosts.Host.{i}.Layer1Interface or it does not match the expected value. Layer1Interface is {layer1_interface}. Continuing to check the next host if available.")
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step} : Failed to find an active {client_type} client with Layer1Interface value {expected_value}")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the number of hosts in Device.Hosts using Device.Hosts.HostNumberOfEntries or No hosts are connected. Number of hosts is {host_number}")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return index, step

########## End of function ##########


# CheckInternetConnectivity
# Syntax      : checkInternetConnectivity(sysobj, host_name, ping_count, step, interface=None)
# Description : Checks connectivity by ping.
# Parameters  : sysobj - sysutil object
#               host_name - host or IP to ping
#               ping_count - number of ping packets
#               step - test step number
#               interface - optional interface name
# Return Value: True - ping succeeds with zero packet loss
#               False - ping fails
def checkInternetConnectivity(sysobj, host_name, ping_count, step, interface=None):
    expectedresult = "SUCCESS"
    if interface is None:
        print(f"TEST STEP {step} : Check internet connectivity by pinging {host_name}")
        command = f"ping -6 -c {ping_count} {host_name} | grep 'packet loss'"
    else:
        print(f"TEST STEP {step} : Check internet connectivity by pinging {host_name} via interface {interface}")
        command = f"ping -6 -I {interface} -c {ping_count} {host_name} | grep 'packet loss'"
    print(f"EXPECTED RESULT {step} : Should check internet connectivity by pinging {host_name}")
    print(f"Command: {command}")
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command output: {details}")
    if expectedresult in actualresult and '0% packet loss' in details:
        print(f"ACTUAL RESULT {step} : Successfully checked internet connectivity by pinging {host_name}. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
        return True
    else:
        print(f"ACTUAL RESULT {step} : Failed to check internet connectivity by pinging {host_name}. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
        return False

########## End of function ##########


# GetClientLinkLocalIPv6Address
# Syntax      : getClientLinkLocalIPv6Address(tr181obj, index, step)
# Description : Gets the client link-local IPv6 address.
# Parameters  : tr181obj - TR-181 object
#               index - active host index
#               step - test step number
# Return Value: ipv6_link_local - link-local IPv6 address or empty string
#               flag - True if retrieval succeeds else False
def getClientLinkLocalIPv6Address(tr181obj, index, step):
    ipv6_link_local = ""
    flag = False
    expectedresult = "SUCCESS"
    print(f"\nTEST STEP {step} : Get the link-local IPv6 address of the active LAN client")
    print(f"EXPECTED RESULT {step} : Should get the link-local IPv6 address of the active LAN client")
    tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
    actualresult, ipv6_link_local = getTR181Value(tdkTestObj, f"Device.Hosts.Host.{index}.IPv6Address.2.IPAddress")
    if expectedresult in actualresult and ipv6_link_local != "":
        flag = True
        print(f"ACTUAL RESULT {step} : Successfully got the link-local IPv6 address of the active LAN client using Device.Hosts.Host.{index}.IPv6Address.2.IPAddress. Link-local IPv6 address is {ipv6_link_local}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the link-local IPv6 address of the active LAN client using Device.Hosts.Host.{index}.IPv6Address.2.IPAddress")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return ipv6_link_local, flag

########## End of function ##########

# GetIPv6DNSServerAddresses
# Syntax      : getIPv6DNSServerAddresses(tr181obj, step, type="Primary")
# Description : Gets the IPv6 DNS server addresses.
# Parameters  : tr181obj - TR-181 object
#               step - test step number
#               type - "Primary" or "Secondary" to specify which DNS server to retrieve
# Return Value: details - DNS server address string
#               tdkTestObj - executed test object
#               flag - True if retrieval succeeds else False
def getIPv6DNSServerAddresses(tr181obj, step, type = "Primary"):
    if type == "Secondary":
        index = 2
    else:
        index = 1
    expectedresult = "SUCCESS"
    details = ""
    print(f"\nTEST STEP {step} : Get the value of Device.DNS.Client.Server.{index}.DNSServer using {type} DNS server")
    print(f"EXPECTED RESULT {step} : Should get the value of Device.DNS.Client.Server.{index}.DNSServer")
    tdkTestObj = tr181obj.createTestStep('TDKB_TR181Stub_Get')
    actualresult, details = getTR181Value(tdkTestObj, f"Device.DNS.Client.Server.{index}.DNSServer")
    if expectedresult in actualresult and details != "":
        print(f"ACTUAL RESULT {step} : Successfully got the value of Device.DNS.Client.Server.{index}.DNSServer using {type} DNS server. Details : {details}")
        tdkTestObj.setResultStatus("SUCCESS")
        print("[TEST EXECUTION RESULT] : SUCCESS\n")
    else:
        print(f"ACTUAL RESULT {step} : Failed to get the value of Device.DNS.Client.Server.{index}.DNSServer using {type} DNS server. Details : {details}")
        tdkTestObj.setResultStatus("FAILURE")
        print("[TEST EXECUTION RESULT] : FAILURE\n")
    return tdkTestObj, details
########## End of function ##########

#resolveDomainUsingDNS
# Syntax      : resolveDomainUsingDNS(sysobj, domain, dns_server, step)
# Description : Resolves a domain using a specified DNS server.
# Parameters  : sysobj - sysutil object
#               domain - domain name to resolve
#               dns_server - DNS server address to use for resolution
#               step - test step number
# Return Value: flag - True if resolution succeeds else False
def resolveDomainUsingDNS(sysobj, domain, dns_server, step):
    expectedresult = "SUCCESS"
    flag = False
    print(f"\nTEST STEP {step} : Resolve the domain {domain} using DNS server {dns_server}")
    print(f"EXPECTED RESULT {step} : Should resolve the domain {domain} using DNS server {dns_server}")
    command = f"nslookup {domain} {dns_server} | xargs"
    print(f"Command: {command}")
    tdkTestObj = sysobj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command output: {details}")
    result_section = details.split("Name:", 1)[1] if "Name:" in details else ""
    resolved_ip = result_section.split("Address 1:", 1)[1].split()[0] if "Address 1:" in result_section else ""
    if expectedresult in actualresult and result_section and "Address 1:" in result_section and "Address 2:" in result_section:
        print(f"ACTUAL RESULT {step} : Successfully resolved the domain {domain} using DNS server {dns_server}.")
        flag = True
    else:
        print(f"ACTUAL RESULT {step} : Failed to resolve the domain {domain} using DNS server {dns_server}.")
    return tdkTestObj, flag, resolved_ip
########## End of function ##########


