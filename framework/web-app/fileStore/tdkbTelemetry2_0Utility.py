#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
from tdkbVariables import *;
from time import sleep;
from tdkbTelemetry2_0_Variables import *
from datetime import datetime, timezone
import json
import base64
import msgpack
from tdkutility import *

#################################################################################
# A utility function to get the telemetry2_0 parameter values
#
# Syntax       : getinitialTelemetry2_0Values(tdkTestObj,telStatus,version,URL)
# Parameter    : tdkTestObj
# Return Value : return the status,initial enable Status,Version and URL
#################################################################################
def getinitialTelemetry2_0Values(tdkTestObj):
    expectedresult="SUCCESS";
    getStatus = 0;
    defaultTelstatus = " ";
    defURL = " " ;
    defVersion = " ";
    tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Enable");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    defaultTelstatus  = tdkTestObj.getResultDetails();
    if expectedresult in actualresult :
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print("Telemetry Enable status is:",defaultTelstatus);
        tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version");
        #Execute testcase on DUT
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        defVersion= tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print("Telemetry Version  is:",defVersion);
            tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL");
            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            defURL = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                getStatus = 1;
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print("Telemetry config URL  ",defURL);
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print("Failed to get Telemetry config URL")
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print(" Failed to Get the Telemetry Version");
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print("Failed to get Telemetry Enable status");
    return getStatus,defaultTelstatus,defURL,defVersion;
#################################################################################
# A utility function to set the telemetry2_0 parameter values
#
# Syntax       : setTelemetry2_0Values(tdkTestObj,telStatus,version,URL)
# Parameter    : tdkTestObj,telStatus,version,URL
# Return Value : return the status
#################################################################################
def setTelemetry2_0Values(tdkTestObj,telStatus,version,URL):
    setStatus = 0;
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Enable");
    tdkTestObj.addParameter("ParamValue",telStatus);
    tdkTestObj.addParameter("Type","bool");
    #Execute the test case in DUT
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails();
    if expectedresult in actualresult:
        #Set the result status of execution
        tdkTestObj.setResultStatus("SUCCESS");
        print("Telemetry Enable status is:",details)
        tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.Version");
        tdkTestObj.addParameter("ParamValue",version);
        tdkTestObj.addParameter("Type","string");
        #Execute the test case in DUT
        tdkTestObj.executeTestCase(expectedresult);
        actualresult = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails();
        if expectedresult in actualresult:
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS");
            print("Telemetry Version set status is:",details)
            tdkTestObj.addParameter("ParamName","Device.DeviceInfo.X_RDKCENTRAL-COM_RFC.Feature.Telemetry.ConfigURL");
            tdkTestObj.addParameter("ParamValue",URL);
            tdkTestObj.addParameter("Type","string");
            #Execute the test case in DUT
            tdkTestObj.executeTestCase(expectedresult);
            actualresult = tdkTestObj.getResult();
            details = tdkTestObj.getResultDetails();
            if expectedresult in actualresult:
                setStatus = 1;
                #Set the result status of execution
                tdkTestObj.setResultStatus("SUCCESS");
                print("Telemetry ConfigURL is",details);
            else:
                #Set the result status of execution
                tdkTestObj.setResultStatus("FAILURE");
                print("Failed to set the Telemetry ConfigURL");
        else:
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE");
            print("Failed to set the Telemetry Version");
    else:
        #Set the result status of execution
        tdkTestObj.setResultStatus("FAILURE");
        print("Failed to set the Telemetry Enable status");
    return  setStatus;
#################################################################################
# A utility function to get the PID value of the given process
#
# Syntax       : getPID(tdkTestObj,ps_name)
# Parameter    : tdkTestObj, process Name
# Return Value : return the status and PID value
#################################################################################
def getPID(tdkTestObj,ps_name):
    status = 1;
    cmd = "pidof %s" %ps_name;
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    return details,actualresult;
#################################################################################
# A utility function to Enable the Telemetry Debug Logs
#
# Syntax       : enableTelemetryDebugLogs(tdkTestObj)
# Parameter    : tdkTestObj
# Return Value : return the result and details
#################################################################################
def enableTelemetryDebugLogs(tdkTestObj):
    status =1;
    cmd = "touch /nvram/enable_t2_debug";
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    return actualresult,details;
#################################################################################
# A utility function to check Pre-requisite for Telemetry2_0
#
# Syntax       : telemetry2_0_Prerequisite(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set)
# Parameter    : sysObj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set
# Return Value : return the status,Revert Flag, initial Status,initial Version and initial URL
#################################################################################
def telemetry2_0_Prerequisite(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_Get,tdkTestObj_Tr181_set):
    SetURL = TEL_CONFIG_URL ;
    expectedresult = "SUCCESS"
    preReq_Status = 0;
    revertFlag = 0;
    paramSet = 0;
    initialStatus = "";
    initialVersion = "";
    initialURL = "";
    enableRes,enableDetails = enableTelemetryDebugLogs(tdkTestObj_Sys_ExeCmd);
    if expectedresult in enableRes:
        tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
        print("TEST STEP : Enable the Telemetry Debug logs");
        print("EXPECTED RESULT : Should Enable the Telemetry Debug logs");
        print("ACTUAL RESULT : Telemetry Debug logs was Enabled");
        print("[TEST EXECUTION RESULT] : SUCCESS")
        pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");
        if expectedresult in pidresult:
            tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
            print("TEST STEP : Get the PID value of Telemetry2_0 Process");
            print("EXPECTED RESULT : Should get the PID value of Telemetry Process");
            print("ACTUAL RESULT : Telemetry PID value was retrieved Successfully");
            print("[TEST EXECUTION RESULT] : SUCCESS")
            if pid != "":
                preReq_Status = 1;
                print("telemetry2_0 Process is already Running, PID is ",pid)
            else:
                print("telemetry2_0 Process is not running in initial stage")
                getResult,initialStatus,initialURL,initialVersion = getinitialTelemetry2_0Values(tdkTestObj_Tr181_Get);
                if getResult == 1:
                    tdkTestObj_Tr181_Get.setResultStatus("SUCCESS");
                    print("TEST STEP : Get the values of Telemetry2_0 Enable,Version and ConfigURL value");
                    print("EXPECTED RESULT : Should get the values of Telemetry2_0 Enable,Version and ConfigURL");
                    print("ACTUAL RESULT : Telemetry2_0 Enable,Version and ConfigURL values retrieved Successfully");
                    print("[TEST EXECUTION RESULT] : SUCCESS")
                    if initialStatus == "true" and initialVersion == 2 and initialURL == SetURL:
                        paramSet = 1;
                    else:
                        setResult = setTelemetry2_0Values(tdkTestObj_Tr181_set,"true","2",SetURL);
                        if setResult == 1:
                            revertFlag = 1;
                            tdkTestObj_Tr181_set.setResultStatus("SUCCESS");
                            print("TEST STEP : Set the values of Telemetry2_0 Enable,Version and ConfigURL value");
                            print("EXPECTED RESULT : Set operation of Telemetry2_0 Enable,Version and ConfigURL should Success");
                            print("ACTUAL RESULT : Successfully set the values of Telemetry2_0 Enable,Version and ConfigURL");
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            paramSet = 1;
                        else:
                            paramSet = 0;
                            tdkTestObj_Tr181_set.setResultStatus("FAILURE");
                            print("TEST STEP : Set the values of Telemetry2_0 Enable,Version and ConfigURL value");
                            print("EXPECTED RESULT : Set operation of Telemetry2_0 Enable,Version and ConfigURL should Success");
                            print("ACTUAL RESULT : Failed to set the values of Telemetry2_0 Enable,Version and ConfigURL");
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    if paramSet == 1:
                        print("******************************************************")
                        print("Initiating Reboot Please wait till the device comes up");
                        print("*******************************************************")
                        sysobj .initiateReboot();
                        sleep(300);
                        pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");
                        if expectedresult in pidresult and pid != "":
                            tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
                            print("TEST STEP : Get the PID value of Telemetry2_0 to make sure process is running");
                            print("EXPECTED RESULT : telemetry2_0 process should be running");
                            print("ACTUAL RESULT : telemetry2_0 process is running after reboot, PID is",pid);
                            print("[TEST EXECUTION RESULT] : SUCCESS")
                            preReq_Status = 1;
                        else:
                            tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
                            print("TEST STEP : Get the PID value of Telemetry2_0 to make sure process is running");
                            print("EXPECTED RESULT : telemetry2_0 process should be running");
                            print("ACTUAL RESULT : telemetry2_0 process is NOT running after reboot");
                            print("[TEST EXECUTION RESULT] : FAILURE")
                    else:
                        tdkTestObj_Tr181_set.setResultStatus("FAILURE");
                        print("Parameters set operation was Failed")
                else:
                    tdkTestObj_Tr181_Get.setResultStatus("FAILURE");
                    print("TEST STEP : Get the values of Telemetry2_0 Enable,Version and ConfigURL value");
                    print("EXPECTED RESULT : Should get the values of Telemetry2_0 Enable,Version and ConfigURL");
                    print("ACTUAL RESULT : Failed to get Telemetry2_0 Enable,Version and ConfigURL values");
                    print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
            print("TEST STEP : Get the PID value of Telemetry2_0 Process");
            print("EXPECTED RESULT : Should get the PID value of Telemetry Process");
            print("ACTUAL RESULT : Failed to get the Telemetry PID value");
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
        print("TEST STEP : Enable the Telemetry Debug logs");
        print("EXPECTED RESULT : Should Enable the Telemetry Debug logs");
        print("ACTUAL RESULT : Failed to Enable Telemetry Debug logs");
        print("[TEST EXECUTION RESULT] : FAILURE")
    return preReq_Status,revertFlag,initialStatus,initialVersion,initialURL;
