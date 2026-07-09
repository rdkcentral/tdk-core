## TestScript Name
RDKV_CERT_AVS_Warehouse

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [WareHouse_Light_Reset](#warehouse_light_reset)
   - [WareHouse_Check_Is_Clean](#warehouse_check_is_clean)
   - [WareHouse_Reset_Device](#warehouse_reset_device)
   - [WareHouse_Internal_Reset](#warehouse_internal_reset)
   - [WareHouse_Check_Event_On_Device_Reset](#warehouse_check_event_on_device_reset)
   - [Warehouse_ActivateDeactivate_Event_Test](#warehouse_activatedeactivate_event_test)
   - [Warehouse_ActivateDeactivate_All_Event_Test](#warehouse_activatedeactivate_all_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **Warehouse** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.Warehouse` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the resetDone event | Register a WebSocket event listener for `resetDone` to receive `resetDone` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.register", "params": {"event": "resetDone", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure NA Tests | `WAREHOUSE_NA_TESTS` must be set to the warehouse test names to skip when not applicable on the DUT | The `WAREHOUSE_NA_TESTS` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="warehouse_light_reset"></a>
### TestCase Name
WareHouse_Light_Reset

### TestCase ID
WH_01

### TestCase Objective
Performs a light reset of application data

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Light Reset | Invoke lightReset on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.lightReset"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the Light Reset completes successfully  |

---

<a id="warehouse_check_is_clean"></a>
### TestCase Name
WareHouse_Check_Is_Clean

### TestCase ID
WH_02

### TestCase Objective
Checks locations where customer data may be stored

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Is Clean | Invoke isClean on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.isClean"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the `clean` flag correctly reflects the status — `true` with no files listed, or `false` with one or more files present  |

---

<a id="warehouse_reset_device"></a>
### TestCase Name
WareHouse_Reset_Device

### TestCase ID
WH_03

### TestCase Objective
Resets the STB to the warehouse state

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset Device | Invoke resetDevice on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the device is reset to the warehouse state successfully  |
| 2 | Check Device Active Status | *(External function call no JSON-RPC command required)*<br>Checks whether the device has come back online after the reset. Once online, plugin pre-requisites are re-initialized internally | Verify that the device comes back online within 120 seconds and plugin pre-requisites are restored successfully  |

---

<a id="warehouse_internal_reset"></a>
### TestCase Name
WareHouse_Internal_Reset

### TestCase ID
WH_04

### TestCase Objective
Invokes the internal reset script, which reboots the Warehouse service

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Internal Reset | Invoke internalReset on org.rdk.Warehouse with passPhrase: "FOR TEST PURPOSES ONLY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.internalReset", "params": {"passPhrase": "FOR TEST PURPOSES ONLY"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the Internal Reset completes successfully, causing the WarehouseService to reboot  |
| 2 | Check Device Active Status | *(External function call no JSON-RPC command required)*<br>Checks whether the device has come back online after the reset. Once online, plugin pre-requisites are re-initialized internally | Verify that the device comes back online within 120 seconds and plugin pre-requisites are restored successfully  |

---

<a id="warehouse_check_event_on_device_reset"></a>
### TestCase Name
WareHouse_Check_Event_On_Device_Reset

### TestCase ID
WH_05

### TestCase Objective
Checks if event is received on device reset

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reset Device | Invoke resetDevice on org.rdk.Warehouse with resetType: "USERFACTORY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice", "params": {"resetType": "USERFACTORY"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the device is reset with `USERFACTORY` reset type successfully  |
| 2 | Check Event Reset Done | *(Event registration done in Pre-condition 2)*<br>Listen for resetDone event (Event_Reset_Done) on org.rdk.Warehouse (wait 5s) | Verify that the API returns `True` and the `resetDone` event is received, confirming the warehouse reset operation completed successfully  |

### TestCase Post-condition

#### TestCase Post-condition 1: Set_Back_Plugin_Pre-requisite

> **Note:** This post-condition re-initializes the plugin pre-requisites after the device resets. It is handled internally (external function call no JSON-RPC command required)

---

<a id="warehouse_activatedeactivate_event_test"></a>
### TestCase Name
Warehouse_ActivateDeactivate_Event_Test

### TestCase ID
WH_06

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Warehouse Plugin | Invoke deactivate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.warehouse` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate Warehouse Plugin | Invoke activate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `org.rdk.warehouse` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="warehouse_activatedeactivate_all_event_test"></a>
### TestCase Name
Warehouse_ActivateDeactivate_All_Event_Test

### TestCase ID
WH_07

### TestCase Objective
Validates all event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate Warehouse Plugin | Invoke deactivate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check All Event | Listen for Event_Controller_All event (wait 2s) | Verify that the `all` event is received for callsign `org.rdk.warehouse` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate Warehouse Plugin | Invoke activate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check All Event | Listen for Event_Controller_All event (wait 2s) | Verify that the `all` event is received for callsign `org.rdk.warehouse` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the resetDone event | Unregister the WebSocket event listener for `resetDone` to stop receiving `resetDone` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.unregister", "params": {"event": "resetDone", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop receiving `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 15 mins

**Priority** : Medium

**Release Version** : M82

<div align="right"><a href="#testscript-name">Go to Top</a></div>
