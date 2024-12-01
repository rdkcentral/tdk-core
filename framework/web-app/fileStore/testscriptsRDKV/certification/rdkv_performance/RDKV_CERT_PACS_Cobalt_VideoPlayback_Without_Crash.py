##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2023 RDK Management
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
  <name>RDKV_CERT_PACS_Cobalt_VideoPlayback_Without_Crash</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_getRequiredLog</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to validate whether the video playback is happening in cobalt without any crash</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>RDKTV</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_146</test_case_id>
    <test_objective>The objective of this test is to validate whether the video playback is happening in cobalt without any crash</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI,Accelerator,RDKTV</test_setup>
    <pre_requisite>1. Wpeframework process should be up and running in the device.
</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>cobalt_test_url:string</input_parameters>
    <automation_approch>1. Launch Cobalt using RDKShell
2. Set a video URL using deeplink method.
3. Save current system time and Start playing by generateKey method
4. Get wpeframework logs to related with video playback
5. Validate whether any crash is observed in wpeframework logs
6. Deactivate the Cobalt plugin.
</automation_approch>
    <expected_output>The video playback in Cobalt should happen without any crash</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PACS_Cobalt_VideoPlayback_Without_Crash</test_script>
    <skipped>No</skipped>
    <release_version>M118</release_version>
    <remarks/>
  </test_cases>
</xml>
'''
 # use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import PerformanceTestVariables
from StabilityTestUtility import *
#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True);
#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PACS_Cobalt_VideoPlayback_Without_Crash');
#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")
#Execution summary variable
Summ_list=[]
#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("Check Pre conditions")
    status = "SUCCESS"
    revert = "NO"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    if cobalt_test_url == "":
        print("\n Please configure the cobalt_test_url value\n")
    plugins_list = ["Cobalt","WebKitBrowser"]
    plugin_status_needed = {"Cobalt":"deactivated","WebKitBrowser":"deactivated"}
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    if curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            status = "FAILURE"
    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
    tdkTestObj.addParameter("realpath",obj.realpath)
    tdkTestObj.addParameter("deviceIP",obj.IP)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResult()
    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
    if status == "SUCCESS" and expectedResult in result and ssh_param_dict != {} and cobalt_test_url != "":
        tdkTestObj.setResultStatus("SUCCESS")
        cobalt_launch_status = launch_cobalt(obj)
        print("\nPre conditions for the test are set successfully")
        time.sleep(30)
        if cobalt_launch_status == "SUCCESS":
            print("\n Set the URL : {} using Cobalt deeplink method \n".format(cobalt_test_url))
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method","Cobalt.1.deeplink")
            tdkTestObj.addParameter("value",cobalt_test_url)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_result = tdkTestObj.getResult()
            time.sleep(20)
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
                time.sleep(40)
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                tdkTestObj.addParameter("value",params)
                tdkTestObj.executeTestCase(expectedResult)
                result2 = tdkTestObj.getResult()
                time.sleep(50)
                if "SUCCESS" == (result1 and result2):
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("\n Check video is started \n")
                    command = 'cat /opt/logs/wpeframework.log | grep -inr State.*changed.*old.*PAUSED.*new.*PLAYING | tail -1'
                    tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog')
                    tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                    tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                    tdkTestObj.addParameter("command",command)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    output = tdkTestObj.getResultDetails()
                    if output != "EXCEPTION" and expectedResult in result and "old: PAUSED" in output:
                        print("\n Video started Playing\n")
                        tdkTestObj.setResultStatus("SUCCESS")
                        command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                        print("COMMAND : %s" %(command))
                        #Primitive test case which associated to this Script
                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                        #Add the parameters to ssh to the DUT and execute the command
                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                        tdkTestObj.addParameter("command",command)
                        #Execute the test case in DUT
                        tdkTestObj.executeTestCase(expectedResult);
                        output = tdkTestObj.getResultDetails()
                        if ("crash" or "CRASH" or "Crash") in output:
                            print("Crash observed")
                            print("\n Validate the status of Cobalt plugin to confirm the crash:\n")
                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                            tdkTestObj.addParameter("plugin","Cobalt")
                            #Execute the test case in DUT
                            tdkTestObj.executeTestCase(expectedResult);
                            output = tdkTestObj.getResultDetails()
                            if output != 'deactivated':
                                print("Crash is not observed and plugin is still active")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("Crash is observed and plugin is deactivated")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("No crash Observed")
                            tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("\n Video play related logs are not available \n")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("\n Error while executing generateKey method \n")
                    tdkTestObj.setResultStatus("FAILURE")
            else:
                print("\n Error while executing deeplink method \n")
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("\n Error while launching Cobalt \n")
            tdkTestObj.setResultStatus("FAILURE")
        print("\n Exiting from Cobalt \n")
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
        print("\n Preconditions are not met \n")
        tdkTestObj.setResultStatus("FAILURE")
    #Revert the values
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict)
    obj.unloadModule("rdkv_performance");
    getSummary(Summ_list,obj)
else:
    obj.setLoadModuleStatus("FAILURE");
    print("Failed to load module")
