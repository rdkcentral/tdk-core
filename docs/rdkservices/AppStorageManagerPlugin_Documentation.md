## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [AppStorageManager_Clear_App_Data (ASM_01)](#appstoragemanager_clear_app_data-asm_01)
   - [AppStorageManager_Clear_App_Data_Invalid_AppId (ASM_02)](#appstoragemanager_clear_app_data_invalid_appid-asm_02)
   - [AppStorageManager_Clear_App_Data_Numeric_AppId (ASM_03)](#appstoragemanager_clear_app_data_numeric_appid-asm_03)
   - [AppStorageManager_Clear_Special_Characters_AppId (ASM_04)](#appstoragemanager_clear_special_characters_appid-asm_04)
   - [AppStorageManager_Clear_Method_Max_Length_Error (ASM_05)](#appstoragemanager_clear_method_max_length_error-asm_05)
   - [AppStorageManager_Clear_App_Data_Invalid_Characters (ASM_06)](#appstoragemanager_clear_app_data_invalid_characters-asm_06)
   - [AppStorageManager_ClearAll_Single_Valid_AppID (ASM_07)](#appstoragemanager_clearall_single_valid_appid-asm_07)
   - [AppStorageManager_ClearAll_Empty_ExemptionAppIds (ASM_08)](#appstoragemanager_clearall_empty_exemptionappids-asm_08)
   - [AppStorageManager_ClearAll_Invalid_AppID (ASM_09)](#appstoragemanager_clearall_invalid_appid-asm_09)
   - [AppStorageManager_ClearAll_Special_Characters (ASM_10)](#appstoragemanager_clearall_special_characters-asm_10)
   - [AppStorageManager_ClearAll_Max_Length_Error (ASM_11)](#appstoragemanager_clearall_max_length_error-asm_11)
   - [AppStorageManager_ClearAll_Invalid_Characters (ASM_12)](#appstoragemanager_clearall_invalid_characters-asm_12)
   - [AppStorageManager_ClearAll_Numeric_ExemptionAppIds (ASM_13)](#appstoragemanager_clearall_numeric_exemptionappids-asm_13)
   - [AppStorageManager_Clear_All_Without_Parameter (ASM_14)](#appstoragemanager_clear_all_without_parameter-asm_14)
   - [AppStorageManager_GetStorage_Valid_Params (ASM_15)](#appstoragemanager_getstorage_valid_params-asm_15)
   - [AppStorageManager_GetStorage_Empty_AppId (ASM_16)](#appstoragemanager_getstorage_empty_appid-asm_16)
   - [AppStorageManager_GetStorage_Numeric_AppId (ASM_17)](#appstoragemanager_getstorage_numeric_appid-asm_17)
   - [AppStorageManager_GetStorage_Special_Characters_AppId (ASM_18)](#appstoragemanager_getstorage_special_characters_appid-asm_18)
   - [AppStorageManager_GetStorage_Max_Length_AppId (ASM_19)](#appstoragemanager_getstorage_max_length_appid-asm_19)
   - [AppStorageManager_GetStorage_Invalid_Characters_AppId (ASM_20)](#appstoragemanager_getstorage_invalid_characters_appid-asm_20)
   - [AppStorageManager_GetStorage_Missing_UserId (ASM_21)](#appstoragemanager_getstorage_missing_userid-asm_21)
   - [AppStorageManager_GetStorage_Missing_GroupId (ASM_22)](#appstoragemanager_getstorage_missing_groupid-asm_22)
   - [AppStorageManager_GetStorage_NonInteger_UserId (ASM_23)](#appstoragemanager_getstorage_noninteger_userid-asm_23)
   - [AppStorageManager_GetStorage_NonInteger_GroupId (ASM_24)](#appstoragemanager_getstorage_noninteger_groupid-asm_24)
   - [AppStorageManager_GetStorage_All_Params_Missing (ASM_25)](#appstoragemanager_getstorage_all_params_missing-asm_25)
   - [AppStorageManager_CreateStorage_Valid_Params (ASM_26)](#appstoragemanager_createstorage_valid_params-asm_26)
   - [AppStorageManager_CreateStorage_Empty_AppId (ASM_27)](#appstoragemanager_createstorage_empty_appid-asm_27)
   - [AppStorageManager_CreateStorage_Numeric_AppId (ASM_28)](#appstoragemanager_createstorage_numeric_appid-asm_28)
   - [AppStorageManager_CreateStorage_Special_Characters_AppId (ASM_29)](#appstoragemanager_createstorage_special_characters_appid-asm_29)
   - [AppStorageManager_CreateStorage_Max_Length_AppId (ASM_30)](#appstoragemanager_createstorage_max_length_appid-asm_30)
   - [AppStorageManager_CreateStorage_Invalid_Characters_AppId (ASM_31)](#appstoragemanager_createstorage_invalid_characters_appid-asm_31)
   - [AppStorageManager_CreateStorage_Missing_Size (ASM_32)](#appstoragemanager_createstorage_missing_size-asm_32)
   - [AppStorageManager_CreateStorage_NonInteger_Size (ASM_33)](#appstoragemanager_createstorage_noninteger_size-asm_33)
   - [AppStorageManager_CreateStorage_Zero_Size (ASM_34)](#appstoragemanager_createstorage_zero_size-asm_34)
   - [AppStorageManager_CreateStorage_All_Params_Missing (ASM_35)](#appstoragemanager_createstorage_all_params_missing-asm_35)
   - [AppStorageManager_DeleteStorage_Valid_AppId (ASM_36)](#appstoragemanager_deletestorage_valid_appid-asm_36)
   - [AppStorageManager_DeleteStorage_Empty_AppId (ASM_37)](#appstoragemanager_deletestorage_empty_appid-asm_37)
   - [AppStorageManager_DeleteStorage_Numeric_AppId (ASM_38)](#appstoragemanager_deletestorage_numeric_appid-asm_38)
   - [AppStorageManager_DeleteStorage_Special_Characters_AppId (ASM_39)](#appstoragemanager_deletestorage_special_characters_appid-asm_39)
   - [AppStorageManager_DeleteStorage_Max_Length_AppId (ASM_40)](#appstoragemanager_deletestorage_max_length_appid-asm_40)
   - [AppStorageManager_DeleteStorage_Invalid_Characters_AppId (ASM_41)](#appstoragemanager_deletestorage_invalid_characters_appid-asm_41)
   - [AppStorageManager_DeleteStorage_Missing_AppId (ASM_42)](#appstoragemanager_deletestorage_missing_appid-asm_42)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **AppStorageManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.AppStorageManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getStorage`
- **Configuration APIs**: `clear`, `clearAll`, `deleteStorage`
- **Other APIs**: `createStorage`

### APIs Under Test

| API | Description |
|-----|-------------|
| `clear` | Clears app data for a given app id |
| `clearAll` | Clears all app data except for the exempt app ids |
| `createStorage` | Creates storage for a given app id |
| `deleteStorage` | Deletes storage for a given app id |
| `getStorage` | Returns the storage location for a given app id |

---

## Pre-conditions

### Pre-condition 1: Activate_AppStorageManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.AppStorageManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.PackageManagerRDKEMS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Existing Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Package list returned successfully |
| 2 | Uninstall Existing Package | Invoke `uninstall` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 3 | Download ValidParameters | Invoke `download` on `org.rdk.DownloadManager` with `url`: `"<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Valid downloadId is returned successfully |
| 4 | Install | Invoke `install` on `org.rdk.PackageManagerRDKEMS` with `packageId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `version`: `"<PACKAGEMANAGER_APPLICATION_VERSION>"`, `fileLocator`: `"<result_step_4>"`, `name`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>"`, `value`: `"<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 5 | Verify Installed Package | Invoke `listPackages` on `org.rdk.PackageManagerRDKEMS`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Installed package validation succeeds |

---

## Test Cases

<a id="appstoragemanager_clear_app_data-asm_01"></a>
### AppStorageManager_Clear_App_Data (ASM_01)

**Objective:** Verify the clear method successfully clears data for a valid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_clear_app_data_invalid_appid-asm_02"></a>
### AppStorageManager_Clear_App_Data_Invalid_AppId (ASM_02)

**Objective:** Verify the clear method returns an error when appId is an empty string

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Invalid AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_numeric_appid-asm_03"></a>
### AppStorageManager_Clear_App_Data_Numeric_AppId (ASM_03)

**Objective:** Verify the clear method returns an error when appId is a non-string value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Numeric AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `123`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_special_characters_appid-asm_04"></a>
### AppStorageManager_Clear_Special_Characters_AppId (ASM_04)

**Objective:** Verify the clear method handles special characters in appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Special Characters | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_method_max_length_error-asm_05"></a>
### AppStorageManager_Clear_Method_Max_Length_Error (ASM_05)

**Objective:** Verify the clear method returns an error when appId exceeds the maximum allowed length

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear App Data Max Length Error | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"ExceedingMaxAllowedLengthAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_invalid_characters-asm_06"></a>
### AppStorageManager_Clear_App_Data_Invalid_Characters (ASM_06)

**Objective:** Verify the clear method returns an error when appId contains whitespace and punctuation characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear Invalid AppId | Invoke `clear` on `org.rdk.AppStorageManager` with `appId`: `"appid !@#"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_single_valid_appid-asm_07"></a>
### AppStorageManager_ClearAll_Single_Valid_AppID (ASM_07)

**Objective:** Call the clearAll method with one valid app ID in exemptionAppIds and ensure app data except the exempted app is cleared

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All With Exemption | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_clearall_empty_exemptionappids-asm_08"></a>
### AppStorageManager_ClearAll_Empty_ExemptionAppIds (ASM_08)

**Objective:** Call the clearAll method with an empty list for exemptionAppIds and ensure all app data is cleared

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Empty ExemptionAppIds | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_appid-asm_09"></a>
### AppStorageManager_ClearAll_Invalid_AppID (ASM_09)

**Objective:** Verify clearAll with an invalid app ID in exemptionAppIds

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Invalid AppID | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `"InvalidAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_special_characters-asm_10"></a>
### AppStorageManager_ClearAll_Special_Characters (ASM_10)

**Objective:** Verify clearAll with exemptionAppIds containing special characters or non-alphanumeric values

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Special Characters | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_max_length_error-asm_11"></a>
### AppStorageManager_ClearAll_Max_Length_Error (ASM_11)

**Objective:** Verify the clearAll method returns an error when exemptionAppIds exceeds the maximum allowed length

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Max Length Error | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `"ExceedingMaxAllowedLengthAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_characters-asm_12"></a>
### AppStorageManager_ClearAll_Invalid_Characters (ASM_12)

**Objective:** Verify the clearAll method returns an error when exemptionAppIds contains whitespace and punctuation characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Invalid Characters | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `"appid !@#"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_numeric_exemptionappids-asm_13"></a>
### AppStorageManager_ClearAll_Numeric_ExemptionAppIds (ASM_13)

**Objective:** Verify the clearAll method returns an error when exemptionAppIds is a numeric value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Numeric ExemptionAppIds | Invoke `clearAll` on `org.rdk.AppStorageManager` with `exemptionAppIds`: `12345`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_all_without_parameter-asm_14"></a>
### AppStorageManager_Clear_All_Without_Parameter (ASM_14)

**Objective:** Check that all app storage is deleted when the exemptionAppIds parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Clear All Without Parameter | Invoke `clearAll` on `org.rdk.AppStorageManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_valid_params-asm_15"></a>
### AppStorageManager_GetStorage_Valid_Params (ASM_15)

**Objective:** Verify getStorage returns storage location for valid appId, userId, and groupId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Valid Params | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_empty_appid-asm_16"></a>
### AppStorageManager_GetStorage_Empty_AppId (ASM_16)

**Objective:** Verify getStorage returns error when appId is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Empty AppId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `""`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_numeric_appid-asm_17"></a>
### AppStorageManager_GetStorage_Numeric_AppId (ASM_17)

**Objective:** Verify getStorage returns error when appId is numeric

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Numeric AppId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `123`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": 123, "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_special_characters_appid-asm_18"></a>
### AppStorageManager_GetStorage_Special_Characters_AppId (ASM_18)

**Objective:** Verify getStorage returns error when appId contains special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Special Characters AppId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"()^*!"`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "()^*!", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_max_length_appid-asm_19"></a>
### AppStorageManager_GetStorage_Max_Length_AppId (ASM_19)

**Objective:** Verify getStorage returns error when appId exceeds maximum allowed length

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Max Length AppId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"ExceedingMaxAllowedLengthAppId"`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_invalid_characters_appid-asm_20"></a>
### AppStorageManager_GetStorage_Invalid_Characters_AppId (ASM_20)

**Objective:** Verify getStorage returns error when appId contains whitespace and punctuation

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Invalid Characters AppId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"appid !@#"`, `userId`: `1001`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "appid !@#", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_userid-asm_21"></a>
### AppStorageManager_GetStorage_Missing_UserId (ASM_21)

**Objective:** Verify getStorage returns error when userId is missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Missing UserId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_groupid-asm_22"></a>
### AppStorageManager_GetStorage_Missing_GroupId (ASM_22)

**Objective:** Verify getStorage returns error when groupId is missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage Missing GroupId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `userId`: `1001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_userid-asm_23"></a>
### AppStorageManager_GetStorage_NonInteger_UserId (ASM_23)

**Objective:** Verify getStorage returns error when userId is not an integer

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage NonInteger UserId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `userId`: `"abc"`, `groupId`: `2001`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": "abc", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_groupid-asm_24"></a>
### AppStorageManager_GetStorage_NonInteger_GroupId (ASM_24)

**Objective:** Verify getStorage returns error when groupId is not an integer

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage NonInteger GroupId | Invoke `getStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `userId`: `1001`, `groupId`: `"xyz"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": "xyz"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_all_params_missing-asm_25"></a>
### AppStorageManager_GetStorage_All_Params_Missing (ASM_25)

**Objective:** Verify getStorage returns error when all parameters are missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetStorage All Params Missing | Invoke `getStorage` on `org.rdk.AppStorageManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_valid_params-asm_26"></a>
### AppStorageManager_CreateStorage_Valid_Params (ASM_26)

**Objective:** Verify createStorage returns storage path for valid appId and size

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Valid Params | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `size`: `102400`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 102400}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_createstorage_empty_appid-asm_27"></a>
### AppStorageManager_CreateStorage_Empty_AppId (ASM_27)

**Objective:** Verify createStorage returns error when appId is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Empty AppId | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `""`, `size`: `1024`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_numeric_appid-asm_28"></a>
### AppStorageManager_CreateStorage_Numeric_AppId (ASM_28)

**Objective:** Verify createStorage returns error when appId is numeric

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Numeric AppId | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `123`, `size`: `1024`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": 123, "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_special_characters_appid-asm_29"></a>
### AppStorageManager_CreateStorage_Special_Characters_AppId (ASM_29)

**Objective:** Verify createStorage returns error when appId contains special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Special Characters AppId | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"()^*!"`, `size`: `1024`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "()^*!", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_max_length_appid-asm_30"></a>
### AppStorageManager_CreateStorage_Max_Length_AppId (ASM_30)

**Objective:** Verify createStorage returns error when appId exceeds maximum allowed length

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Max Length AppId | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"ExceedingMaxAllowedLengthAppId"`, `size`: `1024`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_invalid_characters_appid-asm_31"></a>
### AppStorageManager_CreateStorage_Invalid_Characters_AppId (ASM_31)

**Objective:** Verify createStorage returns error when appId contains whitespace and punctuation

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Invalid Characters AppId | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"appid !@#"`, `size`: `1024`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "appid !@#", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_missing_size-asm_32"></a>
### AppStorageManager_CreateStorage_Missing_Size (ASM_32)

**Objective:** Verify createStorage returns error when size is missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Missing Size | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_noninteger_size-asm_33"></a>
### AppStorageManager_CreateStorage_NonInteger_Size (ASM_33)

**Objective:** Verify createStorage returns error when size is not an integer

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage NonInteger Size | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `size`: `"abc"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": "abc"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_zero_size-asm_34"></a>
### AppStorageManager_CreateStorage_Zero_Size (ASM_34)

**Objective:** Verify createStorage returns error when size is zero

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage Zero Size | Invoke `createStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`, `size`: `0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_all_params_missing-asm_35"></a>
### AppStorageManager_CreateStorage_All_Params_Missing (ASM_35)

**Objective:** Verify createStorage returns error when all parameters are missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | CreateStorage All Params Missing | Invoke `createStorage` on `org.rdk.AppStorageManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_valid_appid-asm_36"></a>
### AppStorageManager_DeleteStorage_Valid_AppId (ASM_36)

**Objective:** Verify deleteStorage successfully deletes storage for a valid appId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Valid AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `"<PACKAGEMANAGER_APPLICATION_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="appstoragemanager_deletestorage_empty_appid-asm_37"></a>
### AppStorageManager_DeleteStorage_Empty_AppId (ASM_37)

**Objective:** Verify deleteStorage returns error when appId is empty

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Empty AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_numeric_appid-asm_38"></a>
### AppStorageManager_DeleteStorage_Numeric_AppId (ASM_38)

**Objective:** Verify deleteStorage returns error when appId is numeric

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Numeric AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `123`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_special_characters_appid-asm_39"></a>
### AppStorageManager_DeleteStorage_Special_Characters_AppId (ASM_39)

**Objective:** Verify deleteStorage returns error when appId contains special characters

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Special Characters AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `"()^*!"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_max_length_appid-asm_40"></a>
### AppStorageManager_DeleteStorage_Max_Length_AppId (ASM_40)

**Objective:** Verify deleteStorage returns error when appId exceeds maximum allowed length

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Max Length AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `"ExceedingMaxAllowedLengthAppId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_invalid_characters_appid-asm_41"></a>
### AppStorageManager_DeleteStorage_Invalid_Characters_AppId (ASM_41)

**Objective:** Verify deleteStorage returns error when appId contains whitespace and punctuation

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Invalid Characters AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager` with `appId`: `"appid !@#"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_missing_appid-asm_42"></a>
### AppStorageManager_DeleteStorage_Missing_AppId (ASM_42)

**Objective:** Verify deleteStorage returns error when appId parameter is missing

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeleteStorage Missing AppId | Invoke `deleteStorage` on `org.rdk.AppStorageManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `ERROR_GENERAL` |

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
| Priority | High |
| TDK Release Version | M147 |