#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
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

import time;
import deepsleephallib;

def setDeepSleep (obj):
    try:
        expectedResult = "SUCCESS";
        print("\nTEST STEP1 : Set deep sleep for 60 seconds using PLAT_DS_SetDeepSleep API")
        print("EXPECTED RESULT : Should set the deep sleep & cpu should be freezed for given timeout duration")
        timeout = 60;
        print("Timeout for deep sleep : %d (secs)" %(timeout))
        tdkTestObj = obj.createTestStep('DeepSleepHal_SetDeepSleep');
        tdkTestObj.addParameter("timeout", timeout);
        tdkTestObj.addParameter("networkStandby", False);
        tdkTestObj.executeTestCase(expectedResult);
        actualResult = tdkTestObj.getResult();
        if expectedResult in actualResult:
            tdkTestObj.setResultStatus("SUCCESS");
            details = tdkTestObj.getResultDetails();
            if "GPIOWakeup" in str(details):
                freezeDuration = int(str(details).split(";")[0].split(":")[1].strip())
                GPIOWakeup = int(str(details).split(";")[1].split(":")[1].strip())
                print("Value Returned : %s secs (approx), %s" %(str(details).split(";")[0],str(details).split(";")[1]))
                print("ACTUAL RESULT  : %s" %(str(details).split(";")[2]))
                print("[TEST EXECUTION RESULT] : SUCCESS\n")

                print("\nTEST STEP2: Check CPU freeze duration & GPIO Wakeup status and reboot the device")
                print("EXPECTED RESULT : Reboot if freeze duration is >= timeout & GPIO Wakeup status should be 0")
                if int(freezeDuration) >= int(timeout) and int(GPIOWakeup) == 0:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("ACTUAL RESULT  : CPU freeze duration & GPIO Wakeup status are as expected")
                    print("[TEST EXECUTION RESULT] : SUCCESS\n")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("ACTUAL RESULT  : CPU freeze duration & GPIO Wakeup status are not as expected")
                    print("[TEST EXECUTION RESULT] : FAILURE\n")
            else:
                freezeDuration = int(str(details).split(";")[0].split(":")[1].strip())
                print("Value Returned : %s secs (approx)" %(str(details).split(";")[0]))
                print("ACTUAL RESULT  : %s" %(str(details).split(";")[1]))
                print("[TEST EXECUTION RESULT] : SUCCESS\n")

                print("\nTEST STEP2: Check CPU freeze duration and reboot the device")
                print("EXPECTED RESULT : Reboot if freeze duration is >= timeout")
                if int(freezeDuration) >= int(timeout):
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("ACTUAL RESULT  : CPU freeze duration is as expected")
                    print("[TEST EXECUTION RESULT] : SUCCESS\n")
                else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("ACTUAL RESULT  : CPU freeze duration is not as expected")
                    print("[TEST EXECUTION RESULT] : FAILURE\n")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            details = tdkTestObj.getResultDetails();
            print("ACTUAL RESULT  : ",details)
            print("[TEST EXECUTION RESULT] : FAILURE\n")
    
    except Exception as e:
        print(e);
        actualResult = "FAILURE";

    return actualResult;
