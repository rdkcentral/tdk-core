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
<?xml version="1.0" encoding="UTF-8"?><xml>
  <id/>
  <version>1</version>
  <name>RDKV_DAB_Output_Image_Api_Validation</name>
  <primitive_test_id/>
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <primitive_test_version>4</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test validates the Screenshot Api of DAB</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>Rdkv_dab_06</test_case_id>
    <test_objective>This test validates DAB Output image api i.e., screenshot API validation</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.DAB adapter service should be up and running in box</pre_requisite>
    <api_or_interface_used>DAB</api_or_interface_used>
    <input_parameters>1.Device_Id
2.Broker_port address
3.Operation_name
</input_parameters>
    <automation_approch>1.As pre-requisite we have to make sure dab service is up and running
2.Invoke DAB Output Image screenshot Api
3.Decode the encoded data received as part of dab response
4.Save the image in path.
5.Validate the image is present in path</automation_approch>
    <expected_output>Screenshot should be successful and save in path specified</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_Output_Image_Api_Validation</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import rdkv_performancelib
import json
import ast
from saveAsPng import *
from tdkvScreenShotUtility import *
from rialto_containerlib import *
from tdkvScreenShotUtility import *
from rdkv_dablib import *
from dab_config import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_dab","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_DAB_Output_Image_Api_Validation');
# Assinging ip address to broker Ip address
broker_address =ip
device_id = ""

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
#Validating the preconditions
print("\nExecuting pre conditions")
if expectedResult in result.upper():
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
        tdkTestObj.setResultStatus("SUCCESS")
        print("\n Enabling DAB Adapter\n")
        #Command to enable dab-adapter
        command = 'touch /opt/dab-enable'
        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
        tdkTestObj.addParameter("command",command)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResult()
        if expectedResult in result:
           tdkTestObj.setResultStatus("SUCCESS");
           print("\n Restarting DAB Adapter\n")
           #Command to enable dab-adapter
           command = 'systemctl restart dab-adapter'
           tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
           tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
           tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
           tdkTestObj.addParameter("command",command)
           tdkTestObj.executeTestCase(expectedResult)
           result = tdkTestObj.getResult()
           #devid = tdkTestObj.getResultDetails()
           if expectedResult in result:
              tdkTestObj.setResultStatus("SUCCESS");
              print("\n checking status of  DAB Adapter\n")
              #Command to enable dab-adapter
              command = 'systemctl status dab-adapter| awk "/DAB Device ID/ {print $5}"'
              tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
              tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
              tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
              tdkTestObj.addParameter("command",command)
              tdkTestObj.executeTestCase(expectedResult)
              result = tdkTestObj.getResult()
              devid = tdkTestObj.getResultDetails()
              try:
                  Dab_id = devid.split(": ")[-1]
                  print(f"Dab adapter is active with Device ID: {Dab_id}")
              except IndexError:
                  print("Error: Couldn't extract device ID (format issue?)")
              if expectedResult in result:
                 tdkTestObj.setResultStatus("SUCCESS");
                #Prmitive test case which associated to this Script
                 tdkTestObj = obj.createTestStep('setup_mqtt_client');
                 tdkTestObj.addParameter("broker_address",broker_address)
                 tdkTestObj.executeTestCase(expectedResult)
                 result_val = tdkTestObj.getResult() ;
                 client = tdkTestObj.getResultDetails();

              else:
                  tdkTestObj.setResultStatus("FAILURE");
           else:
                tdkTestObj.setResultStatus("FAILURE");
        else:
            tdkTestObj.setResultStatus("FAILURE");
#Initializing device_id
device_id = str(Dab_id.strip())
print("\nInvoking DAB screenshot API")
dab_screen_shot =  operation_name["dab_screenshot"]
message_override ={"outputLocation": "/opt/apache-tomcat-7.0.96/webapps/rdk-test-tool/fileStore/"}
tdkTestObj = obj.createTestStep('perform_operation')
tdkTestObj.addParameter('operation_name',str(dab_screen_shot))
tdkTestObj.addParameter('message_override',message_override)
tdkTestObj.addParameter('device_id',device_id)
tdkTestObj.executeTestCase(expectedResult)
key_response =json.loads(tdkTestObj.getResultDetails())
if key_response and key_response["status"] == 200:
    tdkTestObj.setResultStatus("SUCCESS");
    print("\n DAB Screen_shot api invoked successfully")
    encoded_data=key_response['outputImage'].split(',')[1]
    encoded_data =str(encoded_data.strip())
    tdkTestObj = obj.createTestStep('dab_save_png');
    tdkTestObj.addParameter("encoded_data",encoded_data)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult() ;
    if result == "SUCCESS":
       print("\n Screenshot capture is successful")
       tdkTestObj.setResultStatus("SUCCESS");
    else:
       print("\n Failed to capture Screenshot")
       print ("[TEST EXECUTION RESULT] : FAILURE");
       tdkTestObj.setResultStatus("FAILURE");
else:
    print("\n Failed to invoke DAB Screenshot api.")
    print ("[TEST EXECUTION RESULT] : FAILURE");
    tdkTestObj.setResultStatus("FAILURE");

obj.unloadModule("rdkv_dab");
