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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.AppStorageManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of AppStorageManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.AppStorageManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_PackageManagerRDKEMS_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PackageManagerRDKEMS"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PackageManagerRDKEMS Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PackageManagerRDKEMS"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Check_Existing_Package_Before_Install

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Download ValidParameters | Download on DownloadManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DownloadManager.1.download", "params": {"url": "<PACKAGEMANAGER_APPLICATION_HOSTEDURL>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that a valid downloadId is returned |
| 4 | Install | Install on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.install", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>", "version": "<PACKAGEMANAGER_APPLICATION_VERSION>", "fileLocator": "<result_step_4>", "name": "<PACKAGEMANAGER_ADDITIONALMETADATA_NAME>", "value": "<PACKAGEMANAGER_ADDITIONALMETADATA_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Verify Installed Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the installed package is present in the package list |

### Plugin Pre-condition 4: Configure_Device_Parameter

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Packagemanager Application Name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure Packagemanager Application Version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure Packagemanager Application Hostedurl | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure Packagemanager Additionalmetadata Name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 5 | Configure Packagemanager Additionalmetadata Value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
| 6 | Configure Packagemanager Application Md5sum Value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="appstoragemanager_clear_app_data"></a>
### TestCase Name
AppStorageManager_Clear_App_Data

### TestCase ID
ASM_01

### TestCase Objective
Verify the clear method successfully clears data for a valid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear App Data | Invoke clear on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_clear_app_data_invalid_appid"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Invalid_AppId

### TestCase ID
ASM_02

### TestCase Objective
Verify the clear method returns an error when appId is an empty string

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear App Data Invalid AppId | Invoke clear on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_numeric_appid"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Numeric_AppId

### TestCase ID
ASM_03

### TestCase Objective
Verify the clear method returns an error when appId is a non-string value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear App Data Numeric AppId | Invoke clear on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_special_characters_appid"></a>
### TestCase Name
AppStorageManager_Clear_Special_Characters_AppId

### TestCase ID
ASM_04

### TestCase Objective
Verify the clear method handles special characters in appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear App Data Special Characters | Invoke clear on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_method_max_length_error"></a>
### TestCase Name
AppStorageManager_Clear_Method_Max_Length_Error

### TestCase ID
ASM_05

### TestCase Objective
Verify the clear method returns an error when appId exceeds the maximum allowed length

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear App Data Max Length Error | Invoke clear on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_app_data_invalid_characters"></a>
### TestCase Name
AppStorageManager_Clear_App_Data_Invalid_Characters

### TestCase ID
ASM_06

### TestCase Objective
Verify the clear method returns an error when appId contains whitespace and punctuation characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear Invalid AppId | Invoke clear on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clear", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_single_valid_appid"></a>
### TestCase Name
AppStorageManager_ClearAll_Single_Valid_AppID

### TestCase ID
ASM_07

### TestCase Objective
Call the clearAll method with one valid app ID in exemptionAppIds and ensure app data except the exempted app is cleared

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All With Exemption | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_clearall_empty_exemptionappids"></a>
### TestCase Name
AppStorageManager_ClearAll_Empty_ExemptionAppIds

### TestCase ID
ASM_08

### TestCase Objective
Call the clearAll method with an empty list for exemptionAppIds and ensure all app data is cleared

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Empty ExemptionAppIds | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_appid"></a>
### TestCase Name
AppStorageManager_ClearAll_Invalid_AppID

### TestCase ID
ASM_09

### TestCase Objective
Verify clearAll with an invalid app ID in exemptionAppIds

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Invalid AppID | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "InvalidAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "InvalidAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_special_characters"></a>
### TestCase Name
AppStorageManager_ClearAll_Special_Characters

### TestCase ID
ASM_10

### TestCase Objective
Verify clearAll with exemptionAppIds containing special characters or non-alphanumeric values

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Special Characters | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_max_length_error"></a>
### TestCase Name
AppStorageManager_ClearAll_Max_Length_Error

