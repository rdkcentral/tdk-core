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
'''
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <!-- Do not edit id. This will be auto filled while exporting. If you are adding a new script keep the id empty -->
  <version>1</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>NM_WifiMgr_getAvailableSSIDsAsyncIncrement</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>NetSrvMgrAgent_NetSrvMgr_FunctionCall</primitive_test_name>
  <!--  -->
  <primitive_test_version>3</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This would help to scan available SSIDs around device</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>2</execution_time>
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
    <box_type>IPClient-Wifi</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
    <box_type>RPI-Client</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_NM_3</test_case_id>
    <test_objective>To start wifi scanning</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Video_Accelerator</test_setup>
    <pre_requisite>IARMDaemonMain and netsrvmgr should be up and running</pre_requisite>
    <api_or_interface_used>IARM_Bus_Call(IARM_BUS_WIFI_MGR_API_getAvailableSSIDsAsyncIncrement)</api_or_interface_used>
    <input_parameters>char* - method_name</input_parameters>
    <automation_approch>1. TM loads the NetSrvMgr_Agent via the test agent.
2.NetSrvMgr_Agent will connect to a wifi network using the credentials provided.
3.NetSrvMgr_Agent will return SUCCESS or FAILURE based on the result from the above step</automation_approch>
    <expected_output>wifi scanning should be success</expected_output>
    <priority>High</priority>
    <test_stub_interface>libnetsrvmgrstub.so</test_stub_interface>
    <test_script>NM_WifiMgr_getAvailableSSIDsAsyncIncrement</test_script>
    <skipped>No</skipped>
    <release_version>M126</release_version>
    <remarks></remarks>
 </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from iarmbus import IARMBUS_Init,IARMBUS_Connect,IARMBUS_DisConnect,IARMBUS_Term;


#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>

#Test component to be tested
iarmObj = tdklib.TDKScriptingLibrary("iarmbus","2.0");
iarmObj.configureTestCase(ip,port,'NM_WifiMgr_getAvailableSSIDsAsyncIncrement');
#Get the result of connection with test component and STB
iarmLoadStatus = iarmObj.getLoadModuleResult();
print("Iarmbus module loading status : %s" %iarmLoadStatus);
#Set the module loading status
iarmObj.setLoadModuleStatus(iarmLoadStatus);


if "SUCCESS" in iarmLoadStatus.upper():
    #Calling IARMBUS API "IARM_Bus_Init"
    result = IARMBUS_Init(iarmObj,"SUCCESS")
    #Check for SUCCESS/FAILURE return value of IARMBUS_Init
    if "SUCCESS" in result:
        #Calling IARMBUS API "IARM_Bus_Connect"
        result = IARMBUS_Connect(iarmObj,"SUCCESS")
        #Check for SUCCESS/FAILURE return value of IARMBUS_Connect
        if "SUCCESS" in result:
            #Test component to be tested
            netsrvObj = tdklib.TDKScriptingLibrary("netsrvmgr","1");
            netsrvObj.configureTestCase(ip,port,'NM_WifiMgr_getAvailableSSIDsAsyncIncrement');

            #Get the result of connection with test component and DUT
            netsrvLoadStatus =netsrvObj.getLoadModuleResult();
            print("[LIB LOAD STATUS]  :  %s" %netsrvLoadStatus);

            netsrvObj.setLoadModuleStatus(netsrvLoadStatus);

            if "SUCCESS" in netsrvLoadStatus.upper():
                #Prmitive test case which associated to this Script
                tdkTestObj = netsrvObj.createTestStep('NetSrvMgrAgent_NetSrvMgr_FunctionCall');

                tdkTestObj.addParameter("method_name", "getAvailableSSIDsAsyncIncr");
                expectedresult="SUCCESS"
                tdkTestObj.executeTestCase(expectedresult);
                actualresult = tdkTestObj.getResult();
                details = tdkTestObj.getResultDetails();

                print("[TEST EXECUTION RESULT] : %s" %actualresult);
                print("Details: [%s]"%details);

                if expectedresult in actualresult:
                    print("[TEST EXECUTION - SUCCESS] :  WIFI start scan was returned successfully");
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    print("[TEST EXECUTION - FAILURE] :  Failed to WIFI start scan");
                    tdkTestObj.setResultStatus("FAILURE");

                netsrvObj.unloadModule("netsrvmgr");
            else:
                print("Failed to Load netsrvmgr Module");

            result = IARMBUS_DisConnect(iarmObj,"SUCCESS")
        result = IARMBUS_Term(iarmObj,"SUCCESS")
    iarmObj.unloadModule("iarmbus");
else:
    print("Failed to Load iarmbus Module ");
