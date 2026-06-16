## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [RWM_Check_Add_Key_Intercepts (RWM_01)](#rwm_check_add_key_intercepts-rwm_01)
   - [RWM_AddKeyIntercepts_Empty_Modifiers (RWM_02)](#rwm_addkeyintercepts_empty_modifiers-rwm_02)
   - [RWM_Check_AddKeyIntercepts_Invalid_Keys (RWM_03)](#rwm_check_addkeyintercepts_invalid_keys-rwm_03)
   - [RWM_Check_Create_Display_Valid_Params (RWM_04)](#rwm_check_create_display_valid_params-rwm_04)
   - [RWM_CreateDisplay_Empty_DisplayParams (RWM_05)](#rwm_createdisplay_empty_displayparams-rwm_05)
   - [RWM_Create_Display_Invalid_Params (RWM_06)](#rwm_create_display_invalid_params-rwm_06)
   - [RWM_Check_Enable_Inactivity_Reporting (RWM_07)](#rwm_check_enable_inactivity_reporting-rwm_07)
   - [RWM_Check_Disable_Inactivity_Reporting (RWM_08)](#rwm_check_disable_inactivity_reporting-rwm_08)
   - [RWM_Check_Enable_Inactivity_Reporting_Invalid_Value (RWM_09)](#rwm_check_enable_inactivity_reporting_invalid_value-rwm_09)
   - [RWM_Check_GenerateKey_Valid_Key (RWM_10)](#rwm_check_generatekey_valid_key-rwm_10)
   - [RWM_GenerateKey_Invalid_KeyCode (RWM_11)](#rwm_generatekey_invalid_keycode-rwm_11)
   - [RWM_GenerateKey_No_Params (RWM_12)](#rwm_generatekey_no_params-rwm_12)
   - [RWM_Check_Successful_Retrieval_Active_Application_IDs (RWM_13)](#rwm_check_successful_retrieval_active_application_ids-rwm_13)
   - [RWM_RemoveKeyIntercept_Valid_Params (RWM_14)](#rwm_removekeyintercept_valid_params-rwm_14)
   - [RWM_RemoveKeyIntercept_Invalid_Params (RWM_15)](#rwm_removekeyintercept_invalid_params-rwm_15)
   - [RWM_RemoveKeyIntercept_Empty_Params (RWM_16)](#rwm_removekeyintercept_empty_params-rwm_16)
   - [RWM_Check_Reset_Inactivity_Time (RWM_17)](#rwm_check_reset_inactivity_time-rwm_17)
   - [RWM_Check_SetInactivityInterval_Valid_Positive_Value (RWM_18)](#rwm_check_setinactivityinterval_valid_positive_value-rwm_18)
   - [RWM_SetInactivityInterval_NegativeValue (RWM_19)](#rwm_setinactivityinterval_negativevalue-rwm_19)
   - [RWM_Check_SetFocus_Valid_Client (RWM_20)](#rwm_check_setfocus_valid_client-rwm_20)
   - [RWM_SetFocus_Invalid_Client (RWM_21)](#rwm_setfocus_invalid_client-rwm_21)
   - [RWM_SetFocus_Empty_Client (RWM_22)](#rwm_setfocus_empty_client-rwm_22)
   - [RWM_SetVisible_Valid_Client_True (RWM_23)](#rwm_setvisible_valid_client_true-rwm_23)
   - [RWM_SetVisible_Valid_Client_False (RWM_24)](#rwm_setvisible_valid_client_false-rwm_24)
   - [RWM_SetVisible_Invalid_Client (RWM_25)](#rwm_setvisible_invalid_client-rwm_25)
   - [RWM_RenderReady_Valid_ClientId (RWM_26)](#rwm_renderready_valid_clientid-rwm_26)
   - [RWM_Check_RenderReady_Invalid_ClientId (RWM_27)](#rwm_check_renderready_invalid_clientid-rwm_27)
   - [RWM_Check_RenderReady_Empty_ClientId (RWM_28)](#rwm_check_renderready_empty_clientid-rwm_28)
   - [RWM_EnableDisplayRender_Valid_ClientId_Enable_True (RWM_29)](#rwm_enabledisplayrender_valid_clientid_enable_true-rwm_29)
   - [RWM_Check_EnableDisplayRender_Valid_ClientId_Enable_False (RWM_30)](#rwm_check_enabledisplayrender_valid_clientid_enable_false-rwm_30)
   - [RWM_EnableDisplayRender_Invalid_ClientId (RWM_31)](#rwm_enabledisplayrender_invalid_clientid-rwm_31)
   - [RWM_Check_SetZOrder_Valid_ClientId_ZOrder (RWM_32)](#rwm_check_setzorder_valid_clientid_zorder-rwm_32)
   - [RWM_SetZOrder_Invalid_ClientId (RWM_33)](#rwm_setzorder_invalid_clientid-rwm_33)
   - [RWM_SetZOrder_ValidClientId_InvalidZOrder (RWM_34)](#rwm_setzorder_validclientid_invalidzorder-rwm_34)
   - [RWM_Check_GetZOrder_Valid_ClientId (RWM_35)](#rwm_check_getzorder_valid_clientid-rwm_35)
   - [RWM_Check_GetZOrder_Invalid_ClientId (RWM_36)](#rwm_check_getzorder_invalid_clientid-rwm_36)
   - [RWM_GetZOrder_Empty_ClientId (RWM_37)](#rwm_getzorder_empty_clientid-rwm_37)
   - [RWM_Check_On_User_Inactivity_Event (RWM_L2_01)](#rwm_check_on_user_inactivity_event-rwm_l2_01)
   - [RWM_Check_User_Active (RWM_L2_02)](#rwm_check_user_active-rwm_l2_02)
   - [RWM_Reset_Inactivity_Interval (RWM_L2_03)](#rwm_reset_inactivity_interval-rwm_l2_03)
   - [RWM_Check_On_User_Inactivity_Event_Disabled_Reporting (RWM_L2_04)](#rwm_check_on_user_inactivity_event_disabled_reporting-rwm_l2_04)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **RDKWindowManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.RDKWindowManager` (version 1)

**API Coverage**

- **State / Query APIs**: `getApps`, `getZOrder`
- **Configuration APIs**: `addKeyIntercepts`, `enableDisplayRender`, `enableInactivityReporting`, `removeKeyIntercept`, `resetInactivityTime`, `setFocus`, `setInactivityInterval`, `setVisible`, `setZOrder`
- **Events**: `onUserInactivity`
- **Other APIs**: `createDisplay`, `generateKey`, `renderReady`

### APIs Under Test

| API | Description |
|-----|-------------|
| `addKeyIntercepts` | Adds the list of key intercepts |
| `createDisplay` | Creates a new display |
| `enableDisplayRender` | Enables or disables display rendering for a specific app instance |
| `enableInactivityReporting` | Enables or disables inactivity reporting |
| `generateKey` | Generates a key for the window manager |
| `getApps` | Retrieves the list of available applications |
| `getZOrder` | Retrieves the Z-order of a specific application instance |
| `removeKeyIntercept` | Removes a key intercept |
| `renderReady` | Indicates that the rendering is ready for the specified app instance |
| `resetInactivityTime` | Resets the inactivity time counter |
| `setFocus` | Set focus to a specific application instance |
| `setInactivityInterval` | Sets the inactivity interval |
| `setVisible` | Sets the visibility of a specific application instance |
| `setZOrder` | Sets the z-order of the specified app |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onUserInactivity` | Triggered when the user inactivity timer reaches the set interval |

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

### Pre-condition 5: Activate_RDKWindowManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.RDKWindowManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RDKWindowManager"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

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

### Pre-condition 8: Register_And_Listen_Events

- Register and listen to event `Event_On_User_Inactivity` on `RDKWindowManager` plugin

---

## Test Cases

<a id="rwm_check_add_key_intercepts-rwm_01"></a>
### RWM_Check_Add_Key_Intercepts (RWM_01)

**Objective:** Pass a valid list of key intercepts and ensure the method successfully adds the intercepts without errors

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Add Key Intercepts | Invoke `addKeyIntercepts` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `13`, `modifiers`: `"shift"`, `focusOnly`: `true`, `propagate`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_addkeyintercepts_empty_modifiers-rwm_02"></a>
### RWM_AddKeyIntercepts_Empty_Modifiers (RWM_02)

**Objective:** Pass an empty modifiers parameter to the addKeyIntercepts method and check that the API processes the request successfully without errors, handling the empty input gracefully

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Add Key Intercepts Empty Modifiers | Invoke `addKeyIntercepts` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `13`, `modifiers`: `""`, `focusOnly`: `true`, `propagate`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_addkeyintercepts_invalid_keys-rwm_03"></a>
### RWM_Check_AddKeyIntercepts_Invalid_Keys (RWM_03)

**Objective:** Pass a list containing invalid key intercepts and ensure the method returns an appropriate error or handles the input correctly

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Add Key Intercepts Invalid | Invoke `addKeyIntercepts` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `0`, `modifiers`: `"INVALID_MODIFIERS"`, `focusOnly`: `true`, `propagate`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.addKeyIntercepts", "params": {"clientId": "<result_step_1>", "keyCode": 0, "modifiers": "INVALID_MODIFIERS", "focusOnly": true, "propagate": false}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_create_display_valid_params-rwm_04"></a>
### RWM_Check_Create_Display_Valid_Params (RWM_04)

**Objective:** Test the createDisplay method by passing valid displayParams containing all required fields and valid values. Ensure the display is created successfully without errors

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Create Display Valid Params | Invoke `createDisplay` on `org.rdk.RDKWindowManager` with `clientId`: `"testdisplay"`, `displayName`: `"testdisplay"`, `displayWidth`: `1920`, `displayHeight`: `1080`, `virtualWidth`: `1920`, `virtualHeight`: `1080`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "testdisplay", "displayName": "testdisplay", "displayWidth": 1920, "displayHeight": 1080, "virtualWidth": 1920, "virtualHeight": 1080}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_createdisplay_empty_displayparams-rwm_05"></a>
### RWM_CreateDisplay_Empty_DisplayParams (RWM_05)

**Objective:** Test the createDisplay method by passing an empty object or null as displayParams. Ensure the method handles the input gracefully and returns an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Create Display Empty Params | Invoke `createDisplay` on `org.rdk.RDKWindowManager` with `clientId`: `""`, `displayName`: `""`, `displayWidth`: `""`, `displayHeight`: `""`, `virtualWidth`: `""`, `virtualHeight`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "", "displayName": "", "displayWidth": "", "displayHeight": "", "virtualWidth": "", "virtualHeight": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_create_display_invalid_params-rwm_06"></a>
### RWM_Create_Display_Invalid_Params (RWM_06)

**Objective:** Test the createDisplay method by passing displayParams with invalid or malformed data

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Create Display Invalid Params | Invoke `createDisplay` on `org.rdk.RDKWindowManager` with `clientId`: `"INVALID_CLIENT"`, `displayName`: `"INVALID_DISPLAY"`, `displayWidth`: `0`, `displayHeight`: `0`, `virtualWidth`: `0`, `virtualHeight`: `0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.createDisplay", "params": {"clientId": "INVALID_CLIENT", "displayName": "INVALID_DISPLAY", "displayWidth": 0, "displayHeight": 0, "virtualWidth": 0, "virtualHeight": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_enable_inactivity_reporting-rwm_07"></a>
### RWM_Check_Enable_Inactivity_Reporting (RWM_07)

**Objective:** Test the API by passing enable parameter as true to ensure inactivity reporting is successfully enabled

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Enable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_disable_inactivity_reporting-rwm_08"></a>
### RWM_Check_Disable_Inactivity_Reporting (RWM_08)

**Objective:** Test the API by passing enable parameter as false to ensure inactivity reporting is successfully disabled

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_enable_inactivity_reporting_invalid_value-rwm_09"></a>
### RWM_Check_Enable_Inactivity_Reporting_Invalid_Value (RWM_09)

**Objective:** Test the API by passing an invalid value for enable to ensure the API handles invalid inputs gracefully and returns an appropriate error

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Enable Inactivity Reporting Invalid | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `"InvalidValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": "InvalidValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_generatekey_valid_key-rwm_10"></a>
### RWM_Check_GenerateKey_Valid_Key (RWM_10)

**Objective:** Verify the behavior of generateKey when called with valid key press and release. Ensure the method triggers the correct key without errors

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Generate Key Valid Events | Invoke `generateKey` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `13`, `modifiers`: `"shift"`, `delay`: `10.0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift", "delay": 10.0}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_generatekey_invalid_keycode-rwm_11"></a>
### RWM_GenerateKey_Invalid_KeyCode (RWM_11)

**Objective:** Test generateKey with invalid or unsupported key codes. Verify that the method handles the input gracefully and does not trigger any unintended behavior

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Generate Key Invalid | Invoke `generateKey` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `"INVALID_KEY"`, `modifiers`: `"shift"`, `delay`: `10`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_1>", "keyCode": "INVALID_KEY", "modifiers": "shift", "delay": 10}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_generatekey_no_params-rwm_12"></a>
### RWM_GenerateKey_No_Params (RWM_12)

**Objective:** Check the response of generateKey when no parameters are provided. Ensure the method either throws an appropriate error or handles the scenario as expected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Generate Key No Params | Invoke `generateKey` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_successful_retrieval_active_application_ids-rwm_13"></a>
### RWM_Check_Successful_Retrieval_Active_Application_IDs (RWM_13)

**Objective:** Verify the successful retrieval of active application IDs when there are multiple active applications

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Application IDs | Invoke `getApps` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getApps"}' http://127.0.0.1:9998/jsonrpc` | Apps returned successfully |

---

<a id="rwm_removekeyintercept_valid_params-rwm_14"></a>
### RWM_RemoveKeyIntercept_Valid_Params (RWM_14)

**Objective:** Pass a valid intercept parameter and ensure the key intercept is successfully removed

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Remove Key Intercept | Invoke `removeKeyIntercept` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `keyCode`: `13`, `modifiers`: `"shift"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "<result_step_1>", "keyCode": 13, "modifiers": "shift"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_removekeyintercept_invalid_params-rwm_15"></a>
### RWM_RemoveKeyIntercept_Invalid_Params (RWM_15)

**Objective:** Verify removeKeyIntercept with an invalid intercept value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Remove Key Intercept Invalid | Invoke `removeKeyIntercept` on `org.rdk.RDKWindowManager` with `clientId`: `"InvalidClient"`, `keyCode`: `"InvalidKeyCode"`, `modifiers`: `"InvalidModifiers"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "InvalidClient", "keyCode": "InvalidKeyCode", "modifiers": "InvalidModifiers"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_removekeyintercept_empty_params-rwm_16"></a>
### RWM_RemoveKeyIntercept_Empty_Params (RWM_16)

**Objective:** Pass a null or empty intercept parameter and ensure the API handles the input gracefully, returning an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Remove Key Intercept Empty | Invoke `removeKeyIntercept` on `org.rdk.RDKWindowManager` with `clientId`: `""`, `keyCode`: `""`, `modifiers`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.removeKeyIntercept", "params": {"clientId": "", "keyCode": "", "modifiers": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_reset_inactivity_time-rwm_17"></a>
### RWM_Check_Reset_Inactivity_Time (RWM_17)

**Objective:** Call the resetInactivityTime method and ensure it executes successfully, resetting the inactivity timer as expected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Inactivity Time | Invoke `resetInactivityTime` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_setinactivityinterval_valid_positive_value-rwm_18"></a>
### RWM_Check_SetInactivityInterval_Valid_Positive_Value (RWM_18)

**Objective:** Call the setInactivityInterval method with a valid positive integer value for the interval parameter. Ensure the method executes successfully and sets the inactivity interval as expected.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `5`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 5}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_setinactivityinterval_negativevalue-rwm_19"></a>
### RWM_SetInactivityInterval_NegativeValue (RWM_19)

**Objective:** Call the setInactivityInterval method with a negative integer value for the interval parameter and ensure it returns an appropriate error

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval Negative | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `-100`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": -100}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_setfocus_valid_client-rwm_20"></a>
### RWM_Check_SetFocus_Valid_Client (RWM_20)

**Objective:** Pass a valid client to the setFocus method and ensure the focus is successfully set to the specified application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Set Focus Valid Client | Invoke `setFocus` on `org.rdk.RDKWindowManager` with `client`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_setfocus_invalid_client-rwm_21"></a>
### RWM_SetFocus_Invalid_Client (RWM_21)

**Objective:** Pass an invalid or non-existent client to the setFocus method and ensure the method returns an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Focus Invalid Client | Invoke `setFocus` on `org.rdk.RDKWindowManager` with `client`: `"InvalidClient"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": "InvalidClient"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setfocus_empty_client-rwm_22"></a>
### RWM_SetFocus_Empty_Client (RWM_22)

**Objective:** Pass an empty string as the client to the setFocus method and ensure the method handles the input gracefully, returning an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Focus Empty Client | Invoke `setFocus` on `org.rdk.RDKWindowManager` with `client`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setFocus", "params": {"client": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setvisible_valid_client_true-rwm_23"></a>
### RWM_SetVisible_Valid_Client_True (RWM_23)

**Objective:** Test the setVisible method by passing a valid client and setting visible to true. Ensure the application becomes visible successfully

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Set Visible Valid Client True | Invoke `setVisible` on `org.rdk.RDKWindowManager` with `client`: `"<result_step_1>"`, `visible`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<result_step_1>", "visible": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_setvisible_valid_client_false-rwm_24"></a>
### RWM_SetVisible_Valid_Client_False (RWM_24)

**Objective:** Test the setVisible method by passing a valid client and setting visible to false. Ensure the application becomes hidden successfully

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Set Visible Valid Client False | Invoke `setVisible` on `org.rdk.RDKWindowManager` with `client`: `"<result_step_1>"`, `visible`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "<result_step_1>", "visible": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_setvisible_invalid_client-rwm_25"></a>
### RWM_SetVisible_Invalid_Client (RWM_25)

**Objective:** Test the setVisible method by passing an invalid client and setting visible to true. Ensure the method handles the invalid client gracefully and returns an appropriate error

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Visible Invalid Client | Invoke `setVisible` on `org.rdk.RDKWindowManager` with `client`: `"InvalidClient"`, `visible`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setVisible", "params": {"client": "InvalidClient", "visible": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_renderready_valid_clientid-rwm_26"></a>
### RWM_RenderReady_Valid_ClientId (RWM_26)

**Objective:** Call the renderReady method with a valid clientId of an application that has rendered its first frame. Ensure the method returns true indicating the application is ready

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Render Ready Valid ClientId | Invoke `renderReady` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_renderready_invalid_clientid-rwm_27"></a>
### RWM_Check_RenderReady_Invalid_ClientId (RWM_27)

**Objective:** Call the renderReady method with an invalid or non-existent clientId. Ensure the method returns false or an appropriate error response indicating the application is not ready

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Render Ready Invalid ClientId | Invoke `renderReady` on `org.rdk.RDKWindowManager` with `clientId`: `"InvalidClientId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": "InvalidClientId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_renderready_empty_clientid-rwm_28"></a>
### RWM_Check_RenderReady_Empty_ClientId (RWM_28)

**Objective:** Call the renderReady method with a null or empty string as the clientId. Ensure the method handles the input gracefully and returns an error or false indicating invalid input

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | RenderReady Empty ClientId | Invoke `renderReady` on `org.rdk.RDKWindowManager` with `clientId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.renderReady", "params": {"clientId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_enabledisplayrender_valid_clientid_enable_true-rwm_29"></a>
### RWM_EnableDisplayRender_Valid_ClientId_Enable_True (RWM_29)

**Objective:** Call the enableDisplayRender method with a valid clientId and set enable to true. Ensure the display rendering is successfully enabled for the specified application instance

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Enable Display Render | Invoke `enableDisplayRender` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "<result_step_1>", "enable": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_enabledisplayrender_valid_clientid_enable_false-rwm_30"></a>
### RWM_Check_EnableDisplayRender_Valid_ClientId_Enable_False (RWM_30)

**Objective:** Call the enableDisplayRender method with a valid clientId and set enable to false. Ensure the display rendering is successfully disabled for the specified application instance

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Disable Display Render | Invoke `enableDisplayRender` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "<result_step_1>", "enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_enabledisplayrender_invalid_clientid-rwm_31"></a>
### RWM_EnableDisplayRender_Invalid_ClientId (RWM_31)

**Objective:** Call the enableDisplayRender method with an invalid or non-existent clientId and set enable to true. Ensure the method returns an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Enable Display Render Invalid ClientId | Invoke `enableDisplayRender` on `org.rdk.RDKWindowManager` with `clientId`: `"InvalidClientId"`, `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableDisplayRender", "params": {"clientId": "InvalidClientId", "enable": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_setzorder_valid_clientid_zorder-rwm_32"></a>
### RWM_Check_SetZOrder_Valid_ClientId_ZOrder (RWM_32)

**Objective:** Test the setZOrder method by providing a valid clientId and a valid zOrder value. Ensure the method sets the z-order successfully without errors

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Set Z Order Valid Params | Invoke `setZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `zOrder`: `1`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "<result_step_1>", "zOrder": 1}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_setzorder_invalid_clientid-rwm_33"></a>
### RWM_SetZOrder_Invalid_ClientId (RWM_33)

**Objective:** Test the setZOrder method by providing an invalid clientId and a valid zOrder value. Ensure the method returns an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Z Order Invalid ClientId | Invoke `setZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `"InvalidClientId"`, `zOrder`: `1`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "InvalidClientId", "zOrder": 1}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_setzorder_validclientid_invalidzorder-rwm_34"></a>
### RWM_SetZOrder_ValidClientId_InvalidZOrder (RWM_34)

**Objective:** Test the setZOrder method by providing a valid clientId and an invalid zOrder value. Ensure the method returns an appropriate error or failure response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | Set Z Order Invalid ZOrder | Invoke `setZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`, `zOrder`: `"InvalidZOrderValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setZOrder", "params": {"clientId": "<result_step_1>", "zOrder": "InvalidZOrderValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_getzorder_valid_clientid-rwm_35"></a>
### RWM_Check_GetZOrder_Valid_ClientId (RWM_35)

**Objective:** Pass a valid clientId to the getZOrder method and ensure it returns the correct z-order value for the specified application

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 2 | GetZOrder Valid ClientId | Invoke `getZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API call should succeed and return a valid z-order reference |

---

<a id="rwm_check_getzorder_invalid_clientid-rwm_36"></a>
### RWM_Check_GetZOrder_Invalid_ClientId (RWM_36)

**Objective:** Pass an invalid or non-existent clientId to the getZOrder method and ensure it returns an appropriate error or null response

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Verify GetZOrder Invalid ClientId | Invoke `getZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `"InvalidClientId"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": "InvalidClientId"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_getzorder_empty_clientid-rwm_37"></a>
### RWM_GetZOrder_Empty_ClientId (RWM_37)

**Objective:** Verify getZOrder with a null or empty clientId

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetZOrder Empty ClientId | Invoke `getZOrder` on `org.rdk.RDKWindowManager` with `clientId`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.getZOrder", "params": {"clientId": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `ERROR_GENERAL` |

---

<a id="rwm_check_on_user_inactivity_event-rwm_l2_01"></a>
### RWM_Check_On_User_Inactivity_Event (RWM_L2_01)

**Objective:** Test the user inactivity reporting by enabling it, setting a short inactivity interval, and verifying that the OnUserInactivity event is triggered after the specified interval of user inactivity

**Pre-condition:**

#### Pre-condition 1: Reset_Enable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Inactivity Time | Invoke `resetInactivityTime` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Enable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `1`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check On UserInactivity Event | Listen for event `Event_On_User_Inactivity` | Event data validated successfully |

**Post-condition:**

#### Post-condition 1: Disable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_user_active-rwm_l2_02"></a>
### RWM_Check_User_Active (RWM_L2_02)

**Objective:** Check device returns to active mode after user input via generateKey when it was previously inactive

**Pre-condition:**

#### Pre-condition 1: Reset_Enable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Inactivity Time | Invoke `resetInactivityTime` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Enable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `1`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check On UserInactivity Event | Listen for event `Event_On_User_Inactivity` | Event data validated successfully |
| 3 | Get AppInstance Id | Invoke `getLoadedApps` on `org.rdk.AppManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.AppManager.1.getLoadedApps"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<PACKAGEMANAGER_APPLICATION_NAME> (APP_STATE_ACTIVE)` |
| 4 | Generate Key Valid Events | Invoke `generateKey` on `org.rdk.RDKWindowManager` with `clientId`: `"<result_step_3>"`, `keyCode`: `13`, `modifiers`: `"shift"`, `delay`: `3.0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"clientId": "<result_step_3>", "keyCode": 13, "modifiers": "shift", "delay": 3.0}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Post-condition:**

#### Post-condition 1: Disable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_reset_inactivity_interval-rwm_l2_03"></a>
### RWM_Reset_Inactivity_Interval (RWM_L2_03)

**Objective:** Test the resetInactivityTime method to ensure it resets the inactivity timer correctly

**Pre-condition:**

#### Pre-condition 1: Reset_Enable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Inactivity Time | Invoke `resetInactivityTime` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Enable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": true}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `2`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 2}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check On UserInactivity Event | Listen for event `Event_On_User_Inactivity` | Event data validated successfully |
| 3 | Reset Inactivity Time | Invoke `resetInactivityTime` on `org.rdk.RDKWindowManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.resetInactivityTime"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 4 | Check On UserInactivity Event | Listen for event `Event_On_User_Inactivity` | Event data validated successfully |

**Post-condition:**

#### Post-condition 1: Disable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

<a id="rwm_check_on_user_inactivity_event_disabled_reporting-rwm_l2_04"></a>
### RWM_Check_On_User_Inactivity_Event_Disabled_Reporting (RWM_L2_04)

**Objective:** Checks whether the user inactivity reporting event is triggered when inactivity reporting is disabled

**Pre-condition:**

#### Pre-condition 1: Disable_Inactivity_Reporting

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Disable Inactivity Reporting | Invoke `enableInactivityReporting` on `org.rdk.RDKWindowManager` with `enable`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.enableInactivityReporting", "params": {"enable": false}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Inactivity Interval | Invoke `setInactivityInterval` on `org.rdk.RDKWindowManager` with `interval`: `1`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.setInactivityInterval", "params": {"interval": 1}}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |
| 2 | Check On UserInactivity Event NoEvent | Listen for event `Event_On_User_Inactivity` | Event should not be triggered |

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