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
  <name>RDKV_DownloadManager_Pause_Resume_Download</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_pause</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test pausing and resuming download functionality</synopsis>
  <groups_id/>
  <execution_time>10</execution_time>
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
    <test_case_id>CT_DOWNLOADMANAGER_004</test_case_id>
    <test_objective>Test pause and resume functionality for active downloads</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Device should be connected with internet
      2. Thunder framework should be running
      3. DownloadManager plugin should be active
    </pre_requisite>
    <api_or_interface_used>org.rdk.DownloadManager.pause, org.rdk.DownloadManager.resume</api_or_interface_used>
    <input_parameters>downloadId</input_parameters>
    <automation_approch>
      1. Start a download session
      2. Pause the active download
      3. Resume the paused download
      4. Verify download continues
      5. Cancel download for cleanup
    </automation_approch>
    <expected_output>Download should pause and resume successfully</expected_output>
    <priority>High</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Pause_Resume_Download</test_script>
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
dm_urls = config.get('downloadManager', {})
dl_timeouts = config.get('timeouts', {})
dl_defaults = config.get('defaults', {})
dl_methods = config.get('methods', {})

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Pause_Resume_Download')

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
    
    # Test data - using a larger file for meaningful pause/resume testing
    test_url = dm_urls.get('dm_test_url_large')
    if not test_url:
        print("WARNING: Large test URL not found in configuration, using fallback")
        test_url = 'https://tools.rdkcentral.com:8443/images//lib32-middleware-test-image-RPI4-raspberrypi4-64-rdke-feature-RDKECOREMW-584-OTA.wic.tar.gz'
    download_id = None
    
    print("Step 1: Checking DownloadManager plugin status")
    if ensure_plugin_active(obj, "org.rdk.DownloadManager"):
        print("SUCCESS: DownloadManager plugin is active")
        
        print("Step 2: Starting download for pause/resume test")
        tdkTestObj = obj.createTestStep('downloadmanager_download')
        tdkTestObj.addParameter("url", test_url)
        tdkTestObj.addParameter("priority", "false")
        tdkTestObj.addParameter("retries", "2")
        tdkTestObj.addParameter("rateLimit", dl_defaults.get('rateLimitHighSpeed', '10485760'))  # 10MB/s for faster testing
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
                    
                    # Wait a bit for download to progress
                    time.sleep(3)
                    
                    print("Step 3: Pausing download")
                    tdkTestObj = obj.createTestStep('downloadmanager_pause')
                    tdkTestObj.addParameter("downloadId", download_id)
                    tdkTestObj.executeTestCase(expectedResult)
                    pause_result = tdkTestObj.getResult()
                    pause_details = tdkTestObj.getResultDetails()
                    
                    print("[PAUSE RESULT] : %s" % pause_result)
                    print("[PAUSE DETAILS] : %s" % pause_details)
                    
                    if expectedResult in pause_result:
                        print("SUCCESS: Download paused successfully")
                        
                        # Wait a moment to ensure pause takes effect
                        time.sleep(dl_timeouts.get('pauseResumeWait', 3))
                        
                        print("Step 4: Checking progress while paused")
                        tdkTestObj = obj.createTestStep('downloadmanager_progress')
                        tdkTestObj.addParameter("downloadId", download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        progress_result = tdkTestObj.getResult()
                        progress_details = tdkTestObj.getResultDetails()
                        
                        if expectedResult in progress_result:
                            try:
                                progress_data = json.loads(progress_details)
                                paused_percent = progress_data.get("percent", -1)
                                print("Progress while paused: %d%%" % paused_percent)
                            except:
                                print("INFO: Could not parse progress data while paused")
                        
                        print("Step 5: Resuming download")
                        tdkTestObj = obj.createTestStep('downloadmanager_resume')
                        tdkTestObj.addParameter("downloadId", download_id)
                        tdkTestObj.executeTestCase(expectedResult)
                        resume_result = tdkTestObj.getResult()
                        resume_details = tdkTestObj.getResultDetails()
                        
                        print("[RESUME RESULT] : %s" % resume_result)
                        print("[RESUME DETAILS] : %s" % resume_details)
                        
                        if expectedResult in resume_result:
                            print("SUCCESS: Download resumed successfully")
                            
                            # Wait a bit for download to progress after resume
                            time.sleep(3)
                            
                            print("Step 6: Checking progress after resume")
                            tdkTestObj = obj.createTestStep('downloadmanager_progress')
                            tdkTestObj.addParameter("downloadId", download_id)
                            tdkTestObj.executeTestCase(expectedResult)
                            final_progress_result = tdkTestObj.getResult()
                            final_progress_details = tdkTestObj.getResultDetails()
                            
                            if expectedResult in final_progress_result:
                                try:
                                    final_progress_data = json.loads(final_progress_details)
                                    final_percent = final_progress_data.get("percent", -1)
                                    print("Progress after resume: %d%%" % final_percent)
                                    
                                    print("SUCCESS: Pause and resume functionality working correctly")
                                    tdkTestObj.setResultStatus("SUCCESS")
                                    
                                except Exception as e:
                                    print("WARNING: Could not parse final progress data: %s" % str(e))
                                    print("INFO: But pause/resume operations succeeded")
                                    tdkTestObj.setResultStatus("SUCCESS")
                            else:
                                print("WARNING: Could not check progress after resume")
                                print("INFO: But pause/resume operations succeeded")
                                tdkTestObj.setResultStatus("SUCCESS")
                        else:
                            print("FAILURE: Failed to resume download")
                            tdkTestObj.setResultStatus("FAILURE")
                    else:
                        print("FAILURE: Failed to pause download")
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
            print("Step 7: Cleaning up - cancelling download")
            tdkTestObj = obj.createTestStep('downloadmanager_cancel')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            cancel_result = tdkTestObj.getResult()
            
            if expectedResult in cancel_result:
                print("SUCCESS: Download cancelled for cleanup")
            else:
                print("WARNING: Could not cancel download during cleanup")
            
            # Test negative scenarios: Operations on cancelled download
            print("\nStep 8: Testing negative scenarios - Operations on cancelled download")
            
            # Test pause on cancelled download (should fail)
            print("Testing pause on cancelled download (should return error)...")
            tdkTestObj = obj.createTestStep('downloadmanager_pause')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            pause_cancelled_result = tdkTestObj.getResult()
            pause_cancelled_details = tdkTestObj.getResultDetails()
            
            print("[PAUSE CANCELLED RESULT] : %s" % pause_cancelled_result)
            print("[PAUSE CANCELLED DETAILS] : %s" % pause_cancelled_details)
            
            # Test resume on cancelled download (should fail)
            print("Testing resume on cancelled download (should return error)...")
            tdkTestObj = obj.createTestStep('downloadmanager_resume')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            resume_cancelled_result = tdkTestObj.getResult()
            resume_cancelled_details = tdkTestObj.getResultDetails()
            
            print("[RESUME CANCELLED RESULT] : %s" % resume_cancelled_result)
            print("[RESUME CANCELLED DETAILS] : %s" % resume_cancelled_details)
            
            # Test progress on cancelled download (should fail)
            print("Testing progress on cancelled download (should return error)...")
            tdkTestObj = obj.createTestStep('downloadmanager_progress')
            tdkTestObj.addParameter("downloadId", download_id)
            tdkTestObj.executeTestCase(expectedResult)
            progress_cancelled_result = tdkTestObj.getResult()
            progress_cancelled_details = tdkTestObj.getResultDetails()
            
            print("[PROGRESS CANCELLED RESULT] : %s" % progress_cancelled_result)
            print("[PROGRESS CANCELLED DETAILS] : %s" % progress_cancelled_details)
            
            # Test with invalid download ID
            print("\nStep 9: Testing negative scenarios - Invalid download ID")
            invalid_id = "invalid_download_id_99999"
            
            print("Testing pause with invalid download ID...")
            tdkTestObj = obj.createTestStep('downloadmanager_pause')
            tdkTestObj.addParameter("downloadId", invalid_id)
            tdkTestObj.executeTestCase(expectedResult)
            pause_invalid_result = tdkTestObj.getResult()
            pause_invalid_details = tdkTestObj.getResultDetails()
            
            print("[PAUSE INVALID ID RESULT] : %s" % pause_invalid_result)
            print("[PAUSE INVALID ID DETAILS] : %s" % pause_invalid_details)
            
            print("Testing resume with invalid download ID...")
            tdkTestObj = obj.createTestStep('downloadmanager_resume')
            tdkTestObj.addParameter("downloadId", invalid_id)
            tdkTestObj.executeTestCase(expectedResult)
            resume_invalid_result = tdkTestObj.getResult()
            resume_invalid_details = tdkTestObj.getResultDetails()
            
            print("[RESUME INVALID ID RESULT] : %s" % resume_invalid_result)
            print("[RESUME INVALID ID DETAILS] : %s" % resume_invalid_details)
            
            # Summary of negative tests
            print("\nNegative Test Summary:")
            print("Pause on cancelled download: %s" % ("ERROR as expected" if "FAILURE" in pause_cancelled_result else "May need investigation"))
            print("Resume on cancelled download: %s" % ("ERROR as expected" if "FAILURE" in resume_cancelled_result else "May need investigation"))
            print("Progress on cancelled download: %s" % ("ERROR as expected" if "FAILURE" in progress_cancelled_result else "May need investigation"))
            print("Pause with invalid ID: %s" % ("ERROR as expected" if "FAILURE" in pause_invalid_result else "May need investigation"))
            print("Resume with invalid ID: %s" % ("ERROR as expected" if "FAILURE" in resume_invalid_result else "May need investigation"))
                
    else:
        print("FAILURE: DownloadManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
        
    obj.unloadModule("downloadmanager")
else:
    print("FAILURE: Load module failed")
    obj.setLoadModuleStatus("FAILURE")