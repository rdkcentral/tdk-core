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
from datetime import datetime
import re
import tdklib
from tdkbVariables import *
from tdkutility import *

# stability_execute_cmd
# Syntax      : stability_execute_cmd(obj, command)
# Description : Execute a shell command on the DUT via TDK ExecuteCmd stub
# Parameters  : obj     - sysutil module object
#             : command - shell command string to run on DUT
# Return Value: tdkTestObj - tdk test object
#             : actualresult - SUCCESS/FAILURE
#             : details - stdout/stderr from command
def stability_execute_cmd(obj, command):
    expectedresult = "SUCCESS"
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.addParameter("command", command)
    tdkTestObj.executeTestCase(expectedresult)
    actualresult = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails().strip()
    return tdkTestObj, actualresult, details
########## End of function ##########

# sanitize_tag
# Syntax      : sanitize_tag(value)
# Description : Replace characters not safe for filenames/directory names
#               with underscores so artifact paths are always valid
# Parameters  : value - raw string (e.g. failure reason)
# Return Value: sanitized string safe for use in a file/directory name
def stability_sanitize_tag(value):
    sanitized = re.sub(r'[^A-Za-z0-9._-]+', '_', value)
    return sanitized.strip('_') or "unknown"
########## End of function ##########

# collect_failure_artifacts
# Syntax      : collect_failure_artifacts(obj, stability_type, iteration, failure_reason,
#                                         upload_url, artifact_root)
# Description : On first failure of the stability test, collects the
#               device status snapshots on the DUT, bundles them
# Parameters  : obj           - sysutil module object
#             : stability_type - type of stability test
#             : iteration     - current reboot iteration number (int)
#             : failure_reason- short string describing what failed
#             : upload_url    - full HTTP URL of upload server endpoint
#             : artifact_root - directory on DUT to stage files
# Return Value: success        - True if tar created and upload command ran
#             : result         - dict with keys: summary, tar_file,
#                                artifact_dir, failed_command, details
def collect_failure_artifacts(obj, stability_type, iteration, failure_reason, upload_url, artifact_root="/tmp/tdk_stability_failures"):
    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    reason_tag  = stability_sanitize_tag(failure_reason)
    artifact_name = "%s_iter%s_%s_%s" % (stability_type,iteration, reason_tag, timestamp)
    artifact_dir  = "%s/%s" % (artifact_root.rstrip("/"), artifact_name)
    tar_file      = "%s.tar.gz" % artifact_dir
    response_file = "%s/upload_response.txt" % artifact_dir

    result = {
        "artifact_dir"  : artifact_dir,
        "tar_file"      : tar_file,
        "summary"       : "artifact collection not started",
        "failed_command": "",
        "details"       : ""
    }

    # All commands run on DUT in sequence.
    # Each step writes output to a separate named file inside artifact_dir.
    commands = [
        # --- workspace setup ---
        "rm -rf \"%s\" \"%s\""
            % (artifact_dir, tar_file),
        "mkdir -p \"%s\""
            % artifact_dir,

        # --- metadata ---
        "printf 'testcase=TS_STABILITY_MultipleReboots\\niteration=%s\\nfailure_reason=%s\\ntimestamp=%s\\n'"
        " > \"%s/metadata.txt\""
            % (iteration, reason_tag, timestamp, artifact_dir),

        # --- process snapshot ---
        "ps > \"%s/ps_snapshot.txt\" 2>&1"
            % artifact_dir,

        # --- top snapshot ---
        "top -b -n 1 > \"%s/top_snapshot.txt\" 2>&1"
            % artifact_dir,

        # --- memory statistics ---
        "cat /proc/meminfo > \"%s/memory_statistics.txt\" 2>&1"
            % artifact_dir,
        "free -h >> \"%s/memory_statistics.txt\" 2>&1"
            % artifact_dir,

        # --- cpu information ---
        "cat /proc/cpuinfo > \"%s/cpu_information.txt\" 2>&1"
            % artifact_dir,
        "uptime >> \"%s/cpu_information.txt\" 2>&1"
            % artifact_dir,

        # --- service status ---
        "(systemctl --no-pager --full status || service --status-all)"
        " > \"%s/service_status.txt\" 2>&1"
            % artifact_dir,

        # --- core dump listing ---
        "ls -al /minidumps"
        " > \"%s/core_dumps.txt\" 2>&1"
            % artifact_dir,

        # --- network state ---
        "(ifconfig -a || ip addr show) > \"%s/network_state.txt\" 2>&1"
            % artifact_dir,
        "(route -n || ip route show) >> \"%s/network_state.txt\" 2>&1"
            % artifact_dir,
        "(netstat -an || ss -an) >> \"%s/network_state.txt\" 2>&1"
            % artifact_dir,

        # --- connection tracking ---
        "(cat /proc/net/nf_conntrack || cat /proc/net/ip_conntrack || conntrack -L)"
        " > \"%s/connection_tracking.txt\" 2>&1"
            % artifact_dir,

       # --- core dump files ---
        "mkdir -p \"%s/core_dumps_dir\""
            % artifact_dir,
        "if [ -d /minidumps ]; then cp -r /minidumps/. /tmp/*_core.prog* \"%s/core_dumps_dir/\"; fi"
            % artifact_dir,

        # --- full /rdklogs/logs/ copy ---
        "if [ -d /rdklogs/logs ]; then cp -r /rdklogs/logs \"%s/rdklogs_logs\";"
        " else echo '/rdklogs/logs not present' > \"%s/rdklogs_logs_missing.txt\"; fi"
            % (artifact_dir, artifact_dir),

        # --- tar all files together ---
        "tar -czf \"%s\" -C \"%s\" %s"
            % (tar_file, artifact_root.rstrip("/"), artifact_name),

        # --- upload tar to HTTP server ---
        "curl --fail --connect-timeout 30 --max-time 600"
        " -F \"fileName=%s.tar.gz\""
        " -F \"logFile=@%s\""
        " \"%s\""
        " > \"%s\" 2>&1"
            % (artifact_name, tar_file, upload_url, response_file)
    ]

    for command in commands:
        tdkTestObj, actualresult, details = stability_execute_cmd(obj, command)
        if "SUCCESS" not in actualresult.upper():
            tdkTestObj.setResultStatus("FAILURE")
            result["summary"]        = "command failed during artifact collection"
            result["failed_command"] = command
            result["details"]        = details
            return False, result

    # Verify tar file was actually created and is non-empty
    verify_cmd = "if [ -s \"%s\" ]; then echo SUCCESS; else echo FAILURE; fi" % tar_file
    tdkTestObj, actualresult, details = stability_execute_cmd(obj, verify_cmd)
    if "SUCCESS" not in actualresult.upper() or "SUCCESS" not in details:
        tdkTestObj.setResultStatus("FAILURE")
        result["summary"] = "tar file verification failed - file missing or empty"
        result["details"] = details
        return False, result

    # Remove staging folder and tar file from device to free up /tmp space
    cleanup_cmd = "rm -rf \"%s\" \"%s\" \"%s\"" % (artifact_dir, tar_file,artifact_root.rstrip("/"))
    stability_execute_cmd(obj, cleanup_cmd)
    print("[ARTIFACT] Cleaned up staging folder and tar from device: %s" % artifact_dir)

    result["summary"] = "artifact collection and upload completed"
    return True, result
