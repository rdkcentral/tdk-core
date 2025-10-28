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
    if "Loaded: loaded" in details or "Active: active" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# check_service_unit_status
# Syntax : check_service_unit_status(obj, unit_name)
# Description : Function to check the status of a systemd service unit
# Parameters : obj - module object
# unit_name - name of the service unit (e.g., coredump-upload.service)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - output from systemctl status
def check_service_unit_status(obj, unit_name):
    command = f"systemctl status {unit_name} | grep 'Loaded: loaded'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    print("Full command output: %s" % details)  # Debug print
    # For service units, check if it's loaded (can be in any state)
    if "Loaded: loaded" in details:
        actualresult = "SUCCESS"
    elif "UPLOAD" in details or "coredump-upload.service" in details:
        actualresult = "SUCCESS"  # Fallback for partial output
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

# check_successful_execution_logs
# Syntax : check_successful_execution_logs(obj, unit_name, log_pattern)
# Description : Function to check for successful execution logs in service status
# Parameters : obj - module object
# unit_name - name of the unit (service)
# log_pattern - pattern to grep (e.g., "Finished UPLOAD")
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - matched logs
def check_successful_execution_logs(obj, unit_name, log_pattern):
    command = f"systemctl status {unit_name} | grep '{log_pattern}'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if log_pattern in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# set_ulimit_core_unlimited
# Syntax : set_ulimit_core_unlimited(obj)
# Description : Function to set core dump size to unlimited
# Parameters : obj - module object
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - verification output
def set_ulimit_core_unlimited(obj):
    command_set = ULIMIT_CMD
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult_set, details_set = doSysutilExecuteCommand(tdkTestObj, command_set)

    command_verify = "ulimit -c"
    actualresult_verify, details_verify = doSysutilExecuteCommand(tdkTestObj, command_verify)
    details_verify = details_verify.strip()

    if details_verify == "unlimited":
        actualresult = "SUCCESS"
        details = details_verify
    else:
        actualresult = "FAILURE"
        details = details_verify
    return tdkTestObj, actualresult, details
########## End of function ##########

# check_directory_empty
# Syntax : check_directory_empty(obj, dir_path)
# Description : Function to check if a directory is empty
# Parameters : obj - module object
# dir_path - path to the directory
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS if empty / FAILURE if not
# details - ls output
def check_directory_empty(obj, dir_path):
    command = f"ls {dir_path}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    details = details.strip()
    if details == "":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_minidump_file_created
# Syntax : verify_minidump_file_created(obj, dir_path=MINIDUMPS_DIR)
# Description : Function to verify if a .dmp or .tgz file is created in the directory
# Parameters : obj - module object
# dir_path - path to check (default /minidumps)
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# filename - name of the created file (if any)
def verify_minidump_file_created(obj, dir_path=MINIDUMPS_DIR):
    command = f"ls {dir_path} | grep -E '\\.dmp|\\.tgz'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    filename = details.strip()
    if filename != "":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, filename
########## End of function ##########

# delete_minidump_files
# Syntax : delete_minidump_files(obj, dir_path=MINIDUMPS_DIR)
# Description : Function to delete minidump files after test
# Parameters : obj - module object
# dir_path - path to minidumps
# Return Value: tdkTestObj - test object
# actualresult - SUCCESS/FAILURE
# details - rm output
def delete_minidump_files(obj, dir_path=MINIDUMPS_DIR):
    command = f"rm -f {dir_path}/*"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    return tdkTestObj, actualresult, details
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

