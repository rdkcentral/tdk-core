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
  <version>9</version>
  <name>RDKV_DAB_Input_keys_Validation</name>
  <primitive_test_id/>
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <primitive_test_version>4</primitive_test_version>
  <status>FREE</status>
  <synopsis>This tests validate DAB input key press API's</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>Rdkv_dab_05</test_case_id>
    <test_objective>This test validates DAB input key response using screenshot utility lib</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.DAB adapter service should be up and running in box</pre_requisite>
    <api_or_interface_used>DAB
Screenshot Utility</api_or_interface_used>
    <input_parameters>1.Device_Id
2.Broker_port address
3.Operation_name
4.Dab response</input_parameters>
    <automation_approch>1.As pre-requisite we have to make sure dab service is up and running
2.Invoke DAB Input key Api's .
3.Validate the response using Screenshot Utility lib
3.</automation_approch>
    <expected_output>The DAB input key response should be successful, and its response should be successfully validated using the screenshot utility</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_Input_keys_Validation</test_script>
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
import ast
from saveAsPng import *
from tdkvScreenShotUtility import *
from rialto_containerlib import *
from tdkvScreenShotUtility import *
from rdkv_dablib import *
from dab_config import *
from rdkvmemcrlib import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_dab","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_DAB_Input_keys_Validation');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
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
dab_get_result =[]
#Validating all DAB get api responses 
if result_val == expectedResult:
   print("\n All pre conditions executed Successfully")
   print(f"\n{ '*' * 117 }") 
   print("\nLaunching Youtube App\n")
   print(f"\n{ '*' * 117 }")
   dab_app_launch = operation_name["dab_app_launch"]
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_app_launch))
   tdkTestObj.addParameter('device_id',device_id)
   message_override = {"appId":"YouTube"}
   tdkTestObj.addParameter('message_override',message_override)
   tdkTestObj.executeTestCase(expectedResult)
   time.sleep(6)
   result  = tdkTestObj.getResult() ;
   print("result:",result)
   if result:
       end_verify =False
       screenshot = getScreenShot(obj)
       print("\n ====================================================================================================")
       print("\n Performing screenshot to handle app sign-in page")
       print("\n ====================================================================================================")
       if screenshot != "FAILURE" :
           isBlack = is_image_black(screenshot)# validating if screenshot captured is Blank
           if not isBlack:
              verified = verifyTextInImage("youtube_signin_experience",screenshot)
              print("verification step1:youtube_signin_experience")
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
                  print("verification step2:youtube_signin")
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
                  print("verification step3:youtube_accntpg")
                  screenshot = getScreenShot(obj)
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
                 print("verification step4:youtube_homepage")
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
       print("verification step5:YT_template")
       verified = verifyImageTemplate("youtube_icon_logo",screenshot)
       if result == "SUCCESS" and not isBlack and verified != False:
          tdkTestObj.setResultStatus("SUCCESS");
          print(f"\nDAB  YouTube app launched successfully")
          time.sleep(20)
          dab_key_press =  operation_name["dab_key_press"]
          message_override ={"keyCode": "KEY_LEFT"}
          tdkTestObj = obj.createTestStep('perform_operation')            
          tdkTestObj.addParameter('operation_name',str(dab_key_press))
          tdkTestObj.addParameter('message_override',message_override)
          tdkTestObj.addParameter('device_id',device_id)
          tdkTestObj.executeTestCase(expectedResult)
          key_response =json.loads(tdkTestObj.getResultDetails())
          result = tdkTestObj.getResult()
          if key_response is not None and  key_response["status"] == 200:
             tdkTestObj.setResultStatus("SUCCESS")
             print("\n =================================================================================================================== \n")
             print("\n Validating input/keypress DAB API response with corresponding RDK API responses \n")
             print("\n =================================================================================================================== \n")
             screenshot = getScreenShot(obj)
             verified = verifyImageTemplate("youtube_home_icon",screenshot)
             if  result == "SUCCESS" and verified!= False:
                 tdkTestObj.setResultStatus("SUCCESS")
                 print("KEY_LEFT is verified and Home icon is highlighted")
                 dab_key_press =  operation_name["dab_key_press"]
                 message_override ={"keyCode": "KEY_UP"}
                 tdkTestObj = obj.createTestStep('perform_operation')
                 tdkTestObj.addParameter('operation_name',str(dab_key_press))
                 tdkTestObj.addParameter('message_override',message_override)
                 tdkTestObj.addParameter('device_id',device_id)
                 tdkTestObj.executeTestCase(expectedResult)
                 key_response =json.loads(tdkTestObj.getResultDetails())
                 result = tdkTestObj.getResult()
                 screenshot = getScreenShot(obj)
                 verified = verifyImageTemplate("youtube_search_icon",screenshot)
                 if  result == "SUCCESS" and verified!= False:
                      tdkTestObj.setResultStatus("SUCCESS")
                      print("KEY_UP is verified and Search icon is highlighted")                
                      dab_key_press =  operation_name["dab_key_press"]
                      message_override ={"keyCode": "KEY_DOWN"}
                      tdkTestObj = obj.createTestStep('perform_operation')
                      tdkTestObj.addParameter('operation_name',str(dab_key_press))
                      tdkTestObj.addParameter('message_override',message_override)
                      tdkTestObj.addParameter('device_id',device_id)
                      tdkTestObj.executeTestCase(expectedResult)
                      key_response =json.loads(tdkTestObj.getResultDetails())
                      result = tdkTestObj.getResult()
                      dab_key_press =  operation_name["dab_key_press"]
                      message_override ={"keyCode": "KEY_DOWN"}
                      tdkTestObj = obj.createTestStep('perform_operation')
                      tdkTestObj.addParameter('operation_name',str(dab_key_press))
                      tdkTestObj.addParameter('message_override',message_override)
                      tdkTestObj.addParameter('device_id',device_id)
                      tdkTestObj.executeTestCase(expectedResult)
                      key_response =json.loads(tdkTestObj.getResultDetails())
                      result = tdkTestObj.getResult()                      
                      screenshot = getScreenShot(obj)
                      verified = verifyImageTemplate("youtube_gaming_icon",screenshot)
                      if  result == "SUCCESS" and verified!= False:
                          tdkTestObj.setResultStatus("SUCCESS")
                          print("Gaming page is launched ")
                          dab_key_press =  operation_name["dab_key_press"]
                          message_override ={"keyCode": "KEY_RIGHT"}
                          tdkTestObj = obj.createTestStep('perform_operation')
                          tdkTestObj.addParameter('operation_name',str(dab_key_press))
                          tdkTestObj.addParameter('message_override',message_override)
                          tdkTestObj.addParameter('device_id',device_id)
                          tdkTestObj.executeTestCase(expectedResult)
                          key_response =json.loads(tdkTestObj.getResultDetails())
                          result = tdkTestObj.getResult()
                          screenshot = getScreenShot(obj)
                          if  result == "SUCCESS" :
                              dab_key_press =  operation_name["dab_key_press"]
                              message_override ={"keyCode": "KEY_ENTER"}
                              tdkTestObj = obj.createTestStep('perform_operation')
                              tdkTestObj.addParameter('operation_name',str(dab_key_press))
                              tdkTestObj.addParameter('message_override',message_override)
                              tdkTestObj.addParameter('device_id',device_id)
                              tdkTestObj.executeTestCase(expectedResult)
                              key_response =json.loads(tdkTestObj.getResultDetails())
                              result = tdkTestObj.getResult()
                              if  result == "SUCCESS" :
                                  print("Check whether Video is playing")
                                  log_verification = False
                                  tdkTestObj = obj.createTestStep('checkPROC')
                                  tdkTestObj.executeTestCase(expectedResult);
                                  result = tdkTestObj.getResultDetails();
                                  print("AV status result",result)
                                  if "NOT_ENABLED" in result:
                                      print("PROC_ENTRY validation is disabled , checking wpeframeowrk.log for video validation")
                                      log_verification = True
                                  elif "FAILURE" in result:
                                       print("AV status not proper as proc entry validation failed")
                                       tdkTestObj.setResultStatus("FAILURE")
                                  else:
                                     print("\n ====================================================================================================")
                                     print("\n Youtube is video  is playing sucessfully")
                                     print("\n ==================================================================================================")
                                     tdkTestObj.setResultStatus("SUCCESS")
                                  if result == "SUCCESS":
                                      time.sleep(60)
                                      dab_key_press =  operation_name["dab_key_press"]
                                      message_override ={"keyCode": "KEY_PLAY_PAUSE"}
                                      tdkTestObj = obj.createTestStep('perform_operation')
                                      tdkTestObj.addParameter('operation_name',str(dab_key_press))
                                      tdkTestObj.addParameter('message_override',message_override)
                                      tdkTestObj.addParameter('device_id',device_id)
                                      tdkTestObj.executeTestCase(expectedResult)
                                      key_response =json.loads(tdkTestObj.getResultDetails())
                                      result = tdkTestObj.getResult()
                                      print("key_response:",key_response)
                                      screenshot = getScreenShot(obj)
                                      if result =="SUCCESS":
                                          tdkTestObj.setResultStatus("SUCCESS")
                                          tdkTestObj = obj.createTestStep('checkPROC')
                                          tdkTestObj.addParameter("check_pause","True")
                                          tdkTestObj.executeTestCase(expectedResult);
                                          result = tdkTestObj.getResultDetails();
                                          print("AV status result",result)
                                          if "NOT_ENABLED" in result:
                                              print("PROC_ENTRY validation is disabled , checking wpeframeowrk.log for video validation")
                                              log_verification = True
                                          elif "FAILURE" in result:
                                                 print("AV status not proper as proc entry validation failed")
                                                
                                          else:
                                              print("\n =========================================================================================")
                                              print("\n Youtube is video  is paused sucessfully")
                                              print("\n =========================================================================================")
                                              tdkTestObj.setResultStatus("SUCCESS")
                                          if not paused:
                                              print("Video is not paused, exiting with failure message")
                                              tdkTestObj.setResultStatus("FAILURE")                                              
                                              print("Closing youtube Application")
                                              dab_app_exit = operation_name["dab_app_exit"]
                                              tdkTestObj = obj.createTestStep('perform_operation')
                                              tdkTestObj.addParameter('operation_name',str(dab_app_exit))
                                              tdkTestObj.addParameter('device_id',device_id)
                                              message_override = {"appId":"YouTube"}
                                              tdkTestObj.addParameter('message_override',message_override)
                                              tdkTestObj.executeTestCase(expectedResult)
                                              result = tdkTestObj.getResultDetails();
                                              dab_app_exit_status =json.loads(result)
                                              if dab_app_exit_status["status"] == 200 and dab_app_exit_status["state"]=="STOPPED":
                                                  print("Youtube App exited succesfully")
                                                  tdkTestObj.setResultStatus("SUCCESS")
                                              else:
                                                  print("Failed to exit Youtube App")
                                                  tdkTestObj.setResultStatus("FAILURE");
                                      else:
                                          print("Failed to execute dab playpuase key operation")
                                          tdkTestObj.setResultStatus("FAILURE");
                              else:
                                  print("Failed to execute dab enter key operation")
                                  tdkTestObj.setResultStatus("FAILURE");
                          else:
                              print("Failed to execute dab right key operation") 
                              tdkTestObj.setResultStatus("FAILURE"); 
                      else:
                          print("Failed to execute dab down key operation")                              
                          tdkTestObj.setResultStatus("FAILURE");
                 else:
                     print("Failed to execute dab up  key operation")
                     tdkTestObj.setResultStatus("FAILURE");
             else:
                 print("Failed to validate youtube_home_icon")
                 tdkTestObj.setResultStatus("FAILURE");
          else:
             print("Failed to execute dab left key operation") 
             tdkTestObj.setResultStatus("FAILURE");                                       
       else:
           print("YouTube homepage not Launched")
           tdkTestObj.setResultStatus("FAILURE");
   else:
       print("Failed to launch youtube app successfully")
       tdkTestObj.setResultStatus("FAILURE");
else:
    print("Failed to execute preconditions successfully")
    tdkTestObj.setResultStatus("FAILURE");

obj.unloadModule("rdkv_dab");
