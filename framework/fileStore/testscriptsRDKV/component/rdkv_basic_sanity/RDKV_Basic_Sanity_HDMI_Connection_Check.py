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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_HDMI_Connection_Check');

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" % result)
obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

if expectedResult in result.upper():

    tdkTestObj = obj.createTestStep('rdkv_basic_sanity_hdmiConnectionCheck')
    tdkTestObj.executeTestCase(expectedResult)
    print("")

    result  = tdkTestObj.getResult()
    details = tdkTestObj.getResultDetails()
    print("[HDMI Connection Check] : %s | %s" % (result, details))

    if result == "SUCCESS":
        tdkTestObj.setResultStatus("SUCCESS")
    else:
        tdkTestObj.setResultStatus("FAILURE")

    # Unload the module
    obj.unloadModule("rdkv_basic_sanity")

else:
    # Set load module status
    obj.setLoadModuleStatus("FAILURE")
    print("FAILURE: Failed to load module")
