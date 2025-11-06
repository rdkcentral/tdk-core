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
  <name>RDKV_CERT_FCA_All_SDK</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkv_firecertapp_execute</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To execute Firebolt Certification Sanity Suite</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>10</execution_time>
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
    <box_type>RPI-HYB</box_type>
    <!--  -->
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id></test_case_id>
    <test_objective></test_objective>
    <test_type></test_type>
    <test_setup></test_setup>
    <pre_requisite></pre_requisite>
    <api_or_interface_used></api_or_interface_used>
    <input_parameters></input_parameters>
    <automation_approch></automation_approch>
    <expected_output></expected_output>
    <priority></priority>
    <test_stub_interface></test_stub_interface>
    <test_script></test_script>
    <skipped></skipped>
    <release_version></release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import time
import rdkv_performancelib

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_firecertapp","1",standAlone=True);
pvs_obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_FCA_All_SDK');
pvs_obj.configureTestCase(ip,port,'RDKV_CERT_FCA_All_SDK');
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)


expectedResult = "SUCCESS"
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkv_firecertapp_createURL');
    tdkTestObj.addParameter("url_type","fca_test_url")
    tdkTestObj.executeTestCase(expectedResult)
    fca_url=tdkTestObj.getResultDetails()
    if fca_url != "FAILURE":
        tdkTestObj.setResultStatus("SUCCESS")
        print("Successfully created FCA url")
        print (fca_url)

        tdkTestObj = pvs_obj.createTestStep('rdkservice_getPluginStatus');
        tdkTestObj.addParameter("plugin","LightningApp")
        tdkTestObj.executeTestCase(expectedResult)
        plugin_status=tdkTestObj.getResultDetails()
        launch_status,launch_start_time = rdkv_performancelib.launch_plugin(obj,"LightningApp")
        if launch_status == expectedResult:
            time.sleep(10)
            tdkTestObj = pvs_obj.createTestStep('rdkservice_getPluginStatus')
            tdkTestObj.addParameter("plugin","LightningApp")
            tdkTestObj.executeTestCase(expectedResult)
            lightningapp_status = tdkTestObj.getResultDetails()
            result = tdkTestObj.getResult()
            if lightningapp_status == 'resumed' and expectedResult in result:
                print("\n LightningApp resumed successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(10)
                print("\n Set test URL")
                tdkTestObj = pvs_obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","LightningApp.1.url")
                tdkTestObj.addParameter("value",fca_url)
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult()
                time.sleep(10)
                if expectedResult in result:
                    print("\nValidate if the URL is set successfully or not")
                    tdkTestObj = pvs_obj.createTestStep('rdkservice_getValue')
                    tdkTestObj.addParameter("method","LightningApp.1.url")
                    tdkTestObj.executeTestCase(expectedResult)
                    new_url = tdkTestObj.getResultDetails()
                    result = tdkTestObj.getResult()
                    if fca_url in new_url and expectedResult in result:
                        tdkTestObj.setResultStatus("SUCCESS");
                        print ("\n URL(",new_url,") is set successfully")
                        time.sleep(20)

                        sequence = "40,40,40,13,13,40,40,40,13,13"
                        #Prmitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('rdkv_firecertapp_execute');
                        tdkTestObj.addParameter("sequence",sequence)

                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult);

                        #Get the result of execution
                        result = tdkTestObj.getResult();
                        details = tdkTestObj.getResultDetails();

                        if expectedResult in result and details == "SUCCESS" :
                            tdkTestObj.setResultStatus("SUCCESS")
                            print("Successfully executed all SDK suite test cases in FCA app")
                            time.sleep(180)
                            print("Getting the report URL")
                            tdkTestObj = obj.createTestStep('rdkv_firecertapp_createURL');
                            tdkTestObj.addParameter("url_type","fca_report")
                            tdkTestObj.executeTestCase(expectedResult)
                            status=tdkTestObj.getResultDetails()
                            if expectedResult in status:
                                print("Successfully downloaded the FCA report")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                tdkTestObj.setResultStatus("FAILURE")
                                print("Failed to download the FCA report")

                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            print("Failed to execute all SDK suite test cases in FCA app")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print ("The URL in LightningApp is not same as FCA URL or Failed to get the current URL")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Failed to set the FCA URL in LightningApp")
                #Reverting the LightningApp status
                tdkTestObj = pvs_obj.createTestStep('rdkservice_setPluginStatus');
                tdkTestObj.addParameter("plugin","LightningApp")
                tdkTestObj.addParameter("status","deactivate")
                tdkTestObj.executeTestCase(expectedResult)
                status=tdkTestObj.getResult()
                print(status)
                if status in expectedResult:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print ("Deactivated LightningApp")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Failed to deactivate LightningApp")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print ("Failed to resume the LightningApp")
        else:
            tdkTestObj.setResultStatus("FAILURE")
            print ("Failed to launch LightningApp")
    else:
        tdkTestObj.setResultStatus("FAILURE")
        print ("Failed to create the FCA url")
    obj.unloadModule("rdkv_firecertapp");
else:
    obj.setLoadModuleStatus("FAILURE")
    print ("Failed to load module")
