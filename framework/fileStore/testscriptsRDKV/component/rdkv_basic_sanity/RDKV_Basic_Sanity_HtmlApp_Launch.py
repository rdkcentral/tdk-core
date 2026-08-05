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

#use tdklib library,which provides a wrapper for tdk testcase script
import tdklib
import time
import MediaValidationVariables
from rdkv_performancelib import *

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_HtmlApp_Launch')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions")
    status = "SUCCESS"
    
    # HtmlApp details from MediaValidationVariables
    html_app_id = MediaValidationVariables.html_player_app_id
    html_app_download_url = MediaValidationVariables.html_player_app_download_url
    
    print("\nHtmlApp Configuration:")
    print(" App ID: %s" %html_app_id)
    print(" Download URL: %s" %html_app_download_url)
    
    # Step 1: Check if HtmlApp is already installed
    print("\n[STEP 1] Checking if HtmlApp is already installed")
    tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
    tdkTestObj.executeTestCase(expectedResult)
    check_result = tdkTestObj.getResult()
    check_details = tdkTestObj.getResultDetails()
    
    app_already_installed = False
    if check_result != "SUCCESS":
        print("FAILURE: Failed to retrieve installed packages")
        tdkTestObj.setResultStatus("FAILURE")
        status = "FAILURE"
    elif html_app_id in check_details:
        print("HtmlApp is already installed")
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = True
    else:
        print("HtmlApp is not installed")
        tdkTestObj.setResultStatus("SUCCESS")
    
    if status == "SUCCESS":
        # Step 2: Uninstall if already installed
        if app_already_installed:
            print("\n[STEP 2] Uninstalling HtmlApp")
            tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
            tdkTestObj.addParameter("app_id", html_app_id)
            tdkTestObj.executeTestCase(expectedResult)
            uninstall_result = tdkTestObj.getResult()
            
            if uninstall_result == "SUCCESS":
                print("HtmlApp uninstalled successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)

            else:
                print("Failed to uninstall HtmlApp")
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print("\n[STEP 2] Skipping uninstall as app is not installed")
        
        if status == "SUCCESS":
            # Step 4: Download HtmlApp bundle
            print("\n[STEP 4] Downloading HtmlApp bundle")
            tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
            tdkTestObj.addParameter("download_url", html_app_download_url)
            tdkTestObj.executeTestCase(expectedResult)
            download_result = tdkTestObj.getResult()
            download_details = tdkTestObj.getResultDetails()
            
            if download_result == "SUCCESS":
                print("HtmlApp bundle downloaded successfully")
                print("Download Details: %s" %download_details)
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)
                
                # Step 5: Install HtmlApp
                print("\n[STEP 5] Installing HtmlApp")
                # Get fileLocator from device config file
                conf_file, result = getConfigFileName(obj.realpath)
                fileLocator = ""
                if result == "SUCCESS":
                    status, fileLocator = getDeviceConfigKeyValue(conf_file, "PACKAGEMANAGER_FILE_LOCATOR")
                if fileLocator != "":
                    fileLocator = fileLocator + str(download_details)
                    print(fileLocator)
                    tdkTestObj = obj.createTestStep('rdkservice_install_app')
                    tdkTestObj.addParameter("app_id", html_app_id)
                    tdkTestObj.addParameter("fileLocator", fileLocator)
                    tdkTestObj.executeTestCase(expectedResult)
                    install_result = tdkTestObj.getResult()
                else:
                    print("Failed to get fileLocator from device config")
                    install_result = "FAILURE"
                
                if install_result == "SUCCESS":
                    print("HtmlApp installed successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(3)
                    
                    # Step 6: Launch HtmlApp
                    print("\n[STEP 6] Launching HtmlApp")
                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                    tdkTestObj.addParameter("app_name", html_app_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    launch_result = tdkTestObj.getResult()
                    
                    if launch_result == "SUCCESS":
                        print("HtmlApp launched successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                        time.sleep(5)
                        
                        # Step 7: Get loaded apps
                        print("\n[STEP 7] Getting loaded apps")
                        tdkTestObj = obj.createTestStep('rdkservice_get_loaded_apps')
                        tdkTestObj.executeTestCase(expectedResult)
                        loaded_apps_result = tdkTestObj.getResult()
                        loaded_apps_details = tdkTestObj.getResultDetails()
                        
                        if loaded_apps_result == "SUCCESS":
                            print("Successfully retrieved loaded apps")
                            print("Loaded Apps Details: %s" %loaded_apps_details)
                            
                            # Verify if HtmlApp is in loaded apps
                            if "HtmlApp" in loaded_apps_details or html_app_id in loaded_apps_details:
                                print("HtmlApp is in loaded apps")
                                tdkTestObj.setResultStatus("SUCCESS")
                                
                                # Step 8: Terminate HtmlApp
                                print("\n[STEP 8] Terminating HtmlApp")
                                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                tdkTestObj.addParameter("app_id", html_app_id)
                                tdkTestObj.executeTestCase(expectedResult)
                                terminate_result = tdkTestObj.getResult()
                                
                                if terminate_result == "SUCCESS":
                                    print("HtmlApp terminated successfully")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print("Failed to terminate HtmlApp")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("HtmlApp is NOT in loaded apps")
                                print("Expected HtmlApp not found in: %s" %loaded_apps_details)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("Failed to retrieve loaded apps")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("Failed to launch HtmlApp")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Failed to install HtmlApp")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")

