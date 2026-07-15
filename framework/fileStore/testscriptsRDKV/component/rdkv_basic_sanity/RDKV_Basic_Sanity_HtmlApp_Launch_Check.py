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
obj.configureTestCase(ip,port,'RDKV_Basic_Sanity_HtmlApp_Launch_Check')

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
    
    # HtmlApp details from MediaValidationVariables
    html_app_id = MediaValidationVariables.html_player_app_id
    html_app_download_url = MediaValidationVariables.html_player_app_download_url
    
    print("\nHtmlApp Configuration:")
    print("  App ID: %s" %html_app_id)
    print("  Download URL: %s" %html_app_download_url)
    
    # Step 0: Check if HtmlApp is already installed
    print("\n[STEP 0] Checking if HtmlApp is already installed")
    tdkTestObj = obj.createTestStep('rdkv_getInstalledPackages')
    tdkTestObj.executeTestCase(expectedResult)
    check_result = tdkTestObj.getResult()
    check_details = tdkTestObj.getResultDetails()
    
    app_already_installed = False
    if check_result == "SUCCESS" and html_app_id in check_details:
        print("HtmlApp is already installed")
        Summ_list.append('HtmlApp Check : Already Installed')
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = True
    else:
        print("HtmlApp is not installed, proceeding with download and install")
        Summ_list.append('HtmlApp Check : Not Installed')
        tdkTestObj.setResultStatus("SUCCESS")
        app_already_installed = False
    
    if not app_already_installed:
        # Step 1: Download HtmlApp bundle
        print("\n[STEP 1] Downloading HtmlApp bundle")
        tdkTestObj = obj.createTestStep('rdkservice_download_app_bundle')
        tdkTestObj.addParameter("download_url", html_app_download_url)
        tdkTestObj.executeTestCase(expectedResult)
        download_result = tdkTestObj.getResult()
        download_details = tdkTestObj.getResultDetails()
        
        if download_result == "SUCCESS":
            print("HtmlApp bundle downloaded successfully")
            print("Download Details: %s" %download_details)
            Summ_list.append('HtmlApp Download : SUCCESS')
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(3)
            
            # Step 2: Install HtmlApp
            print("\n[STEP 2] Installing HtmlApp")
            tdkTestObj = obj.createTestStep('rdkservice_install_app')
            tdkTestObj.addParameter("app_id", html_app_id)
            tdkTestObj.addParameter("fileLocator", download_details)
            tdkTestObj.executeTestCase(expectedResult)
            install_result = tdkTestObj.getResult()
            
            if install_result == "SUCCESS":
                print("HtmlApp installed successfully")
                Summ_list.append('HtmlApp Install : SUCCESS')
                tdkTestObj.setResultStatus("SUCCESS")
                time.sleep(3)
            else:
                print("Failed to install HtmlApp")
                Summ_list.append('HtmlApp Install : FAILURE')
                tdkTestObj.setResultStatus("FAILURE")
                status = "FAILURE"
        else:
            print("Failed to download HtmlApp bundle")
            print("Download Details: %s" %download_details)
            Summ_list.append('HtmlApp Download : FAILURE')
            tdkTestObj.setResultStatus("FAILURE")
            status = "FAILURE"
    else:
        print("Skipping download and install steps as app is already installed")
    
    if status == "SUCCESS":
        # Step 3: Launch HtmlApp
        print("\n[STEP 3] Launching HtmlApp")
        tdkTestObj = obj.createTestStep('rdkservice_launch_app')
        tdkTestObj.addParameter("app_name", html_app_id)
        tdkTestObj.executeTestCase(expectedResult)
        launch_result = tdkTestObj.getResult()
        
        if launch_result == "SUCCESS":
            print("HtmlApp launched successfully")
            Summ_list.append('HtmlApp Launch : SUCCESS')
            tdkTestObj.setResultStatus("SUCCESS")
            time.sleep(5)
            
            # Step 4: Terminate HtmlApp
            print("\n[STEP 4] Terminating HtmlApp")
            tdkTestObj = obj.createTestStep('rdkv_terminate_app')
            tdkTestObj.addParameter("app_id", html_app_id)
            tdkTestObj.executeTestCase(expectedResult)
            terminate_result = tdkTestObj.getResult()
            
            if terminate_result == "SUCCESS":
                print("HtmlApp terminated successfully")
                Summ_list.append('HtmlApp Termination : SUCCESS')
                tdkTestObj.setResultStatus("SUCCESS")
            else:
                print("Failed to terminate HtmlApp")
                Summ_list.append('HtmlApp Termination : FAILURE')
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("Failed to launch HtmlApp")
            Summ_list.append('HtmlApp Launch : FAILURE')
            tdkTestObj.setResultStatus("FAILURE")
    
    obj.unloadModule("rdkv_basic_sanity")
else:
    obj.setLoadModuleStatus("FAILURE")
    print("Failed to load module")
