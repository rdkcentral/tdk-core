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
  <version>3</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_PVS_LightningApp_Video_Playback_Without_Crash_WithWebinspect</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id> </primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_getValue</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The Objective of the test is to check for any crashes for the Lightning application by keeping the 
 web inspect port open for play and pause operations of mp4 video</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>100</execution_time>
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
    <test_case_id>RDKV_PERFORMANCE_161</test_case_id>
    <test_objective>The Objective of the test is to check for any crashes for the Lightning application by keeping the web inspect port open for play and pause operations of mp4 video</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. As a prerequisite disable all other plugins and enable web kit instance plugin.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.</input_parameters>
    <automation_approch>1.Open Lightning app web inspect port
2. Set the application URL in lightning app
3. Play and pause the video from the application
4.Check for any crashes during playback</automation_approch>
    <expected_output>video playback should happen with out crash</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_LightningApp_Video_Playback_Without_Crash_WithWebinspect</test_script>
    <skipped>No</skipped>
    <release_version>M132</release_version>
    <remarks></remarks>
  </test_cases>
  <script_tags />
</xml>
'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from web_socket_util import *
import PerformanceTestVariables
import MediaValidationVariables
from MediaValidationUtility import *
from StabilityTestUtility import *
from rdkv_performancelib import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_LightningApp_Video_Playback_Without_Crash_WithWebinspect');
deviceIP =str(ip)
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
webkit_console_socket = None
webinspect_launched = True
memory_usage = []
result_dict_list =[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    conf_file, status = get_configfile_name(obj);
    result, logging_method = getDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
    setDeviceConfigFile(conf_file)
    videoURL  = MediaValidationVariables.video_src_url_mp4
    videoURL_type = "mp4"
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    setURLArgument("tmUrl",str(obj.url)+"/")  
    test_duration_in_seconds = 1800
    setOperation("close",test_duration_in_seconds)    
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("options","looptest")
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    video_test_urls = []
    players_list = str(MediaValidationVariables.codec_mp4).split(",")
    print("SELECTED PLAYERS: ", players_list)
    # Getting the complete test app URL
    video_test_urls = getTestURLs(players_list,appArguments)
    print("\n Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    crash_Validation = False
    crash_iteration = None                       
    driver = None    
    set_method = "LightningApp"+'.1.url'
    webinspect_port =str(PerformanceTestVariables.lightning_app_webinspect_port)
    plugins_list = ["Cobalt","LightningApp"]
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
    plugin_status_needed = {"Cobalt":"deactivated","LightningApp":"resumed"}
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\n Error while getting plugin status")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        set_status = set_plugins_status(obj,plugin_status_needed)
        new_plugins_status = get_plugins_status(obj,plugins_list)
        if new_plugins_status != plugin_status_needed:
            status = "FAILURE"
    if status == "SUCCESS":
        print("\n Pre conditions for the test are set successfully");        
        print("\n Get the URL in LightningApp")
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
            time.sleep(60)            
            print("\n Current URL:",current_url)
            original_url = video_test_urls[0]
            video_test_url_new = original_url[:original_url.find("&url=")] +"&url="+ '%22%22'+'"'
            print("\n Set LightningApp Application URL 1")
            tdkTestObj = obj.createTestStep('rdkservice_setValue');
            tdkTestObj.addParameter("method",set_method);
            tdkTestObj.addParameter("value",video_test_url_new);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                tdkTestObj.addParameter("realpath",obj.realpath)
                tdkTestObj.addParameter("deviceIP",obj.IP)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                print("\n Validate if the URL is set successfully or not")                
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                if new_url in video_test_url_new:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\n URL(",new_url,") is set successfully")                    
                    webinspectURL = 'http://'+deviceIP+':'+webinspect_port+'/Main.html?ws='+deviceIP+':'+webinspect_port+'/socket/1/1/WebPage'
                    print (webinspectURL)
                    try:                      
                       driver = openChromeBrowser(webinspectURL);
                       if driver != "EXCEPTION OCCURRED":
                          time.sleep(20)                          
                          print("\Webinspect page in device  launched successfully\n")  
                       else:
                           raise RuntimeError("Failed to launch webinspect page\n")
                    except Exception as error:
                         print("Got exception while opening the browser\n")
                         tdkTestObj.setResultStatus("FAILURE")                                                  
                         print(error)
                         webinspect_launched = False
                else:
                    print("\nFailed to set video_test_url_new in device")
                    tdkTestObj.setResultStatus("FAILURE")
                    webinspect_launched =False  
            if webinspect_launched == True:                              
               print("\nlaunching the video test url to play")
               tdkTestObj = obj.createTestStep('rdkservice_setValue');
               tdkTestObj.addParameter("method",set_method);
               tdkTestObj.addParameter("value",video_test_urls[0]);
               tdkTestObj.executeTestCase(expectedResult);
               result = tdkTestObj.getResult();
               if expectedResult in result:
                  print("\n Validate if the URL is set successfully or not")
                  tdkTestObj.setResultStatus("SUCCESS");
                  tdkTestObj = obj.createTestStep('rdkservice_getValue');
                  tdkTestObj.addParameter("method",set_method);
                  tdkTestObj.executeTestCase(expectedResult);
                  new_url1 = tdkTestObj.getResultDetails();
                  memory_usage = []
                  if new_url1 in video_test_urls[0]:
                     tdkTestObj.setResultStatus("SUCCESS");
                     print("\n URL(",new_url1,") is set successfully")
                     test_time_in_sec = 1200
                     test_time_in_millisec = test_time_in_sec * 1000
                     time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                     iteration = 0                    
                     if ssh_param_dict != {}:
                        while int(round(time.time() * 1000)) < time_limit:
                            iteration += 1
                            print(f"Iteration: {iteration}") 
                            print("Checking for any crash during video playback\n")
                            command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                            print("COMMAND : %s" %(command))            
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                            #Add the parameters to ssh to the DUT and execute the command
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedResult);
                            output = tdkTestObj.getResultDetails()
                            output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
                            output = output[output.find('\n')]            
                            if ("crash" or "CRASH" or "Crash") in output:
                                print("Crash observed during Video playback\n")
                                print("\n Validate the status of LightningApp plugin to confirm the crash:\n")
                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                tdkTestObj.addParameter("plugin","LightningApp")
                                #Execute the test case in DUT                
                                tdkTestObj.executeTestCase(expectedResult);
                                output = tdkTestObj.getResultDetails()
                                if output != 'deactivated':
                                   print("\nCrash is not observed and plugin is still active")
                                   tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print("\nCrash is observed during video playback and plugin is deactivated")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    crash_Validation = True 
                                    crash_iteration = iteration                            
                                    obj.unloadModule("rdkv_performance");
                                    break
                            else:                                 
                                print(f"No crash observed during video playback in iteration: {iteration}")
                                tdkTestObj.setResultStatus("SUCCESS")
                            time.sleep(240)       
                     if logging_method == "REST_API":
                        expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingRestAPI(obj);
                        evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                     elif logging_method == "WEB_INSPECT":
                        if current_url != None and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS");
                            expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingWebInspect(obj,webkit_console_socket);
                            evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                  if ("SUCCESS" in test_result)  and crash_Validation ==False:                       
                     print("Video playback is happening successfully with out any crash")
                     tdkTestObj.setResultStatus("SUCCESS")              
                  else:
                    tdkTestObj.setResultStatus("FAILURE");
                    print ("\n Error occured during video playback\n")
                  #Set the URL back to previous                
                  tdkTestObj = obj.createTestStep('rdkservice_setValue');
                  tdkTestObj.addParameter("method",set_method);
                  tdkTestObj.addParameter("value",current_url);
                  tdkTestObj.executeTestCase(expectedResult);
                  result = tdkTestObj.getResult();
                  if result == "SUCCESS":
                    print("\n URL is reverted successfully")
                    tdkTestObj.setResultStatus("SUCCESS");
                  else:
                    print("\n Failed to revert the URL")
                    tdkTestObj.setResultStatus("FAILURE");
               else:
                  print("\n Failed to load the URL, new URL %s" %(new_url))
                  tdkTestObj.setResultStatus("FAILURE");
        else:
            print("\n Failed to set the URL")
            tdkTestObj.setResultStatus("FAILURE");
    else:
        print("\n Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print("\n Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    if driver and webinspect_launched :
       print("################TEST SUMMARY################\n")
       if crash_Validation == False:
          print("No crash is observed during the execution\n")
       else:
           print(f"Crash observed during execution at iteration:{crash_iteration}\n")
       driver.quit()
    obj.unloadModule("rdkv_performance");