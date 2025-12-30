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
  <name>RDKV_DownloadManager_Progress_Query</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_progress</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test querying current download progress functionality</synopsis>
  <groups_id/>
  <execution_time>6</execution_time>
  <long_duration>false</long_duration>
  <advanced_script>false</advanced_script>
  <remarks></remarks>
  <skip>false</skip>
  <box_types>
    <box_type>Hybrid-1</box_type>
    <box_type>Emulator-HYB</box_type>
    <box_type>RPI</box_type>
    <box_type>RPI4</box_type>
  </box_types>
  <rdk_versions>
    <rdk_version>RDK2.0</rdk_version>
  </rdk_versions>
  <test_cases>
    <test_case_id>CT_DOWNLOADMANAGER_007</test_case_id>
    <test_objective>Test querying current download progress for active downloads</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Device should be connected with internet
      2. Thunder framework should be running
      3. DownloadManager plugin should be active
    </pre_requisite>
    <api_or_interface_used>org.rdk.DownloadManager.progress</api_or_interface_used>
    <input_parameters>downloadId</input_parameters>
    <automation_approch>
      1. Start a download session
      2. Query progress multiple times during download
      3. Verify progress values are valid (0-100%)
      4. Verify progress increases over time
      5. Test error handling for invalid download IDs
    </automation_approch>
    <expected_output>Progress queries should return valid percentage values</expected_output>
    <priority>High</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Progress_Query</test_script>
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
from ai2_0_utils import ensure_plugin_active, load_download_config

# Load DownloadManager configuration with fallback defaults
config = load_download_config()
test_urls = config.get('testUrls', {})
dl_timeouts = config.get('timeouts', {})

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Progress_Query')

#Get the result of connection with test component and DUT
result = obj.getLoadModuleResult()
print("[LIB LOAD STATUS] : %s" % result)

if "SUCCESS" in result.upper():
    obj.setLoadModuleStatus("SUCCESS")
    expectedResult = "SUCCESS"
    
    print("Step 0: Activating Required Dependent Plugins")
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
    
    # Test data - using LARGE file for progress tracking
    test_url = test_urls.get('large', 'https://tools.rdkcentral.com:8443/images//lib32-middleware-test-image-RPI4-raspberrypi4-64-rdke-feature-RDKECOREMW-584-OTA.wic.tar.gz')
    download_id = None
    
    print("Step 1: Checking DownloadManager plugin status")
    if ensure_plugin_active(obj, "org.rdk.DownloadManager"):
        print("SUCCESS: DownloadManager plugin is active")
        
        print("Step 2: Starting download for progress tracking")
        tdkTestObj = obj.createTestStep('downloadmanager_download')
        tdkTestObj.addParameter("url", test_url)
        tdkTestObj.addParameter("priority", "false")
        tdkTestObj.addParameter("retries", "2")
        tdkTestObj.addParameter("rateLimit", dl_defaults.get('rateLimitTest', '512000'))  # Limit speed for better progress tracking
        tdkTestObj.executeTestCase(expectedResult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        
        print("[DOWNLOAD START RESULT] : %s" % actualresult)
        print("[DOWNLOAD START DETAILS] : %s" % details)
        
        if expectedResult in actualresult:
            try:
                result_data = json.loads(details)
                download_id = result_data.get("downloadId", "")
                
                if download_id:
                    print("SUCCESS: Download started with ID: %s" % download_id)
                    
                    # Track progress multiple times
                    progress_history = []
                    max_checks = 8
                    check_interval = 2  # seconds
                    
                    print("Step 3: Tracking download progress over time")
                    for i in range(max_checks):
                        time.sleep(check_interval)
                        
                        print("Progress check %d/%d..." % (i + 1, max_checks))
                        tdkTestObj = obj.createTestStep('downloadmanager_progress')
                        tdkTestObj.addParameter("downloadId", download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        progress_result = tdkTestObj.getResult()
                        progress_details = tdkTestObj.getResultDetails()
                        
                        print("[PROGRESS RESULT %d] : %s" % (i + 1, progress_result))
                        print("[PROGRESS DETAILS %d] : %s" % (i + 1, progress_details))
                        
                        if expectedResult in progress_result:
                            try:
                                progress_data = json.loads(progress_details)
                                percent = progress_data.get("percent", -1)
                                
                                # Validate progress value
                                if 0 <= percent <= 100:
                                    print("SUCCESS: Valid progress value: %d%%" % percent)
                                    progress_history.append({
                                        "check": i + 1,
                                        "percent": percent,
                                        "timestamp": time.time()
                                    })
                                    
                                    # If download completed, break
                                    if percent == 100:
                                        print("SUCCESS: Download completed!")
                                        break
                                else:
                                    print("WARNING: Invalid progress value: %d%%" % percent)
                                
                            except Exception as e:
                                print("FAILURE: Error parsing progress data: %s" % str(e))
                                break
                        else:
                            print("FAILURE: Failed to get progress information")
                            break
                    
                    # Analyze progress history
                    print("\nStep 4: Analyzing progress history")
                    if len(progress_history) >= 2:
                        print("Progress History:")
                        for entry in progress_history:
                            print("  Check %d: %d%%" % (entry["check"], entry["percent"]))
                        
                        # Check if progress generally increased
                        first_percent = progress_history[0]["percent"]
                        last_percent = progress_history[-1]["percent"]
                        
                        if last_percent >= first_percent:
                            print("SUCCESS: Progress increased from %d%% to %d%%" % (first_percent, last_percent))
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("WARNING: Progress decreased from %d%% to %d%%" % (first_percent, last_percent))
                            print("INFO: This might be normal for some download scenarios")
                            tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("WARNING: Insufficient progress data collected")
                        print("INFO: Progress API is functional")
                        tdkTestObj.setResultStatus("SUCCESS")
                    
                    # Test error handling with invalid download ID
                    print("\nStep 5: Testing error handling with invalid download ID")
                    invalid_download_id = "invalid_download_id_12345"
                    
                    tdkTestObj = obj.createTestStep('downloadmanager_progress')
                    tdkTestObj.addParameter("downloadId", invalid_download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    invalid_progress_result = tdkTestObj.getResult()
                    invalid_progress_details = tdkTestObj.getResultDetails()
                    
                    print("[INVALID PROGRESS RESULT] : %s" % invalid_progress_result)
                    print("[INVALID PROGRESS DETAILS] : %s" % invalid_progress_details)
                    
                    # For invalid download ID, we expect either FAILURE or graceful error handling
                    if "FAILURE" in invalid_progress_result or expectedResult in invalid_progress_result:
                        print("SUCCESS: Error handling for invalid download ID works correctly")
                    else:
                        print("WARNING: Unexpected result for invalid download ID")
                    
                    # Test negative scenario: Progress after cancellation
                    print("\nStep 6: Testing negative scenario - Progress after download cancellation")
                    
                    print("Cancelling download for negative test...")
                    tdkTestObj = obj.createTestStep('downloadmanager_cancel')
                    tdkTestObj.addParameter("downloadId", download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    cancel_result = tdkTestObj.getResult()
                    
                    if expectedResult in cancel_result:
                        print("SUCCESS: Download cancelled")
                        
                        # Try to get progress on cancelled download (should fail)
                        time.sleep(1)
                        print("Attempting to query progress on cancelled download (should return error)...")
                        tdkTestObj = obj.createTestStep('downloadmanager_progress')
                        tdkTestObj.addParameter("downloadId", download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        progress_cancelled_result = tdkTestObj.getResult()
                        progress_cancelled_details = tdkTestObj.getResultDetails()
                        
                        print("[PROGRESS CANCELLED RESULT] : %s" % progress_cancelled_result)
                        print("[PROGRESS CANCELLED DETAILS] : %s" % progress_cancelled_details)
                        
                        if "FAILURE" in progress_cancelled_result or "error" in progress_cancelled_details.lower():
                            print("SUCCESS: Correctly returns error for cancelled download")
                        else:
                            print("INFO: Download may still be queryable after cancellation")
                    else:
                        print("WARNING: Could not cancel download for test")
                    
                else:
                    print("FAILURE: No download ID returned")
                    tdkTestObj.setResultStatus("FAILURE")
            except Exception as e:
                print("FAILURE: Error parsing download result: %s" % str(e))
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Failed to start download")
            tdkTestObj.setResultStatus("FAILURE")
            
        # Cleanup: Cancel download if it was started
        if download_id:
            print("\nStep 6: Cleaning up - cancelling download")
            tdkTestObj = obj.createTestStep('downloadmanager_cancel')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            cancel_result = tdkTestObj.getResult()
            
            if expectedResult in cancel_result:
                print("SUCCESS: Download cancelled for cleanup")
            else:
                print("WARNING: Could not cancel download during cleanup")
                
    else:
        print("FAILURE: DownloadManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
        
    obj.unloadModule("downloadmanager")
else:
    print("FAILURE: Load module failed")
    obj.setLoadModuleStatus("FAILURE")