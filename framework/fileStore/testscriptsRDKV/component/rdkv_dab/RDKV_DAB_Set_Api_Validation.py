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
  <name>RDKV_DAB_Set_Api_Validation</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <!--  -->
  <primitive_test_version>4</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates all DAB set Api response against RDK values based on configured mappings.,
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
    <test_case_id>RDKV_DAB_04</test_case_id>
    <test_objective>This test validates DAB set Api response against RDK values based on configured mappings.
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
2.Invoke DAB Get Api response and save it as initial response
3.Invoke DAB Settings supported list Api and save the response
4.Now try to set the settings and their values configured in config file for the settings available in supported setting list
5.Once a setting is set using dab set Api, then get new dab get Api response for that setting and compare it with corresponding rdk Api
6.If comparison is successful, the revert the setting to initial value.
7.Print the setting that failed to set.</automation_approch>
    <expected_output>All DAB settings configured should be successfully set using DAB set Api.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_Set_Api_Validation</test_script>
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
obj.configureTestCase(ip,port,'RDKV_DAB_Set_Api_Validation');
# Assinging ip address to broker Ip address
broker_address =ip
device_id = ""
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
print("\nExecuting pre conditions for DAB api validation")
print("\n =================================================================================================================")
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
#Initializing device id
device_id = str(Dab_id.strip())
settings_to_change = {
    "audioVolume": 90,
    "language": "es-ES",
    "cec": True,
    "outputResolution": "{'frequency': 60.0, 'height': 720, 'width': 1280}",# resolution value will be randonly retrived from supported resolutions
    "audioOutputMode": "Auto",#audioOutputMode value will be randonly retrived from supported audioOutputModes
    "mute": True,
    "textToSpeech": True,
    "audioOutputSource": "Optical",
    "hdrOutputMode": "DisableHdr"
}