### TestCase ID
ASM_11

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds exceeds the maximum allowed length

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Max Length Error | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_invalid_characters"></a>
### TestCase Name
AppStorageManager_ClearAll_Invalid_Characters

### TestCase ID
ASM_12

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds contains whitespace and punctuation characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Invalid Characters | Invoke clearAll on org.rdk.AppStorageManager with exemptionAppIds: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clearall_numeric_exemptionappids"></a>
### TestCase Name
AppStorageManager_ClearAll_Numeric_ExemptionAppIds

### TestCase ID
ASM_13

### TestCase Objective
Verify the clearAll method returns an error when exemptionAppIds is a numeric value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Numeric ExemptionAppIds | Invoke clearAll on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll", "params": {"exemptionAppIds": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_clear_all_without_parameter"></a>
### TestCase Name
AppStorageManager_Clear_All_Without_Parameter

### TestCase ID
ASM_14

### TestCase Objective
Check that all app storage is deleted when the exemptionAppIds parameter is not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Clear All Without Parameter | Invoke clearAll on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.clearAll"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_valid_params"></a>
### TestCase Name
AppStorageManager_GetStorage_Valid_Params

### TestCase ID
ASM_15

### TestCase Objective
Verify getStorage returns storage location for valid appId, userId, and groupId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Valid Params | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_getstorage_empty_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Empty_AppId

### TestCase ID
ASM_16

### TestCase Objective
Verify getStorage returns error when appId is empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Empty AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Numeric_AppId

### TestCase ID
ASM_17

### TestCase Objective
Verify getStorage returns error when appId is numeric

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Numeric AppId | Invoke getStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": 123, "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Special_Characters_AppId

### TestCase ID
ASM_18

### TestCase Objective
Verify getStorage returns error when appId contains special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Special Characters AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "()^*!", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Max_Length_AppId

### TestCase ID
ASM_19

### TestCase Objective
Verify getStorage returns error when appId exceeds maximum allowed length

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Max Length AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_GetStorage_Invalid_Characters_AppId

### TestCase ID
ASM_20

### TestCase Objective
Verify getStorage returns error when appId contains whitespace and punctuation

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Invalid Characters AppId | Invoke getStorage on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "appid !@#", "userId": 1001, "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_userid"></a>
### TestCase Name
AppStorageManager_GetStorage_Missing_UserId

### TestCase ID
ASM_21

### TestCase Objective
Verify getStorage returns error when userId is missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Missing UserId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_missing_groupid"></a>
### TestCase Name
AppStorageManager_GetStorage_Missing_GroupId

### TestCase ID
ASM_22

### TestCase Objective
Verify getStorage returns error when groupId is missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage Missing GroupId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_userid"></a>
### TestCase Name
AppStorageManager_GetStorage_NonInteger_UserId

### TestCase ID
ASM_23

### TestCase Objective
Verify getStorage returns error when userId is not an integer

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage NonInteger UserId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", userId: "abc"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": "abc", "groupId": 2001}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_noninteger_groupid"></a>
### TestCase Name
AppStorageManager_GetStorage_NonInteger_GroupId

### TestCase ID
ASM_24

### TestCase Objective
Verify getStorage returns error when groupId is not an integer

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage NonInteger GroupId | Invoke getStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", groupId: "xyz"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "userId": 1001, "groupId": "xyz"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_getstorage_all_params_missing"></a>
### TestCase Name
AppStorageManager_GetStorage_All_Params_Missing

### TestCase ID
ASM_25

### TestCase Objective
Verify getStorage returns error when all parameters are missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetStorage All Params Missing | Invoke getStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.getStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_valid_params"></a>
### TestCase Name
AppStorageManager_CreateStorage_Valid_Params

### TestCase ID
ASM_26

### TestCase Objective
Verify createStorage returns storage path for valid appId and size

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Valid Params | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 102400}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_createstorage_empty_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Empty_AppId

### TestCase ID
ASM_27

### TestCase Objective
Verify createStorage returns error when appId is empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Empty AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Numeric_AppId

### TestCase ID
ASM_28

