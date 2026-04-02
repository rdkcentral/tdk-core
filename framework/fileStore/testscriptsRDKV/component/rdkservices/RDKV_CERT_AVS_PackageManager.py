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
obj = tdklib.TDKScriptingLibrary("rdkservices","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AVS_PackageManager')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

#Prmitive test case which associated to this Script
tdkTestObj = obj.createTestStep('RdkService_Test')
tdkTestObj.addParameter("xml_name","PackageManager")
expectedResult = "SUCCESS"

#Execute the test case in DUT
tdkTestObj.executeTestCase(expectedResult)

#Get the result of execution
result = tdkTestObj.getResult()
print("[TEST EXECUTION RESULT] : %s" %result)

#Set the result status of execution
tdkTestObj.setResultStatus(result)

obj.unloadModule("rdkservices")