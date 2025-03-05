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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>Rdkfwupgrader_GetServerURL</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_GetServerURL</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To pass string with filename and verify output whether it got scanned properly the URL from the file or not.</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>1</execution_time>
  <!--  -->
  <long_duration>false</long_duration>
  <!--  -->
  <advanced_script>false</advanced_script>
  <!-- execution_time is the time out time for test execution -->
  <remarks></remarks>
  <!-- Reason for skipping the tests if marked to skip -->
  <skip>false</skip>
  <!--  -->
  <box_types>
    <box_type>RPI-Client</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKFWUPGRADE_31</test_case_id>
    <test_objective>To pass string with filename and verify output whether it got scanned properly the URL from the file or not.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>GetServerUrlFile</api_or_interface_used>
    <input_parameters>pServUrl - pointer to a char buffer to store the output string
    szBufSize - the size of the character buffer in argument 1.
    pFileName - a character pointer to a filename to scan.</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent and SystemUtil via the test agent.
    2. Using systemutil execute command, create a test file along with the test url data.
    3. RDK_fwupgradeAgent will invoke GetServerUrlFile API with testurl data.
    4. TM will verify the output by having a expected output string and cross verify.
    5. Delete test file created using systemutil execute command.
    6. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must scan properly the test url data and return correctly</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_GetServerURL</test_script>
    <skipped></skipped>
    <release_version>M134</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib;
from RdkfwupgraderTestVariables import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkfwupgrader","1");
sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'Rdkfwupgrader_GetServerURL');
sysUtilObj.configureTestCase(ip,port,'Rdkfwupgrader_GetServerURL');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print("System module loading status : %s" %sysUtilLoadStatus);
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

#servURL_test_filepath and test_url_data obtained from RdkfwupgraderTestVariables

def createTestFile():
    print("\n")
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    #Create test config file under tmp dir
    cmd = "touch " + servURL_test_filepath + " ;"
    #List files to cross verify the file
    cmd = cmd + "ls " + servURL_test_filepath;
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    if "swupdate.conf" in details:
        print("Test file created successfully");
        tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
        cmd = "echo " + test_url_data + " > " + servURL_test_filepath + " ;"
        cmd = cmd + "echo " + "$(cat " + servURL_test_filepath + ")"; 
        tdkTestObj.addParameter("command", cmd);
        tdkTestObj.executeTestCase("SUCCESS");
        details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n');
        print("details", details);
        print("test_url_data", test_url_data);
        if test_url_data in details:
            print("URL data written successfully to the file");
            tdkTestObj.executeTestCase("SUCCESS");
            return True
        else:
            print("URL data doesn't written successfully to the file");
            tdkTestObj.setResultStatus("FAILURE");
            return False
    else:
        print("FAILURE: Unable to create Test file");
        tdkTestObj.setResultStatus("FAILURE");
        return False
    
def deleteTestFile():
    print("\n")
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    #Delete test directory
    cmd = " rm -rf " + servURL_test_filepath + " ;"
    #Command to cross verify if directory is deleted
    cmd = cmd + 'if [ -d ' + servURL_test_filepath +' ]; then echo "Files exists"; else echo "File does not exist"; fi'
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails();
    if "File does not exist" in details:
        print("Test file deleted successfully\n")
        tdkTestObj.setResultStatus("SUCCESS");
        return True
    else:
        print("FAILURE: Unable to delete Test file")
        tdkTestObj.setResultStatus("FAILURE");
        return False

if "SUCCESS" in result.upper() and "SUCCESS" in sysUtilLoadStatus.upper():
    if createTestFile():
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('rdkfwupgrader_GetServerURL');
        tdkTestObj.addParameter("filename", servURL_test_filepath);
        tdkTestObj.addParameter("null_param", 0);
        tdkTestObj.addParameter("buffer_size", 128);
        tdkTestObj.executeTestCase("SUCCESS");
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n');

        print("[RESULT] : %s" %result);
        print("[DETAILS] : \n%s" %details);

        if result == "SUCCESS":
            if test_url_data in details: 
                print("Successfully scans URL from a test file");
                tdkTestObj.setResultStatus("SUCCESS");
            else:
                print ("URL data mismatch b/w the input data and the result");
                print("Expected Result : ", test_url_data);
                print("Actual Result : ", details.splitlines());
                tdkTestObj.setResultStatus("FAILURE");
        else:
            print ("FAILURE : GetServerUrlFile failed");
            tdkTestObj.setResultStatus("FAILURE");
        deleteTestFile();

    obj.unloadModule("rdkfwupgrader");
    sysUtilObj.unloadModule("systemutil");
else:
    print ("LOAD MODULE FAILED")
