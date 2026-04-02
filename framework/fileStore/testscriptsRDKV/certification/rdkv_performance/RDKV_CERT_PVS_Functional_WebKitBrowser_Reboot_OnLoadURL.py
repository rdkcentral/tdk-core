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
  <version>1</version>
  <name>RDKV_CERT_PVS_Functional_WebKitBrowser_Reboot_OnLoadURL</name>
  <primitive_test_id/>
  <primitive_test_name>rdkservice_setValue</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>The objective of this test is to    load URL in WebKitBrowser, reboot the device, check whether WebKitBrowser is stable and able to load URL again in it once the device is online.</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks/>
  <skip>false</skip>
  <box_types>
    <box_type>RPI-HYB</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>RDKV_PERFORMANCE_84</test_case_id>
    <test_objective>The objective of this test is to load URL in WebKitBrowser, reboot the device, check whether WebKitBrowser is stable and able to load URL again in it once the device is online.</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RPI, Accelerator</test_setup>
    <pre_requisite>1.wpeframework should be up and running</pre_requisite>
    <api_or_interface_used>None</api_or_interface_used>
    <input_parameters>browser_test_url:string</input_parameters>
    <automation_approch>1. Launch the plugin using RDKShell
2. Register for urlchange event
3. Set given URL using url method
4. Verify the events for URL change
5. Reboot the DUT.
6. Launch the plugin using RDKShell
7. Register for urlchange event
8. Set given URL using url method
9. Verify the events for URL change
10. Destroy the plugin</automation_approch>
    <expected_output>The device should be stable after reboot and URL should be loaded before and after reboot</expected_output>
    <priority>High</priority>
    <test_stub_interface>rdkv_performance</test_stub_interface>
    <test_script>RDKV_CERT_PVS_Functional_WebKitBrowser_Reboot_OnLoadURL</test_script>
    <skipped>No</skipped>
    <release_version>M95</release_version>
    <remarks/>
  </test_cases>
</xml>

'''
# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import rdkv_performancelib
from datetime import datetime
from StabilityTestUtility import *
from web_socket_util import *
import PerformanceTestVariables
from rdkv_performancelib import *
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_performance","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_PVS_Functional_WebKitBrowser_Reboot_OnLoadURL')

#The device will reboot before starting the performance testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)
expectedResult = "SUCCESS"
if expectedResult in result.upper():
    conf_file,file_status = get_configfile_name(obj)
    result1, rebootwaitTime = getDeviceConfigKeyValue(conf_file,"REBOOT_WAIT_TIME")
    for count in range(0,2):
        app_bundle_name=PerformanceTestVariables.google_bundle
        app_name="com.rdkcentral.google"
        status = rdkservice_install_launch_app(obj, app_bundle_name, app_name)
        if status == expectedResult:
            tdkTestObj = obj.createTestStep('rdkservice_rebootDevice')
            tdkTestObj.addParameter("waitTime",float(rebootwaitTime))
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            if expectedResult in result:
                tdkTestObj.setResultStatus("SUCCESS")
                print("\n Device is rebooted")
                uptime = get_device_uptime(obj)
                if uptime != -1 and uptime < 280:
                    print("\n Device is rebooted and uptime is: {}\n".format(uptime))
                else:
                    print("\n Error while validating uptime")
                    tdkTestObj.setResultStatus("FAILURE")
                    break
            else:
                print("\n Error while rebooting the device")
                tdkTestObj.setResultStatus("FAILURE")
                break
            if count==1:
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
            print("\n Error while launching the app")
            tdkTestObj.setResultStatus("FAILURE")
            break
        
    obj.unloadModule("rdkv_performance")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
