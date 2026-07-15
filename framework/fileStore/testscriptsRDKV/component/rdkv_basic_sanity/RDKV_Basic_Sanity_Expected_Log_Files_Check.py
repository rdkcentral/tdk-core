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
import json
import ast
from rdkv_basic_sanitylib import *

LOG_DIR = "/opt/logs"
EXPECTED_LOG_FILES = ["dropbear.log", "rdk_shell.log", "version.txt", "device_details.log", "wpeframework.log", "wpa_p2p_supplicant.log", "rfcscript.log", "tr69hostif.log", "top_log.txt", "parodus.log", "lighttpd.error.log", "dcmscript.log"]

obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity", "1", standAlone=True)

# This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,"RDKV_Basic_Sanity_Expected_Log_Files_Check")

result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if expectedResult in result.upper():
    configKeyList = ["SSH_METHOD", "SSH_USERNAME", "SSH_PASSWORD"]
    configValues = {}

    tdkTestObj = obj.createTestStep("rdkv_basic_sanity_getDeviceConfig")
    tdkTestObj.addParameter("basePath", obj.realpath)
    tdkTestObj.addParameter("configKey", json.dumps(configKeyList))
    tdkTestObj.executeTestCase(expectedResult)
    configRaw = str(tdkTestObj.getResultDetails()).strip()
    try:
        configValues = ast.literal_eval(configRaw)
        failed_keys = [k for k, v in configValues.items() if "FAILURE" in str(v) or str(v).strip() == ""]
        for k, v in configValues.items():
            print("{} : {}".format(k, v))
        if failed_keys:
            for k in failed_keys:
                print("FAILURE: Failed to retrieve %s from device config" % k)
            tdkTestObj.setResultStatus("FAILURE")
            result = "FAILURE"
        else:
            print("SUCCESS: Successfully retrieved all device config values")
            tdkTestObj.setResultStatus("SUCCESS")
    except Exception as e:
        print("FAILURE: Could not parse device config response: {}".format(e))
        tdkTestObj.setResultStatus("FAILURE")
        result = "FAILURE"

    if "FAILURE" != result:
        if configValues["SSH_METHOD"] == "directSSH":
            if configValues["SSH_PASSWORD"] == "None":
                configValues["SSH_PASSWORD"] = ""

            credentials = obj.IP + "," + configValues["SSH_USERNAME"] + "," + configValues["SSH_PASSWORD"]
            tdkTestObj = obj.createTestStep("rdkv_basic_sanity_executeInDUT")

            missing_files = []
            empty_files = []

            print("\nChecking expected log files in %s\n" % LOG_DIR)
            files_arg = " ".join(EXPECTED_LOG_FILES)
            command = (
                "for file_name in %s; do "
                "file_path=\"%s/$file_name\"; "
                "if [ -s \"$file_path\" ]; then "
                "echo \"$file_name|PRESENT_NONEMPTY\"; "
                "elif [ -e \"$file_path\" ]; then "
                "echo \"$file_name|PRESENT_EMPTY\"; "
                "else "
                "echo \"$file_name|MISSING\"; "
                "fi; "
                "done"
            ) % (files_arg, LOG_DIR)

            tdkTestObj.addParameter("sshMethod", configValues["SSH_METHOD"])
            tdkTestObj.addParameter("credentials", credentials)
            tdkTestObj.addParameter("command", command)
            tdkTestObj.executeTestCase(expectedResult)

            check_output = str(tdkTestObj.getResultDetails()).strip()
            parsed_status = {}
            for line in check_output.splitlines():
                line = line.strip()
                if "|" not in line:
                    continue
                file_name, status = line.split("|", 1)
                file_name = file_name.strip()
                status = status.strip()
                if file_name in EXPECTED_LOG_FILES:
                    parsed_status[file_name] = status

            for file_name in EXPECTED_LOG_FILES:
                status = parsed_status.get(file_name, "MISSING")
                if status == "PRESENT_NONEMPTY":
                    print("%s -- PRESENT" % file_name)
                elif status == "PRESENT_EMPTY":
                    empty_files.append(file_name)
                    print("%s -- PRESENT-EMPTY" % file_name)
                elif status == "MISSING":
                    missing_files.append(file_name)
                    print("%s -- NON-PRESENT" % file_name)
                else:
                    missing_files.append(file_name)
                    print("%s -- NON-PRESENT (UNEXPECTED RESPONSE)" % file_name)

            if not missing_files and not empty_files:
                print("\nSUCCESS: All expected log files are present and non-empty.")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                if missing_files:
                    print("\nFAILURE: Missing log files: %s" % ", ".join(missing_files))
                if empty_files:
                    print("FAILURE: Empty log files: %s" % ", ".join(empty_files))
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Currently only supports directSSH ssh method")
            tdkTestObj.setResultStatus("FAILURE")

    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
