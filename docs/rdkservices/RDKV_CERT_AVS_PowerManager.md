## TestScript Name
RDKV_CERT_AVS_PowerManager

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [PowerManager_Get_Power_State](#powermanager_get_power_state)
   - [PowerManager_Get_PowerState_Before_Reboot](#powermanager_get_powerstate_before_reboot)
   - [PowerManager_Get_Network_Standby_Mode](#powermanager_get_network_standby_mode)
   - [PowerManager_Get_Temperature_Thresholds](#powermanager_get_temperature_thresholds)
   - [PowerManager_Get_Thermal_State](#powermanager_get_thermal_state)
   - [PowerManager_Get_Time_Since_Wakeup](#powermanager_get_time_since_wakeup)
   - [PowerManager_Get_Wakeup_Source_Config](#powermanager_get_wakeup_source_config)
   - [PowerManager_Get_Last_Wakeup_KeyCode](#powermanager_get_last_wakeup_keycode)
   - [PowerManager_Get_Last_Wakeup_Reason](#powermanager_get_last_wakeup_reason)
   - [PowerManager_Get_Overtemp_Grace_Interval](#powermanager_get_overtemp_grace_interval)
   - [PowerManager_Set_NetworkStandbyMode_Enabled](#powermanager_set_networkstandbymode_enabled)
   - [PowerManager_Set_NetworkStandbyMode_Disabled](#powermanager_set_networkstandbymode_disabled)
   - [PowerManager_Set_OvertempGraceInterval_Valid](#powermanager_set_overtempgraceinterval_valid)
   - [PowerManager_Set_WakeupSourceConfig](#powermanager_set_wakeupsourceconfig)
   - [PowerManager_Get_NetworkStandbyMode_True](#powermanager_get_networkstandbymode_true)
   - [PowerManager_Get_NetworkStandbyMode_False](#powermanager_get_networkstandbymode_false)
   - [PowerManager_Event_ThermalModeChanged](#powermanager_event_thermalmodechanged)
   - [PowerManager_Get_OvertempGraceInterval](#powermanager_get_overtempgraceinterval)
   - [PowerManager_SetPowerState_STANDBY](#powermanager_setpowerstate_standby)
   - [PowerManager_SetPowerState_LIGHT_SLEEP](#powermanager_setpowerstate_light_sleep)
   - [PowerManager_Event_NetworkStandbyModeChanged_True](#powermanager_event_networkstandbymodechanged_true)
   - [PowerManager_Event_NetworkStandbyModeChanged_False](#powermanager_event_networkstandbymodechanged_false)
   - [PowerManager_Event_PowerModeChanged_To_STANDBY](#powermanager_event_powermodechanged_to_standby)
   - [PowerManager_Event_PowerModeChanged_To_LIGHT_SLEEP](#powermanager_event_powermodechanged_to_light_sleep)
   - [PowerManager_Event_RebootBegin](#powermanager_event_rebootbegin)
   - [PowerManager_AddPreChangeClient_Valid](#powermanager_addprechangeclient_valid)
   - [PowerManager_PowerModePreChange_Lifecycle_Event](#powermanager_powermodeprechange_lifecycle_event)
   - [PowerManager_Lifecycle_PreChangeClient_Delay_Complete](#powermanager_lifecycle_prechangeclient_delay_complete)
   - [PowerManager_MultiStep_PowerState_Cycle](#powermanager_multistep_powerstate_cycle)
   - [PowerManager_SetNetworkStandbyMode_Invalid_Type](#powermanager_setnetworkstandbymode_invalid_type)
   - [PowerManager_SetTemperatureThresholds_Invalid_HighType](#powermanager_settemperaturethresholds_invalid_hightype)
   - [PowerManager_SetTemperatureThresholds_Missing_Critical](#powermanager_settemperaturethresholds_missing_critical)
   - [PowerManager_SetWakeupSourceConfig_Invalid_WakeupSource](#powermanager_setwakeupsourceconfig_invalid_wakeupsource)
   - [PowerManager_SetWakeupSourceConfig_Missing_Enabled_Param](#powermanager_setwakeupsourceconfig_missing_enabled_param)
   - [PowerManager_SetOvertempGraceInterval_Negative_Value](#powermanager_setovertempgraceinterval_negative_value)
   - [PowerManager_AddPreChangeClient_EmptyClientName](#powermanager_addprechangeclient_emptyclientname)
   - [PowerManager_AddPreChangeClient_No_Params](#powermanager_addprechangeclient_no_params)
   - [PowerManager_RemovePreChangeClient_Invalid_Id](#powermanager_removeprechangeclient_invalid_id)
   - [PowerManager_PreChangeComplete_Invalid_ClientId](#powermanager_prechangecomplete_invalid_clientid)
   - [PowerManager_DelayPowerModeChange_Invalid_ClientId](#powermanager_delaypowermodechange_invalid_clientid)
   - [PowerManager_ErrorState_PreChangeComplete_After_Remove](#powermanager_errorstate_prechangecomplete_after_remove)
   - [PowerManager_SetPowerState_Invalid_State](#powermanager_setpowerstate_invalid_state)
   - [PowerManager_SetPowerState_Negative_Value](#powermanager_setpowerstate_negative_value)
   - [PowerManager_ActivateDeactivate_StateChange_Event_Test](#powermanager_activatedeactivate_statechange_event_test)
   - [PowerManager_ActivateDeactivate_All_Event_Test](#powermanager_activatedeactivate_all_event_test)
   - [PowerManager_PowerState_Before_Reboot_Persistence](#powermanager_powerstate_before_reboot_persistence)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **PowerManager** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.PowerManager` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_PowerManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onPowerModeChanged event | Register a WebSocket event listener for `onPowerModeChanged` to receive `onPowerModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.register", "params": {"event": "onPowerModeChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the onPowerModePreChange event | Register a WebSocket event listener for `onPowerModePreChange` to receive `onPowerModePreChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.register", "params": {"event": "onPowerModePreChange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the onNetworkStandbyModeChanged event | Register a WebSocket event listener for `onNetworkStandbyModeChanged` to receive `onNetworkStandbyModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.register", "params": {"event": "onNetworkStandbyModeChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 4 | Subscribe to the onRebootBegin event | Register a WebSocket event listener for `onRebootBegin` to receive `onRebootBegin` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.register", "params": {"event": "onRebootBegin", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 5 | Subscribe to the onThermalModeChanged event | Register a WebSocket event listener for `onThermalModeChanged` to receive `onThermalModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.register", "params": {"event": "onThermalModeChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 6 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 7 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure Wakeup Source Config | `POWERMANAGER_WAKEUP_SOURCE_CONFIG` must be set to the wakeup source types supported by the device | The `POWERMANAGER_WAKEUP_SOURCE_CONFIG` value should be correctly configured in the device-specific config file |

## Test Cases

<a id="powermanager_get_power_state"></a>
### TestCase Name
PowerManager_Get_Power_State

### TestCase ID
PWRM_01

### TestCase Objective
Verify getPowerState returns valid currentState and previousState values

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |

---

<a id="powermanager_get_powerstate_before_reboot"></a>
### TestCase Name
PowerManager_Get_PowerState_Before_Reboot

### TestCase ID
PWRM_02

### TestCase Objective
Verify getPowerStateBeforeReboot returns a valid power state enum value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state before reboot | Invoke getPowerStateBeforeReboot on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state before reboot is returned successfully |

---

<a id="powermanager_get_network_standby_mode"></a>
### TestCase Name
PowerManager_Get_Network_Standby_Mode

### TestCase ID
PWRM_03

### TestCase Objective
Verify getNetworkStandbyMode returns a valid boolean standbyMode field

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the network standby mode is returned successfully |

---

<a id="powermanager_get_temperature_thresholds"></a>
### TestCase Name
PowerManager_Get_Temperature_Thresholds

### TestCase ID
PWRM_04

### TestCase Objective
Verify getTemperatureThresholds returns valid values for high and critical fields

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get temperature thresholds | Invoke getTemperatureThresholds on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getTemperatureThresholds"}' http://127.0.0.1:9998/jsonrpc` | Verify that the temperature thresholds is returned successfully |

---

<a id="powermanager_get_thermal_state"></a>
### TestCase Name
PowerManager_Get_Thermal_State

### TestCase ID
PWRM_05

### TestCase Objective
Verify getThermalState returns currentTemperature value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get thermal state | Invoke getThermalState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getThermalState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the thermal state is returned successfully |

---

<a id="powermanager_get_time_since_wakeup"></a>
### TestCase Name
PowerManager_Get_Time_Since_Wakeup

### TestCase ID
PWRM_06

### TestCase Objective
Verify getTimeSinceWakeup returns secondsSinceWakeup as a non-negative integer

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get time since wakeup | Invoke getTimeSinceWakeup on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getTimeSinceWakeup"}' http://127.0.0.1:9998/jsonrpc` | Verify that the time since wakeup is returned successfully |

---

<a id="powermanager_get_wakeup_source_config"></a>
### TestCase Name
PowerManager_Get_Wakeup_Source_Config

### TestCase ID
PWRM_07

### TestCase Objective
Verify getWakeupSourceConfig returns a non-empty array with wakeupSource and enabled fields

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get wakeup source config | Invoke getWakeupSourceConfig on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getWakeupSourceConfig"}' http://127.0.0.1:9998/jsonrpc` | Verify that the wakeup source config is returned successfully |

---

<a id="powermanager_get_last_wakeup_keycode"></a>
### TestCase Name
PowerManager_Get_Last_Wakeup_KeyCode

### TestCase ID
PWRM_08

### TestCase Objective
Verify getLastWakeupKeyCode property returns a valid integer keycode

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get last wakeup key code | Invoke getLastWakeupKeyCode on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getLastWakeupKeyCode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the last wakeup key code is returned successfully |

---

<a id="powermanager_get_last_wakeup_reason"></a>
### TestCase Name
PowerManager_Get_Last_Wakeup_Reason

### TestCase ID
PWRM_09

### TestCase Objective
Verify getLastWakeupReason property returns a valid wakeupReason string from the documented enum

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get last wakeup reason | Invoke getLastWakeupReason on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getLastWakeupReason"}' http://127.0.0.1:9998/jsonrpc` | Verify that the last wakeup reason is returned successfully |

---

<a id="powermanager_get_overtemp_grace_interval"></a>
### TestCase Name
PowerManager_Get_Overtemp_Grace_Interval

### TestCase ID
PWRM_10

### TestCase Objective
Verify getOvertempGraceInterval property returns a non-negative integer graceInterval

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get overtemp grace interval | Invoke getOvertempGraceInterval on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getOvertempGraceInterval"}' http://127.0.0.1:9998/jsonrpc` | Verify that the overtemp grace interval is returned successfully |

---

<a id="powermanager_set_networkstandbymode_enabled"></a>
### TestCase Name
PowerManager_Set_NetworkStandbyMode_Enabled

### TestCase ID
PWRM_11

### TestCase Objective
Verify setNetworkStandbyMode with standbyMode true returns null (success)

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="powermanager_set_networkstandbymode_disabled"></a>
### TestCase Name
PowerManager_Set_NetworkStandbyMode_Disabled

### TestCase ID
PWRM_12

### TestCase Objective
Verify setNetworkStandbyMode with standbyMode false returns null (success)

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "false"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="powermanager_set_overtempgraceinterval_valid"></a>
### TestCase Name
PowerManager_Set_OvertempGraceInterval_Valid

### TestCase ID
PWRM_13

### TestCase Objective
Verify setOvertempGraceInterval write-only property with graceInterval=300 returns null (success)

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set overtemp grace interval | Invoke setOvertempGraceInterval on org.rdk.PowerManager with graceInterval: 300<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setOvertempGraceInterval", "params": {"graceInterval": 300}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="powermanager_set_wakeupsourceconfig"></a>
### TestCase Name
PowerManager_Set_WakeupSourceConfig

### TestCase ID
PWRM_14

### TestCase Objective
Verify setWakeupSourceConfig with various wakeup sources and enabled true returns null (success)

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set wakeup source config | Invoke setWakeupSourceConfig on org.rdk.PowerManager with wakeupSource: "<POWERMANAGER_WAKEUP_SOURCE_CONFIG>", enabled: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setWakeupSourceConfig", "params": {"wakeupSource": "<POWERMANAGER_WAKEUP_SOURCE_CONFIG>", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="powermanager_get_networkstandbymode_true"></a>
### TestCase Name
PowerManager_Get_NetworkStandbyMode_True

### TestCase ID
PWRM_15

### TestCase Objective
Set network standby mode to true, then get it back and verify the value matches

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `True` |

---

<a id="powermanager_get_networkstandbymode_false"></a>
### TestCase Name
PowerManager_Get_NetworkStandbyMode_False

### TestCase ID
PWRM_16

### TestCase Objective
Set network standby mode to false, then get it back and verify the value matches

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "false"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `False` |

---

<a id="powermanager_event_thermalmodechanged"></a>
### TestCase Name
PowerManager_Event_ThermalModeChanged

### TestCase ID
PWRM_17

### TestCase Objective
Set temperature thresholds to high equal to 0.0 and critical equal to 0.0, then get them back and verify values match

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set temperature thresholds | Invoke setTemperatureThresholds on org.rdk.PowerManager with high: 0.0, critical: 0.0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setTemperatureThresholds", "params": {"high": 0.0, "critical": 0.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for thermal mode changed event | Listen for `Event_On_ThermalMode_Changed` event and wait up to 5 second(s) | Verify that the event is received and validated successfully |
| 3 | Get temperature thresholds | Invoke getTemperatureThresholds on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getTemperatureThresholds"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `0.0,0.0` |

---

<a id="powermanager_get_overtempgraceinterval"></a>
### TestCase Name
PowerManager_Get_OvertempGraceInterval

### TestCase ID
PWRM_18

### TestCase Objective
Set overtemp grace interval to 300, then get it back and verify the value matches

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set overtemp grace interval | Invoke setOvertempGraceInterval on org.rdk.PowerManager with graceInterval: 300<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setOvertempGraceInterval", "params": {"graceInterval": 300}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Get overtemp grace interval | Invoke getOvertempGraceInterval on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getOvertempGraceInterval"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `300` |

---

<a id="powermanager_setpowerstate_standby"></a>
### TestCase Name
PowerManager_SetPowerState_STANDBY

### TestCase ID
PWRM_19

### TestCase Objective
Verify setPowerState (STANDBY) changes the power state to STANDBY and getPowerState reflects the change

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "STANDBY", reason: "TDKAPITest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "STANDBY", "reason": "TDKAPITest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Get power state | Invoke getPowerState on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `STANDBY` |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_setpowerstate_light_sleep"></a>
### TestCase Name
PowerManager_SetPowerState_LIGHT_SLEEP

### TestCase ID
PWRM_20

### TestCase Objective
Verify setPowerState (LIGHT_SLEEP) changes the power state to LIGHT_SLEEP and getPowerState reflects the change

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "LIGHT_SLEEP", reason: "TDKAPITest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "LIGHT_SLEEP", "reason": "TDKAPITest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Get power state | Invoke getPowerState on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `LIGHT_SLEEP` |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_event_networkstandbymodechanged_true"></a>
### TestCase Name
PowerManager_Event_NetworkStandbyModeChanged_True

### TestCase ID
PWRM_21

### TestCase Objective
Set network standby mode to true and verify onNetworkStandbyModeChanged event fires with enabled is true

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for network standby mode changed event | Listen for `Event_On_NetworkStandbyMode_Changed` event and wait up to 3 second(s) | Verify that the event is received and validated successfully |
| 3 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `true` |

---

<a id="powermanager_event_networkstandbymodechanged_false"></a>
### TestCase Name
PowerManager_Event_NetworkStandbyModeChanged_False

### TestCase ID
PWRM_22

### TestCase Objective
Set network standby mode to false and verify onNetworkStandbyModeChanged event fires with enabled is false

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "false"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": false}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for network standby mode changed event | Listen for `Event_On_NetworkStandbyMode_Changed` event and wait up to 3 second(s) | Verify that the event is received and validated successfully |
| 3 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `false` |

---

<a id="powermanager_event_powermodechanged_to_standby"></a>
### TestCase Name
PowerManager_Event_PowerModeChanged_To_STANDBY

### TestCase ID
PWRM_23

### TestCase Objective
Verify onPowerModeChanged event fires with newState is STANDBY

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "STANDBY", reason: "TDKEventTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "STANDBY", "reason": "TDKEventTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for power mode changed event | Listen for `Event_On_PowerMode_Changed` event and wait up to 5 second(s) | Verify that the event is received and validated successfully |
| 3 | Get power state | Invoke getPowerState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `STANDBY` |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_event_powermodechanged_to_light_sleep"></a>
### TestCase Name
PowerManager_Event_PowerModeChanged_To_LIGHT_SLEEP

### TestCase ID
PWRM_24

### TestCase Objective
Verify onPowerModeChanged event fires with newState is LIGHT_SLEEP

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "LIGHT_SLEEP", reason: "TDKEventTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "LIGHT_SLEEP", "reason": "TDKEventTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for power mode changed event | Listen for `Event_On_PowerMode_Changed` event and wait up to 5 second(s) | Verify that the event is received and validated successfully |
| 3 | Get power state | Invoke getPowerState on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `LIGHT_SLEEP` |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_event_rebootbegin"></a>
### TestCase Name
PowerManager_Event_RebootBegin

### TestCase ID
PWRM_25

### TestCase Objective
Trigger device reboot with reboot reason and verify onRebootBegin event fires with matching rebootRequestor

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Reboot device | Invoke reboot on org.rdk.PowerManager with rebootRequestor: "TDK", rebootReasonCustom: "TDKAPITest", rebootReasonOther: "TDK API Validation"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.reboot", "params": {"rebootRequestor": "TDK", "rebootReasonCustom": "TDKAPITest", "rebootReasonOther": "TDK API Validation"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Listen for reboot begin event | Listen for `Event_On_Reboot_Begin` event | Verify that the event is received and validated successfully |
| 3 | Wait for device to come up | Wait for device to come up on the device | Device should come up online within the expected time and plugin pre-requisites should be restored successfully |

---

<a id="powermanager_addprechangeclient_valid"></a>
### TestCase Name
PowerManager_AddPreChangeClient_Valid

### TestCase ID
PWRM_26

### TestCase Objective
Verify addPowerModePreChangeClient with valid clientName returns a non-null integer clientId, then clean up

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager with clientName: "TDKTestClient"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient", "params": {"clientName": "TDKTestClient"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that power mode pre change client is registered successfully |
| 2 | Remove power mode pre change client | Invoke removePowerModePreChangeClient on org.rdk.PowerManager with clientId: "<result_step_1>" (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.removePowerModePreChangeClient", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

---

<a id="powermanager_powermodeprechange_lifecycle_event"></a>
### TestCase Name
PowerManager_PowerModePreChange_Lifecycle_Event

### TestCase ID
PWRM_27

### TestCase Objective
Check onPowerModePreChange lifecycle for when a client is added, power state is set to STANDBY, onPowerModePreChange event is received, pre-change is completed, and client is removed

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager with clientName: "TDKPreChangeLifecycle"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient", "params": {"clientName": "TDKPreChangeLifecycle"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that power mode pre change client is registered successfully |
| 2 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "STANDBY", reason: "TDKPreChangeTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "STANDBY", "reason": "TDKPreChangeTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Listen for power mode pre change event | Listen for `Event_On_PowerMode_PreChange` event and wait up to 2 second(s) | Verify that the event is received and validated successfully |
| 4 | Power mode pre change complete | Invoke powerModePreChangeComplete on org.rdk.PowerManager with clientId: "<result_step_1>", transactionId: "<result_step_3>" (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.powerModePreChangeComplete", "params": {"clientId": "<result_step_1>", "transactionId": "<result_step_3>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Remove power mode pre change client | Invoke removePowerModePreChangeClient on org.rdk.PowerManager with clientId: "<result_step_1>" (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.removePowerModePreChangeClient", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_lifecycle_prechangeclient_delay_complete"></a>
### TestCase Name
PowerManager_Lifecycle_PreChangeClient_Delay_Complete

### TestCase ID
PWRM_28

### TestCase Objective
Register pre-change client, delay power mode change, signal complete, then remove client

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager with clientName: "TDKPreChangeLifecycle"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient", "params": {"clientName": "TDKPreChangeLifecycle"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that power mode pre change client is registered successfully |
| 2 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "STANDBY", reason: "TDKPreChangeTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "STANDBY", "reason": "TDKPreChangeTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Listen for power mode pre change event | Listen for `Event_On_PowerMode_PreChange` event and wait up to 2 second(s) | Verify that the event is received and validated successfully |
| 4 | Delay power mode change by | Invoke delayPowerModeChangeBy on org.rdk.PowerManager with clientId: "<result_step_1>", transactionId: "<result_step_3>", delayPeriod: "<result_step_3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.delayPowerModeChangeBy", "params": {"clientId": "<result_step_1>", "transactionId": "<result_step_3>", "delayPeriod": "<result_step_3>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 5 | Power mode pre change complete | Invoke powerModePreChangeComplete on org.rdk.PowerManager with clientId: "<result_step_1>", transactionId: "<result_step_3>" (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.powerModePreChangeComplete", "params": {"clientId": "<result_step_1>", "transactionId": "<result_step_3>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Remove power mode pre change client | Invoke removePowerModePreChangeClient on org.rdk.PowerManager with clientId: "<result_step_1>" (wait 2 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.removePowerModePreChangeClient", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

### TestCase Post-condition

#### TestCase Post-condition 1: Restore_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Power State | Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Restore Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "ON", "reason": "TDKRestore"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Verify Power State ON | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_multistep_powerstate_cycle"></a>
### TestCase Name
PowerManager_MultiStep_PowerState_Cycle

### TestCase ID
PWRM_29

### TestCase Objective
Check power state transitions through STANDBY, LIGHT_SLEEP, and ON with verification after each step

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.PowerManager with keyCode: 0, powerState: "STANDBY", reason: "TDKCycleTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"keyCode": 0, "powerState": "STANDBY", "reason": "TDKCycleTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Get power state | Invoke getPowerState on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `STANDBY` |
| 3 | Set power state | Invoke setPowerState on org.rdk.PowerManager with keyCode: 0, powerState: "LIGHT_SLEEP", reason: "TDKCycleTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"keyCode": 0, "powerState": "LIGHT_SLEEP", "reason": "TDKCycleTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Get power state | Invoke getPowerState on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `LIGHT_SLEEP` |
| 5 | Set power state | Invoke setPowerState on org.rdk.PowerManager with keyCode: 0, powerState: "ON", reason: "TDKCycleTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"keyCode": 0, "powerState": "ON", "reason": "TDKCycleTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 6 | Get power state | Invoke getPowerState on org.rdk.PowerManager (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the expected value `ON` |

---

<a id="powermanager_setnetworkstandbymode_invalid_type"></a>
### TestCase Name
PowerManager_SetNetworkStandbyMode_Invalid_Type

### TestCase ID
PWRM_30

### TestCase Objective
Verify setNetworkStandbyMode with string type 'yes' instead of bool returns an error response

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.PowerManager with standbyMode: "yes"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setNetworkStandbyMode", "params": {"standbyMode": "yes"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_settemperaturethresholds_invalid_hightype"></a>
### TestCase Name
PowerManager_SetTemperatureThresholds_Invalid_HighType

### TestCase ID
PWRM_31

### TestCase Objective
Verify setTemperatureThresholds with non-numeric string for high param returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set temperature thresholds | Invoke setTemperatureThresholds on org.rdk.PowerManager with high: "hot", critical: 100.0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setTemperatureThresholds", "params": {"high": "hot", "critical": 100.0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_settemperaturethresholds_missing_critical"></a>
### TestCase Name
PowerManager_SetTemperatureThresholds_Missing_Critical

### TestCase ID
PWRM_32

### TestCase Objective
Verify setTemperatureThresholds with missing required critical parameter returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set temperature thresholds | Invoke setTemperatureThresholds on org.rdk.PowerManager with high: 60.0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setTemperatureThresholds", "params": {"high": 60.0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_setwakeupsourceconfig_invalid_wakeupsource"></a>
### TestCase Name
PowerManager_SetWakeupSourceConfig_Invalid_WakeupSource

### TestCase ID
PWRM_33

### TestCase Objective
Verify setWakeupSourceConfig with unrecognized wakeupSource enum 'INVALID_SOURCE' returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set wakeup source config | Invoke setWakeupSourceConfig on org.rdk.PowerManager with wakeupSource: "INVALID_SOURCE", enabled: "true"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setWakeupSourceConfig", "params": {"wakeupSource": "INVALID_SOURCE", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_setwakeupsourceconfig_missing_enabled_param"></a>
### TestCase Name
PowerManager_SetWakeupSourceConfig_Missing_Enabled_Param

### TestCase ID
PWRM_34

### TestCase Objective
Verify setWakeupSourceConfig with missing enabled field returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set wakeup source config | Invoke setWakeupSourceConfig on org.rdk.PowerManager with wakeupSource: "<POWERMANAGER_WAKEUP_SOURCE_CONFIG>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setWakeupSourceConfig", "params": {"wakeupSource": "<POWERMANAGER_WAKEUP_SOURCE_CONFIG>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_setovertempgraceinterval_negative_value"></a>
### TestCase Name
PowerManager_SetOvertempGraceInterval_Negative_Value

### TestCase ID
PWRM_35

### TestCase Objective
Verify setOvertempGraceInterval with negative graceInterval (-100) returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set overtemp grace interval | Invoke setOvertempGraceInterval on org.rdk.PowerManager with graceInterval: -100<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setOvertempGraceInterval", "params": {"graceInterval": -100}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `Invalid Parameter` |

---

<a id="powermanager_addprechangeclient_emptyclientname"></a>
### TestCase Name
PowerManager_AddPreChangeClient_EmptyClientName

### TestCase ID
PWRM_36

### TestCase Objective
Verify addPowerModePreChangeClient with empty string clientName returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager with clientName: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient", "params": {"clientName": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `Invalid Parameter` |

---

<a id="powermanager_addprechangeclient_no_params"></a>
### TestCase Name
PowerManager_AddPreChangeClient_No_Params

### TestCase ID
PWRM_37

### TestCase Objective
Verify addPowerModePreChangeClient with no parameters (missing required clientName) returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `Invalid Parameter` |

---

<a id="powermanager_removeprechangeclient_invalid_id"></a>
### TestCase Name
PowerManager_RemovePreChangeClient_Invalid_Id

### TestCase ID
PWRM_38

### TestCase Objective
Verify removePowerModePreChangeClient with invalid clientId (-1) returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Remove power mode pre change client | Invoke removePowerModePreChangeClient on org.rdk.PowerManager with clientId: -1<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.removePowerModePreChangeClient", "params": {"clientId": -1}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `Invalid Parameter` |

---

<a id="powermanager_prechangecomplete_invalid_clientid"></a>
### TestCase Name
PowerManager_PreChangeComplete_Invalid_ClientId

### TestCase ID
PWRM_39

### TestCase Objective
Verify powerModePreChangeComplete with unregistered clientIdreturns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Power mode pre change complete | Invoke powerModePreChangeComplete on org.rdk.PowerManager with clientId: 9999, transactionId: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.powerModePreChangeComplete", "params": {"clientId": 9999, "transactionId": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `Invalid Parameter` |

---

<a id="powermanager_delaypowermodechange_invalid_clientid"></a>
### TestCase Name
PowerManager_DelayPowerModeChange_Invalid_ClientId

### TestCase ID
PWRM_40

### TestCase Objective
Verify delayPowerModeChangeBy with unregistered clientId 9999 returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delay power mode change by | Invoke delayPowerModeChangeBy on org.rdk.PowerManager with clientId: 9999, transactionId: 0, delayPeriod: 5<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.delayPowerModeChangeBy", "params": {"clientId": 9999, "transactionId": 0, "delayPeriod": 5}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_errorstate_prechangecomplete_after_remove"></a>
### TestCase Name
PowerManager_ErrorState_PreChangeComplete_After_Remove

### TestCase ID
PWRM_41

### TestCase Objective
Verify powerModePreChangeComplete with removed clientId returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Add power mode pre change client | Invoke addPowerModePreChangeClient on org.rdk.PowerManager with clientName: "TDKTestClient"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.addPowerModePreChangeClient", "params": {"clientName": "TDKTestClient"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that power mode pre change client is registered successfully |
| 2 | Remove power mode pre change client | Invoke removePowerModePreChangeClient on org.rdk.PowerManager with clientId: "<result_step_1>" (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.removePowerModePreChangeClient", "params": {"clientId": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Power mode pre change complete | Invoke powerModePreChangeComplete on org.rdk.PowerManager with clientId: "<result_step_1>", transactionId: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.powerModePreChangeComplete", "params": {"clientId": "<result_step_1>", "transactionId": 0}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_setpowerstate_invalid_state"></a>
### TestCase Name
PowerManager_SetPowerState_Invalid_State

### TestCase ID
PWRM_42

### TestCase Objective
Verify setPowerState with invalid powerState value returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: "INVALID_STATE", reason: "TDKAPITest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": "INVALID_STATE", "reason": "TDKAPITest"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_setpowerstate_negative_value"></a>
### TestCase Name
PowerManager_SetPowerState_Negative_Value

### TestCase ID
PWRM_43

### TestCase Objective
Verify setPowerState with negative powerState value (-1) returns an error

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.PowerManager with powerState: -1, reason: "TDKAPITest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.setPowerState", "params": {"powerState": -1, "reason": "TDKAPITest"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error: `ERROR_GENERAL` |

---

<a id="powermanager_activatedeactivate_statechange_event_test"></a>
### TestCase Name
PowerManager_ActivateDeactivate_StateChange_Event_Test

### TestCase ID
PWRM_44

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_PowerManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate power manager plugin | Invoke deactivate on Controller with callsign: "org.rdk.PowerManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 2 | Listen for event controller state changed event | Listen for `Event_Controller_State_Changed` event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `org.rdk.powermanager` with state `deactivated` |
| 3 | Check plugin active status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate power manager plugin | Invoke activate on Controller with callsign: "org.rdk.PowerManager" (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Listen for event controller state changed event | Listen for `Event_Controller_State_Changed` event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `org.rdk.powermanager` with state `activated` |
| 6 | Check plugin active status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="powermanager_activatedeactivate_all_event_test"></a>
### TestCase Name
PowerManager_ActivateDeactivate_All_Event_Test

### TestCase ID
PWRM_45

### TestCase Objective
Validates all event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_PowerManager_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PowerManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate power manager plugin | Invoke deactivate on Controller with callsign: "org.rdk.PowerManager"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 2 | Listen for event controller all event | Listen for `Event_Controller_All` event and wait up to 2 second(s) | Verify that the `all` event is received for callsign `org.rdk.powermanager` with state `deactivated` |
| 3 | Check plugin active status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate power manager plugin | Invoke activate on Controller with callsign: "org.rdk.PowerManager" (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.PowerManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Listen for event controller all event | Listen for `Event_Controller_All` event and wait up to 2 second(s) | Verify that the `all` event is received for callsign `org.rdk.powermanager` with state `activated` |
| 6 | Check plugin active status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.PowerManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="powermanager_powerstate_before_reboot_persistence"></a>
### TestCase Name
PowerManager_PowerState_Before_Reboot_Persistence

### TestCase ID
PWRM_46

### TestCase Objective
Verify getPowerStateBeforeReboot returns a valid power state after reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state before reboot | Invoke getPowerStateBeforeReboot on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state before reboot is returned successfully |
| 2 | Reboot device | Invoke reboot on org.rdk.PowerManager with rebootRequestor: "TDK", rebootReasonCustom: "TDKAPITest", rebootReasonOther: "TDK API Validation"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.reboot", "params": {"rebootRequestor": "TDK", "rebootReasonCustom": "TDKAPITest", "rebootReasonOther": "TDK API Validation"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Listen for reboot begin event | Listen for `Event_On_Reboot_Begin` event | Verify that the event is received and validated successfully |
| 4 | Wait for device to come up | Wait for device to come up on the device | Device should come up online within the expected time and plugin pre-requisites should be restored successfully |
| 5 | Get power state before reboot | Invoke getPowerStateBeforeReboot on org.rdk.PowerManager<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and powermanager get power state before reboot matches value from step 1 |

## Plugin Post-conditions

### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onPowerModeChanged event | Unregister the WebSocket event listener for `onPowerModeChanged` to stop receiving `onPowerModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.unregister", "params": {"event": "onPowerModeChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the onPowerModePreChange event | Unregister the WebSocket event listener for `onPowerModePreChange` to stop receiving `onPowerModePreChange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.unregister", "params": {"event": "onPowerModePreChange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the onNetworkStandbyModeChanged event | Unregister the WebSocket event listener for `onNetworkStandbyModeChanged` to stop receiving `onNetworkStandbyModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.unregister", "params": {"event": "onNetworkStandbyModeChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 4 | Unsubscribe from the onRebootBegin event | Unregister the WebSocket event listener for `onRebootBegin` to stop receiving `onRebootBegin` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.unregister", "params": {"event": "onRebootBegin", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 5 | Unsubscribe from the onThermalModeChanged event | Unregister the WebSocket event listener for `onThermalModeChanged` to stop receiving `onThermalModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.PowerManager.1.unregister", "params": {"event": "onThermalModeChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 6 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 7 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop receiving `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M152

<div align="right"><a href="#testscript-name">Go to Top</a></div>
