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
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_LightningApp_Launch')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS]  :  %s" %result)
obj.setLoadModuleStatus(result)

expectedResult = "SUCCESS"
if expectedResult in result.upper():
    print("\nCheck Pre conditions")
    status = "SUCCESS"
    
    # LightningApp details from MediaValidationVariables
    lightning_app_id = MediaValidationVariables.unified_player_app_id
    lightning_app_download_url = MediaValidationVariables.unified_player_app_download_url
    
    print("\nLightningApp Configuration:")
    print("  App ID: %s" %lightning_app_id)
    print("  Download URL: %s" %lightning_app_download_url)
    
    # Step 1: Check if LightningApp is already installed
    print("\n[STEP 1] Checking if LightningApp is already installed")
    tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
    tdkTestObj.executeTestCase(expectedResult)
    check_result = tdkTestObj.getResult()
    check_details = tdkTestObj.getResultDetails()
    
    app_already_installed = False
    if check_result != "SUCCESS":
        print("FAILURE: Failed to retrieve installed packages")
        tdkTestObj.setResultStatus("FAILURE")
        status = "FAILURE"
    elif lightning_app_id in check_details:
        print("LightningApp is already installed")
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = True
    else:
        print("LightningApp is not installed")
        tdkTestObj.setResultStatus("SUCCESS")
    
    if status == "SUCCESS":
        # Step 2: Uninstall if already installed
        if app_already_installed:
            print("\n[STEP 2] Uninstalling LightningApp")
            tdkTestObj = obj.createTestStep('rdkservice_uninstall_app')
            tdkTestObj.addParameter("app_id", lightning_app_id)
            tdkTestObj.executeTestCase(expectedResult)
            uninstall_result = tdkTestObj.getResult()
            
            if uninstall_result == "SUCCESS":
                print("LightningApp uninstalled successfully")
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)
                
                # Reboot device after uninstalling
                print("\n[STEP 3] Rebooting device after uninstall")
                pre_requisite_reboot(obj,"yes")
                time.sleep(5)
            else:
                print("Failed to uninstall LightningApp")
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print("\n[STEP 2] Skipping uninstall as app is not installed")
        
        if status == "SUCCESS":
            # Step 4: Download LightningApp bundle
            print("\n[STEP 4] Downloading LightningApp bundle")
            tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
            tdkTestObj.addParameter("download_url", lightning_app_download_url)
            tdkTestObj.executeTestCase(expectedResult)
            download_result = tdkTestObj.getResult()
            download_details = tdkTestObj.getResultDetails()
            
            if download_result == "SUCCESS":
                print("LightningApp bundle downloaded successfully")
                print("Download Details: %s" %download_details)
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)
                
                # Step 5: Install LightningApp
                print("\n[STEP 5] Installing LightningApp")
                # Get fileLocator from device config file
                conf_file, result = getConfigFileName(obj.realpath)
                fileLocator = ""
                if result == "SUCCESS":
                    status, fileLocator = getDeviceConfigKeyValue(conf_file, "PACKAGEMANAGER_FILE_LOCATOR")
                if fileLocator != "":
                    fileLocator = fileLocator + str(download_details)
                    print(fileLocator)
                    tdkTestObj = obj.createTestStep('rdkservice_install_app')
                    tdkTestObj.addParameter("app_id", lightning_app_id)
                    tdkTestObj.addParameter("fileLocator", fileLocator)
                    tdkTestObj.executeTestCase(expectedResult)
                    install_result = tdkTestObj.getResult()
                else:
                    print("Failed to get fileLocator from device config")
                    install_result = "FAILURE"
                
                if install_result == "SUCCESS":
                    print("LightningApp installed successfully")
                    tdkTestObj.setResultStatus("SUCCESS")
                    time.sleep(3)
                    
                    # Step 6: Launch LightningApp
                    print("\n[STEP 6] Launching LightningApp")
                    tdkTestObj = obj.createTestStep('rdkservice_launch_app')
                    tdkTestObj.addParameter("app_name", lightning_app_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    launch_result = tdkTestObj.getResult()
                    
                    if launch_result == "SUCCESS":
                        print("LightningApp launched successfully")
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
                            
                            # Verify if LightningApp ID is in loaded apps
                            if lightning_app_id in loaded_apps_details:
                                print("LightningApp ID %s is in loaded apps" %lightning_app_id)
                                tdkTestObj.setResultStatus("SUCCESS")
                                
                                # Step 8: Terminate LightningApp
                                print("\n[STEP 8] Terminating LightningApp")
                                tdkTestObj = obj.createTestStep('rdkv_terminate_app')
                                tdkTestObj.addParameter("app_id", lightning_app_id)
                                tdkTestObj.executeTestCase(expectedResult)
                                terminate_result = tdkTestObj.getResult()
                                
                                if terminate_result == "SUCCESS":
                                    print("LightningApp terminated successfully")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                else:
                                    print("Failed to terminate LightningApp")
                                    tdkTestObj.setResultStatus("FAILURE")
                            else:
                                print("LightningApp ID %s is NOT in loaded apps" %lightning_app_id)
                                print("Expected app ID not found in: %s" %loaded_apps_details)
                                tdkTestObj.setResultStatus("FAILURE")
                        else:
                            print("Failed to retrieve loaded apps")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("Failed to launch LightningApp")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("Failed to install LightningApp")
                    tdkTestObj.setResultStatus("FAILURE")
                    status = "FAILURE"
            else:
                print("Failed to download LightningApp bundle")
                print("Download Details: %s" %download_details)
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"

    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")

