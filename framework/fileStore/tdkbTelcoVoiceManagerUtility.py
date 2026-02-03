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
from tdkutility import *
from tdkbTelcoVoiceManagerVariables import *

# initiateCall
# Syntax      : initiateCall(obj, client1_user, client2_user, dialplan_context, step)
# Description : Function to initiate a call between two sip clients configured in asterisk server
# Parameters  : obj - module object
#               client1_user - SIP Client 1 username
#               client2_user - SIP Client 2 username
#               dialplan_context - Dialplan context - internal/external
#               step - Test step number
# Return Value : status - True/False based on call initiation success
def initiateCall(obj, client1_user, client2_user, dialplan_context, step):
    expectedresult = "SUCCESS"

    print(f"\nTEST STEP {step}: Initiate a call between the sip clients configured - {client1_user} to {client2_user}")
    print(f"EXPECTED RESULT {step}: The call should be initiated successfully.")
    command = f"asterisk -x 'channel originate PJSIP/{client1_user} extension {client2_user}@from-{dialplan_context}'"
    print(f"Command : {command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if expectedresult in actualresult and details == "":
        status = True
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: The call is initiated successfully between the configured SIP Clients")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        status = False
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to initiate the call successfully")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return status

# callHangup
# Syntax      : callHangup(obj, step)
# Description : Function to hang up the call between two sip clients configured in asterisk server
# Parameters  : obj - module object
#               step - Test step number
# Return Value : hangup_status - True/False based on call hangup success
def callHangup(obj, step, prereq=False):
    #Hang Up the call
    expectedresult = "SUCCESS"
    if prereq:
        #expected details can be empty or "Requested Hangup" based on whether there was an active call or not
        expected_details = ["", "Requested Hangup"]
    else:
        expected_details = ["Requested Hangup"]

    print(f"\nTEST STEP {step}: Hang up the call between the sip clients in asterisk server.")
    print(f"EXPECTED RESULT {step}: The call should be hung up successfully.")
    command = f"asterisk -x 'channel request hangup all'"
    print(f"Command : {command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Hangup Details: {details}")
    if expectedresult in actualresult and any(item in details for item in expected_details):
        hangup_status = True
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: The call should be hung up successfully between the SIP Clients.")
        print("[TEST EXECUTION RESULT] : SUCCESS")
        sleep(5)
    else:
        hangup_status = False
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to hang up the call.")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return hangup_status


# clientStatus
# Syntax      : clientStatus(obj, client_username)
# Description : Function to get the status of the SIP client configured in asterisk server
# Parameters  : obj - module object
#               client_username - SIP Client username
# Return Value : tdkTestObj - module test object
#                actualresult - actual result of the test execution
#                details - status of the SIP client

def clientStatus(obj, client_username):
    command = f'asterisk -x "pjsip show endpoints" | awk \'$1=="Endpoint:" && $2=="{client_username}"\''
    print(f"Command : {command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Command Output: {details}")
    return tdkTestObj, actualresult, details

# GetActiveCallCount
# Syntax      : getActiveCallCount(obj)
# Description : Function to get the active call count from asterisk server
# Parameters  : obj - module object
# Return Value : tdkTestObj - module test object
#                actualresult - actual result of the test execution
#                call_count - active call count retrieved from asterisk server

def getActiveCallCount(obj):
    command = "asterisk -x 'core show channels' | awk '/active call/ {print $1}'"
    print(f"Command : {command}")
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, call_count = doSysutilExecuteCommand(tdkTestObj, command)
    if call_count.strip().isdigit():
        call_count = int(call_count.strip())
    return tdkTestObj, actualresult, call_count


# getTelcoOutboundConfigs
# Syntax      : getTelcoOutboundConfigs(obj)
# Description : Function to get Telco Outbound configurations
# Parameters  : obj - module object
#               step - test step count
# Return Value : get_flag - Get operation Result Flag
#                values - Outbound call configuration values obtained
def getTelcoOutboundConfigs(obj, step):
    expectedresult = "SUCCESS"
    paramList = ["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable", "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy", "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxyPort", "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName", "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword"]
    result = [None] * len(paramList)
    values = [None] * len(paramList)
    print(f"\nTEST STEP {step}: Get the outbound call configurations in the asterisk server hosted in DUT.")
    print(f"EXPECTED RESULT {step}: Should get the outbound call configurations from the asterisk server.")
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    for index in range(len(paramList)):
        print("\n Getting parameter: %s" %paramList[index])
        result[index], values[index] = getTR181Value(tdkTestObj, paramList[index])
    getValues = dict(zip(paramList, values))
    print(f"Retrieved values: {getValues}")
    print(f"Result : {result}")
    if all(res == expectedresult for res in result):
        get_flag = True
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Successfully got the outbound call configurations")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        get_flag = False
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get the outbound call configurations")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return get_flag, values


# setTelcoOutboundConfigs
# Syntax      : setTelcoOutboundConfigs(obj)
# Description : Function to set Telco Outbound configurations
# Parameters  : obj - module object
#               value_list - List of configuration values to be set\
#               step - test step count
# Return Value : set_flag - outbound configuration values set

def setTelcoOutboundConfigs(obj, value_list, step):
    set_flag = True
    expectedresult = "SUCCESS"

    paramList = ["Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Enable", "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxy", "Device.Services.VoiceService.1.VoiceProfile.1.SIP.OutboundProxyPort", "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthUserName", "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.SIP.AuthPassword"]
    paramType = ["string", "string", "unsignedint", "string", "string"]

    setValues = dict(zip(paramList,value_list))
    print(f"Setting Values: {setValues}")

    print(f"\nTEST STEP {step}: Set the outbound call configurations in the asterisk server hosted in DUT.")
    print(f"EXPECTED RESULT {step}: Should set the outbound call configurations in the asterisk server.")

    set_result = [None] * len(paramList)
    set_details = [None] * len(paramList)
    for i in range(len(paramList)):
        if i == len(paramList)-1:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_SetOnly')
        else:
            tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Set')
        print("\n Setting parameter: %s to value: %s" %(paramList[i], value_list[i]))
        set_result[i], set_details[i] = setTR181Value(tdkTestObj, paramList[i], value_list[i], paramType[i])
    print(f"Set Details: {set_details}")
    print(f"Set Result : {set_result}")

    if all(res == expectedresult for res in set_result) and all(detail != "" for detail in set_details):
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Successfully set the outbound call configurations")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        set_flag = False
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to set the outbound call configurations")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return set_flag


# getLineStatus
# Syntax      : getLineStatus(obj)
# Description : Function to get the status of the line configured in asterisk server
# Parameters  : obj - module object
# Return Value : tdkTestObj - module test object
#                actualresult - actual result of the test execution
#                details - Voice Profile Line Status
def getLineStatus(obj):
    tdkTestObj = obj.createTestStep('TDKB_TR181Stub_Get')
    actualresult, details = getTR181Value(tdkTestObj, "Device.Services.VoiceService.1.VoiceProfile.1.Line.1.Status")
    return tdkTestObj, actualresult, details

# getOutboundEndpointRegistrationStatus
# Syntax      : getOutboundEndpointRegistrationStatus(obj)
# Description : Function to get the registration status of the external SIP client configured in asterisk server
# Parameters  : obj - module object
# Return Value : tdkTestObj - module test object
#                actualresult - actual result of the test execution
#                details - registration status of the external SIP client

def getOutboundEndpointRegistrationStatus(obj):
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    command = f"asterisk -x 'pjsip show registrations' | grep {outbound_client_username}"
    print(f"Command : {command}")
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print(f"Outbound Endpoint Registration Details: {details}")
    return tdkTestObj, actualresult, details