########## End of function ##########

#get_waitTime_configFile
# Syntax      : get_waitTime_configFile(obj1,step)
# Description : function to get the max wait time of process from configuration file
# Parameters  : obj1 - sysutil module tdk object
#             : step - current test step count
# Return Value: step - current test step count
#             : waiTime - max wait time for processes
#             : testFailed - flag for failed test
def get_waitTime_configFile(obj1,step):
    #Get the maximum process up wait time
    step+=1
    expectedresult = "SUCCESS"
    testFailed = False
    print(f"\nTEST STEP {step}: Get the max wait time of processes from configuration file")
    print(f"EXPECTED RESULT {step}: Should get the max wait time of processes from configuration file")
    cmd = "sh %s/tdk_utility.sh parseConfigFile MAX_PROCESSUP_WAITTIME" %TDK_PATH
    tdkTestObj,actualresult,details = stability_execute_cmd(obj1,cmd)
    if expectedresult in actualresult and details!="":
        waitTime = details.replace("\\n", "")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: wait time is {waitTime}")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        testFailed = True
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step} : Failed to get wait time")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,waitTime,testFailed

#get_interfaceList_configFile
# Syntax      : get_interfaceList_configFile(obj1,step)
# Description : function to get the interface list from configuration file
# Parameters  : obj1 - sysutil module tdk object
#             : step - current test step count
# Return Value: step - current test step count
#             : interfaceList - list of interfaces in DUT
#             : testFailed - flag for failed test
def get_interfaceList_configFile(obj1,step):
    #Get the list of interfaces
    step+=1
    expectedresult = "SUCCESS"
    testFailed = False
    print(f"\nTEST STEP {step}: Get the list of interfaces from configuration file ")
    print(f"EXPECTED RESULT {step}: Should get the list of interfaces from configuration file")
    cmd= "sh %s/tdk_utility.sh parseConfigFile INTERFACE_LIST" %TDK_PATH
    tdkTestObj,actualresult,details = stability_execute_cmd(obj1,cmd)
    if "Invalid Argument passed" not in details and details != "":
        interfaceList = details.replace("\\n", "")
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: {interfaceList}")
        #Get the result of execution
        print("[TEST EXECUTION RESULT] : SUCCESS")
        interfaceList = interfaceList.split(",")
    else:
        testFailed = True
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get interface List")
        #Get the result of execution
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,interfaceList,testFailed