#Invoking dab_app_launch_with_content api.
failed_settings = []
if result_val == expectedResult:
   dab_get_api= operation_name["dab_get_api"]
   tdkTestObj.setResultStatus("SUCCESS");
   print("\n Pre conditions are executed Successfully")
   # Get initial GET DAB response and save it
   print("\nInvoking  DAB get API.")
   print("============================================================================================")
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_get_api))
   tdkTestObj.addParameter('device_id',device_id)
   tdkTestObj.executeTestCase(expectedResult)
   time.sleep(5)
   result =tdkTestObj.getResultDetails()
   if result is not None:
      initial_get_response_payload = json.loads(result)
   else:
       print("\n DAB perform operation result is empty")
   if initial_get_response_payload is not None and initial_get_response_payload["status"] == 200:
       tdkTestObj.setResultStatus("SUCCESS");
       print("\nInitial GET response payload:", initial_get_response_payload)
       print("\n=========================================================================================================== ")
       # Get SettingsList response and save it
       print("\nGetting DAB supported settings list API response\n")
       dab_get_settings_list_api =  operation_name["dab_get_settings_list_api"]
       tdkTestObj = obj.createTestStep('perform_operation')
       tdkTestObj.addParameter('operation_name',str(dab_get_settings_list_api))
       tdkTestObj.addParameter('device_id',device_id)
       tdkTestObj.executeTestCase(expectedResult)
       result = tdkTestObj.getResultDetails()
       if result is not None:
           supported_settings_list = json.loads(result)
       else:
           print("\n DAB perform operation result is empty")       
       if supported_settings_list:
          print("\nSupported setting list:", supported_settings_list)
          tdkTestObj.setResultStatus("SUCCESS");
          # Parse the initial response to store initial values
          initial_settings = initial_get_response_payload
          changed_settings = []
          # Loop through settings and perform SET operations
          for setting_name, new_value in settings_to_change.items():
              print(f"Setting name: {setting_name}, new value: {new_value}")
              if setting_name in ["outputResolution", "audioOutputMode"]:
                 print("\nentered resolution audiooutputmode validation logic")
                 supported_settings = supported_settings_list.get(setting_name, [])
                 print("supported_settings:",supported_settings)
                 if supported_settings:
                    new_value = random.choice(supported_settings)
                    print("new_value:",new_value)       
                 else:
                    print(f"\nWarning: No supported settings found for '{setting_name}'.")
                    print("\n=========================================================================================================== \n")
                    failed_settings.append(setting_name)
              else:
                  pass
              # Set new value using SET operation
              message_override = {setting_name: new_value}
              print("\n=========================================================================================================== \n")
              print(f"\nGetting DAB set API response for setting '{setting_name}' to '{new_value}':\n")
              dab_set_api =  operation_name["dab_set_api"]
              tdkTestObj = obj.createTestStep('perform_operation')
              tdkTestObj.addParameter('operation_name',str(dab_set_api))
              tdkTestObj.addParameter('message_override',message_override)
              tdkTestObj.addParameter('device_id',device_id)
              tdkTestObj.executeTestCase(expectedResult)
              set_response_payload =json.loads(tdkTestObj.getResultDetails())
              result = tdkTestObj.getResult()
              # Check if SET operation was successfull
              if set_response_payload["status"] == 200:
                 tdkTestObj.setResultStatus("SUCCESS");
                 print("\n=========================================================================================================== \n")
                 print(f"\nSetting '{setting_name}' to '{new_value}' successful!")
                 #Get new get response after setting
                 tdkTestObj = obj.createTestStep('perform_operation')
                 tdkTestObj.addParameter('operation_name',str(dab_get_api))
                 tdkTestObj.addParameter('device_id',device_id)
                 tdkTestObj.executeTestCase(expectedResult)
                 new_get_response_payload = json.loads(tdkTestObj.getResultDetails())
                 result = tdkTestObj.getResult()
                 #Validate the newly set DAB value with RDK API for the current setting
                 tdkTestObj = obj.createTestStep('validate_set_dab_with_rdk')
                 tdkTestObj.addParameter('dab_response',new_get_response_payload)
                 tdkTestObj.addParameter('changed_settings',[setting_name])
                 tdkTestObj.executeTestCase(expectedResult)
                 failed_validations = ast.literal_eval(tdkTestObj.getResultDetails());
                 validation_success = failed_validations[0]
                 failed_set_validations = failed_validations[1]
                 time.sleep(2)  # Allow processing time
                 if validation_success is True:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\n=========================================================================================================== \n")
                    print(f"\nsetting '{setting_name}'  was applied successfully!")
                    # Revert setting back to original value **only if setting was successful**
                    print(f"\nReverting setting '{setting_name}'  to original value.\n")
                    print("\n=========================================================================================================== \n")
                    #changed_settings =  {setting_name: initial_settings[setting_name]}
                    tdkTestObj = obj.createTestStep('revert_settings')
                    tdkTestObj.addParameter('initial_settings',initial_settings)
                    tdkTestObj.addParameter('device_id',device_id)
                    tdkTestObj.addParameter('changed_settings',{setting_name: initial_settings[setting_name]})
                    tdkTestObj.executeTestCase(expectedResult)
                    failed_reverts = ast.literal_eval(tdkTestObj.getResultDetails());
                    revert_success = failed_reverts[0]
                    failed_set_reverts =  failed_reverts[1]
                    if revert_success is True:
                       tdkTestObj.setResultStatus("SUCCESS");
                       print(f"\nReverting setting '{setting_name}'  to original value was successful.\n")
                       print("\n======================================================================================================== \n")
                       # Validate the reverted value with RDK API
                       print("\n Validating the reverted values using Intital Settings\n")
                       print("\n======================================================================================================= \n")
                       changed_settings_value =[setting_name]
                       tdkTestObj = obj.createTestStep('validate_set_dab_with_rdk')
                       tdkTestObj.addParameter('dab_response',initial_settings)
                       tdkTestObj.addParameter('changed_settings',changed_settings_value)
                       tdkTestObj.executeTestCase(expectedResult)
                       revert_validation = ast.literal_eval(tdkTestObj.getResultDetails());
                       failed_revert_validation =revert_validation[1] 
                       if revert_validation[0] is True:
                           tdkTestObj.setResultStatus("SUCCESS");
                           print("\n Revert validation for   setting passed")
                           print("\n===================================================================================================== \n")
                       else:
                           tdkTestObj.setResultStatus("FAILURE");
                           print(f"\nRevert validation failed for {len(failed_revert_validation)} settings:")
                           print("\n===================================================================================================== \n")
                           for validation in failed_revert_validation:
                               print(f"- {validation['parameter']}: {validation['message']}")

                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("\n===================================================================================================== \n")
                        print(f"\nReverting failed for {len(failed_set_reverts)} settings:")
                        for validation in failed_set_reverts:
                            print(f"- {validation['parameter']}: {validation['message']}")
                 else:
                     print(f"\nValidation failed for {len(failed_validations)} settings:")
                     print("\n=========================================================================================================== \n")
                     tdkTestObj.setResultStatus("FAILURE");
                     for validation in failed_set_validations:
                         print(f"- {validation['parameter']}: {validation['message']}")
              else:
                  print("\n=========================================================================================================== \n")
                  print(f"\nSetting '{setting_name}' to '{new_value}' failed!")
                  tdkTestObj.setResultStatus("FAILURE");
                  failed_settings.append(setting_name)
          print("\nCompleted iterating through settings.")
          print("\n=========================================================================================================== \n")

       else:
           print("\n Failed to get SupportedList_response_payload")
           tdkTestObj.setResultStatus("FAILURE");
   else:
       print("\n Failed to get initial_get_response_payload")
       tdkTestObj.setResultStatus("FAILURE");
       exit()
       obj.unloadModule("rdkv_dab");

   print("\n Overall Test Summary")
   print("\n=========================================================================================================== \n")
   if failed_settings is not None:
      print(f"\nThe following settings failed to be set: {failed_settings}")
      print ("[TEST EXECUTION RESULT] : FAILURE]")
      tdkTestObj.setResultStatus("FAILURE");
   else:
      print("\nAll settings were applied successfully!")
      print ("[TEST EXECUTION RESULT] : SUCCESS");
      tdkTestObj.setResultStatus("SUCCESS");
else:
    print("Failed to set up MQTT client. Aborting test script.")
    print ("[TEST EXECUTION RESULT] : FAILURE");
    tdkTestObj.setResultStatus("FAILURE");


obj.unloadModule("rdkv_dab");