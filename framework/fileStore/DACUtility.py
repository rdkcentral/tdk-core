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
from DACVariables import *
from tdkutility import *
import json
from tdkbVariables import *

# check_service_status
# Syntax : check_service_status(obj, service_name)
# Description : Function to check the status of a systemd service
# Parameters : obj - module object
#              service_name - name of the service (e.g., dobby.service, dsm.service)
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - output from systemctl status
def check_service_status(obj, service_name):
    command = f"systemctl status {service_name} | grep 'Loaded: loaded'"
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

# check_service_enabled
# Syntax : check_service_enabled(obj, service_name)
# Description : Function to check if a systemd service is enabled
# Parameters : obj - module object
#              service_name - name of the service
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - output from systemctl is-enabled
def check_service_enabled(obj, service_name):
    command = f"systemctl is-enabled {service_name}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    details = details.strip()
    print("Command output: %s" % details)
    if details == EXPECTED_ENABLED_STATE:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, details
########## End of function ##########

# get_service_active_state
# Syntax : get_service_active_state(obj, service_name)
# Description : Function to get the active state of a systemd service
# Parameters : obj - module object
#              service_name - name of the service
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               state - full Active: line from systemctl status
def get_service_active_state(obj, service_name):
    command = f"systemctl status {service_name} | grep 'Active:'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, state = doSysutilExecuteCommand(tdkTestObj, command)
    print("Full active state output: %s" % state)
    if EXPECTED_ACTIVE_STATE in state:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
    return tdkTestObj, actualresult, state
########## End of function ##########

# verify_process_exists
# Syntax : verify_process_exists(obj, process_name)
# Description : Function to verify if a process is running
# Parameters : obj - module object
#              process_name - name of the process
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               pid - PID of the process
def verify_process_exists(obj, process_name):
    command = f"pidof {process_name}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    pid = details.strip()
    print("Process PID: %s" % pid)

    if pid and pid.isdigit():
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
        pid = ""
    return tdkTestObj, actualresult, pid
########## End of function ##########

# check_binary_exists
# Syntax : check_binary_exists(obj, binary_name)
# Description : Function to check if a binary exists in the system
# Parameters : obj - module object
#              binary_name - name of the binary
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               path - path to the binary
def check_binary_exists(obj, binary_name):
    command = f"command -v {binary_name}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, path = doSysutilExecuteCommand(tdkTestObj, command)
    path = path.strip()
    print("Binary path: %s" % path)

    if path and binary_name in path:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"
        path = ""

    return tdkTestObj, actualresult, path
########## End of function ##########

# create_directory
# Syntax : create_directory(obj, dir_path)
# Description : Function to create a directory
# Parameters : obj - module object
#              dir_path - path of directory to create
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def create_directory(obj, dir_path):
    command = f"mkdir -p {dir_path}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    # Verify directory was created
    verify_command = f"ls -d {dir_path}"
    actualresult_verify, details_verify = doSysutilExecuteCommand(tdkTestObj, verify_command)

    if dir_path in details_verify:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# download_file
# Syntax : download_file(obj, url, destination)
# Description : Function to download a file using wget
# Parameters : obj - module object
#              url - URL to download from
#              destination - destination directory
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def download_file(obj, url, destination):
    # Extract filename from URL
    filename = url.split('/')[-1]
    file_path = f"{destination}/{filename}"
    command = f"cd {destination} && wget {url}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    # Verify file was downloaded
    actualresult_verify, details_verify = isFilePresent(tdkTestObj, file_path)
    if actualresult_verify == "SUCCESS" and filename in details_verify:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# extract_tar_bundle
# Syntax : extract_tar_bundle(obj, tar_file, extract_dir)
# Description : Function to extract a tar.gz bundle
# Parameters : obj - module object
#              tar_file - path to tar file
#              extract_dir - directory to extract to
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def extract_tar_bundle(obj, tar_file, extract_dir):
    command = f"cd {extract_dir} && tar -xvzf {tar_file}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    # Verify extraction by checking if config.json and rootfs directory exist
    config_path = f"{extract_dir}/config.json"
    rootfs_path = f"{extract_dir}/rootfs"

    actualresult_config, details_config = isFilePresent(tdkTestObj, config_path)
    actualresult_rootfs, details_rootfs = isFilePresent(tdkTestObj, rootfs_path)
    if actualresult_config == "SUCCESS" and actualresult_rootfs == "SUCCESS":
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_bundle_structure
# Syntax : verify_bundle_structure(obj, bundle_dir, expected_files)
# Description : Function to verify OCI bundle structure
# Parameters : obj - module object
#              bundle_dir - bundle directory path
#              expected_files - list of expected files/dirs
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def verify_bundle_structure(obj, bundle_dir, expected_files):
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    all_found = True
    details = ""

    # Check each expected file/directory individually
    for expected_file in expected_files:
        file_path = f"{bundle_dir}/{expected_file}"
        actualresult_check, details_check = isFilePresent(tdkTestObj, file_path)
        details += f"{expected_file}: {details_check}\n"
        if actualresult_check != "SUCCESS":
            all_found = False
    if all_found:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details.strip()
########## End of function ##########

# start_dobby_container
# Syntax : start_dobby_container(obj, container_name, bundle_path, command_args)
# Description : Function to start a Dobby container
# Parameters : obj - module object
#              container_name - name of the container
#              bundle_path - path to OCI bundle
#              command_args - command and arguments to run in container
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def start_dobby_container(obj, container_name, bundle_path, command_args):
    command = f"DobbyTool start {container_name} {bundle_path} {command_args}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if "started" in details and container_name in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# list_dobby_containers
