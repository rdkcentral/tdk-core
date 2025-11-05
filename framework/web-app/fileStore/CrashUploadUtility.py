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
import tdklib
from time import sleep
from CrashUploadVariables import *
from tdkutility import *
import json
from tdkbVariables import *

# check_unit_status
# Syntax : check_unit_status(obj, unit_name)
# Description : Function to check the status of a systemd unit
# Parameters : obj - module object
# unit_name - name of the unit (e.g., coredump-upload.path)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - output from systemctl status
def check_unit_status(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'Loaded: loaded'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Command output: %s" % details)
    if "Loaded: loaded" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# get_service_active_state
# Syntax : get_service_active_state(obj, unit_name)
# Description : Function to get the active state of a systemd service
# Parameters : obj - module object
# unit_name - name of the service unit
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# state - full Active: line from systemctl status
def get_service_active_state(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'Active:'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, state = doSysutilExecuteCommand(tdkTestObj, command)
    print("Full active state output: %s" % state)  # Debug print
    if "Active: inactive (dead)" in state or "Active: active" in state:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, state
########## End of function ##########

# get_active_state
# Syntax : get_active_state(obj, unit_name)
# Description : Function to get the active state of a systemd unit
# Parameters : obj - module object
# unit_name - name of the unit
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# state - full Active: line from systemctl status
def get_active_state(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'Active:'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, state = doSysutilExecuteCommand(tdkTestObj, command)
    print("Full active state output: %s" % state)  # Debug print
    if "Active: active (waiting)" in state:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, state
########## End of function ##########

# check_unit_enabled
# Syntax : check_unit_enabled(obj, unit_name)
# Description : Function to check if a systemd unit is enabled
# Parameters : obj - module object
# unit_name - name of the unit
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - output from systemctl is-enabled
def check_unit_enabled(obj, unit_name):
    command = f"systemctl is-enabled {unit_name}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    details = details.strip()
    if details == "enabled":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# get_triggers
# Syntax : get_triggers(obj, unit_name)
# Description : Function to get the triggers for a path unit
# Parameters : obj - module object
# unit_name - name of the unit (path)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# triggers - extracted triggers
def get_triggers(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'Triggers:'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    triggers = ""
    if "Triggers:" in details:
        triggers = details.split("Triggers:")[1].strip()
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, triggers
########## End of function ##########

# get_triggered_by
# Syntax : get_triggered_by(obj, unit_name)
# Description : Function to get the triggered by for a service unit
# Parameters : obj - module object
# unit_name - name of the unit (service)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# triggered_by - extracted triggered by
def get_triggered_by(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'TriggeredBy:'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    triggered_by = ""
    if "TriggeredBy:" in details:
        triggered_by = details.split("TriggeredBy:")[1].strip()
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, triggered_by
########## End of function ##########

# set_ulimit_core_unlimited
# Syntax : set_ulimit_core_unlimited(obj)
# Description : Function to set core dump size to unlimited
# Parameters : obj - module object
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - verification output
# initial_value - initial ulimit value before change
def set_ulimit_core_unlimited(obj):
    # Get initial value
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    command_get_initial = "ulimit -c"
    actualresult_initial, initial_value = doSysutilExecuteCommand(tdkTestObj, command_get_initial)
    initial_value = initial_value.strip()
    print("Initial ulimit -c value: %s" % initial_value)

    command_set = ULIMIT_CMD
    actualresult_set, details_set = doSysutilExecuteCommand(tdkTestObj, command_set)

    command_verify = "ulimit -c"
    actualresult_verify, details_verify = doSysutilExecuteCommand(tdkTestObj, command_verify)
    details_verify = details_verify.strip()

    if details_verify == "unlimited":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    details = details_verify
    return tdkTestObj, actualresult, details, initial_value
########## End of function ##########

# revert_ulimit_core
# Syntax : revert_ulimit_core(obj, initial_value)
# Description : Function to revert core dump size to initial value
# Parameters : obj - module object
# initial_value - initial ulimit value to revert to
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - verification output
def revert_ulimit_core(obj, initial_value):
    command_revert = f"ulimit -c {initial_value}"
    print("Command : %s" % command_revert)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult_revert, details_revert = doSysutilExecuteCommand(tdkTestObj, command_revert)

    command_verify = "ulimit -c"
    actualresult_verify, details_verify = doSysutilExecuteCommand(tdkTestObj, command_verify)
    details_verify = details_verify.strip()

    if details_verify == initial_value:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    details = details_verify
    return tdkTestObj, actualresult, details
########## End of function ##########

# check_directory_filecount
# Syntax : check_directory_filecount(obj, dir_path)
# Description : Function to get the count of .dmp files in a directory
# Parameters : obj - module object
# dir_path - path to the directory
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# count - number of .dmp files
def check_directory_filecount(obj, dir_path):
    command = f"ls {dir_path} | grep -i .dmp | wc -l"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    count = details.strip()
    if count.isdigit():
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
        count = "0"
    return tdkTestObj, actualresult, count
########## End of function ##########

# verify_minidump_file_created
# Syntax : verify_minidump_file_created(obj, initial_count, dir_path=MINIDUMPS_DIR)
# Description : Function to verify if a .dmp file is created in the directory
# Parameters : obj - module object
# initial_count - initial count of .dmp files
# dir_path - path to check (default /minidumps)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# filename - name of the newly created file (if any)
def verify_minidump_file_created(obj, initial_count, dir_path=MINIDUMPS_DIR):
    command = f"ls {dir_path} | grep -i .dmp | wc -l"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    current_count = details.strip()

    if current_count.isdigit() and int(current_count) > int(initial_count):
        actualresult = "SUCCESS"
        # Get the filename
        command_filename = f"ls {dir_path} | grep -i .dmp"
        actualresult_fn, filename = doSysutilExecuteCommand(tdkTestObj, command_filename)
        filename = filename.strip()
    else:
        actualresult = "FAILURE"
        filename = ""

    return tdkTestObj, actualresult, filename
########## End of function ##########

# verify_process_restart
# Syntax : verify_process_restart(obj, process_name, old_pid, max_retry=6)
# Description : Function to verify if a process restarted with new PID
# Parameters : obj - module object
# process_name - name of the process
# old_pid - old PID before crash
# max_retry - maximum retry count (default 6)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# new_pid - new PID after restart
def verify_process_restart(obj, process_name, old_pid, max_retry=6):
    query = "sh %s/tdk_platform_utility.sh checkProcess %s" % (TDK_PATH, process_name)
    print("Command: %s" % query)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    tdkTestObj.addParameter("command", query)
    print("Check for every 10 secs whether the process is up")
    retryCount = 0
    new_pid = ""
    expectedresult = "SUCCESS"

    while retryCount < max_retry:
        tdkTestObj.executeTestCase("SUCCESS")
        actualresult = tdkTestObj.getResult()
        new_pid = tdkTestObj.getResultDetails().strip().replace("\\n", "")
        if expectedresult in actualresult and new_pid:
            break
        else:
            sleep(10)
            retryCount = retryCount + 1

    if not new_pid:
        print("Retry Again: Check for every 5 mins whether the process is up")
        retryCount = 0
        while retryCount < max_retry:
            tdkTestObj.executeTestCase("SUCCESS")
            actualresult = tdkTestObj.getResult()
            new_pid = tdkTestObj.getResultDetails().strip().replace("\\n", "")
            if expectedresult in actualresult and new_pid:
                break
            else:
                sleep(300)
                retryCount = retryCount + 1

    if new_pid and new_pid != old_pid:
        actualresult = "SUCCESS"
    elif new_pid == old_pid:
        actualresult = "FAILURE"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, new_pid
########## End of function ##########

# verify_log_pattern
# Syntax : verify_log_pattern(obj, log_file, pattern)
# Description : Function to grep a pattern in a log file
# Parameters : obj - module object
# log_file - path to log file
# pattern - pattern to grep
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - matched lines
def verify_log_pattern(obj, log_file, pattern):
    command = f"grep '{pattern}' {log_file}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if pattern in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########
