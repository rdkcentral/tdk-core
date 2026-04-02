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
import tdklib; 

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Vulkan","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Vkmark_Benchmark_MAILBOX_Score');

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"
mode="mailbox"

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('set_prerequisites');
    boxtype = obj.getDeviceBoxType();
    if "RPI-Client" in boxtype:
        tdkTestObj.addParameter("model", "RPI")
    tdkTestObj.executeTestCase(expectedResult);
    details = tdkTestObj.getResultDetails()
    if "SUCCESS" in details:
        print("PRE-REQUISITES SUCCESSFULLY SET")
        tdkTestObj = obj.createTestStep('execute_binary')
        tdkTestObj.addParameter("present_mode",mode)
        tdkTestObj.executeTestCase(expectedResult)
        details = tdkTestObj.getResultDetails()
        if "SUCCESS" in details:
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print ("Setting Result as FAILURE")
            tdkTestObj.setResultStatus("FAILURE")

        tdkTestObj = obj.createTestStep('execute_postrequisites')
        tdkTestObj.executeTestCase(expectedResult)
        details = tdkTestObj.getResultDetails()
        print("POST-REQUISITES EXECUTION SUCCESSFUL")

    else:
        print("Unable to set PRE-REQUISITES")

obj.unloadModule("Vulkan");