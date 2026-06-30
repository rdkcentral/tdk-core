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
obj = tdklib.TDKScriptingLibrary("Cryptography","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Cryptography_Vault_Tests');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
expectedResult="SUCCESS"
failed = False;

if "SUCCESS" in result.upper():
    tdkTestObj = obj.createTestStep('execute_Cmnd_In_DUT')
    testModule = "Vault"
    #Define Module Tests
    Tests = {"Vault":[" Vault::ImportExport", " Vault::SetGet"]}
    test_Names = Tests[testModule]
    if len(test_Names) > 1:
        test_Name_End = str(test_Names[-1]);
    else:
        test_Name_End = str(test_Names[0])
    test_Name_First = str(test_Names[0]);


    command = "cgfacetests | awk '/" + test_Name_First + "/,/" + test_Name_End + " -/'"
    tdkTestObj.addParameter("command",command)
    tdkTestObj.executeTestCase(expectedResult);

    output = tdkTestObj.getResultDetails()
    print("OUTPUT: ...\n", output)

    if "command not found" in output:
        print ("FAILURE : Test application not installed in DUT")
        tdkTestObj.setResultStatus("FAILURE")
        failed = True

    test_result_string = [line for line in output.splitlines() if "PASSED" in line]
    for line in test_result_string:
        if "0 FAILED" not in line and not failed:
            print ("FAILURE : Observed failures in Vault test execution");
            tdkTestObj.setResultStatus("FAILURE")
    if not failed:
        print ("SUCCESS : Vault test execution was successfull, no failures observed")
        tdkTestObj.setResultStatus("SUCCESS")

obj.unloadModule("Cryptography");

