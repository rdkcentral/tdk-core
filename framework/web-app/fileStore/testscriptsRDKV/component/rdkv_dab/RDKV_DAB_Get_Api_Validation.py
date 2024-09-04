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
  <version>2</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_DAB_Get_Api_Validation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <!--  -->
  <primitive_test_version>4</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates all DAB Get Api response against RDK values based on configured mappings.,
Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.</synopsis>
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
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_DAB_01</test_case_id>
    <test_objective>This test validates DAB response against RDK values based on configured mappings.
Compares DAB and RDK values for each specified setting, handling specific cases and data type conversions.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.DAB adapter service should be up and running in box</pre_requisite>
    <api_or_interface_used>DAB</api_or_interface_used>
    <input_parameters>1.Device_Id
2.Broker_port address
3.Operation_name
4.Dab response</input_parameters>
    <automation_approch>1.As pre-requisite we have to make sure dab service is up and running
2.Invoke all supported DAB Get Api and save th response.
3.Compare the dab get response obtained with corresponding rdk Api
3.Print the failed Comparisions.</automation_approch>
    <expected_output>All DAB get Api responses should match with their corresponding rdk Api response.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_Get_Api_Validation</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
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
obj.configureTestCase(ip,port,'RDKV_DAB_Get_Api_Validation');
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
        conf_file,file_status = getConfigFileName(obj.realpath)
        config_status,tr181_parameter = getDeviceConfigKeyValue(conf_file,"DAB_RFC_PARAMETER")
        if "SUCCESS" in config_status:
            tdkTestObj.setResultStatus("SUCCESS")
            tdkTestObj = obj.createTestStep('memcr_datamodelcheck')
            tdkTestObj.addParameter("datamodel",tr181_parameter)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if "SUCCESS" in result:
                tdkTestObj.setResultStatus("SUCCESS")
            conf_file,file_status = getConfigFileName(obj.realpath)
            config_status,dab_enable_parameter = getDeviceConfigKeyValue(conf_file,"DAB_ENABLE_PARAMETER")
            command = 'touch '+str(dab_enable_parameter)
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
                      print("Failed to setup mqtt_client.")
               else:
                   print("Failed to Restart the DAB adapter")
                   tdkTestObj.setResultStatus("FAILURE");
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("Failed to enable dab rfc parameter.")
        else:
            tdkTestObj.setResultStatus("FAILURE");
            print("Failed to get configuration values from device config file.") 
    else:
        print("Failed to load the ssh params")
        tdkTestObj.setResultStatus("FAILURE"); 
else: 
    print("Failed to load the Rdkv_dab module")
    tdkTestObj.setResultStatus("FAILURE");         
