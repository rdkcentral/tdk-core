## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [DownloadManager_Download_ValidParameters (DM_01)](#downloadmanager_download_validparameters-dm_01)
   - [DownloadManager_GetStorageDetails_Functionality (DM_02)](#downloadmanager_getstoragedetails_functionality-dm_02)
   - [DownloadManager_Cancel_EmptyParameters (DM_03)](#downloadmanager_cancel_emptyparameters-dm_03)
   - [DownloadManager_Delete_EmptyFileLocator (DM_04)](#downloadmanager_delete_emptyfilelocator-dm_04)
   - [DownloadManager_Delete_InvalidFileLocator (DM_05)](#downloadmanager_delete_invalidfilelocator-dm_05)
   - [DownloadManager_Delete_Package_TwoTimes (DM_06)](#downloadmanager_delete_package_twotimes-dm_06)
   - [DownloadManager_Download_Pause_Resume_Delete_Package (DM_07)](#downloadmanager_download_pause_resume_delete_package-dm_07)
   - [DownloadManager_Download_Pause_Cancel_Package (DM_08)](#downloadmanager_download_pause_cancel_package-dm_08)
   - [DownloadManager_Download_Multiple_Pause_Resume_Operations (DM_09)](#downloadmanager_download_multiple_pause_resume_operations-dm_09)
   - [DownloadManager_Download_Cancel_Package (DM_10)](#downloadmanager_download_cancel_package-dm_10)
   - [DownloadManager_Download_Pause_Delete_Resume_Delete_Package (DM_11)](#downloadmanager_download_pause_delete_resume_delete_package-dm_11)
   - [DownloadManager_Cancel_Package_Empty_Parameter (DM_12)](#downloadmanager_cancel_package_empty_parameter-dm_12)
   - [DownloadManager_Cancel_Package_Invalid_Parameter (DM_13)](#downloadmanager_cancel_package_invalid_parameter-dm_13)
   - [DownloadManager_Download_Empty_URL (DM_14)](#downloadmanager_download_empty_url-dm_14)
   - [DownloadManager_Download_Invalid_URL (DM_15)](#downloadmanager_download_invalid_url-dm_15)
   - [DownloadManager_Pause_Empty_Parameter (DM_16)](#downloadmanager_pause_empty_parameter-dm_16)
   - [DownloadManager_Pause_Invalid_Parameter (DM_17)](#downloadmanager_pause_invalid_parameter-dm_17)
   - [DownloadManager_Resume_Empty_Parameter (DM_18)](#downloadmanager_resume_empty_parameter-dm_18)
   - [DownloadManager_Resume_Invalid_Parameter (DM_19)](#downloadmanager_resume_invalid_parameter-dm_19)
   - [DownloadManager_Progress_Empty_Parameter (DM_20)](#downloadmanager_progress_empty_parameter-dm_20)
   - [DownloadManager_Progress_Invalid_Parameter (DM_21)](#downloadmanager_progress_invalid_parameter-dm_21)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DownloadManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DownloadManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getStorageDetails`
- **Lifecycle / Control APIs**: `pause`, `resume`
- **Configuration APIs**: `delete`
- **Other APIs**: `cancel`, `download`, `progress`

### APIs Under Test

| API | Description |
|-----|-------------|
| `cancel` | Cancels an ongoing download |
| `delete` | Deletes a package |
| `download` | Downloads a file from the specified URL |
| `getStorageDetails` | Retrieve storage details of packages |
| `pause` | Pauses an ongoing download |
| `progress` | Retrieves the progress of a download |
| `resume` | Resumes a paused download |

---

## Pre-conditions

### Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppStorageManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_DownloadManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DownloadManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

## Test Cases

<a id="downloadmanager_download_validparameters-dm_01"></a>
### DownloadManager_Download_ValidParameters (DM_01)

**Objective:** Verify that the download method works correctly with valid parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_getstoragedetails_functionality-dm_02"></a>
### DownloadManager_GetStorageDetails_Functionality (DM_02)

**Objective:** Verify that the getStorageDetails method functions correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorageDetails | Invoke `getStorageDetails` on `org.rdk.DownloadManager` with `type`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`, `id`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.getStorageDetails", "params": {"type": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>", "id": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Storage details are returned with valid non-empty values |
| 2 | Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Uninstalled Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Uninstalled package validation succeeds |

---

<a id="downloadmanager_cancel_emptyparameters-dm_03"></a>
### DownloadManager_Cancel_EmptyParameters (DM_03)

**Objective:** Verify that the cancel method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Cancel EmptyParameters | Invoke `cancel` on `org.rdk.DownloadManager` with `downloadId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_emptyfilelocator-dm_04"></a>
### DownloadManager_Delete_EmptyFileLocator (DM_04)

**Objective:** Verify that the delete method handles empty fileLocator correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Delete EmptyFileLocator | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_invalidfilelocator-dm_05"></a>
### DownloadManager_Delete_InvalidFileLocator (DM_05)

**Objective:** Verify that the delete method handles invalid fileLocator correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Delete InvalidFileLocator | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"invalid_file_locator"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "invalid_file_locator"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_delete_package_twotimes-dm_06"></a>
### DownloadManager_Delete_Package_TwoTimes (DM_06)

**Objective:** Verify delete method with valid parameters and perform two consecutive delete operations

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | First Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Second Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_download_pause_resume_delete_package-dm_07"></a>
### DownloadManager_Download_Pause_Resume_Delete_Package (DM_07)

**Objective:** Verify download, pause, resume and delete package functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Progress Check During Download | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke `pause` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download remains paused with expected progress value |
| 6 | Resume Download | Invoke `resume` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 7 | Progress Check After Resume | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress increases successfully after resume |
| 8 | Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_download_pause_cancel_package-dm_08"></a>
### DownloadManager_Download_Pause_Cancel_Package (DM_08)

**Objective:** Verify download, pause and cancel package functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Progress Check During Download | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke `pause` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download remains paused with expected progress value |
| 6 | Cancel Download | Invoke `cancel` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_download_multiple_pause_resume_operations-dm_09"></a>
### DownloadManager_Download_Multiple_Pause_Resume_Operations (DM_09)

**Objective:** Verify download with multiple pause and resume operations followed by delete

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Progress Check During Download | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 3 | Download Multiple Pause Resume Operations | Repeat Pause/Resume sequence for `PACKAGEMANAGER_PAUSE_RESUME_TIMES` iterations<br>Pause: invoke `pause` with `downloadId` `<result_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc`<br>Resume: invoke `resume` with `downloadId` `<result_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Pause and Resume calls succeed for each iteration with null/empty response |
| 4 | Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_download_cancel_package-dm_10"></a>
### DownloadManager_Download_Cancel_Package (DM_10)

**Objective:** Verify download and cancel package functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Progress Check During Download | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 3 | Cancel Download | Invoke `cancel` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_download_pause_delete_resume_delete_package-dm_11"></a>
### DownloadManager_Download_Pause_Delete_Resume_Delete_Package (DM_11)

**Objective:** Verify download, pause, delete, resume and delete package functionality

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_LARGE_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Progress Check During Download | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 3 | Pause Download | Invoke `pause` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check Download Paused Status | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress is reported successfully (0-100%) |
| 5 | Confirm Download Remains Paused | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download remains paused with expected progress value |
| 6 | Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |
| 7 | Resume Download | Invoke `resume` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 8 | Progress Check After Resume | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Download progress increases successfully after resume |
| 9 | Delete Package | Invoke `delete` on `org.rdk.DownloadManager` with `fileLocator`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.delete", "params": {"fileLocator": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="downloadmanager_cancel_package_empty_parameter-dm_12"></a>
### DownloadManager_Cancel_Package_Empty_Parameter (DM_12)

**Objective:** Check cancel package functionality with empty parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Cancel Download Empty Parameter | Invoke `cancel` on `org.rdk.DownloadManager` with `downloadId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_cancel_package_invalid_parameter-dm_13"></a>
### DownloadManager_Cancel_Package_Invalid_Parameter (DM_13)

**Objective:** Check cancel package functionality with invalid parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Cancel Download Invalid Parameter | Invoke `cancel` on `org.rdk.DownloadManager` with `downloadId`: `"invalid_handle"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.cancel", "params": {"downloadId": "invalid_handle"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_download_empty_url-dm_14"></a>
### DownloadManager_Download_Empty_URL (DM_14)

**Objective:** Verify that the download method handles empty URL correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download Empty URL | Invoke `download` on `org.rdk.DownloadManager` with `url`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_download_invalid_url-dm_15"></a>
### DownloadManager_Download_Invalid_URL (DM_15)

**Objective:** Verify that the download method handles invalid URL correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download Invalid URL | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"http://invalid.com/"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "http://invalid.com/"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_pause_empty_parameter-dm_16"></a>
### DownloadManager_Pause_Empty_Parameter (DM_16)

**Objective:** Verify that the pause method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Pause Download Empty Parameter | Invoke `pause` on `org.rdk.DownloadManager` with `downloadId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_pause_invalid_parameter-dm_17"></a>
### DownloadManager_Pause_Invalid_Parameter (DM_17)

**Objective:** Verify that the pause method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Pause Download Invalid Parameter | Invoke `pause` on `org.rdk.DownloadManager` with `downloadId`: `"invalid_download_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.pause", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_resume_empty_parameter-dm_18"></a>
### DownloadManager_Resume_Empty_Parameter (DM_18)

**Objective:** Verify that the resume method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Download Empty Parameter | Invoke `resume` on `org.rdk.DownloadManager` with `downloadId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_resume_invalid_parameter-dm_19"></a>
### DownloadManager_Resume_Invalid_Parameter (DM_19)

**Objective:** Verify that the resume method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Download Invalid Parameter | Invoke `resume` on `org.rdk.DownloadManager` with `downloadId`: `"invalid_download_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.resume", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_progress_empty_parameter-dm_20"></a>
### DownloadManager_Progress_Empty_Parameter (DM_20)

**Objective:** Verify that the progress method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Progress Download Empty Parameter | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="downloadmanager_progress_invalid_parameter-dm_21"></a>
### DownloadManager_Progress_Invalid_Parameter (DM_21)

**Objective:** Verify that the progress method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Progress Download Invalid Parameter | Invoke `progress` on `org.rdk.DownloadManager` with `downloadId`: `"invalid_download_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.progress", "params": {"downloadId": "invalid_download_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 30 minutes |
| Priority | High |
| TDK Release Version | M147 |