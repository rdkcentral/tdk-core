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
import tdklib
import ast
import time
import web_socket_util
from web_socket_util import *
import rdkv_appmanagerslib
from rdkv_appmanagerslib import wait_for_event
import json

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_appmanagers","1",standAlone=True)

#IP and Port of device type, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_CERT_AppManagers_Functional_Check_OnBlur_Event')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

# Predefined variables which will be used in the script
installation_status_dict = {}
download_status_dict = {}
launch_status_dict = {}
event_listener = None
applications = []
app_presence_status_dict = {}
filelocator_url_dict = {}
blur_status = "FALSE"

if "SUCCESS" in result.upper():
    # Step 1 : Get the device configuration values
    print("\n")
    configkeylist = ["PACKAGEMANAGER_APPLICATION_HOSTEDURL","PACKAGEMANAGER_APPLICATION_DOWNLOAD_TIME","PACKAGEMANAGER_APPLICATION_NAME","PACKAGEMANAGER_APPLICATION_VERSION","PACKAGEMANAGER_ADDITIONALMETADATA_NAME","PACKAGEMANAGER_ADDITIONALMETADATA_VALUE","PACKAGEMANAGER_SECOND_APPLICATION_HOSTEDURL","PACKAGEMANAGER_SECOND_APPLICATION_NAME"]
    tdkTestObj = obj.createTestStep('appmanagers_getdeviceconfig')
    tdkTestObj.addParameter("configkeylist",configkeylist)
    tdkTestObj.executeTestCase(expectedResult)
    result = tdkTestObj.getResultDetails()
    result = ast.literal_eval(result)
    download_url = result[0]["PACKAGEMANAGER_APPLICATION_HOSTEDURL"]
    download_time = result[0]["PACKAGEMANAGER_APPLICATION_DOWNLOAD_TIME"]
    application_name = result[0]["PACKAGEMANAGER_APPLICATION_NAME"]
    application_version = result[0]["PACKAGEMANAGER_APPLICATION_VERSION"]
    additionalmetadata_name = result[0]["PACKAGEMANAGER_ADDITIONALMETADATA_NAME"]
    additionalmetadata_value = result[0]["PACKAGEMANAGER_ADDITIONALMETADATA_VALUE"]
    second_application_hostedurl = result[0]["PACKAGEMANAGER_SECOND_APPLICATION_HOSTEDURL"]
    second_application_name = result[0]["PACKAGEMANAGER_SECOND_APPLICATION_NAME"]
    # Pairing first and second application name together
    applications = [ (application_name, download_url), (second_application_name, second_application_hostedurl) ]

    if "SUCCESS" in result[1]:
        tdkTestObj.setResultStatus("SUCCESS")
        
        # Step 2 : Check the status of the dependent plugins
        print("\n")
        pluginlist = ["org.rdk.AppStorageManager", "org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager", "org.rdk.RDKWindowManager"]
        tdkTestObj = obj.createTestStep('appmanagers_checkpluginstatus')
        tdkTestObj.addParameter("pluginlist",pluginlist)
        tdkTestObj.executeTestCase(expectedResult)
        result = tdkTestObj.getResultDetails()
        if "SUCCESS" in result:
            tdkTestObj.setResultStatus("SUCCESS")

            # Register and Listen the events
            print("\nRegistering and Listening to the events")
            thunder_port = rdkv_appmanagerslib.devicePort
            deviceToken = rdkv_appmanagerslib.deviceToken
            web_socket_util.deviceToken = deviceToken
            payloads = []
            # Format of events list is : '{"callsign": "eventname"}'
            events = ['{"org.rdk.DownloadManager": "onAppDownloadStatus"}','{"org.rdk.PackageManagerRDKEMS": "onAppInstallationStatus"}','{"org.rdk.RDKWindowManager": "onBlur"}']
            for item in events:
                parsed_item = json.loads(item)
                for callsign, event_name in parsed_item.items():
                    payload = '{"jsonrpc": "2.0","id": 1,"method": "'+callsign+'.1.register","params": {"event": "'+event_name+'", "id": "client.events.1" }}'
                    payloads.append(payload)
            print("Event Registration List : ", payloads)
            event_listener = createEventListener(ip,thunder_port,payloads,"/jsonrpc",False)
            
            # Step 3 : Check whether the package is already installed if installed skip download and installation steps
            time.sleep(10)
            for app_name, app_url in applications:
                print("\n")
                method = "org.rdk.AppManager.1.isInstalled"
                value = '{"appId": "'+app_name+'"}'
                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",value)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                if "error" in result and "result" not in result:
                    print("FAILURE : Failed to get the installation status of the package")
                    tdkTestObj.setResultStatus("FAILURE")
                    break
                if "error" not in result and "result" in result and result["result"] == True:
                    print("INFO : Package %s is already installed, skipping download and installation steps" % app_name)
                    tdkTestObj.setResultStatus("SUCCESS")
                    app_presence_status_dict[app_name] = "TRUE"
                if "error" not in result and "result" in result and result["result"] == False:
                    tdkTestObj.setResultStatus("SUCCESS")
                    print("INFO : Package is not installed, proceeding with download and installation steps")

                    # Clear the event buffer before waiting for events to avoid processing old events
                    event_listener.clearEventsBuffer()
                    # Step 4 : Download the package
                    print("\n")
                    method = "org.rdk.DownloadManager.1.download"
                    value = '{"url": "'+app_url+'"}'
                    tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    if "error" not in result and "result" in result and result["result"] not in (None, '', 'NONE'):
                        download_id = result["result"]
                        print("SUCCESS : Package download initiated successfully and download ID is : ", download_id)

                        # Wait for the download status event and check the download status
                        event_log = wait_for_event(event_listener)
                        if len(event_log) > 0:
                            for entry in event_log:
                                _, json_part = entry.split("$$$", 1)
                                json_part = json_part.encode().decode("unicode_escape")
                                outer = json.loads(json_part)
                                inner = json.loads(outer["params"]["downloadStatus"])
                                #print("\nParsed Event : ", inner)
                                event_download_id = inner[0]["downloadId"]
                                filelocator_url = inner[0]["fileLocator"]
                                filelocator_url_dict[app_name] = filelocator_url
                                if ( event_download_id == download_id and filelocator_url not in (None, '', 'NONE') ):
                                    print("SUCCESS : Package download successful with correct download status")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    download_status_dict[app_name] = "TRUE"
                                    break

                            if download_status_dict and download_status_dict[app_name] == "TRUE":
                                # Clear the event buffer before waiting for events to avoid processing old events
                                event_listener.clearEventsBuffer()
                                # Step 5 : Form filelocator URL and Install the package
                                print("\n")
                                time.sleep(int(download_time))
                                method = "org.rdk.PackageManagerRDKEMS.1.install"
                                value = '{ "packageId": "'+app_name+'", "version": "'+application_version+'", "additionalMetadata": [ {"name": "'+additionalmetadata_name+'", "value": "'+additionalmetadata_value+'"} ], "fileLocator": "'+filelocator_url+'" }'
                                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                                tdkTestObj.addParameter("method",method)
                                tdkTestObj.addParameter("value",value)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                result = ast.literal_eval(result)
                                if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                                    print("INFO : Package installation initiated, waiting for installation status event...")

                                    # Wait for the installation status event and check the installation status
                                    event_log = wait_for_event(event_listener)
                                    if len(event_log) > 0:
                                        for entry in event_log:
                                            _, json_part = entry.split("$$$", 1)
                                            json_part = json_part.encode().decode("unicode_escape")
                                            outer = json.loads(json_part)
                                            inner = json.loads(outer["params"]["jsonresponse"])
                                            #print("\nParsed Event : ", inner)
                                            package_id = inner[0]["packageId"]
                                            version = inner[0]["version"]
                                            state = inner[0]["state"]
                                            if ( package_id == app_name and version == application_version and state == "INSTALLED" ):
                                                print("SUCCESS : Application installation successful with correct installation status")
                                                tdkTestObj.setResultStatus("SUCCESS")
                                                installation_status_dict[app_name] = "TRUE"
                                                break
                                        if installation_status_dict and installation_status_dict[app_name] != "TRUE":
                                            print("FAILURE : Application installation failed or incorrect installation status received in event")
                                            tdkTestObj.setResultStatus("FAILURE")
                                            break
                                    else:
                                        tdkTestObj.setResultStatus("FAILURE")
                                        break
                                else:
                                    print("FAILURE : Failed to initiate package installation")
                                    tdkTestObj.setResultStatus("FAILURE")
                                    break
                            else:
                                print("FAILURE : Package download failed or incorrect download status received in event")
                                tdkTestObj.setResultStatus("FAILURE")
                                break
                        else:
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                        print("FAILURE : Failed to initiate package download")
                        break
            
            if (app_presence_status_dict and "FALSE" not in app_presence_status_dict.values()) or (installation_status_dict and "FALSE" not in installation_status_dict.values()):
                print("\nINFO : %s are present, proceeding with launch steps" % applications)

                # Clear the event buffer before waiting for events to avoid processing old events
                event_listener.clearEventsBuffer()
                # Step 6 : Launch the first application
                print("\n")
                time.sleep(5)
                method = "org.rdk.AppManager.1.launchApp"
                value = '{"appId": "'+application_name+'"}'
                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                tdkTestObj.addParameter("method",method)
                tdkTestObj.addParameter("value",value)
                tdkTestObj.executeTestCase(expectedResult)
                result = tdkTestObj.getResultDetails()
                result = ast.literal_eval(result)
                if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                    print("SUCCESS : Application launch initiated successfully")

                    # Step 7 : Get the launched applications list and check whether the first application is in active state
                    print("\n")
                    time.sleep(10)
                    method = "org.rdk.AppManager.1.getLoadedApps"
                    tdkTestObj = obj.createTestStep('appmanagers_getvalue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    if "error" not in result and "result" in result and result["result"] not in (None, '', 'NONE'):
                        for app in result["result"]:
                            if app["appId"] == application_name and app["lifecycleState"] == "APP_STATE_ACTIVE":
                                print("SUCCESS : First application is in active state after launch")
                                first_app_instance_id = app["appInstanceId"]
                                launch_status_dict[application_name] = "TRUE"
                                tdkTestObj.setResultStatus("SUCCESS")
                                break
                                
                        if launch_status_dict and launch_status_dict.get(application_name) == "TRUE":
                            # Clear the event buffer before waiting for events to avoid processing old events
                            event_listener.clearEventsBuffer()
                            # Step 8 : Launch the second application
                            print("\n")
                            time.sleep(5)
                            method = "org.rdk.AppManager.1.launchApp"
                            value = '{"appId": "'+second_application_name+'"}'
                            tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                            tdkTestObj.addParameter("method",method)
                            tdkTestObj.addParameter("value",value)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            result = ast.literal_eval(result)
                            if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                                print("SUCCESS : Application launch initiated successfully")

                                # Step 9 : Get the launched applications list and check whether the second application is in active state
                                print("\n")
                                time.sleep(10)
                                method = "org.rdk.AppManager.1.getLoadedApps"
                                tdkTestObj = obj.createTestStep('appmanagers_getvalue')
                                tdkTestObj.addParameter("method",method)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                result = ast.literal_eval(result)
                                if "error" not in result and "result" in result and result["result"] not in (None, '', 'NONE'):
                                    for app in result["result"]:
                                        if app["appId"] == second_application_name and app["lifecycleState"] == "APP_STATE_ACTIVE":
                                            print("SUCCESS : Second application is in active state after launch")
                                            launch_status_dict[second_application_name] = "TRUE"
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            break
                                        
                                    if launch_status_dict and launch_status_dict.get(second_application_name) == "TRUE":
                                        # Wait for the onblur event and check whether the first application goes to background
                                        event_log = wait_for_event(event_listener)
                                        if len(event_log) > 0:
                                            for entry in event_log:
                                                _, json_part = entry.split("$$$", 1)
                                                json_part = json_part.encode().decode("unicode_escape")
                                                outer = json.loads(json_part)
                                                inner = outer["params"]
                                                #print("\nParsed Event : ", inner)
                                                second_app_instance_Id = inner["appInstanceId"]
                                                if second_app_instance_Id == first_app_instance_id:
                                                    print("SUCCESS : onBlur event received with correct appInstanceId for the first application")
                                                    tdkTestObj.setResultStatus("SUCCESS")
                                                    blur_status = "TRUE"
                                                    break
                                            if blur_status != "TRUE":
                                                print("FAILURE : onBlur event not received for the first application after launching the second application")
                                                tdkTestObj.setResultStatus("FAILURE")
                                        else:
                                            tdkTestObj.setResultStatus("FAILURE")
                                    else:
                                        print("FAILURE : Second application is not in active state after launch")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("FAILURE : Failed to get the launched applications list")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("FAILURE : Failed to initiate application launch")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("FAILURE : First application is not in active state after launch")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("FAILURE : Failed to get the launched applications list")
                        tdkTestObj.setResultStatus("FAILURE")                  
                else:
                    print("FAILURE : Failed to initiate application launch")
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")

        if launch_status_dict and "TRUE" in launch_status_dict.values():
            for key, value in launch_status_dict.items():
                if value == "TRUE":
                    # Step 9 : Terminate the launched application
                    print("\n")
                    time.sleep(3)
                    method = "org.rdk.AppManager.1.terminateApp"
                    value = '{"appId": "'+key+'"}'
                    tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                        print("SUCCESS : Application termination initiated successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE : Failed to initiate application termination")
                        tdkTestObj.setResultStatus("FAILURE")
                        break
                    
        if installation_status_dict and "TRUE" in installation_status_dict.values():
            for key, value in installation_status_dict.items():
                if value == "TRUE":
                    # Step 10 : Uninstall the package
                    print("\n")
                    time.sleep(3)
                    method = "org.rdk.PackageManagerRDKEMS.1.uninstall"
                    value = '{ "packageId": "'+key+'"}'
                    tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                        print("SUCCESS : Package uninstallation successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE : Package uninstallation failed")
                        tdkTestObj.setResultStatus("FAILURE")
                        break

        if download_status_dict and filelocator_url_dict and "TRUE" in download_status_dict.values():
            for key, value in download_status_dict.items():
                for key1, value1 in filelocator_url_dict.items():
                        if key == key1 and value == "TRUE" and value1 is not None:
                            filelocator_url = value1
                            # Step 11 : Delete the package
                            print("\n")
                            time.sleep(3)
                            method = "org.rdk.DownloadManager.1.delete"
                            value = '{"fileLocator": "'+filelocator_url+'"}'
                            tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                            tdkTestObj.addParameter("method",method)
                            tdkTestObj.addParameter("value",value)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            result = ast.literal_eval(result)
                            if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                                print("SUCCESS : Package deleted successfully")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("FAILURE : Package deletion failed")
                                tdkTestObj.setResultStatus("FAILURE")
                                break

        if event_listener:
            # Closing the websocket connection
            print("\nUnregistering the events and closing the websocket connection")
            event_listener.disconnect()
            time.sleep(10)
            
    else:
        tdkTestObj.setResultStatus("FAILURE")
else:
    print("FAILURE : Module Loading Status Failure\n")
    obj.setLoadModuleStatus("FAILURE")

# Unload the module
print("\n")
obj.unloadModule("rdkv_appmanagers")