#################################################################################
# A utility function to run after all simulations on Telemetry2_0
#
# Syntax       : telemetry2_0_PostProcess(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL)
# Parameter    : sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL
# Return Value : return the status
#################################################################################
def telemetry2_0_PostProcess(sysobj,tdkTestObj_Sys_ExeCmd,tdkTestObj_Tr181_set,revertFlag,initialStatus,initialVersion,initialURL):
    postprocess_Status = 0;
    if revertFlag == 1:
        print("Revert Flag was SET, Initiating Revert operations")
        revertResult = setTelemetry2_0Values(tdkTestObj_Tr181_set,initialStatus,initialVersion,initialURL);
        if revertResult == 1:
            tdkTestObj_Tr181_set.setResultStatus("SUCCESS");
            print("TEST STEP : Revert the Telemetry parameters");
            print("EXPECTED RESULT : Telemetry parameters should be reverted ");
            print("ACTUAL RESULT : Revert operation was success");
            print("[TEST EXECUTION RESULT] : SUCCESS")
            print("******************************************************")
            print("Initiating Reboot Please wait till the device comes up");
            print("*******************************************************")
            sysobj .initiateReboot();
            sleep(300);
            pid,pidresult = getPID(tdkTestObj_Sys_ExeCmd,"telemetry2_0");
            if expectedresult in pidresult and pid == "":
                postprocess_Status = 1;
                tdkTestObj_Sys_ExeCmd.setResultStatus("SUCCESS");
                print("TEST STEP : Get the PID value of telemetry2_0");
                print("EXPECTED RESULT : Telemetry process shouldnt be running");
                print("ACTUAL RESULT : telemetry2_0 Process is NOT Running After Reboot");
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj_Sys_ExeCmd.setResultStatus("FAILURE");
                print("TEST STEP : Get the PID value of telemetry2_0");
                print("EXPECTED RESULT : Telemetry process Should not be running");
                print("ACTUAL RESULT : telemetry2_0 Process is  Running After Reboot");
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj_Tr181_set.setResultStatus("FAILURE");
            print("TEST STEP : Revert the Telemetry parameters");
            print("EXPECTED RESULT : Telemetry parameters should be reverted ");
            print("ACTUAL RESULT : Revert operation was Failed");
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        postprocess_Status = 1;
        print("Revert Flag is not set, no need for Revert Operation")
    return postprocess_Status;
#################################################################################
# A utility function to get the number of lines from the Telemetry Log File
#
# Syntax       : getTelLogFileTotalLinesCount(tdkTestObj)
# Parameter    : tdkTestObj
# Return Value : return the number of lines
#################################################################################
def getTelLogFileTotalLinesCount(tdkTestObj):
    cmd = "cat /rdklogs/logs/telemetry2_0.txt.0 | wc -l";
    expectedresult="SUCCESS";
    tdkTestObj.addParameter("command",cmd);
    tdkTestObj.executeTestCase(expectedresult);
    actualresult = tdkTestObj.getResult();
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "");
    linecount = int(details);
    return actualresult,linecount;