### TestCase Objective
Verify createStorage returns error when appId is numeric

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Numeric AppId | Invoke createStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": 123, "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Special_Characters_AppId

### TestCase ID
ASM_29

### TestCase Objective
Verify createStorage returns error when appId contains special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Special Characters AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "()^*!", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Max_Length_AppId

### TestCase ID
ASM_30

### TestCase Objective
Verify createStorage returns error when appId exceeds maximum allowed length

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Max Length AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_CreateStorage_Invalid_Characters_AppId

### TestCase ID
ASM_31

### TestCase Objective
Verify createStorage returns error when appId contains whitespace and punctuation

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Invalid Characters AppId | Invoke createStorage on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "appid !@#", "size": 1024}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_missing_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_Missing_Size

### TestCase ID
ASM_32

### TestCase Objective
Verify createStorage returns error when size is missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Missing Size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_noninteger_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_NonInteger_Size

### TestCase ID
ASM_33

### TestCase Objective
Verify createStorage returns error when size is not an integer

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage NonInteger Size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>", size: "abc"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": "abc"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_zero_size"></a>
### TestCase Name
AppStorageManager_CreateStorage_Zero_Size

### TestCase ID
ASM_34

### TestCase Objective
Verify createStorage returns error when size is zero

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage Zero Size | Invoke createStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>", "size": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_createstorage_all_params_missing"></a>
### TestCase Name
AppStorageManager_CreateStorage_All_Params_Missing

### TestCase ID
ASM_35

### TestCase Objective
Verify createStorage returns error when all parameters are missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | CreateStorage All Params Missing | Invoke createStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.createStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_valid_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Valid_AppId

### TestCase ID
ASM_36

### TestCase Objective
Verify deleteStorage successfully deletes storage for a valid appId

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Valid AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "<PACKAGEMANAGER_APPLICATION_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="appstoragemanager_deletestorage_empty_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Empty_AppId

### TestCase ID
ASM_37

### TestCase Objective
Verify deleteStorage returns error when appId is empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Empty AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_numeric_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Numeric_AppId

### TestCase ID
ASM_38

### TestCase Objective
Verify deleteStorage returns error when appId is numeric

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Numeric AppId | Invoke deleteStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": 123}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_special_characters_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Special_Characters_AppId

### TestCase ID
ASM_39

### TestCase Objective
Verify deleteStorage returns error when appId contains special characters

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Special Characters AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_max_length_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Max_Length_AppId

### TestCase ID
ASM_40

### TestCase Objective
Verify deleteStorage returns error when appId exceeds maximum allowed length

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Max Length AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "ExceedingMaxAllowedLengthAppId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "ExceedingMaxAllowedLengthAppId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_invalid_characters_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Invalid_Characters_AppId

### TestCase ID
ASM_41

### TestCase Objective
Verify deleteStorage returns error when appId contains whitespace and punctuation

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Invalid Characters AppId | Invoke deleteStorage on org.rdk.AppStorageManager with appId: "appid !@#"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage", "params": {"appId": "appid !@#"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="appstoragemanager_deletestorage_missing_appid"></a>
### TestCase Name
AppStorageManager_DeleteStorage_Missing_AppId

### TestCase ID
ASM_42

### TestCase Objective
Verify deleteStorage returns error when appId parameter is missing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeleteStorage Missing AppId | Invoke deleteStorage on org.rdk.AppStorageManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppStorageManager.1.deleteStorage"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

## Plugin Post-conditions

### Plugin Post-condition 1: Uninstall_Package

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Existing Package | Get Packages from PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.listPackages"}' http://127.0.0.1:9998/jsonrpc` | Verify that the package list is returned successfully |
| 2 | Uninstall Existing Package | *(Conditional statement executed only if package/app is currently present)*<br>Uninstall on PackageManagerRDKEMS<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PackageManagerRDKEMS.1.uninstall", "params": {"packageId": "<PACKAGEMANAGER_APPLICATION_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M147 |

<div align="right"><a href="#">&#8593; Go to Top</a></div>
