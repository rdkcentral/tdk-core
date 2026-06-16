## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [UserPreferences_SetAndGet_UI_Language (UP_01)](#userpreferences_setandget_ui_language-up_01)
   - [UserPreferences_ActivateDeactivate_Event_Test (UP_02)](#userpreferences_activatedeactivate_event_test-up_02)
   - [UserPreferences_ActivateDeactivate_All_Event_Test (UP_03)](#userpreferences_activatedeactivate_all_event_test-up_03)
   - [UserPreferences_Verify_Get_UI_Language_Error (UP_04)](#userpreferences_verify_get_ui_language_error-up_04)
   - [UserPreferences_Verify_SetUILanguage_without_Params (UP_05)](#userpreferences_verify_setuilanguage_without_params-up_05)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **UserPreferences** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.UserPreferences` (version 1)

**API Coverage**

- **State / Query APIs**: `getUILanguage`
- **Configuration APIs**: `setUILanguage`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getUILanguage` | Gets the user preferred UI language |
| `setUILanguage` | Sets the user preferred UI language |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="userpreferences_setandget_ui_language-up_01"></a>
### UserPreferences_SetAndGet_UI_Language (UP_01)

**Objective:** Set and get user preferred UI language

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set UI Language | Invoke `setUILanguage` on `org.rdk.UserPreferences` with `ui_language`: `"US_en"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.setUILanguage", "params": {"ui_language": "US_en"}}' http://127.0.0.1:9998/jsonrpc` | UI Language set successfully |
| 2 | Get UI Language | Invoke `getUILanguage` on `org.rdk.UserPreferences`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.getUILanguage"}' http://127.0.0.1:9998/jsonrpc` | Expected: `US_en` |

---

<a id="userpreferences_activatedeactivate_event_test-up_02"></a>
### UserPreferences_ActivateDeactivate_Event_Test (UP_02)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate UserPreferences Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate org.rdk.UserPreferences Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="userpreferences_activatedeactivate_all_event_test-up_03"></a>
### UserPreferences_ActivateDeactivate_All_Event_Test (UP_03)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate UserPreferences Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for event `Event_Controller_All` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate UserPreferences Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for event `Event_Controller_All` | Event data validated successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="userpreferences_verify_get_ui_language_error-up_04"></a>
### UserPreferences_Verify_Get_UI_Language_Error (UP_04)

**Objective:** Verify that the getUiLanguage method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate UserPreferences Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check UserPreferences Get UI Language API Response | Invoke `getUILanguage` on `org.rdk.UserPreferences`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.getUILanguage"}' http://127.0.0.1:9998/jsonrpc` | Expected error`Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate UserPreferences Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.UserPreferences"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.UserPreferences"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.UserPreferences"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="userpreferences_verify_setuilanguage_without_params-up_05"></a>
### UserPreferences_Verify_SetUILanguage_without_Params (UP_05)

**Objective:** Verify that the setUILanguage API returns an error when UI language parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set UI Language | Invoke `setUILanguage` on `org.rdk.UserPreferences`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.UserPreferences.1.setUILanguage"}' http://127.0.0.1:9998/jsonrpc` | API returns error response with `"success": false` (missing `ui_language` parameter) |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M81 |