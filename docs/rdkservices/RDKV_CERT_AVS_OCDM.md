## TestScript Name
RDKV_CERT_AVS_OCDM

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Plugin Pre-conditions](#plugin-pre-conditions)
4. [Test Cases](#test-cases)
   - [OCDM_Get_All_DRM_Info](#ocdm_get_all_drm_info)
   - [OCDM_ActivateDeactivate_Event_Test](#ocdm_activatedeactivate_event_test)
5. [Plugin Post-conditions](#plugin-post-conditions)
6. [Test Attributes](#test-attributes)

## Objective

The **OCDM** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `OCDM` (version 1)

## APIs Under Test

| API | Description |
| --- | --- |
| `drms` | Retrieves supported DRM systems |
| `keysystems` | Provides access to the DRM key systems |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="ocdm_get_all_drm_info"></a>
### TestCase Name
OCDM_Get_All_DRM_Info

### TestCase ID
OCDM_01

### TestCase Objective
Gets supported DRMs & DRM key systems

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported DRM Systems | Invoke drms on OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "OCDM.1.drms"}' http://127.0.0.1:9998/jsonrpc` | Expected `<OCDM_SUPPORTED_DRM_SYSTEMS>` |
| 2 | Get DRM Key Systems | Invoke keysystems on OCDM for <result_step_1><br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "OCDM.1.keysystems@<result_step_1>"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` drm key matches value from step 1 |

---

<a id="ocdm_activatedeactivate_event_test"></a>
### TestCase Name
OCDM_ActivateDeactivate_Event_Test

### TestCase ID
OCDM_02

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate OCDM Plugin | Invoke deactivate on Controller with callsign: "OCDM"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `ocdm` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate OCDM Plugin | Invoke activate on Controller with callsign: "OCDM"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `ocdm` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M81 |
