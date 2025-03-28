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
  <version>25</version>
  <!-- Do not edit version. This will be auto incremented while updating. If you are adding a new script you can keep the vresion as 1 -->
  <name>RDKV_CERT_RVS_WebKitBrowser_LongDuration_Video_Playback_MemoryUsage_WithWebinspect</name>
  <!-- If you are adding a new script you can specify the script name. Script Name should be unique same as this file name with out .py extension -->
  <primitive_test_id></primitive_test_id>
  <!-- Do not change primitive_test_id if you are editing an existing script. -->
  <primitive_test_name>rdkservice_validateResourceUsage</primitive_test_name>
  <!--  -->
  <primitive_test_version>1</primitive_test_version>
  <!--  -->
  <status>FREE</status>
  <!--  -->
  <synopsis>The Objective of the test is to calculate memory usage of the WebKitBrowser by keeping the 
 web inspect port open for playback of mp4 video for long duration</synopsis>
  <!--  -->
  <groups_id />
  <!--  -->
  <execution_time>720</execution_time>
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
    <test_case_id>RDKV_STABILITY_77</test_case_id>
    <test_objective>The Objective of the test is to calculate memory usage of the WebKitBrowser by keeping the 
 web inspect port open for playback of mp4 video for long duration</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. As a prerequisite disable all other plugins and enable WebKitBrowser app</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>1. The URL of the application to be launched.
2, Memory Usage Threshold limit.</input_parameters>
    <automation_approch>1.Open WebKitBrowser app web inspect port
