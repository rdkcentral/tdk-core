## TestScript Name
RDKV_CERT_AVS_DownloadManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [DownloadManager_Download_ValidParameters](#downloadmanager_download_validparameters)
   - [DownloadManager_GetStorageDetails_Functionality](#downloadmanager_getstoragedetails_functionality)
   - [DownloadManager_Cancel_EmptyParameters](#downloadmanager_cancel_emptyparameters)
   - [DownloadManager_Delete_EmptyFileLocator](#downloadmanager_delete_emptyfilelocator)
   - [DownloadManager_Delete_InvalidFileLocator](#downloadmanager_delete_invalidfilelocator)
   - [DownloadManager_Delete_Package_TwoTimes](#downloadmanager_delete_package_twotimes)
   - [DownloadManager_Download_Pause_Resume_Delete_Package](#downloadmanager_download_pause_resume_delete_package)
   - [DownloadManager_Download_Pause_Cancel_Package](#downloadmanager_download_pause_cancel_package)
   - [DownloadManager_Download_Multiple_Pause_Resume_Operations](#downloadmanager_download_multiple_pause_resume_operations)
   - [DownloadManager_Download_Cancel_Package](#downloadmanager_download_cancel_package)
   - [DownloadManager_Download_Pause_Delete_Resume_Delete_Package](#downloadmanager_download_pause_delete_resume_delete_package)
   - [DownloadManager_Cancel_Package_Empty_Parameter](#downloadmanager_cancel_package_empty_parameter)
   - [DownloadManager_Cancel_Package_Invalid_Parameter](#downloadmanager_cancel_package_invalid_parameter)
   - [DownloadManager_Download_Empty_URL](#downloadmanager_download_empty_url)
   - [DownloadManager_Download_Invalid_URL](#downloadmanager_download_invalid_url)
   - [DownloadManager_Pause_Empty_Parameter](#downloadmanager_pause_empty_parameter)
   - [DownloadManager_Pause_Invalid_Parameter](#downloadmanager_pause_invalid_parameter)
   - [DownloadManager_Resume_Empty_Parameter](#downloadmanager_resume_empty_parameter)
   - [DownloadManager_Resume_Invalid_Parameter](#downloadmanager_resume_invalid_parameter)
   - [DownloadManager_Progress_Empty_Parameter](#downloadmanager_progress_empty_parameter)
   - [DownloadManager_Progress_Invalid_Parameter](#downloadmanager_progress_invalid_parameter)
   - [DownloadManager_Download_Optional_Parameters](#downloadmanager_download_optional_parameters)
   - [DownloadManager_Download_Ratelimit_Pause_Resume_Delete_Package](#downloadmanager_download_ratelimit_pause_resume_delete_package)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **DownloadManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DownloadManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DownloadManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Packagemanager Application Name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure Packagemanager Application Version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure Packagemanager Application Hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure Packagemanager Additionalmetadata Name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure Packagemanager Additionalmetadata Value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure Packagemanager Application MD5 Checksum Value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
| 7 | Configure Packagemanager Large Application Hosted URL | `PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL` must be set to the hosted URL of the large application or asset/package | The `PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 8 | Configure Packagemanager Large Application MD5 Checksum Value | `PACKAGEMANAGER_LARGE_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the large application or asset package for integrity verification | The `PACKAGEMANAGER_LARGE_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
| 9 | Configure Packagemanager Pause Resume Times | `PACKAGEMANAGER_PAUSE_RESUME_TIMES` must be set to the number of pause and resume cycles to perform during package download validation | The `PACKAGEMANAGER_PAUSE_RESUME_TIMES` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="downloadmanager_download_validparameters"></a>
### TestCase Name
DownloadManager_Download_ValidParameters

### TestCase ID
DM_01

### TestCase Objective
Verify that the download method works correctly with valid parameters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_getstoragedetails_functionality"></a>
### TestCase Name
DownloadManager_GetStorageDetails_Functionality

### TestCase ID
DM_02

### TestCase Objective
Verify that the getStorageDetails method functions correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorageDetails | Invoke getStorageDetails on org.rdk.DownloadManager with type: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>", id: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.getStorageDetails", "params": {"type": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>", "id": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that storage details are returned with valid non-empty values |
| 2 | Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Uninstalled Package | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the package is successfully uninstalled |

---

<a id="downloadmanager_cancel_emptyparameters"></a>
### TestCase Name
DownloadManager_Cancel_EmptyParameters

### TestCase ID
DM_03

### TestCase Objective
Verify that the cancel method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Cancel EmptyParameters | Invoke cancel on org.rdk.DownloadManager with downloadId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_emptyfilelocator"></a>
### TestCase Name
DownloadManager_Delete_EmptyFileLocator

### TestCase ID
DM_04

### TestCase Objective
Verify that the delete method handles empty fileLocator correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete EmptyFileLocator | Invoke delete on org.rdk.DownloadManager with fileLocator: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_invalidfilelocator"></a>
### TestCase Name
DownloadManager_Delete_InvalidFileLocator

### TestCase ID
DM_05

### TestCase Objective
Verify that the delete method handles invalid fileLocator correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete InvalidFileLocator | Invoke delete on org.rdk.DownloadManager with fileLocator: "invalid_file_locator"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "invalid_file_locator"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_package_twotimes"></a>
### TestCase Name
DownloadManager_Delete_Package_TwoTimes

### TestCase ID
DM_06

### TestCase Objective
Verify delete method with valid parameters and perform two consecutive delete operations

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | First Delete Package | *(Conditional statement executed only if package/app is currently present)*<br>Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Second Delete Package | *(Conditional statement executed only if package/app is currently present)*<br>Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_download_pause_resume_delete_package"></a>
### TestCase Name
DownloadManager_Download_Pause_Resume_Delete_Package

### TestCase ID
DM_07

### TestCase Objective
Verify download, pause, resume and delete package functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke pause on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the download remains paused with the expected progress value |
| 6 | Resume Download | Invoke resume on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 7 | Progress Check After Resume | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress increases after resume |
| 8 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_download_pause_cancel_package"></a>
### TestCase Name
DownloadManager_Download_Pause_Cancel_Package

### TestCase ID
DM_08

### TestCase Objective
Verify download, pause and cancel package functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke pause on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the download remains paused with the expected progress value |
| 6 | Cancel Download | Invoke cancel on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_download_multiple_pause_resume_operations"></a>
### TestCase Name
DownloadManager_Download_Multiple_Pause_Resume_Operations

### TestCase ID
DM_09

### TestCase Objective
Verify download with multiple pause and resume operations followed by delete

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 3 | Download Multiple Pause Resume Operations | Invoke resume on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the Pause and Resume calls succeed for each iteration, returning a null/empty response as expected  |
| 4 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_download_cancel_package"></a>
### TestCase Name
DownloadManager_Download_Cancel_Package

### TestCase ID
DM_10

### TestCase Objective
Verify download and cancel package functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 3 | Cancel Download | Invoke cancel on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_download_pause_delete_resume_delete_package"></a>
### TestCase Name
DownloadManager_Download_Pause_Delete_Resume_Delete_Package

### TestCase ID
DM_11

### TestCase Objective
Verify download, pause, delete, resume and delete package functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke pause on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the download remains paused with the expected progress value |
| 6 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |
| 7 | Resume Download | Invoke resume on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 8 | Progress Check After Resume | Invoke progress on org.rdk.DownloadManager with downloadId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress increases after resume |
| 9 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_cancel_package_empty_parameter"></a>
### TestCase Name
DownloadManager_Cancel_Package_Empty_Parameter

### TestCase ID
DM_12

### TestCase Objective
Check cancel package functionality with empty parameter

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Cancel Download Empty Parameter | Invoke cancel on org.rdk.DownloadManager with downloadId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_cancel_package_invalid_parameter"></a>
### TestCase Name
DownloadManager_Cancel_Package_Invalid_Parameter

### TestCase ID
DM_13

### TestCase Objective
Check cancel package functionality with invalid parameter

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Cancel Download Invalid Parameter | Invoke cancel on org.rdk.DownloadManager with downloadId: "invalid_handle"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "invalid_handle"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_download_empty_url"></a>
### TestCase Name
DownloadManager_Download_Empty_URL

### TestCase ID
DM_14

### TestCase Objective
Verify that the download method handles empty URL correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download Empty URL | Invoke download on org.rdk.DownloadManager with url: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_download_invalid_url"></a>
### TestCase Name
DownloadManager_Download_Invalid_URL

### TestCase ID
DM_15

### TestCase Objective
Verify that the download method handles invalid URL correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download Invalid URL | Invoke download on org.rdk.DownloadManager with url: "http://invalid.com/"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "http://invalid.com/"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_pause_empty_parameter"></a>
### TestCase Name
DownloadManager_Pause_Empty_Parameter

### TestCase ID
DM_16

### TestCase Objective
Verify that the pause method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Pause Download Empty Parameter | Invoke pause on org.rdk.DownloadManager with downloadId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_pause_invalid_parameter"></a>
### TestCase Name
DownloadManager_Pause_Invalid_Parameter

### TestCase ID
DM_17

### TestCase Objective
Verify that the pause method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Pause Download Invalid Parameter | Invoke pause on org.rdk.DownloadManager with downloadId: "invalid_download_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_resume_empty_parameter"></a>
### TestCase Name
DownloadManager_Resume_Empty_Parameter

### TestCase ID
DM_18

### TestCase Objective
Verify that the resume method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Resume Download Empty Parameter | Invoke resume on org.rdk.DownloadManager with downloadId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_resume_invalid_parameter"></a>
### TestCase Name
DownloadManager_Resume_Invalid_Parameter

### TestCase ID
DM_19

### TestCase Objective
Verify that the resume method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Resume Download Invalid Parameter | Invoke resume on org.rdk.DownloadManager with downloadId: "invalid_download_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_progress_empty_parameter"></a>
### TestCase Name
DownloadManager_Progress_Empty_Parameter

### TestCase ID
DM_20

### TestCase Objective
Verify that the progress method handles empty parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Progress Download Empty Parameter | Invoke progress on org.rdk.DownloadManager with downloadId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_progress_invalid_parameter"></a>
### TestCase Name
DownloadManager_Progress_Invalid_Parameter

### TestCase ID
DM_21

### TestCase Objective
Verify that the progress method handles invalid parameters correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Progress Download Invalid Parameter | Invoke progress on org.rdk.DownloadManager with downloadId: "invalid_download_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="downloadmanager_download_optional_parameters"></a>
### TestCase Name
DownloadManager_Download_Optional_Parameters

### TestCase ID
DM_22

### TestCase Objective
Verify that the download method works correctly with optional parameters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>", priority: "true", retries: "0", rateLimit: "0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>", "priority": true, "retries": 0, "rateLimit": 0}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Form Package FileLocator URL | Downloadmanager form filelocator url on the device | Verify that the file locator URL is formed successfully |
| 3 | Check Package Status Before Install | Check downloaded package status on the device | Downloaded package checksum matches expected value: `<PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE>` |
| 4 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<DOWNLOADED_FILE_LOCATOR_URL>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="downloadmanager_download_ratelimit_pause_resume_delete_package"></a>
### TestCase Name
DownloadManager_Download_Ratelimit_Pause_Resume_Delete_Package

### TestCase ID
DM_23

### TestCase Objective
Verify download, ratelimit, pause, resume and delete package functionality

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Form Package FileLocator URL | Downloadmanager form filelocator url on the device | Verify that the file locator URL is formed successfully |
| 3 | Progress Check During Download | Invoke progress on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 4 | Apply Rate Limit | Invoke rateLimit on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>", rateLimit: "0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.rateLimit", "params": {"downloadId": "<DOWNLOAD_ID>", "rateLimit": 0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Pause Download | Invoke pause on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Check Download Paused Status | Invoke progress on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress is reported successfully (0-100%) |
| 7 | Confirm Download Remains Paused | Invoke progress on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`; download progress matches value from step 6  |
| 8 | Resume Download | Invoke resume on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 9 | Progress Check After Resume | Invoke progress on org.rdk.DownloadManager with downloadId: "<DOWNLOAD_ID>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<DOWNLOAD_ID>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that download progress increases after resume |
| 10 | Check Package Download Completion | Check downloaded package status on the device | Downloaded package checksum matches expected value: `<PACKAGEMANAGER_LARGE_APPLICATION_MD5SUM_VALUE>` |
| 11 | Delete Package | Invoke delete on org.rdk.DownloadManager with fileLocator: "<DOWNLOADED_FILE_LOCATOR_URL>" (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<DOWNLOADED_FILE_LOCATOR_URL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Plugin Post-conditions

_No plugin-level post-conditions defined_

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 30 mins

**Priority** : Medium

**Release Version** : M147

<div align="right"><a href="#testscript-name">Go to Top</a></div>
