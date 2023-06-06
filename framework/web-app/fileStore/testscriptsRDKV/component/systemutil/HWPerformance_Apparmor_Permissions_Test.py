##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>HWPerformance_Apparmor_Permissions_Test</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>SystemUtilAgent_ExecuteBinary</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>File Permissions Test</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>5</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
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
    <test_case_id>TC_HWPerformance_23</test_case_id>
    <test_objective>To check whether profile permission correct or wrong</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI-HYB</test_setup>
    <pre_requisite>1. TDK Agent should be up and running 2.  tdk_sample.profile should be available in DUT 3. tdk_apparmoraccess should be available in /opt/TDK path</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>File present path and file permission</input_parameters>
    <automation_approch>1. Enable apparmor 2. Validate profile</automation_approch>
    <expected_output>The command should execute successfully</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>libsystemutilstub.so.0</test_stub_interface>
    <test_script>HWPerformance_Apparmor_Permissions_Test</test_script>
    <skipped>No</skipped>
    <release_version>M113</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from rdkv_performancelib import * ;

#IP and Port of box, No need to change,
#This will be replaced with corresponding Box Ip and port while executing script
ip = <ipaddress>
port = <port>

sysUtilObj = tdklib.TDKScriptingLibrary("systemutil","1");
sysUtilObj.configureTestCase(ip,port,'HWPerformance_Apparmor_Permissions_Test');
sysUtilLoadStatus = sysUtilObj.getLoadModuleResult();
print "System module loading status : %s" %sysUtilLoadStatus;
#Set the module loading status
sysUtilObj.setLoadModuleStatus(sysUtilLoadStatus);

if ("SUCCESS" in sysUtilLoadStatus.upper()):
     # Execute apparmor permission test and get the result
     tdkTestObj = sysUtilObj.createTestStep('ExecuteCommand')
     command = "touch /tmp/foobar | apparmor_parser -r /opt/TDK/tdk_sample.profile && echo 1 || echo 0"
     print "Executor Command : %s" %command
     tdkTestObj.addParameter("command",command)
     tdkTestObj.executeTestCase("SUCCESS");
     details=tdkTestObj.getResultDetails();
     if "1" in details :
         command ="tdk_apparmoraccess /bin/ls r"
         print "Executor Command : %s" %command
         tdkTestObj.addParameter("command",command)
         tdkTestObj.executeTestCase("SUCCESS");
         details=tdkTestObj.getResultDetails();
         details=details.replace(r'\"','\"').replace(r'\n', '\n')
         if "Success" in  details and "error" not in details and "Fail: 0" in details:
             print details
             print "\n[TEST EXECUTION RESULT] : SUCCESS\n"

             command = "tdk_apparmoraccess /tmp/foobar rw"
             print "Executor Command : %s" %command
             tdkTestObj.addParameter("command",command)
             tdkTestObj.executeTestCase("SUCCESS");
             details=tdkTestObj.getResultDetails();
             details=details.replace(r'\"','\"').replace(r'\n', '\n')
             if "Success" in details and "error" not in details and "Fail: 0" in details:
                  print details
                  print "\n[TEST EXECUTION RESULT] : SUCCESS\n"

                  command = "tdk_apparmoraccess /bin/ls rw"
                  print "Executor Command : %s" %command
                  tdkTestObj.addParameter("command",command)
                  tdkTestObj.executeTestCase("SUCCESS");
                  details=tdkTestObj.getResultDetails();
                  details=details.replace(r'\"','\"').replace(r'\n', '\n')
                  if details and "error" in details:
                      tdkTestObj.setResultStatus("SUCCESS");
                      print details
                      print "Failed as expected because /bin/ls is readonly as per tdk_sample.profile"
                      print "\n[TEST EXECUTION RESULT] : SUCCESS\n"
                  else:
                      print details
                      tdkTestObj.setResultStatus("FAILURE");
                      print "\n[TEST EXECUTION RESULT] : FAILURE\n"
             else:
                 print details
                 tdkTestObj.setResultStatus("FAILURE");
                 print "\n[TEST EXECUTION RESULT] : FAILURE\n"
         else:
             print details
             tdkTestObj.setResultStatus("FAILURE");
             print "[TEST EXECUTION RESULT] : FAILURE\n"
     else:
         print "\nFile tdk_sample.profile not found\n"
         tdkTestObj.setResultStatus("FAILURE");
else:
    print "System Module Loading Status:FAILURE"

#Unload systemutil module
sysUtilObj.unloadModule("systemutil");
