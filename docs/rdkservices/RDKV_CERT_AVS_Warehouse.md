## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [WareHouse_Get_STB_Device_Info (WH_01)](#warehouse_get_stb_device_info-wh_01)
   - [WareHouse_Set_Front_Panel_State_None (WH_02)](#warehouse_set_front_panel_state_none-wh_02)
   - [WareHouse_Set_Front_Panel_State_Download_In_Progress (WH_03)](#warehouse_set_front_panel_state_download_in_progress-wh_03)
   - [WareHouse_Set_Front_Panel_State_Download_Failed (WH_04)](#warehouse_set_front_panel_state_download_failed-wh_04)
   - [WareHouse_Set_Front_Panel_State_Download_Invalid (WH_05)](#warehouse_set_front_panel_state_download_invalid-wh_05)
   - [WareHouse_Light_Reset (WH_06)](#warehouse_light_reset-wh_06)
   - [WareHouse_Check_Is_Clean (WH_07)](#warehouse_check_is_clean-wh_07)
   - [WareHouse_Reset_Device (WH_08)](#warehouse_reset_device-wh_08)
   - [WareHouse_Internal_Reset (WH_09)](#warehouse_internal_reset-wh_09)
   - [WareHouse_Check_Event_On_Device_Reset (WH_10)](#warehouse_check_event_on_device_reset-wh_10)
   - [Warehouse_ActivateDeactivate_Event_Test (WH_11)](#warehouse_activatedeactivate_event_test-wh_11)
   - [WareHouse_Set_Front_Panel_State_EmptyValue (WH_12)](#warehouse_set_front_panel_state_emptyvalue-wh_12)
   - [Warehouse_ActivateDeactivate_All_Event_Test (WH_13)](#warehouse_activatedeactivate_all_event_test-wh_13)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **Warehouse** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.Warehouse` (version 1)

**API Coverage**

- **State / Query APIs**: `getDeviceInfo`, `isClean`
- **Configuration APIs**: `resetDevice`, `setFrontPanelState`
- **Events**: `resetDone`
- **Other APIs**: `internalReset`, `lightReset`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getDeviceInfo` | Provides STB device information |
| `internalReset` | Invokes the internal reset script, which reboots the WarehouseService |
| `isClean` | Checks locations where customer data may be stored |
| `lightReset` | Performs light reset |
| `resetDevice` | Resets the STB to the warehouse state |
| `setFrontPanelState` | Sets the discoverable status of the device |

### Events Under Test

| Event | Description |
|-------|-------------|
| `resetDone` | Notifies about the status of the warehouse reset operation |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Warehouse"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Reset_Done` on `Warehouse` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="warehouse_get_stb_device_info-wh_01"></a>
### WareHouse_Get_STB_Device_Info (WH_01)

**Objective:** Gets all STB device info

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get STB DeviceInfo | Invoke `getDeviceInfo` on `org.rdk.Warehouse`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.getDeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` STB device info returned successfully with all device details |

---

<a id="warehouse_set_front_panel_state_none-wh_02"></a>
### WareHouse_Set_Front_Panel_State_None (WH_02)

**Objective:** Sets the front panel state to None

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke `setFrontPanelState` on `org.rdk.Warehouse` with `state`: `0` (None)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": -1}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Front Panel State set to None successfully |

---

<a id="warehouse_set_front_panel_state_download_in_progress-wh_03"></a>
### WareHouse_Set_Front_Panel_State_Download_In_Progress (WH_03)

**Objective:** Sets the front panel state to DOWNLOAD IN PROGRESS

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke `setFrontPanelState` on `org.rdk.Warehouse` with `state`: `1` (Download In Progress)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 1}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Front Panel State set to Download In Progress successfully |

---

<a id="warehouse_set_front_panel_state_download_failed-wh_04"></a>
### WareHouse_Set_Front_Panel_State_Download_Failed (WH_04)

**Objective:** Sets the front panel state to DOWNLOAD FAILED

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke `setFrontPanelState` on `org.rdk.Warehouse` with `state`: `3` (Download Failed)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 3}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Front Panel State set to Download Failed successfully |

---

<a id="warehouse_set_front_panel_state_download_invalid-wh_05"></a>
### WareHouse_Set_Front_Panel_State_Download_Invalid (WH_05)

**Objective:** Sets the front panel state to invalid value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State | Invoke `setFrontPanelState` on `org.rdk.Warehouse` with `state`: `2` (invalid value)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState", "params": {"state": 2}}' http://127.0.0.1:9998/jsonrpc` | API returns error `success: false`  |

---

<a id="warehouse_light_reset-wh_06"></a>
### WareHouse_Light_Reset (WH_06)

**Objective:** Performs a light reset of application data

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Light Reset | Invoke `lightReset` on `org.rdk.Warehouse`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.lightReset"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Light Reset completed successfully |

---

<a id="warehouse_check_is_clean-wh_07"></a>
### WareHouse_Check_Is_Clean (WH_07)

**Objective:** Checks locations where customer data may be stored

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Is Clean | Invoke `isClean` on `org.rdk.Warehouse`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.isClean"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Clean status returned with `clean` boolean field and any `dirty` locations listed |

---

<a id="warehouse_reset_device-wh_08"></a>
### WareHouse_Reset_Device (WH_08)

**Objective:** Resets the STB to the warehouse state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Device | Invoke `resetDevice` on `org.rdk.Warehouse`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Device reset to warehouse state successfully |

---

<a id="warehouse_internal_reset-wh_09"></a>
### WareHouse_Internal_Reset (WH_09)

**Objective:** Resets the STB to the warehouse state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Internal Reset | Invoke `internalReset` on `org.rdk.Warehouse` with `passPhrase`: `"FOR TEST PURPOSES ONLY"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.internalReset", "params": {"passPhrase": "FOR TEST PURPOSES ONLY"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Internal Reset completed successfully; WarehouseService rebooted |

---

<a id="warehouse_check_event_on_device_reset-wh_10"></a>
### WareHouse_Check_Event_On_Device_Reset (WH_10)

**Objective:** Checks if event is received on device reset

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Reset Device | Invoke `resetDevice` on `org.rdk.Warehouse` with `resetType`: `"USERFACTORY"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.resetDevice", "params": {"resetType": "USERFACTORY"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Device reset with `USERFACTORY` reset type successfully |
| 2 | Check Event Reset Done | Listen for `resetDone` event (`Event_Reset_Done`) on `org.rdk.Warehouse` (wait 5s)<br>*(Event registration done in Pre-condition 2)* | Expected `True` and `resetDone` event received confirming warehouse reset operation completed |

**Post-condition:**

#### Post-condition 1: Set_Back_Plugin_Pre-requisite

> **Note:** This post-condition re-initializes the plugin pre-requisites after the device resets. It is handled internally (external function call no JSON-RPC command required)

---

<a id="warehouse_activatedeactivate_event_test-wh_11"></a>
### Warehouse_ActivateDeactivate_Event_Test (WH_11)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Warehouse"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Warehouse Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.Warehouse"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.warehouse`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Warehouse Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Warehouse"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `org.rdk.warehouse`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="warehouse_set_front_panel_state_emptyvalue-wh_12"></a>
### WareHouse_Set_Front_Panel_State_EmptyValue (WH_12)

**Objective:** Sets the front panel state to EmptyValue

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set FrontPanel State EmptyValue | Invoke `setFrontPanelState` on `org.rdk.Warehouse`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.Warehouse.1.setFrontPanelState"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `incorrect state` |

---

<a id="warehouse_activatedeactivate_all_event_test-wh_13"></a>
### Warehouse_ActivateDeactivate_All_Event_Test (WH_13)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Warehouse"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Warehouse Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.Warehouse"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for `Event_Controller_All` event (wait 2s) | Controller `all` event received; callsign = `org.rdk.warehouse`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate Warehouse Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.Warehouse"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.Warehouse"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for `Event_Controller_All` event (wait 2s) | Controller `all` event received; callsign = `org.rdk.warehouse`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.Warehouse"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M82 |