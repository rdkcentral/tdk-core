## TestScript Name
RDKV_CERT_AVS_Warehouse

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
   - [WareHouse_Get_STB_Device_Info](#warehouse_get_stb_device_info)
   - [WareHouse_Set_Front_Panel_State_None](#warehouse_set_front_panel_state_none)
   - [WareHouse_Set_Front_Panel_State_Download_In_Progress](#warehouse_set_front_panel_state_download_in_progress)
   - [WareHouse_Set_Front_Panel_State_Download_Failed](#warehouse_set_front_panel_state_download_failed)
   - [WareHouse_Set_Front_Panel_State_Download_Invalid](#warehouse_set_front_panel_state_download_invalid)
   - [WareHouse_Light_Reset](#warehouse_light_reset)
   - [WareHouse_Check_Is_Clean](#warehouse_check_is_clean)
   - [WareHouse_Reset_Device](#warehouse_reset_device)
   - [WareHouse_Internal_Reset](#warehouse_internal_reset)
   - [WareHouse_Check_Event_On_Device_Reset](#warehouse_check_event_on_device_reset)
   - [Warehouse_ActivateDeactivate_Event_Test](#warehouse_activatedeactivate_event_test)
   - [WareHouse_Set_Front_Panel_State_EmptyValue](#warehouse_set_front_panel_state_emptyvalue)
   - [Warehouse_ActivateDeactivate_All_Event_Test](#warehouse_activatedeactivate_all_event_test)
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **Warehouse** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.Warehouse` (version 1)

## APIs Under Test

| API | Description |
|-----|-------------|
| `getDeviceInfo` | Provides STB device information |
| `internalReset` | Invokes the internal reset script, which reboots the WarehouseService |
| `isClean` | Checks locations where customer data may be stored |
| `lightReset` | Performs light reset |
| `resetDevice` | Resets the STB to the warehouse state |
| `setFrontPanelState` | Sets the discoverable status of the device |

## Events Under Test

| Event | Description |
|-------|-------------|
| `resetDone` | Notifies about the status of the warehouse reset operation |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Reset_Done` on `Warehouse` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

## Test Cases

<a id="warehouse_get_stb_device_info"></a>
### TestCase Name
WareHouse_Get_STB_Device_Info

### TestCase ID
WH_01

### TestCase Objective
Gets all STB device info

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get STB DeviceInfo | Invoke getDeviceInfo on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.getDeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that STB device info is returned successfully with all device details (`success` : `true`) |

---

<a id="warehouse_set_front_panel_state_none"></a>
### TestCase Name
WareHouse_Set_Front_Panel_State_None

### TestCase ID
WH_02

### TestCase Objective
Sets the front panel state to None

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke setFrontPanelState on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": -1}}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Front Panel State set to None successfully |

---

<a id="warehouse_set_front_panel_state_download_in_progress"></a>
### TestCase Name
WareHouse_Set_Front_Panel_State_Download_In_Progress

### TestCase ID
WH_03

### TestCase Objective
Sets the front panel state to DOWNLOAD IN PROGRESS

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke setFrontPanelState on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 1}}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Front Panel State set to Download In Progress successfully |

---

<a id="warehouse_set_front_panel_state_download_failed"></a>
### TestCase Name
WareHouse_Set_Front_Panel_State_Download_Failed

### TestCase ID
WH_04

### TestCase Objective
Sets the front panel state to DOWNLOAD FAILED

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke setFrontPanelState on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 3}}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Front Panel State set to Download Failed successfully |

---

<a id="warehouse_set_front_panel_state_download_invalid"></a>
### TestCase Name
WareHouse_Set_Front_Panel_State_Download_Invalid

### TestCase ID
WH_05

### TestCase Objective
Sets the front panel state to invalid value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke setFrontPanelState on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 2}}' http://127.0.0.1:9998/jsonrpc` | API returns error `success: false`  |

---

<a id="warehouse_light_reset"></a>
### TestCase Name
WareHouse_Light_Reset

### TestCase ID
WH_06

### TestCase Objective
Performs a light reset of application data

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Light Reset | Invoke lightReset on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.lightReset"}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Light Reset completed successfully |

---

<a id="warehouse_check_is_clean"></a>
### TestCase Name
WareHouse_Check_Is_Clean

### TestCase ID
WH_07

### TestCase Objective
Checks locations where customer data may be stored

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Is Clean | Invoke isClean on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.isClean"}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Clean status returned with `clean` boolean field and any `dirty` locations listed |

---

<a id="warehouse_reset_device"></a>
### TestCase Name
WareHouse_Reset_Device

### TestCase ID
WH_08

### TestCase Objective
Resets the STB to the warehouse state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Device | Invoke resetDevice on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice"}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Device reset to warehouse state successfully |

---

<a id="warehouse_internal_reset"></a>
### TestCase Name
WareHouse_Internal_Reset

### TestCase ID
WH_09

### TestCase Objective
Resets the STB to the warehouse state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Internal Reset | Invoke internalReset on org.rdk.Warehouse with passPhrase: "FOR TEST PURPOSES ONLY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.internalReset", "params": {"passPhrase": "FOR TEST PURPOSES ONLY"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Internal Reset completed successfully; WarehouseService rebooted |

---

<a id="warehouse_check_event_on_device_reset"></a>
### TestCase Name
WareHouse_Check_Event_On_Device_Reset

### TestCase ID
WH_10

### TestCase Objective
Checks if event is received on device reset

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Device | Invoke resetDevice on org.rdk.Warehouse with resetType: "USERFACTORY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice", "params": {"resetType": "USERFACTORY"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success` : `true` Device reset with `USERFACTORY` reset type successfully |
| 2 | Check Event Reset Done | *(Event registration done in Pre-condition 2)*<br>Listen for resetDone event (Event_Reset_Done) on org.rdk.Warehouse (wait 5s) | Expected `True` and `resetDone` event received confirming warehouse reset operation completed |

### TestCase Post-condition

#### TestCase Post-condition 1: Set_Back_Plugin_Pre-requisite

> **Note:** This post-condition re-initializes the plugin pre-requisites after the device resets. It is handled internally (external function call no JSON-RPC command required)

---

<a id="warehouse_activatedeactivate_event_test"></a>
### TestCase Name
Warehouse_ActivateDeactivate_Event_Test

### TestCase ID
WH_11

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Warehouse Plugin | Invoke deactivate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | `statechange` event received; callsign = `org.rdk.warehouse`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Warehouse Plugin | Invoke activate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait 2s) | `statechange` event received; callsign = `org.rdk.warehouse`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="warehouse_set_front_panel_state_emptyvalue"></a>
### TestCase Name
WareHouse_Set_Front_Panel_State_EmptyValue

### TestCase ID
WH_12

### TestCase Objective
Sets the front panel state to EmptyValue

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State EmptyValue | Invoke setFrontPanelState on org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `incorrect state` |

---

<a id="warehouse_activatedeactivate_all_event_test"></a>
### TestCase Name
Warehouse_ActivateDeactivate_All_Event_Test

### TestCase ID
WH_13

### TestCase Objective
Validates all event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of Warehouse Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Warehouse Plugin | Invoke deactivate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check All Event | Listen for Event_Controller_All event (wait 2s) | Controller `all` event received; callsign = `org.rdk.warehouse`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Warehouse Plugin | Invoke activate on Controller with callsign: "org.rdk.Warehouse"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check All Event | Listen for Event_Controller_All event (wait 2s) | Controller `all` event received; callsign = `org.rdk.warehouse`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.Warehouse<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

## Plugin Post-conditions

_No plugin-level post-conditions defined_

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M82 |