#Initializing device_id
device_id = str(Dab_id.strip())
#Validating all DAB get api responses 
if result_val == expectedResult:
   print("\n All pre conditions executed Successfully")
   print(f"\n{ '*' * 117 }") 
   print("\nInvoking Dab Get API\n")
   print(f"\n{ '*' * 117 }")
   dab_get_response = None 
   dab_get_api= operation_name["dab_get_api"]
   tdkTestObj.setResultStatus("SUCCESS");
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_get_api))
   tdkTestObj.addParameter('device_id',device_id)
   tdkTestObj.executeTestCase(expectedResult)
   result = tdkTestObj.getResultDetails();
   if result is not None:
         dab_get_response = json.loads(result)
   else:
       print("\n DAB perform operation result is empty")
   if dab_get_response is not None and  dab_get_response["status"] == 200:
       print("\n =================================================================================================================== \n")
       print("\n Validating system/settings/get DAB API response with corresponding RDK API responses \n")
       print("\n =================================================================================================================== \n")
       tdkTestObj = obj.createTestStep('validate_get_dab_with_rdk')
       tdkTestObj.addParameter('dab_response',dab_get_response)
       tdkTestObj.executeTestCase(expectedResult)
       dab_get_result = ast.literal_eval(tdkTestObj.getResultDetails());
       Failed_get_result =dab_get_result[1]
       if Failed_get_result:
          print("\n Following get  DAB api validations Failed \n")
          print(f"\nFailed get api  Validations are:{Failed_get_result}.")
          tdkTestObj.setResultStatus("FAILURE");
       else:
           print("\n All Validations for get DAB api passed")
           tdkTestObj.setResultStatus("SUCCESS");
   else:
       print("\n ===================================================================================================================== \n")
       print("\nDevice_info dab_response is empty")
   print("\n *********************************************************************************************************************")
   print("\nInvoking Dab DeviceInfo API\n")
   print("\n *********************************************************************************************************************")
   dab_device_info_api= operation_name["dab_device_info_api"]
   tdkTestObj.setResultStatus("SUCCESS");
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_device_info_api))
   tdkTestObj.addParameter('device_id',device_id)
   tdkTestObj.executeTestCase(expectedResult)
   result = tdkTestObj.getResultDetails();
   if result is not None:
        dab_devinfo_response = json.loads(result)
   else:
      print("\n DAB perform operation result is empty")      
   dev_info_result =None
   if dab_devinfo_response is not None and dab_devinfo_response ["status"] == 200:
       #Validate DAB response against RDK parameters
       print("\n =================================================================================================================== \n")
       print("\n Validating device/info DAB API response with corresponding RDK API responses \n")
       print("\n =================================================================================================================== \n")
       tdkTestObj = obj.createTestStep('validate_device_info_with_rdk')
       tdkTestObj.addParameter('dab_response',dab_devinfo_response)
       tdkTestObj.executeTestCase(expectedResult)
       dev_info_result =ast.literal_eval(tdkTestObj.getResultDetails());
       Failed_dev_info =dev_info_result[1]
       if Failed_dev_info:
          print("\n Following Device info  DAB api validations Failed \n")
          print(f"\nFailed Device info  Validations are: {Failed_dev_info}.")
          tdkTestObj.setResultStatus("FAILURE");
       else:
          print("\n All Validations for Device info DAB api passed")
          tdkTestObj.setResultStatus("SUCCESS");
                         
   else:
       print("\n ===================================================================================================================== \n")
       print("\nDevice_info dab_response is empty")
       tdkTestObj.setResultStatus("FAILURE");
   print("\n********************************************************************************************************************* ")
   print("\nInvoking Dab SettingsList API\n")
   print("\n********************************************************************************************************************* ")
   dab_device_info_api= operation_name["dab_get_settings_list_api"]
   tdkTestObj.setResultStatus("SUCCESS");
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_device_info_api))
   tdkTestObj.addParameter('device_id',device_id)
   tdkTestObj.executeTestCase(expectedResult)
   result = tdkTestObj.getResultDetails();
   if result is not None:
       dab_settinglist_response = json.loads(result)
   else:
       print("\n DAB perform operation result is empty")
   Settingslist_result =[]
   if dab_settinglist_response is not None and dab_settinglist_response["status"] == 200:
       #Validate DAB response against RDK parameters
       print("\n =================================================================================================================== \n")
       print("\n Validating  DAB SettingsList API response with corresponding RDK API responses \n")
       print("\n =================================================================================================================== \n")
       tdkTestObj = obj.createTestStep('validate_settingslist_dab_with_rdk')
       tdkTestObj.addParameter('dab_response',dab_settinglist_response)
       tdkTestObj.executeTestCase(expectedResult)
       result = tdkTestObj.getResult();
       Settingslist_result =ast.literal_eval(tdkTestObj.getResultDetails()); 
       Failed_SettingList =Settingslist_result[1]
       if not Failed_SettingList:
          print("\n All SettingList DAB api validations passed\n")
          tdkTestObj.setResultStatus("SUCCESS");
       else:
           print("\n Following SettingList DAB api validations Failed \n")
           print(f"\nFailed SettingList Validations are :{Failed_SettingList}.")
           tdkTestObj.setResultStatus("FAILURE");

   else:
       print("\n ===================================================================================================================== \n")
       print("\nSettingslist  dab_response is empty")
       tdkTestObj.setResultStatus("FAILURE");
else:
    print("\nPre conditions Failed to execute")
    tdkTestObj.setResultStatus("FAILURE");
# Print the overall test summary
results = [Settingslist_result, dev_info_result, dab_get_result]
print(f"\n{ '*' * 117 }")
print("OverallTest Summary:")
for result, validation_name in zip(results, ["Settingslist", "Device Info", "DAB Get"]): 
  if  result:
      passed = result[0]
      if passed:
         print(f"\n{ '*' * 117 }")
         print(f"\t- All validations for {validation_name} passed.")

      else:
         failed_validations = result[1]
         print(f"\n{ '*' * 117 }")
         print(f"\t-Following Validations for  {validation_name} Failed")
         print("\n Printing the failed validations")
         for validation in failed_validations:
             parameter = validation["parameter"]
             message = validation["message"]
             print(f"\n{ '*' * 117 }")
             print(f"\t\t- Parameter: {parameter}")
             print(f"\t\t- Message: {message}")
  else:
      print(f"\n{ '*' * 117 }")
      print(f"\t- No results for {validation_name}.")
      continue

obj.unloadModule("rdkv_dab");
