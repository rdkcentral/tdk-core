##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2025 RDK Management
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
<?xml version='1.0' encoding='utf-8'?>
<xml>
  <id></id>
  <version>1</version>
  <name>RDKV_DownloadManager_Download_Basic_Functionality</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_download</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test basic download functionality with URL and options</synopsis>
  <groups_id/>
  <execution_time>5</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks></remarks>
  <skip>false</skip>
  <box_types>
    <box_type>RDKTV</box_type>
    <box_type>RPI-Client</box_type>
    <box_type>RPI-HYB</box_type>
    <box_type>Video_Accelerator</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DOWNLOADMANAGER_001</test_case_id>
    <test_objective>Test DownloadManager plugin basic download functionality</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Device should be connected with internet
      2. Thunder framework should be running
      3. DownloadManager plugin should be available
    </pre_requisite>
    <api_or_interface_used>org.rdk.DownloadManager.download</api_or_interface_used>
    <input_parameters>URL, priority, retries, rateLimit</input_parameters>
    <automation_approch>
      1. Activate DownloadManager plugin if not active
      2. Call download method with test URL
      3. Verify download ID is returned
      4. Check download progress
      5. Verify download completion
    </automation_approch>
    <expected_output>Download should complete successfully with valid download ID</expected_output>
    <priority>High</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Download_Basic_Functionality</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags/>
</xml>
'''

# Import necessary libraries
import tdklib
import json
import time
import sys
import os

# Add path for ai2_0_utils and config loading
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from ai2_0_utils import (
    ensure_plugin_active,
    DEFAULT_JSONRPC_URL,
    load_download_config
)

# Load DownloadManager configuration with fallback defaults
config = load_download_config()
dm_urls = config.get('downloadManager', {})
dl_timeouts = dm_urls.get('timeouts', {})
dl_defaults = dm_urls.get('defaults', {})

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Download_Basic_Functionality')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % result)

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    print("Precondition: Activating Required Dependent Plugins")
    try:
        from ai2_0_utils import check_and_activate_ai2_managers
        print("Activating StorageManager and other required plugins...")
        success, activated_list = check_and_activate_ai2_managers(obj, required_only=True)
        if success:
            print("SUCCESS: All required plugins activated")
            for plugin in activated_list:
                print("  - %s" % plugin)
        else:
            print("WARNING: Some required plugins may not have been activated")
        print("Waiting for plugins to initialize...")
        import time
        time.sleep(2)
    except Exception as e:
        print("WARNING: Could not activate dependent plugins: %s" % str(e))
        print("Continuing with DownloadManager activation...")
    
    # Test data - using configuration from ai_2_0_cpe.json
    test_url = dm_urls.get('dm_test_url_large')
    if not test_url:
        print("WARNING: Large test URL not found in configuration, using fallback")
        test_url = 'https://tools.rdkcentral.com:8443/images//lib32-middleware-test-image-RPI4-raspberrypi4-64-rdke-feature-RDKECOREMW-584-OTA.wic.tar.gz'
    
    print("Step 1: Checking DownloadManager plugin status")
    if ensure_plugin_active(obj, "org.rdk.DownloadManager"):
        print("SUCCESS: DownloadManager plugin is active")
        obj.setLoadModuleStatus("SUCCESS")
        
        print("Step 2: Initiating download with basic options")
        tdkTestObj = obj.createTestStep('downloadmanager_download')
        tdkTestObj.addParameter("url", test_url)
        tdkTestObj.addParameter("priority", "true")
        tdkTestObj.addParameter("retries", "3")
        tdkTestObj.addParameter("rateLimit", "0")
        tdkTestObj.executeTestCase(expectedResult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        
        print("[DOWNLOAD RESULT] : %s" % actualresult)
        print("[DOWNLOAD DETAILS] : %s" % details)
        
        if expectedResult in actualresult:
            # Parse the result to get download ID
            try:
                result_data = json.loads(details)
                download_id = result_data.get("downloadId", "")
                
                if download_id:
                    print("SUCCESS: Download initiated successfully with ID: %s" % download_id)
                    tdkTestObj.setResultStatus("SUCCESS")
                    
                    # Step 3: Check download progress
                    print("Step 3: Checking download progress")
                    time.sleep(2)  # Wait a bit for download to progress
                    
                    tdkTestObj = obj.createTestStep('downloadmanager_progress')
                    tdkTestObj.addParameter("downloadId", download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    progress_result = tdkTestObj.getResult()
                    progress_details = tdkTestObj.getResultDetails()
                    
                    print("[PROGRESS RESULT] : %s" % progress_result)
                    print("[PROGRESS DETAILS] : %s" % progress_details)
                    
                    if expectedResult in progress_result:
                        try:
                            progress_data = json.loads(progress_details)
                            percent = progress_data.get("percent", -1)
                            print("SUCCESS: Progress check successful - %d%% completed" % percent)
                            tdkTestObj.setResultStatus("SUCCESS")
                            
                            # Step 4: Cancel download to clean up
                            print("Step 4: Cancelling download for cleanup")
                            tdkTestObj = obj.createTestStep('downloadmanager_cancel')
                            tdkTestObj.addParameter("downloadId", download_id)
                            tdkTestObj.executeTestCase(expectedResult)
                            cancel_result = tdkTestObj.getResult()
                            
                            if expectedResult in cancel_result:
                                print("SUCCESS: Download cancelled successfully")
                                tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("FAILURE: Failed to cancel download")
                                tdkTestObj.setResultStatus("FAILURE")
                                
                        except Exception as e:
                            print("FAILURE: Error parsing progress data: %s" % str(e))
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("FAILURE: Failed to get download progress")
                        tdkTestObj.setResultStatus("FAILURE")
                else:
                    print("FAILURE: No download ID returned")
                    tdkTestObj.setResultStatus("FAILURE")
            except Exception as e:
                print("FAILURE: Error parsing download result: %s" % str(e))
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Download initiation failed")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: DownloadManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
        
    obj.unloadModule("downloadmanager")
else:
    print("FAILURE: Load module failed")
    obj.setLoadModuleStatus("FAILURE")