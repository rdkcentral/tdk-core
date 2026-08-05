## TestScript Name
RDKV_CERT_AVS_Monitor

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [Monitor_Reset_Statistics_NetworkManager](#monitor_reset_statistics_networkmanager)
   - [Monitor_Get_Status_NetworkManager](#monitor_get_status_networkmanager)
   - [Monitor_Restart_Limits_NetworkManager](#monitor_restart_limits_networkmanager)
   - [Monitor_ActivateDeactivate_Event_Test](#monitor_activatedeactivate_event_test)
   - [Monitor_ActivateDeactivate_All_Event_Test](#monitor_activatedeactivate_all_event_test)
   - [Monitor_Verify_restartlimits_Info_Error](#monitor_verify_restartlimits_info_error)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **Monitor** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `Monitor` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Monitor_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_NetworkManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of NetworkManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate NetworkManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of NetworkManager plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="monitor_reset_statistics_networkmanager"></a>
### TestCase Name
Monitor_Reset_Statistics_NetworkManager

### TestCase ID
MN_01

### TestCase Objective
Resets memory and process statistics for a single service

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset plugin monitoring statistics | Invoke resetstats on Monitor with callsign: "org.rdk.NetworkManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.resetstats", "params": {"callsign": "org.rdk.NetworkManager"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains `observable`: `"org.rdk.NetworkManager"` with `restartLimit` and `restartWindow` numeric values present  |

---

<a id="monitor_get_status_networkmanager"></a>
### TestCase Name
Monitor_Get_Status_NetworkManager

### TestCase ID
MN_02

### TestCase Objective
Lists the service statistics

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get plugin monitoring status | Invoke status on Monitor for org.rdk.NetworkManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.status@org.rdk.NetworkManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains `observable`: `"org.rdk.NetworkManager"` with `restartLimit` and `restartWindow` numeric values present  |

---

<a id="monitor_restart_limits_networkmanager"></a>
### TestCase Name
Monitor_Restart_Limits_NetworkManager

### TestCase ID
MN_03

### TestCase Objective
Sets new restart limits for a service

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set restart limits for monitored plugin | Invoke restartlimits on Monitor with callsign: "org.rdk.NetworkManager", limit: 3, window: 60<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.restartlimits", "params": {"callsign": "org.rdk.NetworkManager", "limit": 3, "window": 60}}' http://127.0.0.1:9998/jsonrpc` | Confirm that restart limits are set successfully for `org.rdk.NetworkManager` with `limit: 3` and `window: 60` seconds |

---

<a id="monitor_activatedeactivate_event_test"></a>
### TestCase Name
Monitor_ActivateDeactivate_Event_Test

### TestCase ID
MN_04

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate monitor plugin | Invoke deactivate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `monitor` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate monitor plugin | Invoke activate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `monitor` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="monitor_activatedeactivate_all_event_test"></a>
### TestCase Name
Monitor_ActivateDeactivate_All_Event_Test

### TestCase ID
MN_05

### TestCase Objective
Validates all event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate monitor plugin | Invoke deactivate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check all event | Listen for Event_Controller_All event and wait up to 2 second(s) | Verify that the `all` event is received for callsign `monitor` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate monitor plugin | Invoke activate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check all event | Listen for Event_Controller_All event and wait up to 2 second(s) | Verify that the `all` event is received for callsign `monitor` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="monitor_verify_restartlimits_info_error"></a>
### TestCase Name
Monitor_Verify_restartlimits_Info_Error

### TestCase ID
MN_06

### TestCase Objective
Verify that the restartlimits method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate monitor plugin | Invoke deactivate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `monitor` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Check monitor restartlimits API response | Invoke restartlimits on Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Monitor.1.restartlimits"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate monitor plugin | Invoke activate on Controller with callsign: "Monitor"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `monitor` with state `"activated"` |
| 7 | Check plugin active status | Invoke status on Controller for Monitor<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

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

**Release Version** : M82

<div align="right"><a href="#testscript-name">Go to Top</a></div>