2. Set the application URL in WebKitBrowser app
3. Play  the video from the application
4.Calcute the Memory usage  </automation_approch>
    <expected_output>Memory usage must be with in threshold value</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_stability</test_stub_interface>
    <test_script>RDKV_CERT_RVS_WebKitBrowser_LongDuration_Video_Playback_MemoryUsage_WithWebinspect</test_script>
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
from BrowserPerformanceUtility import *
import StabilityTestVariables
from SSHUtility import *
import ast
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_WebKitBrowser_LongDuration_Video_Playback_MemoryUsage_WithWebinspect');
deviceIP =str(ip)
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
result_dict_list = []
webkit_console_socket = None
webinspect_launched = True
memory_usage = []
driver = None
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)
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
    test_duration_in_seconds = 18000
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
    set_method = "WebKitBrowser"+'.1.url'
    webinspect_port = str(PerformanceTestVariables.webinspect_port)
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"resumed"}
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(20)
    status = "SUCCESS"
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
        print("\n Pre conditions for the test are set successfully\n");        
        print("\n Get the URL in WebKitBrowser")
        tdkTestObj = obj.createTestStep('rdkservice_getValue');
        tdkTestObj.addParameter("method",set_method);
        tdkTestObj.executeTestCase(expectedResult);
        current_url = tdkTestObj.getResultDetails();
        result = tdkTestObj.getResult()
        if current_url != None and expectedResult in result:
            tdkTestObj.setResultStatus("SUCCESS");
            webkit_console_socket = createEventListener(ip,webinspect_port,[],"/devtools/page/1",False)
            time.sleep(60)
            original_url = video_test_urls[0]
            video_test_url_new = original_url[:original_url.find("&url=")] +"&url="+ '%22%22'+'"'
            print("\n Current URL:",current_url)
            print("\n Set WebKitBrowser Application URL 1\n")
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
                print("\n Validate if the URL is set successfully or not\n")                
                tdkTestObj = obj.createTestStep('rdkservice_getValue');
                tdkTestObj.addParameter("method",set_method);
                tdkTestObj.executeTestCase(expectedResult);
                new_url = tdkTestObj.getResultDetails();
                if new_url in video_test_url_new:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\n URL(",new_url,") is set successfully\n")                    
                    webinspectURL = 'http://'+deviceIP+':'+webinspect_port+'/Main.html?ws='+deviceIP+':'+webinspect_port+'/socket/1/1/WebPage'
                    print (webinspectURL)
                    try:                      
                       driver = openChromeBrowser(webinspectURL);
                       if driver != "EXCEPTION OCCURRED":
                          time.sleep(20)                          
                          print("\nWebinspect page in device launched successfully \n")  
                       else:
                           raise RuntimeError("failed to launch webinspect page")              
                
                    except Exception as error:
                         print("\nGot exception while opening the browser\n")
                         tdkTestObj.setResultStatus("FAILURE")                                                  
                         print(error)
                         webinspect_launched = False
                else:
                    print("\nFailed to set video_test_url_new in device\n")
                    tdkTestObj.setResultStatus("FAILURE") 
                    webinspect_launched =False                                             
            if webinspect_launched == True:                                                 
               print("\nlaunching the video test url to play\n")
               tdkTestObj = obj.createTestStep('rdkservice_setValue');
               tdkTestObj.addParameter("method",set_method);
               tdkTestObj.addParameter("value",video_test_urls[0]);
               tdkTestObj.executeTestCase(expectedResult);
               result = tdkTestObj.getResult();
               if expectedResult in result:
                  print("\n Validate if the URL is set successfully or not\n")
                  tdkTestObj = obj.createTestStep('rdkservice_getValue');
                  tdkTestObj.addParameter("method",set_method);
                  tdkTestObj.executeTestCase(expectedResult);
                  new_url1 = tdkTestObj.getResultDetails();                  
                  if new_url1 in video_test_urls[0]:
                    tdkTestObj.setResultStatus("SUCCESS");
                    print("\n URL(",new_url1,") is set successfully")
                    if logging_method == "REST_API":
                        expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingRestAPI(obj);
                        evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                    elif logging_method == "WEB_INSPECT":
                        if current_url != None and expectedResult in result:
                            tdkTestObj.setResultStatus("SUCCESS");
                            expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result = testusingWebInspect(obj,webkit_console_socket);
                            evt_list = [expected_pause_evt,observed_pause_evt,expected_play_evt,observed_play_evt,test_result]
                    test_time_in_sec = 14400
                    test_time_in_millisec = test_time_in_sec * 1000
                    time_limit = int(round(time.time() * 1000)) + test_time_in_millisec
                    iteration = 0                    
                    if ssh_param_dict != {} and ("SUCCESS" in test_result):
                        while int(round(time.time() * 1000)) < time_limit:
                            iteration += 1
                            print(f"Iteration: {iteration}") 
                            print("\n Calculating the memory usage in bytes\n")                                          
                            command = 'cd /sys/fs/cgroup/memory &&  cat memory.max_usage_in_bytes'
                            tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                            tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                            tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                            tdkTestObj.addParameter("command",command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResult()
                            output = tdkTestObj.getResultDetails()    
                            output = int(output.split()[-1] )                        
                            print(f"\nOutput: {output}")  
                            memory_usage.append(output)
                            time.sleep(240) 
                            conf_file, status = get_configfile_name(obj);
                            result, memory_threshold = getDeviceConfigKeyValue(conf_file,"MEMORY_USAGE_THRESHOLD")  
                            threshold = int(memory_threshold) 
                            initial_memory = memory_usage[0]
                        for i in range(1, len(memory_usage)):
                                difference = memory_usage[i] - memory_usage[i-1]
                                if difference > threshold:
                                   print(f"Value increased by {difference} bytes in iteration {i}, exceeding the threshold of {threshold} bytes\n")                     
                                   print("FAILURE:","Stopping the execution\n",)
                                   tdkTestObj.setResultStatus("FAILURE")
                                   break
                                elif difference < 0:
                                     print(f"Value decreased by {abs(difference)} bytes in iteration {i}\n")                                     
                                elif difference == 0:
                                     print(f"Value remained the same in iteration {i}") 
                                     tdkTestObj.setResultStatus("SUCCESS")                                    
                                else:
                                    print(f"Value increased by {difference} bytes in iteration {i}")
                        # Check if the final memory usage is double the initial
                        if memory_usage[-1] > 2 * initial_memory:
                               print("Final memory usage is more than double the initial usage\n")
                               print("FAILURE:","Stopping the execution\n",)
                               tdkTestObj.setResultStatus("FAILURE")
                               obj.unloadModule("rdkv_performance");
                               if driver:
                                  driver.quit()
                               exit()          
     
                    else:
                        tdkTestObj.setResultStatus("FAILURE");
                        print("\n Error occured during video playback\n") 
                    tdkTestObj = obj.createTestStep('rdkservice_validateResourceUsage')
                    tdkTestObj.executeTestCase(expectedResult)
                    status = tdkTestObj.getResult()
                    result = tdkTestObj.getResultDetails()               
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
    if driver != None and webinspect_launched :
       driver.quit()
    obj.unloadModule("rdkv_performance");    
    
else:
    obj.setLoadModuleStatus("FAILURE");
    print ("\n Failed to load module")
