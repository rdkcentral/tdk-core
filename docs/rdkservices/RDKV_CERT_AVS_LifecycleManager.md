## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Verify_AppReady_Valid_AppId (LCM_01)](#verify_appready_valid_appid-lcm_01)
   - [Verify_AppReady_Empty_AppId (LCM_02)](#verify_appready_empty_appid-lcm_02)
   - [Verify_AppReady_Numeric_AppId (LCM_03)](#verify_appready_numeric_appid-lcm_03)
   - [Verify_AppReady_Special_Char_AppId (LCM_04)](#verify_appready_special_char_appid-lcm_04)
   - [Verify_AppReady_Long_String_AppId (LCM_05)](#verify_appready_long_string_appid-lcm_05)
   - [LifecycleManager_Verify_AppReady_Boolean_AppId (LCM_06)](#lifecyclemanager_verify_appready_boolean_appid-lcm_06)
   - [LifecycleManager_Verify_AppReady_Without_Parameters (LCM_07)](#lifecyclemanager_verify_appready_without_parameters-lcm_07)
   - [CloseApp_Valid_AppId_USER_EXIT_CloseReason (LCM_08)](#closeapp_valid_appid_user_exit_closereason-lcm_08)
   - [CloseApp_Valid_AppId_ERROR_CloseReason (LCM_09)](#closeapp_valid_appid_error_closereason-lcm_09)
   - [CloseApp_ValidAppId_EmptyCloseReason (LCM_12)](#closeapp_validappid_emptyclosereason-lcm_12)
   - [CloseApp_Empty_AppId_USER_EXIT_CloseReason (LCM_13)](#closeapp_empty_appid_user_exit_closereason-lcm_13)
   - [CloseApp_Empty_AppId_ERROR_CloseReason (LCM_14)](#closeapp_empty_appid_error_closereason-lcm_14)
   - [CloseApp_Empty_AppId_KILL_AND_RUN_CloseReason (LCM_15)](#closeapp_empty_appid_kill_and_run_closereason-lcm_15)
   - [CloseApp_Empty_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_16)](#closeapp_empty_appid_kill_and_activate_closereason-lcm_16)
   - [LifecycleManager_CloseApp_Empty_Params (LCM_17)](#lifecyclemanager_closeapp_empty_params-lcm_17)
   - [CloseApp_Without_Parameters (LCM_18)](#closeapp_without_parameters-lcm_18)
   - [CloseApp_Invalid_AppId_USER_EXIT_CloseReason (LCM_19)](#closeapp_invalid_appid_user_exit_closereason-lcm_19)
   - [CloseApp_Invalid_AppId_ERROR_CloseReason (LCM_20)](#closeapp_invalid_appid_error_closereason-lcm_20)
   - [CloseApp_Invalid_AppId_KILL_AND_RUN_CloseReason (LCM_21)](#closeapp_invalid_appid_kill_and_run_closereason-lcm_21)
   - [CloseApp_Invalid_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_22)](#closeapp_invalid_appid_kill_and_activate_closereason-lcm_22)
   - [CloseApp_Numeric_AppId_USER_EXIT_CloseReason (LCM_23)](#closeapp_numeric_appid_user_exit_closereason-lcm_23)
   - [CloseApp_Numeric_AppId_ERROR_CloseReason (LCM_24)](#closeapp_numeric_appid_error_closereason-lcm_24)
   - [CloseApp_Numeric_AppId_KILL_AND_RUN_CloseReason (LCM_25)](#closeapp_numeric_appid_kill_and_run_closereason-lcm_25)
   - [CloseApp_Numeric_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_26)](#closeapp_numeric_appid_kill_and_activate_closereason-lcm_26)
   - [CloseApp_Special_Char_AppId_USER_EXIT_CloseReason (LCM_27)](#closeapp_special_char_appid_user_exit_closereason-lcm_27)
   - [CloseApp_Special_Char_AppId_ERROR_CloseReason (LCM_28)](#closeapp_special_char_appid_error_closereason-lcm_28)
   - [CloseApp_Special_Char_AppId_KILL_AND_RUN_CloseReason (LCM_29)](#closeapp_special_char_appid_kill_and_run_closereason-lcm_29)
   - [CloseApp_Special_Char_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_30)](#closeapp_special_char_appid_kill_and_activate_closereason-lcm_30)
   - [CloseApp_Boolean_AppId_USER_EXIT_CloseReason (LCM_31)](#closeapp_boolean_appid_user_exit_closereason-lcm_31)
   - [CloseApp_Boolean_AppId_ERROR_CloseReason (LCM_32)](#closeapp_boolean_appid_error_closereason-lcm_32)
   - [CloseApp_Boolean_AppId_KILL_AND_RUN_CloseReason (LCM_33)](#closeapp_boolean_appid_kill_and_run_closereason-lcm_33)
   - [CloseApp_Boolean_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_34)](#closeapp_boolean_appid_kill_and_activate_closereason-lcm_34)
   - [CloseApp_Long_String_AppId_USER_EXIT_CloseReason (LCM_35)](#closeapp_long_string_appid_user_exit_closereason-lcm_35)
   - [CloseApp_Long_String_AppId_ERROR_CloseReason (LCM_36)](#closeapp_long_string_appid_error_closereason-lcm_36)
   - [CloseApp_Long_String_AppId_KILL_AND_RUN_CloseReason (LCM_37)](#closeapp_long_string_appid_kill_and_run_closereason-lcm_37)
   - [CloseApp_Long_String_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_38)](#closeapp_long_string_appid_kill_and_activate_closereason-lcm_38)
   - [CloseApp_Valid_AppId_Numeric_CloseReason (LCM_39)](#closeapp_valid_appid_numeric_closereason-lcm_39)
   - [CloseApp_Valid_AppId_Special_Char_CloseReason (LCM_40)](#closeapp_valid_appid_special_char_closereason-lcm_40)
   - [CloseApp_Valid_AppId_Boolean_CloseReason (LCM_41)](#closeapp_valid_appid_boolean_closereason-lcm_41)
   - [CloseApp_Valid_AppId_Long_String_CloseReason (LCM_42)](#closeapp_valid_appid_long_string_closereason-lcm_42)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **LifecycleManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.LifecycleManager` (version 1)

**API Coverage**

- **Lifecycle / Control APIs**: `closeApp`
- **Other APIs**: `appReady`

### APIs Under Test

| API | Description |
|-----|-------------|
| `appReady` | Response API call to appInitializing API |
| `closeApp` | Close the app |

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

### Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PackageManagerRDKEMS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 4: Activate_AppManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 5: Activate_LifecycleManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.LifecycleManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.LifecycleManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.LifecycleManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.LifecycleManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 6: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_4>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

---

## Test Cases

<a id="verify_appready_valid_appid-lcm_01"></a>
### Verify_AppReady_Valid_AppId (LCM_01)

**Objective:** Verify appReady with a valid appId string

**Pre-condition:**

#### Pre-condition 1: Launch_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="verify_appready_empty_appid-lcm_02"></a>
### Verify_AppReady_Empty_AppId (LCM_02)

**Objective:** Verify appReady with an empty appId string

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_numeric_appid-lcm_03"></a>
### Verify_AppReady_Numeric_AppId (LCM_03)

**Objective:** Verify appReady with a numeric value for appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_special_char_appid-lcm_04"></a>
### Verify_AppReady_Special_Char_AppId (LCM_04)

**Objective:** Verify appReady with a special character string as appId.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady Special Char | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `"!()*^"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "!()*^"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_long_string_appid-lcm_05"></a>
### Verify_AppReady_Long_String_AppId (LCM_05)

**Objective:** Verify appReady with a very long string as appId.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady Long String | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "VeryLongStringForAppIdTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_verify_appready_boolean_appid-lcm_06"></a>
### LifecycleManager_Verify_AppReady_Boolean_AppId (LCM_06)

**Objective:** Verify appReady with a boolean value for appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady Boolean AppId | Invoke `appReady` on `org.rdk.LifecycleManager` with `appId`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_verify_appready_without_parameters-lcm_07"></a>
### LifecycleManager_Verify_AppReady_Without_Parameters (LCM_07)

**Objective:** Verify appReady without any parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify AppReady No Params | Invoke `appReady` on `org.rdk.LifecycleManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_user_exit_closereason-lcm_08"></a>
### CloseApp_Valid_AppId_USER_EXIT_CloseReason (LCM_08)

**Objective:** Verify closeApp with valid appId and USER_EXIT closeReason

**Pre-condition:**

#### Pre-condition 1: Launch_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Valid Params | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="closeapp_valid_appid_error_closereason-lcm_09"></a>
### CloseApp_Valid_AppId_ERROR_CloseReason (LCM_09)

**Objective:** Verify closeApp with valid appId and ERROR closeReason

**Pre-condition:**

#### Pre-condition 1: Launch_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App ERROR Reason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="closeapp_validappid_emptyclosereason-lcm_12"></a>
### CloseApp_ValidAppId_EmptyCloseReason (LCM_12)

**Objective:** Verify closeApp with valid appId and empty closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App ValidAppId EmptyCloseReason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_user_exit_closereason-lcm_13"></a>
### CloseApp_Empty_AppId_USER_EXIT_CloseReason (LCM_13)

**Objective:** Verify closeApp with empty appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_error_closereason-lcm_14"></a>
### CloseApp_Empty_AppId_ERROR_CloseReason (LCM_14)

**Objective:** Verify closeApp with empty appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_kill_and_run_closereason-lcm_15"></a>
### CloseApp_Empty_AppId_KILL_AND_RUN_CloseReason (LCM_15)

**Objective:** Verify closeApp with empty appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_kill_and_activate_closereason-lcm_16"></a>
### CloseApp_Empty_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_16)

**Objective:** Verify closeApp with empty appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_closeapp_empty_params-lcm_17"></a>
### LifecycleManager_CloseApp_Empty_Params (LCM_17)

**Objective:** Verify closeApp with empty appId and empty closeReason.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty Params | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`, `closeReason`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_without_parameters-lcm_18"></a>
### CloseApp_Without_Parameters (LCM_18)

**Objective:** Verify closeApp without any parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App No Params | Invoke `closeApp` on `org.rdk.LifecycleManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_user_exit_closereason-lcm_19"></a>
### CloseApp_Invalid_AppId_USER_EXIT_CloseReason (LCM_19)

**Objective:** Verify closeApp with invalid appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"InvalidAppID"`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_error_closereason-lcm_20"></a>
### CloseApp_Invalid_AppId_ERROR_CloseReason (LCM_20)

**Objective:** Verify closeApp with invalid appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"InvalidAppID"`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_kill_and_run_closereason-lcm_21"></a>
### CloseApp_Invalid_AppId_KILL_AND_RUN_CloseReason (LCM_21)

**Objective:** Verify closeApp with invalid appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"InvalidAppID"`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_kill_and_activate_closereason-lcm_22"></a>
### CloseApp_Invalid_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_22)

**Objective:** Verify closeApp with invalid appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"InvalidAppID"`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_user_exit_closereason-lcm_23"></a>
### CloseApp_Numeric_AppId_USER_EXIT_CloseReason (LCM_23)

**Objective:** Verify closeApp with numeric value for appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Numeric AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `12345`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_error_closereason-lcm_24"></a>
### CloseApp_Numeric_AppId_ERROR_CloseReason (LCM_24)

**Objective:** Verify closeApp with numeric value for appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Numeric AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `12345`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_kill_and_run_closereason-lcm_25"></a>
### CloseApp_Numeric_AppId_KILL_AND_RUN_CloseReason (LCM_25)

**Objective:** Verify closeApp with numeric value for appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Numeric AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `12345`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_kill_and_activate_closereason-lcm_26"></a>
### CloseApp_Numeric_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_26)

**Objective:** Verify closeApp with numeric value for appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Numeric AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `12345`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_user_exit_closereason-lcm_27"></a>
### CloseApp_Special_Char_AppId_USER_EXIT_CloseReason (LCM_27)

**Objective:** Verify closeApp with special character string as appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"!()*^"`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_error_closereason-lcm_28"></a>
### CloseApp_Special_Char_AppId_ERROR_CloseReason (LCM_28)

**Objective:** Verify closeApp with special character string as appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"!()*^"`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_kill_and_run_closereason-lcm_29"></a>
### CloseApp_Special_Char_AppId_KILL_AND_RUN_CloseReason (LCM_29)

**Objective:** Verify closeApp with special character string as appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"!()*^"`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_kill_and_activate_closereason-lcm_30"></a>
### CloseApp_Special_Char_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_30)

**Objective:** Verify closeApp with special character string as appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"!()*^"`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_user_exit_closereason-lcm_31"></a>
### CloseApp_Boolean_AppId_USER_EXIT_CloseReason (LCM_31)

**Objective:** Verify closeApp with boolean value for appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Boolean AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `true`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_error_closereason-lcm_32"></a>
### CloseApp_Boolean_AppId_ERROR_CloseReason (LCM_32)

**Objective:** Verify closeApp with boolean value for appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Boolean AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `true`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_kill_and_run_closereason-lcm_33"></a>
### CloseApp_Boolean_AppId_KILL_AND_RUN_CloseReason (LCM_33)

**Objective:** Verify closeApp with boolean value for appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Boolean AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `true`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_kill_and_activate_closereason-lcm_34"></a>
### CloseApp_Boolean_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_34)

**Objective:** Verify closeApp with boolean value for appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Boolean AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `true`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_user_exit_closereason-lcm_35"></a>
### CloseApp_Long_String_AppId_USER_EXIT_CloseReason (LCM_35)

**Objective:** Verify closeApp with very long string as appId and USER_EXIT closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Long String AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`, `closeReason`: `"USER_EXIT"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_error_closereason-lcm_36"></a>
### CloseApp_Long_String_AppId_ERROR_CloseReason (LCM_36)

**Objective:** Verify closeApp with very long string as appId and ERROR closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Long String AppId ERROR | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`, `closeReason`: `"ERROR"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_kill_and_run_closereason-lcm_37"></a>
### CloseApp_Long_String_AppId_KILL_AND_RUN_CloseReason (LCM_37)

**Objective:** Verify closeApp with very long string as appId and KILL_AND_RUN closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Long String AppId KILL AND RUN | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`, `closeReason`: `"KILL_AND_RUN"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_kill_and_activate_closereason-lcm_38"></a>
### CloseApp_Long_String_AppId_KILL_AND_ACTIVATE_CloseReason (LCM_38)

**Objective:** Verify closeApp with very long string as appId and KILL_AND_ACTIVATE closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Long String AppId KILL AND ACTIVATE | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`, `closeReason`: `"KILL_AND_ACTIVATE"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_numeric_closereason-lcm_39"></a>
### CloseApp_Valid_AppId_Numeric_CloseReason (LCM_39)

**Objective:** Verify closeApp with valid appId and numeric value for closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Numeric CloseReason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_special_char_closereason-lcm_40"></a>
### CloseApp_Valid_AppId_Special_Char_CloseReason (LCM_40)

**Objective:** Verify closeApp with valid appId and special character string as closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char CloseReason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `"!()*^"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "!()*^"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_boolean_closereason-lcm_41"></a>
### CloseApp_Valid_AppId_Boolean_CloseReason (LCM_41)

**Objective:** Verify closeApp with valid appId and boolean value for closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Boolean CloseReason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_long_string_closereason-lcm_42"></a>
### CloseApp_Valid_AppId_Long_String_CloseReason (LCM_42)

**Objective:** Verify closeApp with valid appId and very long string as closeReason

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Long String CloseReason | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `closeReason`: `"VeryLongStringForCloseReasonTestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "VeryLongStringForCloseReasonTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

---

## Post-conditions

### Post-condition 1: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check Package Info | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 4 | Uninstall Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |