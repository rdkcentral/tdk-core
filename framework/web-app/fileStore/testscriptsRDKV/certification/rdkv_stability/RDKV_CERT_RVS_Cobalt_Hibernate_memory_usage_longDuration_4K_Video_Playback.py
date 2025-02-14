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
  <version>15</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_Cobalt_Hibernate_memory_usage_longDuration_4K_Video_Playback</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateProcEntry</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>This test validates memory usage during long-duration 4k video playback while the application is hibernated and restored during playback</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>740</execution_time>
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
    <box_type>Video_Accelerator</box_type>
    <!--  -->
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
    <!--  -->
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_STABILITY_74</test_case_id>
    <test_objective>The objective of this test is to do the stability testing by validating memory usage during long-duration 4k video playback while the cobalt application is hibernated and restored during playback.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>Accelerator</test_setup>
    <pre_requisite> Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. Cobalt_hibernate_test_duration
2.The URL of the 4k video to be played</input_parameters>
    <automation_approch>1. As a pre requisite, disable all the other plugins and enable Cobalt only.
2. Set the URL of 4K video to be played.
3. Validate if the video is playing using proc entries
4. Validate memory usage
5.Hibernate the application and validate the memory usage
6.Restore cobalt and confirm video playback is resumed
7. Revert all values</automation_approch>
    <expected_output>The video should play without interruption for the given time.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_Cobalt_Hibernate_memory_usage_longDuration_4K_Video_Playback</test_script>
    <skipped>No</skipped>
    <release_version>M130</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from BrowserPerformanceUtility import *
import BrowserPerformanceUtility
from rdkv_performancelib import *
import rdkv_performancelib
import StabilityTestVariables
from StabilityTestUtility import *
from SSHUtility import *
from rdkvmemcrlib import*
import re
import ast
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_Hibernate_memory_usage_longDuration_4K_Video_Playback');

#The device will reboot before starting the stability testing if "pre_req_reboot" is
#configured as "Yes".
pre_requisite_reboot(obj)