#################################################################################
# A utility function to Kill the running proccess
#
# Syntax       : killProcess(tdkTestObj_Sys_ExeCmd,pid,scriptName)
# Parameter    : tdkTestObj_Sys_ExeCmd,pid,scriptname
# Return Value : return the actualresult
################################################################################
def killProcess(tdkTestObj_Sys_ExeCmd,pid,scriptname):
    expectedresult="SUCCESS";
    if scriptname !="":
        cmd = "kill %d ;sh %s &" %(pid,scriptname);
        tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
        tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
        actualresult = tdkTestObj_Sys_ExeCmd.getResult();
        details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    else:
        cmd = "kill %d " %pid;
        tdkTestObj_Sys_ExeCmd.addParameter("command",cmd);
        tdkTestObj_Sys_ExeCmd.executeTestCase(expectedresult);
        actualresult = tdkTestObj_Sys_ExeCmd.getResult();
        details = tdkTestObj_Sys_ExeCmd.getResultDetails().strip().replace("\\n", "");
    return actualresult;
#################################################################################
# A utility function to Check if process restarted
#
# Syntax       : checkProcessRestarted(tdkTestObj_Sys_ExeCmd,processname)
# Parameter    : tdkTestObj_Sys_ExeCmd,processname
# Return Value : return the actualresult,pid
################################################################################
def checkProcessRestarted(tdkTestObj_Sys_ExeCmd,processname):
    print("Check for every 10 secs whether the process is up")
    retryCount = 0;
    MAX_RETRY =5 ;
    expectedresult="SUCCESS";
    while retryCount < MAX_RETRY:
        pid,actualresult = getPID(tdkTestObj_Sys_ExeCmd,processname);
        if expectedresult in actualresult and pid != "":
            break;
        else:
            sleep(10);
            retryCount = retryCount + 1;
    if pid == "":
        print("Retry Again: Check for every 5 mins whether the process is up")
        retryCount = 0;
        while retryCount < MAX_RETRY:
            pid,actualresult = getPID(tdkTestObj_Sys_ExeCmd,processname);
            if expectedresult in actualresult and pid != "":
                break;
            else:
                sleep(300);
                retryCount = retryCount + 1;
    return  actualresult,pid;

################################################################################
# A utility function to create Report Profiles json body
#
# Syntax       : createReportProfilesJSON(numProfiles,profileType,scenario)
# Parameter    : numProfiles,profileType,scenario
# Return Value : return the JSON body with requested number of profiles
################################################################################
def createReportProfilesJSON(numProfiles, profileType, scenario = "default"):
    # Base parameters
    base_params_wifi = [
        {"type": "dataModel", "reference": "Profile.Name"},
        {"type": "dataModel", "reference": "Device.WiFi.Radio.1.Stats.X_COMCAST-COM_NoiseFloor"},
    ]

    base_params_selfheal = [
        {"type": "dataModel", "reference": "Profile.Name"},
        {"type": "dataModel", "name": "UPTIME", "reference": "Device.DeviceInfo.UpTime", "use": "absolute"},
    ]

    #Attach time stamp to profilename to avoid conflict
    time_stamp =  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    #Reporting Interval and Activation TimeOut
    reporting_interval = REPORTING_INTERVAL
    activation_timeout = ACTIVATION_TIMEOUT
    t2_upload_url = TELEMETRY_UPLOAD_URL
    profiles_out = []


    if scenario == "invalid_interval":
        #Negative reporting interval
        reporting_interval = -10
    elif scenario == "invalid_timeout":
        #Activation timeout less than reporting interval
        reporting_interval = 90
        activation_timeout = 60
    elif scenario == "invalid_upload_url":
        #Invalid upload URL
        t2_upload_url = "http://dummy_url.com/upload"
    elif scenario == "invalid_msgpack":
        #Returning JSON body without mandatory fields for MsgPack
        profiles_out = {"profiles": [{"name": "Invalid_JSON"}]}
        return profiles_out


    # Profile specifications
    profiles_spec = [
        {
            "name": f"WiFi_{profileType}_{time_stamp}" if numProfiles == 1 else f"WiFi_{profileType}_{time_stamp}",
            "description": "WiFi Report" if numProfiles == 1 else "WiFi Report",
            "version": "1",
            "url": t2_upload_url,
            "params": base_params_wifi
        }
    ]
    # Add SelfHeal profile if numProfiles is 2
    if numProfiles == 2:
        profiles_spec.append({
            "name": f"SelfHeal_{profileType}_{time_stamp}",
            "description": "SelfHeal Report",
            "version": "2",
            "url": t2_upload_url,
            "params": base_params_selfheal
        })

    # Generate profiles
    for idx, spec in enumerate(profiles_spec, start=1):
        profile_entry = {
            "name": spec["name"],
            "hash": f"hash{idx}",
            "value": {
                "Protocol": "HTTP",
                "EncodingType": "JSON",
                "ReportingInterval": reporting_interval,
                "TimeReference": time_stamp,
                "ActivationTimeOut": activation_timeout,
                "HTTP": {
                    "URL": spec["url"],
                    "Compression": "None",
                    "Method": "POST",
                    "RequestURIParameter": [
                        {"Name": "deviceId", "Reference": "Device.DeviceInfo.X_COMCAST-COM_CM_MAC"},
                        {"Name": "reportName", "Reference": "Profile.Name"}
                    ]
                },
                "JSONEncoding": {"ReportFormat": "NameValuePair", "ReportTimestamp": "None"},
                "Name": spec["name"],
                "Description": spec["description"],
                "Version": spec["version"],
                "Parameter": spec["params"]
            }
        }
        profiles_out.append(profile_entry)
    return {"profiles": profiles_out}

