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
  <name>RDKV_CERT_RVS_RDKService_APIs_SynchronousCall</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_synchronous_request</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>To invoke RDK Services APIs simultaneously repeatedly and verify it</synopsis>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_66</test_case_id>
    <test_objective>To invoke RDK Services APIs simultaneously repeatedly and verify it</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>Update StabilityTestVariable file and add the number of iteration needed for the stress test</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>url, iterations</input_parameters>
    <automation_approch>1. Load rdkv stability module
2. Construct a list of api requests with provided methods and callsign
3. For each request, capture and process api response
4. Run the stress test by iterating over the prepared request multiple times as per number of iterations provided. Gather failure counts and track failed requests
5. After completing the stress test iterations, display summary results, including the number of iteration, failure counts, and details of failed requests
6. Set the overall test result status based on success or failure of entire stress test
7. Unload module</automation_approch>
    <expected_output>The DUT should handle multiple api requests successfully without failing under stress conditions. If all the API requests are successfully executed without any failures, the test result status will be marked as "SUCCESS" and indicating that the device meets the expected behavior of handling multiple api request without issues</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_RDKService_APIs_SynchronousCall</test_script>
    <skipped>No</skipped>
    <release_version>M135</release_version>
    <remarks></remarks>
  </test_cases>
</xml>
'''
import tdklib
import StabilityTestVariables

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_RDKService_APIs_SynchronousCall');

#Get the result of connection with test component and DUT


result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in (result.upper()):

    #Prmitive test case which associated to this Script
    print("\nRebooting the device before starting the stress test")

    rebootwaitTime =  StabilityTestVariables.rebootwaitTime
    tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
    tdkTestObj.addParameter("waitTime",rebootwaitTime)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    print(result)
    if expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print ("\n Rebooted device successfully")

        print ("Starting the stress testing")
        required_config_values = ["iterations", "methods" ]
        missing_values = [attr for attr in required_config_values if not hasattr(StabilityTestVariables, attr) or getattr(StabilityTestVariables, attr) == ""]
        if not missing_values:
            iterations = StabilityTestVariables.iterations
            methods = StabilityTestVariables.methods
            failed_reqs = []
            failed_req_count = {}
            for count in range(int(iterations)):
                print ("\nITERATION : {}".format(count + 1))
                tdkTestObj = obj.createTestStep('rdkservice_synchronous_request');
                tdkTestObj.addParameter("method",methods)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                if result != "SUCCESS":
                    failed_reqs.append(result)
                    failed_methods = eval(result)
                    for method in failed_methods:
                        if method in failed_req_count:
                            failed_req_count[method] += 1
                        else:
                            failed_req_count[method] = 1
                if expectedResult in result:
                    tdkTestObj.setResultStatus("SUCCESS");
                else:
                    tdkTestObj.setResultStatus("FAILURE")
            print ("Total iteration count: {}".format(iterations))
            total_failure_count = sum(failed_req_count.values())
            print ("Total failure count: {}".format(total_failure_count))
            for method, count in failed_req_count.items():
                print( "API Failed: {} ({})".format(method, count))
            print ("Failed Requests: {}".format(failed_reqs))
        else:
            print("Required values not configured in StabilityTestVariables: {}".format(missing_values))
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print ("Failed to reboot the device")
        tdkTestObj.setResultStatus("FAILURE");
    obj.unloadModule("rdkv_stability")
else:
    obj.setLoadModuleStatus("FAILURE");
    print( "Failed to load module")
