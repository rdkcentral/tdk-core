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
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("Graphics","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'FNCS_Essos_Wayland_Client_Validation');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"

if "SUCCESS" in result.upper():

    tdkTestObj = obj.createTestStep('execute_Cmnd_InDUT')
    command = "cd /opt/TDK; sh RunGraphicsTDKTest.sh Essos 30 USE_WAYLAND"
    print("Executing command in DUT: ", command)
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails()
    if not output:
        print ("FAILURE : No output was obtained from test")
        tdkTestObj.setResultStatus("FAILURE")
    else:
        tdkTestObj.setResultStatus("SUCCESS")

        tdkTestObj = obj.createTestStep('parse_graphics_output')
        tdkTestObj.addParameter("graphics_output",output)
        tdkTestObj.executeTestCase(expectedResult);
        output = tdkTestObj.getResultDetails()
        tdkTestObj.setResultStatus(output)

obj.unloadModule("Graphics");
