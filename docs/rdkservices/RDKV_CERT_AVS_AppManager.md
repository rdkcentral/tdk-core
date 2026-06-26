## TestScript Name
RDKV_CERT_AVS_AppManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [AppManager_Check_Response_Get_Installed_Apps](#appmanager_check_response_get_installed_apps)
   - [AppManager_Verify_IsInstalled_Valid_AppId](#appmanager_verify_isinstalled_valid_appid)
   - [AppManager_Verify_IsInstalled_With_Invalid_AppId](#appmanager_verify_isinstalled_with_invalid_appid)
   - [AppManager_Verify_IsInstalled_Empty_AppId](#appmanager_verify_isinstalled_empty_appid)
   - [AppManager_Verify_IsInstalled_NonExistent_AppId](#appmanager_verify_isinstalled_nonexistent_appid)
   - [AppManager_Verify_IsInstalled_Numeric_AppId](#appmanager_verify_isinstalled_numeric_appid)
   - [AppManager_Verify_IsInstalled_SpecialChar_AppId](#appmanager_verify_isinstalled_specialchar_appid)
   - [AppManager_Verify_IsInstalled_Long_AppId](#appmanager_verify_isinstalled_long_appid)
   - [AppManager_Verify_IsInstalled_With_Whitespace_AppId](#appmanager_verify_isinstalled_with_whitespace_appid)
   - [AppManager_Verify_IsInstalled_Mixed_Alphanumeric_SpecialChars](#appmanager_verify_isinstalled_mixed_alphanumeric_specialchars)
   - [AppManager_Check_Response_Get_Loaded_Apps](#appmanager_check_response_get_loaded_apps)
   - [AppManager_LaunchApp_Valid_Param](#appmanager_launchapp_valid_param)
   - [AppManager_LaunchApp_Invalid_AppId](#appmanager_launchapp_invalid_appid)
   - [AppManager_LaunchApp_Invalid_Intent](#appmanager_launchapp_invalid_intent)
   - [AppManager_LaunchApp_Invalid_LaunchArgs](#appmanager_launchapp_invalid_launchargs)
   - [AppManager_LaunchApp_Invalid_Params](#appmanager_launchapp_invalid_params)
   - [AppManager_LaunchApp_Empty_AppId](#appmanager_launchapp_empty_appid)
   - [AppManager_LaunchApp_Fail_Gracefully_Empty_Intent](#appmanager_launchapp_fail_gracefully_empty_intent)
   - [AppManager_LaunchApp_Fail_Gracefully_Empty_LaunchArgs](#appmanager_launchapp_fail_gracefully_empty_launchargs)
   - [AppManager_LaunchApp_Fail_Gracefully_Without_Params](#appmanager_launchapp_fail_gracefully_without_params)
   - [AppManager_LaunchApp_EdgeCase_LongStrings](#appmanager_launchapp_edgecase_longstrings)
   - [AppManager_Verify_PreloadApp_Valid_Param](#appmanager_verify_preloadapp_valid_param)
   - [AppManager_PreloadApp_Empty_AppId](#appmanager_preloadapp_empty_appid)
   - [AppManager_PreloadApp_Empty_LaunchArgs](#appmanager_preloadapp_empty_launchargs)
   - [AppManager_PreloadApp_Special_Char_AppId](#appmanager_preloadapp_special_char_appid)
   - [AppManager_PreloadApp_Special_Char_LaunchArgs](#appmanager_preloadapp_special_char_launchargs)
   - [AppManager_Verify_PreloadApp_with_Numeric_AppId](#appmanager_verify_preloadapp_with_numeric_appid)
   - [AppManager_PreloadApp_Numeric_LaunchArgs](#appmanager_preloadapp_numeric_launchargs)
   - [AppManager_Verify_PreloadApp_with_Alphanumeric_AppId](#appmanager_verify_preloadapp_with_alphanumeric_appid)
   - [AppManager_Verify_PreloadApp_with_Alphanumeric_LaunchArgs](#appmanager_verify_preloadapp_with_alphanumeric_launchargs)
   - [AppManager_PreloadApp_Valid_AppId_Already_Preloaded](#appmanager_preloadapp_valid_appid_already_preloaded)
   - [AppManager_CloseApp_Valid_AppId](#appmanager_closeapp_valid_appid)
   - [AppManager_CloseApp_Invalid_AppId](#appmanager_closeapp_invalid_appid)
   - [AppManager_CloseApp_Empty_AppId](#appmanager_closeapp_empty_appid)
   - [AppManager_CloseApp_Special_Char_AppId](#appmanager_closeapp_special_char_appid)
   - [AppManager_CloseApp_ValidAppId_NotLoaded](#appmanager_closeapp_validappid_notloaded)
   - [AppManager_TerminateApp_Valid_AppId_Param](#appmanager_terminateapp_valid_appid_param)
   - [AppManager_TerminateApp_Invalid_AppId](#appmanager_terminateapp_invalid_appid)
   - [AppManager_TerminateApp_Empty_AppId](#appmanager_terminateapp_empty_appid)
   - [AppManager_TerminateApp_Numeric_AppId](#appmanager_terminateapp_numeric_appid)
   - [AppManager_TerminateApp_Special_Char_AppId](#appmanager_terminateapp_special_char_appid)
   - [AppManager_StartSystemApp_Valid_AppId](#appmanager_startsystemapp_valid_appid)
   - [AppManager_StartSystemApp_Invalid_AppId](#appmanager_startsystemapp_invalid_appid)
   - [AppManager_StartSystemApp_Empty_AppId](#appmanager_startsystemapp_empty_appid)
   - [AppManager_StartSystemApp_Special_Char_AppId](#appmanager_startsystemapp_special_char_appid)
   - [AppManager_StartSystemApp_Numeric_AppId](#appmanager_startsystemapp_numeric_appid)
   - [AppManager_StopSystemApp_Valid_AppId](#appmanager_stopsystemapp_valid_appid)
   - [AppManager_StopSystemApp_Valid_AppId_Already_Stopped](#appmanager_stopsystemapp_valid_appid_already_stopped)
   - [AppManager_StopSystemApp_Invalid_AppId](#appmanager_stopsystemapp_invalid_appid)
   - [AppManager_StopSystemApp_Empty_AppId](#appmanager_stopsystemapp_empty_appid)
   - [AppManager_StopSystemApp_Special_Char_AppId](#appmanager_stopsystemapp_special_char_appid)
   - [AppManager_StopSystemApp_Numeric_AppId](#appmanager_stopsystemapp_numeric_appid)
   - [AppManager_StopSystemApp_Alphanumeric_AppId](#appmanager_stopsystemapp_alphanumeric_appid)
   - [AppManager_KillApp_Valid_AppId](#appmanager_killapp_valid_appid)
   - [AppManager_KillApp_Invalid_AppId](#appmanager_killapp_invalid_appid)
   - [AppManager_KillApp_Empty_AppId](#appmanager_killapp_empty_appid)
   - [AppManager_KillApp_Numeric_AppId](#appmanager_killapp_numeric_appid)
   - [AppManager_KillApp_Special_Char_AppId](#appmanager_killapp_special_char_appid)
   - [AppManager_Send_Intent_Valid_Params](#appmanager_send_intent_valid_params)
   - [AppManager_SendIntent_ValidAppId_EmptyIntent](#appmanager_sendintent_validappid_emptyintent)
   - [AppManager_SendIntent_EmptyAppId_ValidIntent](#appmanager_sendintent_emptyappid_validintent)
   - [AppManager_SendIntent_Empty_Params](#appmanager_sendintent_empty_params)
   - [AppManager_SendIntent_Invalid_AppId](#appmanager_sendintent_invalid_appid)
   - [AppManager_Clear_App_Data_Valid_AppId](#appmanager_clear_app_data_valid_appid)
   - [AppManager_Clear_App_Data_Invalid_AppId](#appmanager_clear_app_data_invalid_appid)
   - [AppManager_ClearAppData_Empty_AppId](#appmanager_clearappdata_empty_appid)
   - [AppManager_ClearAppData_SpecialCharacters](#appmanager_clearappdata_specialcharacters)
   - [AppManager_ClearAppData_Long_AppId](#appmanager_clearappdata_long_appid)
   - [ClearAppData_Numeric_AppId](#clearappdata_numeric_appid)
   - [AppManager_ClearAppData_Alphanumeric_AppId](#appmanager_clearappdata_alphanumeric_appid)
   - [AppManager_Clear_All_App_Data](#appmanager_clear_all_app_data)
   - [AppManager_SetAppProperty_ValidAppId_Delay_10](#appmanager_setappproperty_validappid_delay_10)
   - [AppManager_SetAppProperty_Empty_AppId_Key_Value](#appmanager_setappproperty_empty_appid_key_value)
   - [AppManager_SetAppProperty_Numeric_AppId_Key_Value](#appmanager_setappproperty_numeric_appid_key_value)
   - [AppManager_SetAppProperty_SpecialChars_All_Params](#appmanager_setappproperty_specialchars_all_params)
   - [AppManager_SetAppProperty_InvalidAppId_ValidKey_ValidValue](#appmanager_setappproperty_invalidappid_validkey_validvalue)
   - [AppManager_SetAppProperty_ValidAppId_InvalidKey_ValidValue](#appmanager_setappproperty_validappid_invalidkey_validvalue)
   - [AppManager_SetAppProperty_ValidAppId_EmptyKey_ValidValue](#appmanager_setappproperty_validappid_emptykey_validvalue)
   - [AppManager_GetAppProperty_ValidAppId_InvalidKey](#appmanager_getappproperty_validappid_invalidkey)
   - [AppManager_GetAppProperty_ValidAppId_EmptyKey](#appmanager_getappproperty_validappid_emptykey)
   - [AppManager_GetAppProperty_Invalid_AppId_Valid_Key](#appmanager_getappproperty_invalid_appid_valid_key)
   - [AppManager_GetAppProperty_Invalid_Params](#appmanager_getappproperty_invalid_params)
   - [AppManager_GetAppProperty_InvalidAppId_EmptyKey](#appmanager_getappproperty_invalidappid_emptykey)
   - [AppManager_GetAppProperty_EmptyAppId_ValidKey](#appmanager_getappproperty_emptyappid_validkey)
   - [AppManager_GetAppProperty_EmptyAppId_InvalidKey](#appmanager_getappproperty_emptyappid_invalidkey)
   - [AppManager_GetAppProperty_EmptyAppId_EmptyKey](#appmanager_getappproperty_emptyappid_emptykey)
   - [AppManager_Max_Running_Apps](#appmanager_max_running_apps)
   - [AppManager_GetAppProperty_ValidAppId_ValidKey_Pinlock](#appmanager_getappproperty_validappid_validkey_pinlock)
   - [AppManager_GetAppProperty_ValidAppId_ValidKey_InactivePriority](#appmanager_getappproperty_validappid_validkey_inactivepriority)
   - [AppManager_GetAppProperty_NumericAppId_NumericKey](#appmanager_getappproperty_numericappid_numerickey)
   - [AppManager_ActivateSystemApp_Valid_AppId](#appmanager_activatesystemapp_valid_appid)
   - [AppManager_ActivateSystemApp_Invalid_AppId](#appmanager_activatesystemapp_invalid_appid)
   - [AppManager_ActivateSystemApp_Empty_AppId](#appmanager_activatesystemapp_empty_appid)
   - [AppManager_ActivateSystemApp_Special_Char_AppId](#appmanager_activatesystemapp_special_char_appid)
   - [AppManager_ActivateSystemApp_Numeric_AppId](#appmanager_activatesystemapp_numeric_appid)
   - [AppManager_ActivateSystemApp_Without_Param](#appmanager_activatesystemapp_without_param)
   - [AppManager_DeactivateSystemApp_Valid_AppId](#appmanager_deactivatesystemapp_valid_appid)
   - [AppManager_DeactivateSystemApp_Invalid_AppId](#appmanager_deactivatesystemapp_invalid_appid)
   - [AppManager_DeactivateSystemApp_Empty_AppId](#appmanager_deactivatesystemapp_empty_appid)
   - [AppManager_DeactivateSystemApp_Special_Char_AppId](#appmanager_deactivatesystemapp_special_char_appid)
   - [AppManager_DeactivateSystemApp_Numeric_AppId](#appmanager_deactivatesystemapp_numeric_appid)
   - [AppManager_DeactivateSystemApp_Without_Param](#appmanager_deactivatesystemapp_without_param)
   - [AppManager_HibernateSystemApp_Valid_AppId](#appmanager_hibernatesystemapp_valid_appid)
   - [AppManager_HibernateSystemApp_Invalid_AppId](#appmanager_hibernatesystemapp_invalid_appid)
   - [AppManager_HibernateSystemApp_Empty_AppId](#appmanager_hibernatesystemapp_empty_appid)
   - [AppManager_HibernateSystemApp_Special_Char_AppId](#appmanager_hibernatesystemapp_special_char_appid)
   - [AppManager_HibernateSystemApp_Numeric_AppId](#appmanager_hibernatesystemapp_numeric_appid)
   - [AppManager_HibernateSystemApp_Without_Param](#appmanager_hibernatesystemapp_without_param)
   - [AppManager_Max_Inactive_Ramusage](#appmanager_max_inactive_ramusage)
   - [AppManager_App_Lock_Launch_Terminate_Unlock_Operations](#appmanager_app_lock_launch_terminate_unlock_operations)
   - [AppManager_App_Launch_Terminate_Lock_Unlock_Operations](#appmanager_app_launch_terminate_lock_unlock_operations)
   - [AppManager_App_Launch_Kill_Lock_Unlock_Operations](#appmanager_app_launch_kill_lock_unlock_operations)
   - [AppManager_App_Launch_Close_Lock_Unlock_Operations](#appmanager_app_launch_close_lock_unlock_operations)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Close](#appmanager_check_on_applifecyclestatechanged_event_after_close)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Kill](#appmanager_check_on_applifecyclestatechanged_event_after_kill)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Terminate](#appmanager_check_on_applifecyclestatechanged_event_after_terminate)
   - [AppManager_App_Launch_Twice](#appmanager_app_launch_twice)
   - [AppManager_Check_Get_Loaded_Apps_After_Launch](#appmanager_check_get_loaded_apps_after_launch)
   - [AppManager_Check_Get_Loaded_Apps_After_Close](#appmanager_check_get_loaded_apps_after_close)
   - [AppManager_Check_Get_Loaded_Apps_After_Kill](#appmanager_check_get_loaded_apps_after_kill)
   - [AppManager_Check_Get_Loaded_Apps_After_Terminate](#appmanager_check_get_loaded_apps_after_terminate)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **AppManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.AppManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getAppProperty`, `getInstalledApps`, `getLoadedApps`, `getMaxRunningApps`, `isInstalled`
- **Lifecycle / Control APIs**: `activateSystemApp`, `closeApp`, `deactivateSystemApp`, `hibernateSystemApp`, `killApp`, `launchApp`, `preloadApp`, `sendIntent`, `startSystemApp`, `stopSystemApp`, `terminateApp`
- **Configuration APIs**: `clearAllAppData`, `clearAppData`, `setAppProperty`
- **Events**: `onAppLifecycleStateChanged`

## APIs Under Test

| API | Description |
|-----|-------------|
| `activateSystemApp` | Activates the device application |
| `clearAllAppData` | Clears all application data |
| `clearAppData` | Clears the data of a specific application |
| `closeApp` | Close the app |
| `deactivateSystemApp` | Deactivates the device application |
| `getAppProperty` | Retrieve a specific property of an application |
| `getInstalledApps` | Function fetches the details of all applications currently installed |
| `getLoadedApps` | Retrieves a list of applications currently loaded on the device |
| `getMaxRunningApps` | Retrieves the maximum number of running applications allowed |
| `hibernateSystemApp` | Hibernates the device application |
| `isInstalled` | Check if an application is installed |
| `killApp` | Terminates the specified application |
| `launchApp` | Launches an application |
| `preloadApp` | Preloads an application instance. |
| `sendIntent` | Sends an intent to a specific application |
| `setAppProperty` | Sets a property for the application instance |
| `startSystemApp` | Starts the device application |
| `stopSystemApp` | Stops the device application |
| `terminateApp` | Terminates an application |

## Events Under Test

| Event | Description |
|-------|-------------|
| `onAppLifecycleStateChanged` | Triggered whenever there is a change in the lifecycle state of a running application |

---

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

### Plugin Pre-condition 5: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 6: Register_And_Listen_Events

- Register and listen to event `Event_On_App_Lifecycle_State_Changed` on `AppManager` plugin

---

## Test Cases

<a id="appmanager_check_response_get_installed_apps"></a>
### TestCase Name
AppManager_Check_Response_Get_Installed_Apps

### TestCase ID
AM_01

### TestCase Objective
Check the response when applications are installed

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Installed Apps | Invoke getInstalledApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that installed applications appear in the list |

---

<a id="appmanager_verify_isinstalled_valid_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_Valid_AppId

### TestCase ID
AM_02

### TestCase Objective
Verify isInstalled with a valid appId of an installed application

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled | Invoke isInstalled on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `true` |

---

<a id="appmanager_verify_isinstalled_with_invalid_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_With_Invalid_AppId

### TestCase ID
AM_03

### TestCase Objective
Verify isInstalled with an invalid appId of an application that is not installed

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled With Invalid AppId | Invoke isInstalled on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_empty_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_Empty_AppId

### TestCase ID
AM_04

### TestCase Objective
Verify isInstalled with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Empty AppId | Invoke isInstalled on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_isinstalled_nonexistent_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_NonExistent_AppId

### TestCase ID
AM_05

### TestCase Objective
Verify isInstalled with a non-existent appId (e.g., random string)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled NonExistent AppId | Invoke isInstalled on org.rdk.AppManager with appId: "zxcvbasdfg"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "zxcvbasdfg"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_numeric_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_Numeric_AppId

### TestCase ID
AM_06

### TestCase Objective
Verify isInstalled with a numeric value as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Numeric AppId | Invoke isInstalled on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_specialchar_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_SpecialChar_AppId

### TestCase ID
AM_07

### TestCase Objective
Verify isInstalled with a special character string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled SpecialChar AppId | Invoke isInstalled on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_long_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_Long_AppId

### TestCase ID
AM_08

### TestCase Objective
Verify isInstalled with a very long string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Long AppId | Invoke isInstalled on org.rdk.AppManager with appId: "VeryLongStringForAppIdTestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "VeryLongStringForAppIdTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_with_whitespace_appid"></a>
### TestCase Name
AppManager_Verify_IsInstalled_With_Whitespace_AppId

### TestCase ID
AM_09

### TestCase Objective
Verify isInstalled with a appId containing spaces or whitespace characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Whitespace AppId | Invoke isInstalled on org.rdk.AppManager with appId: "App Id"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "App Id"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_mixed_alphanumeric_specialchars"></a>
### TestCase Name
AppManager_Verify_IsInstalled_Mixed_Alphanumeric_SpecialChars

### TestCase ID
AM_10

### TestCase Objective
Verify isInstalled with a appId containing mixed alphanumeric and special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled | Invoke isInstalled on org.rdk.AppManager with appId: "MixedAlphaNum@123!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "MixedAlphaNum@123!"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_check_response_get_loaded_apps"></a>
### TestCase Name
AppManager_Check_Response_Get_Loaded_Apps

### TestCase ID
AM_11

### TestCase Objective
Retrieves a list of applications currently loaded

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Loaded Apps | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Ensure the getLoadedApps API responds without errors when no applications are running, and provides a non-empty response when applications are active |

---

<a id="appmanager_launchapp_valid_param"></a>
### TestCase Name
AppManager_LaunchApp_Valid_Param

### TestCase ID
AM_12

### TestCase Objective
Verify that the launchApp method successfully launches an application when provided with a valid appId

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Param | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_launchapp_invalid_appid"></a>
### TestCase Name
AppManager_LaunchApp_Invalid_AppId

### TestCase ID
AM_13

### TestCase Objective
Verify that the launchApp method fails gracefully when an invalid appId is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid AppId | Invoke launchApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_intent"></a>
### TestCase Name
AppManager_LaunchApp_Invalid_Intent

### TestCase ID
AM_14

### TestCase Objective
Verify that the launchApp method fails gracefully when an invalid intent is provided, while appId is valid

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid Intent | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", intent: "InvalidIntent"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "InvalidIntent"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_launchargs"></a>
### TestCase Name
AppManager_LaunchApp_Invalid_LaunchArgs

### TestCase ID
AM_15

### TestCase Objective
Verify that the launchApp method fails gracefully when an invalid launchArgs is provided, while appId is valid

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid LaunchArgs | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", launchArgs: "InvalidSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "InvalidSource"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_params"></a>
### TestCase Name
AppManager_LaunchApp_Invalid_Params

### TestCase ID
AM_16

### TestCase Objective
Verify that the launchApp method fails gracefully when all parameters appId, intent, and launchArgs are invalid

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid Params | Invoke launchApp on org.rdk.AppManager with appId: "InvalidAppId", intent: "InvalidIntent", launchArgs: "InvalidSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "InvalidAppId", "intent": "InvalidIntent", "launchArgs": "InvalidSource"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_empty_appid"></a>
### TestCase Name
AppManager_LaunchApp_Empty_AppId

### TestCase ID
AM_17

### TestCase Objective
Verify that the launchApp method fails gracefully when the appId parameter is empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty AppId | Invoke launchApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_empty_intent"></a>
### TestCase Name
AppManager_LaunchApp_Fail_Gracefully_Empty_Intent

### TestCase ID
AM_18

### TestCase Objective
Verify that the launchApp method fails gracefully when the intent parameter is empty, while appId is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty Intent | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", intent: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_empty_launchargs"></a>
### TestCase Name
AppManager_LaunchApp_Fail_Gracefully_Empty_LaunchArgs

### TestCase ID
AM_19

### TestCase Objective
Verify that the launchApp method fails gracefully when the launchArgs parameter is empty, while appId is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty LaunchArgs | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", launchArgs: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_without_params"></a>
### TestCase Name
AppManager_LaunchApp_Fail_Gracefully_Without_Params

### TestCase ID
AM_20

### TestCase Objective
Verify that the launchApp method fails gracefully when all parameters appId, intent, and launchArgs are missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Without Params | Invoke launchApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_edgecase_longstrings"></a>
### TestCase Name
AppManager_LaunchApp_EdgeCase_LongStrings

### TestCase ID
AM_21

### TestCase Objective
Verify that the launchApp method handles edge cases, such as extremely long strings for appId, intent, and launchArgs, without crashing or unexpected behavior

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Long Strings | Invoke launchApp on org.rdk.AppManager with appId: "A_very_long_string_exceeding_normal_limits_for_testing_purposes_appId", intent: "A_very_long_string_exceeding_normal_limits_for_testing_purposes_intent", launchArgs: "A_very_long_string_exceeding_normal_limits_for_testing_purposes_source"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_appId", "intent": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_intent", "launchArgs": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_source"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_valid_param"></a>
### TestCase Name
AppManager_Verify_PreloadApp_Valid_Param

### TestCase ID
AM_22

### TestCase Objective
Verify preloadApp with a valid param when provided with a valid appId

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Valid Param | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_preloadapp_empty_appid"></a>
### TestCase Name
AppManager_PreloadApp_Empty_AppId

### TestCase ID
AM_23

### TestCase Objective
Verify preloadApp with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Empty AppId | Invoke preloadApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_empty_launchargs"></a>
### TestCase Name
AppManager_PreloadApp_Empty_LaunchArgs

### TestCase ID
AM_24

### TestCase Objective
Verify preloadApp with an empty string as launchArgs

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Empty LaunchArgs | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", launchArgs: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_special_char_appid"></a>
### TestCase Name
AppManager_PreloadApp_Special_Char_AppId

### TestCase ID
AM_25

### TestCase Objective
Verify preloadApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Preload App Special Char AppId | Invoke preloadApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_special_char_launchargs"></a>
### TestCase Name
AppManager_PreloadApp_Special_Char_LaunchArgs

### TestCase ID
AM_26

### TestCase Objective
Verify preloadApp with launchArgs containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Special Char LaunchArgs | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", launchArgs: "()*^!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "()*^!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_numeric_appid"></a>
### TestCase Name
AppManager_Verify_PreloadApp_with_Numeric_AppId

### TestCase ID
AM_27

### TestCase Objective
Verify preloadApp with a appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Numeric AppId | Invoke preloadApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": 123456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_numeric_launchargs"></a>
### TestCase Name
AppManager_PreloadApp_Numeric_LaunchArgs

### TestCase ID
AM_28

### TestCase Objective
Verify preloadApp with launchArgs containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Preload App Numeric LaunchArgs | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": 123456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_alphanumeric_appid"></a>
### TestCase Name
AppManager_Verify_PreloadApp_with_Alphanumeric_AppId

### TestCase ID
AM_29

### TestCase Objective
Verify preloadApp with an appId containing a mix of alphanumeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Alphanumeric AppId | Invoke preloadApp on org.rdk.AppManager with appId: "abc123XYZ"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "abc123XYZ"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message`ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_alphanumeric_launchargs"></a>
### TestCase Name
AppManager_Verify_PreloadApp_with_Alphanumeric_LaunchArgs

### TestCase ID
AM_30

### TestCase Objective
Verify preloadApp with launchArgs containing a mix of alphanumeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Alphanumeric LaunchArgs | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", launchArgs: "arg1Value2Test3"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "arg1Value2Test3"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_valid_appid_already_preloaded"></a>
### TestCase Name
AppManager_PreloadApp_Valid_AppId_Already_Preloaded

### TestCase ID
AM_31

### TestCase Objective
Verify preloadApp with a appId that is a valid application but is already preloaded

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Valid AppId | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 3 | PreloadApp Valid AppId Already Preloaded | Invoke preloadApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_closeapp_valid_appid"></a>
### TestCase Name
AppManager_CloseApp_Valid_AppId

### TestCase ID
AM_32

### TestCase Objective
Verify closeApp with valid appId

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check App Launched | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Valid Params | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_closeapp_invalid_appid"></a>
### TestCase Name
AppManager_CloseApp_Invalid_AppId

### TestCase ID
AM_33

### TestCase Objective
Verify closeApp with an invalid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_empty_appid"></a>
### TestCase Name
AppManager_CloseApp_Empty_AppId

### TestCase ID
AM_34

### TestCase Objective
Verify closeApp with an empty appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_special_char_appid"></a>
### TestCase Name
AppManager_CloseApp_Special_Char_AppId

### TestCase ID
AM_35

### TestCase Objective
Verify closeApp with an appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId | Invoke closeApp on org.rdk.LifecycleManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_validappid_notloaded"></a>
### TestCase Name
AppManager_CloseApp_ValidAppId_NotLoaded

### TestCase ID
AM_36

### TestCase Objective
Verify closeApp with an appId that is valid but the app is not loaded in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Valid NotLoaded | Invoke closeApp on org.rdk.LifecycleManager with appId: "Cobalt"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "Cobalt"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_valid_appid_param"></a>
### TestCase Name
AppManager_TerminateApp_Valid_AppId_Param

### TestCase ID
AM_37

### TestCase Objective
Verify terminateApp with valid appId

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check App Launched | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_terminateapp_invalid_appid"></a>
### TestCase Name
AppManager_TerminateApp_Invalid_AppId

### TestCase ID
AM_38

### TestCase Objective
Verify terminateApp with an invalid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Invalid AppId | Invoke terminateApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_empty_appid"></a>
### TestCase Name
AppManager_TerminateApp_Empty_AppId

### TestCase ID
AM_39

### TestCase Objective
Verify terminateApp with an empty appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Empty AppId | Invoke terminateApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_numeric_appid"></a>
### TestCase Name
AppManager_TerminateApp_Numeric_AppId

### TestCase ID
AM_40

### TestCase Objective
Verify terminateApp with an appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Numeric AppId | Invoke terminateApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_special_char_appid"></a>
### TestCase Name
AppManager_TerminateApp_Special_Char_AppId

### TestCase ID
AM_41

### TestCase Objective
Verify terminateApp with an appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Special Char AppId | Invoke terminateApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_valid_appid"></a>
### TestCase Name
AppManager_StartSystemApp_Valid_AppId

### TestCase ID
AM_42

### TestCase Objective
Verify startSystemApp with a valid appId of an installed device application

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke startSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_startsystemapp_invalid_appid"></a>
### TestCase Name
AppManager_StartSystemApp_Invalid_AppId

### TestCase ID
AM_43

### TestCase Objective
Verify startSystemApp with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Invalid AppId | Invoke startSystemApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_empty_appid"></a>
### TestCase Name
AppManager_StartSystemApp_Empty_AppId

### TestCase ID
AM_44

### TestCase Objective
Verify startSystemApp with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Empty AppId | Invoke startSystemApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_special_char_appid"></a>
### TestCase Name
AppManager_StartSystemApp_Special_Char_AppId

### TestCase ID
AM_45

### TestCase Objective
Verify startSystemApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Special Char | Invoke startSystemApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_numeric_appid"></a>
### TestCase Name
AppManager_StartSystemApp_Numeric_AppId

### TestCase ID
AM_46

### TestCase Objective
Verify startSystemApp with an appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Numeric AppId | Invoke startSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_valid_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Valid_AppId

### TestCase ID
AM_47

### TestCase Objective
Verify stopSystemApp with a valid appId of an actively running device application

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Invoke stopSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_stopsystemapp_valid_appid_already_stopped"></a>
### TestCase Name
AppManager_StopSystemApp_Valid_AppId_Already_Stopped

### TestCase ID
AM_48

### TestCase Objective
Verify stopSystemApp with a valid appId of a device application that is already stopped

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke startSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Stop System App | Invoke stopSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Stop System App | Invoke stopSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_invalid_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Invalid_AppId

### TestCase ID
AM_49

### TestCase Objective
Verify stopSystemApp with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Invalid AppId | Invoke stopSystemApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_empty_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Empty_AppId

### TestCase ID
AM_50

### TestCase Objective
Verify stopSystemApp with an empty string as the appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Empty AppId | Invoke stopSystemApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_special_char_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Special_Char_AppId

### TestCase ID
AM_51

### TestCase Objective
Verify stopSystemApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Special Char | Invoke stopSystemApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_numeric_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Numeric_AppId

### TestCase ID
AM_52

### TestCase Objective
Verify stopSystemApp with a appId containing only numeric values

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Numeric AppId | Invoke stopSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_alphanumeric_appid"></a>
### TestCase Name
AppManager_StopSystemApp_Alphanumeric_AppId

### TestCase ID
AM_53

### TestCase Objective
Verify stopSystemApp with a appId containing a mix of alphanumeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Alphanumeric AppId | Invoke stopSystemApp on org.rdk.AppManager with appId: "App123Alpha"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "App123Alpha"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_valid_appid"></a>
### TestCase Name
AppManager_KillApp_Valid_AppId

### TestCase ID
AM_54

### TestCase Objective
Verify killApp with valid appId

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check App Launched | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Valid Param | Invoke killApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_killapp_invalid_appid"></a>
### TestCase Name
AppManager_KillApp_Invalid_AppId

### TestCase ID
AM_55

### TestCase Objective
Verify killApp with an invalid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Invalid AppId | Invoke killApp on org.rdk.AppManager with appId: "InvalidApp"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "InvalidApp"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_empty_appid"></a>
### TestCase Name
AppManager_KillApp_Empty_AppId

### TestCase ID
AM_56

### TestCase Objective
Verify killApp with an empty appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Empty AppId | Invoke killApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_numeric_appid"></a>
### TestCase Name
AppManager_KillApp_Numeric_AppId

### TestCase ID
AM_57

### TestCase Objective
Verify killApp with a numeric appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Numeric AppId | Invoke killApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_special_char_appid"></a>
### TestCase Name
AppManager_KillApp_Special_Char_AppId

### TestCase ID
AM_58

### TestCase Objective
Verify killApp with an appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Special Char AppId | Invoke killApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_send_intent_valid_params"></a>
### TestCase Name
AppManager_Send_Intent_Valid_Params

### TestCase ID
AM_59

### TestCase Objective
Verify sendIntent with valid appId and valid intent

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Valid Params | Invoke sendIntent on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", intent: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_sendintent_validappid_emptyintent"></a>
### TestCase Name
AppManager_SendIntent_ValidAppId_EmptyIntent

### TestCase ID
AM_60

### TestCase Objective
Verify sendIntent with valid appId and an empty string for intent

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent ValidAppId EmptyIntent | Invoke sendIntent on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", intent: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_emptyappid_validintent"></a>
### TestCase Name
AppManager_SendIntent_EmptyAppId_ValidIntent

### TestCase ID
AM_61

### TestCase Objective
Verify sendIntent with an empty string for appId and valid intent

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent EmptyAppId ValidIntent | Invoke sendIntent on org.rdk.AppManager with appId: "", intent: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_empty_params"></a>
### TestCase Name
AppManager_SendIntent_Empty_Params

### TestCase ID
AM_62

### TestCase Objective
Verify sendIntent with empty strings for all parameters appId and intent

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Empty Params | Invoke sendIntent on org.rdk.AppManager with appId: "", intent: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_invalid_appid"></a>
### TestCase Name
AppManager_SendIntent_Invalid_AppId

### TestCase ID
AM_63

### TestCase Objective
Verify sendIntent with invalid appId and valid intent

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Invalid AppId | Invoke sendIntent on org.rdk.AppManager with appId: "InvalidAppId", intent: "start"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "InvalidAppId", "intent": "start"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clear_app_data_valid_appid"></a>
### TestCase Name
AppManager_Clear_App_Data_Valid_AppId

### TestCase ID
AM_64

### TestCase Objective
Verify clearAppData with a valid appId of an installed application

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Valid AppId | Invoke clear on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_clear_app_data_invalid_appid"></a>
### TestCase Name
AppManager_Clear_App_Data_Invalid_AppId

### TestCase ID
AM_65

### TestCase Objective
Verify clearAppData with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Invalid AppId | Invoke clear on org.rdk.AppStorageManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_empty_appid"></a>
### TestCase Name
AppManager_ClearAppData_Empty_AppId

### TestCase ID
AM_66

### TestCase Objective
Verify clearAppData with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Empty AppId | Invoke clear on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_specialcharacters"></a>
### TestCase Name
AppManager_ClearAppData_SpecialCharacters

### TestCase ID
AM_67

### TestCase Objective
Verify clearAppData with appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Special Characters | Invoke clear on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_long_appid"></a>
### TestCase Name
AppManager_ClearAppData_Long_AppId

### TestCase ID
AM_68

### TestCase Objective
Verify clearAppData with appId containing a very long string

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Long AppId | Invoke clear on org.rdk.AppStorageManager with appId: "A_very_long_string_characters_here"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "A_very_long_string_characters_here"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="clearappdata_numeric_appid"></a>
### TestCase Name
ClearAppData_Numeric_AppId

### TestCase ID
AM_69

### TestCase Objective
Verify clearAppData with appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Numeric AppId | Invoke clear on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_alphanumeric_appid"></a>
### TestCase Name
AppManager_ClearAppData_Alphanumeric_AppId

### TestCase ID
AM_70

### TestCase Objective
Verify clearAppData with appId containing a mix of alphanumeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Alphanumeric AppId | Invoke clear on org.rdk.AppStorageManager with appId: "TestApp123"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "TestApp123"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clear_all_app_data"></a>
### TestCase Name
AppManager_Clear_All_App_Data

### TestCase ID
AM_71

### TestCase Objective
Verify that clearAllAppData successfully clears all persistent data for all installed applications when invoked

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All App Data | Invoke clearAllAppData on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.clearAllAppData"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_setappproperty_validappid_delay_10"></a>
### TestCase Name
AppManager_SetAppProperty_ValidAppId_Delay_10

### TestCase ID
AM_72

### TestCase Objective
Verify setAppProperty sets key 'delay' to value '10' for the valid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Delay 10 | Invoke setAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "delay"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "delay", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Verify Get App Property | Invoke getAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "delay"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | Status matches expected value `10` |

---

<a id="appmanager_setappproperty_empty_appid_key_value"></a>
### TestCase Name
AppManager_SetAppProperty_Empty_AppId_Key_Value

### TestCase ID
AM_73

### TestCase Objective
Verify setAppProperty with all parameters empty.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Empty Params | Invoke setAppProperty on org.rdk.AppManager with appId: "", key: "", value: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "", "key": "", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_numeric_appid_key_value"></a>
### TestCase Name
AppManager_SetAppProperty_Numeric_AppId_Key_Value

### TestCase ID
AM_74

### TestCase Objective
Verify setAppProperty with numeric strings for all parameters.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Numeric Params | Invoke setAppProperty on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": 12345, "key": 67890, "value": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_specialchars_all_params"></a>
### TestCase Name
AppManager_SetAppProperty_SpecialChars_All_Params

### TestCase ID
AM_75

### TestCase Objective
Verify setAppProperty with only special characters for all parameters.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property SpecialChars All | Invoke setAppProperty on org.rdk.AppManager with appId: "()^*!", key: "!*()", value: "@@@"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "()^*!", "key": "!*()", "value": "@@@"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_invalidappid_validkey_validvalue"></a>
### TestCase Name
AppManager_SetAppProperty_InvalidAppId_ValidKey_ValidValue

### TestCase ID
AM_76

### TestCase Objective
Verify setAppProperty with invalid appId and valid key/value.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property InvalidAppId | Invoke setAppProperty on org.rdk.AppManager with appId: "Invalid@AppId!", key: "delay"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "Invalid@AppId!", "key": "delay", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_validappid_invalidkey_validvalue"></a>
### TestCase Name
AppManager_SetAppProperty_ValidAppId_InvalidKey_ValidValue

### TestCase ID
AM_77

### TestCase Objective
Verify setAppProperty with valid appId, invalid key, valid value.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property InvalidKey | Invoke setAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "Invalid#Key"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "Invalid#Key", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_validappid_emptykey_validvalue"></a>
### TestCase Name
AppManager_SetAppProperty_ValidAppId_EmptyKey_ValidValue

### TestCase ID
AM_78

### TestCase Objective
Verify setAppProperty with valid appId/value and empty key.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property EmptyKey | Invoke setAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_validappid_invalidkey"></a>
### TestCase Name
AppManager_GetAppProperty_ValidAppId_InvalidKey

### TestCase ID
AM_79

### TestCase Objective
Verify getAppProperty with valid appId and invalid key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty | Invoke getAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "InvalidKey"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_validappid_emptykey"></a>
### TestCase Name
AppManager_GetAppProperty_ValidAppId_EmptyKey

### TestCase ID
AM_80

### TestCase Objective
Verify getAppProperty with valid appId and empty key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty | Invoke getAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalid_appid_valid_key"></a>
### TestCase Name
AppManager_GetAppProperty_Invalid_AppId_Valid_Key

### TestCase ID
AM_81

### TestCase Objective
Verify getAppProperty with invalid appId and valid key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty Invalid AppId Valid Key | Invoke getAppProperty on org.rdk.AppManager with appId: "InvalidAppId", key: "delay"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalid_params"></a>
### TestCase Name
AppManager_GetAppProperty_Invalid_Params

### TestCase ID
AM_82

### TestCase Objective
Verify getAppProperty with invalid appId and invalid key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty Invalid Params | Invoke getAppProperty on org.rdk.AppManager with appId: "InvalidAppId", key: "InvalidKey"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalidappid_emptykey"></a>
### TestCase Name
AppManager_GetAppProperty_InvalidAppId_EmptyKey

### TestCase ID
AM_83

### TestCase Objective
Verify getAppProperty with invalid appId and empty key.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property InvalidAppId EmptyKey | Invoke getAppProperty on org.rdk.AppManager with appId: "InvalidAppId", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_validkey"></a>
### TestCase Name
AppManager_GetAppProperty_EmptyAppId_ValidKey

### TestCase ID
AM_84

### TestCase Objective
Verify getAppProperty with empty appId and valid key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property EmptyAppId ValidKey | Invoke getAppProperty on org.rdk.AppManager with appId: "", key: "delay"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_invalidkey"></a>
### TestCase Name
AppManager_GetAppProperty_EmptyAppId_InvalidKey

### TestCase ID
AM_85

### TestCase Objective
Verify getAppProperty with empty appId and invalid key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetAppProperty EmptyAppId InvalidKey | Invoke getAppProperty on org.rdk.AppManager with appId: "", key: "InvalidKey"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_emptykey"></a>
### TestCase Name
AppManager_GetAppProperty_EmptyAppId_EmptyKey

### TestCase ID
AM_86

### TestCase Objective
Verify getAppProperty with empty appId and empty key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Empty Params | Invoke getAppProperty on org.rdk.AppManager with appId: "", key: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_max_running_apps"></a>
### TestCase Name
AppManager_Max_Running_Apps

### TestCase ID
AM_87

### TestCase Objective
Verify the successful retrieval of the maximum number of running apps

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Max Running Apps | Invoke getMaxRunningApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getMaxRunningApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the max running apps count is returned successfully |

---

<a id="appmanager_getappproperty_validappid_validkey_pinlock"></a>
### TestCase Name
AppManager_GetAppProperty_ValidAppId_ValidKey_Pinlock

### TestCase ID
AM_88

### TestCase Objective
Verify getAppProperty with valid appId and valid key as pinlock

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Valid Params | Invoke getAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "pinlock"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "pinlock"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with empty/null response |

---

<a id="appmanager_getappproperty_validappid_validkey_inactivepriority"></a>
### TestCase Name
AppManager_GetAppProperty_ValidAppId_ValidKey_InactivePriority

### TestCase ID
AM_89

### TestCase Objective
Verify getAppProperty with valid appId and valid key as inactivePriority

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Valid Params | Invoke getAppProperty on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", key: "inactivePriority"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "inactivePriority"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with empty/null response |

---

<a id="appmanager_getappproperty_numericappid_numerickey"></a>
### TestCase Name
AppManager_GetAppProperty_NumericAppId_NumericKey

### TestCase ID
AM_90

### TestCase Objective
Verify getAppProperty with numeric appId and numeric key

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Numeric Params | Invoke getAppProperty on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": 123, "key": 456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_valid_appid"></a>
### TestCase Name
AppManager_ActivateSystemApp_Valid_AppId

### TestCase ID
AM_91

### TestCase Objective
Verify activateSystemApp with a valid appId of an installed device application

### TestCase Pre-condition

#### TestCase Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Start System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App | Invoke activateSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Stop System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_activatesystemapp_invalid_appid"></a>
### TestCase Name
AppManager_ActivateSystemApp_Invalid_AppId

### TestCase ID
AM_92

### TestCase Objective
Verify activateSystemApp with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Invalid AppId | Invoke activateSystemApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_empty_appid"></a>
### TestCase Name
AppManager_ActivateSystemApp_Empty_AppId

### TestCase ID
AM_93

### TestCase Objective
Verify activateSystemApp with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Empty AppId | Invoke activateSystemApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_special_char_appid"></a>
### TestCase Name
AppManager_ActivateSystemApp_Special_Char_AppId

### TestCase ID
AM_94

### TestCase Objective
Verify activateSystemApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Special Char | Invoke activateSystemApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_numeric_appid"></a>
### TestCase Name
AppManager_ActivateSystemApp_Numeric_AppId

### TestCase ID
AM_95

### TestCase Objective
Verify activateSystemApp with an appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Numeric AppId | Invoke activateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_without_param"></a>
### TestCase Name
AppManager_ActivateSystemApp_Without_Param

### TestCase ID
AM_96

### TestCase Objective
Verify activateSystemApp fails gracefully when called without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Without Param | Invoke activateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_valid_appid"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Valid_AppId

### TestCase ID
AM_97

### TestCase Objective
Verify deactivateSystemApp with a valid appId of an installed device application

### TestCase Pre-condition

#### TestCase Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Start System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Activate System App | Activate System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App | Invoke deactivateSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Stop System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_deactivatesystemapp_invalid_appid"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Invalid_AppId

### TestCase ID
AM_98

### TestCase Objective
Verify deactivateSystemApp with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Invalid AppId | Invoke deactivateSystemApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_empty_appid"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Empty_AppId

### TestCase ID
AM_99

### TestCase Objective
Verify deactivateSystemApp with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Empty AppId | Invoke deactivateSystemApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_special_char_appid"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Special_Char_AppId

### TestCase ID
AM_100

### TestCase Objective
Verify deactivateSystemApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Special Char | Invoke deactivateSystemApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_numeric_appid"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Numeric_AppId

### TestCase ID
AM_101

### TestCase Objective
Verify deactivateSystemApp with an appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Numeric AppId | Invoke deactivateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_without_param"></a>
### TestCase Name
AppManager_DeactivateSystemApp_Without_Param

### TestCase ID
AM_102

### TestCase Objective
Verify deactivateSystemApp fails gracefully when called without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Without Param | Invoke deactivateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_valid_appid"></a>
### TestCase Name
AppManager_HibernateSystemApp_Valid_AppId

### TestCase ID
AM_103

### TestCase Objective
Verify hibernateSystemApp with a valid appId of an installed device application

### TestCase Pre-condition

#### TestCase Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Start System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Activate System App | Activate System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App | Invoke hibernateSystemApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Stop System App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_hibernatesystemapp_invalid_appid"></a>
### TestCase Name
AppManager_HibernateSystemApp_Invalid_AppId

### TestCase ID
AM_104

### TestCase Objective
Verify hibernateSystemApp with an invalid appId that does not exist in the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Invalid AppId | Invoke hibernateSystemApp on org.rdk.AppManager with appId: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_empty_appid"></a>
### TestCase Name
AppManager_HibernateSystemApp_Empty_AppId

### TestCase ID
AM_105

### TestCase Objective
Verify hibernateSystemApp with an empty string as appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Empty AppId | Invoke hibernateSystemApp on org.rdk.AppManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_special_char_appid"></a>
### TestCase Name
AppManager_HibernateSystemApp_Special_Char_AppId

### TestCase ID
AM_106

### TestCase Objective
Verify hibernateSystemApp with a appId containing special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Special Char | Invoke hibernateSystemApp on org.rdk.AppManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_numeric_appid"></a>
### TestCase Name
AppManager_HibernateSystemApp_Numeric_AppId

### TestCase ID
AM_107

### TestCase Objective
Verify hibernateSystemApp with an appId containing only numeric characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Numeric AppId | Invoke hibernateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_without_param"></a>
### TestCase Name
AppManager_HibernateSystemApp_Without_Param

### TestCase ID
AM_108

### TestCase Objective
Verify hibernateSystemApp fails gracefully when called without parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Without Param | Invoke hibernateSystemApp on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_max_inactive_ramusage"></a>
### TestCase Name
AppManager_Max_Inactive_Ramusage

### TestCase ID
AM_109

### TestCase Objective
Verify the successful retrieval of the maximum inactive ram usage

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Max Inactive Ramusage | Invoke getMaxInactiveRamUsage on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getMaxInactiveRamUsage"}' http://127.0.0.1:9998/jsonrpc` | Verify that the max inactive ram usage is returned successfully |

---

<a id="appmanager_app_lock_launch_terminate_unlock_operations"></a>
### TestCase Name
AppManager_App_Lock_Launch_Terminate_Unlock_Operations

### TestCase ID
AM_L2_01

### TestCase Objective
Verify that an app can be launched successfully after performing lock operation on the device

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package ValidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Launch App After Lock | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 4 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_terminate_lock_unlock_operations"></a>
### TestCase Name
AppManager_App_Launch_Terminate_Lock_Unlock_Operations

### TestCase ID
AM_L2_02

### TestCase Objective
Verify that an app can be launch, terminate, lock and unlock successfully

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 3 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_kill_lock_unlock_operations"></a>
### TestCase Name
AppManager_App_Launch_Kill_Lock_Unlock_Operations

### TestCase ID
AM_L2_03

### TestCase Objective
Verify that an app can be launch, kill, lock and unlock successfully

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 3 | Kill App Valid Param | Invoke killApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_close_lock_unlock_operations"></a>
### TestCase Name
AppManager_App_Launch_Close_Lock_Unlock_Operations

### TestCase ID
AM_L2_04

### TestCase Objective
Verify that an app can be launch, close, lock and unlock successfully

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 3 | Close App Valid Params | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke lock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>", lockReason: "TestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke unlock on org.rdk.PackageManagerRDKEMS with packageId: "<PACKAGEMANAGER_APPLICATION_NAME>", version: "<PACKAGEMANAGER_APPLICATION_VERSION>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_close"></a>
### TestCase Name
AppManager_Check_On_AppLifecycleStateChanged_Event_After_Close

### TestCase ID
AM_L2_05

### TestCase Objective
Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, closed

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Close App Valid Params | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Close | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 5 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_kill"></a>
### TestCase Name
AppManager_Check_On_AppLifecycleStateChanged_Event_After_Kill

### TestCase ID
AM_L2_06

### TestCase Objective
Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, killed

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Kill App Valid Param | Invoke killApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Kill | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_terminate"></a>
### TestCase Name
AppManager_Check_On_AppLifecycleStateChanged_Event_After_Terminate

### TestCase ID
AM_L2_07

### TestCase Objective
Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, terminated

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Terminate | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |

---

<a id="appmanager_app_launch_twice"></a>
### TestCase Name
AppManager_App_Launch_Twice

### TestCase ID
AM_L2_08

### TestCase Objective
Check that an app can be launched successfully after terminating the app which is launched previously

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App First Time | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Launch App Second Time | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 6 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_launch"></a>
### TestCase Name
AppManager_Check_Get_Loaded_Apps_After_Launch

### TestCase ID
AM_L2_09

### TestCase Objective
Verify that the launched app is reflected in the list of loaded apps

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Get Loaded Apps After Launch | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_close"></a>
### TestCase Name
AppManager_Check_Get_Loaded_Apps_After_Close

### TestCase ID
AM_L2_10

### TestCase Objective
Verify_that the closed app is no longer reflected in the list of loaded apps

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Close App Valid Param | Invoke closeApp on org.rdk.LifecycleManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Close | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_kill"></a>
### TestCase Name
AppManager_Check_Get_Loaded_Apps_After_Kill

### TestCase ID
AM_L2_11

### TestCase Objective
Verify that the killed app is no longer reflected in the list of loaded apps

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Kill App Valid Param | Invoke killApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Kill | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

---

<a id="appmanager_check_get_loaded_apps_after_terminate"></a>
### TestCase Name
AppManager_Check_Get_Loaded_Apps_After_Terminate

### TestCase ID
AM_L2_12

### TestCase Objective
Verify that the terminated app is no longer reflected in the list of loaded apps

### TestCase Pre-condition

#### TestCase Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke launchApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event Event_On_App_Lifecycle_State_Changed | Verify that event data is validated successfully |
| 3 | Terminate App Valid Param | Invoke terminateApp on org.rdk.AppManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Terminate | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

---

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Get Loaded Apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate App Valid Param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check Package Info | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M147 |
