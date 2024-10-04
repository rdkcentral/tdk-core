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
  <version>3</version>
  <name>RDKV_DAB_AppLaunch_API_Validation</name>
  <primitive_test_id/>
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <primitive_test_version>4</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test validates the all supported DAB app launch api .</synopsis>
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
    <test_case_id>Rdkv_dab_01</test_case_id>
    <test_objective>In this test we validate whether all supported DAB application is successfully launching with the help of DAB Api's.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.DAB adapter service should be up and running in box</pre_requisite>
    <api_or_interface_used>DAB</api_or_interface_used>
    <input_parameters>1.Device_Id
2.Operation_name
3.broker_port</input_parameters>
    <automation_approch>1. As pre-requisite we have to make sure dab service is up and running
2.Get all supported DAB apps list and compare with list configured in device config file
3.Lauch them one by one using DAB Api's
4.Handle any sign in issues using screenshot validation
5.verify the app launch is successful</automation_approch>
    <expected_output>All DAB apps in supported list should be launched successfully without fail.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_AppLaunch_API_Validation</test_script>
    <skipped>No</skipped>
    <release_version>M128</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script 
import tdklib; 
import rdkv_performancelib
import json
from saveAsPng import *
from tdkvScreenShotUtility import *
from rialto_containerlib import *
from rdkv_dablib import *
from dab_config import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_dab","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_DAB_AppLaunch_API_Validation');
# Assinging ip address to broker Ip address
broker_address =ip
device_id = ""
failed_apps =[]
Passed =True
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
#Validating the preconditions
print("\nExecuting pre conditions")
print("\n==============================================================================================================")
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
                      print(f"Extracted Device ID: {Dab_id}")
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
                      print("Failed to setup mqtt client")
               else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print("Failed to restart rdkv dab adapter")
            else:
                tdkTestObj.setResultStatus("FAILURE");
                print("Failed to enable dab adapter")
        else:
            print("Failed to get config valu from device config file")
else:
    print("Failed to load rdkv dab module")
    tdkTestObj.setResultStatus("FAILURE");
#Initializing device_id
device_id = str(Dab_id.strip())
# Validating DAB App launch APi by launching all dab supported applications.
if result_val == expectedResult:
   dab_app_list=operation_name["dab_app_list"]
   tdkTestObj.setResultStatus("SUCCESS");
   print("\n All pre conditions executed Successfully")
   print(f"\n{ '*' * 117 }")
   print("\nFetching Device DAB supported App list")
   print("============================================================================================")
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_app_list))
   tdkTestObj.addParameter('device_id',device_id)
   tdkTestObj.executeTestCase(expectedResult)
   result = tdkTestObj.getResultDetails();
   dab_app_supp_list =json.loads(result)

   if dab_app_supp_list["status"] == 200:
       print("\ndab_app_supp_list:",dab_app_supp_list)
       dab_app_set = set(app['appId'] for app in dab_app_supp_list['applications'])
       conf_file,result = getConfigFileName(tdkTestObj.realpath)
       result1, supported_apps = getDeviceConfigKeyValue(conf_file,"DAB_SUPPORTED_APPS")
       supported_app_set =  ast.literal_eval(supported_apps)
       print("supported_app_set:",supported_app_set,"dab_app_set:",dab_app_set)
       if dab_app_set == supported_app_set:
          tdkTestObj.setResultStatus("SUCCESS");
          print("\nApps in both expected and actulal list are same!")
       else:
          print("\nApps in both expected and actulal list are different!")
       for app in dab_app_supp_list['applications']:
            print(f"\nTrying to launch  {app['appId']} App.")
            print("============================================================================================")
            dab_app_launch = operation_name["dab_app_launch"]
            tdkTestObj = obj.createTestStep('perform_operation')
            tdkTestObj.addParameter('operation_name',str(dab_app_launch))
            tdkTestObj.addParameter('device_id',device_id)
            message_override = {"appId": app['appId']}
            tdkTestObj.addParameter('message_override',message_override)
            tdkTestObj.executeTestCase(expectedResult)
            time.sleep(4)
            result  = tdkTestObj.getResult()
            if result:
                end_verify =False
                screenshot = getScreenShot(obj)
                print("\n ====================================================================================================")
                print("\n Performing screenshot to handle app sign-in page")
                print("\n ====================================================================================================")
                if screenshot != "FAILURE" :
                   isBlack = is_image_black(screenshot)# validating if screenshot captured is Blank
                   if not isBlack:
                      if app['appId']=="YouTube":
                         verified = verifyTextInImage("youtube_signin_experience",screenshot)
                         if verified:
                            print("YouTube sign-in experience page launched")
                            params = '{"keys":[ {"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
                            tdkTestObj = obj.createTestStep('rdkservice_setValue')
                            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                            tdkTestObj.addParameter("value",params)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            end_verify =True
                         if not end_verify:
                            verified = verifyImageTemplate("youtube_signin", screenshot)
                            if verified:
                               print("YouTube sign-in page launched")
                               params = '{"keys":[ {"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
                               tdkTestObj = obj.createTestStep('rdkservice_setValue')
                               tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                               tdkTestObj.addParameter("value",params)
                               tdkTestObj.executeTestCase(expectedResult)
                               result = tdkTestObj.getResult()
                               end_verify =True
                         if not end_verify :
                             verified = verifyTextInImage("youtube_account_page", screenshot)
                             if verified:
                                print("YouTube Account page sign-in launched")
                                params = '{"keys":[ {"keyCode": 39,"modifiers": [],"delay":2.0},{"keyCode": 39,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                                tdkTestObj.addParameter("value",params)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                end_verify = True
                         if end_verify:
                             screenshot = getScreenShot(obj)
                             print("\n ====================================================================================================")
                             print("\n Performing screenshot to validate launch of youtube homepage")
                             print("\n ====================================================================================================")
                             verified = verifyTextInImage("youtube_homepage_signin", screenshot)
                         if verified:
                             print("YouTube home page sign-in launched")
                         else:
                             print("YouTube home page sign-in not launched")
                   else:
                       print("Screenshot captured is blank")
                       tdkTestObj.setResultStatus("FAILURE");

                else:
                     print("Failed to capture screenshot\n")
                     tdkTestObj.setResultStatus("FAILURE");
                # Validating App Launch
                verified = verifyImageTemplate(app['appId'],screenshot)
                if result == "SUCCESS"   and not isBlack and verified != False:
                   tdkTestObj.setResultStatus("SUCCESS");
                   print(f"\nDAB App  {app['appId']} launched successfully")
                   time.sleep(20)
                   print(f"\nTrying to get {app['appId']} DAB current Application status")
                   print("============================================================================================")
                   dab_app_state = operation_name["dab_app_state"]
                   tdkTestObj = obj.createTestStep('perform_operation')
                   tdkTestObj.addParameter('operation_name',str(dab_app_state))
                   tdkTestObj.addParameter('device_id',device_id)
                   message_override = {"appId": app['appId']}
                   tdkTestObj.addParameter('message_override',message_override)
                   tdkTestObj.executeTestCase(expectedResult)
                   result = tdkTestObj.getResultDetails();
                   dab_app_state =json.loads(result)
              
                   if dab_app_state["status"] == 200 and dab_app_state["state"] == "FOREGROUND":
                      tdkTestObj.setResultStatus("SUCCESS");
                      print(f"\nCurrent APP status of {app['appId']} is: ",dab_app_state["state"])
                      print(f"\nTrying to get {app['appId']} exit status")
                      print("============================================================================================")
                      dab_app_exit = operation_name["dab_app_exit"]
                      tdkTestObj = obj.createTestStep('perform_operation')
                      tdkTestObj.addParameter('operation_name',str(dab_app_exit))
                      tdkTestObj.addParameter('device_id',device_id)
                      message_override = {"appId": app['appId']}
                      tdkTestObj.addParameter('message_override',message_override)
                      tdkTestObj.executeTestCase(expectedResult)
                      result = tdkTestObj.getResultDetails();
                      dab_app_exit_status =json.loads(result)
                      if dab_app_exit_status["status"] == 200 and dab_app_exit_status["state"]=="STOPPED":
                         tdkTestObj.setResultStatus("SUCCESS");
                         print(f"\nDAB App {app['appId']} exitted successfully:",dab_app_exit_status["state"])
                         print("============================================================================================")
                      else:
                          tdkTestObj.setResultStatus("FAILURE");
                          print(f"\nFailed to exit  {app['appId']} :",dab_app_exit_status)
                   else:
                       tdkTestObj.setResultStatus("FAILURE");
                       print(f"\nFailed to get current application state of  {app['appId']} :",dab_app_state)
                
                else:
                   tdkTestObj.setResultStatus("FAILURE");
                   print(f"\nFailed to launch app {app['appId']}")
                   Passed = False  
                   failed_apps.append(app['appId'])
   else:
       print("Failed to get dab app supported list response")
       tdkTestObj.setResultStatus("FAILURE");
else:
    print("Failed to execute all preconditions successfully")



#Overall summary
if Passed:
    print("All tests passed!")
else:
    print(f"Tests failed for apps: {', '.join(failed_apps)}")
obj.unloadModule("rdkv_dab");









