##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2026 RDK Management
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

# use tdklib library,which provides a wrapper for tdk testcase script
import tdklib;
import PerformanceTestVariables 
import rdkv_performancelib
from StabilityTestUtility import *
from web_socket_util import *
from StabilityTestVariables import launch_and_load_max_count

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_stability","1",standAlone=True);

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_RVS_Cobalt_LoadMultipleApps');

#The device will reboot before starting the stability testing if "pre_req_reboot_pvs" is
#configured as "Yes".
pre_requisite_reboot(obj,"yes")

#Get the result of connection with test component and DUT
result =obj.getLoadModuleResult();
print("[LIB LOAD STATUS]  :  %s" %result);
obj.setLoadModuleStatus(result);

#Check the device status before starting the stress test
pre_condition_status = check_device_state(obj)

expectedResult = "SUCCESS"
if expectedResult in (result.upper() and pre_condition_status):
    print("\n Check Pre conditions")
    #No need to revert any values if the pre conditions are already set.
    revert="NO"
    status = "SUCCESS"
    cobalt_test_url = PerformanceTestVariables.cobalt_test_url
    browser_test_url = PerformanceTestVariables.browser_test_url
    plugins_list = ["HtmlApp","Cobalt","WebKitBrowser","LightningApp"]
    plugin_status_needed = {"HtmlApp":"deactivated","Cobalt":"deactivated","WebKitBrowser":"deactivated","LightningApp":"deactivated"}
    conf_file, status = get_configfile_name(obj);
    status,supported_plugins = getDeviceConfigValue(conf_file,"SUPPORTED_PLUGINS")
    for plugin in plugins_list[:]:
        if plugin not in supported_plugins:
            plugins_list.remove(plugin)
            plugin_status_needed.pop(plugin)
    curr_plugins_status_dict = get_plugins_status(obj,plugins_list)
    time.sleep(10)
    if any(curr_plugins_status_dict[plugin] == "FAILURE" for plugin in plugins_list):
        print("\n Error while getting the status of plugins")
        status = "FAILURE"
    elif curr_plugins_status_dict != plugin_status_needed:
        revert = "YES"
        status = set_plugins_status(obj,plugin_status_needed)
        time.sleep(10)
        new_status_dict = get_plugins_status(obj,plugins_list)
        if new_status_dict != plugin_status_needed:
            print("\n Unable to deactivate plugins")
            status = "FAILURE"
    if status == "SUCCESS":
        print("\nPre conditions for the test are set successfully")
        for count in range(launch_and_load_max_count):
            print("\n=============== Iteration #{} ===============".format(count+1))
            cobalt_launch_status = launch_cobalt(obj)
            if cobalt_launch_status in expectedResult:
                time.sleep(30)
                print("\n Set the URL : {} using Cobalt deeplink method".format(cobalt_test_url))
                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                tdkTestObj.addParameter("method","Cobalt.1.deeplink")
                tdkTestObj.addParameter("value",cobalt_test_url)
                tdkTestObj.executeTestCase(expectedResult)
                cobalt_result = tdkTestObj.getResult()
                time.sleep(10)
                if(cobalt_result in expectedResult):
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("Clicking OK to play video")
                    params = '{"keys":[ {"keyCode": 13,"modifiers": [],"delay":1.0}]}'
                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                    tdkTestObj.addParameter("method","org.rdk.RDKShell.1.generateKey")
                    tdkTestObj.addParameter("value",params)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResult()
                    if result == "SUCCESS":
                        print("\n Pressed OK key")
                        tdkTestObj.setResultStatus("SUCCESS")
                        #Launching Multiple apps and validating if Cobalt is still running or not
                        print("Launching HtmlApp")
                        launch_status,launch_start_time = launch_plugin(obj,"HtmlApp")
                        if launch_status == expectedResult:
                            time.sleep(10)
                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                            tdkTestObj.addParameter("plugin","HtmlApp")
                            tdkTestObj.executeTestCase(expectedResult)
                            htmlapp_status = tdkTestObj.getResultDetails()
                            result = tdkTestObj.getResult()
                            if htmlapp_status == 'resumed' and expectedResult in result:
                                print("\n HtmlApp resumed successfully")
                                tdkTestObj.setResultStatus("SUCCESS")
                                time.sleep(10)
                                print("\n Set test URL")
                                tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                tdkTestObj.addParameter("method","HtmlApp.1.url")
                                tdkTestObj.addParameter("value",browser_test_url)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResult()
                                time.sleep(10)
                                if expectedResult in result:
                                    print("\nValidate if the URL is set successfully or not")
                                    tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                    tdkTestObj.addParameter("method","HtmlApp.1.url")
                                    tdkTestObj.executeTestCase(expectedResult)
                                    new_url = tdkTestObj.getResultDetails()
                                    result = tdkTestObj.getResult() 
                                    if browser_test_url in new_url and expectedResult in result:
                                        tdkTestObj.setResultStatus("SUCCESS");
                                        print("\n URL(",new_url,") is set successfully")
                                        print("\n Exiting from HtmlApp")
                                        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                                        tdkTestObj.addParameter("plugin","HtmlApp")
                                        tdkTestObj.addParameter("status","deactivate")
                                        tdkTestObj.executeTestCase(expectedResult)
                                        result = tdkTestObj.getResult() 
                                        if result == "SUCCESS":
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            print("Launching LightningApp")
                                            launch_status,launch_start_time = launch_plugin(obj,"LightningApp")
                                            if launch_status == expectedResult:
                                                time.sleep(10)
                                                tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                                tdkTestObj.addParameter("plugin","LightningApp")
                                                tdkTestObj.executeTestCase(expectedResult)
                                                lightningapp_status = tdkTestObj.getResultDetails()
                                                result = tdkTestObj.getResult()
                                                if lightningapp_status == 'resumed' and expectedResult in result:
                                                    print("\n LightningApp resumed successfully")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    time.sleep(10)
                                                    print("\n Set test URL")
                                                    tdkTestObj = obj.createTestStep('rdkservice_setValue')
                                                    tdkTestObj.addParameter("method","LightningApp.1.url")
                                                    tdkTestObj.addParameter("value",browser_test_url)
                                                    tdkTestObj.executeTestCase(expectedResult)
                                                    result = tdkTestObj.getResult()
                                                    time.sleep(10)
                                                    if expectedResult in result:
                                                        print("\nValidate if the URL is set successfully or not")
                                                        tdkTestObj = obj.createTestStep('rdkservice_getValue')
                                                        tdkTestObj.addParameter("method","LightningApp.1.url")
                                                        tdkTestObj.executeTestCase(expectedResult)
                                                        new_url = tdkTestObj.getResultDetails()
                                                        result = tdkTestObj.getResult()
                                                        if browser_test_url in new_url and expectedResult in result:
                                                            tdkTestObj.setResultStatus("SUCCESS");
                                                            print("\n URL(",new_url,") is set successfully")
                                                            print("\n Exiting from LightningApp")
                                                            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                                                            tdkTestObj.addParameter("plugin","LightningApp")
                                                            tdkTestObj.addParameter("status","deactivate")
                                                            tdkTestObj.executeTestCase(expectedResult)
                                                            result = tdkTestObj.getResult()
                                                            if result == "SUCCESS":
                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                print("Launching WebKitBrowser")
                                                                launch_status,launch_start_time = launch_plugin(obj,"WebKitBrowser")
                                                                if launch_status == expectedResult:
                                                                    time.sleep(10)
                                                                    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                                                    tdkTestObj.addParameter("plugin","WebKitBrowser")
                                                                    tdkTestObj.executeTestCase(expectedResult)
                                                                    webkit_status = tdkTestObj.getResultDetails()
                                                                    result = tdkTestObj.getResult()
                                                                    if webkit_status == 'resumed' and expectedResult in result:
                                                                        print("\n WebKitBrowser resumed successfully")
                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                        time.sleep(10)
                                                                        print("\nSet Browser test URL")
                                                                        tdkTestObj = obj.createTestStep('rdkservice_setValue');
                                                                        tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                                                                        tdkTestObj.addParameter("value",browser_test_url);
                                                                        tdkTestObj.executeTestCase(expectedResult);
                                                                        result = tdkTestObj.getResult();
                                                                        if expectedResult in result:
                                                                            print("\nValidate if the URL is set successfully or not")
                                                                            tdkTestObj = obj.createTestStep('rdkservice_getValue');
                                                                            tdkTestObj.addParameter("method","WebKitBrowser.1.url");
                                                                            tdkTestObj.executeTestCase(expectedResult);
                                                                            new_url = tdkTestObj.getResultDetails();
                                                                            result = tdkTestObj.getResult()
                                                                            if browser_test_url in new_url and expectedResult in result:
                                                                                tdkTestObj.setResultStatus("SUCCESS");
                                                                                print("\n URL(",new_url,") is set successfully")
                                                                                time.sleep(30)
                                                                                print("\n Exiting from WebKitBrowser")
                                                                                tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                                                                                tdkTestObj.addParameter("plugin","WebKitBrowser")
                                                                                tdkTestObj.addParameter("status","deactivate")
                                                                                tdkTestObj.executeTestCase(expectedResult)
                                                                                result = tdkTestObj.getResult()
                                                                                if result == "SUCCESS":
                                                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                                                    print("Checking for any crash\n")
                                                                                    command = 'cat /opt/logs/wpeframework.log | grep -inr crash'
                                                                                    print("COMMAND : %s" %(command))   
                                                                                    tdkTestObj = obj.createTestStep('rdkservice_getSSHParams')
                                                                                    tdkTestObj.addParameter("realpath",obj.realpath)
                                                                                    tdkTestObj.addParameter("deviceIP",obj.IP)
                                                                                    tdkTestObj.executeTestCase(expectedResult)
                                                                                    result = tdkTestObj.getResult()
                                                                                    ssh_param_dict = json.loads(tdkTestObj.getResultDetails())
                                                                                    if status == "SUCCESS"  and ssh_param_dict != {} :   
                                                                                        time.sleep(30)
                                                                                        print("Successfully retrieved the SSH params from the conf file")
                                                                                        tdkTestObj.setResultStatus("SUCCESS")
                                                                                        tdkTestObj = obj.createTestStep('rdkservice_getRequiredLog');
                                                                                        tdkTestObj.addParameter("ssh_method",ssh_param_dict["ssh_method"])
                                                                                        tdkTestObj.addParameter("credentials",ssh_param_dict["credentials"])
                                                                                        tdkTestObj.addParameter("command",command)
                                                                                        tdkTestObj.executeTestCase(expectedResult);
                                                                                        output = tdkTestObj.getResultDetails()
                                                                                        output = tdkTestObj.getResultDetails().replace(r'\n', '\n');
                                                                                        output = output[output.find('\n')]
                                                                                        if ("crash" or "CRASH" or "Crash") in output:
                                                                                            print("Crash log observed while launching multiple apps with Cobalt in the background")
                                                                                            print("\n Validate the status of Cobalt plugin to confirm the crash:\n")
                                                                                            tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                                                                            tdkTestObj.addParameter("plugin","Cobalt")
                                                                                            tdkTestObj.executeTestCase(expectedResult);
                                                                                            output = tdkTestObj.getResultDetails()
                                                                                            if output != 'deactivated':
                                                                                                print("Crash is not observed and plugin is still active")
                                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                            else:
                                                                                                print("Crash is observed while launching multiple apps with Cobalt in the backgroundd")
                                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                                break
                                                                                        else:
                                                                                            print("No crash logs found in the log file")
                                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                                        #Check the status of Cobalt
                                                                                        print("Check the status of Cobalt")
                                                                                        tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
                                                                                        tdkTestObj.addParameter("plugin","Cobalt")
                                                                                        tdkTestObj.executeTestCase(expectedResult)
                                                                                        cobalt_status = tdkTestObj.getResultDetails()
                                                                                        result = tdkTestObj.getResult()
                                                                                        if cobalt_status != 'deactivated' and expectedResult in result:
                                                                                            print("Cobalt is still activated and didnt crash")
                                                                                            tdkTestObj.setResultStatus("SUCCESS")
                                                                                            print("\n Exiting from Cobalt")
                                                                                            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
                                                                                            tdkTestObj.addParameter("plugin","Cobalt")
                                                                                            tdkTestObj.addParameter("status","deactivate")
                                                                                            tdkTestObj.executeTestCase(expectedResult)
                                                                                            result = tdkTestObj.getResult()
                                                                                            if result == "SUCCESS":
                                                                                                tdkTestObj.setResultStatus("SUCCESS")
                                                                                            else:
                                                                                                print("\n Unable to deactivate Cobalt")
                                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                                break
                                                                                        else:
                                                                                            print("HtmlApp is deactivated in between the validation")
                                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                                            break
                                                                                    else:
                                                                                        print("Unable to get the SSH params from the conf file")
                                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                                        break
                                                                                else:
                                                                                    print("Unable to deactivate WebKitBrowser")
                                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                                    break
                                                                            else:
                                                                                print("Failed to set the URL in WebKitBrowser")
                                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                                break
                                                                        else:
                                                                            print("Unable to set the URL in WebKitBrowser")
                                                                            tdkTestObj.setResultStatus("FAILURE")
                                                                            break
                                                                    else:
                                                                        print("Unable to launch WebKitBrowser")
                                                                        tdkTestObj.setResultStatus("FAILURE")
                                                                        break
                                                                else:
                                                                    print("Unable to launch WebKitBrowser")
                                                                    tdkTestObj.setResultStatus("FAILURE")
                                                                    break
                                                            else:
                                                                print("Unable to deactivate LightningApp")
                                                                tdkTestObj.setResultStatus("FAILURE")
                                                                break
                                                        else:
                                                            print("Failed to load the URL in LightningApp")
                                                            tdkTestObj.setResultStatus("FAILURE")
                                                            break
                                                    else:
                                                        print("Failed to set the URL in LightningApp")
                                                        tdkTestObj.setResultStatus("FAILURE")
                                                        break
                                                else:
                                                    print("Failed to launch LightningApp")
                                                    tdkTestObj.setResultStatus("FAILURE")
                                                    break
                                            else:
                                                print("Unable to launch LightningApp")
                                                tdkTestObj.setResultStatus("FAILURE")
                                                break
                                        else:
                                            print("Unable to deactivate HtmlApp")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        print("Failed to load the URL in HtmlApp")
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print("Failed to set the URL in HtmlApp")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print("Failed to launch HtmlApp")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            print("Unable to launch HtmlApp")
                            tdkTestObj.setResultStatus("FAILURE")  
                            break  
                    else:
                        print("\n Error during key press")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                else:
                    print("Failed to launch the URL in Cobalt")
                    tdkTestObj.setResultStatus("FAILURE") 
                    break   
            else:
                print("Failed to launch Cobalt")
                tdkTestObj.setResultStatus("FAILURE");
                break
        if count != launch_and_load_max_count-1:
            print("Test failed at ITERATION #{} -------------------------------------------".format(count+1))
        else:
            print("\n Successfully Completed {} iterations".format(launch_and_load_max_count)) 

    else:
        print("\n Preconditions are not met")
        obj.setLoadModuleStatus("FAILURE")
    if revert=="YES":
        print("Revert the values before exiting")
        status = set_plugins_status(obj,curr_plugins_status_dict) 

    post_condition_status = check_device_state(obj)       
    obj.unloadModule("rdkv_stability") 
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
