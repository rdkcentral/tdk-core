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
import socket
import time

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_Reboot_Validation');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    configKeyList = ["SSH_PORT", "SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    configValues = {}
    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_getDeviceConfig')
    for configKey in configKeyList:
        tdkTestObj.addParameter("basePath", obj.realpath)
        tdkTestObj.addParameter("configKey", configKey)
        tdkTestObj.executeTestCase(expectedResult)
        configValues[configKey] = tdkTestObj.getResultDetails()
        if "FAILURE" not in configValues[configKey] and configValues[configKey] != "":
            print("SUCCESS: Successfully retrieved %s configuration from device config file" % configKey)
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("FAILURE: Failed to retrieve %s configuration from device config file" % configKey)
            if configValues[configKey] == "":
                print("\n Please configure the %s key in the device config file" % configKey)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
            break

    if "FAILURE" != result:
        if "directSSH" == configValues["SSH_METHOD"]:
            if configValues["SSH_PASSWORD"] == "None":
                configValues["SSH_PASSWORD"] = ""
            credentials = obj.IP + ',' + configValues["SSH_USERNAME"] + ',' + configValues["SSH_PASSWORD"]
            ssh_port = int(configValues["SSH_PORT"])

            # Step 1: Reboot the DUT
            tdkTestObj = obj.createTestStep('rdkv_basic_sanity_rebootexecution')
            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"])
            tdkTestObj.addParameter("credentials", credentials)
            tdkTestObj.addParameter("command", "reboot")
            tdkTestObj.executeTestCase(expectedResult)
            print("INFO: Reboot command sent to DUT")
            tdkTestObj.setResultStatus("SUCCESS")
            reboot_start_time = time.time()

            # Step 2: Verify SSH port is not accessible (device is rebooting)
            WAIT_FOR_DOWN = 10
            CHECK_INTERVAL = 2
            port_down = False
            print("INFO: Waiting for SSH port to go down (max {}s)...".format(WAIT_FOR_DOWN))
            for _ in range(WAIT_FOR_DOWN // CHECK_INTERVAL):
                time.sleep(CHECK_INTERVAL)
                try:
                    s = socket.create_connection((obj.IP, ssh_port), timeout=3)
                    s.close()
                except Exception:
                    port_down = True
                    print("INFO: SSH port is not accessible - device is rebooting")
                    break

            if not port_down:
                print("FAILURE: SSH port still accessible after {}s - device may not have rebooted".format(WAIT_FOR_DOWN))
                tdkTestObj.setResultStatus("FAILURE")
                result = "FAILURE"
            else:
                tdkTestObj.setResultStatus("SUCCESS")

            if "FAILURE" != result:
                # Step 3: Wait for SSH port to come back up, then attempt uptime at each check
                WAIT_FOR_UP = 180
                STABLE_INTERVAL = 3
                print("INFO: Waiting for SSH port to come back up and stabilise (max {}s)...".format(WAIT_FOR_UP))
                port_up = False
                uptime_mins = None
                first_seen_elapsed = None
                deadline = time.time() + WAIT_FOR_UP
                while time.time() < deadline:
                    time.sleep(CHECK_INTERVAL)
                    try:
                        s = socket.create_connection((obj.IP, ssh_port), timeout=3)
                        s.close()
                        elapsed = time.time() - reboot_start_time
                        if first_seen_elapsed is None:
                            first_seen_elapsed = elapsed
                            print("INFO: SSH port first seen up - at {:.0f} seconds, executing uptime command".format(elapsed))
                        else:
                            print("INFO: Going for stability check - at {:.0f} seconds, executing uptime command".format(elapsed))

                        # Attempt uptime command via SSH
                        uptime_obj = obj.createTestStep('rdkv_basic_sanity_executeInDUT')
                        uptime_obj.addParameter("sshMethod", configValues["SSH_METHOD"])
                        uptime_obj.addParameter("sshPort", configValues["SSH_PORT"])
                        uptime_obj.addParameter("credentials", credentials)
                        uptime_obj.addParameter("command", "awk '{print int($1/60)}' /proc/uptime")
                        uptime_obj.executeTestCase(expectedResult)
                        uptime_result = uptime_obj.getResult()
                        uptime_output = str(uptime_obj.getResultDetails()).strip()
                        last_line = uptime_output.splitlines()[-1].strip() if uptime_output else ""

                        if expectedResult in uptime_result.upper() and last_line.isdigit():
                            uptime_mins = int(last_line)
                            reboot_elapsed = elapsed
                            print("INFO: Uptime command succeeded - got uptime: {} minute(s)".format(uptime_mins))
                            print("INFO: SSH port is stable - device is back online")
                            print("INFO: Device reboot time: {:.1f} seconds".format(reboot_elapsed))
                            port_up = True
                            break
                        else:
                            print("INFO: Uptime command not ready yet, retrying in {}s...".format(STABLE_INTERVAL))
                            time.sleep(STABLE_INTERVAL)
                    except Exception:
                        pass

                if not port_up:
                    print("FAILURE: Device did not come back online within {}s".format(WAIT_FOR_UP))
                    tdkTestObj.setResultStatus("FAILURE")
                else:
                    # Step 4: Validate uptime
                    if uptime_mins < 5:
                        print("SUCCESS: Uptime is {} min - device has freshly rebooted".format(uptime_mins))
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE: Uptime is {} min - expected < 5 min after reboot".format(uptime_mins))
                        tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: Failed to get SSH configuration values")
        tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
