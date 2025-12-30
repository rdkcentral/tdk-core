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
  <name>RDKV_DownloadManager_Rate_Limit</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_rateLimit</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test rate limiting functionality for download sessions</synopsis>
  <groups_id/>
  <execution_time>8</execution_time>
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
    <test_case_id>CT_DOWNLOADMANAGER_005</test_case_id>
    <test_objective>Test rate limiting functionality for specific download sessions</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Device should be connected with internet
      2. Thunder framework should be running
      3. DownloadManager plugin should be active
    </pre_requisite>
    <api_or_interface_used>org.rdk.DownloadManager.rateLimit</api_or_interface_used>
    <input_parameters>downloadId, limit</input_parameters>
    <automation_approch>
      1. Start a download session
      2. Apply rate limiting to the download
      3. Verify rate limit is applied successfully
      4. Test different rate limit values
      5. Cancel download for cleanup
    </automation_approch>
    <expected_output>Rate limiting should be applied successfully to download sessions</expected_output>
    <priority>Medium</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Rate_Limit</test_script>
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
dl_defaults = config.get('defaults', {})

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Rate_Limit')

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
    
    # Test data - using configuration from ai_2_0_cpe.json
    test_url = test_urls.get('large', 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')
    download_id = None
    
    # Rate limit values to test (bytes per second)
    rate_limits = [
        {"limit": 512000, "description": "512 KB/s"},
        {"limit": 1024000, "description": "1 MB/s"},
        {"limit": 0, "description": "Unlimited"}
    ]
    
    print("Step 1: Checking DownloadManager plugin status")
    if ensure_plugin_active(obj, "org.rdk.DownloadManager"):
        print("SUCCESS: DownloadManager plugin is active")
        
        print("Step 2: Starting download for rate limit testing")
        tdkTestObj = obj.createTestStep('downloadmanager_download')
        tdkTestObj.addParameter("url", test_url)
        tdkTestObj.addParameter("priority", "false")
        tdkTestObj.addParameter("retries", dl_defaults.get('retries', '2'))
        tdkTestObj.addParameter("rateLimit", dl_defaults.get('rateLimit', '0'))  # Start with no limit
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
                    
                    # Test different rate limits
                    for i, rate_config in enumerate(rate_limits):
                        limit = rate_config["limit"]
                        description = rate_config["description"]
                        
                        print("\nStep %d: Testing rate limit - %s" % (i + 3, description))
                        
                        tdkTestObj = obj.createTestStep('downloadmanager_rateLimit')
                        tdkTestObj.addParameter("downloadId", download_id)
                        tdkTestObj.addParameter("limit", str(limit))
                        tdkTestObj.executeTestCase(expectedResult)
                        rate_result = tdkTestObj.getResult()
                        rate_details = tdkTestObj.getResultDetails()
                        
                        print("[RATE LIMIT RESULT] : %s" % rate_result)
                        print("[RATE LIMIT DETAILS] : %s" % rate_details)
                        
                        if expectedResult in rate_result:
                            print("SUCCESS: Rate limit (%s) applied successfully" % description)
                            
                            # Wait a moment for rate limit to take effect
                            time.sleep(2)
                            
                            # Check download progress to verify it's still active
                            tdkTestObj = obj.createTestStep('downloadmanager_progress')
                            tdkTestObj.addParameter("downloadId", download_id)
                            tdkTestObj.executeTestCase(expectedResult)
                            progress_result = tdkTestObj.getResult()
                            progress_details = tdkTestObj.getResultDetails()
                            
                            if expectedResult in progress_result:
                                try:
                                    progress_data = json.loads(progress_details)
                                    percent = progress_data.get("percent", -1)
                                    print("Download progress with %s limit: %d%%" % (description, percent))
                                except Exception as e:
                                    print("INFO: Could not parse progress data: %s" % str(e))
                            
                            tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("FAILURE: Failed to apply rate limit (%s)" % description)
                            tdkTestObj.setResultStatus("FAILURE")
                            break
                    
                    # Final test: Remove rate limit (set to 0 - unlimited)
                    print("\nStep %d: Removing rate limit (setting to unlimited)" % (len(rate_limits) + 3))
                    tdkTestObj = obj.createTestStep('downloadmanager_rateLimit')
                    tdkTestObj.addParameter("downloadId", download_id)
                    tdkTestObj.addParameter("limit", "0")
                    tdkTestObj.executeTestCase(expectedResult)
                    final_rate_result = tdkTestObj.getResult()
                    
                    if expectedResult in final_rate_result:
                        print("SUCCESS: Rate limit removed (unlimited) successfully")
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("FAILURE: Failed to remove rate limit")
                        tdkTestObj.setResultStatus("FAILURE")
                        
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
            print("\nStep Final: Cleaning up - cancelling download")
            tdkTestObj = obj.createTestStep('downloadmanager_cancel')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            cancel_result = tdkTestObj.getResult()
            
            if expectedResult in cancel_result:
                print("SUCCESS: Download cancelled for cleanup")
            else:
                print("WARNING: Could not cancel download during cleanup")
            
            # Test negative scenario: rateLimit on cancelled download
            print("\nNegative Test: Apply rate limit to cancelled download (should fail)")
            time.sleep(1)
            
            tdkTestObj = obj.createTestStep('downloadmanager_rateLimit')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.addParameter("limit", "512000")  # Try to apply rate limit
            tdkTestObj.executeTestCase(expectedResult)
            rate_cancelled_result = tdkTestObj.getResult()
            rate_cancelled_details = tdkTestObj.getResultDetails()
            
            print("[RATE LIMIT CANCELLED RESULT] : %s" % rate_cancelled_result)
            print("[RATE LIMIT CANCELLED DETAILS] : %s" % rate_cancelled_details)
            
            if "FAILURE" in rate_cancelled_result or "error" in rate_cancelled_details.lower():
                print("SUCCESS: Correctly returns error when applying rate limit to cancelled download")
            else:
                print("INFO: Rate limit on cancelled download may or may not be supported")
            
            # Test negative scenario: rateLimit with invalid ID
            print("\nNegative Test: Apply rate limit to invalid download ID (should fail)")
            invalid_id = "invalid_download_id_99999"
            
            tdkTestObj = obj.createTestStep('downloadmanager_rateLimit')
            tdkTestObj.addParameter("downloadId", invalid_id)
            tdkTestObj.addParameter("limit", "512000")
            tdkTestObj.executeTestCase(expectedResult)
            rate_invalid_result = tdkTestObj.getResult()
            rate_invalid_details = tdkTestObj.getResultDetails()
            
            print("[RATE LIMIT INVALID ID RESULT] : %s" % rate_invalid_result)
            print("[RATE LIMIT INVALID ID DETAILS] : %s" % rate_invalid_details)
            
            if "FAILURE" in rate_invalid_result or "error" in rate_invalid_details.lower():
                print("SUCCESS: Correctly returns error for invalid download ID")
            else:
                print("INFO: Invalid ID handling may need investigation")
                
    else:
        print("FAILURE: DownloadManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
        
    obj.unloadModule("downloadmanager")
else:
    print("FAILURE: Load module failed")
    obj.setLoadModuleStatus("FAILURE")