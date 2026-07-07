## TestScript Name
RDKV_CERT_AVS_PackageManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [PackageManager_ListPackages_Functionality](#packagemanager_listpackages_functionality)
   - [PackageManager_Install_ValidParameters](#packagemanager_install_validparameters)
   - [PackageManager_Uninstall_ValidParameters](#packagemanager_uninstall_validparameters)
   - [PackageManager_GetPackageState_EmptyParameters](#packagemanager_getpackagestate_emptyparameters)
   - [PackageManager_GetPackageState_InvalidParameters](#packagemanager_getpackagestate_invalidparameters)
   - [PackageManager_Uninstall_InvalidParameter](#packagemanager_uninstall_invalidparameter)
   - [PackageManager_Install_InvalidParameters](#packagemanager_install_invalidparameters)
   - [PackageManager_Uninstall_EmptyParameters](#packagemanager_uninstall_emptyparameters)
   - [PackageManager_Uninstall_InvalidParameters](#packagemanager_uninstall_invalidparameters)
   - [PackageManager_Unlock_Package_EmptyParameters](#packagemanager_unlock_package_emptyparameters)
   - [PackageManager_Unlock_Package_InvalidPackageId_EmptyVersion](#packagemanager_unlock_package_invalidpackageid_emptyversion)
   - [PackageManager_Unlock_Package_EmptyPackageId_InvalidVersion](#packagemanager_unlock_package_emptypackageid_invalidversion)
   - [PackageManager_GetLockedInfo_EmptyParameters](#packagemanager_getlockedinfo_emptyparameters)
   - [PackageManager_GetLockedInfo_InvalidPackageId_EmptyVersion](#packagemanager_getlockedinfo_invalidpackageid_emptyversion)
   - [PackageManager_GetLockedInfo_EmptyPackageId_InvalidVersion](#packagemanager_getlockedinfo_emptypackageid_invalidversion)
   - [PackageManager_Uninstall_TwoTimes](#packagemanager_uninstall_twotimes)
   - [PackageManager_Install_EmptyParameters](#packagemanager_install_emptyparameters)
   - [PackageManager_Lock_Package_EmptyParameters](#packagemanager_lock_package_emptyparameters)
   - [PackageManager_Lock_Package_InvalidParameters](#packagemanager_lock_package_invalidparameters)
   - [PackageManager_Check_Package_State_After_Install](#packagemanager_check_package_state_after_install)
   - [PackageManager_Check_Package_State_After_Uninstall](#packagemanager_check_package_state_after_uninstall)
   - [PackageManager_Config_ValidParameters](#packagemanager_config_validparameters)
   - [PackageManager_Config_EmptyParameters](#packagemanager_config_emptyparameters)
   - [PackageManager_Config_InvalidParameters](#packagemanager_config_invalidparameters)
   - [PackageManager_Config_EmptyPackageId_ValidVersion](#packagemanager_config_emptypackageid_validversion)
   - [PackageManager_Config_ValidPackageId_EmptyVersion](#packagemanager_config_validpackageid_emptyversion)
   - [PackageManager_Lock_Package_ValidParameters](#packagemanager_lock_package_validparameters)
   - [PackageManager_Lock_Package_EmptyPackageId](#packagemanager_lock_package_emptypackageid)
   - [PackageManager_Lock_Package_EmptyVersion](#packagemanager_lock_package_emptyversion)
   - [PackageManager_Lock_Package_EmptyLockReason](#packagemanager_lock_package_emptylockreason)
   - [PackageManager_Lock_Package_InvalidPackageId](#packagemanager_lock_package_invalidpackageid)
   - [PackageManager_Lock_Package_InvalidVersion](#packagemanager_lock_package_invalidversion)
   - [PackageManager_Lock_Package_NoParameters](#packagemanager_lock_package_noparameters)
   - [PackageManager_Unlock_Package_ValidParameters](#packagemanager_unlock_package_validparameters)
   - [PackageManager_Unlock_Package_NoParameters](#packagemanager_unlock_package_noparameters)
   - [PackageManager_GetLockedInfo_ValidParameters](#packagemanager_getlockedinfo_validparameters)
   - [PackageManager_GetLockedInfo_NoParameters](#packagemanager_getlockedinfo_noparameters)
   - [PackageManager_Check_On_AppInstallationStatus_Event](#packagemanager_check_on_appinstallationstatus_event)
   - [PackageManager_GetPackageState_ValidPackageId_InvalidVersion](#packagemanager_getpackagestate_validpackageid_invalidversion)
   - [PackageManager_GetPackageState_InvalidPackageId_ValidVersion](#packagemanager_getpackagestate_invalidpackageid_validversion)
   - [PackageManager_GetPackageState_NoParameters](#packagemanager_getpackagestate_noparameters)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **PackageManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PackageManagerRDKEMS` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_PackageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onAppInstallationStatus event | Register a WebSocket event listener for `onAppInstallationStatus` to receive `onAppInstallationStatus` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.register", "params": {"event": "onAppInstallationStatus", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 4: Configure_Device_Parameter

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Application Name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure Application Version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure Application Hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure Additionalmetadata Name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure Additionalmetadata Value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure Application MD5 Checksum Value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="packagemanager_listpackages_functionality"></a>
### TestCase Name
PackageManager_ListPackages_Functionality

### TestCase ID
PM_01

### TestCase Objective
Verify that the listPackages method functions correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | ListPackages | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |

---

<a id="packagemanager_install_validparameters"></a>
### TestCase Name
PackageManager_Install_ValidParameters

### TestCase ID
PM_02

### TestCase Objective
Verify that the install method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Invoke install on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

---

<a id="packagemanager_uninstall_validparameters"></a>
### TestCase Name
PackageManager_Uninstall_ValidParameters

### TestCase ID
PM_03

### TestCase Objective
Verify that the uninstall method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Verify Uninstalled Package | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the package is successfully uninstalled |

---

<a id="packagemanager_getpackagestate_emptyparameters"></a>
### TestCase Name
PackageManager_GetPackageState_EmptyParameters

### TestCase ID
PM_04

### TestCase Objective
Verify that the getPackageState method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState EmptyParameters | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_invalidparameters"></a>
### TestCase Name
PackageManager_GetPackageState_InvalidParameters

### TestCase ID
PM_05

### TestCase Objective
Verify that the getPackageState method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState InvalidParameters | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_invalidparameter"></a>
### TestCase Name
PackageManager_Uninstall_InvalidParameter

### TestCase ID
PM_06

### TestCase Objective
Verify that the uninstall method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall InvalidParameter | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "invalid_package_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_install_invalidparameters"></a>
### TestCase Name
PackageManager_Install_InvalidParameters

### TestCase ID
PM_07

### TestCase Objective
Verify that the install method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Install InvalidParameters | Invoke install on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "invalid_version", fileLocator: "invalid_file_locator", name: "invalid_name", value: "invalid_value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "invalid_package_id", "version": "invalid_version", "fileLocator": "invalid_file_locator", "name": "invalid_name", "value": "invalid_value"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_emptyparameters"></a>
### TestCase Name
PackageManager_Uninstall_EmptyParameters

### TestCase ID
PM_08

### TestCase Objective
Verify that the uninstall method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall EmptyParameters | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_uninstall_invalidparameters"></a>
### TestCase Name
PackageManager_Uninstall_InvalidParameters

### TestCase ID
PM_09

### TestCase Objective
Verify that the uninstall method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall InvalidParameters | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "invalid_package_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_unlock_package_emptyparameters"></a>
### TestCase Name
PackageManager_Unlock_Package_EmptyParameters

### TestCase ID
PM_10

### TestCase Objective
Verify that the unlock method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package EmptyParameters | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_unlock_package_invalidpackageid_emptyversion"></a>
### TestCase Name
PackageManager_Unlock_Package_InvalidPackageId_EmptyVersion

### TestCase ID
PM_11

### TestCase Objective
Verify that the unlock method handles invalid packageId with empty version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package InvalidPackageId EmptyVersion | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "invalid_package_id", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_unlock_package_emptypackageid_invalidversion"></a>
### TestCase Name
PackageManager_Unlock_Package_EmptyPackageId_InvalidVersion

### TestCase ID
PM_12

### TestCase Objective
Verify that the unlock method handles empty packageId with invalid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package EmptyPackageId InvalidVersion | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_emptyparameters"></a>
### TestCase Name
PackageManager_GetLockedInfo_EmptyParameters

### TestCase ID
PM_13

### TestCase Objective
Verify that the getLockedInfo method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetLockedInfo EmptyParameters | Invoke getLockedInfo on org.rdk.PackageManagerRDKEMS with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_invalidpackageid_emptyversion"></a>
### TestCase Name
PackageManager_GetLockedInfo_InvalidPackageId_EmptyVersion

### TestCase ID
PM_14

### TestCase Objective
Verify that the getLockedInfo method handles invalid packageId with empty version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetLockedInfo InvalidPackageId EmptyVersion | Invoke getLockedInfo on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "invalid_package_id", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_getlockedinfo_emptypackageid_invalidversion"></a>
### TestCase Name
PackageManager_GetLockedInfo_EmptyPackageId_InvalidVersion

### TestCase ID
PM_15

### TestCase Objective
Verify that the getLockedInfo method handles empty packageId with invalid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetLockedInfo EmptyPackageId InvalidVersion | Invoke getLockedInfo on org.rdk.PackageManagerRDKEMS with packageId: "", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_uninstall_twotimes"></a>
### TestCase Name
PackageManager_Uninstall_TwoTimes

### TestCase ID
PM_16

### TestCase Objective
Verify uninstall method with valid parameters and perform two consecutive uninstall operations

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | First Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Verify Uninstalled Package | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the package is successfully uninstalled |
| 3 | Second Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_install_emptyparameters"></a>
### TestCase Name
PackageManager_Install_EmptyParameters

### TestCase ID
PM_17

### TestCase Objective
Verify that the install method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Install EmptyParameters | Invoke install on org.rdk.PackageManagerRDKEMS with packageId: "", version: "", fileLocator: "", name: "", value: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "", "version": "", "fileLocator": "", "name": "", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Requested version is not supported.` |

---

<a id="packagemanager_lock_package_emptyparameters"></a>
### TestCase Name
PackageManager_Lock_Package_EmptyParameters

### TestCase ID
PM_18

### TestCase Objective
Verify that the lock method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package EmptyParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "", version: "", lockReason: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "", "version": "", "lockReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_lock_package_invalidparameters"></a>
### TestCase Name
PackageManager_Lock_Package_InvalidParameters

### TestCase ID
PM_19

### TestCase Objective
Verify that the lock method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package InvalidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "invalid_version", lockReason: "invalid_reason"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "invalid_package_id", "version": "invalid_version", "lockReason": "invalid_reason"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Could not access requested service` |

---

<a id="packagemanager_check_package_state_after_install"></a>
### TestCase Name
PackageManager_Check_Package_State_After_Install

### TestCase ID
PM_20

### TestCase Objective
Verify that the package state method works correctly after installing a package with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Package State | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the installation status is `INSTALLED`, confirming the package was installed successfully  |

---

<a id="packagemanager_check_package_state_after_uninstall"></a>
### TestCase Name
PackageManager_Check_Package_State_After_Uninstall

### TestCase ID
PM_21

### TestCase Objective
Verify that the package state method works correctly after uninstalling a package with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check Package State | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the package status is `UNINSTALLED`, confirming successful uninstallation  |

---

<a id="packagemanager_config_validparameters"></a>
### TestCase Name
PackageManager_Config_ValidParameters

### TestCase ID
PM_22

### TestCase Objective
Verify that the config method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Invoke install on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Invoke listPackages on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |
| 4 | Get Installed App Config | Invoke config on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call is successful and returns a non-null, non-empty response  |

---

<a id="packagemanager_config_emptyparameters"></a>
### TestCase Name
PackageManager_Config_EmptyParameters

### TestCase ID
PM_23

### TestCase Objective
Verify that the config method handles empty parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config EmptyParameters | Invoke config on org.rdk.PackageManagerRDKEMS with packageId: "", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_config_invalidparameters"></a>
### TestCase Name
PackageManager_Config_InvalidParameters

### TestCase ID
PM_24

### TestCase Objective
Verify that the config method handles invalid parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config InvalidParameters | Invoke config on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "invalid_package_id", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_config_emptypackageid_validversion"></a>
### TestCase Name
PackageManager_Config_EmptyPackageId_ValidVersion

### TestCase ID
PM_25

### TestCase Objective
Verify that the config method handles empty packageId with valid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config EmptyPackageId ValidVersion | Invoke config on org.rdk.PackageManagerRDKEMS with packageId: "", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_config_validpackageid_emptyversion"></a>
### TestCase Name
PackageManager_Config_ValidPackageId_EmptyVersion

### TestCase ID
PM_26

### TestCase Objective
Verify that the config method handles valid packageId with empty version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config ValidPackageId EmptyVersion | Invoke config on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.config", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_validparameters"></a>
### TestCase Name
PackageManager_Lock_Package_ValidParameters

### TestCase ID
PM_27

### TestCase Objective
Verify that the lock method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package ValidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Unlock_Package_After_Lock

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package | Unlock on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="packagemanager_lock_package_emptypackageid"></a>
### TestCase Name
PackageManager_Lock_Package_EmptyPackageId

### TestCase ID
PM_28

### TestCase Objective
Verify that the lock method handles empty packageId correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package EmptyPackageId | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_emptyversion"></a>
### TestCase Name
PackageManager_Lock_Package_EmptyVersion

### TestCase ID
PM_29

### TestCase Objective
Verify that the lock method handles empty version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package EmptyVersion | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_emptylockreason"></a>
### TestCase Name
PackageManager_Lock_Package_EmptyLockReason

### TestCase ID
PM_30

### TestCase Objective
Verify that the lock method handles empty lockReason correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package EmptyLockReason | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_invalidpackageid"></a>
### TestCase Name
PackageManager_Lock_Package_InvalidPackageId

### TestCase ID
PM_31

### TestCase Objective
Verify that the lock method handles invalid packageId correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package InvalidPackageId | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "invalid_package_id", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_invalidversion"></a>
### TestCase Name
PackageManager_Lock_Package_InvalidVersion

### TestCase ID
PM_32

### TestCase Objective
Verify that the lock method handles invalid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package InvalidVersion | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "invalid_version", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "invalid_version", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_lock_package_noparameters"></a>
### TestCase Name
PackageManager_Lock_Package_NoParameters

### TestCase ID
PM_33

### TestCase Objective
Verify that the lock method handles missing parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package NoParameters | Invoke lock on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_unlock_package_validparameters"></a>
### TestCase Name
PackageManager_Unlock_Package_ValidParameters

### TestCase ID
PM_34

### TestCase Objective
Verify that the unlock method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: Lock_Package_Before_Unlock

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package ValidParameters | Lock on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="packagemanager_unlock_package_noparameters"></a>
### TestCase Name
PackageManager_Unlock_Package_NoParameters

### TestCase ID
PM_35

### TestCase Objective
Verify that the unlock method handles missing parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package NoParameters | Invoke unlock on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_getlockedinfo_validparameters"></a>
### TestCase Name
PackageManager_GetLockedInfo_ValidParameters

### TestCase ID
PM_36

### TestCase Objective
Verify that the getLockedInfo method works correctly with valid parameters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Uninstall_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

#### TestCase Pre-condition 2: Download_Install_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

#### TestCase Pre-condition 3: Lock_Package_Before_GetLockedInfo

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Lock Package ValidParameters | Lock on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetLockedInfo ValidParameters | Invoke getLockedInfo on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call is successful and returns a non-null, non-empty response  |

### TestCase Post-condition

#### TestCase Post-condition 1: Unlock_Package_After_GetLockedInfo

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unlock Package | Unlock on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="packagemanager_getlockedinfo_noparameters"></a>
### TestCase Name
PackageManager_GetLockedInfo_NoParameters

### TestCase ID
PM_37

### TestCase Objective
Verify that the getLockedInfo method handles missing parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetLockedInfo NoParameters | Invoke getLockedInfo on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.getLockedInfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_check_on_appinstallationstatus_event"></a>
### TestCase Name
PackageManager_Check_On_AppInstallationStatus_Event

### TestCase ID
PM_38

### TestCase Objective
Verify that the appInstallationStatus event is triggered with correct status during app installation and uninstallation

### TestCase Pre-condition

#### TestCase Pre-condition 1: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Download ValidParameters | Invoke download on org.rdk.DownloadManager with url: "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 2 | Install | Invoke install on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", fileLocator: "<result_step_2>", name: "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", value: "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_2>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | GetPackageState ValidParameters | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the installation status is `INSTALLED`, confirming the package was installed successfully  |
| 4 | Check Event On App Installation Status | Listen for event Event_On_AppInstallationStatus | Verify that event data is validated successfully |
| 5 | Uninstall | Invoke uninstall on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | GetPackageState After Uninstall | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the package status is `UNINSTALLED`, confirming successful uninstallation  |
| 7 | Check Event On App Installation Status | Listen for event Event_On_AppInstallationStatus | Verify that event data is validated successfully |

---

<a id="packagemanager_getpackagestate_validpackageid_invalidversion"></a>
### TestCase Name
PackageManager_GetPackageState_ValidPackageId_InvalidVersion

### TestCase ID
PM_39

### TestCase Objective
Verify that the getPackageState method handles valid packageId with invalid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState ValidPackageId InvalidVersion | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "invalid_version"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "invalid_version"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_invalidpackageid_validversion"></a>
### TestCase Name
PackageManager_GetPackageState_InvalidPackageId_ValidVersion

### TestCase ID
PM_40

### TestCase Objective
Verify that the getPackageState method handles invalid packageId with valid version correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState InvalidPackageId ValidVersion | Invoke packageState on org.rdk.PackageManagerRDKEMS with packageId: "invalid_package_id", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState", "params": {"packageId": "invalid_package_id", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="packagemanager_getpackagestate_noparameters"></a>
### TestCase Name
PackageManager_GetPackageState_NoParameters

### TestCase ID
PM_41

### TestCase Objective
Verify that the getPackageState method handles missing parameters correctly

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetPackageState NoParameters | Invoke packageState on org.rdk.PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.packageState"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onAppInstallationStatus event | Unregister the WebSocket event listener for `onAppInstallationStatus` to stop receiving `onAppInstallationStatus` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PreinstallManager.1.unregister", "params": {"event": "onAppInstallationStatus", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

### Plugin Post-condition 2: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI-Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |

<div align="right"><a href="#testscript-name">&#8593; Go to Top</a></div>
