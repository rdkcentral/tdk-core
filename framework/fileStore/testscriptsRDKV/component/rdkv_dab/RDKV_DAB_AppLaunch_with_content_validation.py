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
  <version>2</version>
  <name>RDKV_DAB_AppLaunch_with_content_validation</name>
  <primitive_test_id/>
  <primitive_test_name>setup_mqtt_client</primitive_test_name>
  <primitive_test_version>4</primitive_test_version>
  <status>FREE</status>
  <synopsis>This test validates all the supported DAB app launch and play the content using DAB Api.</synopsis>
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
    <test_case_id>RDKV_DAB_02</test_case_id>
    <test_objective>In this test we validate whether all supported DAB application is successfully launching with the content configured using DAB Api's.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1.DAB adapter service should be up and running in the box</pre_requisite>
    <api_or_interface_used>DAB</api_or_interface_used>
    <input_parameters>1.Device_Id
2.Operation_name
3.broker_port
</input_parameters>
    <automation_approch>1. As pre-requisite we have to make sure dab service is up and running
2.Get all supported DAB apps list and compare with list configured in device config file
3.Launch them one by one using DAB Api's to launch with content
4.Handle any sign in issues using screenshot validation
5.verify the app launch is successful using checkPROC method</automation_approch>
    <expected_output>1.Apps launched using DAB launch app with content API should successfully launch the app and play video that is configured</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_dab</test_stub_interface>
    <test_script>RDKV_DAB_AppLaunch_with_content_validation</test_script>
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
from tdkvScreenShotUtility import *
from rdkv_dablib import *
from dab_config import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_dab","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_DAB_AppLaunch_with_content_validation');
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

#Invoking dab_app_launch_with_content api.
if result_val == expectedResult:
   dab_app_launch_with_content = operation_name["dab_app_launch_with_content"]
   tdkTestObj.setResultStatus("SUCCESS");
   print("\n Pre conditions are executed Successfully")
   print("\nInvoking DAB App launch with content Api")
   print("============================================================================================")
   tdkTestObj = obj.createTestStep('perform_operation')
   tdkTestObj.addParameter('operation_name',str(dab_app_launch_with_content))
   tdkTestObj.addParameter('device_id',device_id)
   message_override =  {"appId": "YouTube", "contentId": "79XS4qpRw50"}
   tdkTestObj.addParameter('message_override',message_override)
   tdkTestObj.executeTestCase(expectedResult)
   time.sleep(5)
   launch_response = tdkTestObj.getResultDetails();
   result = tdkTestObj.getResult()
   video_start_time = str(datetime.utcnow()).split()[1]
   end_verify =False
   isBlack = False
   verified =False
   screenshot = None
   if expectedResult in result.upper() :
      tdkTestObj.setResultStatus("SUCCESS")
      print ("\n Check video is started \n")
      command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
      tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
      tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
      tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
      tdkTestObj.addParameter("command",command)
      tdkTestObj.executeTestCase(expectedResult)
      result = tdkTestObj.getResult()
      output = tdkTestObj.getResultDetails()
      if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
         video_playing_log = output.split('\n')[1]
         video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
         video_played_time=extract_timestamp(video_playing_log)         
         video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
         if video_played_time_in_millisec > video_play_starttime_in_millisec:
            print("\n ====================================================================================================")
            print("\n Youtube is launched and video started playing")
            print("\n ====================================================================================================") 
            tdkTestObj.setResultStatus("SUCCESS")            
            end_verify = True
            verified =True
            obj.unloadModule("rdkv_dab");
            exit()
         else:
             print("\nVideo is not playing moving to next stage of skipping youtube sign in pages")
             verified =True
      else:
          print("\nVideo related logs are not present  moving to next step")
          verified =True
   if not end_verify :  
      print("\n =====================================================================================================")
      print("\n Performing screenshot to handle youtube signin pages ")
      print("\n ====================================================================================================")
      screenshot = getScreenShot(obj)
      if screenshot != "FAILURE":
        isBlack = is_image_black(screenshot)# validating if screenshot captured is Blank
        if not isBlack:
           verified = verifyTextInImage("youtube_signin_experience",screenshot)
           if verified:
              print("\nYouTube sign-in experience page launched")
              params = '{"keys":[ {"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
              tdkTestObj = obj.createTestStep('rdkservice_setValue')
              tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
              tdkTestObj.addParameter("value",params)
              tdkTestObj.executeTestCase(expectedResult)
              result = tdkTestObj.getResult()
              end_verify =True
              screenshot = getScreenShot(obj)
           if not end_verify:
             verified = verifyTextInImage("youtube_signin", screenshot)
             if verified:
                print("\nYouTube sign-in page launched")
                params = '{"keys":[ {"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 40,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                end_verify =True
                screenshot = getScreenShot(obj)
           if not end_verify :
             verified = verifyTextInImage("youtube_account_page", screenshot)  
             if verified:
                  print("\nYouTube account page sign-in launched")
                  params = '{"keys":[ {"keyCode": 39,"modifiers": [],"delay":2.0},{"keyCode": 39,"modifiers": [],"delay":2.0},{"keyCode": 13,"modifiers": [],"delay":2.0}]}'
                  tdkTestObj = obj.createTestStep('rdkservice_setValue')
                  tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                  tdkTestObj.addParameter("value",params)
                  tdkTestObj.executeTestCase(expectedResult)
                  result = tdkTestObj.getResult()
                  screenshot = getScreenShot(obj)        
        else:
           print("Screenshot captured is blank")           
      else:
         print("Failed to capture screenshot\n")
         tdkTestObj.setResultStatus("FAILURE")
      print("\n =====================================================================================================")
      print("\n Screenshot validation completed")
      print("\n ====================================================================================================")
else:
  print("Failed to execute preconditions successfully")
  tdkTestObj.setResultStatus("FAILURE");
# Validate the video play using CheckPROC function.
isBlack = is_image_black(screenshot)
if isBlack and verified != False:
   tdkTestObj.setResultStatus("SUCCESS");
   print("\n ====================================================================================================")
   print("\nValidating whether the video is paying")
   log_verification = False
   tdkTestObj = obj.createTestStep('checkPROC')
   tdkTestObj.executeTestCase(expectedResult);
   result = tdkTestObj.getResultDetails();
   print("AV status result",result)
   if "NOT_ENABLED" in result:
      print("PROC_ENTRY validation is disabled , checking wpeframeowrk.log for video validation")
      log_verification = True
   elif "FAILURE" in result:
        print("\n Youtube is launched and video  is not playing")
        print("AV status not proper as proc entry validation failed")
        tdkTestObj.setResultStatus("FAILURE")
   else:
       print("\n =====================================================================================================")
       print("\n Youtube is launched and video  is playing sucessfully")
       print("\n ====================================================================================================")
       tdkTestObj.setResultStatus("SUCCESS")
obj.unloadModule("rdkv_dab");