################################################################################
# A utility function to convert JSON body to Base64 encoded string
#
# Syntax       : JsontoMsgPackBase64(jsonBody)
# Parameter    : jsonBody
# Return Value : return the Base64 encoded msgpack string
################################################################################
def JsontoMsgPackBase64(jsonBody):
    msgpack_bytes = msgpack.packb(jsonBody)
    base64_str = base64.b64encode(msgpack_bytes).decode()
    return base64_str

################################################################################
# A utility function to check if the Report Profile files are created in /nvram/.t2reportprofiles/
#
# Syntax       : isProfileFileExist(tdktestObj,profile_names)
# Parameter    : tdktestObj,profile_names
# Return Value : return True if all profiles exist, False otherwise
################################################################################
def isProfileFileExist(tdktestObj, profile_names):
    profile_check = True
    expectedresult = "SUCCESS"
    for profile in profile_names:
        file_path = f"/nvram/.t2reportprofiles/{profile}"
        actualresult, details = isFilePresent(tdktestObj, file_path)
        if expectedresult in actualresult and profile in details:
            print(f"Profile {profile} is created in /nvram/.t2reportprofiles/")
        else:
            print(f"Profile {profile} is NOT created in /nvram/.t2reportprofiles/")
            profile_check = False
    return profile_check

################################################################################
# A utility function to Set and Validate Report Profiles
#
# Syntax       : SetReportProfiles(wifiobj,profileValue,profileType,numProfiles,step)
# Parameter    : wifiobj,profileValue,profileType,numProfiles,step
# Return Value : return flag - success/failure status, initial_report_profiles, param_name, step
################################################################################
def SetReportProfiles(wifiobj, profileValue, profileType, numProfiles, step):

    expectedresult = "SUCCESS"
    flag = 0
    initial_report_profiles = ""
    set_report_profiles = ""

    #Determine parameter name based on profile type
    if profileType == "JSON":
        param_name = "Device.X_RDKCENTRAL-COM_T2.ReportProfiles"
    elif profileType == "MsgPack":
        param_name = "Device.X_RDKCENTRAL-COM_T2.ReportProfilesMsgPack"

    #Determine profile mode based on number of profiles
    profileMode = "single profile" if numProfiles == 1 else "multiple profiles"

    #Get initial value of DM
    print(f"\nTEST STEP {step}: Get the initial value of {param_name}")
    print(f"EXPECTED RESULT {step}: Should get the initial value of {param_name}")
    tdkTestObj = wifiobj.createTestStep("WIFIAgent_Get_LargeValue")
    tdkTestObj.addParameter("ParamName",param_name)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
    initial_report_profiles = extract_report_profile(details, profileType)
    if expectedresult in actualresult:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Successfully got the initial value of {param_name}. Details : {initial_report_profiles}")
        print("[TEST EXECUTION RESULT] : SUCCESS")

        #Set DM with profile value
        step += 1
        print(f"\nTEST STEP {step}: Set {param_name} with {profileMode} in {profileType} Format")
        print(f"EXPECTED RESULT {step}: Should set {param_name} with {profileMode} in {profileType} Format")
        print(f"Report Profiles body to be set : {profileValue}")
        tdkTestObj = wifiobj.createTestStep('WIFIAgent_Set_LargeValue')
        tdkTestObj.addParameter("ParamName",param_name)
        tdkTestObj.addParameter("ParamValue",profileValue)
        tdkTestObj.addParameter("ParamType","string")
        tdkTestObj.executeTestCase(expectedresult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
        if expectedresult in actualresult and "success" in details.lower():
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: Successfully set {param_name} with {profileMode} in {profileType} Format. Details : {details}")
            print("[TEST EXECUTION RESULT] : SUCCESS")

            # Validate the set value
            step += 1
            print(f"\nTEST STEP {step}: Validate the set value of {param_name}")
            print(f"EXPECTED RESULT {step}: Should get the set value of {param_name}")
            tdkTestObj = wifiobj.createTestStep("WIFIAgent_Get_LargeValue")
            tdkTestObj.addParameter("ParamName",param_name)
            tdkTestObj.executeTestCase(expectedresult)
            actualresult = tdkTestObj.getResult()
            details = tdkTestObj.getResultDetails().strip().replace("\\n", "")
            set_report_profiles = extract_report_profile(details, profileType)
            if expectedresult in actualresult and profileValue == set_report_profiles:
                flag = 1
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: Successfully validated the set value of {param_name}. Details : {set_report_profiles}")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to validate the set value of {param_name}. Details : {set_report_profiles}")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to set {param_name} with {profileMode} in {profileType} Format. Details : {details}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get the initial value of {param_name}. Details : {details}")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return flag, initial_report_profiles, param_name, step

################################################################################
# A utility function to check if the cJSON report is generated in telemetry2.0 logs
#
# Syntax       : checkReportGenerated(tdktestObj,profile_names)
# Parameter    : tdktestObj,profile_names
# Return Value : log_check - True[all reports generated]/False[any not generated], details
################################################################################
def checkReportGenerated(tdktestObj, profile_names):
    log_check = True
    for profile in profile_names:
        cmd = f"grep -i '{profile}' /rdklogs/logs/telemetry2_0.txt.0 | grep -i 'cJSON'"
        print(f"Command : {cmd}")
        expectedresult = "SUCCESS"
        actualresult, details = doSysutilExecuteCommand(tdktestObj, cmd)
        print(f"Command Output: {details}")
        if expectedresult in actualresult and profile in details:
            print(f"cJSON report for profile {profile} is generated in the telemetry2.0 logs")
        else:
            print(f"cJSON report for profile {profile} is NOT generated in the telemetry2.0 logs")
            log_check = False
    return log_check, details

################################################################################
# A utility function to check if the Report is uploaded successfully
#
# Syntax       : checkReportUpload(tdktestObj,profile_names)
# Parameter    : tdktestObj,profile_names
# Return Value : upload_check - True if reports are uploaded successfully, False otherwise
################################################################################
def checkReportUpload(tdktestObj, profile_names):
    cmd = f"grep -i 'Report Sent Successfully over HTTP : 200' /rdklogs/logs/telemetry2_0.txt.0 | wc -l"
    print(f"Command : {cmd}")
    expectedresult = "SUCCESS"
    actualresult, details = doSysutilExecuteCommand(tdktestObj, cmd)
    if expectedresult in actualresult and int(details) >= len(profile_names):
        upload_check = True
    else:
        upload_check = False
    return upload_check

#################################################################################
# A utility function to extract report profile value from the response details
#
# Syntax       : extract_report_profile(details, profileType)
# Parameter    : details, profileType
# Return Value : report_profiles - the report profile value
#################################################################################
def extract_report_profile(details, profileType):
    report_profiles = ""
    before, separator, after = details.partition(' VALUE:')
    if separator:  # ' VALUE:' found
        value, _, _ = after.partition(' TYPE:')
        if profileType == "JSON":
            report_profiles = value.replace('\\"', '"').strip()
        else:
            report_profiles = value.strip()
    else:
        print(f"VALUE: not found in the response. Details : {details}")
    return report_profiles