## TestScript Name
RDKV_CERT_AVS_RDKWindowManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [RWM_Check_Add_Key_Intercepts](#rwm_check_add_key_intercepts)
   - [RWM_AddKeyIntercepts_Empty_Modifiers](#rwm_addkeyintercepts_empty_modifiers)
   - [RWM_Check_AddKeyIntercepts_Invalid_Keys](#rwm_check_addkeyintercepts_invalid_keys)
   - [RWM_Check_Create_Display_Valid_Params](#rwm_check_create_display_valid_params)
   - [RWM_CreateDisplay_Empty_DisplayParams](#rwm_createdisplay_empty_displayparams)
   - [RWM_Create_Display_Invalid_Params](#rwm_create_display_invalid_params)
   - [RWM_Check_Enable_Inactivity_Reporting](#rwm_check_enable_inactivity_reporting)
   - [RWM_Check_Disable_Inactivity_Reporting](#rwm_check_disable_inactivity_reporting)
   - [RWM_Check_Enable_Inactivity_Reporting_Invalid_Value](#rwm_check_enable_inactivity_reporting_invalid_value)
   - [RWM_Check_GenerateKey_Valid_Key](#rwm_check_generatekey_valid_key)
   - [RWM_GenerateKey_Invalid_KeyCode](#rwm_generatekey_invalid_keycode)
   - [RWM_GenerateKey_No_Params](#rwm_generatekey_no_params)
   - [RWM_Check_Successful_Retrieval_Active_Application_IDs](#rwm_check_successful_retrieval_active_application_ids)
   - [RWM_RemoveKeyIntercept_Valid_Params](#rwm_removekeyintercept_valid_params)
   - [RWM_RemoveKeyIntercept_Invalid_Params](#rwm_removekeyintercept_invalid_params)
   - [RWM_RemoveKeyIntercept_Empty_Params](#rwm_removekeyintercept_empty_params)
   - [RWM_Check_Reset_Inactivity_Time](#rwm_check_reset_inactivity_time)
   - [RWM_Check_SetInactivityInterval_Valid_Positive_Value](#rwm_check_setinactivityinterval_valid_positive_value)
   - [RWM_SetInactivityInterval_NegativeValue](#rwm_setinactivityinterval_negativevalue)
   - [RWM_Check_SetFocus_Valid_Client](#rwm_check_setfocus_valid_client)
   - [RWM_SetFocus_Invalid_Client](#rwm_setfocus_invalid_client)
   - [RWM_SetFocus_Empty_Client](#rwm_setfocus_empty_client)
   - [RWM_SetVisible_Valid_Client_True](#rwm_setvisible_valid_client_true)
   - [RWM_SetVisible_Valid_Client_False](#rwm_setvisible_valid_client_false)
   - [RWM_SetVisible_Invalid_Client](#rwm_setvisible_invalid_client)
   - [RWM_RenderReady_Valid_ClientId](#rwm_renderready_valid_clientid)
   - [RWM_Check_RenderReady_Invalid_ClientId](#rwm_check_renderready_invalid_clientid)
   - [RWM_Check_RenderReady_Empty_ClientId](#rwm_check_renderready_empty_clientid)
   - [RWM_EnableDisplayRender_Valid_ClientId_Enable_True](#rwm_enabledisplayrender_valid_clientid_enable_true)
   - [RWM_Check_EnableDisplayRender_Valid_ClientId_Enable_False](#rwm_check_enabledisplayrender_valid_clientid_enable_false)
   - [RWM_EnableDisplayRender_Invalid_ClientId](#rwm_enabledisplayrender_invalid_clientid)
   - [RWM_Check_SetZOrder_Valid_ClientId_ZOrder](#rwm_check_setzorder_valid_clientid_zorder)
   - [RWM_SetZOrder_Invalid_ClientId](#rwm_setzorder_invalid_clientid)
   - [RWM_SetZOrder_ValidClientId_InvalidZOrder](#rwm_setzorder_validclientid_invalidzorder)
   - [RWM_Check_GetZOrder_Valid_ClientId](#rwm_check_getzorder_valid_clientid)
   - [RWM_Check_GetZOrder_Invalid_ClientId](#rwm_check_getzorder_invalid_clientid)
   - [RWM_GetZOrder_Empty_ClientId](#rwm_getzorder_empty_clientid)
   - [RWM_Check_On_User_Inactivity_Event](#rwm_check_on_user_inactivity_event)
   - [RWM_Check_User_Active](#rwm_check_user_active)
   - [RWM_Reset_Inactivity_Interval](#rwm_reset_inactivity_interval)
   - [RWM_Check_On_User_Inactivity_Event_Disabled_Reporting](#rwm_check_on_user_inactivity_event_disabled_reporting)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **RDKWindowManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.RDKWindowManager` (version 1)

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

### Plugin Pre-condition 5: Activate_RDKWindowManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of RDKWindowManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate RDKWindowManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RDKWindowManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of RDKWindowManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

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

### Plugin Pre-condition 8: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onUserInactivity event | Register a WebSocket event listener for `onUserInactivity` to receive `onUserInactivity` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.register", "params": {"event": "onUserInactivity", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the onScreenshotComplete event | Register a WebSocket event listener for `onScreenshotComplete` to receive `onScreenshotComplete` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.register", "params": {"event": "onScreenshotComplete", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 9: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure packagemanager application name | `PACKAGEMANAGER_APPLICATION_NAME` must be set to the application/package name to be installed | The `PACKAGEMANAGER_APPLICATION_NAME` value should be correctly configured in the device-specific config file |
| 2 | Configure packagemanager application version | `PACKAGEMANAGER_APPLICATION_VERSION` must be set to the application version to be installed | The `PACKAGEMANAGER_APPLICATION_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure packagemanager application hosted URL | `PACKAGEMANAGER_APPLICATION_HOSTEDURL` must be set to the hosted URL of the primary application/package | The `PACKAGEMANAGER_APPLICATION_HOSTEDURL` value should be correctly configured in the device-specific config file |
| 4 | Configure packagemanager application MD5 checksum value | `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` must be set to the expected MD5 checksum of the application/package for download integrity verification | The `PACKAGEMANAGER_APPLICATION_MD5SUM_VALUE` value should be correctly configured in the device-specific config file |
| 5 | Configure packagemanager additionalmetadata name | `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` must be set to the additional metadata key associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_NAME` value should be correctly configured in the device-specific config file |
| 6 | Configure packagemanager additionalmetadata value | `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` must be set to the additional metadata value associated with the application/package | The `PACKAGEMANAGER_ADDITIONALMETADATA_VALUE` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="rwm_check_add_key_intercepts"></a>
### TestCase Name
RWM_Check_Add_Key_Intercepts

### TestCase ID
RWM_01

### TestCase Objective
Pass a valid list of key intercepts and ensure the method successfully adds the intercepts without errors

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Add key intercepts | Invoke addKeyIntercepts on org.rdk.RDKWindowManager with clientId: "<result_step_1>", modifiers: "shift", keyCode: 13<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_addkeyintercepts_empty_modifiers"></a>
### TestCase Name
RWM_AddKeyIntercepts_Empty_Modifiers

### TestCase ID
RWM_02

### TestCase Objective
Pass an empty modifiers parameter to the addKeyIntercepts method and check that the API processes the request successfully without errors, handling the empty input gracefully

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Add key intercepts empty modifiers | Invoke addKeyIntercepts on org.rdk.RDKWindowManager with clientId: "<result_step_1>", modifiers: "", keyCode: 13<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_addkeyintercepts_invalid_keys"></a>
### TestCase Name
RWM_Check_AddKeyIntercepts_Invalid_Keys

### TestCase ID
RWM_03

### TestCase Objective
Pass a list containing invalid key intercepts and ensure the method returns an appropriate error or handles the input correctly

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Add key intercepts invalid | Invoke addKeyIntercepts on org.rdk.RDKWindowManager with clientId: "<result_step_1>", modifiers: "INVALID_MODIFIERS", keyCode: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 0, "modifiers": "INVALID_MODIFIERS", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_create_display_valid_params"></a>
### TestCase Name
RWM_Check_Create_Display_Valid_Params

### TestCase ID
RWM_04

### TestCase Objective
Test the createDisplay method by passing valid displayParams containing all required fields and valid values. Ensure the display is created successfully without errors

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Create display valid params | Invoke createDisplay on org.rdk.RDKWindowManager with clientId: "testdisplay", displayName: "testdisplay", displayWidth: 1920, displayHeight: 1080, virtualWidth: 1920, virtualHeight: 1080<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "testdisplay", "displayName": "testdisplay", "displayWidth": 1920, "displayHeight": 1080, "virtualWidth": 1920, "virtualHeight": 1080}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_createdisplay_empty_displayparams"></a>
### TestCase Name
RWM_CreateDisplay_Empty_DisplayParams

### TestCase ID
RWM_05

### TestCase Objective
Test the createDisplay method by passing an empty object or null as displayParams. Ensure the method handles the input gracefully and returns an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Create display empty params | Invoke createDisplay on org.rdk.RDKWindowManager with clientId: "", displayName: "", displayWidth: "", displayHeight: "", virtualWidth: "", virtualHeight: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "", "displayName": "", "displayWidth": "", "displayHeight": "", "virtualWidth": "", "virtualHeight": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_create_display_invalid_params"></a>
### TestCase Name
RWM_Create_Display_Invalid_Params

### TestCase ID
RWM_06

### TestCase Objective
Test the createDisplay method by passing displayParams with invalid or malformed data

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Create display invalid params | Invoke createDisplay on org.rdk.RDKWindowManager with clientId: "INVALID_CLIENT", displayName: "INVALID_DISPLAY", displayWidth: 0, displayHeight: 0, virtualWidth: 0, virtualHeight: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "INVALID_CLIENT", "displayName": "INVALID_DISPLAY", "displayWidth": 0, "displayHeight": 0, "virtualWidth": 0, "virtualHeight": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_enable_inactivity_reporting"></a>
### TestCase Name
RWM_Check_Enable_Inactivity_Reporting

### TestCase ID
RWM_07

### TestCase Objective
Test the API by passing enable parameter as true to ensure inactivity reporting is successfully enabled

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable inactivity reporting | Invoke enableInactivityReporting on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_disable_inactivity_reporting"></a>
### TestCase Name
RWM_Check_Disable_Inactivity_Reporting

### TestCase ID
RWM_08

### TestCase Objective
Test the API by passing enable parameter as false to ensure inactivity reporting is successfully disabled

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable inactivity reporting | Invoke enableInactivityReporting on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_enable_inactivity_reporting_invalid_value"></a>
### TestCase Name
RWM_Check_Enable_Inactivity_Reporting_Invalid_Value

### TestCase ID
RWM_09

### TestCase Objective
Test the API by passing an invalid value for enable to ensure the API handles invalid inputs gracefully and returns an appropriate error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable inactivity reporting invalid | Invoke enableInactivityReporting on org.rdk.RDKWindowManager with enable: "InvalidValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": "InvalidValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_generatekey_valid_key"></a>
### TestCase Name
RWM_Check_GenerateKey_Valid_Key

### TestCase ID
RWM_10

### TestCase Objective
Verify the behavior of generateKey when called with valid key press and release. Ensure the method triggers the correct key without errors

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Generate key valid events | Invoke generateKey on org.rdk.RDKWindowManager with clientId: "<result_step_1>", modifiers: "shift", keyCode: 13, delay: 10.0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift", "delay": 10.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_generatekey_invalid_keycode"></a>
### TestCase Name
RWM_GenerateKey_Invalid_KeyCode

### TestCase ID
RWM_11

### TestCase Objective
Test generateKey with invalid or unsupported key codes. Verify that the method handles the input gracefully and does not trigger any unintended behavior

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Generate key invalid | Invoke generateKey on org.rdk.RDKWindowManager with clientId: "<result_step_1>", keyCode: "INVALID_KEY", modifiers: "shift", delay: 10<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_1>", "keyCode": "INVALID_KEY", "modifiers": "shift", "delay": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_generatekey_no_params"></a>
### TestCase Name
RWM_GenerateKey_No_Params

### TestCase ID
RWM_12

### TestCase Objective
Check the response of generateKey when no parameters are provided. Ensure the method either throws an appropriate error or handles the scenario as expected

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Generate key no params | Invoke generateKey on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_successful_retrieval_active_application_ids"></a>
### TestCase Name
RWM_Check_Successful_Retrieval_Active_Application_IDs

### TestCase ID
RWM_13

### TestCase Objective
Verify the successful retrieval of active application IDs when there are multiple active applications

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get active application IDs | Invoke getApps on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that the apps list is returned successfully |

---

<a id="rwm_removekeyintercept_valid_params"></a>
### TestCase Name
RWM_RemoveKeyIntercept_Valid_Params

### TestCase ID
RWM_14

### TestCase Objective
Pass a valid intercept parameter and ensure the key intercept is successfully removed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Remove key intercept | Invoke removeKeyIntercept on org.rdk.RDKWindowManager with clientId: "<result_step_1>", modifiers: "shift", keyCode: 13<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_removekeyintercept_invalid_params"></a>
### TestCase Name
RWM_RemoveKeyIntercept_Invalid_Params

### TestCase ID
RWM_15

### TestCase Objective
Verify removeKeyIntercept with an invalid intercept value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Remove key intercept invalid | Invoke removeKeyIntercept on org.rdk.RDKWindowManager with clientId: "InvalidClient", keyCode: "InvalidKeyCode", modifiers: "InvalidModifiers"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "InvalidClient", "keyCode": "InvalidKeyCode", "modifiers": "InvalidModifiers"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_removekeyintercept_empty_params"></a>
### TestCase Name
RWM_RemoveKeyIntercept_Empty_Params

### TestCase ID
RWM_16

### TestCase Objective
Pass a null or empty intercept parameter and ensure the API handles the input gracefully, returning an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Remove key intercept empty | Invoke removeKeyIntercept on org.rdk.RDKWindowManager with clientId: "", keyCode: "", modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "", "keyCode": "", "modifiers": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_reset_inactivity_time"></a>
### TestCase Name
RWM_Check_Reset_Inactivity_Time

### TestCase ID
RWM_17

### TestCase Objective
Call the resetInactivityTime method and ensure it executes successfully, resetting the inactivity timer as expected

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset inactivity time | Invoke resetInactivityTime on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_setinactivityinterval_valid_positive_value"></a>
### TestCase Name
RWM_Check_SetInactivityInterval_Valid_Positive_Value

### TestCase ID
RWM_18

### TestCase Objective
Call the setInactivityInterval method with a valid positive integer value for the interval parameter. Ensure the method executes successfully and sets the inactivity interval as expected.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: 5<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 5}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_setinactivityinterval_negativevalue"></a>
### TestCase Name
RWM_SetInactivityInterval_NegativeValue

### TestCase ID
RWM_19

### TestCase Objective
Call the setInactivityInterval method with a negative integer value for the interval parameter and ensure it returns an appropriate error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval negative | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: -100<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": -100}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_setfocus_valid_client"></a>
### TestCase Name
RWM_Check_SetFocus_Valid_Client

### TestCase ID
RWM_20

### TestCase Objective
Pass a valid client to the setFocus method and ensure the focus is successfully set to the specified application

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Set focus valid client | Invoke setFocus on org.rdk.RDKWindowManager with client: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_setfocus_invalid_client"></a>
### TestCase Name
RWM_SetFocus_Invalid_Client

### TestCase ID
RWM_21

### TestCase Objective
Pass an invalid or non-existent client to the setFocus method and ensure the method returns an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set focus invalid client | Invoke setFocus on org.rdk.RDKWindowManager with client: "InvalidClient"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "InvalidClient"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setfocus_empty_client"></a>
### TestCase Name
RWM_SetFocus_Empty_Client

### TestCase ID
RWM_22

### TestCase Objective
Pass an empty string as the client to the setFocus method and ensure the method handles the input gracefully, returning an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set focus empty client | Invoke setFocus on org.rdk.RDKWindowManager with client: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setvisible_valid_client_true"></a>
### TestCase Name
RWM_SetVisible_Valid_Client_True

### TestCase ID
RWM_23

### TestCase Objective
Test the setVisible method by passing a valid client and setting visible to true. Ensure the application becomes visible successfully

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Set visible valid client true | Invoke setVisible on org.rdk.RDKWindowManager with client: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<result_step_1>", "visible": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_setvisible_valid_client_false"></a>
### TestCase Name
RWM_SetVisible_Valid_Client_False

### TestCase ID
RWM_24

### TestCase Objective
Test the setVisible method by passing a valid client and setting visible to false. Ensure the application becomes hidden successfully

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Set visible valid client false | Invoke setVisible on org.rdk.RDKWindowManager with client: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<result_step_1>", "visible": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_setvisible_invalid_client"></a>
### TestCase Name
RWM_SetVisible_Invalid_Client

### TestCase ID
RWM_25

### TestCase Objective
Test the setVisible method by passing an invalid client and setting visible to true. Ensure the method handles the invalid client gracefully and returns an appropriate error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set visible invalid client | Invoke setVisible on org.rdk.RDKWindowManager with client: "InvalidClient"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "InvalidClient", "visible": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_renderready_valid_clientid"></a>
### TestCase Name
RWM_RenderReady_Valid_ClientId

### TestCase ID
RWM_26

### TestCase Objective
Call the renderReady method with a valid clientId of an application that has rendered its first frame. Ensure the method returns true indicating the application is ready

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Render ready valid ClientId | Invoke renderReady on org.rdk.RDKWindowManager with clientId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_renderready_invalid_clientid"></a>
### TestCase Name
RWM_Check_RenderReady_Invalid_ClientId

### TestCase ID
RWM_27

### TestCase Objective
Call the renderReady method with an invalid or non-existent clientId. Ensure the method returns false or an appropriate error response indicating the application is not ready

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Render ready invalid ClientId | Invoke renderReady on org.rdk.RDKWindowManager with clientId: "InvalidClientId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": "InvalidClientId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_renderready_empty_clientid"></a>
### TestCase Name
RWM_Check_RenderReady_Empty_ClientId

### TestCase ID
RWM_28

### TestCase Objective
Call the renderReady method with a null or empty string as the clientId. Ensure the method handles the input gracefully and returns an error or false indicating invalid input

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | RenderReady empty ClientId | Invoke renderReady on org.rdk.RDKWindowManager with clientId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_enabledisplayrender_valid_clientid_enable_true"></a>
### TestCase Name
RWM_EnableDisplayRender_Valid_ClientId_Enable_True

### TestCase ID
RWM_29

### TestCase Objective
Call the enableDisplayRender method with a valid clientId and set enable to true. Ensure the display rendering is successfully enabled for the specified application instance

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Enable display render | Invoke enableDisplayRender on org.rdk.RDKWindowManager with clientId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "<result_step_1>", "enable": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_enabledisplayrender_valid_clientid_enable_false"></a>
### TestCase Name
RWM_Check_EnableDisplayRender_Valid_ClientId_Enable_False

### TestCase ID
RWM_30

### TestCase Objective
Call the enableDisplayRender method with a valid clientId and set enable to false. Ensure the display rendering is successfully disabled for the specified application instance

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Disable display render | Invoke enableDisplayRender on org.rdk.RDKWindowManager with clientId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "<result_step_1>", "enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_enabledisplayrender_invalid_clientid"></a>
### TestCase Name
RWM_EnableDisplayRender_Invalid_ClientId

### TestCase ID
RWM_31

### TestCase Objective
Call the enableDisplayRender method with an invalid or non-existent clientId and set enable to true. Ensure the method returns an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable display render invalid ClientId | Invoke enableDisplayRender on org.rdk.RDKWindowManager with clientId: "InvalidClientId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "InvalidClientId", "enable": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_setzorder_valid_clientid_zorder"></a>
### TestCase Name
RWM_Check_SetZOrder_Valid_ClientId_ZOrder

### TestCase ID
RWM_32

### TestCase Objective
Test the setZOrder method by providing a valid clientId and a valid zOrder value. Ensure the method sets the z-order successfully without errors

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Set z order valid params | Invoke setZOrder on org.rdk.RDKWindowManager with clientId: "<result_step_1>", zOrder: 1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "<result_step_1>", "zOrder": 1}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_setzorder_invalid_clientid"></a>
### TestCase Name
RWM_SetZOrder_Invalid_ClientId

### TestCase ID
RWM_33

### TestCase Objective
Test the setZOrder method by providing an invalid clientId and a valid zOrder value. Ensure the method returns an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set z order invalid ClientId | Invoke setZOrder on org.rdk.RDKWindowManager with clientId: "InvalidClientId", zOrder: 1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "InvalidClientId", "zOrder": 1}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setzorder_validclientid_invalidzorder"></a>
### TestCase Name
RWM_SetZOrder_ValidClientId_InvalidZOrder

### TestCase ID
RWM_34

### TestCase Objective
Test the setZOrder method by providing a valid clientId and an invalid zOrder value. Ensure the method returns an appropriate error or failure response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | Set z order invalid ZOrder | Invoke setZOrder on org.rdk.RDKWindowManager with clientId: "<result_step_1>", zOrder: "InvalidZOrderValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "<result_step_1>", "zOrder": "InvalidZOrderValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_getzorder_valid_clientid"></a>
### TestCase Name
RWM_Check_GetZOrder_Valid_ClientId

### TestCase ID
RWM_35

### TestCase Objective
Pass a valid clientId to the getZOrder method and ensure it returns the correct z-order value for the specified application

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 2 | GetZOrder valid ClientId | Invoke getZOrder on org.rdk.RDKWindowManager with clientId: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call returns a valid z-order reference |

---

<a id="rwm_check_getzorder_invalid_clientid"></a>
### TestCase Name
RWM_Check_GetZOrder_Invalid_ClientId

### TestCase ID
RWM_36

### TestCase Objective
Pass an invalid or non-existent clientId to the getZOrder method and ensure it returns an appropriate error or null response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Verify GetZOrder invalid ClientId | Invoke getZOrder on org.rdk.RDKWindowManager with clientId: "InvalidClientId"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": "InvalidClientId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_getzorder_empty_clientid"></a>
### TestCase Name
RWM_GetZOrder_Empty_ClientId

### TestCase ID
RWM_37

### TestCase Objective
Verify getZOrder with a null or empty clientId

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetZOrder empty ClientId | Invoke getZOrder on org.rdk.RDKWindowManager with clientId: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_on_user_inactivity_event"></a>
### TestCase Name
RWM_Check_On_User_Inactivity_Event

### TestCase ID
RWM_L2_01

### TestCase Objective
Test the user inactivity reporting by enabling it, setting a short inactivity interval, and verifying that the OnUserInactivity event is triggered after the specified interval of user inactivity

### TestCase Pre-condition

#### TestCase Pre-condition 1: Reset_Enable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset inactivity time | Reset Inactivity Time on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Enable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: 1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check on UserInactivity event | Listen for event Event_On_User_Inactivity | Verify that event data is validated successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Disable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_user_active"></a>
### TestCase Name
RWM_Check_User_Active

### TestCase ID
RWM_L2_02

### TestCase Objective
Check device returns to active mode after user input via generateKey when it was previously inactive

### TestCase Pre-condition

#### TestCase Pre-condition 1: Reset_Enable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset inactivity time | Reset Inactivity Time on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Enable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: 1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check on UserInactivity event | Listen for event Event_On_User_Inactivity | Verify that event data is validated successfully |
| 3 | Get AppInstance id | Invoke getLoadedApps on org.rdk.AppManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Verify that application `<PACKAGEMANAGER_APPLICATION_NAME>` is in `APP_STATE_ACTIVE` state as expected  |
| 4 | Generate key valid events | Invoke generateKey on org.rdk.RDKWindowManager with clientId: "<result_step_3>", modifiers: "shift", keyCode: 13, delay: 3.0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_3>", "keyCode": 13, "modifiers": "shift", "delay": 3.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Disable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_reset_inactivity_interval"></a>
### TestCase Name
RWM_Reset_Inactivity_Interval

### TestCase ID
RWM_L2_03

### TestCase Objective
Test the resetInactivityTime method to ensure it resets the inactivity timer correctly

### TestCase Pre-condition

#### TestCase Pre-condition 1: Reset_Enable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset inactivity time | Reset Inactivity Time on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Enable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: 2<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 2}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check on UserInactivity event | Listen for event Event_On_User_Inactivity | Verify that event data is validated successfully |
| 3 | Reset inactivity time | Invoke resetInactivityTime on org.rdk.RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Check on UserInactivity event | Listen for event Event_On_User_Inactivity | Verify that event data is validated successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Disable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="rwm_check_on_user_inactivity_event_disabled_reporting"></a>
### TestCase Name
RWM_Check_On_User_Inactivity_Event_Disabled_Reporting

### TestCase ID
RWM_L2_04

### TestCase Objective
Checks whether the user inactivity reporting event is triggered when inactivity reporting is disabled

### TestCase Pre-condition

#### TestCase Pre-condition 1: Disable_Inactivity_Reporting

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Disable inactivity reporting | Enable Inactivity Reporting on RDKWindowManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set inactivity interval | Invoke setInactivityInterval on org.rdk.RDKWindowManager with interval: 1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Check on UserInactivity event NoEvent | Listen for event Event_On_User_Inactivity | Verify that no event is triggered during this operation  |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onUserInactivity event | Unregister the WebSocket event listener for `onUserInactivity` to stop receiving `onUserInactivity` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.unregister", "params": {"event": "onUserInactivity", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the onScreenshotComplete event | Unregister the WebSocket event listener for `onScreenshotComplete` to stop receiving `onScreenshotComplete` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.unregister", "params": {"event": "onScreenshotComplete", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

### Plugin Post-condition 2: Uninstall_Package

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
