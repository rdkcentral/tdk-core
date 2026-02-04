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

import tdklib
from time import sleep
from RNDISVariables import *
from tdkutility import *

# get_target_wan_interface
# Syntax : get_target_wan_interface(obj, expected_interface)
# Description : Function to verify the target WAN interface has an IP address assigned
# Parameters : obj - module object
#              expected_interface - expected interface name
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
def get_target_wan_interface(obj, expected_interface):
    command = f"ifconfig {expected_interface} | grep '{INET_ADDR_PATTERN}' | awk '{{print $2}}' | cut -d: -f2"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Command output: %s" % details)

    if details.strip() != "":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# get_interface_mac_address
# Syntax : get_interface_mac_address(obj, interface_name)
# Description : Function to get the MAC address of a network interface
# Parameters : obj - module object
#              interface_name - name of the interface
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               mac_address - MAC address of the interface
def get_interface_mac_address(obj, interface_name):
    command = f"ifconfig {interface_name} | grep '{HWADDR_PATTERN}' | awk '{{print $5}}'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Command output: %s" % details)

    mac_address = details.strip()
    if mac_address != "":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, mac_address
########## End of function ##########

# verify_ip_match
# Syntax : verify_ip_match(interface_ip, dm_ip)
# Description : Function to verify if interface IP matches data model IP
# Parameters : interface_ip - IP address from interface
#              dm_ip - IP address from data model
# Return Value: actualresult - SUCCESS/FAILURE
#               details - comparison details
def verify_ip_match(interface_ip, dm_ip):
    print("Comparing Interface IP: %s with DM IP: %s" % (interface_ip, dm_ip))

    if interface_ip == dm_ip:
        actualresult = "SUCCESS"
        details = f"IP addresses match: Interface={interface_ip}, DM={dm_ip}"
    else:
        actualresult = "FAILURE"
        details = f"IP addresses mismatch: Interface={interface_ip}, DM={dm_ip}"

    return actualresult, details
########## End of function ##########

# verify_mac_match
# Syntax : verify_mac_match(interface_mac, dm_mac)
# Description : Function to verify if interface MAC matches data model MAC
# Parameters : interface_mac - MAC address from interface
#              dm_mac - MAC address from data model
# Return Value: actualresult - SUCCESS/FAILURE
#               details - comparison details
def verify_mac_match(interface_mac, dm_mac):
    print("Comparing Interface MAC: %s with DM MAC: %s" % (interface_mac, dm_mac))

    # Normalize MAC addresses to upper case for comparison
    interface_mac_upper = interface_mac.upper()
    dm_mac_upper = dm_mac.upper()

    if interface_mac_upper == dm_mac_upper:
        actualresult = "SUCCESS"
        details = f"MAC addresses match: Interface={interface_mac}, DM={dm_mac}"
    else:
        actualresult = "FAILURE"
        details = f"MAC addresses mismatch: Interface={interface_mac}, DM={dm_mac}"

    return actualresult, details
########## End of function ##########

# perform_ping_test
# Syntax : perform_ping_test(obj, target, count)
# Description : Function to perform ping test and verify 0% packet loss
# Parameters : obj - module object
#              target - ping target
#              count - number of ping packets to send
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - ping command output
def perform_ping_test(obj, target, count):
    command = f'ping -c {count} {target} | grep "0% packet loss"'
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Command output: %s" % details)

    # Check if ping was successful with 0% packet loss
    if "0% packet loss" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# check_interface_no_ip
# Syntax : check_interface_no_ip(obj, interface_name)
# Description : Function to verify interface does not have an IP address
# Parameters : obj - module object
#              interface_name - name of the interface
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - interface status details
def check_interface_no_ip(obj, interface_name):
    command = f"ifconfig {interface_name} | grep {INET_ADDR_PATTERN}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Command output: %s" % details)

    # Check if interface has no IP address
    if details == "":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# monitor_cellular_status
# Syntax : monitor_cellular_status(obj)
# Description : Function to monitor cellular registration status over time
# Parameters : obj - TR181 module object
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - monitoring results summary
def monitor_cellular_status(obj):
    print(f"Starting monitoring of {DM_CELLULAR_RDK_STATUS} for {MONITORING_DURATION} seconds, checking every {MONITORING_INTERVAL} seconds...")
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    import time
    start_time = time.time()
    check_count = 0
    successful_checks = 0

    while (time.time() - start_time) < MONITORING_DURATION:
        check_count += 1
        actualresult, details = getTR181Value(tdkTestObj, DM_CELLULAR_RDK_STATUS)

        if "SUCCESS" in actualresult:
            status_value = details.split("VALUE:")[1].split(' ')[0].strip() if "VALUE:" in details else details.strip()
            print(f"Check {check_count}: Current status is {status_value}")
            if status_value == EXPECTED_STATUS_CONNECTED:
                successful_checks += 1
        else:
            print(f"Check {check_count}: Failed to get status - {details}")

        sleep(MONITORING_INTERVAL)

    # Determine overall result
    if successful_checks == check_count and check_count > 0:
        actualresult = "SUCCESS"
        details = f"Monitoring completed successfully: {successful_checks}/{check_count} checks passed, Status remained {EXPECTED_STATUS_CONNECTED}"
    else:
        actualresult = "FAILURE"
        details = f"Monitoring failed: {successful_checks}/{check_count} checks passed"

    return tdkTestObj, actualresult, details
########## End of function ##########

