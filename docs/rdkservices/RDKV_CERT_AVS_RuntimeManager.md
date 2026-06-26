## TestScript Name
RDKV_CERT_AVS_RuntimeManager

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Plugin Pre-conditions](#plugin-pre-conditions)
4. [Test Cases](#test-cases)
   - [RuntimeManager_GetInfo](#runtimemanager_getinfo)
   - [RuntimeManager_GetInfo_EmptyAppId](#runtimemanager_getinfo_emptyappid)
   - [RuntimeManager_GetInfo_InvalidAppId](#runtimemanager_getinfo_invalidappid)
   - [RuntimeManager_GetInfo_SpecialCharsAppId](#runtimemanager_getinfo_specialcharsappid)
   - [RuntimeManager_GetInfo_Without_Parameter](#runtimemanager_getinfo_without_parameter)
   - [RuntimeManager_GetInfo_NumericAppId](#runtimemanager_getinfo_numericappid)
   - [RuntimeManager_Annotate_ValidParameters](#runtimemanager_annotate_validparameters)
   - [RuntimeManager_Annotate_EmptyAppId](#runtimemanager_annotate_emptyappid)
   - [RuntimeManager_Annotate_InvalidAppId](#runtimemanager_annotate_invalidappid)
   - [RuntimeManager_Annotate_EmptyKey](#runtimemanager_annotate_emptykey)
   - [RuntimeManager_Annotate_InvalidKey](#runtimemanager_annotate_invalidkey)
   - [RuntimeManager_Annotate_SpecialCharsKey](#runtimemanager_annotate_specialcharskey)
   - [RuntimeManager_Annotate_EmptyValue](#runtimemanager_annotate_emptyvalue)
   - [RuntimeManager_Annotate_SpecialCharsValue](#runtimemanager_annotate_specialcharsvalue)
   - [RuntimeManager_Annotate_InvalidParameter](#runtimemanager_annotate_invalidparameter)
   - [RuntimeManager_Annotate_Without_Parameters](#runtimemanager_annotate_without_parameters)
   - [RuntimeManager_Hibernate_Application](#runtimemanager_hibernate_application)
   - [RuntimeManager_Hibernate_EmptyAppId](#runtimemanager_hibernate_emptyappid)
   - [RuntimeManager_Hibernate_InvalidAppId](#runtimemanager_hibernate_invalidappid)
   - [RuntimeManager_Hibernate_SpecialCharsAppId](#runtimemanager_hibernate_specialcharsappid)
   - [RuntimeManager_Hibernate_NumericAppId](#runtimemanager_hibernate_numericappid)
   - [RuntimeManager_Hibernate_Without_Parameter](#runtimemanager_hibernate_without_parameter)
   - [RuntimeManager_Suspend_Application](#runtimemanager_suspend_application)
   - [RuntimeManager_Suspend_EmptyAppId](#runtimemanager_suspend_emptyappid)
   - [RuntimeManager_Suspend_InvalidAppId](#runtimemanager_suspend_invalidappid)
   - [RuntimeManager_Suspend_SpecialCharsAppId](#runtimemanager_suspend_specialcharsappid)
   - [RuntimeManager_Suspend_NumericAppId](#runtimemanager_suspend_numericappid)
   - [RuntimeManager_Suspend_Without_Parameter](#runtimemanager_suspend_without_parameter)
   - [RuntimeManager_Resume_Application](#runtimemanager_resume_application)
   - [RuntimeManager_Resume_EmptyAppId](#runtimemanager_resume_emptyappid)
   - [RuntimeManager_Resume_InvalidAppId](#runtimemanager_resume_invalidappid)
   - [RuntimeManager_Resume_SpecialCharsAppId](#runtimemanager_resume_specialcharsappid)
   - [RuntimeManager_Resume_NumericAppId](#runtimemanager_resume_numericappid)
   - [RuntimeManager_Resume_Without_Parameter](#runtimemanager_resume_without_parameter)
   - [RuntimeManager_Wake_Application](#runtimemanager_wake_application)
   - [RuntimeManager_Wake_Application_Suspended_State](#runtimemanager_wake_application_suspended_state)
   - [RuntimeManager_Wake_EmptyAppId](#runtimemanager_wake_emptyappid)
   - [RuntimeManager_Wake_InvalidAppId](#runtimemanager_wake_invalidappid)
   - [RuntimeManager_Wake_SpecialCharsAppId](#runtimemanager_wake_specialcharsappid)
   - [RuntimeManager_Wake_NumericAppId](#runtimemanager_wake_numericappid)
   - [RuntimeManager_Wake_InvalidState](#runtimemanager_wake_invalidstate)
   - [RuntimeManager_Wake_EmptyState](#runtimemanager_wake_emptystate)
   - [RuntimeManager_Wake_Without_Parameters](#runtimemanager_wake_without_parameters)
   - [RuntimeManager_Wake_Without_State](#runtimemanager_wake_without_state)
5. [Plugin Post-conditions](#plugin-post-conditions)
6. [Test Attributes](#test-attributes)

## Objective

The **RuntimeManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.RuntimeManager` (version 1)

## APIs Under Test

| API | Description |
|-----|-------------|
| `annotate` | Annotates are sent to Dobby for recording |
| `getInfo` | Get info of the application |
| `hibernate` | Hibernate the application |
| `resume` | Resume the application |
| `suspend` | Suspend the application |
| `wake` | Wake the application |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Activate_DownloadManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DownloadManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 4: Activate_AppManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 5: Activate_RuntimeManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of RuntimeManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RuntimeManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate RuntimeManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RuntimeManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of RuntimeManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RuntimeManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 6: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 7: Launch_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

## Test Cases

<a id="runtimemanager_getinfo"></a>
### TestCase Name
RuntimeManager_GetInfo

### TestCase ID
RTM_01

### TestCase Objective
Check whether getInfo method returns non-empty result

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Get Application Info | Invoke getInfo on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call should succeed and return a non-empty result |

---

<a id="runtimemanager_getinfo_emptyappid"></a>
### TestCase Name
RuntimeManager_GetInfo_EmptyAppId

### TestCase ID
RTM_02

### TestCase Objective
Test getInfo method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Empty AppId | Invoke getInfo on org.rdk.RuntimeManager with appInstanceId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_invalidappid"></a>
### TestCase Name
RuntimeManager_GetInfo_InvalidAppId

### TestCase ID
RTM_03

### TestCase Objective
Test getInfo method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Invalid AppId | Invoke getInfo on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_specialcharsappid"></a>
### TestCase Name
RuntimeManager_GetInfo_SpecialCharsAppId

### TestCase ID
RTM_04

### TestCase Objective
Test getInfo method with special characters in appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info SpecialChars AppId | Invoke getInfo on org.rdk.RuntimeManager with appInstanceId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_without_parameter"></a>
### TestCase Name
RuntimeManager_GetInfo_Without_Parameter

### TestCase ID
RTM_05

### TestCase Objective
Test getInfo method without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Without Parameter | Invoke getInfo on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_getinfo_numericappid"></a>
### TestCase Name
RuntimeManager_GetInfo_NumericAppId

### TestCase ID
RTM_06

### TestCase Objective
Test getInfo method with numeric only appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Info Numeric AppId | Invoke getInfo on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.getInfo", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_validparameters"></a>
### TestCase Name
RuntimeManager_Annotate_ValidParameters

### TestCase ID
RTM_07

### TestCase Objective
Test annotate method with valid parameters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Valid Params | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "testKey", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_annotate_emptyappid"></a>
### TestCase Name
RuntimeManager_Annotate_EmptyAppId

### TestCase ID
RTM_08

### TestCase Objective
Test annotate method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Empty AppId | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "", key: "testKey", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidappid"></a>
### TestCase Name
RuntimeManager_Annotate_InvalidAppId

### TestCase ID
RTM_09

### TestCase Objective
Test annotate method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Invalid AppId | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id", key: "testKey", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "invalid_app_id", "key": "testKey", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_emptykey"></a>
### TestCase Name
RuntimeManager_Annotate_EmptyKey

### TestCase ID
RTM_10

### TestCase Objective
Test annotate method with empty key parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Empty Key | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidkey"></a>
### TestCase Name
RuntimeManager_Annotate_InvalidKey

### TestCase ID
RTM_11

### TestCase Objective
Test annotate method with invalid key parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Invalid Key | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "invalid_key", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "invalid_key", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_specialcharskey"></a>
### TestCase Name
RuntimeManager_Annotate_SpecialCharsKey

### TestCase ID
RTM_12

### TestCase Objective
Test annotate method with special characters in key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application SpecialChars Key | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "()^*!", value: "testValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "()^*!", "value": "testValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_emptyvalue"></a>
### TestCase Name
RuntimeManager_Annotate_EmptyValue

### TestCase ID
RTM_13

### TestCase Objective
Test annotate method with empty value parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Empty Value | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "testKey", value: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_specialcharsvalue"></a>
### TestCase Name
RuntimeManager_Annotate_SpecialCharsValue

### TestCase ID
RTM_14

### TestCase Objective
Test annotate method with special characters in value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application SpecialChars Value | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "testKey", value: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "value": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_invalidparameter"></a>
### TestCase Name
RuntimeManager_Annotate_InvalidParameter

### TestCase ID
RTM_15

### TestCase Objective
Test annotate method with invalid parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Annotate Application Invalid Parameter | Invoke annotate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", key: "testKey", invalidParam: "invalidValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate", "params": {"appInstanceId": "<result_step_1>", "key": "testKey", "invalidParam": "invalidValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_annotate_without_parameters"></a>
### TestCase Name
RuntimeManager_Annotate_Without_Parameters

### TestCase ID
RTM_16

### TestCase Objective
Test annotate method without parameters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Annotate Application Without Parameters | Invoke annotate on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.annotate"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_application"></a>
### TestCase Name
RuntimeManager_Hibernate_Application

### TestCase ID
RTM_17

### TestCase Objective
Test hibernate method with valid appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Hibernate Application | Invoke hibernate on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_hibernate_emptyappid"></a>
### TestCase Name
RuntimeManager_Hibernate_EmptyAppId

### TestCase ID
RTM_18

### TestCase Objective
Test hibernate method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Empty AppId | Invoke hibernate on org.rdk.RuntimeManager with appInstanceId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_invalidappid"></a>
### TestCase Name
RuntimeManager_Hibernate_InvalidAppId

### TestCase ID
RTM_19

### TestCase Objective
Test hibernate method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Invalid AppId | Invoke hibernate on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_specialcharsappid"></a>
### TestCase Name
RuntimeManager_Hibernate_SpecialCharsAppId

### TestCase ID
RTM_20

### TestCase Objective
Test hibernate method with special characters in appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application SpecialChars AppId | Invoke hibernate on org.rdk.RuntimeManager with appInstanceId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_numericappid"></a>
### TestCase Name
RuntimeManager_Hibernate_NumericAppId

### TestCase ID
RTM_21

### TestCase Objective
Test hibernate method with numeric only appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Numeric AppId | Invoke hibernate on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_hibernate_without_parameter"></a>
### TestCase Name
RuntimeManager_Hibernate_Without_Parameter

### TestCase ID
RTM_22

### TestCase Objective
Test hibernate method without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate Application Without Parameter | Invoke hibernate on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.hibernate"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_application"></a>
### TestCase Name
RuntimeManager_Suspend_Application

### TestCase ID
RTM_23

### TestCase Objective
Test suspend method with valid appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Suspend Application | Invoke suspend on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_suspend_emptyappid"></a>
### TestCase Name
RuntimeManager_Suspend_EmptyAppId

### TestCase ID
RTM_24

### TestCase Objective
Test suspend method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Empty AppId | Invoke suspend on org.rdk.RuntimeManager with appInstanceId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_invalidappid"></a>
### TestCase Name
RuntimeManager_Suspend_InvalidAppId

### TestCase ID
RTM_25

### TestCase Objective
Test suspend method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Invalid AppId | Invoke suspend on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_specialcharsappid"></a>
### TestCase Name
RuntimeManager_Suspend_SpecialCharsAppId

### TestCase ID
RTM_26

### TestCase Objective
Test suspend method with special characters in appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application SpecialChars AppId | Invoke suspend on org.rdk.RuntimeManager with appInstanceId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_numericappid"></a>
### TestCase Name
RuntimeManager_Suspend_NumericAppId

### TestCase ID
RTM_27

### TestCase Objective
Test suspend method with numeric only appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Numeric AppId | Invoke suspend on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_suspend_without_parameter"></a>
### TestCase Name
RuntimeManager_Suspend_Without_Parameter

### TestCase ID
RTM_28

### TestCase Objective
Test suspend method without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Suspend Application Without Parameter | Invoke suspend on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.suspend"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_application"></a>
### TestCase Name
RuntimeManager_Resume_Application

### TestCase ID
RTM_29

### TestCase Objective
Test resume method with valid appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Resume Application | Invoke resume on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_resume_emptyappid"></a>
### TestCase Name
RuntimeManager_Resume_EmptyAppId

### TestCase ID
RTM_30

### TestCase Objective
Test resume method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Empty AppId | Invoke resume on org.rdk.RuntimeManager with appInstanceId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_invalidappid"></a>
### TestCase Name
RuntimeManager_Resume_InvalidAppId

### TestCase ID
RTM_31

### TestCase Objective
Test resume method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Invalid AppId | Invoke resume on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "invalid_app_id"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_specialcharsappid"></a>
### TestCase Name
RuntimeManager_Resume_SpecialCharsAppId

### TestCase ID
RTM_32

### TestCase Objective
Test resume method with special characters in appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application SpecialChars AppId | Invoke resume on org.rdk.RuntimeManager with appInstanceId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_numericappid"></a>
### TestCase Name
RuntimeManager_Resume_NumericAppId

### TestCase ID
RTM_33

### TestCase Objective
Test resume method with numeric only appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Numeric AppId | Invoke resume on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume", "params": {"appInstanceId": 123456789}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_resume_without_parameter"></a>
### TestCase Name
RuntimeManager_Resume_Without_Parameter

### TestCase ID
RTM_34

### TestCase Objective
Test resume method without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Resume Application Without Parameter | Invoke resume on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.resume"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_application"></a>
### TestCase Name
RuntimeManager_Wake_Application

### TestCase ID
RTM_35

### TestCase Objective
Test wake method with valid appInstanceId and running state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Running State | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", state: "running"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_wake_application_suspended_state"></a>
### TestCase Name
RuntimeManager_Wake_Application_Suspended_State

### TestCase ID
RTM_36

### TestCase Objective
Test wake method with valid appInstanceId and suspended state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Suspended State | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", state: "suspended"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "suspended"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="runtimemanager_wake_emptyappid"></a>
### TestCase Name
RuntimeManager_Wake_EmptyAppId

### TestCase ID
RTM_37

### TestCase Objective
Test wake method with empty appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Empty AppId | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "", state: "running"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_invalidappid"></a>
### TestCase Name
RuntimeManager_Wake_InvalidAppId

### TestCase ID
RTM_38

### TestCase Objective
Test wake method with invalid appInstanceId parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Invalid AppId | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "invalid_app_id", state: "running"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "invalid_app_id", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_specialcharsappid"></a>
### TestCase Name
RuntimeManager_Wake_SpecialCharsAppId

### TestCase ID
RTM_39

### TestCase Objective
Test wake method with special characters in appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application SpecialChars AppId | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "()^*!", state: "running"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "()^*!", "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_numericappid"></a>
### TestCase Name
RuntimeManager_Wake_NumericAppId

### TestCase ID
RTM_40

### TestCase Objective
Test wake method with numeric only appInstanceId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Numeric AppId | Invoke wake on org.rdk.RuntimeManager with state: "running"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": 123456789, "state": "running"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_invalidstate"></a>
### TestCase Name
RuntimeManager_Wake_InvalidState

### TestCase ID
RTM_41

### TestCase Objective
Test wake method with invalid state parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Invalid State | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", state: "invalid_state"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": "invalid_state"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_emptystate"></a>
### TestCase Name
RuntimeManager_Wake_EmptyState

### TestCase ID
RTM_42

### TestCase Objective
Test wake method with empty state parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Empty State | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>", state: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>", "state": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_without_parameters"></a>
### TestCase Name
RuntimeManager_Wake_Without_Parameters

### TestCase ID
RTM_43

### TestCase Objective
Test wake method without parameters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Wake Application Without Parameters | Invoke wake on org.rdk.RuntimeManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="runtimemanager_wake_without_state"></a>
### TestCase Name
RuntimeManager_Wake_Without_State

### TestCase ID
RTM_44

### TestCase Objective
Test wake method without state parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Wake Application Without State | Invoke wake on org.rdk.RuntimeManager with appInstanceId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RuntimeManager.1.wake", "params": {"appInstanceId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check Package Info | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |
