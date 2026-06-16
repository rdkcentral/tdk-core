## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [PackageManager_ListPackages_Functionality (PM_01)](#packagemanager_listpackages_functionality-pm_01)
   - [PackageManager_Install_ValidParameters (PM_02)](#packagemanager_install_validparameters-pm_02)
   - [PackageManager_Uninstall_ValidParameters (PM_03)](#packagemanager_uninstall_validparameters-pm_03)
   - [PackageManager_GetPackageState_EmptyParameters (PM_04)](#packagemanager_getpackagestate_emptyparameters-pm_04)
   - [PackageManager_GetPackageState_InvalidParameters (PM_05)](#packagemanager_getpackagestate_invalidparameters-pm_05)
   - [PackageManager_Uninstall_InvalidParameter (PM_06)](#packagemanager_uninstall_invalidparameter-pm_06)
   - [PackageManager_Install_InvalidParameters (PM_07)](#packagemanager_install_invalidparameters-pm_07)
   - [PackageManager_Uninstall_EmptyParameters (PM_08)](#packagemanager_uninstall_emptyparameters-pm_08)
   - [PackageManager_Uninstall_InvalidParameters (PM_09)](#packagemanager_uninstall_invalidparameters-pm_09)
   - [PackageManager_Unlock_Package_EmptyParameters (PM_10)](#packagemanager_unlock_package_emptyparameters-pm_10)
   - [PackageManager_Unlock_Package_InvalidPackageId_EmptyVersion (PM_11)](#packagemanager_unlock_package_invalidpackageid_emptyversion-pm_11)
   - [PackageManager_Unlock_Package_EmptyPackageId_InvalidVersion (PM_12)](#packagemanager_unlock_package_emptypackageid_invalidversion-pm_12)
   - [PackageManager_GetLockedInfo_EmptyParameters (PM_13)](#packagemanager_getlockedinfo_emptyparameters-pm_13)
   - [PackageManager_GetLockedInfo_InvalidPackageId_EmptyVersion (PM_14)](#packagemanager_getlockedinfo_invalidpackageid_emptyversion-pm_14)
   - [PackageManager_GetLockedInfo_EmptyPackageId_InvalidVersion (PM_15)](#packagemanager_getlockedinfo_emptypackageid_invalidversion-pm_15)
   - [PackageManager_Uninstall_TwoTimes (PM_16)](#packagemanager_uninstall_twotimes-pm_16)
   - [PackageManager_Install_EmptyParameters (PM_17)](#packagemanager_install_emptyparameters-pm_17)
   - [PackageManager_Lock_Package_EmptyParameters (PM_18)](#packagemanager_lock_package_emptyparameters-pm_18)
   - [PackageManager_Lock_Package_InvalidParameters (PM_19)](#packagemanager_lock_package_invalidparameters-pm_19)
   - [PackageManager_Check_Package_State_After_Install (PM_20)](#packagemanager_check_package_state_after_install-pm_20)
   - [PackageManager_Check_Package_State_After_Uninstall (PM_21)](#packagemanager_check_package_state_after_uninstall-pm_21)
   - [PackageManager_Config_ValidParameters (PM_22)](#packagemanager_config_validparameters-pm_22)
   - [PackageManager_Config_EmptyParameters (PM_23)](#packagemanager_config_emptyparameters-pm_23)
   - [PackageManager_Config_InvalidParameters (PM_24)](#packagemanager_config_invalidparameters-pm_24)
   - [PackageManager_Config_EmptyPackageId_ValidVersion (PM_25)](#packagemanager_config_emptypackageid_validversion-pm_25)
   - [PackageManager_Config_ValidPackageId_EmptyVersion (PM_26)](#packagemanager_config_validpackageid_emptyversion-pm_26)
   - [PackageManager_Lock_Package_ValidParameters (PM_27)](#packagemanager_lock_package_validparameters-pm_27)
   - [PackageManager_Lock_Package_EmptyPackageId (PM_28)](#packagemanager_lock_package_emptypackageid-pm_28)
   - [PackageManager_Lock_Package_EmptyVersion (PM_29)](#packagemanager_lock_package_emptyversion-pm_29)
   - [PackageManager_Lock_Package_EmptyLockReason (PM_30)](#packagemanager_lock_package_emptylockreason-pm_30)
   - [PackageManager_Lock_Package_InvalidPackageId (PM_31)](#packagemanager_lock_package_invalidpackageid-pm_31)
   - [PackageManager_Lock_Package_InvalidVersion (PM_32)](#packagemanager_lock_package_invalidversion-pm_32)
   - [PackageManager_Lock_Package_NoParameters (PM_33)](#packagemanager_lock_package_noparameters-pm_33)
   - [PackageManager_Unlock_Package_ValidParameters (PM_34)](#packagemanager_unlock_package_validparameters-pm_34)
   - [PackageManager_Unlock_Package_NoParameters (PM_35)](#packagemanager_unlock_package_noparameters-pm_35)
   - [PackageManager_GetLockedInfo_ValidParameters (PM_36)](#packagemanager_getlockedinfo_validparameters-pm_36)
   - [PackageManager_GetLockedInfo_NoParameters (PM_37)](#packagemanager_getlockedinfo_noparameters-pm_37)
   - [PackageManager_Check_On_AppInstallationStatus_Event (PM_38)](#packagemanager_check_on_appinstallationstatus_event-pm_38)
   - [PackageManager_GetPackageState_ValidPackageId_InvalidVersion (PM_39)](#packagemanager_getpackagestate_validpackageid_invalidversion-pm_39)
   - [PackageManager_GetPackageState_InvalidPackageId_ValidVersion (PM_40)](#packagemanager_getpackagestate_invalidpackageid_validversion-pm_40)
   - [PackageManager_GetPackageState_NoParameters (PM_41)](#packagemanager_getpackagestate_noparameters-pm_41)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **PackageManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PackageManagerRDKEMS` (version 1)

**API Coverage**

- **State / Query APIs**: `getLockedInfo`, `listPackages`
- **Events**: `onAppInstallationStatus`
- **Other APIs**: `config`, `install`, `lock`, `packageState`, `uninstall`, `unlock`

### APIs Under Test

| API | Description |
|-----|-------------|
| `config` | Retrieves configuration information for a installed application |
| `getLockedInfo` | Retrieves lock information for packages |
| `install` | Installs a package |
| `listPackages` | Retrieves information about packages |
| `lock` | Locks an application to prevent uninstallation |
| `packageState` | Retrieves the current state of a package |
| `uninstall` | Uninstalls a package |
| `unlock` | Unlocks a package |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onAppInstallationStatus` | Emitted when the Installation status of a queued requested has changed, including if it's terminated either gracefully or via a crash |

---

## Pre-conditions

### Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppStorageManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_PackageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PackageManagerRDKEMS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Register_And_Listen_Events

- Register and listen to event `Event_On_AppInstallationStatus` on `PackageManager` plugin

---

## Test Cases

<a id="packagemanager_listpackages_functionality-pm_01"></a>
### PackageManager_ListPackages_Functionality (PM_01)

**Objective:** Verify that the listPackages method functions correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | ListPackages | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |

---

<a id="packagemanager_install_validparameters-pm_02"></a>
### PackageManager_Install_ValidParameters (PM_02)

**Objective:** Verify that the install method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

---

<a id="packagemanager_uninstall_validparameters-pm_03"></a>
### PackageManager_Uninstall_ValidParameters (PM_03)

**Objective:** Verify that the uninstall method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Verify Uninstalled Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Uninstalled package validation succeeds |

---

<a id="packagemanager_getpackagestate_emptyparameters-pm_04"></a>
### PackageManager_GetPackageState_EmptyParameters (PM_04)

**Objective:** Verify that the getPackageState method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetPackageState EmptyParameters | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_invalidparameters-pm_05"></a>
### PackageManager_GetPackageState_InvalidParameters (PM_05)

**Objective:** Verify that the getPackageState method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetPackageState InvalidParameters | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"invalid_version"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_invalidparameter-pm_06"></a>
### PackageManager_Uninstall_InvalidParameter (PM_06)

**Objective:** Verify that the uninstall method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Uninstall InvalidParameter | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "invalid_package_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_install_invalidparameters-pm_07"></a>
### PackageManager_Install_InvalidParameters (PM_07)

**Objective:** Verify that the install method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Install InvalidParameters | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"invalid_version"`, `fileLocator`: `"invalid_file_locator"`, `name`: `"invalid_name"`, `value`: `"invalid_value"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "invalid_package_id", "version": "invalid_version", "fileLocator": "invalid_file_locator", "name": "invalid_name", "value": "invalid_value"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_emptyparameters-pm_08"></a>
### PackageManager_Uninstall_EmptyParameters (PM_08)

**Objective:** Verify that the uninstall method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Uninstall EmptyParameters | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_invalidparameters-pm_09"></a>
### PackageManager_Uninstall_InvalidParameters (PM_09)

**Objective:** Verify that the uninstall method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Uninstall InvalidParameters | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "invalid_package_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_unlock_package_emptyparameters-pm_10"></a>
### PackageManager_Unlock_Package_EmptyParameters (PM_10)

**Objective:** Verify that the unlock method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package EmptyParameters | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_unlock_package_invalidpackageid_emptyversion-pm_11"></a>
### PackageManager_Unlock_Package_InvalidPackageId_EmptyVersion (PM_11)

**Objective:** Verify that the unlock method handles invalid packageId with empty version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package InvalidPackageId EmptyVersion | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "invalid_package_id", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_unlock_package_emptypackageid_invalidversion-pm_12"></a>
### PackageManager_Unlock_Package_EmptyPackageId_InvalidVersion (PM_12)

**Objective:** Verify that the unlock method handles empty packageId with invalid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package EmptyPackageId InvalidVersion | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `"invalid_version"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_emptyparameters-pm_13"></a>
### PackageManager_GetLockedInfo_EmptyParameters (PM_13)

**Objective:** Verify that the getLockedInfo method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetLockedInfo EmptyParameters | Invoke `getLockedInfo` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_invalidpackageid_emptyversion-pm_14"></a>
### PackageManager_GetLockedInfo_InvalidPackageId_EmptyVersion (PM_14)

**Objective:** Verify that the getLockedInfo method handles invalid packageId with empty version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetLockedInfo InvalidPackageId EmptyVersion | Invoke `getLockedInfo` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "invalid_package_id", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_emptypackageid_invalidversion-pm_15"></a>
### PackageManager_GetLockedInfo_EmptyPackageId_InvalidVersion (PM_15)

**Objective:** Verify that the getLockedInfo method handles empty packageId with invalid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetLockedInfo EmptyPackageId InvalidVersion | Invoke `getLockedInfo` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `"invalid_version"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_uninstall_twotimes-pm_16"></a>
### PackageManager_Uninstall_TwoTimes (PM_16)

**Objective:** Verify uninstall method with valid parameters and perform two consecutive uninstall operations

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | First Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Verify Uninstalled Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Uninstalled package validation succeeds |
| 3 | Second Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_install_emptyparameters-pm_17"></a>
### PackageManager_Install_EmptyParameters (PM_17)

**Objective:** Verify that the install method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Install EmptyParameters | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`, `fileLocator`: `""`, `name`: `""`, `value`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "", "version": "", "fileLocator": "", "name": "", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Requested version is not supported.` |

---

<a id="packagemanager_lock_package_emptyparameters-pm_18"></a>
### PackageManager_Lock_Package_EmptyParameters (PM_18)

**Objective:** Verify that the lock method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package EmptyParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`, `lockReason`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "", "version": "", "lockReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_lock_package_invalidparameters-pm_19"></a>
### PackageManager_Lock_Package_InvalidParameters (PM_19)

**Objective:** Verify that the lock method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package InvalidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"invalid_version"`, `lockReason`: `"invalid_reason"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "invalid_package_id", "version": "invalid_version", "lockReason": "invalid_reason"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Could not access requested service` |

---

<a id="packagemanager_check_package_state_after_install-pm_20"></a>
### PackageManager_Check_Package_State_After_Install (PM_20)

**Objective:** Verify that the package state method works correctly after installing a package with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Package State | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `INSTALLED` |

---

<a id="packagemanager_check_package_state_after_uninstall-pm_21"></a>
### PackageManager_Check_Package_State_After_Uninstall (PM_21)

**Objective:** Verify that the package state method works correctly after uninstalling a package with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check Package State | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `UNINSTALLED` |

---

<a id="packagemanager_config_validparameters-pm_22"></a>
### PackageManager_Config_ValidParameters (PM_22)

**Objective:** Verify that the config method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |
| 4 | Get Installed App Config | Invoke `config` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call is successful when the response is not null or empty |

---

<a id="packagemanager_config_emptyparameters-pm_23"></a>
### PackageManager_Config_EmptyParameters (PM_23)

**Objective:** Verify that the config method handles empty parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Config EmptyParameters | Invoke `config` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_config_invalidparameters-pm_24"></a>
### PackageManager_Config_InvalidParameters (PM_24)

**Objective:** Verify that the config method handles invalid parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Config InvalidParameters | Invoke `config` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"invalid_version"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_config_emptypackageid_validversion-pm_25"></a>
### PackageManager_Config_EmptyPackageId_ValidVersion (PM_25)

**Objective:** Verify that the config method handles empty packageId with valid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Config EmptyPackageId ValidVersion | Invoke `config` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_config_validpackageid_emptyversion-pm_26"></a>
### PackageManager_Config_ValidPackageId_EmptyVersion (PM_26)

**Objective:** Verify that the config method handles valid packageId with empty version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Config ValidPackageId EmptyVersion | Invoke `config` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_validparameters-pm_27"></a>
### PackageManager_Lock_Package_ValidParameters (PM_27)

**Objective:** Verify that the lock method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Unlock_Package_After_Lock

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="packagemanager_lock_package_emptypackageid-pm_28"></a>
### PackageManager_Lock_Package_EmptyPackageId (PM_28)

**Objective:** Verify that the lock method handles empty packageId correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package EmptyPackageId | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `""`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_emptyversion-pm_29"></a>
### PackageManager_Lock_Package_EmptyVersion (PM_29)

**Objective:** Verify that the lock method handles empty version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package EmptyVersion | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `""`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_emptylockreason-pm_30"></a>
### PackageManager_Lock_Package_EmptyLockReason (PM_30)

**Objective:** Verify that the lock method handles empty lockReason correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package EmptyLockReason | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_invalidpackageid-pm_31"></a>
### PackageManager_Lock_Package_InvalidPackageId (PM_31)

**Objective:** Verify that the lock method handles invalid packageId correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package InvalidPackageId | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "invalid_package_id", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_invalidversion-pm_32"></a>
### PackageManager_Lock_Package_InvalidVersion (PM_32)

**Objective:** Verify that the lock method handles invalid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package InvalidVersion | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"invalid_version"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "invalid_version", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_noparameters-pm_33"></a>
### PackageManager_Lock_Package_NoParameters (PM_33)

**Objective:** Verify that the lock method handles missing parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package NoParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_unlock_package_validparameters-pm_34"></a>
### PackageManager_Unlock_Package_ValidParameters (PM_34)

**Objective:** Verify that the unlock method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

#### Pre-condition 3: Lock_Package_Before_Unlock

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="packagemanager_unlock_package_noparameters-pm_35"></a>
### PackageManager_Unlock_Package_NoParameters (PM_35)

**Objective:** Verify that the unlock method handles missing parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package NoParameters | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_getlockedinfo_validparameters-pm_36"></a>
### PackageManager_GetLockedInfo_ValidParameters (PM_36)

**Objective:** Verify that the getLockedInfo method works correctly with valid parameters

**Pre-condition:**

#### Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

#### Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

#### Pre-condition 3: Lock_Package_Before_GetLockedInfo

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetLockedInfo ValidParameters | Invoke `getLockedInfo` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call is successful when the response is not null or empty |

**Post-condition:**

#### Post-condition 1: Unlock_Package_After_GetLockedInfo

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="packagemanager_getlockedinfo_noparameters-pm_37"></a>
### PackageManager_GetLockedInfo_NoParameters (PM_37)

**Objective:** Verify that the getLockedInfo method handles missing parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetLockedInfo NoParameters | Invoke `getLockedInfo` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_check_on_appinstallationstatus_event-pm_38"></a>
### PackageManager_Check_On_AppInstallationStatus_Event (PM_38)

**Objective:** Verify that the appInstallationStatus event is triggered with correct status during app installation and uninstallation

**Pre-condition:**

#### Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 2 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_2>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | GetPackageState ValidParameters | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `INSTALLED` |
| 4 | Check Event On App Installation Status | Listen for event `Event_On_AppInstallationStatus` | Event data validated successfully |
| 5 | Uninstall | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 6 | GetPackageState After Uninstall | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `UNINSTALLED` |
| 7 | Check Event On App Installation Status | Listen for event `Event_On_AppInstallationStatus` | Event data validated successfully |

---

<a id="packagemanager_getpackagestate_validpackageid_invalidversion-pm_39"></a>
### PackageManager_GetPackageState_ValidPackageId_InvalidVersion (PM_39)

**Objective:** Verify that the getPackageState method handles valid packageId with invalid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetPackageState ValidPackageId InvalidVersion | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"invalid_version"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_invalidpackageid_validversion-pm_40"></a>
### PackageManager_GetPackageState_InvalidPackageId_ValidVersion (PM_40)

**Objective:** Verify that the getPackageState method handles invalid packageId with valid version correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetPackageState InvalidPackageId ValidVersion | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"invalid_package_id"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "invalid_package_id", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_noparameters-pm_41"></a>
### PackageManager_GetPackageState_NoParameters (PM_41)

**Objective:** Verify that the getPackageState method handles missing parameters correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetPackageState NoParameters | Invoke `packageState` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

---

## Post-conditions

### Post-condition 1: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |