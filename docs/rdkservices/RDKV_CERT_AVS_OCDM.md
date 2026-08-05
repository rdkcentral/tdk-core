## TestScript Name
RDKV_CERT_AVS_OCDM

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [OCDM_Get_All_DRM_Info](#ocdm_get_all_drm_info)
   - [OCDM_ActivateDeactivate_Event_Test](#ocdm_activatedeactivate_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **OCDM** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `OCDM` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure supported DRM systems | `OCDM_SUPPORTED_DRM_SYSTEMS` must be configured as required for the test setup | The `OCDM_SUPPORTED_DRM_SYSTEMS` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="ocdm_get_all_drm_info"></a>
### TestCase Name
OCDM_Get_All_DRM_Info

### TestCase ID
OCDM_01

### TestCase Objective
Gets supported DRMs & DRM key systems

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get supported DRM systems | Invoke drms on OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "OCDM.1.drms"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported DRM systems match the expected value `<OCDM_SUPPORTED_DRM_SYSTEMS>` from the device config file  |
| 2 | Get DRM key systems | Invoke keysystems on OCDM for <result_step_1><br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "OCDM.1.keysystems@<result_step_1>"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` drm key matches value from step 1  |

---

<a id="ocdm_activatedeactivate_event_test"></a>
### TestCase Name
OCDM_ActivateDeactivate_Event_Test

### TestCase ID
OCDM_02

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate OCDM plugin | Invoke deactivate on Controller with callsign: "OCDM"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `ocdm` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate OCDM plugin | Invoke activate on Controller with callsign: "OCDM"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `ocdm` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for OCDM<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
