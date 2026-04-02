##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2021 RDK Management
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
  <name>RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to get the CPU and Memory usage while launching an application with WiFi.</synopsis>
  <groups_id/>
  <execution_time>15</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_27</test_case_id>
    <test_objective>The objective of this test is to get the CPU and Memory usage while launching an application with WiFi.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator</test_setup>
    <pre_requisite>1. Either the DUT should be already connected and configured with WiFi IP in test manager or WiFi Access point with same IP range is required.
2. Lightning application for ip change detection should be already hosted.
3.Lightning application for video player test should be already hosted.
4. Wpeframework process should be up and running in the device.</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>video_test_url : string
ip_change_app_url: string
tm_username : string
tm_password : string
device_ip_address_type : string</input_parameters>
    <automation_approch>1. Launch Lightning application to detect IP address change, then connect to WiFi
2.Launch Lightning application for video player
3. Validate CPU and memory usage are within expected range
4. Revert everything</automation_approch>
    <expected_output>1. Lightning application for detecting IP address change must be lauched.
2. Should connect to WiFI.
3. Lightning application for video player must be lauched.
4. CPU load and memory usage must be within the expected range.</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch</test_script>
    <skipped>No</skipped>
    <release_version>M86</release_version>
    <remarks/>
  </test_cases>
  <script_tags/>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
from StabilityTestUtility import *
from ip_change_detection_utility import *
import PerformanceTestVariables
from MediaValidationUtility import *
from web_socket_util import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Apps_WiFi_ResourceUsage_Launch');

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT

result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    conf_file, status = get_configfile_name(obj);
    result, logging_method = getDeviceConfigKeyValue(conf_file,"LOGGING_METHOD")
    setDeviceConfigFile(conf_file)
    videoURL  = MediaValidationVariables.video_src_url_dash_h264
    videoURL_type = "dash"
    # Setting VideoPlayer Operations
    setURLArgument("execID",str(obj.execID))
    setURLArgument("execDevId",str(obj.execDevId))
    setURLArgument("resultId",str(obj.resultId))
    setLoggingMethod(obj)
    setURLArgument("logging",logging_method)
    setURLArgument("tmUrl",str(obj.url)+"/")
    setOperation("close",10)
    operations = getOperations()
    # Setting VideoPlayer test app URL arguments
    setURLArgument("url",videoURL)
    setURLArgument("operations",operations)
    setURLArgument("autotest","true")
    setURLArgument("type",videoURL_type)
    appArguments = getURLArguments()
    video_test_urls = []
    players_list = str(MediaValidationVariables.codec_dash_h264).split(",")
    print("SELECTED PLAYERS: ", players_list)
    # Getting the complete test app URL
    video_test_urls = getTestURLs(players_list,appArguments)

    print("\n Check Pre conditions")
    status = "SUCCESS"
    revert = "NO"
    #Check current interface
    current_interface,revert_nw = check_current_interface(obj)
    print("\n Current interface is: ", current_interface)
    if current_interface == "EMPTY":
        status = "FAILURE"
    elif current_interface == "eth0":
        print("\nCurrent interface is ETHERNET, Please connect to WiFi and run the script")
        status = "FAILURE"
    else:
        print("\n Current interface is WIFI \n")
    if status == "SUCCESS":
        plugins_list = ["DeviceInfo","org.rdk.PersistentStore"]
        plugin_status_needed = {"org.rdk.PersistentStore":"activated","DeviceInfo":"activated"}
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
            time.sleep(10)
            tdkTestObj = obj.createTestStep('setPS_value');
            tdkTestObj.addParameter("video_test_url",video_test_urls[0]);
            tdkTestObj.executeTestCase(expectedResult);
            result = tdkTestObj.getResult();
            if result == "SUCCESS":
                tdkTestObj.setResultStatus("SUCCESS");
                print("\n Video test URL is set successfully");
            # rdkv_performancelib.setPS_value(video_test_urls[0])
                app_bundle_name=MediaValidationVariables.unified_player_app_download_url.split("/")[-1]
                print(f"\nApp bundle name: {app_bundle_name}")
                app_name = app_bundle_name.split("+")[0]
                print(f"\nApp name: {app_name}")
                app_download_url = MediaValidationVariables.unified_player_app_download_url.split(app_bundle_name)[0]
                print("app_download_url", app_download_url)
                status = rdkservice_install_launch_app(obj, app_bundle_name, app_name,app_download_url)
                if status == "SUCCESS":
                    if logging_method == "REST_API":
                        app_log_file = obj.logpath+"/"+str(obj.execID)+"/"+str(obj.execID)+"_"+str(obj.execDevId)+"_"+str(obj.resultId)+"_mvs_applog.txt"
                        continue_count = 0
                        file_check_count = 0
                        logging_flag = 0
                        hang_detected = 0
                        test_result = ""
                        lastLine = None
                        lastIndex = 0
                        while True:
                            if file_check_count > 60:
                                print("\nREST API Logging is not happening properly. Exiting...")
                                break;
                            if os.path.exists(app_log_file):
                                logging_flag = 1
                                break;
                            else:
                                file_check_count += 1
                                time.sleep(1);
                        while logging_flag:
                            if continue_count > 60:
                                hang_detected = 1
                                print("\nApp not proceeding for 60 secs. Exiting...")
                                break;
                            with open(app_log_file,'r') as f:
                                lines = f.readlines()
                            if lines:
                                if len(lines) != lastIndex:
                                    continue_count = 0
                                    #print(lastIndex,len(lines))
                                    for i in range(lastIndex,len(lines)):
                                        print(lines[i])
                                        if "URL Info:" in lines[i]:
                                            test_result = lines[i]
                                    lastIndex = len(lines)
                                    if test_result != "":
                                        break;
                                else:
                                    continue_count += 1
                            else:
                                continue_count += 1
                            time.sleep(1)
                    elif logging_method == "WEB_INSPECT":
                        webkit_console_socket = createEventListener(obj.IP,webinspect_port,[],"/devtools/page/1",False)
                        continue_count = 0
                        test_result = ""
                        while True:
                            if continue_count > 60:
                                print("\n Lightning Application is not launched within 60 seconds \n")
                                break
                            if (len(webkit_console_socket.getEventsBuffer())== 0):
                                time.sleep(1)
                                continue_count += 1
                                continue
                            console_log = webkit_console_socket.getEventsBuffer().pop(0)
                            if "URL Info:" in console_log or "Connection refused" in console_log:
                                test_result = getConsoleMessage(console_log)
                                break;
                        webkit_console_socket.disconnect()
                    if "URL Info:" in test_result:
                        print("\n Application launched successfully")
                        tdkTestObj = obj.createTestStep("rdkservice_validateResourceUsage")
                        tdkTestObj.executeTestCase(expectedResult)
                        resource_usage = tdkTestObj.getResultDetails()
                        result = tdkTestObj.getResult()
                        if expectedResult in result and resource_usage != "ERROR":
                            print("\n Successfully validated Resource usage")
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("\n Error while validating Resource usage")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("\n Error occured during application launch")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to set the video url value in PersistanceStorage")
                print("\n Terminating the app")
                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                tdkTestObj.addParameter("app_id",app_name)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResult()
                if result == "SUCCESS":
                    tdkTestObj.setResultStatus("SUCCESS")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("Unable to terminate the app")
            else:
                tdkTestObj.setResultStatus("FAILURE")
                print("Failed to install or launch app")
        else:
            print("\n Pre conditions are not met")
    else:
        print("\n Pre conditions are not met")
        obj.setLoadModuleStatus("FAILURE");
    #Revert the values
    if revert=="YES":
        print("\n Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
