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

# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import re

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Vulkan","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Vkmark_Benchmark_Score');


#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"


if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('set_prerequisites');
    tdkTestObj.executeTestCase(expectedResult);
    details = tdkTestObj.getResultDetails()

    if "SUCCESS" in details:
        print("PRE-REQUISITES SUCCESSFULLY SET")
        tdkTestObj = obj.createTestStep('execute_binary')
        #command = "while ! ls /run/westeros* 1>/dev/null 2>&1; do sleep 1; done; export XDG_RUNTIME_DIR=/run; export WAYLAND_DISPLAY=$(ls /run/westeros* | head -n1); vkmark --winsys-dir /usr/lib/vkmark/ --data-dir /usr/share/vkmark/ --winsys wayland --present-mode=fifo"
        tdkTestObj.executeTestCase(expectedResult);
        detail = tdkTestObj.getResultDetails()
        
        match = re.search(r"vkmark Score:\s*(\d+)", detail, re.IGNORECASE)

        if not detail or "error" in detail.lower() or not match:
            print ("FAILURE : Unable to obtain the Vkmark score")
            tdkTestObj.setResultStatus("FAILURE")
        else:
            score = match.group(1)
            print(f"Vkmark Score Obtained : {score}")
            tdkTestObj.setResultStatus("SUCCESS")
    else:
        print("Unable to set PRE-REQUISITES")

obj.unloadModule("Vulkan");

