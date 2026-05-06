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
obj.configureTestCase(ip,port,'RDKV_CERT_AppManagers_Functional_App_Terminate_ContainerMode_Status_Check')

# Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)

obj.setLoadModuleStatus(result.upper())

expectedResult = "SUCCESS"

# Predefined variables which will be used in the script
installation_status = "FALSE"
download_status = "FALSE"
launch_status = "FALSE"
container_status = "FALSE"
terminate_status = "FALSE"  
event_listener = None

if "SUCCESS" in result.upper():
    # Step 1 : Get the device configuration values
    print("\n")
    configkeylist = ["SSH_METHOD","SSH_USERNAME","SSH_PASSWORD","PACKAGEMANAGER_APPLICATION_HOSTEDURL","PACKAGEMANAGER_APPLICATION_DOWNLOAD_TIME","PACKAGEMANAGER_APPLICATION_NAME","PACKAGEMANAGER_APPLICATION_VERSION","PACKAGEMANAGER_ADDITIONALMETADATA_NAME","PACKAGEMANAGER_ADDITIONALMETADATA_VALUE"]
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
    if "SUCCESS" in result[1]:
        tdkTestObj.setResultStatus("SUCCESS")

        # Step 2 : Check the status of the dependent plugins
        print("\n")
        pluginlist = ["org.rdk.AppStorageManager", "org.rdk.DownloadManager", "org.rdk.PackageManagerRDKEMS", "org.rdk.AppManager","org.rdk.RDKWindowManager"]
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
            events = ['{"org.rdk.DownloadManager": "onAppDownloadStatus"}','{"org.rdk.PackageManagerRDKEMS": "onAppInstallationStatus"}','{"org.rdk.AppManager": "onAppLifecycleStateChanged"}']
            for item in events:
                parsed_item = json.loads(item)
                for callsign, event_name in parsed_item.items():
                    payload = '{"jsonrpc": "2.0","id": 1,"method": "'+callsign+'.1.register","params": {"event": "'+event_name+'", "id": "client.events.1" }}'
                    payloads.append(payload)
            print("Event Registration List : ", payloads)
            event_listener = createEventListener(ip,thunder_port,payloads,"/jsonrpc",False)
            
            # Step 3 : Check whether the package is already installed if installed skip download and installation steps
            time.sleep(10)
            print("\n")
            method = "org.rdk.AppManager.1.isInstalled"
            value = '{"appId": "'+application_name+'"}'
            tdkTestObj = obj.createTestStep('appmanagers_setvalue')
            tdkTestObj.addParameter("method",method)
            tdkTestObj.addParameter("value",value)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            result = ast.literal_eval(result)
            if "error" in result and "result" not in result:
                print("FAILURE : Failed to get the installation status of the package")
                tdkTestObj.setResultStatus("FAILURE")
            if "error" not in result and "result" in result and result["result"] == False:
                tdkTestObj.setResultStatus("SUCCESS")
                print("INFO : Package is not installed, proceeding with download and installation steps")

                # Step 4 : Download the package
                print("\n")
                method = "org.rdk.DownloadManager.1.download"
                value = '{"url": "'+download_url+'"}'
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
                            if ( event_download_id == download_id and filelocator_url not in (None, '', 'NONE') ):
                                print("SUCCESS : Package download successful with correct download status")
                                tdkTestObj.setResultStatus("SUCCESS")
                                download_status = "TRUE"
                                break

                        if download_status == "TRUE":
                            # Clear the event buffer before waiting for events to avoid processing old events
                            event_listener.clearEventsBuffer()
                            # Step 5 : Form filelocator URL and Install the package
                            print("\n")
                            time.sleep(int(download_time))
                            #filelocator_url = filelocator_url + str(download_id)
                            method = "org.rdk.PackageManagerRDKEMS.1.install"
                            value = '{ "packageId": "'+application_name+'", "version": "'+application_version+'", "additionalMetadata": [ {"name": "'+additionalmetadata_name+'", "value": "'+additionalmetadata_value+'"} ], "fileLocator": "'+filelocator_url+'" }'
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
                                        if ( package_id == application_name and version == application_version and state == "INSTALLED" ):
                                            print("SUCCESS : Application installation successful with correct installation status")
                                            tdkTestObj.setResultStatus("SUCCESS")
                                            installation_status = "TRUE"
                                            break
                                    if installation_status != "TRUE":
                                        print("FAILURE : Application installation failed or incorrect installation status received in event")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("FAILURE : Failed to initiate package installation")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("FAILURE : Package download failed or incorrect download status received in event")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    tdkTestObj.setResultStatus("FAILURE")
                    print("FAILURE : Failed to initiate package download")
            
            if ("error" not in result and "result" in result) or result["result"] == True or installation_status == "TRUE":
                print("INFO : Package is installed, proceeding with launch step")

                # Clear the event buffer before waiting for events to avoid processing old events
                event_listener.clearEventsBuffer()
                # Step 6 : Launch the application
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
                    print("SUCCESS : Application launched successfully")

                    # Wait for the lifecycle status event and check the lifecycle status
                    event_log = wait_for_event(event_listener)
                    if len(event_log) > 0:
                        for entry in event_log:
                            _, json_part = entry.split("$$$", 1)
                            json_part = json_part.encode().decode("unicode_escape")
                            outer = json.loads(json_part)
                            inner = outer["params"]
                            #print("\nParsed Event : ", inner)
                            appId = inner["appId"]
                            newState = inner["newState"]
                            errorReason = inner["errorReason"]
                            appInstanceId = inner["appInstanceId"]
                            if appId == application_name and newState == "APP_STATE_ACTIVE" and errorReason == "APP_ERROR_NONE":
                                print("SUCCESS : Application launch successful with correct lifecycle state")
                                tdkTestObj.setResultStatus("SUCCESS")
                                launch_status = "TRUE"
                                break
                
                        if launch_status == "TRUE":
                            # Step 7 : Check the launched application is running in container mode
                            print("\n")
                            time.sleep(3)
                            command = "DobbyTool list"
                            tdkTestObj = obj.createTestStep('appmanagers_executeInDUT')
                            tdkTestObj.addParameter("command", command)
                            tdkTestObj.executeTestCase(expectedResult)
                            result = tdkTestObj.getResultDetails()
                            print("\nExecuting Command : %s" %command)
                            print("Output of executing command : %s" %result)
                            result = result.splitlines()
                            for line in result:
                                if appInstanceId in line.lower() and "running" in line.lower():
                                    print("SUCCESS : Launched application is running in container mode")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    container_status = "TRUE"
                                    break
                            if container_status == "TRUE":
                                # Step 8 : Terminate the application
                                print("\n")
                                time.sleep(3)
                                method  = "org.rdk.AppManager.1.terminateApp"
                                value = '{"appId": "'+application_name+'"}'
                                tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                                tdkTestObj.addParameter("method",method)
                                tdkTestObj.addParameter("value",value)
                                tdkTestObj.executeTestCase(expectedResult)
                                result = tdkTestObj.getResultDetails()
                                result = ast.literal_eval(result)
                                if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                                    print("SUCCESS : Application terminated successfully")
                                    tdkTestObj.setResultStatus("SUCCESS")

                                    # Step 9 : Check the terminated application is not running in container mode
                                    print("\n")
                                    time.sleep(3)
                                    container_status = "FALSE"
                                    command = "DobbyTool list"
                                    tdkTestObj = obj.createTestStep('appmanagers_executeInDUT')
                                    tdkTestObj.addParameter("command", command)
                                    tdkTestObj.executeTestCase(expectedResult)
                                    result = tdkTestObj.getResultDetails()
                                    print("\nExecuting Command : %s" %command)
                                    print("Output of executing command : %s" %result)
                                    result = result.splitlines()
                                    for line in result:
                                        if appInstanceId in line.lower():
                                            container_status = "TRUE"
                                            break
                                    if container_status != "TRUE":
                                        print("SUCCESS : Terminated application is not running in container mode")
                                        tdkTestObj.setResultStatus("SUCCESS")
                                    else:
                                        print("FAILURE : Terminated application is still running in container mode")
                                        tdkTestObj.setResultStatus("FAILURE")
                                else:
                                    print("FAILURE : Failed to terminate the application")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("FAILURE : Launched application is not running in container mode")
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("FAILURE : Application launch failed or incorrect lifecycle state received in event")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        tdkTestObj.setResultStatus("FAILURE")                    
                else:
                    print("FAILURE : Application launch failed")
                    tdkTestObj.setResultStatus("FAILURE")
        else:
            tdkTestObj.setResultStatus("FAILURE")

        if launch_status == "TRUE":
            # Step 10 : Check whether the launched application is present in loaded apps list before termination
            print("\n")
            time.sleep(3)
            method = "org.rdk.AppManager.1.getLoadedApps"
            tdkTestObj = obj.createTestStep('appmanagers_getvalue')
            tdkTestObj.addParameter("method",method)
            tdkTestObj.executeTestCase(expectedResult)
            result = tdkTestObj.getResultDetails()
            result = ast.literal_eval(result)
            if "error" not in result and "result" in result and result["result"] not in (None, '', 'NONE'):
                result = result["result"]
                for app in result:
                     if app["appId"] == application_name:
                        print("INFO : Application is present in loaded apps list so proceeding with termination")
                        terminate_status = "TRUE"
                        break
                
                if terminate_status == "TRUE":
                    # Step 11 : Terminate the application
                    print("\n")
                    time.sleep(3)
                    method  = "org.rdk.AppManager.1.terminateApp"
                    value = '{"appId": "'+application_name+'"}'
                    tdkTestObj = obj.createTestStep('appmanagers_setvalue')
                    tdkTestObj.addParameter("method",method)
                    tdkTestObj.addParameter("value",value)
                    tdkTestObj.executeTestCase(expectedResult)
                    result = tdkTestObj.getResultDetails()
                    result = ast.literal_eval(result)
                    if "error" not in result and "result" in result and result["result"] in (None, '', 'NONE'):
                        print("SUCCESS : Application terminated successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE : Failed to terminate the application")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("INFO : Application not present in loaded apps list, skipped terminate step")
                    tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("FAILURE : Failed to get the loaded apps list")
                tdkTestObj.setResultStatus("FAILURE")
        
        if installation_status == "TRUE":
            # Step 12 : Uninstall the package
            print("\n")
            time.sleep(3)
            method = "org.rdk.PackageManagerRDKEMS.1.uninstall"
            value = '{ "packageId": "'+application_name+'"}'
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

        if download_status == "TRUE":
            # Step 13 : Delete the package
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
