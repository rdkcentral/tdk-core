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

import time
import subprocess
from firmwareUpgradeVariables import *
from firmwareUpgradeUtility import *

# Function to wait for the device to come up after reboot, validate whether firmware got upgraded and perform revert firmware operation.
def fw_upgrade_checker(dest_ip, initial_firmware, target_firmware, fw_binary):
    # Wait till device comes up after reboot
    print("Sleeping while waiting for the device to come up")
    time.sleep(600)
    hostname = dest_ip
    upgraded_firmware = ""
    revert_flag = False
    # Get the current firmware details and check if it has been upgraded to target firmware
    try:
        command = "head -n 1 /version.txt"
        result = subprocess.run(["ssh", f"{username}@{hostname}", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        image_name = result.stdout.strip()
        upgraded_firmware= image_name.split(":",1)[1] if ':' in image_name else ""
        print(f"Current Image Name : {upgraded_firmware}")
        if upgraded_firmware == target_firmware:
            print(f"The firmware has been successfully upgraded to {upgraded_firmware}.")
        else:
            print(f"Failed to upgrade the firware to the target firmware version {target_firmware}. Current Firmware is {upgraded_firmware}")
            return revert_flag, upgraded_firmware
    except Exception as e:
        print(f"Exception {e}")

    # Revert the firmware to its initial version
    try:
        print(f"Revert the firmware to initial firmware version {initial_firmware}")
        revert_flag = True
        revert_command = f'setsid sh -c "sleep 5;{fw_binary}" > /dev/null 2>&1 &'
        print(f"Revert Command : {revert_command}")
        result = subprocess.run(["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "ConnectTimeout=10", f"{username}@{hostname}", revert_command], capture_output=True, text=True)
    except Exception as e:
        revert_flag = False
        print(f"Exception : {e}")

    #Wait till device comes up after reboot
    print("Sleeping while waiting for the device to come up")
    time.sleep(600)
    print("Returing to main code....\n")
    # Return back to the script
    return revert_flag, upgraded_firmware
