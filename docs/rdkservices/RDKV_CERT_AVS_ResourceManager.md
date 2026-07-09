## TestScript Name
RDKV_CERT_AVS_ResourceManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [ResourceManager_Set_AV_Blocked_Valid_AppId_True](#resourcemanager_set_av_blocked_valid_appid_true)
   - [ResourceManager_Set_AV_Blocked_Valid_AppId_False](#resourcemanager_set_av_blocked_valid_appid_false)
   - [ResourceManager_Set_AV_Blocked_Empty_AppId_True](#resourcemanager_set_av_blocked_empty_appid_true)
   - [ResourceManager_Set_AV_Blocked_Empty_AppId_False](#resourcemanager_set_av_blocked_empty_appid_false)
   - [ResourceManager_SetAVBlocked_SpecialCharacters_True](#resourcemanager_setavblocked_specialcharacters_true)
   - [ResourceManager_SetAVBlocked_SpecialChars_False](#resourcemanager_setavblocked_specialchars_false)
   - [ResourceManager_SetAVBlocked_LongAppId_True](#resourcemanager_setavblocked_longappid_true)
   - [ResourceManager_SetAVBlocked_LongAppId_False](#resourcemanager_setavblocked_longappid_false)
   - [ResourceManager_Check_Get_Blocked_List_API_Response](#resourcemanager_check_get_blocked_list_api_response)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps](#resourcemanager_verify_reserve_tts_resource_for_apps)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Empty_AppIds](#resourcemanager_verify_reserve_tts_resource_for_apps_empty_appids)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Numeric_AppIds](#resourcemanager_verify_reserve_tts_resource_for_apps_numeric_appids)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Special_Char](#resourcemanager_verify_reserve_tts_resource_for_apps_special_char)
   - [ResourceManager_Verify_reserveTTSResourceForApps_Long_String](#resourcemanager_verify_reservettsresourceforapps_long_string)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_With_Spaces](#resourcemanager_verify_reserve_tts_resource_for_apps_with_spaces)
   - [ResourceManager_Verify_ReserveTTSResourceForApps_Mixed_Alphanumeric_SpecialChars](#resourcemanager_verify_reservettsresourceforapps_mixed_alphanumeric_specialchars)
   - [ResourceManager_Reserve_TTS_Resource_Valid_AppId](#resourcemanager_reserve_tts_resource_valid_appid)
   - [ResourceManager_Reserve_TTS_Resource_Empty_AppId](#resourcemanager_reserve_tts_resource_empty_appid)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Numeric](#resourcemanager_reserve_tts_resource_appid_numeric)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Invalid](#resourcemanager_reserve_tts_resource_appid_invalid)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Alphanumeric](#resourcemanager_reserve_tts_resource_appid_alphanumeric)
   - [ResourceManager_Reserve_TTS_Resource_AppId_SpecialChars](#resourcemanager_reserve_tts_resource_appid_specialchars)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **ResourceManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.ResourceManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DownloadManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DownloadManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DownloadManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DownloadManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DownloadManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DownloadManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Activate_PackageManagerRDKEMS_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 4: Activate_AppManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of AppManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of AppManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 5: Activate_ResourceManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of ResourceManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ResourceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate ResourceManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.ResourceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of ResourceManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ResourceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 6: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install package on device | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify installed package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 7: Launch_Application

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Launch app valid params | Launch App on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.launchApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "intent": "", "launchArgs": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check app launched | Get loaded apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |

### Plugin Pre-condition 8: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure packagemanager application name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure packagemanager application version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure packagemanager application hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure packagemanager additionalmetadata name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure packagemanager additionalmetadata value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure packagemanager application MD5 checksum value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="resourcemanager_set_av_blocked_valid_appid_true"></a>
### TestCase Name
ResourceManager_Set_AV_Blocked_Valid_AppId_True

### TestCase ID
RM_01

### TestCase Objective
Verify the behavior of setAVBlocked when a valid appId is provided and blocked is set to true

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that AV blocking is set successfully |

---

<a id="resourcemanager_set_av_blocked_valid_appid_false"></a>
### TestCase Name
ResourceManager_Set_AV_Blocked_Valid_AppId_False

### TestCase ID
RM_02

### TestCase Objective
Verify the behavior of setAVBlocked when a valid appId is provided and blocked is set to false

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that AV blocking is set successfully |

---

<a id="resourcemanager_set_av_blocked_empty_appid_true"></a>
### TestCase Name
ResourceManager_Set_AV_Blocked_Empty_AppId_True

### TestCase ID
RM_03

### TestCase Objective
Verify the behavior of setAVBlocked when an empty string is passed as appId and blocked is set to true

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked empty AppId | Invoke setAVBlocked on org.rdk.ResourceManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_set_av_blocked_empty_appid_false"></a>
### TestCase Name
ResourceManager_Set_AV_Blocked_Empty_AppId_False

### TestCase ID
RM_04

### TestCase Objective
Verify the behavior of setAVBlocked when an empty string is passed as appId and blocked is set to false

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked empty AppId false | Invoke setAVBlocked on org.rdk.ResourceManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_setavblocked_specialcharacters_true"></a>
### TestCase Name
ResourceManager_SetAVBlocked_SpecialCharacters_True

### TestCase ID
RM_05

### TestCase Objective
Verify the behavior of setAVBlocked when appId contains special characters and blocked is set to true

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked special true | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "()^*!", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_setavblocked_specialchars_false"></a>
### TestCase Name
ResourceManager_SetAVBlocked_SpecialChars_False

### TestCase ID
RM_06

### TestCase Objective
Verify the behavior of setAVBlocked when appId contains special characters and blocked is set to false.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked special chars false | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "()^*!", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_setavblocked_longappid_true"></a>
### TestCase Name
ResourceManager_SetAVBlocked_LongAppId_True

### TestCase ID
RM_07

### TestCase Objective
Verify the behavior of setAVBlocked when appId is a very long string and blocked is set to true

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked LongAppId true | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "VeryLongStringForAppIdTestingPurpose"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_setavblocked_longappid_false"></a>
### TestCase Name
ResourceManager_SetAVBlocked_LongAppId_False

### TestCase ID
RM_08

### TestCase Objective
Verify the behavior of setAVBlocked when appId is a very long string and blocked is set to false.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set AV blocked LongAppId false | Invoke setAVBlocked on org.rdk.ResourceManager with appId: "VeryLongStringRepresentingAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "VeryLongStringRepresentingAppId", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_check_get_blocked_list_api_response"></a>
### TestCase Name
ResourceManager_Check_Get_Blocked_List_API_Response

### TestCase ID
RM_09

### TestCase Objective
Check that get blocked AV list API returns a well-formed blocked list

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get blocked AV applications | Invoke getBlockedAVApplications on org.rdk.ResourceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.getBlockedAVApplications"}' http://127.0.0.1:9998/jsonrpc` | Verify that the blocked AV applications are returned successfully |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps"></a>
### TestCase Name
ResourceManager_Verify_Reserve_TTS_Resource_For_Apps

### TestCase ID
RM_10

### TestCase Objective
Verify reserveTTSResourceForApps with a valid appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a true success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_empty_appids"></a>
### TestCase Name
ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Empty_AppIds

### TestCase ID
RM_11

### TestCase Objective
Verify reserveTTSResourceForApps with an empty string as appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps empty AppIds | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_numeric_appids"></a>
### TestCase Name
ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Numeric_AppIds

### TestCase ID
RM_12

### TestCase Objective
Verify reserveTTSResourceForApps with a numeric value as appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps numeric AppIds | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": 12345}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_special_char"></a>
### TestCase Name
ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Special_Char

### TestCase ID
RM_13

### TestCase Objective
Verify reserveTTSResourceForApps with a special character string as appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource special char | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_verify_reservettsresourceforapps_long_string"></a>
### TestCase Name
ResourceManager_Verify_reserveTTSResourceForApps_Long_String

### TestCase ID
RM_14

### TestCase Objective
Verify reserveTTSResourceForApps with a very long string as appids.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps (error case) | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: "A_Very_Long_String_As_AppInstanceId_Example_1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "A_Very_Long_String_As_AppInstanceId_Example_1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_with_spaces"></a>
### TestCase Name
ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_With_Spaces

### TestCase ID
RM_15

### TestCase Objective
Verify reserveTTSResourceForApps with a string containing spaces as appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps with spaces | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: "App Instance ID With Spaces"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "App Instance ID With Spaces"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_verify_reservettsresourceforapps_mixed_alphanumeric_specialchars"></a>
### TestCase Name
ResourceManager_Verify_ReserveTTSResourceForApps_Mixed_Alphanumeric_SpecialChars

### TestCase ID
RM_16

### TestCase Objective
Verify reserveTTSResourceForApps with a string containing mixed alphanumeric and special characters as appids

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource for apps | Invoke reserveTTSResourceForApps on org.rdk.ResourceManager with appids: "App123!@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "App123!@#"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_reserve_tts_resource_valid_appid"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_Valid_AppId

### TestCase ID
RM_17

### TestCase Objective
Verify reserveTTSResource succeeds with a valid appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a true success status |

---

<a id="resourcemanager_reserve_tts_resource_empty_appid"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_Empty_AppId

### TestCase ID
RM_18

### TestCase Objective
Verify reserveTTSResource fails when appId is an empty string

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource empty AppId | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_numeric"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_AppId_Numeric

### TestCase ID
RM_19

### TestCase Objective
Verify reserveTTSResource fails when appId is numeric

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource AppId numeric | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_invalid"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_AppId_Invalid

### TestCase ID
RM_20

### TestCase Objective
Verify reserveTTSResource fails when appId is invalid

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource AppId invalid | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: "InvalidApp"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "InvalidApp"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_alphanumeric"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_AppId_Alphanumeric

### TestCase ID
RM_21

### TestCase Objective
Verify reserveTTSResource fails when appId is alphanumeric

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource AppId alphanumeric | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: "App123"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "App123"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_specialchars"></a>
### TestCase Name
ResourceManager_Reserve_TTS_Resource_AppId_SpecialChars

### TestCase ID
RM_22

### TestCase Objective
Verify reserveTTSResource fails when appId contains special characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reserve TTS resource AppId special chars | Invoke reserveTTSResource on org.rdk.ResourceManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a false success status |

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check loaded apps | Get loaded apps from AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the loaded apps information is returned successfully |
| 2 | Terminate app valid param | *(Conditional statement executed only if package/app is currently present)*<br>Terminate app on AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.terminateApp", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Check package info | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 4 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M147

<div align="right"><a href="#testscript-name">Go to Top</a></div>
