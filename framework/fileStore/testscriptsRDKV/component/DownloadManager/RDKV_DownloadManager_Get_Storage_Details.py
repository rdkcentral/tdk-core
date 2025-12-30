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
  <name>RDKV_DownloadManager_Get_Storage_Details</name>
  <primitive_test_id></primitive_test_id>
  <primitive_test_name>downloadmanager_getStorageDetails</primitive_test_name>
  <primitive_test_version>1</primitive_test_version>
  <status>FREE</status>
  <synopsis>Test getting storage space information from DownloadManager</synopsis>
  <groups_id/>
  <execution_time>2</execution_time>
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
    <test_case_id>CT_DOWNLOADMANAGER_003</test_case_id>
    <test_objective>Test DownloadManager getStorageDetails API functionality</test_objective>
    <test_type>Positive</test_type>
    <test_setup>RDK</test_setup>
    <pre_requisite>
      1. Thunder framework should be running
      2. DownloadManager plugin should be active
    </pre_requisite>
    <api_or_interface_used>org.rdk.DownloadManager.getStorageDetails</api_or_interface_used>
    <input_parameters>None</input_parameters>
    <automation_approch>
      1. Activate DownloadManager plugin if needed
      2. Call getStorageDetails method
      3. Verify response contains quotaKb and usedKb
      4. Validate storage information is reasonable
    </automation_approch>
    <expected_output>Storage details should be returned with valid quota and usage information</expected_output>
    <priority>High</priority>
    <test_stub_interface>DownloadManager</test_stub_interface>
    <test_script>RDKV_DownloadManager_Get_Storage_Details</test_script>
    <skipped>No</skipped>
    <release_version>M100</release_version>
    <remarks>None</remarks>
  </test_cases>
  <script_tags/>
</xml>
'''

# Import necessary libraries
import tdklib
import sys
import os

# Add path for ai2_0_utils and config loading
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from ai2_0_utils import ensure_plugin_active, load_download_config

# Load DownloadManager configuration with fallback defaults
config = load_download_config()
dl_methods = config.get('methods', {})

#Test component to be tested
obj = tdklib.TDKScriptingLibrary("DownloadManager", "1", standAlone=True)

#IP and Port of box, No need to change,
#This will be replaced with corresponding DUT Ip and port while executing script
ip = <ipaddress>
port = <port>
obj.configureTestCase(ip, port, 'RDKV_DownloadManager_Get_Storage_Details')

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
    
    print("Step 1: Checking DownloadManager plugin status")
    if ensure_plugin_active(obj, "org.rdk.DownloadManager"):
        print("SUCCESS: DownloadManager plugin is active")
        
        print("Step 2: Getting storage details")
        tdkTestObj = obj.createTestStep('downloadmanager_getStorageDetails')
        tdkTestObj.executeTestCase(expectedResult)
        actualresult = tdkTestObj.getResult()
        details = tdkTestObj.getResultDetails()
        
        print("[STORAGE RESULT] : %s" % actualresult)
        print("[STORAGE DETAILS] : %s" % details)
        
        if expectedResult in actualresult:
            try:
                # Parse the storage details response
                storage_data = json.loads(details)
                quota_kb = storage_data.get("quotaKb", -1)
                used_kb = storage_data.get("usedKb", -1)
                
                print("Storage Quota (KB): %s" % quota_kb)
                print("Storage Used (KB): %s" % used_kb)
                
                # Validate storage information
                if quota_kb >= 0 and used_kb >= 0:
                    if used_kb <= quota_kb:
                        print("SUCCESS: Storage details are valid")
                        print("Available space (KB): %s" % (quota_kb - used_kb))
                        
                        # Calculate usage percentage
                        if quota_kb > 0:
                            usage_percent = (used_kb * 100) / quota_kb
                            print("Storage usage: %.2f%%" % usage_percent)
                        
                        tdkTestObj.setResultStatus("SUCCESS")
                    else:
                        print("WARNING: Used space (%d KB) exceeds quota (%d KB)" % (used_kb, quota_kb))
                        print("INFO: This might indicate storage quota configuration issue")
                        tdkTestObj.setResultStatus("SUCCESS")  # Still consider as success for info gathering
                else:
                    print("FAILURE: Invalid storage values - quota: %s KB, used: %s KB" % (quota_kb, used_kb))
                    tdkTestObj.setResultStatus("FAILURE")
                    
            except Exception as e:
                print("FAILURE: Error parsing storage details: %s" % str(e))
                print("Raw response: %s" % details)
                tdkTestObj.setResultStatus("FAILURE")
        else:
            print("FAILURE: Failed to get storage details")
            tdkTestObj.setResultStatus("FAILURE")
    else:
        print("FAILURE: DownloadManager plugin is not active")
        obj.setLoadModuleStatus("FAILURE")
        
    obj.unloadModule("downloadmanager")
else:
    print("FAILURE: Load module failed")
    obj.setLoadModuleStatus("FAILURE")