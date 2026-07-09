## TestScript Name
RDKV_CERT_AVS_LifecycleManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [Verify_AppReady_Valid_AppId](#verify_appready_valid_appid)
   - [Verify_AppReady_Empty_AppId](#verify_appready_empty_appid)
   - [Verify_AppReady_Numeric_AppId](#verify_appready_numeric_appid)
   - [Verify_AppReady_Special_Char_AppId](#verify_appready_special_char_appid)
   - [Verify_AppReady_Long_String_AppId](#verify_appready_long_string_appid)
   - [LifecycleManager_Verify_AppReady_Boolean_AppId](#lifecyclemanager_verify_appready_boolean_appid)
   - [LifecycleManager_Verify_AppReady_Without_Parameters](#lifecyclemanager_verify_appready_without_parameters)
   - [CloseApp_Valid_AppId_USER_EXIT_CloseReason](#closeapp_valid_appid_user_exit_closereason)
   - [CloseApp_Valid_AppId_ERROR_CloseReason](#closeapp_valid_appid_error_closereason)
   - [CloseApp_ValidAppId_EmptyCloseReason](#closeapp_validappid_emptyclosereason)
   - [CloseApp_Empty_AppId_USER_EXIT_CloseReason](#closeapp_empty_appid_user_exit_closereason)
   - [CloseApp_Empty_AppId_ERROR_CloseReason](#closeapp_empty_appid_error_closereason)
   - [CloseApp_Empty_AppId_KILL_AND_RUN_CloseReason](#closeapp_empty_appid_kill_and_run_closereason)
   - [CloseApp_Empty_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_empty_appid_kill_and_activate_closereason)
   - [LifecycleManager_CloseApp_Empty_Params](#lifecyclemanager_closeapp_empty_params)
   - [CloseApp_Without_Parameters](#closeapp_without_parameters)
   - [CloseApp_Invalid_AppId_USER_EXIT_CloseReason](#closeapp_invalid_appid_user_exit_closereason)
   - [CloseApp_Invalid_AppId_ERROR_CloseReason](#closeapp_invalid_appid_error_closereason)
   - [CloseApp_Invalid_AppId_KILL_AND_RUN_CloseReason](#closeapp_invalid_appid_kill_and_run_closereason)
   - [CloseApp_Invalid_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_invalid_appid_kill_and_activate_closereason)
   - [CloseApp_Numeric_AppId_USER_EXIT_CloseReason](#closeapp_numeric_appid_user_exit_closereason)
   - [CloseApp_Numeric_AppId_ERROR_CloseReason](#closeapp_numeric_appid_error_closereason)
   - [CloseApp_Numeric_AppId_KILL_AND_RUN_CloseReason](#closeapp_numeric_appid_kill_and_run_closereason)
   - [CloseApp_Numeric_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_numeric_appid_kill_and_activate_closereason)
   - [CloseApp_Special_Char_AppId_USER_EXIT_CloseReason](#closeapp_special_char_appid_user_exit_closereason)
   - [CloseApp_Special_Char_AppId_ERROR_CloseReason](#closeapp_special_char_appid_error_closereason)
   - [CloseApp_Special_Char_AppId_KILL_AND_RUN_CloseReason](#closeapp_special_char_appid_kill_and_run_closereason)
   - [CloseApp_Special_Char_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_special_char_appid_kill_and_activate_closereason)
   - [CloseApp_Boolean_AppId_USER_EXIT_CloseReason](#closeapp_boolean_appid_user_exit_closereason)
   - [CloseApp_Boolean_AppId_ERROR_CloseReason](#closeapp_boolean_appid_error_closereason)
   - [CloseApp_Boolean_AppId_KILL_AND_RUN_CloseReason](#closeapp_boolean_appid_kill_and_run_closereason)
   - [CloseApp_Boolean_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_boolean_appid_kill_and_activate_closereason)
   - [CloseApp_Long_String_AppId_USER_EXIT_CloseReason](#closeapp_long_string_appid_user_exit_closereason)
   - [CloseApp_Long_String_AppId_ERROR_CloseReason](#closeapp_long_string_appid_error_closereason)
   - [CloseApp_Long_String_AppId_KILL_AND_RUN_CloseReason](#closeapp_long_string_appid_kill_and_run_closereason)
   - [CloseApp_Long_String_AppId_KILL_AND_ACTIVATE_CloseReason](#closeapp_long_string_appid_kill_and_activate_closereason)
   - [CloseApp_Valid_AppId_Numeric_CloseReason](#closeapp_valid_appid_numeric_closereason)
   - [CloseApp_Valid_AppId_Special_Char_CloseReason](#closeapp_valid_appid_special_char_closereason)
   - [CloseApp_Valid_AppId_Boolean_CloseReason](#closeapp_valid_appid_boolean_closereason)
   - [CloseApp_Valid_AppId_Long_String_CloseReason](#closeapp_valid_appid_long_string_closereason)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **LifecycleManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.LifecycleManager` (version 1)

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

### Plugin Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 4: Activate_AppManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of AppManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 5: Activate_LifecycleManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of LifecycleManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.LifecycleManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate LifecycleManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.LifecycleManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of LifecycleManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.LifecycleManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 6: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 7: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Packagemanager Application Name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure Packagemanager Application Version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure Packagemanager Application Hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure Packagemanager Additionalmetadata Name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure Packagemanager Additionalmetadata Value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure Packagemanager Application MD5 Checksum Value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="verify_appready_valid_appid"></a>
### TestCase Name
Verify_AppReady_Valid_AppId

### TestCase ID
LCM_01

### TestCase Objective
Verify appReady with a valid appId string

### TestCase Pre-condition

#### TestCase Pre-condition 1: Launch_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Launch App Valid Params | *(Conditional statement executed only if package/app is currently present)*<br>Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | *(Conditional statement executed only if package/app is currently present)*<br>Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady | Invoke appReady on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="verify_appready_empty_appid"></a>
### TestCase Name
Verify_AppReady_Empty_AppId

### TestCase ID
LCM_02

### TestCase Objective
Verify appReady with an empty appId string

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady | Invoke appReady on org.rdk.LifecycleManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_numeric_appid"></a>
### TestCase Name
Verify_AppReady_Numeric_AppId

### TestCase ID
LCM_03

### TestCase Objective
Verify appReady with a numeric value for appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady | Invoke appReady on org.rdk.LifecycleManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_special_char_appid"></a>
### TestCase Name
Verify_AppReady_Special_Char_AppId

### TestCase ID
LCM_04

### TestCase Objective
Verify appReady with a special character string as appId.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady Special Char | Invoke appReady on org.rdk.LifecycleManager with appId: "!()*^"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "!()*^"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="verify_appready_long_string_appid"></a>
### TestCase Name
Verify_AppReady_Long_String_AppId

### TestCase ID
LCM_05

### TestCase Objective
Verify appReady with a very long string as appId.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady Long String | Invoke appReady on org.rdk.LifecycleManager with appId: "VeryLongStringForAppIdTestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": "VeryLongStringForAppIdTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_verify_appready_boolean_appid"></a>
### TestCase Name
LifecycleManager_Verify_AppReady_Boolean_AppId

### TestCase ID
LCM_06

### TestCase Objective
Verify appReady with a boolean value for appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady Boolean AppId | Invoke appReady on org.rdk.LifecycleManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady", "params": {"appId": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_verify_appready_without_parameters"></a>
### TestCase Name
LifecycleManager_Verify_AppReady_Without_Parameters

### TestCase ID
LCM_07

### TestCase Objective
Verify appReady without any parameters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify AppReady No Params | Invoke appReady on org.rdk.LifecycleManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.appReady"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_08

### TestCase Objective
Verify closeApp with valid appId and USER_EXIT closeReason

### TestCase Pre-condition

#### TestCase Pre-condition 1: Launch_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Launch App Valid Params | *(Conditional statement executed only if package/app is currently present)*<br>Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | *(Conditional statement executed only if package/app is currently present)*<br>Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Valid Params | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="closeapp_valid_appid_error_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_ERROR_CloseReason

### TestCase ID
LCM_09

### TestCase Objective
Verify closeApp with valid appId and ERROR closeReason

### TestCase Pre-condition

#### TestCase Pre-condition 1: Launch_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Launch App Valid Params | *(Conditional statement executed only if package/app is currently present)*<br>Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | *(Conditional statement executed only if package/app is currently present)*<br>Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App ERROR Reason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="closeapp_validappid_emptyclosereason"></a>
### TestCase Name
CloseApp_ValidAppId_EmptyCloseReason

### TestCase ID
LCM_12

### TestCase Objective
Verify closeApp with valid appId and empty closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App ValidAppId EmptyCloseReason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", closeReason: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Empty_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_13

### TestCase Objective
Verify closeApp with empty appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Empty AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "", closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_error_closereason"></a>
### TestCase Name
CloseApp_Empty_AppId_ERROR_CloseReason

### TestCase ID
LCM_14

### TestCase Objective
Verify closeApp with empty appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Empty AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with appId: "", closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Empty_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_15

### TestCase Objective
Verify closeApp with empty appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Empty AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with appId: "", closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_empty_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Empty_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_16

### TestCase Objective
Verify closeApp with empty appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Empty AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with appId: "", closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="lifecyclemanager_closeapp_empty_params"></a>
### TestCase Name
LifecycleManager_CloseApp_Empty_Params

### TestCase ID
LCM_17

### TestCase Objective
Verify closeApp with empty appId and empty closeReason.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Empty Params | Invoke closeApp on org.rdk.LifecycleManager with appId: "", closeReason: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "", "closeReason": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_without_parameters"></a>
### TestCase Name
CloseApp_Without_Parameters

### TestCase ID
LCM_18

### TestCase Objective
Verify closeApp without any parameters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App No Params | Invoke closeApp on org.rdk.LifecycleManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Invalid_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_19

### TestCase Objective
Verify closeApp with invalid appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Invalid AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "InvalidAppID", closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_error_closereason"></a>
### TestCase Name
CloseApp_Invalid_AppId_ERROR_CloseReason

### TestCase ID
LCM_20

### TestCase Objective
Verify closeApp with invalid appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Invalid AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with appId: "InvalidAppID", closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Invalid_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_21

### TestCase Objective
Verify closeApp with invalid appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Invalid AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with appId: "InvalidAppID", closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_invalid_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Invalid_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_22

### TestCase Objective
Verify closeApp with invalid appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Invalid AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with appId: "InvalidAppID", closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppID", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Numeric_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_23

### TestCase Objective
Verify closeApp with numeric value for appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Numeric AppId | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_error_closereason"></a>
### TestCase Name
CloseApp_Numeric_AppId_ERROR_CloseReason

### TestCase ID
LCM_24

### TestCase Objective
Verify closeApp with numeric value for appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Numeric AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Numeric_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_25

### TestCase Objective
Verify closeApp with numeric value for appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Numeric AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_numeric_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Numeric_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_26

### TestCase Objective
Verify closeApp with numeric value for appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Numeric AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": 12345, "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Special_Char_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_27

### TestCase Objective
Verify closeApp with special character string as appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Special Char AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "!()*^", closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_error_closereason"></a>
### TestCase Name
CloseApp_Special_Char_AppId_ERROR_CloseReason

### TestCase ID
LCM_28

### TestCase Objective
Verify closeApp with special character string as appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Special Char AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with appId: "!()*^", closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Special_Char_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_29

### TestCase Objective
Verify closeApp with special character string as appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Special Char AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with appId: "!()*^", closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_special_char_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Special_Char_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_30

### TestCase Objective
Verify closeApp with special character string as appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Special Char AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with appId: "!()*^", closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "!()*^", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Boolean_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_31

### TestCase Objective
Verify closeApp with boolean value for appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Boolean AppId | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_error_closereason"></a>
### TestCase Name
CloseApp_Boolean_AppId_ERROR_CloseReason

### TestCase ID
LCM_32

### TestCase Objective
Verify closeApp with boolean value for appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Boolean AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Boolean_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_33

### TestCase Objective
Verify closeApp with boolean value for appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Boolean AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_boolean_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Boolean_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_34

### TestCase Objective
Verify closeApp with boolean value for appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Boolean AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": true, "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_user_exit_closereason"></a>
### TestCase Name
CloseApp_Long_String_AppId_USER_EXIT_CloseReason

### TestCase ID
LCM_35

### TestCase Objective
Verify closeApp with very long string as appId and USER_EXIT closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Long String AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "VeryLongStringForAppIdTestingPurpose", closeReason: "USER_EXIT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "USER_EXIT"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_error_closereason"></a>
### TestCase Name
CloseApp_Long_String_AppId_ERROR_CloseReason

### TestCase ID
LCM_36

### TestCase Objective
Verify closeApp with very long string as appId and ERROR closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Long String AppId ERROR | Invoke closeApp on org.rdk.LifecycleManager with appId: "VeryLongStringForAppIdTestingPurpose", closeReason: "ERROR"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "ERROR"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_kill_and_run_closereason"></a>
### TestCase Name
CloseApp_Long_String_AppId_KILL_AND_RUN_CloseReason

### TestCase ID
LCM_37

### TestCase Objective
Verify closeApp with very long string as appId and KILL_AND_RUN closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Long String AppId KILL AND RUN | Invoke closeApp on org.rdk.LifecycleManager with appId: "VeryLongStringForAppIdTestingPurpose", closeReason: "KILL_AND_RUN"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "KILL_AND_RUN"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_long_string_appid_kill_and_activate_closereason"></a>
### TestCase Name
CloseApp_Long_String_AppId_KILL_AND_ACTIVATE_CloseReason

### TestCase ID
LCM_38

### TestCase Objective
Verify closeApp with very long string as appId and KILL_AND_ACTIVATE closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Long String AppId KILL AND ACTIVATE | Invoke closeApp on org.rdk.LifecycleManager with appId: "VeryLongStringForAppIdTestingPurpose", closeReason: "KILL_AND_ACTIVATE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "closeReason": "KILL_AND_ACTIVATE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_numeric_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_Numeric_CloseReason

### TestCase ID
LCM_39

### TestCase Objective
Verify closeApp with valid appId and numeric value for closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Numeric CloseReason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_special_char_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_Special_Char_CloseReason

### TestCase ID
LCM_40

### TestCase Objective
Verify closeApp with valid appId and special character string as closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Special Char CloseReason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", closeReason: "!()*^"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "!()*^"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_boolean_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_Boolean_CloseReason

### TestCase ID
LCM_41

### TestCase Objective
Verify closeApp with valid appId and boolean value for closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Boolean CloseReason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="closeapp_valid_appid_long_string_closereason"></a>
### TestCase Name
CloseApp_Valid_AppId_Long_String_CloseReason

### TestCase ID
LCM_42

### TestCase Objective
Verify closeApp with valid appId and very long string as closeReason

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close App Long String CloseReason | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", closeReason: "VeryLongStringForCloseReasonTestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "closeReason": "VeryLongStringForCloseReasonTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check Package Info | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : Medium

**Release Version** : M147

<div align="right"><a href="#testscript-name">Go to Top</a></div>
