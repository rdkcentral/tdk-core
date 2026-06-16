## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Monitor_Reset_Statistics_NetworkManager (MN_01)](#monitor_reset_statistics_networkmanager-mn_01)
   - [Monitor_Get_Status_NetworkManager (MN_02)](#monitor_get_status_networkmanager-mn_02)
   - [Monitor_Restart_Limits_NetworkManager (MN_03)](#monitor_restart_limits_networkmanager-mn_03)
   - [Monitor_ActivateDeactivate_Event_Test (MN_04)](#monitor_activatedeactivate_event_test-mn_04)
   - [Monitor_ActivateDeactivate_All_Event_Test (MN_05)](#monitor_activatedeactivate_all_event_test-mn_05)
   - [Monitor_Verify_restartlimits_Info_Error (MN_06)](#monitor_verify_restartlimits_info_error-mn_06)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **Monitor** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `Monitor` (version 1)

**API Coverage**

- **Configuration APIs**: `resetstats`
- **Other APIs**: `restartlimits`, `status`

### APIs Under Test

| API | Description |
|-----|-------------|
| `resetstats` | Resets memory and process statistics for a single service watched by the Monitor |
| `restartlimits` | Sets new restart limits for a service |
| `status` | Provides access to the service statistics |

---

## Pre-conditions

### Pre-condition 1: Activate_Monitor_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_NetworkManager_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="monitor_reset_statistics_networkmanager-mn_01"></a>
### Monitor_Reset_Statistics_NetworkManager (MN_01)

**Objective:** Resets memory and process statistics for a single service

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Statistics | Invoke `resetstats` on `Monitor` with `callsign`: `"org.rdk.NetworkManager"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.resetstats", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Response contains `observable`: `"org.rdk.NetworkManager"`, `restartLimit` and `restartWindow` numeric values are present and `measurements` array is returned (each entry has `operational` boolean and `count` integer fields) |

---

<a id="monitor_get_status_networkmanager-mn_02"></a>
### Monitor_Get_Status_NetworkManager (MN_02)

**Objective:** Lists the service statistics

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Status | Invoke `status` on `Monitor` with plugin filter `org.rdk.NetworkManager`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Response contains `observable`: `"org.rdk.NetworkManager"`, `restartLimit` and `restartWindow` numeric values are present and `measurements` array is returned (each entry has `operational` boolean and `count` integer fields) |

---

<a id="monitor_restart_limits_networkmanager-mn_03"></a>
### Monitor_Restart_Limits_NetworkManager (MN_03)

**Objective:** Sets new restart limits for a service

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Restart Limits | Invoke `restartlimits` on `Monitor` with `callsign`: `"org.rdk.NetworkManager"`, `limit`: `3`, `window`: `60`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.restartlimits", "params": {"callsign": "org.rdk.NetworkManager", "limit": 3, "window": 60}}' http://127.0.0.1:9998/jsonrpc` | Restart limits set successfully for `org.rdk.NetworkManager` with `limit: 3` and `window: 60` seconds |

---

<a id="monitor_activatedeactivate_event_test-mn_04"></a>
### Monitor_ActivateDeactivate_Event_Test (MN_04)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Monitor Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `monitor`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Monitor Plugin | Invoke `activate` on `Controller` with `callsign`: `"Monitor"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `monitor`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="monitor_activatedeactivate_all_event_test-mn_05"></a>
### Monitor_ActivateDeactivate_All_Event_Test (MN_05)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Monitor Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `monitor`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Monitor Plugin | Invoke `activate` on `Controller` with `callsign`: `"Monitor"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `monitor`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="monitor_verify_restartlimits_info_error-mn_06"></a>
### Monitor_Verify_restartlimits_Info_Error (MN_06)

**Objective:** Verify that the restartlimits method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Monitor Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `monitor`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check Monitor restartlimits API Response | Invoke `restartlimits` on `Monitor`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.restartlimits"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate Monitor Plugin | Invoke `activate` on `Controller` with `callsign`: `"Monitor"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `monitor`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M82 |