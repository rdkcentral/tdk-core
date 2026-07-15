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

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("rdkv_basic_sanity","1",standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_LightningApp_Launch_Check')

#Execution summary variable
Summ_list=[]

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
    
    # Step 0: Check if LightningApp is already installed
    print("\n[STEP 0] Checking if LightningApp is already installed")
    tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
    tdkTestObj.executeTestCase(expectedResult)
    check_result = tdkTestObj.getResult()
    check_details = tdkTestObj.getResultDetails()
    
    app_already_installed = False
    if check_result == "SUCCESS" and lightning_app_id in check_details:
        print("LightningApp is already installed")
        Summ_list.append('LightningApp Check : Already Installed')
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = True
    else:
        print("LightningApp is not installed, proceeding with download and install")
        Summ_list.append('LightningApp Check : Not Installed')
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = False
    
    if not app_already_installed:
        # Step 1: Download LightningApp bundle
        print("\n[STEP 1] Downloading LightningApp bundle")
        tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
        tdkTestObj.addParameter("download_url", lightning_app_download_url)
        tdkTestObj.executeTestCase(expectedResult)
        download_result = tdkTestObj.getResult()
        download_details = tdkTestObj.getResultDetails()
        
        if download_result == "SUCCESS":
            print("LightningApp bundle downloaded successfully")
            print("Download Details: %s" %download_details)
            Summ_list.append('LightningApp Download : SUCCESS')
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(3)
            
            # Step 2: Install LightningApp
            print("\n[STEP 2] Installing LightningApp")
            tdkTestObj = obj.createTestStep('rdkservice_install_app')
            tdkTestObj.addParameter("app_id", lightning_app_id)
            tdkTestObj.addParameter("fileLocator", download_details)
            tdkTestObj.executeTestCase(expectedResult)
            install_result = tdkTestObj.getResult()
            
            if install_result == "SUCCESS":
                print("LightningApp installed successfully")
                Summ_list.append('LightningApp Install : SUCCESS')
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)
            else:
                print("Failed to install LightningApp")
                Summ_list.append('LightningApp Install : FAILURE')
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print("Failed to download LightningApp bundle")
            print("Download Details: %s" %download_details)
            Summ_list.append('LightningApp Download : FAILURE')
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    else:
        print("Skipping download and install steps as app is already installed")
    
    if status == "SUCCESS":
        # Step 3: Launch LightningApp
        print("\n[STEP 3] Launching LightningApp")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", lightning_app_id)
        tdkTestObj.executeTestCase(expectedResult)
        launch_result = tdkTestObj.getResult()
        
        if launch_result == "SUCCESS":
            print("LightningApp launched successfully")
            Summ_list.append('LightningApp Launch : SUCCESS')
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(5)
            
            # Step 4: Terminate LightningApp
            print("\n[STEP 4] Terminating LightningApp")
            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", lightning_app_id)
            tdkTestObj.executeTestCase(expectedResult)
            terminate_result = tdkTestObj.getResult()
            
            if terminate_result == "SUCCESS":
                print("LightningApp terminated successfully")
                Summ_list.append('LightningApp Termination : SUCCESS')
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Failed to terminate LightningApp")
                Summ_list.append('LightningApp Termination : FAILURE')
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to launch LightningApp")
            Summ_list.append('LightningApp Launch : FAILURE')
            tdkTestObj.setResultStatus("FAILURE")
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
