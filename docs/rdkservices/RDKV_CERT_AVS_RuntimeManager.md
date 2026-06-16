## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [RuntimeManager_GetInfo (RTM_01)](#runtimemanager_getinfo-rtm_01)
   - [RuntimeManager_GetInfo_EmptyAppId (RTM_02)](#runtimemanager_getinfo_emptyappid-rtm_02)
   - [RuntimeManager_GetInfo_InvalidAppId (RTM_03)](#runtimemanager_getinfo_invalidappid-rtm_03)
   - [RuntimeManager_GetInfo_SpecialCharsAppId (RTM_04)](#runtimemanager_getinfo_specialcharsappid-rtm_04)
   - [RuntimeManager_GetInfo_Without_Parameter (RTM_05)](#runtimemanager_getinfo_without_parameter-rtm_05)
   - [RuntimeManager_GetInfo_NumericAppId (RTM_06)](#runtimemanager_getinfo_numericappid-rtm_06)
   - [RuntimeManager_Annotate_ValidParameters (RTM_07)](#runtimemanager_annotate_validparameters-rtm_07)
   - [RuntimeManager_Annotate_EmptyAppId (RTM_08)](#runtimemanager_annotate_emptyappid-rtm_08)
   - [RuntimeManager_Annotate_InvalidAppId (RTM_09)](#runtimemanager_annotate_invalidappid-rtm_09)
   - [RuntimeManager_Annotate_EmptyKey (RTM_10)](#runtimemanager_annotate_emptykey-rtm_10)
   - [RuntimeManager_Annotate_InvalidKey (RTM_11)](#runtimemanager_annotate_invalidkey-rtm_11)
   - [RuntimeManager_Annotate_SpecialCharsKey (RTM_12)](#runtimemanager_annotate_specialcharskey-rtm_12)
   - [RuntimeManager_Annotate_EmptyValue (RTM_13)](#runtimemanager_annotate_emptyvalue-rtm_13)
   - [RuntimeManager_Annotate_SpecialCharsValue (RTM_14)](#runtimemanager_annotate_specialcharsvalue-rtm_14)
   - [RuntimeManager_Annotate_InvalidParameter (RTM_15)](#runtimemanager_annotate_invalidparameter-rtm_15)
   - [RuntimeManager_Annotate_Without_Parameters (RTM_16)](#runtimemanager_annotate_without_parameters-rtm_16)
   - [RuntimeManager_Hibernate_Application (RTM_17)](#runtimemanager_hibernate_application-rtm_17)
   - [RuntimeManager_Hibernate_EmptyAppId (RTM_18)](#runtimemanager_hibernate_emptyappid-rtm_18)
   - [RuntimeManager_Hibernate_InvalidAppId (RTM_19)](#runtimemanager_hibernate_invalidappid-rtm_19)
   - [RuntimeManager_Hibernate_SpecialCharsAppId (RTM_20)](#runtimemanager_hibernate_specialcharsappid-rtm_20)
   - [RuntimeManager_Hibernate_NumericAppId (RTM_21)](#runtimemanager_hibernate_numericappid-rtm_21)
   - [RuntimeManager_Hibernate_Without_Parameter (RTM_22)](#runtimemanager_hibernate_without_parameter-rtm_22)
   - [RuntimeManager_Suspend_Application (RTM_23)](#runtimemanager_suspend_application-rtm_23)
   - [RuntimeManager_Suspend_EmptyAppId (RTM_24)](#runtimemanager_suspend_emptyappid-rtm_24)
   - [RuntimeManager_Suspend_InvalidAppId (RTM_25)](#runtimemanager_suspend_invalidappid-rtm_25)
   - [RuntimeManager_Suspend_SpecialCharsAppId (RTM_26)](#runtimemanager_suspend_specialcharsappid-rtm_26)
   - [RuntimeManager_Suspend_NumericAppId (RTM_27)](#runtimemanager_suspend_numericappid-rtm_27)
   - [RuntimeManager_Suspend_Without_Parameter (RTM_28)](#runtimemanager_suspend_without_parameter-rtm_28)
   - [RuntimeManager_Resume_Application (RTM_29)](#runtimemanager_resume_application-rtm_29)
   - [RuntimeManager_Resume_EmptyAppId (RTM_30)](#runtimemanager_resume_emptyappid-rtm_30)
   - [RuntimeManager_Resume_InvalidAppId (RTM_31)](#runtimemanager_resume_invalidappid-rtm_31)
   - [RuntimeManager_Resume_SpecialCharsAppId (RTM_32)](#runtimemanager_resume_specialcharsappid-rtm_32)
   - [RuntimeManager_Resume_NumericAppId (RTM_33)](#runtimemanager_resume_numericappid-rtm_33)
   - [RuntimeManager_Resume_Without_Parameter (RTM_34)](#runtimemanager_resume_without_parameter-rtm_34)
   - [RuntimeManager_Wake_Application (RTM_35)](#runtimemanager_wake_application-rtm_35)
   - [RuntimeManager_Wake_Application_Suspended_State (RTM_36)](#runtimemanager_wake_application_suspended_state-rtm_36)
   - [RuntimeManager_Wake_EmptyAppId (RTM_37)](#runtimemanager_wake_emptyappid-rtm_37)
   - [RuntimeManager_Wake_InvalidAppId (RTM_38)](#runtimemanager_wake_invalidappid-rtm_38)
   - [RuntimeManager_Wake_SpecialCharsAppId (RTM_39)](#runtimemanager_wake_specialcharsappid-rtm_39)
   - [RuntimeManager_Wake_NumericAppId (RTM_40)](#runtimemanager_wake_numericappid-rtm_40)
   - [RuntimeManager_Wake_InvalidState (RTM_41)](#runtimemanager_wake_invalidstate-rtm_41)
   - [RuntimeManager_Wake_EmptyState (RTM_42)](#runtimemanager_wake_emptystate-rtm_42)
   - [RuntimeManager_Wake_Without_Parameters (RTM_43)](#runtimemanager_wake_without_parameters-rtm_43)
   - [RuntimeManager_Wake_Without_State (RTM_44)](#runtimemanager_wake_without_state-rtm_44)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **RuntimeManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.RuntimeManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getInfo`
- **Lifecycle / Control APIs**: `hibernate`, `resume`, `suspend`
- **Other APIs**: `annotate`, `wake`

### APIs Under Test

| API | Description |
|-----|-------------|
| `annotate` | Annotates are sent to Dobby for recording |
| `getInfo` | Get info of the application |
| `hibernate` | Hibernate the application |
| `resume` | Resume the application |
| `suspend` | Suspend the application |
| `wake` | Wake the application |

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

### Pre-condition 5: Activate_RuntimeManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RuntimeManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.RuntimeManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RuntimeManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RuntimeManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 6: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_4>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

### Pre-condition 7: Launch_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

---

## Test Cases

<a id="runtimemanager_getinfo-rtm_01"></a>
### RuntimeManager_GetInfo (RTM_01)

**Objective:** Check whether getInfo method returns non-empty result

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Get Application Info | Invoke `getInfo` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call should succeed and return a non-empty result |

---

<a id="runtimemanager_getinfo_emptyappid-rtm_02"></a>
### RuntimeManager_GetInfo_EmptyAppId (RTM_02)

**Objective:** Test getInfo method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Empty AppId | Invoke `getInfo` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_invalidappid-rtm_03"></a>
### RuntimeManager_GetInfo_InvalidAppId (RTM_03)

**Objective:** Test getInfo method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Invalid AppId | Invoke `getInfo` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_specialcharsappid-rtm_04"></a>
### RuntimeManager_GetInfo_SpecialCharsAppId (RTM_04)

**Objective:** Test getInfo method with special characters in appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info SpecialChars AppId | Invoke `getInfo` on `org.rdk.RuntimeManager` with `appInstanceId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_without_parameter-rtm_05"></a>
### RuntimeManager_GetInfo_Without_Parameter (RTM_05)

**Objective:** Test getInfo method without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Without Parameter | Invoke `getInfo` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_numericappid-rtm_06"></a>
### RuntimeManager_GetInfo_NumericAppId (RTM_06)

**Objective:** Test getInfo method with numeric only appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Numeric AppId | Invoke `getInfo` on `org.rdk.RuntimeManager` with `appInstanceId`: `123456789`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_validparameters-rtm_07"></a>
### RuntimeManager_Annotate_ValidParameters (RTM_07)

**Objective:** Test annotate method with valid parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Valid Params | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"testKey"`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_annotate_emptyappid-rtm_08"></a>
### RuntimeManager_Annotate_EmptyAppId (RTM_08)

**Objective:** Test annotate method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Empty AppId | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`, `key`: `"testKey"`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidappid-rtm_09"></a>
### RuntimeManager_Annotate_InvalidAppId (RTM_09)

**Objective:** Test annotate method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Invalid AppId | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`, `key`: `"testKey"`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "invalid_app_id", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_emptykey-rtm_10"></a>
### RuntimeManager_Annotate_EmptyKey (RTM_10)

**Objective:** Test annotate method with empty key parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Empty Key | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `""`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidkey-rtm_11"></a>
### RuntimeManager_Annotate_InvalidKey (RTM_11)

**Objective:** Test annotate method with invalid key parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Invalid Key | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"invalid_key"`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "invalid_key", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_specialcharskey-rtm_12"></a>
### RuntimeManager_Annotate_SpecialCharsKey (RTM_12)

**Objective:** Test annotate method with special characters in key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application SpecialChars Key | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"()^*!"`, `value`: `"testValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "()^*!", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_emptyvalue-rtm_13"></a>
### RuntimeManager_Annotate_EmptyValue (RTM_13)

**Objective:** Test annotate method with empty value parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Empty Value | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"testKey"`, `value`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_specialcharsvalue-rtm_14"></a>
### RuntimeManager_Annotate_SpecialCharsValue (RTM_14)

**Objective:** Test annotate method with special characters in value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application SpecialChars Value | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"testKey"`, `value`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidparameter-rtm_15"></a>
### RuntimeManager_Annotate_InvalidParameter (RTM_15)

**Objective:** Test annotate method with invalid parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Invalid Parameter | Invoke `annotate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `key`: `"testKey"`, `invalidParam`: `"invalidValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "invalidParam": "invalidValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_without_parameters-rtm_16"></a>
### RuntimeManager_Annotate_Without_Parameters (RTM_16)

**Objective:** Test annotate method without parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Without Parameters | Invoke `annotate` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_application-rtm_17"></a>
### RuntimeManager_Hibernate_Application (RTM_17)

**Objective:** Test hibernate method with valid appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Hibernate Application | Invoke `hibernate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_hibernate_emptyappid-rtm_18"></a>
### RuntimeManager_Hibernate_EmptyAppId (RTM_18)

**Objective:** Test hibernate method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Empty AppId | Invoke `hibernate` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_invalidappid-rtm_19"></a>
### RuntimeManager_Hibernate_InvalidAppId (RTM_19)

**Objective:** Test hibernate method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Invalid AppId | Invoke `hibernate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_specialcharsappid-rtm_20"></a>
### RuntimeManager_Hibernate_SpecialCharsAppId (RTM_20)

**Objective:** Test hibernate method with special characters in appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application SpecialChars AppId | Invoke `hibernate` on `org.rdk.RuntimeManager` with `appInstanceId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_numericappid-rtm_21"></a>
### RuntimeManager_Hibernate_NumericAppId (RTM_21)

**Objective:** Test hibernate method with numeric only appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Numeric AppId | Invoke `hibernate` on `org.rdk.RuntimeManager` with `appInstanceId`: `123456789`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_without_parameter-rtm_22"></a>
### RuntimeManager_Hibernate_Without_Parameter (RTM_22)

**Objective:** Test hibernate method without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Without Parameter | Invoke `hibernate` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_application-rtm_23"></a>
### RuntimeManager_Suspend_Application (RTM_23)

**Objective:** Test suspend method with valid appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Suspend Application | Invoke `suspend` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_suspend_emptyappid-rtm_24"></a>
### RuntimeManager_Suspend_EmptyAppId (RTM_24)

**Objective:** Test suspend method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Empty AppId | Invoke `suspend` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_invalidappid-rtm_25"></a>
### RuntimeManager_Suspend_InvalidAppId (RTM_25)

**Objective:** Test suspend method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Invalid AppId | Invoke `suspend` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_specialcharsappid-rtm_26"></a>
### RuntimeManager_Suspend_SpecialCharsAppId (RTM_26)

**Objective:** Test suspend method with special characters in appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application SpecialChars AppId | Invoke `suspend` on `org.rdk.RuntimeManager` with `appInstanceId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_numericappid-rtm_27"></a>
### RuntimeManager_Suspend_NumericAppId (RTM_27)

**Objective:** Test suspend method with numeric only appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Numeric AppId | Invoke `suspend` on `org.rdk.RuntimeManager` with `appInstanceId`: `123456789`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_without_parameter-rtm_28"></a>
### RuntimeManager_Suspend_Without_Parameter (RTM_28)

**Objective:** Test suspend method without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Without Parameter | Invoke `suspend` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_application-rtm_29"></a>
### RuntimeManager_Resume_Application (RTM_29)

**Objective:** Test resume method with valid appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Resume Application | Invoke `resume` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_resume_emptyappid-rtm_30"></a>
### RuntimeManager_Resume_EmptyAppId (RTM_30)

**Objective:** Test resume method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Empty AppId | Invoke `resume` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_invalidappid-rtm_31"></a>
### RuntimeManager_Resume_InvalidAppId (RTM_31)

**Objective:** Test resume method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Invalid AppId | Invoke `resume` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_specialcharsappid-rtm_32"></a>
### RuntimeManager_Resume_SpecialCharsAppId (RTM_32)

**Objective:** Test resume method with special characters in appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application SpecialChars AppId | Invoke `resume` on `org.rdk.RuntimeManager` with `appInstanceId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_numericappid-rtm_33"></a>
### RuntimeManager_Resume_NumericAppId (RTM_33)

**Objective:** Test resume method with numeric only appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Numeric AppId | Invoke `resume` on `org.rdk.RuntimeManager` with `appInstanceId`: `123456789`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_without_parameter-rtm_34"></a>
### RuntimeManager_Resume_Without_Parameter (RTM_34)

**Objective:** Test resume method without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Without Parameter | Invoke `resume` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_application-rtm_35"></a>
### RuntimeManager_Wake_Application (RTM_35)

**Objective:** Test wake method with valid appInstanceId and running state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Running State | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `state`: `"running"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_wake_application_suspended_state-rtm_36"></a>
### RuntimeManager_Wake_Application_Suspended_State (RTM_36)

**Objective:** Test wake method with valid appInstanceId and suspended state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Suspended State | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `state`: `"suspended"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "suspended"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="runtimemanager_wake_emptyappid-rtm_37"></a>
### RuntimeManager_Wake_EmptyAppId (RTM_37)

**Objective:** Test wake method with empty appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Empty AppId | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `""`, `state`: `"running"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_invalidappid-rtm_38"></a>
### RuntimeManager_Wake_InvalidAppId (RTM_38)

**Objective:** Test wake method with invalid appInstanceId parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Invalid AppId | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"invalid_app_id"`, `state`: `"running"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "invalid_app_id", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_specialcharsappid-rtm_39"></a>
### RuntimeManager_Wake_SpecialCharsAppId (RTM_39)

**Objective:** Test wake method with special characters in appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application SpecialChars AppId | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"()^*!"`, `state`: `"running"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "()^*!", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_numericappid-rtm_40"></a>
### RuntimeManager_Wake_NumericAppId (RTM_40)

**Objective:** Test wake method with numeric only appInstanceId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Numeric AppId | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `123456789`, `state`: `"running"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": 123456789, "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_invalidstate-rtm_41"></a>
### RuntimeManager_Wake_InvalidState (RTM_41)

**Objective:** Test wake method with invalid state parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Invalid State | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `state`: `"invalid_state"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "invalid_state"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_emptystate-rtm_42"></a>
### RuntimeManager_Wake_EmptyState (RTM_42)

**Objective:** Test wake method with empty state parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Empty State | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`, `state`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_without_parameters-rtm_43"></a>
### RuntimeManager_Wake_Without_Parameters (RTM_43)

**Objective:** Test wake method without parameters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Without Parameters | Invoke `wake` on `org.rdk.RuntimeManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_without_state-rtm_44"></a>
### RuntimeManager_Wake_Without_State (RTM_44)

**Objective:** Test wake method without state parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Without State | Invoke `wake` on `org.rdk.RuntimeManager` with `appInstanceId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

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