#get_processList_configFile
# Syntax      : get_processList_configFile(obj1,step)
# Description : function to get the process list from configuration file
# Parameters  : obj1 - sysutil module tdk object
#             : step - current test step count
# Return Value: step - current test step count
#             : processList - list of processes
#             : testFailed - flag for failed test
def get_processList_configFile(obj1,step):
    #Get the list of processes
    step+=1
    expectedresult = "SUCCESS"
    testFailed = False
    print(f"\nTEST STEP {step}: Get the list of processes from configuration file")
    print(f"EXPECTED RESULT {step}: Should get the list of processes from configuration file")
    List = ["CCSP_PROCESS","SNMP_PROCESS","WEBPA_PROCESS","LIGHTTPD_PROCESS","DROPBEAR_PROCESS","WEBCONFIG_PROCESS","PSM_PROCESS","TELEMETRY_PROCESS","WIFI_PROCESS"]
    process_List = []
    invalidProcessConfig = False
    for item in List :
        Process= "sh %s/tdk_utility.sh parseConfigFile %s" %(TDK_PATH,item)
        tdkTestObj,actualresult,details = stability_execute_cmd(obj1,Process)
        if expectedresult in actualresult and details !="":
            getProcess = details.replace("\\n", "")
            if "Invalid Argument passed" in getProcess:
                invalidProcessConfig = True
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: Failed to get process entry for {item}")
                print("[TEST EXECUTION RESULT] : FAILURE")
                break
            getProcess=getProcess.split(",")
            process_List.append(getProcess)
        else:
            invalidProcessConfig = True
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to parse process entry for {item}")
            print("[TEST EXECUTION RESULT] : FAILURE")
            break
    processList = []
    #converting nested list to flat list
    processList = [ item for elem in process_List for item in elem]
    if not invalidProcessConfig and processList and "Invalid Argument passed" not in processList:
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: {processList}")
        #Get the result of execution
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        testFailed = True
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get the process list")
        #Get the result of execution
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,processList,testFailed

#get_device_uptime
# Syntax      : get_device_uptime(obj1,step)
# Description : function to get the device uptime
# Parameters  : obj1 - tdkbtr181 module tdk object
#             : step - current test step count
# Return Value: step - current test step count
#             : upTime - up time of the device
#             : iterationFailed - flag for failed test
#             : failureReason - reason for test failure
def get_device_uptime(obj1,step):
    failureReason = ""
    expectedresult = "SUCCESS"
    iterationFailed = False
    step+=1
    print(f"\nTEST STEP {step}: Get the Uptime of the DUT")
    print(f"EXPECTED RESULT {step}: Should get the Uptime of the DUT")
    tdkTestObj = obj1.createTestStep('TDKB_TR181Stub_Get')
    actualresult,upTime = getTR181Value(tdkTestObj,"Device.DeviceInfo.UpTime")
    if expectedresult in actualresult and upTime!="":
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: Uptime of the DUT is : {upTime}")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        iterationFailed = True
        failureReason = "uptime_fetch_failed"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get Uptime")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,upTime,iterationFailed,failureReason
########## End of function ##########

#get_status_interfaces
# Syntax      : get_status_interfaces(obj1,step,interfaceList)
# Description : function to check if all the specified list of interfaces are up
# Parameters  : obj1 - sysutil module tdk object
#             : step - current test step count
#             : processList - specified list of interfaces
# Return Value: step - current test step count
#             : iterationFailed - flag for failed test
#             : failureReason - reason for test failure
def get_status_interfaces(obj1,step,interfaceList):
    failureReason = ""
    expectedresult = "SUCCESS"
    iterationFailed = False
    for interfaceName in interfaceList:
        if "wlan" in interfaceName:
            command = "ifconfig | grep -A 1 %s | grep inet6 | awk '{ print $3 }'| tr \"\n\" \" \"" %interfaceName
        else:
            command = "ifconfig | grep -A 1 %s | grep inet | cut -f2 -d ':' | cut -f1 -d ' ' | tr \"\n\" \" \"" %interfaceName
        step+=1
        print(f"\nTEST STEP {step}: Check if {interfaceName} is up")
        print(f"EXPECTED RESULT {step}: {interfaceName} should be up")
        tdkTestObj,actualresult,details = stability_execute_cmd(obj1,command)
        if expectedresult in actualresult and details != "":
            ip = details.replace("\\n", "")
            #Set the result status of execution
            tdkTestObj.setResultStatus("SUCCESS")
            print(f"ACTUAL RESULT {step}: {interfaceName} is up with ip {ip}")
            #Get the result of execution
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            iterationFailed = True
            #Set the result status of execution
            tdkTestObj.setResultStatus("FAILURE")
            failureReason = "interface_down_%s" % interfaceName
            print(f"ACTUAL RESULT {step}: {interfaceName} is not up, details: {details}")
            #Get the result of execution
            print("[TEST EXECUTION RESULT] : FAILURE")
            break
    return step,iterationFailed,failureReason
########## End of function ##########

#get_status_processes
# Syntax      : get_status_processes(obj1,obj2,step,processList)
# Description : function to check if all the specified list of processes are up and running
# Parameters  : obj1 - sysutil module tdk object
#             : obj2 - tdkbtr181 module tdk object
#             : step - current test step count
#             : processList - specified list of processes
# Return Value: step - current test step count
#             : iterationFailed - flag for failed test
#             : failureReason - reason for test failure
def get_status_processes(obj1,obj2,step,processList):
    step += 1
    failureReason = ""
    expectedresult = "SUCCESS"
    iterationFailed = False
    print(f"\nTEST STEP {step}: Verify processes are running")
    print(f"EXPECTED RESULT {step}: The processes should be running")
    for process_name in processList:
        if process_name == "CcspHotspot":
            tdkTestObj = obj2.createTestStep('TDKB_TR181Stub_Get')
            result,hotspot_enabled = getTR181Value(tdkTestObj,"Device.DeviceInfo.X_COMCAST_COM_xfinitywifiEnable")
            if expectedresult in result and hotspot_enabled.strip().lower() != "true":
                print("ACTUAL RESULT %d: xfinitywifi is disabled, skipping CcspHotspot check" % step)
                print("[TEST EXECUTION RESULT] : SUCCESS")
                continue

        command1 = "pidof %s" %process_name
        tdkTestObj,actualresult,details = stability_execute_cmd(obj1,command1)
        if expectedresult in actualresult and details != "":
            pid = details.replace("\\n", "")
            tdkTestObj.setResultStatus("SUCCESS")
            print("Process Name : %s" %process_name)
            print("PID : %s" %pid)
            print("%s with process ID %s is running" %(process_name,pid))
            print("[TEST EXECUTION RESULT] : SUCCESS")
        else:
            iterationFailed = True
            tdkTestObj.setResultStatus("FAILURE")
            failureReason = "process_down_%s" % process_name
            print("Process Name : %s" %process_name)
            print("%s is not running" %process_name)
            print("[TEST EXECUTION RESULT] : FAILURE")
            break
    return step,iterationFailed,failureReason
########## End of function ##########

# get_cpu_usage_from_top_output
# Syntax      : get_cpu_usage_from_top_output(top_output)
# Description : Parse the Cpu(s) line from top output and return busy CPU percentage
# Parameters  : top_output - output from top command
# Return Value: cpu_usage  - usage of CPU  or -1.0 on failure
def get_cpu_usage_from_top_output(top_output):
    for line in top_output.splitlines():
        line = line.strip()
        if "Cpu(s)" not in line:
            continue

        idle_match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*id', line)
        if idle_match:
            idle_percent = float(idle_match.group(1))
            cpu_usage = 100.0 - idle_percent
            return round(cpu_usage, 1)

    return -1.0
########## End of function ##########

