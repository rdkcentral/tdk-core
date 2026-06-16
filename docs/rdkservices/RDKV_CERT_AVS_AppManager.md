## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [AppManager_Check_Response_Get_Installed_Apps (AM_01)](#appmanager_check_response_get_installed_apps-am_01)
   - [AppManager_Verify_IsInstalled_Valid_AppId (AM_02)](#appmanager_verify_isinstalled_valid_appid-am_02)
   - [AppManager_Verify_IsInstalled_With_Invalid_AppId (AM_03)](#appmanager_verify_isinstalled_with_invalid_appid-am_03)
   - [AppManager_Verify_IsInstalled_Empty_AppId (AM_04)](#appmanager_verify_isinstalled_empty_appid-am_04)
   - [AppManager_Verify_IsInstalled_NonExistent_AppId (AM_05)](#appmanager_verify_isinstalled_nonexistent_appid-am_05)
   - [AppManager_Verify_IsInstalled_Numeric_AppId (AM_06)](#appmanager_verify_isinstalled_numeric_appid-am_06)
   - [AppManager_Verify_IsInstalled_SpecialChar_AppId (AM_07)](#appmanager_verify_isinstalled_specialchar_appid-am_07)
   - [AppManager_Verify_IsInstalled_Long_AppId (AM_08)](#appmanager_verify_isinstalled_long_appid-am_08)
   - [AppManager_Verify_IsInstalled_With_Whitespace_AppId (AM_09)](#appmanager_verify_isinstalled_with_whitespace_appid-am_09)
   - [AppManager_Verify_IsInstalled_Mixed_Alphanumeric_SpecialChars (AM_10)](#appmanager_verify_isinstalled_mixed_alphanumeric_specialchars-am_10)
   - [AppManager_Check_Response_Get_Loaded_Apps (AM_11)](#appmanager_check_response_get_loaded_apps-am_11)
   - [AppManager_LaunchApp_Valid_Param (AM_12)](#appmanager_launchapp_valid_param-am_12)
   - [AppManager_LaunchApp_Invalid_AppId (AM_13)](#appmanager_launchapp_invalid_appid-am_13)
   - [AppManager_LaunchApp_Invalid_Intent (AM_14)](#appmanager_launchapp_invalid_intent-am_14)
   - [AppManager_LaunchApp_Invalid_LaunchArgs (AM_15)](#appmanager_launchapp_invalid_launchargs-am_15)
   - [AppManager_LaunchApp_Invalid_Params (AM_16)](#appmanager_launchapp_invalid_params-am_16)
   - [AppManager_LaunchApp_Empty_AppId (AM_17)](#appmanager_launchapp_empty_appid-am_17)
   - [AppManager_LaunchApp_Fail_Gracefully_Empty_Intent (AM_18)](#appmanager_launchapp_fail_gracefully_empty_intent-am_18)
   - [AppManager_LaunchApp_Fail_Gracefully_Empty_LaunchArgs (AM_19)](#appmanager_launchapp_fail_gracefully_empty_launchargs-am_19)
   - [AppManager_LaunchApp_Fail_Gracefully_Without_Params (AM_20)](#appmanager_launchapp_fail_gracefully_without_params-am_20)
   - [AppManager_LaunchApp_EdgeCase_LongStrings (AM_21)](#appmanager_launchapp_edgecase_longstrings-am_21)
   - [AppManager_Verify_PreloadApp_Valid_Param (AM_22)](#appmanager_verify_preloadapp_valid_param-am_22)
   - [AppManager_PreloadApp_Empty_AppId (AM_23)](#appmanager_preloadapp_empty_appid-am_23)
   - [AppManager_PreloadApp_Empty_LaunchArgs (AM_24)](#appmanager_preloadapp_empty_launchargs-am_24)
   - [AppManager_PreloadApp_Special_Char_AppId (AM_25)](#appmanager_preloadapp_special_char_appid-am_25)
   - [AppManager_PreloadApp_Special_Char_LaunchArgs (AM_26)](#appmanager_preloadapp_special_char_launchargs-am_26)
   - [AppManager_Verify_PreloadApp_with_Numeric_AppId (AM_27)](#appmanager_verify_preloadapp_with_numeric_appid-am_27)
   - [AppManager_PreloadApp_Numeric_LaunchArgs (AM_28)](#appmanager_preloadapp_numeric_launchargs-am_28)
   - [AppManager_Verify_PreloadApp_with_Alphanumeric_AppId (AM_29)](#appmanager_verify_preloadapp_with_alphanumeric_appid-am_29)
   - [AppManager_Verify_PreloadApp_with_Alphanumeric_LaunchArgs (AM_30)](#appmanager_verify_preloadapp_with_alphanumeric_launchargs-am_30)
   - [AppManager_PreloadApp_Valid_AppId_Already_Preloaded (AM_31)](#appmanager_preloadapp_valid_appid_already_preloaded-am_31)
   - [AppManager_CloseApp_Valid_AppId (AM_32)](#appmanager_closeapp_valid_appid-am_32)
   - [AppManager_CloseApp_Invalid_AppId (AM_33)](#appmanager_closeapp_invalid_appid-am_33)
   - [AppManager_CloseApp_Empty_AppId (AM_34)](#appmanager_closeapp_empty_appid-am_34)
   - [AppManager_CloseApp_Special_Char_AppId (AM_35)](#appmanager_closeapp_special_char_appid-am_35)
   - [AppManager_CloseApp_ValidAppId_NotLoaded (AM_36)](#appmanager_closeapp_validappid_notloaded-am_36)
   - [AppManager_TerminateApp_Valid_AppId_Param (AM_37)](#appmanager_terminateapp_valid_appid_param-am_37)
   - [AppManager_TerminateApp_Invalid_AppId (AM_38)](#appmanager_terminateapp_invalid_appid-am_38)
   - [AppManager_TerminateApp_Empty_AppId (AM_39)](#appmanager_terminateapp_empty_appid-am_39)
   - [AppManager_TerminateApp_Numeric_AppId (AM_40)](#appmanager_terminateapp_numeric_appid-am_40)
   - [AppManager_TerminateApp_Special_Char_AppId (AM_41)](#appmanager_terminateapp_special_char_appid-am_41)
   - [AppManager_StartSystemApp_Valid_AppId (AM_42)](#appmanager_startsystemapp_valid_appid-am_42)
   - [AppManager_StartSystemApp_Invalid_AppId (AM_43)](#appmanager_startsystemapp_invalid_appid-am_43)
   - [AppManager_StartSystemApp_Empty_AppId (AM_44)](#appmanager_startsystemapp_empty_appid-am_44)
   - [AppManager_StartSystemApp_Special_Char_AppId (AM_45)](#appmanager_startsystemapp_special_char_appid-am_45)
   - [AppManager_StartSystemApp_Numeric_AppId (AM_46)](#appmanager_startsystemapp_numeric_appid-am_46)
   - [AppManager_StopSystemApp_Valid_AppId (AM_47)](#appmanager_stopsystemapp_valid_appid-am_47)
   - [AppManager_StopSystemApp_Valid_AppId_Already_Stopped (AM_48)](#appmanager_stopsystemapp_valid_appid_already_stopped-am_48)
   - [AppManager_StopSystemApp_Invalid_AppId (AM_49)](#appmanager_stopsystemapp_invalid_appid-am_49)
   - [AppManager_StopSystemApp_Empty_AppId (AM_50)](#appmanager_stopsystemapp_empty_appid-am_50)
   - [AppManager_StopSystemApp_Special_Char_AppId (AM_51)](#appmanager_stopsystemapp_special_char_appid-am_51)
   - [AppManager_StopSystemApp_Numeric_AppId (AM_52)](#appmanager_stopsystemapp_numeric_appid-am_52)
   - [AppManager_StopSystemApp_Alphanumeric_AppId (AM_53)](#appmanager_stopsystemapp_alphanumeric_appid-am_53)
   - [AppManager_KillApp_Valid_AppId (AM_54)](#appmanager_killapp_valid_appid-am_54)
   - [AppManager_KillApp_Invalid_AppId (AM_55)](#appmanager_killapp_invalid_appid-am_55)
   - [AppManager_KillApp_Empty_AppId (AM_56)](#appmanager_killapp_empty_appid-am_56)
   - [AppManager_KillApp_Numeric_AppId (AM_57)](#appmanager_killapp_numeric_appid-am_57)
   - [AppManager_KillApp_Special_Char_AppId (AM_58)](#appmanager_killapp_special_char_appid-am_58)
   - [AppManager_Send_Intent_Valid_Params (AM_59)](#appmanager_send_intent_valid_params-am_59)
   - [AppManager_SendIntent_ValidAppId_EmptyIntent (AM_60)](#appmanager_sendintent_validappid_emptyintent-am_60)
   - [AppManager_SendIntent_EmptyAppId_ValidIntent (AM_61)](#appmanager_sendintent_emptyappid_validintent-am_61)
   - [AppManager_SendIntent_Empty_Params (AM_62)](#appmanager_sendintent_empty_params-am_62)
   - [AppManager_SendIntent_Invalid_AppId (AM_63)](#appmanager_sendintent_invalid_appid-am_63)
   - [AppManager_Clear_App_Data_Valid_AppId (AM_64)](#appmanager_clear_app_data_valid_appid-am_64)
   - [AppManager_Clear_App_Data_Invalid_AppId (AM_65)](#appmanager_clear_app_data_invalid_appid-am_65)
   - [AppManager_ClearAppData_Empty_AppId (AM_66)](#appmanager_clearappdata_empty_appid-am_66)
   - [AppManager_ClearAppData_SpecialCharacters (AM_67)](#appmanager_clearappdata_specialcharacters-am_67)
   - [AppManager_ClearAppData_Long_AppId (AM_68)](#appmanager_clearappdata_long_appid-am_68)
   - [ClearAppData_Numeric_AppId (AM_69)](#clearappdata_numeric_appid-am_69)
   - [AppManager_ClearAppData_Alphanumeric_AppId (AM_70)](#appmanager_clearappdata_alphanumeric_appid-am_70)
   - [AppManager_Clear_All_App_Data (AM_71)](#appmanager_clear_all_app_data-am_71)
   - [AppManager_SetAppProperty_ValidAppId_Delay_10 (AM_72)](#appmanager_setappproperty_validappid_delay_10-am_72)
   - [AppManager_SetAppProperty_Empty_AppId_Key_Value (AM_73)](#appmanager_setappproperty_empty_appid_key_value-am_73)
   - [AppManager_SetAppProperty_Numeric_AppId_Key_Value (AM_74)](#appmanager_setappproperty_numeric_appid_key_value-am_74)
   - [AppManager_SetAppProperty_SpecialChars_All_Params (AM_75)](#appmanager_setappproperty_specialchars_all_params-am_75)
   - [AppManager_SetAppProperty_InvalidAppId_ValidKey_ValidValue (AM_76)](#appmanager_setappproperty_invalidappid_validkey_validvalue-am_76)
   - [AppManager_SetAppProperty_ValidAppId_InvalidKey_ValidValue (AM_77)](#appmanager_setappproperty_validappid_invalidkey_validvalue-am_77)
   - [AppManager_SetAppProperty_ValidAppId_EmptyKey_ValidValue (AM_78)](#appmanager_setappproperty_validappid_emptykey_validvalue-am_78)
   - [AppManager_GetAppProperty_ValidAppId_InvalidKey (AM_79)](#appmanager_getappproperty_validappid_invalidkey-am_79)
   - [AppManager_GetAppProperty_ValidAppId_EmptyKey (AM_80)](#appmanager_getappproperty_validappid_emptykey-am_80)
   - [AppManager_GetAppProperty_Invalid_AppId_Valid_Key (AM_81)](#appmanager_getappproperty_invalid_appid_valid_key-am_81)
   - [AppManager_GetAppProperty_Invalid_Params (AM_82)](#appmanager_getappproperty_invalid_params-am_82)
   - [AppManager_GetAppProperty_InvalidAppId_EmptyKey (AM_83)](#appmanager_getappproperty_invalidappid_emptykey-am_83)
   - [AppManager_GetAppProperty_EmptyAppId_ValidKey (AM_84)](#appmanager_getappproperty_emptyappid_validkey-am_84)
   - [AppManager_GetAppProperty_EmptyAppId_InvalidKey (AM_85)](#appmanager_getappproperty_emptyappid_invalidkey-am_85)
   - [AppManager_GetAppProperty_EmptyAppId_EmptyKey (AM_86)](#appmanager_getappproperty_emptyappid_emptykey-am_86)
   - [AppManager_Max_Running_Apps (AM_87)](#appmanager_max_running_apps-am_87)
   - [AppManager_GetAppProperty_ValidAppId_ValidKey_Pinlock (AM_88)](#appmanager_getappproperty_validappid_validkey_pinlock-am_88)
   - [AppManager_GetAppProperty_ValidAppId_ValidKey_InactivePriority (AM_89)](#appmanager_getappproperty_validappid_validkey_inactivepriority-am_89)
   - [AppManager_GetAppProperty_NumericAppId_NumericKey (AM_90)](#appmanager_getappproperty_numericappid_numerickey-am_90)
   - [AppManager_ActivateSystemApp_Valid_AppId (AM_91)](#appmanager_activatesystemapp_valid_appid-am_91)
   - [AppManager_ActivateSystemApp_Invalid_AppId (AM_92)](#appmanager_activatesystemapp_invalid_appid-am_92)
   - [AppManager_ActivateSystemApp_Empty_AppId (AM_93)](#appmanager_activatesystemapp_empty_appid-am_93)
   - [AppManager_ActivateSystemApp_Special_Char_AppId (AM_94)](#appmanager_activatesystemapp_special_char_appid-am_94)
   - [AppManager_ActivateSystemApp_Numeric_AppId (AM_95)](#appmanager_activatesystemapp_numeric_appid-am_95)
   - [AppManager_ActivateSystemApp_Without_Param (AM_96)](#appmanager_activatesystemapp_without_param-am_96)
   - [AppManager_DeactivateSystemApp_Valid_AppId (AM_97)](#appmanager_deactivatesystemapp_valid_appid-am_97)
   - [AppManager_DeactivateSystemApp_Invalid_AppId (AM_98)](#appmanager_deactivatesystemapp_invalid_appid-am_98)
   - [AppManager_DeactivateSystemApp_Empty_AppId (AM_99)](#appmanager_deactivatesystemapp_empty_appid-am_99)
   - [AppManager_DeactivateSystemApp_Special_Char_AppId (AM_100)](#appmanager_deactivatesystemapp_special_char_appid-am_100)
   - [AppManager_DeactivateSystemApp_Numeric_AppId (AM_101)](#appmanager_deactivatesystemapp_numeric_appid-am_101)
   - [AppManager_DeactivateSystemApp_Without_Param (AM_102)](#appmanager_deactivatesystemapp_without_param-am_102)
   - [AppManager_HibernateSystemApp_Valid_AppId (AM_103)](#appmanager_hibernatesystemapp_valid_appid-am_103)
   - [AppManager_HibernateSystemApp_Invalid_AppId (AM_104)](#appmanager_hibernatesystemapp_invalid_appid-am_104)
   - [AppManager_HibernateSystemApp_Empty_AppId (AM_105)](#appmanager_hibernatesystemapp_empty_appid-am_105)
   - [AppManager_HibernateSystemApp_Special_Char_AppId (AM_106)](#appmanager_hibernatesystemapp_special_char_appid-am_106)
   - [AppManager_HibernateSystemApp_Numeric_AppId (AM_107)](#appmanager_hibernatesystemapp_numeric_appid-am_107)
   - [AppManager_HibernateSystemApp_Without_Param (AM_108)](#appmanager_hibernatesystemapp_without_param-am_108)
   - [AppManager_App_Lock_Launch_Terminate_Unlock_Operations (AM_L2_01)](#appmanager_app_lock_launch_terminate_unlock_operations-am_l2_01)
   - [AppManager_App_Launch_Terminate_Lock_Unlock_Operations (AM_L2_02)](#appmanager_app_launch_terminate_lock_unlock_operations-am_l2_02)
   - [AppManager_App_Launch_Kill_Lock_Unlock_Operations (AM_L2_03)](#appmanager_app_launch_kill_lock_unlock_operations-am_l2_03)
   - [AppManager_App_Launch_Close_Lock_Unlock_Operations (AM_L2_04)](#appmanager_app_launch_close_lock_unlock_operations-am_l2_04)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Close (AM_L2_05)](#appmanager_check_on_applifecyclestatechanged_event_after_close-am_l2_05)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Kill (AM_L2_06)](#appmanager_check_on_applifecyclestatechanged_event_after_kill-am_l2_06)
   - [AppManager_Check_On_AppLifecycleStateChanged_Event_After_Terminate (AM_L2_07)](#appmanager_check_on_applifecyclestatechanged_event_after_terminate-am_l2_07)
   - [AppManager_App_Launch_Twice (AM_L2_08)](#appmanager_app_launch_twice-am_l2_08)
   - [AppManager_Check_Get_Loaded_Apps_After_Launch (AM_L2_09)](#appmanager_check_get_loaded_apps_after_launch-am_l2_09)
   - [AppManager_Check_Get_Loaded_Apps_After_Close (AM_L2_10)](#appmanager_check_get_loaded_apps_after_close-am_l2_10)
   - [AppManager_Check_Get_Loaded_Apps_After_Kill (AM_L2_11)](#appmanager_check_get_loaded_apps_after_kill-am_l2_11)
   - [AppManager_Check_Get_Loaded_Apps_After_Terminate (AM_L2_12)](#appmanager_check_get_loaded_apps_after_terminate-am_l2_12)
4. [Post-conditions](#post-conditions)
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

### APIs Under Test

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

### Events Under Test

| Event | Description |
|-------|-------------|
| `onAppLifecycleStateChanged` | Triggered whenever there is a change in the lifecycle state of a running application |

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

### Pre-condition 5: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_4>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

### Pre-condition 6: Register_And_Listen_Events

- Register and listen to event `Event_On_App_Lifecycle_State_Changed` on `AppManager` plugin

---

## Test Cases

<a id="appmanager_check_response_get_installed_apps-am_01"></a>
### AppManager_Check_Response_Get_Installed_Apps (AM_01)

**Objective:** Check the response when applications are installed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Installed Apps | Invoke `getInstalledApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getInstalledApps"}' http://127.0.0.1:9998/jsonrpc` | Installed applications should appear in the list |

---

<a id="appmanager_verify_isinstalled_valid_appid-am_02"></a>
### AppManager_Verify_IsInstalled_Valid_AppId (AM_02)

**Objective:** Verify isInstalled with a valid appId of an installed application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `true` |

---

<a id="appmanager_verify_isinstalled_with_invalid_appid-am_03"></a>
### AppManager_Verify_IsInstalled_With_Invalid_AppId (AM_03)

**Objective:** Verify isInstalled with an invalid appId of an application that is not installed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled With Invalid AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_empty_appid-am_04"></a>
### AppManager_Verify_IsInstalled_Empty_AppId (AM_04)

**Objective:** Verify isInstalled with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Empty AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_isinstalled_nonexistent_appid-am_05"></a>
### AppManager_Verify_IsInstalled_NonExistent_AppId (AM_05)

**Objective:** Verify isInstalled with a non-existent appId (e.g., random string)

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled NonExistent AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"zxcvbasdfg"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "zxcvbasdfg"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_numeric_appid-am_06"></a>
### AppManager_Verify_IsInstalled_Numeric_AppId (AM_06)

**Objective:** Verify isInstalled with a numeric value as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Numeric AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_specialchar_appid-am_07"></a>
### AppManager_Verify_IsInstalled_SpecialChar_AppId (AM_07)

**Objective:** Verify isInstalled with a special character string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled SpecialChar AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_long_appid-am_08"></a>
### AppManager_Verify_IsInstalled_Long_AppId (AM_08)

**Objective:** Verify isInstalled with a very long string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Long AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "VeryLongStringForAppIdTestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_with_whitespace_appid-am_09"></a>
### AppManager_Verify_IsInstalled_With_Whitespace_AppId (AM_09)

**Objective:** Verify isInstalled with a appId containing spaces or whitespace characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled Whitespace AppId | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"App Id"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "App Id"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_verify_isinstalled_mixed_alphanumeric_specialchars-am_10"></a>
### AppManager_Verify_IsInstalled_Mixed_Alphanumeric_SpecialChars (AM_10)

**Objective:** Verify isInstalled with a appId containing mixed alphanumeric and special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify IsInstalled | Invoke `isInstalled` on `org.rdk.AppManager` with `appId`: `"MixedAlphaNum@123!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.isInstalled", "params": {"appId": "MixedAlphaNum@123!"}}' http://127.0.0.1:9998/jsonrpc` | Installed status matches expected value `false` |

---

<a id="appmanager_check_response_get_loaded_apps-am_11"></a>
### AppManager_Check_Response_Get_Loaded_Apps (AM_11)

**Objective:** Retrieves a list of applications currently loaded

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Ensure the getLoadedApps API responds without errors when no applications are running, and provides a non-empty response when applications are active |

---

<a id="appmanager_launchapp_valid_param-am_12"></a>
### AppManager_LaunchApp_Valid_Param (AM_12)

**Objective:** Verify that the launchApp method successfully launches an application when provided with a valid appId

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Param | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_launchapp_invalid_appid-am_13"></a>
### AppManager_LaunchApp_Invalid_AppId (AM_13)

**Objective:** Verify that the launchApp method fails gracefully when an invalid appId is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid AppId | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_intent-am_14"></a>
### AppManager_LaunchApp_Invalid_Intent (AM_14)

**Objective:** Verify that the launchApp method fails gracefully when an invalid intent is provided, while appId is valid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid Intent | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `"InvalidIntent"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "InvalidIntent"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_launchargs-am_15"></a>
### AppManager_LaunchApp_Invalid_LaunchArgs (AM_15)

**Objective:** Verify that the launchApp method fails gracefully when an invalid launchArgs is provided, while appId is valid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid LaunchArgs | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `"InvalidSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "InvalidSource"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_invalid_params-am_16"></a>
### AppManager_LaunchApp_Invalid_Params (AM_16)

**Objective:** Verify that the launchApp method fails gracefully when all parameters appId, intent, and launchArgs are invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Invalid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`, `intent`: `"InvalidIntent"`, `launchArgs`: `"InvalidSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "InvalidAppId", "intent": "InvalidIntent", "launchArgs": "InvalidSource"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_empty_appid-am_17"></a>
### AppManager_LaunchApp_Empty_AppId (AM_17)

**Objective:** Verify that the launchApp method fails gracefully when the appId parameter is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty AppId | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_empty_intent-am_18"></a>
### AppManager_LaunchApp_Fail_Gracefully_Empty_Intent (AM_18)

**Objective:** Verify that the launchApp method fails gracefully when the intent parameter is empty, while appId is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty Intent | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_empty_launchargs-am_19"></a>
### AppManager_LaunchApp_Fail_Gracefully_Empty_LaunchArgs (AM_19)

**Objective:** Verify that the launchApp method fails gracefully when the launchArgs parameter is empty, while appId is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Empty LaunchArgs | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_fail_gracefully_without_params-am_20"></a>
### AppManager_LaunchApp_Fail_Gracefully_Without_Params (AM_20)

**Objective:** Verify that the launchApp method fails gracefully when all parameters appId, intent, and launchArgs are missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Without Params | Invoke `launchApp` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_launchapp_edgecase_longstrings-am_21"></a>
### AppManager_LaunchApp_EdgeCase_LongStrings (AM_21)

**Objective:** Verify that the launchApp method handles edge cases, such as extremely long strings for appId, intent, and launchArgs, without crashing or unexpected behavior

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Long Strings | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"A_very_long_string_exceeding_normal_limits_for_testing_purposes_appId"`, `intent`: `"A_very_long_string_exceeding_normal_limits_for_testing_purposes_intent"`, `launchArgs`: `"A_very_long_string_exceeding_normal_limits_for_testing_purposes_source"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_appId", "intent": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_intent", "launchArgs": "A_very_long_string_exceeding_normal_limits_for_testing_purposes_source"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_valid_param-am_22"></a>
### AppManager_Verify_PreloadApp_Valid_Param (AM_22)

**Objective:** Verify preloadApp with a valid param when provided with a valid appId

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Valid Param | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_preloadapp_empty_appid-am_23"></a>
### AppManager_PreloadApp_Empty_AppId (AM_23)

**Objective:** Verify preloadApp with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Empty AppId | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_empty_launchargs-am_24"></a>
### AppManager_PreloadApp_Empty_LaunchArgs (AM_24)

**Objective:** Verify preloadApp with an empty string as launchArgs

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Empty LaunchArgs | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_special_char_appid-am_25"></a>
### AppManager_PreloadApp_Special_Char_AppId (AM_25)

**Objective:** Verify preloadApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Preload App Special Char AppId | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_special_char_launchargs-am_26"></a>
### AppManager_PreloadApp_Special_Char_LaunchArgs (AM_26)

**Objective:** Verify preloadApp with launchArgs containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Special Char LaunchArgs | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `"()*^!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "()*^!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_numeric_appid-am_27"></a>
### AppManager_Verify_PreloadApp_with_Numeric_AppId (AM_27)

**Objective:** Verify preloadApp with a appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Numeric AppId | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `123456`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": 123456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_numeric_launchargs-am_28"></a>
### AppManager_PreloadApp_Numeric_LaunchArgs (AM_28)

**Objective:** Verify preloadApp with launchArgs containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Preload App Numeric LaunchArgs | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `123456`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": 123456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_alphanumeric_appid-am_29"></a>
### AppManager_Verify_PreloadApp_with_Alphanumeric_AppId (AM_29)

**Objective:** Verify preloadApp with an appId containing a mix of alphanumeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Alphanumeric AppId | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"abc123XYZ"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "abc123XYZ"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message`ERROR_GENERAL` |

---

<a id="appmanager_verify_preloadapp_with_alphanumeric_launchargs-am_30"></a>
### AppManager_Verify_PreloadApp_with_Alphanumeric_LaunchArgs (AM_30)

**Objective:** Verify preloadApp with launchArgs containing a mix of alphanumeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp with Alphanumeric LaunchArgs | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `launchArgs`: `"arg1Value2Test3"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "launchArgs": "arg1Value2Test3"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_preloadapp_valid_appid_already_preloaded-am_31"></a>
### AppManager_PreloadApp_Valid_AppId_Already_Preloaded (AM_31)

**Objective:** Verify preloadApp with a appId that is a valid application but is already preloaded

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | PreloadApp Valid AppId | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 3 | PreloadApp Valid AppId Already Preloaded | Invoke `preloadApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.preloadApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_closeapp_valid_appid-am_32"></a>
### AppManager_CloseApp_Valid_AppId (AM_32)

**Objective:** Verify closeApp with valid appId

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Valid Params | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Terminate_Application

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_closeapp_invalid_appid-am_33"></a>
### AppManager_CloseApp_Invalid_AppId (AM_33)

**Objective:** Verify closeApp with an invalid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Invalid AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_empty_appid-am_34"></a>
### AppManager_CloseApp_Empty_AppId (AM_34)

**Objective:** Verify closeApp with an empty appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Empty AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_special_char_appid-am_35"></a>
### AppManager_CloseApp_Special_Char_AppId (AM_35)

**Objective:** Verify closeApp with an appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Special Char AppId | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_closeapp_validappid_notloaded-am_36"></a>
### AppManager_CloseApp_ValidAppId_NotLoaded (AM_36)

**Objective:** Verify closeApp with an appId that is valid but the app is not loaded in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Close App Valid NotLoaded | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"Cobalt"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "Cobalt"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_valid_appid_param-am_37"></a>
### AppManager_TerminateApp_Valid_AppId_Param (AM_37)

**Objective:** Verify terminateApp with valid appId

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_terminateapp_invalid_appid-am_38"></a>
### AppManager_TerminateApp_Invalid_AppId (AM_38)

**Objective:** Verify terminateApp with an invalid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Invalid AppId | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_empty_appid-am_39"></a>
### AppManager_TerminateApp_Empty_AppId (AM_39)

**Objective:** Verify terminateApp with an empty appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Empty AppId | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_numeric_appid-am_40"></a>
### AppManager_TerminateApp_Numeric_AppId (AM_40)

**Objective:** Verify terminateApp with an appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Numeric AppId | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_terminateapp_special_char_appid-am_41"></a>
### AppManager_TerminateApp_Special_Char_AppId (AM_41)

**Objective:** Verify terminateApp with an appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Special Char AppId | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_valid_appid-am_42"></a>
### AppManager_StartSystemApp_Valid_AppId (AM_42)

**Objective:** Verify startSystemApp with a valid appId of an installed device application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_startsystemapp_invalid_appid-am_43"></a>
### AppManager_StartSystemApp_Invalid_AppId (AM_43)

**Objective:** Verify startSystemApp with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Invalid AppId | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_empty_appid-am_44"></a>
### AppManager_StartSystemApp_Empty_AppId (AM_44)

**Objective:** Verify startSystemApp with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Empty AppId | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_special_char_appid-am_45"></a>
### AppManager_StartSystemApp_Special_Char_AppId (AM_45)

**Objective:** Verify startSystemApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Special Char | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_startsystemapp_numeric_appid-am_46"></a>
### AppManager_StartSystemApp_Numeric_AppId (AM_46)

**Objective:** Verify startSystemApp with an appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App Numeric AppId | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_valid_appid-am_47"></a>
### AppManager_StopSystemApp_Valid_AppId (AM_47)

**Objective:** Verify stopSystemApp with a valid appId of an actively running device application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_stopsystemapp_valid_appid_already_stopped-am_48"></a>
### AppManager_StopSystemApp_Valid_AppId_Already_Stopped (AM_48)

**Objective:** Verify stopSystemApp with a valid appId of a device application that is already stopped

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_invalid_appid-am_49"></a>
### AppManager_StopSystemApp_Invalid_AppId (AM_49)

**Objective:** Verify stopSystemApp with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Invalid AppId | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_empty_appid-am_50"></a>
### AppManager_StopSystemApp_Empty_AppId (AM_50)

**Objective:** Verify stopSystemApp with an empty string as the appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Empty AppId | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_special_char_appid-am_51"></a>
### AppManager_StopSystemApp_Special_Char_AppId (AM_51)

**Objective:** Verify stopSystemApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Special Char | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_numeric_appid-am_52"></a>
### AppManager_StopSystemApp_Numeric_AppId (AM_52)

**Objective:** Verify stopSystemApp with a appId containing only numeric values

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Numeric AppId | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_stopsystemapp_alphanumeric_appid-am_53"></a>
### AppManager_StopSystemApp_Alphanumeric_AppId (AM_53)

**Objective:** Verify stopSystemApp with a appId containing a mix of alphanumeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App Alphanumeric AppId | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"App123Alpha"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "App123Alpha"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_valid_appid-am_54"></a>
### AppManager_KillApp_Valid_AppId (AM_54)

**Objective:** Verify killApp with valid appId

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Valid Param | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_killapp_invalid_appid-am_55"></a>
### AppManager_KillApp_Invalid_AppId (AM_55)

**Objective:** Verify killApp with an invalid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Invalid AppId | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"InvalidApp"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "InvalidApp"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_empty_appid-am_56"></a>
### AppManager_KillApp_Empty_AppId (AM_56)

**Objective:** Verify killApp with an empty appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Empty AppId | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_numeric_appid-am_57"></a>
### AppManager_KillApp_Numeric_AppId (AM_57)

**Objective:** Verify killApp with a numeric appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Numeric AppId | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_killapp_special_char_appid-am_58"></a>
### AppManager_KillApp_Special_Char_AppId (AM_58)

**Objective:** Verify killApp with an appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Kill App Special Char AppId | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_send_intent_valid_params-am_59"></a>
### AppManager_Send_Intent_Valid_Params (AM_59)

**Objective:** Verify sendIntent with valid appId and valid intent

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Valid Params | Invoke `sendIntent` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_sendintent_validappid_emptyintent-am_60"></a>
### AppManager_SendIntent_ValidAppId_EmptyIntent (AM_60)

**Objective:** Verify sendIntent with valid appId and an empty string for intent

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent ValidAppId EmptyIntent | Invoke `sendIntent` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `intent`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_emptyappid_validintent-am_61"></a>
### AppManager_SendIntent_EmptyAppId_ValidIntent (AM_61)

**Objective:** Verify sendIntent with an empty string for appId and valid intent

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent EmptyAppId ValidIntent | Invoke `sendIntent` on `org.rdk.AppManager` with `appId`: `""`, `intent`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_empty_params-am_62"></a>
### AppManager_SendIntent_Empty_Params (AM_62)

**Objective:** Verify sendIntent with empty strings for all parameters appId and intent

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Empty Params | Invoke `sendIntent` on `org.rdk.AppManager` with `appId`: `""`, `intent`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "", "intent": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_sendintent_invalid_appid-am_63"></a>
### AppManager_SendIntent_Invalid_AppId (AM_63)

**Objective:** Verify sendIntent with invalid appId and valid intent

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Intent Invalid AppId | Invoke `sendIntent` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`, `intent`: `"start"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.sendIntent", "params": {"appId": "InvalidAppId", "intent": "start"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clear_app_data_valid_appid-am_64"></a>
### AppManager_Clear_App_Data_Valid_AppId (AM_64)

**Objective:** Verify clearAppData with a valid appId of an installed application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Valid AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_clear_app_data_invalid_appid-am_65"></a>
### AppManager_Clear_App_Data_Invalid_AppId (AM_65)

**Objective:** Verify clearAppData with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Invalid AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_empty_appid-am_66"></a>
### AppManager_ClearAppData_Empty_AppId (AM_66)

**Objective:** Verify clearAppData with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Empty AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_specialcharacters-am_67"></a>
### AppManager_ClearAppData_SpecialCharacters (AM_67)

**Objective:** Verify clearAppData with appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Special Characters | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_long_appid-am_68"></a>
### AppManager_ClearAppData_Long_AppId (AM_68)

**Objective:** Verify clearAppData with appId containing a very long string

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Long AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"A_very_long_string_characters_here"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "A_very_long_string_characters_here"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="clearappdata_numeric_appid-am_69"></a>
### ClearAppData_Numeric_AppId (AM_69)

**Objective:** Verify clearAppData with appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Numeric AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clearappdata_alphanumeric_appid-am_70"></a>
### AppManager_ClearAppData_Alphanumeric_AppId (AM_70)

**Objective:** Verify clearAppData with appId containing a mix of alphanumeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Alphanumeric AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"TestApp123"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "TestApp123"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_clear_all_app_data-am_71"></a>
### AppManager_Clear_All_App_Data (AM_71)

**Objective:** Verify that clearAllAppData successfully clears all persistent data for all installed applications when invoked

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All App Data | Invoke `clearAllAppData` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.clearAllAppData"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_setappproperty_validappid_delay_10-am_72"></a>
### AppManager_SetAppProperty_ValidAppId_Delay_10 (AM_72)

**Objective:** Verify setAppProperty sets key 'delay' to value '10' for the valid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Delay 10 | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"delay"`, `value`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "delay", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Verify Get App Property | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"delay"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | Status matches expected value: `10` |

---

<a id="appmanager_setappproperty_empty_appid_key_value-am_73"></a>
### AppManager_SetAppProperty_Empty_AppId_Key_Value (AM_73)

**Objective:** Verify setAppProperty with all parameters empty.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Empty Params | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `""`, `key`: `""`, `value`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "", "key": "", "value": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_numeric_appid_key_value-am_74"></a>
### AppManager_SetAppProperty_Numeric_AppId_Key_Value (AM_74)

**Objective:** Verify setAppProperty with numeric strings for all parameters.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property Numeric Params | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `12345`, `key`: `67890`, `value`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": 12345, "key": 67890, "value": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_specialchars_all_params-am_75"></a>
### AppManager_SetAppProperty_SpecialChars_All_Params (AM_75)

**Objective:** Verify setAppProperty with only special characters for all parameters.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property SpecialChars All | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `"()^*!"`, `key`: `"!*()"`, `value`: `"@@@"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "()^*!", "key": "!*()", "value": "@@@"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_invalidappid_validkey_validvalue-am_76"></a>
### AppManager_SetAppProperty_InvalidAppId_ValidKey_ValidValue (AM_76)

**Objective:** Verify setAppProperty with invalid appId and valid key/value.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property InvalidAppId | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `"Invalid@AppId!"`, `key`: `"delay"`, `value`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "Invalid@AppId!", "key": "delay", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_validappid_invalidkey_validvalue-am_77"></a>
### AppManager_SetAppProperty_ValidAppId_InvalidKey_ValidValue (AM_77)

**Objective:** Verify setAppProperty with valid appId, invalid key, valid value.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property InvalidKey | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"Invalid#Key"`, `value`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "Invalid#Key", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_setappproperty_validappid_emptykey_validvalue-am_78"></a>
### AppManager_SetAppProperty_ValidAppId_EmptyKey_ValidValue (AM_78)

**Objective:** Verify setAppProperty with valid appId/value and empty key.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set App Property EmptyKey | Invoke `setAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `""`, `value`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.setAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "", "value": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_validappid_invalidkey-am_79"></a>
### AppManager_GetAppProperty_ValidAppId_InvalidKey (AM_79)

**Objective:** Verify getAppProperty with valid appId and invalid key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"InvalidKey"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_validappid_emptykey-am_80"></a>
### AppManager_GetAppProperty_ValidAppId_EmptyKey (AM_80)

**Objective:** Verify getAppProperty with valid appId and empty key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalid_appid_valid_key-am_81"></a>
### AppManager_GetAppProperty_Invalid_AppId_Valid_Key (AM_81)

**Objective:** Verify getAppProperty with invalid appId and valid key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty Invalid AppId Valid Key | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`, `key`: `"delay"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalid_params-am_82"></a>
### AppManager_GetAppProperty_Invalid_Params (AM_82)

**Objective:** Verify getAppProperty with invalid appId and invalid key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetAppProperty Invalid Params | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`, `key`: `"InvalidKey"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_invalidappid_emptykey-am_83"></a>
### AppManager_GetAppProperty_InvalidAppId_EmptyKey (AM_83)

**Objective:** Verify getAppProperty with invalid appId and empty key.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property InvalidAppId EmptyKey | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`, `key`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "InvalidAppId", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_validkey-am_84"></a>
### AppManager_GetAppProperty_EmptyAppId_ValidKey (AM_84)

**Objective:** Verify getAppProperty with empty appId and valid key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property EmptyAppId ValidKey | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `""`, `key`: `"delay"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": "delay"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_invalidkey-am_85"></a>
### AppManager_GetAppProperty_EmptyAppId_InvalidKey (AM_85)

**Objective:** Verify getAppProperty with empty appId and invalid key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetAppProperty EmptyAppId InvalidKey | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `""`, `key`: `"InvalidKey"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": "InvalidKey"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_getappproperty_emptyappid_emptykey-am_86"></a>
### AppManager_GetAppProperty_EmptyAppId_EmptyKey (AM_86)

**Objective:** Verify getAppProperty with empty appId and empty key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Empty Params | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `""`, `key`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "", "key": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_max_running_apps-am_87"></a>
### AppManager_Max_Running_Apps (AM_87)

**Objective:** Verify the successful retrieval of the maximum number of running apps

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Max Running Apps | Invoke `getMaxRunningApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getMaxRunningApps"}' http://127.0.0.1:9998/jsonrpc` | Max Running Apps returned successfully |

---

<a id="appmanager_getappproperty_validappid_validkey_pinlock-am_88"></a>
### AppManager_GetAppProperty_ValidAppId_ValidKey_Pinlock (AM_88)

**Objective:** Verify getAppProperty with valid appId and valid key as pinlock

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Valid Params | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"pinlock"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "pinlock"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds (empty/null response) |

---

<a id="appmanager_getappproperty_validappid_validkey_inactivepriority-am_89"></a>
### AppManager_GetAppProperty_ValidAppId_ValidKey_InactivePriority (AM_89)

**Objective:** Verify getAppProperty with valid appId and valid key as inactivePriority

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Valid Params | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `key`: `"inactivePriority"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "key": "inactivePriority"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds (empty/null response) |

---

<a id="appmanager_getappproperty_numericappid_numerickey-am_90"></a>
### AppManager_GetAppProperty_NumericAppId_NumericKey (AM_90)

**Objective:** Verify getAppProperty with numeric appId and numeric key

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get App Property Numeric Params | Invoke `getAppProperty` on `org.rdk.AppManager` with `appId`: `123`, `key`: `456`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getAppProperty", "params": {"appId": 123, "key": 456}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_valid_appid-am_91"></a>
### AppManager_ActivateSystemApp_Valid_AppId (AM_91)

**Objective:** Verify activateSystemApp with a valid appId of an installed device application

**Pre-condition:**

#### Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_activatesystemapp_invalid_appid-am_92"></a>
### AppManager_ActivateSystemApp_Invalid_AppId (AM_92)

**Objective:** Verify activateSystemApp with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Invalid AppId | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_empty_appid-am_93"></a>
### AppManager_ActivateSystemApp_Empty_AppId (AM_93)

**Objective:** Verify activateSystemApp with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Empty AppId | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_special_char_appid-am_94"></a>
### AppManager_ActivateSystemApp_Special_Char_AppId (AM_94)

**Objective:** Verify activateSystemApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Special Char | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_numeric_appid-am_95"></a>
### AppManager_ActivateSystemApp_Numeric_AppId (AM_95)

**Objective:** Verify activateSystemApp with an appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Numeric AppId | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_activatesystemapp_without_param-am_96"></a>
### AppManager_ActivateSystemApp_Without_Param (AM_96)

**Objective:** Verify activateSystemApp fails gracefully when called without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate System App Without Param | Invoke `activateSystemApp` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_valid_appid-am_97"></a>
### AppManager_DeactivateSystemApp_Valid_AppId (AM_97)

**Objective:** Verify deactivateSystemApp with a valid appId of an installed device application

**Pre-condition:**

#### Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Activate System App | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App | Invoke `deactivateSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_deactivatesystemapp_invalid_appid-am_98"></a>
### AppManager_DeactivateSystemApp_Invalid_AppId (AM_98)

**Objective:** Verify deactivateSystemApp with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Invalid AppId | Invoke `deactivateSystemApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_empty_appid-am_99"></a>
### AppManager_DeactivateSystemApp_Empty_AppId (AM_99)

**Objective:** Verify deactivateSystemApp with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Empty AppId | Invoke `deactivateSystemApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_special_char_appid-am_100"></a>
### AppManager_DeactivateSystemApp_Special_Char_AppId (AM_100)

**Objective:** Verify deactivateSystemApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Special Char | Invoke `deactivateSystemApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_numeric_appid-am_101"></a>
### AppManager_DeactivateSystemApp_Numeric_AppId (AM_101)

**Objective:** Verify deactivateSystemApp with an appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Numeric AppId | Invoke `deactivateSystemApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_deactivatesystemapp_without_param-am_102"></a>
### AppManager_DeactivateSystemApp_Without_Param (AM_102)

**Objective:** Verify deactivateSystemApp fails gracefully when called without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System App Without Param | Invoke `deactivateSystemApp` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.deactivateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_valid_appid-am_103"></a>
### AppManager_HibernateSystemApp_Valid_AppId (AM_103)

**Objective:** Verify hibernateSystemApp with a valid appId of an installed device application

**Pre-condition:**

#### Pre-condition 1: Start_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start System App | Invoke `startSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.startSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Activate System App | Invoke `activateSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.activateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App | Invoke `hibernateSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Stop_System_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Stop System App | Invoke `stopSystemApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.stopSystemApp", "params": {"appId": "<PACKAGEMANAGER_SYSTEM_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_hibernatesystemapp_invalid_appid-am_104"></a>
### AppManager_HibernateSystemApp_Invalid_AppId (AM_104)

**Objective:** Verify hibernateSystemApp with an invalid appId that does not exist in the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Invalid AppId | Invoke `hibernateSystemApp` on `org.rdk.AppManager` with `appId`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_empty_appid-am_105"></a>
### AppManager_HibernateSystemApp_Empty_AppId (AM_105)

**Objective:** Verify hibernateSystemApp with an empty string as appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Empty AppId | Invoke `hibernateSystemApp` on `org.rdk.AppManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_special_char_appid-am_106"></a>
### AppManager_HibernateSystemApp_Special_Char_AppId (AM_106)

**Objective:** Verify hibernateSystemApp with a appId containing special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Special Char | Invoke `hibernateSystemApp` on `org.rdk.AppManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_numeric_appid-am_107"></a>
### AppManager_HibernateSystemApp_Numeric_AppId (AM_107)

**Objective:** Verify hibernateSystemApp with an appId containing only numeric characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Numeric AppId | Invoke `hibernateSystemApp` on `org.rdk.AppManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_hibernatesystemapp_without_param-am_108"></a>
### AppManager_HibernateSystemApp_Without_Param (AM_108)

**Objective:** Verify hibernateSystemApp fails gracefully when called without parameter

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Hibernate System App Without Param | Invoke `hibernateSystemApp` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.hibernateSystemApp"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appmanager_app_lock_launch_terminate_unlock_operations-am_l2_01"></a>
### AppManager_App_Lock_Launch_Terminate_Unlock_Operations (AM_L2_01)

**Objective:** Verify that an app can be launched successfully after performing lock operation on the device

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Launch App After Lock | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 4 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_terminate_lock_unlock_operations-am_l2_02"></a>
### AppManager_App_Launch_Terminate_Lock_Unlock_Operations (AM_L2_02)

**Objective:** Verify that an app can be launch, terminate, lock and unlock successfully

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 3 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_kill_lock_unlock_operations-am_l2_03"></a>
### AppManager_App_Launch_Kill_Lock_Unlock_Operations (AM_L2_03)

**Objective:** Verify that an app can be launch, kill, lock and unlock successfully

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 3 | Kill App Valid Param | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_app_launch_close_lock_unlock_operations-am_l2_04"></a>
### AppManager_App_Launch_Close_Lock_Unlock_Operations (AM_L2_04)

**Objective:** Verify that an app can be launch, close, lock and unlock successfully

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Before Lock | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check App Launched | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 3 | Close App Valid Params | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Lock Package ValidParameters | Invoke `lock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `lockReason`: `"TestingPurpose"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.lock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "lockReason": "TestingPurpose"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Unlock Package | Invoke `unlock` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.unlock", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_close-am_l2_05"></a>
### AppManager_Check_On_AppLifecycleStateChanged_Event_After_Close (AM_L2_05)

**Objective:** Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, closed

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Close App Valid Params | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Close | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 5 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_kill-am_l2_06"></a>
### AppManager_Check_On_AppLifecycleStateChanged_Event_After_Kill (AM_L2_06)

**Objective:** Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, killed

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Kill App Valid Param | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Kill | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |

---

<a id="appmanager_check_on_applifecyclestatechanged_event_after_terminate-am_l2_07"></a>
### AppManager_Check_On_AppLifecycleStateChanged_Event_After_Terminate (AM_L2_07)

**Objective:** Verify that appLifecycleStateChanged event is received with correct parameters when an app is launched, terminated

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check AppLifecycleStateChanged Event After Terminate | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |

---

<a id="appmanager_app_launch_twice-am_l2_08"></a>
### AppManager_App_Launch_Twice (AM_L2_08)

**Objective:** Check that an app can be launched successfully after terminating the app which is launched previously

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App First Time | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Launch App Second Time | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 6 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_launch-am_l2_09"></a>
### AppManager_Check_Get_Loaded_Apps_After_Launch (AM_L2_09)

**Objective:** Verify that the launched app is reflected in the list of loaded apps

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Get Loaded Apps After Launch | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Post-condition:**

#### Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_close-am_l2_10"></a>
### AppManager_Check_Get_Loaded_Apps_After_Close (AM_L2_10)

**Objective:** Verify_that the closed app is no longer reflected in the list of loaded apps

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Close App Valid Param | Invoke `closeApp` on `org.rdk.LifecycleManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.LifecycleManager.1.closeApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Close | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

**Post-condition:**

#### Post-condition 1: Terminate_the_Launched_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appmanager_check_get_loaded_apps_after_kill-am_l2_11"></a>
### AppManager_Check_Get_Loaded_Apps_After_Kill (AM_L2_11)

**Objective:** Verify that the killed app is no longer reflected in the list of loaded apps

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Kill App Valid Param | Invoke `killApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.killApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Kill | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

---

<a id="appmanager_check_get_loaded_apps_after_terminate-am_l2_12"></a>
### AppManager_Check_Get_Loaded_Apps_After_Terminate (AM_L2_12)

**Objective:** Verify that the terminated app is no longer reflected in the list of loaded apps

**Pre-condition:**

#### Pre-condition 1: Terminate_Existing_App

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Loaded Apps | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |
| 2 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Launch App Valid Params | Invoke `launchApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check AppLifecycleStateChanged Event After Launch | Listen for event `Event_On_App_Lifecycle_State_Changed` | Event data validated successfully |
| 3 | Terminate App Valid Param | Invoke `terminateApp` on `org.rdk.AppManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Get Loaded Apps After Terminate | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Loaded apps information validated successfully |

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
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M147 |