output_file = '{}{}_{}_{}_MemoryUsageInfo.json'.format(obj.logpath,str(obj.execID),str(obj.execDevId),str(obj.resultId))
json_file = open(output_file,"w")
result_dict_list = []
mem_usage_info_dict = {}
test_interval = 900
result_dict ={}

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status): 
    cobalt_4k_longduration_test_url = StabilityTestVariables.cobalt_4k_longduration_test_url;
    if cobalt_4k_longduration_test_url == "":
        print ("\n Please configure the cobalt_4k_longduration_test_url value\n")   
    browser_test_url = PerformanceTestVariables.browser_test_url
    if browser_test_url == "":
        print ("\n Please configure the browser_test_url value\n")
    print("Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    plugins_list = ["WebKitBrowser","Cobalt","DeviceInfo"]
    plugin_status_needed = {"WebKitBrowser":"deactivated","Cobalt":"resumed","DeviceInfo":"activated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    status = "SUCCESS"
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        status = "FAILURE"
        print("\n Error while getting status of plugins")
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        if plugin_status_needed.get("Cobalt") == "hibernated":
          restore_plugin(obj,"Cobalt")
          time.sleep(5)
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    cobal_launch_status = launch_cobalt(obj)  
    validation_dict = get_validation_params(obj)
    resolution_required_4k = str(StabilityTestVariables.resolution_required_4k)
    supp_resolutions =[];
    set_resolution = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if ssh_param_dict != {} and expectedResult in result:
       tdkTestObj.setResultStatus("SUCCESS")
       print("\n Get the current screen resolution \n")
       tdkTestObj = obj.createTestStep('rdkservice_getValue');
       tdkTestObj.addParameter("method","org.rdk.DisplaySettings.getCurrentResolution");
       tdkTestObj.executeTestCase(expectedResult);
       result = tdkTestObj.getResult();
       curr_resolution = tdkTestObj.getResultDetails();
       curr_resolution_dict = eval(curr_resolution)
       curr_resolution  = curr_resolution_dict.get("resolution")
       print(curr_resolution);
       prev_resolution = curr_resolution
       if resolution_required_4k in curr_resolution :
          print ("\ncurrent resolution is 4k:\n",curr_resolution);
          tdkTestObj.setResultStatus("SUCCESS")
          set_resolution = "SUCCESS"
       else:
          print ("\nCurrent resolution is not 4k:\n");
          print("\n Getting the  supported  resolutions \n")
          tdkTestObj = obj.createTestStep('rdkservice_getValue');
          tdkTestObj.addParameter("method","org.rdk.DisplaySettings.getSupportedResolutions");
          tdkTestObj.executeTestCase(expectedResult);
          supp_resolutions = tdkTestObj.getResultDetails();         
          if resolution_required_4k in supp_resolutions:
             tdkTestObj.setResultStatus("SUCCESS");
             print("\n 4k resolution is Supported\n")
             supp_resolutions_dict = eval(supp_resolutions)
             supp_resolutions  = supp_resolutions_dict.get("supportedResolutions")
             supp_resolutions  = sorted(supp_resolutions)
             print(supp_resolutions)
             resolution_4k = [res for res in supp_resolutions if res.startswith("2160p")]
             # If there are multiple 4K resolutions, take the last one
             if resolution_4k:
                resolution_4k = resolution_4k[-1]
             else:
                resolution_4k = None  # No 4K resolution found
             print("resolution_4k=",resolution_4k)
             print(resolution_4k)
             params ='{\
                       "videoDisplay": "HDMI0",\
                       "resolution": "'+ resolution_4k +'"}'
             print("\n Setting Resolution \n")
             tdkTestObj = obj.createTestStep('rdkservice_setValue')
             tdkTestObj.addParameter("method","org.rdk.DisplaySettings.setCurrentResolution");
             tdkTestObj.addParameter("value",params);        
             tdkTestObj.executeTestCase(expectedResult);
             result = tdkTestObj.getResult();
             if expectedResult in  result:
                tdkTestObj.setResultStatus("SUCCESS")
                print("\n Get the current screen resolution \n")
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method","org.rdk.DisplaySettings.getCurrentResolution");
                tdkTestObj.executeTestCase(expectedResult);
                result = tdkTestObj.getResult();
                curr_resolution = tdkTestObj.getResultDetails();
                print(curr_resolution);
             if curr_resolution != None and expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS");
                print("\n Current resolution is set to 4k\n")
                set_resolution = "SUCCESS"
             else:
                print("\n failed to set 4k Resolution \n")
                set_resolution = "FAILURE"  
    if set_resolution == "SUCCESS" and cobal_launch_status == "SUCCESS" and validation_dict != {} :
        time.sleep(30)
        print("\nPre conditions for the test are set successfully")        
        print("\n Set the URL : {} using Cobalt deeplink method".format(cobalt_4k_longduration_test_url))
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","Cobalt.1.deeplink")
        tdkTestObj.addParameter("value",cobalt_4k_longduration_test_url)
        tdkTestObj.executeTestCase(expectedResult)
        cobalt_result = tdkTestObj.getResult()
        time.sleep(10)
        if(cobalt_result == expectedResult):
            tdkTestObj.setResultStatus("SUCCESS")
            print("Clicking OK to play video")
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            video_start_time = str(datetime.utcnow()).split()[1]
            tdkTestObj.executeTestCase(expectedResult)
            result1 = tdkTestObj.getResult()
            time.sleep(50)
            #Clicking OK to skip Ad
            params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
            tdkTestObj.addParameter("value",params)
            tdkTestObj.executeTestCase(expectedResult)
            result2 = tdkTestObj.getResult()

            time.sleep(30)
            if "SUCCESS" == (result1 and result2):
                tdkTestObj.setResultStatus("SUCCESS")
                test_time_in_mins = int(StabilityTestVariables.cobalt_hibernate_test_duration)
                test_time_in_millisec = test_time_in_mins * 60 * 1000
                time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                iteration = 1
                completed = True
                video_playing =False
                print ("\n Check video is started \n")
                if validation_dict["validation_required"]:
                    if validation_dict["password"] == "None":
                       password = ""
                    else:
                       password = validation_dict["password"]
                    credentials = validation_dict["host_name"]+','+validation_dict["user_name"]+','+password
                    tdkTestObj = obj.createTestStep('rdkservice_validateProcEntry')
                    tdkTestObj.addParameter("sshmethod",validation_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",credentials)
                    tdkTestObj.addParameter("video_validation_script",validation_dict["video_validation_script"])
                    tdkTestObj.executeTestCase(expectedResult)
                    result_val = tdkTestObj.getResultDetails()
                    if result_val == "SUCCESS" :
                        tdkTestObj.setResultStatus("SUCCESS")
                        print("\nVideo playback is happening\n")
                        video_playing = True
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("Video playback is not happening")
                        obj.unloadModule("rdkv_stability");
                        completed =  False
                if video_playing == True:
                    while int(round(time.time() * 1000)) < time_limit:                      
                       print("Calculating memory usage\n")
                       print("Iteration : ", iteration)                       
                       tdkTestObj = obj.createTestStep('memcr_getProcessID')
                       tdkTestObj.addParameter("appname","CobaltImplementation")
                       tdkTestObj.executeTestCase(expectedResult)
                       result = tdkTestObj.getResultDetails()
                       result = ast.literal_eval(result)
                       result = list(result)
                       processID = result[1].strip()
                       if "SUCCESS" in result:
                           tdkTestObj.setResultStatus("SUCCESS")
                           print("SUCCESS : ProceesID retrieval successful\n")
                           tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                           tdkTestObj.addParameter("processID",processID)
                           tdkTestObj.executeTestCase(expectedResult)
                           result = tdkTestObj.getResultDetails()
                           result = ast.literal_eval(result)
                           result = list(result)
                           BeforeHibernate_appusage = result[1].strip()
                           if "SUCCESS" in result:
                               tdkTestObj.setResultStatus("SUCCESS")
                               print("SUCCESS : Memory usage of the app was successfully retrieved before hibernate state\n")
                               time.sleep(10)                                                     
                           else:
                               completed = False
                               print("\n Error while validating memory usage")
                               tdkTestObj.setResultStatus("FAILURE")
                               break                        
                           print("\n Set the cobalt in Hibernate state by suspending it.")
                           print("\nSuspend the Cobalt plugin :\n")
                           launch_status,launch_start_time = launch_plugin(obj,"WebKitBrowser",browser_test_url)
                           time.sleep(10)
                           if launch_status == expectedResult:
                              tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                              tdkTestObj.addParameter("plugin","WebKitBrowser")
                              tdkTestObj.executeTestCase(expectedResult)
                              webkit_status = tdkTestObj.getResultDetails()
                              result = tdkTestObj.getResult()
                              if webkit_status == 'resumed' and expectedResult in result:
                                 print("\n WebKitBrowser resumed successfully")
                                 time.sleep(10)
                                 print("\n Checking Cobalt current state")
                                 tdkTestObj.setResultStatus("SUCCESS")
                                 tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                 tdkTestObj.addParameter("plugin","Cobalt")
                                 tdkTestObj.executeTestCase(expectedResult)
                                 result = tdkTestObj.getResult()
                                 cobalt_status = tdkTestObj.getResultDetails()
                                 if cobalt_status == 'hibernated' and expectedResult in result:
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    time.sleep(5)
                                    print("\nCobalt is in hibernated state")
                                    tdkTestObj = obj.createTestStep('memcr_appMemorySize')
                                    tdkTestObj.addParameter("processID",processID)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResultDetails()
                                    result = ast.literal_eval(result)
                                    result = list(result)
                                    AfterHibernate_appusage = result[1].strip()
                                    if "SUCCESS" in result:
                                         tdkTestObj.setResultStatus("SUCCESS")
                                         print("SUCCESS : Memory usage of the app was successfully retrieved after hibernated state")
                                         AfterHibernate_value = getNumericValue(AfterHibernate_appusage)
                                         BeforeHibernate_value = getNumericValue(BeforeHibernate_appusage)
                                         result_dict["iteration"] = iteration
                                         result_dict["AfterHibernate_value"] = float(AfterHibernate_value)
                                         result_dict["BeforeHibernate_value"] = float(BeforeHibernate_value)
                                         result_dict_list.append(result_dict)
                                         onebytenth_value = float(BeforeHibernate_value)/10
                                         print(f"1/10th value of {BeforeHibernate_appusage} is {onebytenth_value}")
                                         validation =True
                                         if float(AfterHibernate_value) <= onebytenth_value:
                                              tdkTestObj.setResultStatus("SUCCESS")
                                              print("SUCCESS : After hibernating the app, its memory consumption decreased to "+AfterHibernate_appusage+" down from 1/10th of "+BeforeHibernate_appusage+" before suspension\n")
                                         else:
                                              validation =False
                                              tdkTestObj.setResultStatus("FAILURE")
                                              print("FAILURE : After hibernating the app, its memory consumption decreased to "+AfterHibernate_appusage+" up from 1/10th of "+BeforeHibernate_appusage+" before suspension\n")
                                         restore_status,start_restore =restore_plugin(obj,"Cobalt")
                                         if restore_status == expectedResult:                                               
                                               print("\n Cobalt app restored successfully and trying to launch it")
                                               resume_status,start_resume = launch_plugin(obj,"Cobalt")
                                               time.sleep(5)
                                               if resume_status == expectedResult:
                                                   print("\n Cobalt app resumed successfully")
                                                   time.sleep(30)
                                                   print ("\n Check video is resumed \n")
                                                   command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                                                   tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                                                   tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                                   tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                                   tdkTestObj.addParameter("command",command)
                                                   tdkTestObj.executeTestCase(expectedResult)
                                                   result = tdkTestObj.getResult()
                                                   output = tdkTestObj.getResultDetails()
                                                   if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                                                      video_resumed_log = output.split('\n')[1]
                                                      video_play_starttime_in_millisec = getTimeInMilliSec(video_start_time)
                                                      video_played_time = getTimeStampFromString(video_resumed_log)
                                                      video_played_time_in_millisec = getTimeInMilliSec(video_played_time)
                                                      if video_played_time_in_millisec > video_play_starttime_in_millisec:
                                                         print ("\n Video resumed Playing\n")
                                                         video_playing = True
                                                         tdkTestObj.setResultStatus("SUCCESS")
                                                      else:
                                                          print ("\n Video has not resumed after cobalt restore. \n")
                                                          tdkTestObj.setResultStatus("FAILURE")
                                                          completed =  False
                                                          break
                                                      iteration += 1
                                                      time.sleep(test_interval)
                                                   else:
                                                      print ("\n Video play related logs are not available after resume \n")
                                                      tdkTestObj.setResultStatus("FAILURE")
                                               else:
                                                  print("\n Failed to resume cobalt application")
                                                  tdkTestObj.setResultStatus("FAILURE")
                                         else:
                                              print("\n Failed to restore cobalt application")
                                              tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                       tdkTestObj.setResultStatus("FAILURE")
                                       print("FAILURE ; Failed to retrieve memory usage of the app after hibernated state\n")
                                 else:
                                     tdkTestObj.setResultStatus("FAILURE")
                                     print("FAILURE ; cobalt is not in  hibernated state\n")
                    
                    if(completed):
                        print("\nsuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins))
                        mem_usage_info_dict["memoryUsageDetails"] = result_dict_list
                        json.dump(mem_usage_info_dict,json_file)
                        json_file.close()
        else:
            print("Unable to launch the url")
            tdkTestObj.setResultStatus("FAILURE")
            print("\n Exit from Cobalt \n")
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin","Cobalt")
            tdkTestObj.addParameter("status","deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
        if result == "SUCCESS":
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            print("Unable to deactivate Cobalt")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print("Revert the values before exiting")
        params ='{\
                       "videoDisplay": "HDMI0",\
                       "resolution": "'+ prev_resolution +'"}'
        print("\n Setting Resolution \n")
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method","org.rdk.DisplaySettings.setCurrentResolution");
        tdkTestObj.addParameter("value",params);
        tdkTestObj.executeTestCase(expectedResult);
        result = tdkTestObj.getResult();
        if expectedResult in  result:
           tdkTestObj.setResultStatus("SUCCESS")
           print("\n Get the current screen resolution \n")
           tdkTestObj = obj.createTestStep('rdkservice_getValue');
           tdkTestObj.addParameter("method","org.rdk.DisplaySettings.getCurrentResolution");
           tdkTestObj.executeTestCase(expectedResult);
           result = tdkTestObj.getResult();
           curr_resolution = tdkTestObj.getResultDetails();
           print(curr_resolution);
        if curr_resolution != None and expectedResult in result:
           tdkTestObj.setResultStatus("SUCCESS");
           print("\n Previous resolution is set \n")        
        else:
           print("\n failed to set Previous Resolution \n")
           tdkTestObj.setResultStatus("FAILURE")

        status = set_plugins_status(obj,curr_plugins_status_dict)
        post_condition_status = check_device_state(obj)
        obj.unloadModule("rdkv_stability");
        if(completed):
            print("\n#################ExecutionSummary##################")
            print("\nSuccessfully completed the {} times in {} minutes".format(iteration,test_time_in_mins))
        else:
            print("\n Failed to complete the execution")
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