#get_process_status
# Syntax      : get_process_status(obj1,step,process)
# Description : Function to check status of specific process
# Parameters  : obj1 - sysutil module object
#             : step - current test step count
#             : process - specific RDKB process
# Return Value: step - test step count
#             : testFailed - flag for failure test
#             : failureReason - reason of failure
#             : pid - process id of specific RDKB process
def get_process_status(obj1,step,process):
    #Get the process id of the process
    step+=1
    testFailed = False
    expectedresult = "SUCCESS"
    failureReason = ""
    pid = 0
    print(f"\nTEST STEP {step}: Capture {process} process PID")
    print(f"EXPECTED RESULT {step}: {process} process should be running")
    tdkTestObj,actualresult,details = stability_execute_cmd(obj1,f"pidof {process}")
    if expectedresult in actualresult and details != "":
        pid = int(details.replace("\\n", ""))
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: {process} process PID is {pid}")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        testFailed = True
        failureReason = f"{process}_process_check_failed"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: {process} process is not running")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,testFailed,failureReason,pid
########## End of function ##########

#get_freeMemory
# Syntax      : get_freeMemory(obj1,step)
# Description : Function to get device free memory
# Parameters  : obj1 - sysutil module object
#             : step - current test step count
# Return Value: step - test step count
#             : testFailed - flag for failure test
#             : failureReason - reason of failure
#             : freeMemory - free memory of the device
def get_freeMemory(obj1,step):
    step+=1
    testFailed = False
    expectedresult = "SUCCESS"
    failureReason = ""
    freeMemory = 0.0
    print(f"\nTEST STEP {step}: Capture the free memory")
    print(f"EXPECTED RESULT {step}: Should get the free memory")
    tdkTestObj,actualresult,details = stability_execute_cmd(obj1,"free -m | awk '/^Mem:/ {print $4}'")
    if expectedresult in actualresult and details != "":
        freeMemory = int(details.replace("\\n", ""))
        tdkTestObj.setResultStatus("SUCCESS")
        print(f"ACTUAL RESULT {step}: free memory is {freeMemory}")
        print("[TEST EXECUTION RESULT] : SUCCESS")
    else:
        testFailed = True
        failureReason = "free_memory_fetch_failed"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get free memory")
        print("[TEST EXECUTION RESULT] : FAILURE")
    return step,testFailed,failureReason,freeMemory
########## End of function ##########

#get_device_CPUUsage
# Syntax      : get_device_CPUUsage(obj1,step)
# Description : Function to check cpuUsage of device
# Parameters  : obj1 - sysutil module object
#             : step - current test step count
# Return Value: step - test step count
#             : testFailed - flag for failure test
#             : failureReason - reason of failure
#             : cpuUsage - CPU usage of the DUT
def get_device_CPUUsage(obj1,step):
    step+=1
    testFailed = False
    expectedresult = "SUCCESS"
    failureReason = ""
    cpuUsage = -1.0
    print(f"\nTEST STEP {step}: Capture CPU usage")
    print(f"EXPECTED RESULT {step}: Should get the current CPU usage and stay below 90%")
    tdkTestObj,actualresult,details = stability_execute_cmd(obj1,"top -bn1 | grep 'Cpu(s)'")
    if expectedresult in actualresult and details != "":
        cpuUsage = get_cpu_usage_from_top_output(details)
        if cpuUsage >= 0:
            if cpuUsage <= 90:
                tdkTestObj.setResultStatus("SUCCESS")
                print(f"ACTUAL RESULT {step}: CPU usage is {cpuUsage}%")
                print("[TEST EXECUTION RESULT] : SUCCESS")
            else:
                testFailed = True
                failureReason = "cpu_spike_detected"
                tdkTestObj.setResultStatus("FAILURE")
                print(f"ACTUAL RESULT {step}: CPU usage is {cpuUsage}% which is above 90%")
                print("[TEST EXECUTION RESULT] : FAILURE")
        else:
            testFailed = True
            failureReason = "cpu_parse_failed"
            tdkTestObj.setResultStatus("FAILURE")
            print(f"ACTUAL RESULT {step}: Failed to parse CPU usage from top output: {details}")
            print("[TEST EXECUTION RESULT] : FAILURE")
    else:
        testFailed = True
        failureReason = "cpu_fetch_failed"
        tdkTestObj.setResultStatus("FAILURE")
        print(f"ACTUAL RESULT {step}: Failed to get CPU usage")
        print("[TEST EXECUTION RESULT] : FAILURE")

    return step,testFailed,failureReason,cpuUsage
########## End of function ##########
