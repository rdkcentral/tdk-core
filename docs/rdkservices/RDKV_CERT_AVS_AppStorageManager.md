## TestScript Name
RDKV_CERT_AVS_AppStorageManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [AppStorageManager_Clear_App_Data](#appstoragemanager_clear_app_data)
   - [AppStorageManager_Clear_App_Data_Invalid_AppId](#appstoragemanager_clear_app_data_invalid_appid)
   - [AppStorageManager_Clear_App_Data_Numeric_AppId](#appstoragemanager_clear_app_data_numeric_appid)
   - [AppStorageManager_Clear_Special_Characters_AppId](#appstoragemanager_clear_special_characters_appid)
   - [AppStorageManager_Clear_Method_Max_Length_Error](#appstoragemanager_clear_method_max_length_error)
   - [AppStorageManager_Clear_App_Data_Invalid_Characters](#appstoragemanager_clear_app_data_invalid_characters)
   - [AppStorageManager_ClearAll_Single_Valid_AppID](#appstoragemanager_clearall_single_valid_appid)
   - [AppStorageManager_ClearAll_Empty_ExemptionAppIds](#appstoragemanager_clearall_empty_exemptionappids)
   - [AppStorageManager_ClearAll_Invalid_AppID](#appstoragemanager_clearall_invalid_appid)
   - [AppStorageManager_ClearAll_Special_Characters](#appstoragemanager_clearall_special_characters)
   - [AppStorageManager_ClearAll_Max_Length_Error](#appstoragemanager_clearall_max_length_error)
   - [AppStorageManager_ClearAll_Invalid_Characters](#appstoragemanager_clearall_invalid_characters)
   - [AppStorageManager_ClearAll_Numeric_ExemptionAppIds](#appstoragemanager_clearall_numeric_exemptionappids)
   - [AppStorageManager_Clear_All_Without_Parameter](#appstoragemanager_clear_all_without_parameter)
   - [AppStorageManager_GetStorage_Valid_Params](#appstoragemanager_getstorage_valid_params)
   - [AppStorageManager_GetStorage_Empty_AppId](#appstoragemanager_getstorage_empty_appid)
   - [AppStorageManager_GetStorage_Numeric_AppId](#appstoragemanager_getstorage_numeric_appid)
   - [AppStorageManager_GetStorage_Special_Characters_AppId](#appstoragemanager_getstorage_special_characters_appid)
   - [AppStorageManager_GetStorage_Max_Length_AppId](#appstoragemanager_getstorage_max_length_appid)
   - [AppStorageManager_GetStorage_Invalid_Characters_AppId](#appstoragemanager_getstorage_invalid_characters_appid)
   - [AppStorageManager_GetStorage_Missing_UserId](#appstoragemanager_getstorage_missing_userid)
   - [AppStorageManager_GetStorage_Missing_GroupId](#appstoragemanager_getstorage_missing_groupid)
   - [AppStorageManager_GetStorage_NonInteger_UserId](#appstoragemanager_getstorage_noninteger_userid)
   - [AppStorageManager_GetStorage_NonInteger_GroupId](#appstoragemanager_getstorage_noninteger_groupid)
   - [AppStorageManager_GetStorage_All_Params_Missing](#appstoragemanager_getstorage_all_params_missing)
   - [AppStorageManager_CreateStorage_Valid_Params](#appstoragemanager_createstorage_valid_params)
   - [AppStorageManager_CreateStorage_Empty_AppId](#appstoragemanager_createstorage_empty_appid)
   - [AppStorageManager_CreateStorage_Numeric_AppId](#appstoragemanager_createstorage_numeric_appid)
   - [AppStorageManager_CreateStorage_Special_Characters_AppId](#appstoragemanager_createstorage_special_characters_appid)
   - [AppStorageManager_CreateStorage_Max_Length_AppId](#appstoragemanager_createstorage_max_length_appid)
   - [AppStorageManager_CreateStorage_Invalid_Characters_AppId](#appstoragemanager_createstorage_invalid_characters_appid)
   - [AppStorageManager_CreateStorage_Missing_Size](#appstoragemanager_createstorage_missing_size)
   - [AppStorageManager_CreateStorage_NonInteger_Size](#appstoragemanager_createstorage_noninteger_size)
   - [AppStorageManager_CreateStorage_Zero_Size](#appstoragemanager_createstorage_zero_size)
   - [AppStorageManager_CreateStorage_All_Params_Missing](#appstoragemanager_createstorage_all_params_missing)
   - [AppStorageManager_DeleteStorage_Valid_AppId](#appstoragemanager_deletestorage_valid_appid)
   - [AppStorageManager_DeleteStorage_Empty_AppId](#appstoragemanager_deletestorage_empty_appid)
   - [AppStorageManager_DeleteStorage_Numeric_AppId](#appstoragemanager_deletestorage_numeric_appid)
   - [AppStorageManager_DeleteStorage_Special_Characters_AppId](#appstoragemanager_deletestorage_special_characters_appid)
   - [AppStorageManager_DeleteStorage_Max_Length_AppId](#appstoragemanager_deletestorage_max_length_appid)
   - [AppStorageManager_DeleteStorage_Invalid_Characters_AppId](#appstoragemanager_deletestorage_invalid_characters_appid)
   - [AppStorageManager_DeleteStorage_Missing_AppId](#appstoragemanager_deletestorage_missing_appid)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **AppStorageManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.AppStorageManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_AppStorageManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of AppStorageManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_PackageManagerRDKEMS_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PackageManagerRDKEMS plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Check_Existing_Package_Before_Install

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download valid parameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install package on device | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify installed package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 4: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure packagemanager application name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure packagemanager application version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure packagemanager application hostedurl | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure packagemanager additionalmetadata name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure packagemanager additionalmetadata value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure packagemanager application md5sum value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="appstoragemanager_clear_app_data"></a>
### TestCase Name
AppStorageManager_Clear_App_Data

### TestCase ID
ASM_01

### TestCase Objective
Verify the clear method successfully clears data for a valid appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear app data | Invoke clear on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_clear_app_data_invalid_appid"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Invalid_AppId

### TestCase ID
ASM_02

### TestCase Objective
Verify the clear method returns an error when appId is an empty string

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear app data invalid AppId | Invoke clear on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_numeric_appid"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Numeric_AppId

### TestCase ID
ASM_03

### TestCase Objective
Verify the clear method returns an error when appId is a non-string value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear app data numeric AppId | Invoke clear on org.rdk.AppStorageManager with appId: 123<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_special_characters_appid"></a>
### TestCase Name
AppStorageManager_Clear_Special_Characters_AppId

### TestCase ID
ASM_04

### TestCase Objective
Verify the clear method handles special characters in appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear app data special characters | Invoke clear on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_method_max_length_error"></a>
### TestCase Name
AppStorageManager_Clear_Method_Max_Length_Error

### TestCase ID
ASM_05

### TestCase Objective
Verify the clear method returns an error when appId exceeds the maximum allowed length

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear app data max length error | Invoke clear on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_invalid_characters"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Invalid_Characters

### TestCase ID
ASM_06

### TestCase Objective
Verify the clear method returns an error when appId contains whitespace and punctuation characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear invalid AppId | Invoke clear on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_single_valid_appid"></a>
### TestCase Name
AppStorageManager_ClearAll_Single_Valid_AppID

### TestCase ID
ASM_07

### TestCase Objective
Call the clearAll method with one valid app ID in exemptionAppIds and ensure app data except the exempted app is cleared

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all with exemption | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_clearall_empty_exemptionappids"></a>
### TestCase Name
AppStorageManager_ClearAll_Empty_ExemptionAppIds

### TestCase ID
ASM_08

### TestCase Objective
Call the clearAll method with an empty list for exemptionAppIds and ensure all app data is cleared

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all empty ExemptionAppIds | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_appid"></a>
### TestCase Name
AppStorageManager_ClearAll_Invalid_AppID

### TestCase ID
ASM_09

### TestCase Objective
Verify clearAll with an invalid app ID in exemptionAppIds

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all invalid AppID | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_special_characters"></a>
### TestCase Name
AppStorageManager_ClearAll_Special_Characters

### TestCase ID
ASM_10

### TestCase Objective
Verify clearAll with exemptionAppIds containing special characters or non-alphanumeric values

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all special characters | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_max_length_error"></a>
### TestCase Name
AppStorageManager_ClearAll_Max_Length_Error

### TestCase ID
ASM_11

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds exceeds the maximum allowed length

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all max length error | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_characters"></a>
### TestCase Name
AppStorageManager_ClearAll_Invalid_Characters

### TestCase ID
ASM_12

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds contains whitespace and punctuation characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all invalid characters | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_numeric_exemptionappids"></a>
### TestCase Name
AppStorageManager_ClearAll_Numeric_ExemptionAppIds

### TestCase ID
ASM_13

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds is a numeric value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all numeric ExemptionAppIds | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_all_without_parameter"></a>
### TestCase Name
AppStorageManager_Clear_All_Without_Parameter

### TestCase ID
ASM_14

### TestCase Objective
Check that all app storage is deleted when the exemptionAppIds parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear all without parameter | Invoke clearAll on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_valid_params"></a>
### TestCase Name
AppStorageManager_GetStorage_Valid_Params

### TestCase ID
ASM_15

### TestCase Objective
Verify getStorage returns storage location for valid appId, userId, and groupId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage valid params | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_empty_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Empty_AppId

### TestCase ID
ASM_16

### TestCase Objective
Verify getStorage returns error when appId is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage empty AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "", userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Numeric_AppId

### TestCase ID
ASM_17

### TestCase Objective
Verify getStorage returns error when appId is numeric

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage numeric AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: 123, userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": 123, "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Special_Characters_AppId

### TestCase ID
ASM_18

### TestCase Objective
Verify getStorage returns error when appId contains special characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage special characters AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "()^*!", userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "()^*!", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Max_Length_AppId

### TestCase ID
ASM_19

### TestCase Objective
Verify getStorage returns error when appId exceeds maximum allowed length

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage max length AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId", userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Invalid_Characters_AppId

### TestCase ID
ASM_20

### TestCase Objective
Verify getStorage returns error when appId contains whitespace and punctuation

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage invalid characters AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "appid !@#", userId: 1001, groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "appid !@#", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_userid"></a>
### TestCase Name
AppStorageManager_GetStorage_Missing_UserId

### TestCase ID
ASM_21

### TestCase Objective
Verify getStorage returns error when userId is missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage missing UserId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_groupid"></a>
### TestCase Name
AppStorageManager_GetStorage_Missing_GroupId

### TestCase ID
ASM_22

### TestCase Objective
Verify getStorage returns error when groupId is missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage missing GroupId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", userId: 1001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_userid"></a>
### TestCase Name
AppStorageManager_GetStorage_NonInteger_UserId

### TestCase ID
ASM_23

### TestCase Objective
Verify getStorage returns error when userId is not an integer

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage NonInteger UserId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", userId: "abc", groupId: 2001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": "abc", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_groupid"></a>
### TestCase Name
AppStorageManager_GetStorage_NonInteger_GroupId

### TestCase ID
ASM_24

### TestCase Objective
Verify getStorage returns error when groupId is not an integer

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage NonInteger GroupId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", groupId: "xyz", userId: 1001<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": "xyz"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_all_params_missing"></a>
### TestCase Name
AppStorageManager_GetStorage_All_Params_Missing

### TestCase ID
ASM_25

### TestCase Objective
Verify getStorage returns error when all parameters are missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage all params missing | Invoke getStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_valid_params"></a>
### TestCase Name
AppStorageManager_CreateStorage_Valid_Params

### TestCase ID
ASM_26

### TestCase Objective
Verify createStorage returns storage path for valid appId and size

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage valid params | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", size: 102400<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 102400}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_createstorage_empty_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Empty_AppId

### TestCase ID
ASM_27

### TestCase Objective
Verify createStorage returns error when appId is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage empty AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "", size: 1024<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Numeric_AppId

### TestCase ID
ASM_28

### TestCase Objective
Verify createStorage returns error when appId is numeric

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage numeric AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: 123, size: 1024<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": 123, "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Special_Characters_AppId

### TestCase ID
ASM_29

### TestCase Objective
Verify createStorage returns error when appId contains special characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage special characters AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "()^*!", size: 1024<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "()^*!", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Max_Length_AppId

### TestCase ID
ASM_30

### TestCase Objective
Verify createStorage returns error when appId exceeds maximum allowed length

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage max length AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId", size: 1024<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Invalid_Characters_AppId

### TestCase ID
ASM_31

### TestCase Objective
Verify createStorage returns error when appId contains whitespace and punctuation

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage invalid characters AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "appid !@#", size: 1024<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "appid !@#", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_missing_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_Missing_Size

### TestCase ID
ASM_32

### TestCase Objective
Verify createStorage returns error when size is missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage missing size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_noninteger_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_NonInteger_Size

### TestCase ID
ASM_33

### TestCase Objective
Verify createStorage returns error when size is not an integer

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage NonInteger size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", size: "abc"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": "abc"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_zero_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_Zero_Size

### TestCase ID
ASM_34

### TestCase Objective
Verify createStorage returns error when size is zero

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage zero size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", size: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_all_params_missing"></a>
### TestCase Name
AppStorageManager_CreateStorage_All_Params_Missing

### TestCase ID
ASM_35

### TestCase Objective
Verify createStorage returns error when all parameters are missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage all params missing | Invoke createStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_valid_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Valid_AppId

### TestCase ID
ASM_36

### TestCase Objective
Verify deleteStorage successfully deletes storage for a valid appId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage valid AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_deletestorage_empty_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Empty_AppId

### TestCase ID
ASM_37

### TestCase Objective
Verify deleteStorage returns error when appId is empty

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage empty AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Numeric_AppId

### TestCase ID
ASM_38

### TestCase Objective
Verify deleteStorage returns error when appId is numeric

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage numeric AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: 123<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Special_Characters_AppId

### TestCase ID
ASM_39

### TestCase Objective
Verify deleteStorage returns error when appId contains special characters

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage special characters AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Max_Length_AppId

### TestCase ID
ASM_40

### TestCase Objective
Verify deleteStorage returns error when appId exceeds maximum allowed length

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage max length AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Invalid_Characters_AppId

### TestCase ID
ASM_41

### TestCase Objective
Verify deleteStorage returns error when appId contains whitespace and punctuation

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage invalid characters AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_missing_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Missing_AppId

### TestCase ID
ASM_42

### TestCase Objective
Verify deleteStorage returns error when appId parameter is missing

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage missing AppId | Invoke deleteStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check existing package | Get packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall existing package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M147

<div align="right"><a href="#testscript-name">Go to Top</a></div>
