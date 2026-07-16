## TestScript Name
RDKV_CERT_AVS_User_Preferences

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [UserPreferences_SetAndGet_UI_Language](#userpreferences_setandget_ui_language)
   - [UserPreferences_ActivateDeactivate_Event_Test](#userpreferences_activatedeactivate_event_test)
   - [UserPreferences_ActivateDeactivate_All_Event_Test](#userpreferences_activatedeactivate_all_event_test)
   - [UserPreferences_Verify_Get_UI_Language_Error](#userpreferences_verify_get_ui_language_error)
   - [UserPreferences_Verify_SetUILanguage_without_Params](#userpreferences_verify_setuilanguage_without_params)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **UserPreferences** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.UserPreferences` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="userpreferences_setandget_ui_language"></a>
### TestCase Name
UserPreferences_SetAndGet_UI_Language

### TestCase ID
UP_01

### TestCase Objective
Set and get user preferred UI language

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set UI language | Invoke setUILanguage on org.rdk.UserPreferences with ui_language: "US_en"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.setUILanguage", "params": {"ui_language": "US_en"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the UI language is set successfully |
| 2 | Get UI language | Invoke getUILanguage on org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.getUILanguage"}' http://127.0.0.1:9998/jsonrpc` | Verify that the UI language is set to `US_en` as expected  |

---

<a id="userpreferences_activatedeactivate_event_test"></a>
### TestCase Name
UserPreferences_ActivateDeactivate_Event_Test

### TestCase ID
UP_02

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate UserPreferences plugin | Invoke deactivate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate org.rdk.UserPreferences plugin | Invoke activate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="userpreferences_activatedeactivate_all_event_test"></a>
### TestCase Name
UserPreferences_ActivateDeactivate_All_Event_Test

### TestCase ID
UP_03

### TestCase Objective
Validates all event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate UserPreferences plugin | Invoke deactivate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check all event | Listen for event Event_Controller_All | Verify that event data is validated successfully |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate UserPreferences plugin | Invoke activate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check all event | Listen for event Event_Controller_All | Verify that event data is validated successfully |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="userpreferences_verify_get_ui_language_error"></a>
### TestCase Name
UserPreferences_Verify_Get_UI_Language_Error

### TestCase ID
UP_04

### TestCase Objective
Verify that the getUiLanguage method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of UserPreferences plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate UserPreferences plugin | Invoke deactivate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Check UserPreferences get UI language API response | Invoke getUILanguage on org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.getUILanguage"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API returns the expected error: `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.`  |
| 5 | Activate UserPreferences plugin | Invoke activate on Controller with callsign: "org.rdk.UserPreferences"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check state change event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 7 | Check plugin active status | Invoke status on Controller for org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="userpreferences_verify_setuilanguage_without_params"></a>
### TestCase Name
UserPreferences_Verify_SetUILanguage_without_Params

### TestCase ID
UP_05

### TestCase Objective
Verify that the setUILanguage API returns an error when UI language parameter is not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set UI language | Invoke setUILanguage on org.rdk.UserPreferences<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.setUILanguage"}' http://127.0.0.1:9998/jsonrpc` | API returns error response with `"success": false` (missing `ui_language` parameter) |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop receiving `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