# get_cellular_statistics
# Syntax : get_cellular_statistics(obj)
# Description : Function to get cellular interface statistics
# Parameters : obj - TR181 module object
# Return Value: tdkTestObj - test object
#               bytes_sent - BytesSent value
#               bytes_received - BytesReceived value
#               packets_sent - PacketsSent value
#               packets_received - PacketsReceived value
def get_cellular_statistics(obj):
    tdkTestObj = obj.createTestStep("TDKB_TR181Stub_Get")
    # Get BytesSent
    actualresult, details = getTR181Value(tdkTestObj, DM_CELLULAR_STATS_BYTES_SENT)
    if "SUCCESS" in actualresult and details != "":
        bytes_sent = int(details.strip())
    else:
        print("FAILURE: Failed to get %s. Details: %s" % (DM_CELLULAR_STATS_BYTES_SENT, details))
        bytes_sent = 0
    # Get BytesReceived
    actualresult, details = getTR181Value(tdkTestObj, DM_CELLULAR_STATS_BYTES_RECEIVED)
    if "SUCCESS" in actualresult and details != "":
        bytes_received = int(details.strip())
    else:
        print("FAILURE: Failed to get %s. Details: %s" % (DM_CELLULAR_STATS_BYTES_RECEIVED, details))
        bytes_received = 0
    # Get PacketsSent
    actualresult, details = getTR181Value(tdkTestObj, DM_CELLULAR_STATS_PACKETS_SENT)
    if "SUCCESS" in actualresult and details != "":
        packets_sent = int(details.strip())
    else:
        print("FAILURE: Failed to get %s. Details: %s" % (DM_CELLULAR_STATS_PACKETS_SENT, details))
        packets_sent = 0
    # Get PacketsReceived
    actualresult, details = getTR181Value(tdkTestObj, DM_CELLULAR_STATS_PACKETS_RECEIVED)
    if "SUCCESS" in actualresult and details != "":
        packets_received = int(details.strip())
    else:
        print("FAILURE: Failed to get %s. Details: %s" % (DM_CELLULAR_STATS_PACKETS_RECEIVED, details))
        packets_received = 0
    return tdkTestObj, bytes_sent, bytes_received, packets_sent, packets_received
########## End of function ##########

# traverse_host_table_for_client
# Syntax : traverse_host_table_for_client(obj, host_entries, client_type, step)
# Description : Function to traverse host table and find client entry based on type
# Parameters : obj - TR181 module object
#              host_entries - total number of host entries to traverse
#              client_type - type of client
#              step - current test step number
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               client_detected - 1 if client detected, 0 otherwise
#               client_index - index of detected client entry
#               detected_info - additional info
#               step - updated step number
def traverse_host_table_for_client(obj, host_entries, client_type, step):
    expectedresult = "SUCCESS"
    clientDetected = 0
    clientIndex = -1
    detectedInfo = ""

    for index in range(1, host_entries + 1):
        print("\n**········For Host Table Entry %d**········" % index)

        step += 1
        # Get the value of Device.Hosts.Host.{i}.Layer1Interface
        paramName = "Device.Hosts.Host." + str(index) + ".Layer1Interface"

        print("\nTEST STEP %d: Get the value of %s and check if it is Ethernet" % (step, paramName))

        print("EXPECTED RESULT %d: Should successfully retrieve %s" % (step, paramName))
        tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
        actualresult, details = getTR181Value(tdkTestObj_tr181, paramName)

        if expectedresult in actualresult:
            layer1Interface = details.split("VALUE:")[1].split(',')[0].strip() if "VALUE:" in details else details.strip()
            tdkTestObj_tr181.setResultStatus("SUCCESS")
            print("ACTUAL RESULT %d: %s : %s" % (step, paramName, layer1Interface))
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Check for LAN client only
            client_match = False
            if layer1Interface == EXPECTED_LAYER1_INTERFACE_ETHERNET:
                client_match = True

            if client_match:
                clientDetected = 1
                clientIndex = index
                print("Identified the Host Table Entry for %s client as : %d" % (client_type, index))

                # Check if the client is shown as active
                step += 1
                paramName = "Device.Hosts.Host." + str(index) + ".Active"
                print("\nTEST STEP %d: Get the value of %s and check if it is true" % (step, paramName))
                print("EXPECTED RESULT %d: Should successfully retrieve %s and it should be true" % (step, paramName))
                tdkTestObj_tr181 = obj.createTestStep('TDKB_TR181Stub_Get')
                actualresult, details = getTR181Value(tdkTestObj_tr181, paramName)

                if expectedresult in actualresult:
                    activeStatus = details.split("VALUE:")[1].split(',')[0].strip() if "VALUE:" in details else details.strip()
                    tdkTestObj_tr181.setResultStatus("SUCCESS")
                    print("ACTUAL RESULT %d: %s : %s" % (step, paramName, activeStatus))
                    print("[TEST EXECUTION RESULT] : SUCCESS")

                    if activeStatus == "true":
                        tdkTestObj_tr181.setResultStatus("SUCCESS")
                        print("Host is Active - LAN client detected in Host Table while RNDIS is active")
                        break
                    else:
                        tdkTestObj_tr181.setResultStatus("FAILURE")
                        print("Host is NOT Active")
                        break
                else:
                    tdkTestObj_tr181.setResultStatus("FAILURE")
                    print("ACTUAL RESULT %d: Failed to get %s. Details: %s" % (step, paramName, details))
                    print("[TEST EXECUTION RESULT] : FAILURE")
                    break
            else:
                print("Host Table Entry %d Layer1Interface is %s (not Ethernet)" % (index, layer1Interface))
                continue
        else:
            tdkTestObj_tr181.setResultStatus("FAILURE")
            print("ACTUAL RESULT %d: Failed to get %s. Details: %s" % (step, paramName, details))
            print("[TEST EXECUTION RESULT] : FAILURE")
            break

    return tdkTestObj_tr181, actualresult, clientDetected, clientIndex, detectedInfo, step
########## End of function ##########
