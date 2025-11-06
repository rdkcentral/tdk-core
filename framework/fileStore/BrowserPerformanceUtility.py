##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2020 RDK Management
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
#########################################################################
import time
from StabilityTestUtility import *

expectedResult ="SUCCESS"
#METHODS
#---------------------------------------------------------------
#CHECK FOR THE PRE_REQUISITES
#---------------------------------------------------------------
def check_pre_requisites(obj):
    conf_file, status = get_configfile_name(obj)
    status,supported_plugins = getDeviceConfigValue(conf_file, "SUPPORTED_PLUGINS")
    plugins_list = ['WebKitBrowser', 'Cobalt']
    plugin_statuses = {}
    tdkTestObj = obj.createTestStep('rdkservice_getPluginStatus')
    for plugin in plugins_list:
        if plugin in supported_plugins:
            tdkTestObj.addParameter("plugin", plugin)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResult()
            status = tdkTestObj.getResultDetails()
            plugin_statuses[plugin] = {
                'result': result,
                'status': status
            }
        else:
            plugin_statuses[plugin] = {
                'result': "SUCCESS",
                'status': "SUCCESS"
            }
    webkit_result = plugin_statuses.get("WebKitBrowser", {}).get('result', "SUCCESS")
    webkit_status = plugin_statuses.get("WebKitBrowser", {}).get('status', "SUCCESS")
    cobalt_result = plugin_statuses.get("Cobalt", {}).get('result', "SUCCESS")
    cobalt_status = plugin_statuses.get("Cobalt", {}).get('status', "SUCCESS")
    expected_status_list = ["deactivated", "suspended", "None", "SUCCESS"]
    expected_webkit_status = "resumed"
    status_list = ["activated", "deactivated", "resumed", "suspended", "None", "SUCCESS"]
    if "FAILURE" not in (webkit_result, cobalt_result):
        if all(status in status_list for status in [webkit_status, cobalt_status]):
            tdkTestObj.setResultStatus("SUCCESS")
        else:
            tdkTestObj.setResultStatus("FAILURE")
        
        if cobalt_status in expected_status_list and webkit_status == expected_webkit_status:
            return ("SUCCESS", webkit_status, cobalt_status)
        else:
            return ("FAILURE", webkit_status, cobalt_status)
    else:
        return ("FAILURE", webkit_result, cobalt_result)

#--------------------------------------------------------------------
#SET PRE_REQUISITES
#---------------------------------------------------------------------
def set_pre_requisites(obj):
    conf_file, status = get_configfile_name(obj)
    status, supported_plugins = getDeviceConfigValue(conf_file, "SUPPORTED_PLUGINS")
    plugin_statuses = {
        "Cobalt": {"result": "SUCCESS", "status": "Not Supported"},
        "WebKitBrowser": {"result": "SUCCESS", "status": "Not Supported"}
    }
    
    if "Cobalt" in supported_plugins:
        print("\nDeactivating Cobalt")
        tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
        tdkTestObj.addParameter("plugin", "Cobalt")
        tdkTestObj.addParameter("status", "deactivate")
        tdkTestObj.executeTestCase(expectedResult)
        result1 = tdkTestObj.getResult()
        time.sleep(5)
        plugin_statuses["Cobalt"]["result"] = result1
        plugin_statuses["Cobalt"]["status"] = "Deactivated"
        print(f"Cobalt Status: {plugin_statuses['Cobalt']['status']}")
    else:
        print("Cobalt not in supported plugins. Skipping deactivation.")
    
    if "WebKitBrowser" in supported_plugins:
        print("\nActivate and resume WebKitBrowser")
        params = '{"callsign":"WebKitBrowser", "type":"", "uri":""}'
        tdkTestObj = obj.createTestStep('rdkservice_setValue')
        tdkTestObj.addParameter("method", "org.rdk.RDKShell.1.launch")
        tdkTestObj.addParameter("value", params)
        tdkTestObj.executeTestCase(expectedResult)
        result2 = tdkTestObj.getResult()
        time.sleep(5)
        plugin_statuses["WebKitBrowser"]["result"] = result2
        plugin_statuses["WebKitBrowser"]["status"] = "Activated and Resumed"
        print(f"WebKitBrowser Status: {plugin_statuses['WebKitBrowser']['status']}")
    else:
        print("WebKitBrowser not in supported plugins. Skipping activation.")
    
    if all(plugin_statuses[plugin]["result"] == "SUCCESS" for plugin in plugin_statuses):
        tdkTestObj.setResultStatus("SUCCESS")
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        return "FAILURE"   
    
#---------------------------------------------------------------------
#REVERT THE VALUES
#---------------------------------------------------------------------
def revert_value(curr_webkit_status,curr_cobalt_status,obj):
    conf_file, status = get_configfile_name(obj)
    status, supported_plugins = getDeviceConfigValue(conf_file, "SUPPORTED_PLUGINS")

    if "WebKitBrowser" in supported_plugins:
        webkit_status = "SUCCESS" if curr_webkit_status == "None" else "FAILURE"
        if curr_webkit_status != "deactivated" and curr_webkit_status != "None":
            print("WebKit was activated")
        elif curr_webkit_status == "deactivated":
            print("WebKit was deactivated")
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin", "WebKitBrowser")
            tdkTestObj.addParameter("status", "deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            webkit_status = tdkTestObj.getResult()
    else:
        print("WebKitBrowser not in supported plugins. Skipping WebKit revert.")
        webkit_status = "SUCCESS" 

    if "Cobalt" in supported_plugins:
        print("\nRevert Cobalt status")
        cobalt_status = "SUCCESS" if curr_cobalt_status == "None" else "FAILURE"
        if curr_cobalt_status != "deactivated" and curr_cobalt_status != "None":
            print("Cobalt was activated")
            params = '{"callsign":"Cobalt", "type":"", "uri":""}'
            tdkTestObj = obj.createTestStep('rdkservice_setValue')
            tdkTestObj.addParameter("method", "org.rdk.RDKShell.1.launch")
            tdkTestObj.addParameter("value", params)
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_status = tdkTestObj.getResult()
        elif curr_cobalt_status == "deactivated":
            print("Cobalt was deactivated")
            tdkTestObj = obj.createTestStep('rdkservice_setPluginStatus')
            tdkTestObj.addParameter("plugin", "Cobalt")
            tdkTestObj.addParameter("status", "deactivate")
            tdkTestObj.executeTestCase(expectedResult)
            cobalt_status = tdkTestObj.getResult()
    else:
        print("Cobalt not in supported plugins. Skipping Cobalt revert.")
        cobalt_status = "SUCCESS"  

    if all(status == "SUCCESS" for status in [webkit_status, cobalt_status]):
        tdkTestObj.setResultStatus("SUCCESS")
        return "SUCCESS"
    else:
        tdkTestObj.setResultStatus("FAILURE")
        return "FAILURE"
