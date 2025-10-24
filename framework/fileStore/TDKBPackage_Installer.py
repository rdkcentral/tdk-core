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
#

import time
import subprocess
from firmwareUpgradeVariables import *
from firmwareUpgradeUtility import *

# Function to wait for the device to come up after reboot and then SCP the TDK packages and execute the installation script to enable TDK if not already enabled
def package_installer(dest_ip):
    # Wait till device comes up after reboot
    print("Sleeping while waiting for the device to come up")
    time.sleep(300)
    hostname = dest_ip
    #Check whether the upgraded image is TDK enabled
    try:
        command = "head -n 1 /version.txt"
        result = subprocess.run(["ssh", f"{username}@{hostname}", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        image_name = result.stdout.strip()
        if "TDK" in image_name:
            print("The firmware upgraded is already a TDK-B Image. No need to install TDK-B package")
            return
        else:
            print("The current firmware is not a TDK-B Image. Proceeding with TDK-B package installation")
    except Exception as e:
        print(f"Exception {e}")
        print("Proceeding with TDK-B package installation")

    # After device is up, SCP the TDK packages to the device if TDK service is not enabled
    try:
        print("Starting file transfer")
        sourcefile = f"{source_path}/{install_script} {source_path}/{tdk_package}"
        print(f"Source file: {sourcefile}")
        scp_command = 'scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '+ sourcefile + ' ' + username + '@' + dest_ip + ':' + dest_path
        print(f"SCP command: {scp_command}")
        p = subprocess.Popen(scp_command, shell=True)
        sts = p.wait()
        print(f"file {sourcefile} copied to the device")
    except Exception as error:
        print("Failed to copy files to device")
        print(error)

    # Execute the TDK Installation script in the device after accessing it via ssh
    try:
        print("Start installation")
        command = f"cd / && sh {dest_path}/{install_script} {dest_path}/{tdk_package}"
        print(f"Run Command : {command}")
        result = subprocess.run(["ssh", f"{username}@{hostname}", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Completed installation")
    except Exception as e:
        print(f"Exception {e}")

    #Wait till device comes up after reboot
    print("Sleeping while waiting for the device to come up")
    time.sleep(300)

    # Return back to the script
    return

if __name__ == "__main__":
    package_installer()
