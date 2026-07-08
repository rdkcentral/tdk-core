## TestScript Name
RDKV_CERT_AVS_MaintenanceManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [MaintenanceManager_Get_MaintenanceActivity_Status](#maintenancemanager_get_maintenanceactivity_status)
   - [MaintenanceManager_Get_Maintenance_Mode](#maintenancemanager_get_maintenance_mode)
   - [MaintenanceManager_Start_Stop_Maintenance](#maintenancemanager_start_stop_maintenance)
   - [MaintenanceManager_Check_On_Maintenance_StatusChange_Event](#maintenancemanager_check_on_maintenance_statuschange_event)
   - [MaintenanceManager_Check_Start_Maintenance_Twice](#maintenancemanager_check_start_maintenance_twice)
   - [MaintenanceManager_Activate_Deactivate_Event_Test](#maintenancemanager_activate_deactivate_event_test)
   - [MaintenanceManager_Check_MaintenanceActivity_Status](#maintenancemanager_check_maintenanceactivity_status)
   - [MaintenanceManager_Set_MaintenanceMode_With_Invalid_Parameters](#maintenancemanager_set_maintenancemode_with_invalid_parameters)
   - [MaintenanceManager_Set_MaintenanceMode_With_Empty_Parameters](#maintenancemanager_set_maintenancemode_with_empty_parameters)
   - [MaintenanceManager_Set_Invalid_Optout](#maintenancemanager_set_invalid_optout)
   - [MaintenanceManager_Set_Invalid_Maintenancemode](#maintenancemanager_set_invalid_maintenancemode)
   - [MaintenanceManager_Set_MaintenanceMode_Without_Parameters](#maintenancemanager_set_maintenancemode_without_parameters)
   - [MaintenanceManager_Background_OptOutModes_Test](#maintenancemanager_background_optoutmodes_test)
   - [MaintenanceManager_Foreground_OptOutModes_Test](#maintenancemanager_foreground_optoutmodes_test)
   - [MaintenanceManager_Set_MaintenanceMode_Parameter_Only](#maintenancemanager_set_maintenancemode_parameter_only)
   - [MaintenanceManager_Set_Optout_Parameter_Only](#maintenancemanager_set_optout_parameter_only)
   - [MaintenanceManager_Set_Empty_Maintenancemode](#maintenancemanager_set_empty_maintenancemode)
   - [MaintenanceManager_Set_Empty_Optoutmode](#maintenancemanager_set_empty_optoutmode)
   - [MaintenanceManager_Check_Get_MaintenanceActivity_Status_Error](#maintenancemanager_check_get_maintenanceactivity_status_error)
   - [MaintenanceManager_Check_Get_Maintenance_StartTime_Error](#maintenancemanager_check_get_maintenance_starttime_error)
   - [MaintenanceManager_Set_Foreground_MaintenanceMode_with_Invalid_OptOut](#maintenancemanager_set_foreground_maintenancemode_with_invalid_optout)
   - [MaintenanceManager_Set_Background_MaintenanceMode_with_Empty_OptOut](#maintenancemanager_set_background_maintenancemode_with_empty_optout)
   - [MaintenanceManager_Set_Specialchars_MaintenanceMode_with_BYPASS_OPTOUT](#maintenancemanager_set_specialchars_maintenancemode_with_bypass_optout)
   - [MaintenanceManager_Check_Stop_Maintenance_Error](#maintenancemanager_check_stop_maintenance_error)
   - [MaintenanceManager_Set_Numeric_MaintenanceMode_with_None_OptOut](#maintenancemanager_set_numeric_maintenancemode_with_none_optout)
   - [MaintenanceManager_Set_Foreground_MaintenanceMode_with_Numeric_OptOut](#maintenancemanager_set_foreground_maintenancemode_with_numeric_optout)
   - [MaintenanceManager_Set_Specialchars_MaintenanceMode_with_ENFORCE_OPTOUT_OptOut](#maintenancemanager_set_specialchars_maintenancemode_with_enforce_optout_optout)
   - [MaintenanceManager_Set_Specialchars_MaintenanceMode_with_None_OptOut](#maintenancemanager_set_specialchars_maintenancemode_with_none_optout)
   - [MaintenanceManager_Set_Foreground_MaintenanceMode_with_Specialchars_OptOut](#maintenancemanager_set_foreground_maintenancemode_with_specialchars_optout)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **MaintenanceManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.MaintenanceManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onMaintenanceStatusChange event | Register a WebSocket event listener for `onMaintenanceStatusChange` to receive `onMaintenanceStatusChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.register", "params": {"event": "onMaintenanceStatusChange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Optout Modes | `MAINTENANCEMANAGER_OPTOUT_MODES` must be set to the opt-out mode value required for the test | The `MAINTENANCEMANAGER_OPTOUT_MODES` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="maintenancemanager_get_maintenanceactivity_status"></a>
### TestCase Name
MaintenanceManager_Get_MaintenanceActivity_Status

### TestCase ID
MM_01

### TestCase Objective
Check the device fetches and displays the current status of a maintenance activity

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MaintenanceActivity Status | Invoke getMaintenanceActivityStatus on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance activity status is returned successfully |

---

<a id="maintenancemanager_get_maintenance_mode"></a>
### TestCase Name
MaintenanceManager_Get_Maintenance_Mode

### TestCase ID
MM_02

### TestCase Objective
Check if the current maintenance mode and software upgrade opt-out mode can be retrieved from the stored location

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Maintenance Mode | Invoke getMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance mode is returned successfully |

---

<a id="maintenancemanager_start_stop_maintenance"></a>
### TestCase Name
MaintenanceManager_Start_Stop_Maintenance

### TestCase ID
MM_03

### TestCase Objective
Check if the start and stop maintenance methods were successful or not

### TestCase Pre-condition

#### TestCase Pre-condition 1: Stop_Maintenance_If_Started

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MaintenanceActivity Status | Get Maintenance Activity Status from MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance activity status is returned successfully |
| 2 | Stop Maintenance | *(Conditional statement executed only if previous step condition is met)*<br>Stop Maintenance on MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Maintenance | Invoke startMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.startMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is launched successfully  |
| 2 | Stop Maintenance | Invoke stopMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

---

<a id="maintenancemanager_check_on_maintenance_statuschange_event"></a>
### TestCase Name
MaintenanceManager_Check_On_Maintenance_StatusChange_Event

### TestCase ID
MM_04

### TestCase Objective
Check if the event is triggered when there is a change in the maintenance state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Stop_Maintenance_If_Started

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MaintenanceActivity Status | Get Maintenance Activity Status from MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance activity status is returned successfully |
| 2 | Stop Maintenance | *(Conditional statement executed only if previous step condition is met)*<br>Stop Maintenance on MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Maintenance | Invoke startMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.startMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is launched successfully  |
| 2 | Check On Maintenance StatusChange Event | Listen for `Event_On_Maintenance_StatusChange` event (timeout: 3s) | Verify that the event is received and validated successfully |
| 3 | Stop Maintenance | Invoke stopMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

---

<a id="maintenancemanager_check_start_maintenance_twice"></a>
### TestCase Name
MaintenanceManager_Check_Start_Maintenance_Twice

### TestCase ID
MM_05

### TestCase Objective
Check start maintenance API returns success status as false when called twice simultaneously

### TestCase Pre-condition

#### TestCase Pre-condition 1: Stop_Maintenance_If_Started

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MaintenanceActivity Status | Get Maintenance Activity Status from MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance activity status is returned successfully |
| 2 | Stop Maintenance | *(Conditional statement executed only if previous step condition is met)*<br>Stop Maintenance on MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Maintenance | Invoke startMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.startMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is launched successfully  |
| 2 | Start Maintenance | Invoke startMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.startMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_activate_deactivate_event_test"></a>
### TestCase Name
MaintenanceManager_Activate_Deactivate_Event_Test

### TestCase ID
MM_06

### TestCase Objective
Validates statechange event on Activating and deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate MaintenanceManager Plugin | Invoke deactivate on Controller with callsign: "org.rdk.MaintenanceManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.maintenancemanager` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate MaintenanceManager Plugin | Invoke activate on Controller with callsign: "org.rdk.MaintenanceManager" (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | Verify that the `statechange` event is received for callsign `org.rdk.maintenancemanager` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="maintenancemanager_check_maintenanceactivity_status"></a>
### TestCase Name
MaintenanceManager_Check_MaintenanceActivity_Status

### TestCase ID
MM_07

### TestCase Objective
Check the status of maintenance activity after initiating the start maintenance API

### TestCase Pre-condition

#### TestCase Pre-condition 1: Stop_Maintenance_If_Started

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MaintenanceActivity Status | Get Maintenance Activity Status from MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance activity status is returned successfully |
| 2 | Stop Maintenance | *(Conditional statement executed only if previous step condition is met)*<br>Stop Maintenance on MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is stopped successfully  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start Maintenance | Invoke startMaintenance on org.rdk.MaintenanceManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.startMaintenance"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance is launched successfully  |
| 2 | Check MaintenanceActivity Status | Invoke getMaintenanceActivityStatus on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned status matches the expected value `MAINTENANCE_STARTED`  |

---

<a id="maintenancemanager_set_maintenancemode_with_invalid_parameters"></a>
### TestCase Name
MaintenanceManager_Set_MaintenanceMode_With_Invalid_Parameters

### TestCase ID
MM_08

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when invalid parameters are provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set MaintenanceMode With Invalid Parameters | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "test", optOut: "test"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "test", "optOut": "test"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_maintenancemode_with_empty_parameters"></a>
### TestCase Name
MaintenanceManager_Set_MaintenanceMode_With_Empty_Parameters

### TestCase ID
MM_09

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when empty parameters are provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set MaintenanceMode With Empty Parameters | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "", optOut: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "", "optOut": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_invalid_optout"></a>
### TestCase Name
MaintenanceManager_Set_Invalid_Optout

### TestCase ID
MM_10

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when invalid optOut parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Invalid Optout | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "BACKGROUND", optOut: "test"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "BACKGROUND", "optOut": "test"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_invalid_maintenancemode"></a>
### TestCase Name
MaintenanceManager_Set_Invalid_Maintenancemode

### TestCase ID
MM_11

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when invalid maintenancemode parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Invalid Maintenancemode | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "test", optOut: "NONE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "test", "optOut": "NONE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_maintenancemode_without_parameters"></a>
### TestCase Name
MaintenanceManager_Set_MaintenanceMode_Without_Parameters

### TestCase ID
MM_12

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when parameters are not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set MaintenanceMode Without Parameters | Invoke setMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_background_optoutmodes_test"></a>
### TestCase Name
MaintenanceManager_Background_OptOutModes_Test

### TestCase ID
MM_13

### TestCase Objective
Check the ability to set and retrieve the maintenance mode as 'Background' and the software upgrade opt-out modes (NONE, ENFORCE_OPTOUT, BYPASS_OPTOUT, IGNORE_UPDATE)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Maintenance Optout Mode | Invoke getMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance mode is returned successfully |
| 2 | Set Maintenance Optout Mode | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "BACKGROUND", optOut: "<MAINTENANCEMANAGER_OPTOUT_MODES>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "BACKGROUND", "optOut": "<MAINTENANCEMANAGER_OPTOUT_MODES>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance mode is set successfully  |
| 3 | Get Maintenance Optout Mode | Invoke getMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Returned value matches the iterated value set in the previous step  |

---

<a id="maintenancemanager_foreground_optoutmodes_test"></a>
### TestCase Name
MaintenanceManager_Foreground_OptOutModes_Test

### TestCase ID
MM_14

### TestCase Objective
Check the ability to set and retrieve the maintenance mode as 'Foreground' and the software upgrade opt-out modes (NONE, ENFORCE_OPTOUT, BYPASS_OPTOUT, IGNORE_UPDATE)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Maintenance Optout Mode | Invoke getMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the maintenance mode is returned successfully |
| 2 | Set Maintenance Optout Mode | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND", optOut: "<MAINTENANCEMANAGER_OPTOUT_MODES>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND", "optOut": "<MAINTENANCEMANAGER_OPTOUT_MODES>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Confirm that maintenance mode is set successfully  |
| 3 | Get Maintenance Optout Mode | Invoke getMaintenanceMode on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true`. Returned value matches the iterated value set in the previous step  |

---

<a id="maintenancemanager_set_maintenancemode_parameter_only"></a>
### TestCase Name
MaintenanceManager_Set_MaintenanceMode_Parameter_Only

### TestCase ID
MM_15

### TestCase Objective
Check that the SetMaintenanceMode method returns an error when only the maintenancemode parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set MaintenanceMode Parameter Only | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_optout_parameter_only"></a>
### TestCase Name
MaintenanceManager_Set_Optout_Parameter_Only

### TestCase ID
MM_16

### TestCase Objective
Check that the SetMaintenanceMode method returns an error when only the optoutmode parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Optout Parameter Only | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with optOut: "NONE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"optOut": "NONE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_empty_maintenancemode"></a>
### TestCase Name
MaintenanceManager_Set_Empty_Maintenancemode

### TestCase ID
MM_17

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when empty maintenancemode parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Empty Maintenancemode | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "", optOut: "NONE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "", "optOut": "NONE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_empty_optoutmode"></a>
### TestCase Name
MaintenanceManager_Set_Empty_Optoutmode

### TestCase ID
MM_18

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when empty optoutmode parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Empty Optoutmode | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND", optOut: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND", "optOut": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_check_get_maintenanceactivity_status_error"></a>
### TestCase Name
MaintenanceManager_Check_Get_MaintenanceActivity_Status_Error

### TestCase ID
MM_19

### TestCase Objective
Check if the getMaintenanceActivityStatus method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is disabled successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Get MaintenanceActivity Status API Response | Invoke getMaintenanceActivityStatus on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceActivityStatus"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="maintenancemanager_check_get_maintenance_starttime_error"></a>
### TestCase Name
MaintenanceManager_Check_Get_Maintenance_StartTime_Error

### TestCase ID
MM_20

### TestCase Objective
Check if the getMaintenanceStartTime method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is disabled successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Get Maintenance StartTime API Response | Invoke getMaintenanceStartTime on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.getMaintenanceStartTime"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="maintenancemanager_set_foreground_maintenancemode_with_invalid_optout"></a>
### TestCase Name
MaintenanceManager_Set_Foreground_MaintenanceMode_with_Invalid_OptOut

### TestCase ID
MM_21

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when maintenancemode as foreground and invalid optOut parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Foreground MaintenanceMode with Invalid OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND", optOut: "INVALID_OPTOUT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND", "optOut": "INVALID_OPTOUT"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_background_maintenancemode_with_empty_optout"></a>
### TestCase Name
MaintenanceManager_Set_Background_MaintenanceMode_with_Empty_OptOut

### TestCase ID
MM_22

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when maintenancemode as background and empty optOut parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Background MaintenanceMode with Empty OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "BACKGROUND", optOut: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "BACKGROUND", "optOut": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_specialchars_maintenancemode_with_bypass_optout"></a>
### TestCase Name
MaintenanceManager_Set_Specialchars_MaintenanceMode_with_BYPASS_OPTOUT

### TestCase ID
MM_23

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when Maintenancemode as special character and with OptOut parameter as BYPASS_OPTOUT

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Specialchars MaintenanceMode with BYPASS OPTOUT | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "@", optOut: "BYPASS_OPTOUT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "@", "optOut": "BYPASS_OPTOUT"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_check_stop_maintenance_error"></a>
### TestCase Name
MaintenanceManager_Check_Stop_Maintenance_Error

### TestCase ID
MM_24

### TestCase Objective
Check if the stop maintenance methods returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Deactivate_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate Plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.MaintenanceManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is disabled successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if previous step condition is met)*<br>Check Active Status of MaintenanceManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.MaintenanceManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Stop Maintenance API Response | Invoke stopMaintenance on org.rdk.MaintenanceManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.stopMaintenance"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |

---

<a id="maintenancemanager_set_numeric_maintenancemode_with_none_optout"></a>
### TestCase Name
MaintenanceManager_Set_Numeric_MaintenanceMode_with_None_OptOut

### TestCase ID
MM_25

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when the MaintenanceMode is set to a numeric value (123) and the OptOut parameter is none

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Numeric MaintenanceMode with None OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "123", optOut: "NONE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": 123, "optOut": "NONE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_foreground_maintenancemode_with_numeric_optout"></a>
### TestCase Name
MaintenanceManager_Set_Foreground_MaintenanceMode_with_Numeric_OptOut

### TestCase ID
MM_26

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when maintenancemode as foreground and invalid optOut parameter is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Foreground MaintenanceMode with Numeric OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND", optOut: "456"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND", "optOut": 456}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_specialchars_maintenancemode_with_enforce_optout_optout"></a>
### TestCase Name
MaintenanceManager_Set_Specialchars_MaintenanceMode_with_ENFORCE_OPTOUT_OptOut

### TestCase ID
MM_27

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when Maintenancemode set as special character and with OptOut parameter set as ENFORCE_OPTOUT

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Specialchars MaintenanceMode with ENFORCE OPTOUT OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "@", optOut: "ENFORCE_OPTOUT"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "@", "optOut": "ENFORCE_OPTOUT"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_specialchars_maintenancemode_with_none_optout"></a>
### TestCase Name
MaintenanceManager_Set_Specialchars_MaintenanceMode_with_None_OptOut

### TestCase ID
MM_28

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when the MaintenanceMode contains special characters and the OptOut parameter is none

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Specialchars MaintenanceMode with None OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "@#\$%^\*()", optOut: "NONE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "@#$%^*()", "optOut": "NONE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="maintenancemanager_set_foreground_maintenancemode_with_specialchars_optout"></a>
### TestCase Name
MaintenanceManager_Set_Foreground_MaintenanceMode_with_Specialchars_OptOut

### TestCase ID
MM_29

### TestCase Objective
Check if the SetMaintenanceMode method returns an error when the OptOut parameter contains special characters while the MaintenanceMode is foreground

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Foreground MaintenanceMode with Specialchars OptOut | Invoke setMaintenanceMode on org.rdk.MaintenanceManager with maintenanceMode: "FOREGROUND", optOut: "@#\$%^\*()"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.setMaintenanceMode", "params": {"maintenanceMode": "FOREGROUND", "optOut": "@#$%^*()"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onMaintenanceStatusChange event | Unregister the WebSocket event listener for `onMaintenanceStatusChange` to stop receiving `onMaintenanceStatusChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.MaintenanceManager.1.unregister", "params": {"event": "onMaintenanceStatusChange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI-Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M134 |

<div align="right"><a href="#testscript-name">&#8593; Go to Top</a></div>
