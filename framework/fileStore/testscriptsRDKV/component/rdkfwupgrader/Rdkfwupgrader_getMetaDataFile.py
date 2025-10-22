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
  <name>Rdkfwupgrader_getMetaDataFile</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkfwupgrader_getMetaDataFile</primitive_test_name>
  <!--  -->
  <primitive_test_version>2</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To obtain file list from a test directory via rdkfwupgrader API getMetaDataFile and verify output</synopsis>
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
    <test_case_id>RDKFWUPGRADE_18</test_case_id>
    <test_objective>To obtain file list from a test directory via rdkfwupgrader API getMetaDataFile and verify output</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video Accelerator,RPI</test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used>getMetaDataFile</api_or_interface_used>
    <input_parameters>testString</input_parameters>
    <automation_approch>1. TM loads the RDK_fwupgradeAgent and SystemUtil via the test agent.
    2. Using systemutil execute command , create test packages in a test directory
    3. RDK_fwupgradeAgent will invoke getMetaDataFile API with testString.
    4. TM will verify the output by having a expected output string and cross verify.
    5. Delete test packages created using systemutil execute command.
    6. TM will return SUCCESS or FAILURE based on the result from the above step.</automation_approch>
    <expected_output>API must return file names correctly</expected_output>
    <priority>High</priority>
    <test_stub_interface>librdkfwupgraderstub.so.0.0.0</test_stub_interface>
    <test_script>Rdkfwupgrader_getMetaDataFile</test_script>
    <skipped></skipped>
    <release_version>M133</release_version>
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
obj.configureTestCase(ip,port,'Rdkfwupgrader_getMetaDataFile');
sysUtilObj.configureTestCase(ip,port,'Rdkfwupgrader_getMetaDataFile');

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print("System module loading status : %s" %sysUtilLoadStatus);
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

#test_dir and test_packages obtained from RdkfwupgraderTestVariables

def createPackages():
    print("\n")
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    #Create test directory
    cmd = "mkdir " + test_dir + " ; "
    #Create dummy packages for testing
    for test_package in test_packages:
        cmd =  cmd + "touch " + test_dir + test_package + " ;"
    #List files to cross verify package creation
    cmd = cmd + "ls " + test_dir
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    if "TDK_1_package.json" in details and "TDK_2_package.json" in details:
        print("Test packages created successfully")
        tdkTestObj.setResultStatus("SUCCESS");
        return True
    else:
        print("FAILURE: Unable to create Test packages")
        tdkTestObj.setResultStatus("FAILURE");
        return False
    
def deletePackages():
    print("\n")
    tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand');
    #Delete test directory
    cmd = " rm -rf " + test_dir + " ;"
    #Command to cross verify if directory is deleted
    cmd = cmd + 'if [ -d ' + test_dir +' ]; then echo "Directory exists"; else echo "Directory does not exist"; fi'
    tdkTestObj.addParameter("command", cmd);
    tdkTestObj.executeTestCase("SUCCESS");
    details = tdkTestObj.getResultDetails()
    if "Directory does not exist" in details:
        print("Test packages deleted successfully\n")
        tdkTestObj.setResultStatus("SUCCESS");
        return True
    else:
        print("FAILURE: Unable to delete Test packages")
        tdkTestObj.setResultStatus("FAILURE");
        return False

if "SUCCESS" in result.upper() and "SUCCESS" in sysUtilLoadStatus.upper():
    if createPackages():
        #Primitive test case which associated to this Script
        tdkTestObj = obj.createTestStep('rdkfwupgrader_getMetaDataFile');
        tdkTestObj.addParameter("directory", test_dir)
        tdkTestObj.executeTestCase("SUCCESS");
        #Get the result of execution
        result = tdkTestObj.getResult();
        details = tdkTestObj.getResultDetails().strip().replace(r'\n', '\n');

        print("[RESULT] : %s" %result);
        print("[DETAILS] : \n%s" %details);

        if result == "SUCCESS":
            print ("Successfully  obtained files from ",test_dir);
            print ("Validating result")
            files_present = True
            checkFiles = []
            for test_package in test_packages:
                checkString =  test_dir + "/" + test_package
                checkFiles.append(checkString)
                if checkString not in details:
                    print ("ERROR : %s not found in getMetaDataFile result"%(checkString))
                    files_present = False
                    tdkTestObj.setResultStatus("FAILURE")
            if files_present:
                print("SUCCESS : Validation successfull")
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("FAILURE : Validation unsuccessfull")
                print("Expected Result : ",checkFiles)
                print("Actual Result : ",details.splitlines())
        else:
            print ("FAILURE : getMetaDataFile failed")
            tdkTestObj.setResultStatus("FAILURE")
        deletePackages();

    obj.unloadModule("rdkfwupgrader");
    sysUtilObj.unloadModule("systemutil");
else:
    print ("LOAD MODULE FAILED")