# Syntax : list_dobby_containers(obj)
# Description : Function to list running Dobby containers
# Parameters : obj - module object
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def list_dobby_containers(obj):
    command = "DobbyTool list"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    actualresult = "SUCCESS"

    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_container_running
# Syntax : verify_container_running(obj, container_name)
# Description : Function to verify if a container is running
# Parameters : obj - module object
#              container_name - name of the container
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def verify_container_running(obj, container_name):
    command = f"DobbyTool list | grep '{container_name}'"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if container_name in details and "running" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_multiple_containers_running
# Syntax : verify_multiple_containers_running(obj, container_names)
# Description : Function to verify if multiple containers are running
# Parameters : obj - module object
#              container_names - list of container names
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - combined status of all containers
def verify_multiple_containers_running(obj, container_names):
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    all_running = True
    details = ""
    for container_name in container_names:
        command = f"DobbyTool list | grep '{container_name}' | grep 'running'"
        print("Command : %s" % command)
        actualresult_check, details_check = doSysutilExecuteCommand(tdkTestObj, command)

        if container_name in details_check and "running" in details_check:
            details += f"{container_name}: running\n"
        else:
            details += f"{container_name}: not found or not running\n"
            all_running = False

    if all_running:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details.strip()
########## End of function ##########

# stop_dobby_container
# Syntax : stop_dobby_container(obj, container_name)
# Description : Function to stop a Dobby container
# Parameters : obj - module object
#              container_name - name of the container
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def stop_dobby_container(obj, container_name):
    command = f"DobbyTool stop {container_name}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    if "stopped" in details and container_name in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# remove_directory
# Syntax : remove_directory(obj, dir_path)
# Description : Function to remove a directory
# Parameters : obj - module object
#              dir_path - path of directory to remove
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def remove_directory(obj, dir_path):
    command = f"rm -rf {dir_path}"
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    # Verify directory was removed
    verify_command = f"ls -d {dir_path}"
    actualresult_verify, details_verify = doSysutilExecuteCommand(tdkTestObj, verify_command)
    if "No such file or directory" in details_verify or not details_verify.strip():
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_containers_removed
# Syntax : verify_containers_removed(obj, container_names)
# Description : Function to verify specific containers are no longer running
# Parameters : obj - module object
#              container_names - list of container names to verify are removed
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def verify_containers_removed(obj, container_names):
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    all_removed = True
    details = ""

    for container_name in container_names:
        command = f"DobbyTool list | grep '{container_name}'"
        print("Command : %s" % command)
        actualresult_check, details_check = doSysutilExecuteCommand(tdkTestObj, command)

        # If grep finds the container, it means it still exists
        if container_name in details_check:
            details += f"{container_name}: still present\n"
            all_removed = False
        else:
            details += f"{container_name}: removed\n"

    if all_removed:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details.strip()
########## End of function ##########

# usppa_install_bundle
# Syntax : usppa_install_bundle(obj, bundle_url)
# Description : Function to install DAC bundle via USP-PA
# Parameters : obj - module object
#              bundle_url - URL of the bundle to install
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def usppa_install_bundle(obj, bundle_url):
    command = f'UspPa -c operate "{DU_INSTALL_PARAM}(URL={bundle_url})" | grep -i "started successfully"'
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if "Started successfully" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# usppa_uninstall_bundle
# Syntax : usppa_uninstall_bundle(obj, du_param)
# Description : Function to uninstall DAC bundle via USP-PA
# Parameters : obj - module object
#              du_param - DeploymentUnit parameter (e.g., Device.SoftwareModules.DeploymentUnit.1.Uninstall)
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def usppa_uninstall_bundle(obj, du_param):
    command = f'UspPa -c operate "{du_param}()" | grep -i "started successfully"'
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)
    if "Started successfully" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# usppa_set_eu_state
# Syntax : usppa_set_eu_state(obj, eu_param, state)
# Description : Function to set ExecutionUnit state via USP-PA
# Parameters : obj - module object
#              eu_param - ExecutionUnit parameter
#              state - Requested state (Active/Idle)
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def usppa_set_eu_state(obj, eu_param, state):
    command = f'UspPa -c operate "{eu_param}(RequestedState={state})" | grep -i "completed successfully"'
    print("Command : %s" % command)
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    actualresult, details = doSysutilExecuteCommand(tdkTestObj, command)

    if "completed successfully" in details:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details
########## End of function ##########

# verify_directory_contents
# Syntax : verify_directory_contents(obj, dir_path, expected_items)
# Description : Function to verify directory contains expected items
# Parameters : obj - module object
#              dir_path - directory path
#              expected_items - list of expected files/directories
# Return Value: tdkTestObj - test object
#               actualresult - SUCCESS/FAILURE
#               details - command output
def verify_directory_contents(obj, dir_path, expected_items):
    tdkTestObj = obj.createTestStep('ExecuteCmd')
    all_found = True
    details = ""

    for item in expected_items:
        item_path = f"{dir_path}/{item}"
        actualresult_check, details_check = isFilePresent(tdkTestObj, item_path)
        details += f"{item}: {actualresult_check}\n"

        if actualresult_check != "SUCCESS":
            all_found = False

    if all_found:
        actualresult = "SUCCESS"
    else:
        actualresult = "FAILURE"

    return tdkTestObj, actualresult, details.strip()
########## End of function ##########
