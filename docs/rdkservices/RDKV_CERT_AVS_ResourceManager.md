## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [ResourceManager_Set_AV_Blocked_Valid_AppId_True (RM_01)](#resourcemanager_set_av_blocked_valid_appid_true-rm_01)
   - [ResourceManager_Set_AV_Blocked_Valid_AppId_False (RM_02)](#resourcemanager_set_av_blocked_valid_appid_false-rm_02)
   - [ResourceManager_Set_AV_Blocked_Empty_AppId_True (RM_03)](#resourcemanager_set_av_blocked_empty_appid_true-rm_03)
   - [ResourceManager_Set_AV_Blocked_Empty_AppId_False (RM_04)](#resourcemanager_set_av_blocked_empty_appid_false-rm_04)
   - [ResourceManager_SetAVBlocked_SpecialCharacters_True (RM_05)](#resourcemanager_setavblocked_specialcharacters_true-rm_05)
   - [ResourceManager_SetAVBlocked_SpecialChars_False (RM_06)](#resourcemanager_setavblocked_specialchars_false-rm_06)
   - [ResourceManager_SetAVBlocked_LongAppId_True (RM_07)](#resourcemanager_setavblocked_longappid_true-rm_07)
   - [ResourceManager_SetAVBlocked_LongAppId_False (RM_08)](#resourcemanager_setavblocked_longappid_false-rm_08)
   - [ResourceManager_Check_Get_Blocked_List_API_Response (RM_09)](#resourcemanager_check_get_blocked_list_api_response-rm_09)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps (RM_10)](#resourcemanager_verify_reserve_tts_resource_for_apps-rm_10)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Empty_AppIds (RM_11)](#resourcemanager_verify_reserve_tts_resource_for_apps_empty_appids-rm_11)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Numeric_AppIds (RM_12)](#resourcemanager_verify_reserve_tts_resource_for_apps_numeric_appids-rm_12)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Special_Char (RM_13)](#resourcemanager_verify_reserve_tts_resource_for_apps_special_char-rm_13)
   - [ResourceManager_Verify_reserveTTSResourceForApps_Long_String (RM_14)](#resourcemanager_verify_reservettsresourceforapps_long_string-rm_14)
   - [ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_With_Spaces (RM_15)](#resourcemanager_verify_reserve_tts_resource_for_apps_with_spaces-rm_15)
   - [ResourceManager_Verify_ReserveTTSResourceForApps_Mixed_Alphanumeric_SpecialChars (RM_16)](#resourcemanager_verify_reservettsresourceforapps_mixed_alphanumeric_specialchars-rm_16)
   - [ResourceManager_Reserve_TTS_Resource_Valid_AppId (RM_17)](#resourcemanager_reserve_tts_resource_valid_appid-rm_17)
   - [ResourceManager_Reserve_TTS_Resource_Empty_AppId (RM_18)](#resourcemanager_reserve_tts_resource_empty_appid-rm_18)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Numeric (RM_19)](#resourcemanager_reserve_tts_resource_appid_numeric-rm_19)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Invalid (RM_20)](#resourcemanager_reserve_tts_resource_appid_invalid-rm_20)
   - [ResourceManager_Reserve_TTS_Resource_AppId_Alphanumeric (RM_21)](#resourcemanager_reserve_tts_resource_appid_alphanumeric-rm_21)
   - [ResourceManager_Reserve_TTS_Resource_AppId_SpecialChars (RM_22)](#resourcemanager_reserve_tts_resource_appid_specialchars-rm_22)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **ResourceManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.ResourceManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getBlockedAVApplications`
- **Configuration APIs**: `setAVBlocked`
- **Other APIs**: `reserveTTSResource`, `reserveTTSResourceForApps`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getBlockedAVApplications` | Gets a list of blacklisted clients |
| `reserveTTSResource` | Reserves the Text To speech Resource for specified client |
| `reserveTTSResourceForApps` | Reserves TTS resource for applications |
| `setAVBlocked` | Adds/removes the list of applications with the given callsigns to/from the blacklist |

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

### Pre-condition 5: Activate_ResourceManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ResourceManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.ResourceManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.ResourceManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.ResourceManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

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

<a id="resourcemanager_set_av_blocked_valid_appid_true-rm_01"></a>
### ResourceManager_Set_AV_Blocked_Valid_AppId_True (RM_01)

**Objective:** Verify the behavior of setAVBlocked when a valid appId is provided and blocked is set to true

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `blocked`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | AV Blocked set successfully |

---

<a id="resourcemanager_set_av_blocked_valid_appid_false-rm_02"></a>
### ResourceManager_Set_AV_Blocked_Valid_AppId_False (RM_02)

**Objective:** Verify the behavior of setAVBlocked when a valid appId is provided and blocked is set to false

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `blocked`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | AV Blocked set successfully |

---

<a id="resourcemanager_set_av_blocked_empty_appid_true-rm_03"></a>
### ResourceManager_Set_AV_Blocked_Empty_AppId_True (RM_03)

**Objective:** Verify the behavior of setAVBlocked when an empty string is passed as appId and blocked is set to true

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked Empty AppId | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `""`, `blocked`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_set_av_blocked_empty_appid_false-rm_04"></a>
### ResourceManager_Set_AV_Blocked_Empty_AppId_False (RM_04)

**Objective:** Verify the behavior of setAVBlocked when an empty string is passed as appId and blocked is set to false

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked Empty AppId False | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `""`, `blocked`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_setavblocked_specialcharacters_true-rm_05"></a>
### ResourceManager_SetAVBlocked_SpecialCharacters_True (RM_05)

**Objective:** Verify the behavior of setAVBlocked when appId contains special characters and blocked is set to true

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked Special True | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"()^*!"`, `blocked`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "()^*!", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_setavblocked_specialchars_false-rm_06"></a>
### ResourceManager_SetAVBlocked_SpecialChars_False (RM_06)

**Objective:** Verify the behavior of setAVBlocked when appId contains special characters and blocked is set to false.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked SpecialChars False | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"()^*!"`, `blocked`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "()^*!", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_setavblocked_longappid_true-rm_07"></a>
### ResourceManager_SetAVBlocked_LongAppId_True (RM_07)

**Objective:** Verify the behavior of setAVBlocked when appId is a very long string and blocked is set to true

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked LongAppId True | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"VeryLongStringForAppIdTestingPurpose"`, `blocked`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "VeryLongStringForAppIdTestingPurpose", "blocked": true}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_setavblocked_longappid_false-rm_08"></a>
### ResourceManager_SetAVBlocked_LongAppId_False (RM_08)

**Objective:** Verify the behavior of setAVBlocked when appId is a very long string and blocked is set to false.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set AV Blocked LongAppId False | Invoke `setAVBlocked` on `org.rdk.ResourceManager` with `appId`: `"VeryLongStringRepresentingAppId"`, `blocked`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.setAVBlocked", "params": {"appId": "VeryLongStringRepresentingAppId", "blocked": false}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_check_get_blocked_list_api_response-rm_09"></a>
### ResourceManager_Check_Get_Blocked_List_API_Response (RM_09)

**Objective:** Check that get blocked AV list API returns a well-formed blocked list

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Blocked AV Applications | Invoke `getBlockedAVApplications` on `org.rdk.ResourceManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.getBlockedAVApplications"}' http://127.0.0.1:9998/jsonrpc` | Blocked AV Applications returned successfully |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps-rm_10"></a>
### ResourceManager_Verify_Reserve_TTS_Resource_For_Apps (RM_10)

**Objective:** Verify reserveTTSResourceForApps with a valid appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource For Apps | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a true success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_empty_appids-rm_11"></a>
### ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Empty_AppIds (RM_11)

**Objective:** Verify reserveTTSResourceForApps with an empty string as appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource For Apps Empty AppIds | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": ""}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_numeric_appids-rm_12"></a>
### ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Numeric_AppIds (RM_12)

**Objective:** Verify reserveTTSResourceForApps with a numeric value as appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource For Apps Numeric AppIds | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": 12345}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_special_char-rm_13"></a>
### ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_Special_Char (RM_13)

**Objective:** Verify reserveTTSResourceForApps with a special character string as appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource Special Char | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_verify_reservettsresourceforapps_long_string-rm_14"></a>
### ResourceManager_Verify_reserveTTSResourceForApps_Long_String (RM_14)

**Objective:** Verify reserveTTSResourceForApps with a very long string as appids.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify reserveTTSResourceForApps | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `"A_Very_Long_String_As_AppInstanceId_Example_1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "A_Very_Long_String_As_AppInstanceId_Example_1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_verify_reserve_tts_resource_for_apps_with_spaces-rm_15"></a>
### ResourceManager_Verify_Reserve_TTS_Resource_For_Apps_With_Spaces (RM_15)

**Objective:** Verify reserveTTSResourceForApps with a string containing spaces as appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource For Apps With Spaces | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `"App Instance ID With Spaces"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "App Instance ID With Spaces"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_verify_reservettsresourceforapps_mixed_alphanumeric_specialchars-rm_16"></a>
### ResourceManager_Verify_ReserveTTSResourceForApps_Mixed_Alphanumeric_SpecialChars (RM_16)

**Objective:** Verify reserveTTSResourceForApps with a string containing mixed alphanumeric and special characters as appids

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource For Apps | Invoke `reserveTTSResourceForApps` on `org.rdk.ResourceManager` with `appids`: `"App123!@#"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResourceForApps", "params": {"appids": "App123!@#"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_reserve_tts_resource_valid_appid-rm_17"></a>
### ResourceManager_Reserve_TTS_Resource_Valid_AppId (RM_17)

**Objective:** Verify reserveTTSResource succeeds with a valid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a true success status |

---

<a id="resourcemanager_reserve_tts_resource_empty_appid-rm_18"></a>
### ResourceManager_Reserve_TTS_Resource_Empty_AppId (RM_18)

**Objective:** Verify reserveTTSResource fails when appId is an empty string

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource Empty AppId | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_numeric-rm_19"></a>
### ResourceManager_Reserve_TTS_Resource_AppId_Numeric (RM_19)

**Objective:** Verify reserveTTSResource fails when appId is numeric

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource AppId Numeric | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": 12345}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_invalid-rm_20"></a>
### ResourceManager_Reserve_TTS_Resource_AppId_Invalid (RM_20)

**Objective:** Verify reserveTTSResource fails when appId is invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource AppId Invalid | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `"InvalidApp"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "InvalidApp"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_alphanumeric-rm_21"></a>
### ResourceManager_Reserve_TTS_Resource_AppId_Alphanumeric (RM_21)

**Objective:** Verify reserveTTSResource fails when appId is alphanumeric

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource AppId Alphanumeric | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `"App123"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "App123"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

---

<a id="resourcemanager_reserve_tts_resource_appid_specialchars-rm_22"></a>
### ResourceManager_Reserve_TTS_Resource_AppId_SpecialChars (RM_22)

**Objective:** Verify reserveTTSResource fails when appId contains special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reserve TTS Resource AppId SpecialChars | Invoke `reserveTTSResource` on `org.rdk.ResourceManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.ResourceManager.1.reserveTTSResource", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API call was expected to return a false success status |

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