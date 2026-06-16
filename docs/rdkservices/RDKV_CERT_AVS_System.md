## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [System_Get_ESTB_MAC (SYS_01)](#system_get_estb_mac-sys_01)
   - [System_Get_Serial_Number (SYS_02)](#system_get_serial_number-sys_02)
   - [System_Get_Version (SYS_03)](#system_get_version-sys_03)
   - [System_Get_Uptime (SYS_04)](#system_get_uptime-sys_04)
   - [System_Get_RFC_Config (SYS_05)](#system_get_rfc_config-sys_05)
   - [System_SetAndGet_Power_State (SYS_06)](#system_setandget_power_state-sys_06)
   - [System_SetAndGet_TimeZone_DST (SYS_07)](#system_setandget_timezone_dst-sys_07)
   - [System_Set_NORMAL_Mode (SYS_08)](#system_set_normal_mode-sys_08)
   - [System_GetMac_Address (SYS_09)](#system_getmac_address-sys_09)
   - [System_Get_Image_Version (SYS_10)](#system_get_image_version-sys_10)
   - [System_Get_model_number (SYS_11)](#system_get_model_number-sys_11)
   - [System_Get_boxIP (SYS_12)](#system_get_boxip-sys_12)
   - [System_Get_build_type (SYS_13)](#system_get_build_type-sys_13)
   - [System_Get_eth_mac (SYS_14)](#system_get_eth_mac-sys_14)
   - [System_Get_rf4ce_mac (SYS_15)](#system_get_rf4ce_mac-sys_15)
   - [System_Get_Bluetooth_mac (SYS_16)](#system_get_bluetooth_mac-sys_16)
   - [System_Get_WiFi_Mac (SYS_17)](#system_get_wifi_mac-sys_17)
   - [Check_Power_State_Before_Reboot (SYS_18)](#check_power_state_before_reboot-sys_18)
   - [System_Check_On_SystemMode_Changed (SYS_19)](#system_check_on_systemmode_changed-sys_19)
   - [System_Check_Reboot_Reason_Event (SYS_20)](#system_check_reboot_reason_event-sys_20)
   - [Enable_And_Disable_Telemetry_OptOut_Status (SYS_21)](#enable_and_disable_telemetry_optout_status-sys_21)
   - [System_Validate_Firmware_Upgrade (SYS_22)](#system_validate_firmware_upgrade-sys_22)
   - [System_Check_Model_Number (SYS_23)](#system_check_model_number-sys_23)
   - [System_Check_Device_Mac_Address (SYS_24)](#system_check_device_mac_address-sys_24)
   - [System_Check_Firmware_Upgrade_Status (SYS_25)](#system_check_firmware_upgrade_status-sys_25)
   - [System_Check_Public_IP_Address (SYS_26)](#system_check_public_ip_address-sys_26)
   - [System_Check_HDR_Capabilities (SYS_27)](#system_check_hdr_capabilities-sys_27)
   - [SetAndGet_All_Time_Zones (SYS_28)](#setandget_all_time_zones-sys_28)
   - [System_Toggle_Network_Standby_Mode_Status (SYS_29)](#system_toggle_network_standby_mode_status-sys_29)
   - [Check_Power_State_Before_Reboot_On_Standby_State (SYS_30)](#check_power_state_before_reboot_on_standby_state-sys_30)
   - [Check_Time_Zones_Persist_After_Reboot (SYS_31)](#check_time_zones_persist_after_reboot-sys_31)
   - [System_Reboot_And_Check_System_Uptime (SYS_32)](#system_reboot_and_check_system_uptime-sys_32)
   - [System_Check_On_TimeZoneDST_Changed_Event (SYS_33)](#system_check_on_timezonedst_changed_event-sys_33)
   - [System_Check_RFC_Status (SYS_34)](#system_check_rfc_status-sys_34)
   - [System_SetandGet_Friendly_Name (SYS_35)](#system_setandget_friendly_name-sys_35)
   - [System_Check_Friendly_Name_Persist (SYS_36)](#system_check_friendly_name_persist-sys_36)
   - [System_Set_Invalid_TimeZone_DST (SYS_37)](#system_set_invalid_timezone_dst-sys_37)
   - [System_Check_RFCList_with_Empty_Value (SYS_38)](#system_check_rfclist_with_empty_value-sys_38)
   - [System_Check_Device_Type (SYS_39)](#system_check_device_type-sys_39)
   - [System_Check_Device_SSH_State_After_Reboot_On_Standby_State (SYS_40)](#system_check_device_ssh_state_after_reboot_on_standby_state-sys_40)
   - [System_Set_Invalid_Territory_And_Region (SYS_41)](#system_set_invalid_territory_and_region-sys_41)
   - [System_Set_Empty_Territory_And_Region (SYS_42)](#system_set_empty_territory_and_region-sys_42)
   - [System_Set_Invalid_Territory_And_Valid_Region (SYS_43)](#system_set_invalid_territory_and_valid_region-sys_43)
   - [System_Set_Empty_Territory_And_Valid_Region (SYS_44)](#system_set_empty_territory_and_valid_region-sys_44)
   - [System_Set_And_Get_Territory_Region (SYS_45)](#system_set_and_get_territory_region-sys_45)
   - [System_Verify_Set_Territory_without_Params (SYS_46)](#system_verify_set_territory_without_params-sys_46)
   - [System_Set_Valid_Territory_And_Set_Invalid_Region (SYS_47)](#system_set_valid_territory_and_set_invalid_region-sys_47)
   - [System_Set_Valid_Territory_And_Set_Empty_Region (SYS_48)](#system_set_valid_territory_and_set_empty_region-sys_48)
   - [System_Get_Mfg_Serial_Number (SYS_49)](#system_get_mfg_serial_number-sys_49)
   - [System_ActivateDeactivate_Event_Test (SYS_50)](#system_activatedeactivate_event_test-sys_50)
   - [System_Invalid_Set_Mode (SYS_51)](#system_invalid_set_mode-sys_51)
   - [System_SetandGet_Empty_Friendly_Name (SYS_52)](#system_setandget_empty_friendly_name-sys_52)
   - [System_Invalid_Set_Power_State (SYS_53)](#system_invalid_set_power_state-sys_53)
   - [System_Invalid_TimeZone_ErrorValidation (SYS_54)](#system_invalid_timezone_errorvalidation-sys_54)
   - [System_Invalid_Key_ErrorMessage (SYS_55)](#system_invalid_key_errormessage-sys_55)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **System** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.System` (version 1)

**API Coverage**

- **State / Query APIs**: `getAvailableStandbyModes`, `getCachedValue`, `getCoreTemperature`, `getDeviceInfo`, `getDownloadedFirmwareInfo`, `getFriendlyName`, `getLastDeepSleepReason`, `getMacAddresses`, `getMfgSerialNumber`, `getMilestones`, `getMode`, `getNetworkStandbyMode`, `getOvertempGraceInterval`, `getPlatformConfiguration`, `getPowerState`, `getPowerStateBeforeReboot`, `getPowerStateIsManagedByDevice`, `getPreferredStandbyMode`, `getPreviousRebootInfo`, `getPreviousRebootInfo2`, `getPreviousRebootReason`, `getRFCConfig`, `getSerialNumber`, `getStateInfo`, `getSystemVersions`, `getTemperatureThresholds`, `getTerritory`, `getTimeZoneDST`, `getTimeZones`, `getXconfParams`, `hasRebootBeenRequested`, `isGzEnabled`, `isOptOutTelemetry`
- **Configuration APIs**: `clearLastDeepSleepReason`, `deletePersistentPath`, `enableMoca`, `removeCacheKey`, `setCachedValue`, `setFriendlyName`, `setGzEnabled`, `setMode`, `setNetworkStandbyMode`, `setOptOutTelemetry`, `setOvertempGraceInterval`, `setPowerState`, `setPreferredStandbyMode`, `setTemperatureThresholds`, `setTerritory`, `setTimeZoneDST`, `updateFirmware`
- **Events**: `onFriendlyNameChanged`, `onMacAddressesRetreived`, `onNetworkStandbyModeChanged`, `onRebootRequest`, `onSystemModeChanged`, `onSystemPowerStateChanged`, `onTemperatureThresholdChanged`, `onTerritoryChanged`, `onTimeZoneDSTChanged`
- **Other APIs**: `cacheContains`, `queryMocaStatus`, `reboot`, `requestSystemUptime`

### APIs Under Test

| API | Description |
|-----|-------------|
| `cacheContains` | Checks if key is present in cache |
| `clearLastDeepSleepReason` | Clear the last deep sleep reason. |
| `deletePersistentPath` | Deletes the persistent path |
| `enableMoca` | Enables or disables Moca support for the platform |
| `getAvailableStandbyModes` | Get available standby modes |
| `getCachedValue` | Get value of the key in cache |
| `getCoreTemperature` | Gives core temperature of the device |
| `getDeviceInfo` | Gives device details |
| `getDownloadedFirmwareInfo` | Returns information about firmware downloads |
| `getFriendlyName` | Returns the friendly name set by setFriendlyName API or default value |
| `getLastDeepSleepReason` | Retrieve the last deep sleep reason. |
| `getMacAddresses` | Retrieve the mac addresses. |
| `getMfgSerialNumber` | Gets the manufacturing serial number |
| `getMilestones` | Gives list of milestones |
| `getMode` | Gets currently set mode |
| `getNetworkStandbyMode` | Returns the network standby mode of the device |
| `getOvertempGraceInterval` | Returns the over-temperature grace interval value |
| `getPlatformConfiguration` | Returns the supported features and device/account info |
| `getPowerState` | Get power state |
| `getPowerStateBeforeReboot` | Gets the power state before reboot |
| `getPowerStateIsManagedByDevice` | Checks whether the power state is managed by the device |
| `getPreferredStandbyMode` | Get preferred standby mode |
| `getPreviousRebootInfo` | Retrieve basic information about a reboot |
| `getPreviousRebootInfo2` | Retrieve detailed information about a reboot |
| `getPreviousRebootReason` | Retrieve the last reboot reason. |
| `getRFCConfig` | Gets RFC configurations |
| `getSerialNumber` | Gives device serial number |
| `getStateInfo` | Query device state information of various properties |
| `getSystemVersions` | Gives system version details |
| `getTemperatureThresholds` | Gets temperature thresholds |
| `getTerritory` | Gets the configured system territory and region.  |
| `getTimeZoneDST` | Get configured time zone |
| `getTimeZones` | Gets the available timezones from the system's time zone database |
| `getXconfParams` | Gives Xconf configuration of the device |
| `hasRebootBeenRequested` | Check whether a reboot has been requested. |
| `isGzEnabled` | Gives GZ enabled status |
| `isOptOutTelemetry` | Checks the telemetry opt-out status |
| `queryMocaStatus` | Check whether Moca is enabled |
| `reboot` | system perform a reboot of the set-top box |
| `removeCacheKey` | Remove key from cache |
| `requestSystemUptime` | Gives system uptime |
| `setCachedValue` | Set value of the key in cache |
| `setFriendlyName` | Sets the friendly name of the device |
| `setGzEnabled` | Sets GZ enabled status  |
| `setMode` | Set mode for specific duration |
| `setNetworkStandbyMode` | Enables or disables the network standby mode of the device |
| `setOptOutTelemetry` | Sets the telemetry opt-out status |
| `setOvertempGraceInterval` | Sets the over-temperature grace interval value |
| `setPowerState` | Set power state |
| `setPreferredStandbyMode` | Set preferred standby mode |
| `setTemperatureThresholds` | Sets temperature thresholds |
| `setTerritory` | Sets the system territory and region |
| `setTimeZoneDST` | Set configured time zone |
| `updateFirmware` | Initiates a firmware update |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onFriendlyNameChanged` | Triggered when the device friendly name change |
| `onMacAddressesRetreived` | MacAddressesRetreived |
| `onNetworkStandbyModeChanged` | Triggered when the network standby mode setting changes |
| `onRebootRequest` | Fires on reboot request |
| `onSystemModeChanged` | Fires on system mode changed event |
| `onSystemPowerStateChanged` | power state changed event |
| `onTemperatureThresholdChanged` | Fires on temperature threshold change |
| `onTerritoryChanged` | Triggered when the device territory changed |
| `onTimeZoneDSTChanged` | Triggered when device timezone changed |

---

## Pre-conditions

### Pre-condition 1: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_MacAddresses_Retreived` on `System` plugin

- Register and listen to event `Event_PowerState_Changed` on `System` plugin

- Register and listen to event `Event_SystemMode_Changed` on `System` plugin

- Register and listen to event `Event_Reboot_Request` on `System` plugin

- Register and listen to event `Event_On_Network_Standby_Mode_Changed` on `System` plugin

- Register and listen to event `Event_On_TimeZoneDST_Changed` on `System` plugin

- Register and listen to event `Event_On_Friendly_Name_Changed` on `System` plugin

- Register and listen to event `Event_On_Territory_Changed` on `System` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="system_get_estb_mac-sys_01"></a>
### System_Get_ESTB_MAC (SYS_01)

**Objective:** Get requested device detail

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device ESTB MAC | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"<SYSTEM_DEVICE_PARAMS>"` (value read from device config file)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Device info response for `<SYSTEM_DEVICE_PARAMS>` is returned successfully and the value must not be empty |

---

<a id="system_get_serial_number-sys_02"></a>
### System_Get_Serial_Number (SYS_02)

**Objective:** Gets the serial number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Serial No | Invoke `getSerialNumber` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Serial Number returned successfully |

---

<a id="system_get_version-sys_03"></a>
### System_Get_Version (SYS_03)

**Objective:** Gets system version details

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Version | Invoke `getSystemVersions` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSystemVersions"}' http://127.0.0.1:9998/jsonrpc` | System Versions returned successfully |

---

<a id="system_get_uptime-sys_04"></a>
### System_Get_Uptime (SYS_04)

**Objective:** Gets system version details

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Uptime | Invoke `requestSystemUptime` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | The uptime value should be returned and must not be empty |

---

<a id="system_get_rfc_config-sys_05"></a>
### System_Get_RFC_Config (SYS_05)

**Objective:** Gets RFC configurations

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System RFC Config | Invoke `getRFCConfig` on `org.rdk.System` with `rfcList`: `"<SYSTEM_RFC_PARAMS>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | RFC config returned successfully |

---

<a id="system_setandget_power_state-sys_06"></a>
### System_SetAndGet_Power_State (SYS_06)

**Objective:** Set and get device power state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke `getPowerState` on `org.rdk.System` to retrieve the current power state before setting<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Current power state is returned successfully and must be one of: `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"APIUnitTest"`, `powerState`: `"STANDBY"` (switched from value retrieved in step 1)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power state set to `STANDBY` successfully |
| 3 | Power State Changed Event | Listen for event `onSystemPowerStateChanged` (wait up to 30 seconds) | Event `onSystemPowerStateChanged` is received with new state matching `STANDBY` (the value set in step 2) |
| 4 | Get Power State | Invoke `getPowerState` on `org.rdk.System` to verify the state was applied<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power state returned is `STANDBY`, confirming the set operation in step 2 was successful |

**Post-condition:**

#### Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Power State | Invoke `getPowerState` on `org.rdk.System` to check current state before reverting<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Current power state is returned successfully and must be one of: `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"APIUnitTest"`, `powerState`: `"ON"` to revert device to original state<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power state reverted to `ON` successfully |
| 3 | Check Power State | Invoke `getPowerState` on `org.rdk.System` to confirm revert was successful<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power state returned is `ON`, confirming device is restored to original state |

---

<a id="system_setandget_timezone_dst-sys_07"></a>
### System_SetAndGet_TimeZone_DST (SYS_07)

**Objective:** Set and get DST time zone

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke `setTimeZoneDST` on `org.rdk.System` with `timeZone`: `"America/New_York"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "America/New_York"}}' http://127.0.0.1:9998/jsonrpc` | Time Zone D S T set successfully |
| 2 | Get TimeZone DST | Invoke `getTimeZoneDST` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Expected: `America/New_York` |

---

<a id="system_set_normal_mode-sys_08"></a>
### System_Set_NORMAL_Mode (SYS_08)

**Objective:** Set STB mode to NORMAL

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set STB Mode NORMAL | Invoke `setMode` on `org.rdk.System` with `duration`: `"<value>"`, `mode`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": "<value>", "mode": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Mode set successfully |

---

<a id="system_getmac_address-sys_09"></a>
### System_GetMac_Address (SYS_09)

**Objective:** Get Mac Address

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get MacAddress | Invoke `getMacAddresses` on `org.rdk.System` with `GUID`: `"61734787891723481"` (default GUID value)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMacAddresses", "params": {"GUID": "61734787891723481"}}' http://127.0.0.1:9998/jsonrpc` | `asyncResponse` is `true` and `success` is `true`, confirming the async MAC address retrieval was triggered successfully |
| 2 | Check Mac Address | Listen for event `onMacAddressesRetrieved` (wait up to 2 seconds for async response) | Event is received and all MAC address fields (`ECM_MAC`, `ESTB_MAC`, `MOCA_MAC`, `ETH_MAC`, `WIFI_MAC`, `BLUETOOTH_MAC`, `RF4CE_MAC`) are validated against the pattern `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` each non-zero MAC must match a valid format |

---

<a id="system_get_image_version-sys_10"></a>
### System_Get_Image_Version (SYS_10)

**Objective:** Gets the image version

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Image Version | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"imageVersion"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "imageVersion"}}' http://127.0.0.1:9998/jsonrpc` | `imageVersion` is returned successfully and must not be empty |

---

<a id="system_get_model_number-sys_11"></a>
### System_Get_model_number (SYS_11)

**Objective:** Gets the model number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device model number | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"model_number"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "model_number"}}' http://127.0.0.1:9998/jsonrpc` | `model_number` is returned successfully and must not be empty |

---

<a id="system_get_boxip-sys_12"></a>
### System_Get_boxIP (SYS_12)

**Objective:** Gets the box IP

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device boxIP | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"boxIP"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "boxIP"}}' http://127.0.0.1:9998/jsonrpc` | `boxIP` value is returned successfully and must not be empty |

---

<a id="system_get_build_type-sys_13"></a>
### System_Get_build_type (SYS_13)

**Objective:** Gets the build type

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device build type | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"build_type"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "build_type"}}' http://127.0.0.1:9998/jsonrpc` | `build_type` value is returned successfully and must not be empty |

---

<a id="system_get_eth_mac-sys_14"></a>
### System_Get_eth_mac (SYS_14)

**Objective:** Gets eth mac of the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device eth mac | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"eth_mac"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "eth_mac"}}' http://127.0.0.1:9998/jsonrpc` | `eth_mac` value is returned and validated against MAC format: `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="system_get_rf4ce_mac-sys_15"></a>
### System_Get_rf4ce_mac (SYS_15)

**Objective:** Gets the rf4ce mac of the device

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device rf4ce mac | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"rf4ce_mac"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "rf4ce_mac"}}' http://127.0.0.1:9998/jsonrpc` | `rf4ce_mac` value is returned successfully and must not be empty (8-byte RF4CE MAC format) |

---

<a id="system_get_bluetooth_mac-sys_16"></a>
### System_Get_Bluetooth_mac (SYS_16)

**Objective:** Gets device bluetooth mac

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Bluetooth Mac | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"bluetooth_mac"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "bluetooth_mac"}}' http://127.0.0.1:9998/jsonrpc` | `bluetooth_mac` value is returned and validated against MAC format: `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="system_get_wifi_mac-sys_17"></a>
### System_Get_WiFi_Mac (SYS_17)

**Objective:** Gets device WiFi mac

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device WiFi Mac | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"wifi_mac"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "wifi_mac"}}' http://127.0.0.1:9998/jsonrpc` | `wifi_mac` value is returned and validated against MAC format: `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="check_power_state_before_reboot-sys_18"></a>
### Check_Power_State_Before_Reboot (SYS_18)

**Objective:** Checks the powerstate before reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke `getPowerState` on `org.rdk.System` to record current state before reboot<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Current power state returned successfully and must be one of: `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` saved for comparison in step 3 |
| 2 | System reboot | Invoke `reboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 3 | Get Power State Before Reboot | Invoke `getPowerStateBeforeReboot` on `org.rdk.System` after device reconnects<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Power state before reboot matches the state recorded in step 1 |

---

<a id="system_check_on_systemmode_changed-sys_19"></a>
### System_Check_On_SystemMode_Changed (SYS_19)

**Objective:** Checks for the system mode changed event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set STB Mode WAREHOUSE | Invoke `setMode` on `org.rdk.System` with `duration`: `5`, `mode`: `"WAREHOUSE"` (mode auto-reverts to `NORMAL` after 5 seconds)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": 5, "mode": "WAREHOUSE"}}' http://127.0.0.1:9998/jsonrpc` | Mode set to `WAREHOUSE` successfully (`success: true`) |
| 2 | Check On SystemMode Changed Event | Listen for event `onSystemModeChanged` (triggered immediately when mode is set to WAREHOUSE) | Event received with `mode`: `"WAREHOUSE"` |
| 3 | Check On SystemMode Changed Event | Listen for event `onSystemModeChanged` (wait up to 5 seconds for auto-revert) | Event received with `mode`: `"NORMAL"` confirming automatic revert after duration expires |

---

<a id="system_check_reboot_reason_event-sys_20"></a>
### System_Check_Reboot_Reason_Event (SYS_20)

**Objective:** Retrieve basic information about a reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System reboot | Invoke `reboot` on `org.rdk.System` with `rebootReason`: `"API Validation"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot", "params": {"rebootReason": "API Validation"}}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 2 | Check On Reboot Request Event | Listen for event `onRebootRequest` (wait up to 60 seconds) | Event received with `rebootReason`: `"API Validation"` and `requestedApp`: `"SystemServices"` |

---

<a id="enable_and_disable_telemetry_optout_status-sys_21"></a>
### Enable_And_Disable_Telemetry_OptOut_Status (SYS_21)

**Objective:** Checks whether able to enable and disable the telemetry opt-out status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OptOut Telemetry Status | Invoke `isOptOutTelemetry` on `org.rdk.System` to retrieve current opt-out status before modification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | `optOut` status returned successfully as `true` or `false` — saved for revert |
| 2 | Set OptOut Telemetry Status | Invoke `setOptOutTelemetry` on `org.rdk.System` with `Opt-Out`: `true` (first iteration), then `false` (second iteration)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setOptOutTelemetry", "params": {"Opt-Out": true}}' http://127.0.0.1:9998/jsonrpc` | Telemetry opt-out status set successfully (`success: true`) for each iteration |
| 3 | Get OptOut Telemetry Status | Invoke `isOptOutTelemetry` on `org.rdk.System` after each set to verify<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | `optOut` value matches the value set in step 2 for the current iteration (`true` then `false`) |

---

<a id="system_validate_firmware_upgrade-sys_22"></a>
### System_Validate_Firmware_Upgrade (SYS_22)

**Objective:** Upgrades to specified firmware version

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Version File | SSH to device: verify `/version.txt` exists (`[ -f "/version.txt" ] && echo 1 \|\| echo 0`) and is not empty (`[ -s "/version.txt" ] && echo 1 \|\| echo 0`) before the firmware upgrade test begins | `/version.txt` file exists and is not empty on the device |
| 2 | Get Downloaded Firmware Info | Invoke `getDownloadedFirmwareInfo` on `org.rdk.System` — records the current running firmware version as the baseline; this value is used in step 25 to verify successful revert to the original firmware<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Current firmware version returned successfully and saved |
| 3 | Get Model Name | SSH read `model_number` from device details cache file `<SYSTEM_DEVICE_DETAILS_FILE_PATH>`: `grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs` model string saved for XCONF rule targeting | Model number read from device cache file successfully and saved |
| 4 | Check Existing Model ID | Query XCONF REST API: `GET /xconfAdminService/queries/models/TDK_{MODEL}_TEST_MODEL` using model from step 3 checks whether a model ID entry already exists for this device | XCONF query executed successfully existing model ID returned and saved (or `null` if not found — triggers step 5) |
| 5 | Create New Model ID | **Conditional** (step 4 = no existing model ID) — Create model ID rule in XCONF: `POST /xconfAdminService/updates/models` with model name from step 3 | New model ID rule `TDK_{MODEL}_TEST_MODEL` created in XCONF successfully (step skipped if model ID already existed in step 4) |
| 6 | Check Existing Firmware Configuration | Query XCONF REST API: `GET /xconfAdminService/queries/firmwares/model/TDK_{MODEL}_TEST_MODEL?applicationType=stb` — checks whether a firmware configuration already exists for this model | XCONF query executed; existing firmware configuration returned and saved (or empty — triggers step 7) |
| 7 | Create New Firmware Configuration | **Conditional** (step 6 = no existing firmware config) — Create firmware configuration in XCONF: `POST /xconfAdminService/updates/firmwares` linking model to target firmware `<FIRMWARE_VERSION>` | New firmware configuration `TDK_{MODEL}_TEST_FIRMWARE_CONFIGURATION` created in XCONF (step skipped if configuration already existed in step 6) |
| 8 | Get ESTB MAC | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"<SYSTEM_DEVICE_PARAMS>"` (config key `SYSTEM_DEVICE_PARAMS`) — retrieves ESTB MAC address for XCONF firmware rule targeting<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | ESTB MAC address returned and must not be empty — saved for use in steps 9–12 |
| 9 | Check Existing Firmware Rule | Query XCONF REST API: `GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_RULE&applicationType=stb&templateId=MAC_RULE` using ESTB MAC (step 8), model (step 3), and firmware config (step 6/7) | XCONF query executed; existing firmware rule returned and saved (or `null` — triggers step 10) |
| 10 | Create New Firmware Rule | **Conditional** (step 9 = no existing firmware rule) — Create MAC-based firmware rule in XCONF: `POST /xconfAdminService/firmwarerule/importAll?applicationType=stb` with condition `eStbMac IS <ESTB_MAC>`, configId from step 6/7, `rebootImmediately: true` | New firmware rule `TDK_{MODEL}_TEST_FIRMWARE_RULE` imported to XCONF — `IMPORTED` list non-empty (step skipped if rule already existed) |
| 11 | Check Existing Firmware Local Server Rule | Query XCONF REST API: `GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE&applicationType=stb&templateId=DOWNLOAD_LOCATION_FILTER` — checks if local server download filter rule exists for this device | XCONF query executed; existing local server rule returned (or `null` — triggers step 12) |
| 12 | Create New Firmware Local Server Rule | **Conditional** (step 11 = no existing local server rule) — Create `DOWNLOAD_LOCATION_FILTER` rule in XCONF: `POST /xconfAdminService/firmwarerule/importAll?applicationType=stb` with `firmwareLocation: https://tdktest.rdkcentral.com:8443/images/`, `firmwareDownloadProtocol: http`, matching device ESTB MAC from step 8 | New local server rule `TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE` imported to XCONF (step skipped if rule already existed) |
| 13 | Check disk partition | SSH `ls /dev/mmcblk0*` | wc -l` — counts disk partitions before initiating upgrade; partition count ≥ `4` routes through steps 14–15 (reboot-based partition upgrade path); count < `4` skips directly to step 16 (direct upgrade path) | Disk partition count retrieved and saved (e.g., `5` for devices with ≥ 4 partitions) |
| 14 | Update Firmware (upgrade — partition 4 path) | **Conditional** (step 13 partition count ≥ `4`) — Invoke `updateFirmware` on `org.rdk.System` (wait 60 seconds before invoking); device initiates reboot to download target firmware from XCONF local server<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success: true`; device reboots to start downloading new firmware (step skipped if partition count < 4) |
| 15 | Check disk partition (post-upgrade-reboot) | **Conditional** (step 13 partition count ≥ `4`) — SSH `ls /dev/mmcblk0*` | wc -l` after device reconnects from the reboot in step 14 — verifies partition count is ≥ `4` after the reboot-based upgrade step; expected partition count = `4` (after_reboot check) | Partition count ≥ `4` confirmed after reboot, validating partition upgrade path is proceeding correctly (step skipped if partition count < 4) |
| 16 | Update Firmware (upgrade — direct trigger) | Invoke `updateFirmware` on `org.rdk.System` (wait 60 seconds) — for non-partition-4 devices this is the primary upgrade trigger; for partition-4 devices, this is the second push after the reboot from step 14<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success: true`; firmware download to target version begins |
| 17 | Check Current Version (verify upgrade) | Invoke `getDownloadedFirmwareInfo` on `org.rdk.System` — waits `<FIRMWARE_DOWNLOAD_REBOOT_IN_SECONDS>` seconds for device to install firmware and reboot; plugin is re-activated after reboot (PluginOnStep)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Downloaded firmware version matches `<FIRMWARE_VERSION>` from device config file, confirming upgrade to the new firmware succeeded |
| 18 | Check Time Sync (post-upgrade) | SSH `date` on device to get DUT UTC time — compare against the actual current UTC time (wall clock at time of execution) to verify time sync is active after the upgrade reboot | DUT UTC time matches current UTC time (within 1 minute), confirming NTP/time sync is active on the upgraded firmware |
| 19 | Check Version File (post-upgrade) | SSH verify `/version.txt` exists and is not empty after upgrade reboot: `[ -f "/version.txt" ] && echo 1 \|\| echo 0` | `/version.txt` exists and is not empty on the upgraded firmware, confirming version file is present post-upgrade |
| 20 | Update Firmware Configuration (prepare revert) | Query XCONF for current firmware configuration (`GET /xconfAdminService/queries/firmwares/model/{MODEL}`), then update it (`PUT /xconfAdminService/updates/firmwares`) — sets `firmwareFilename` to the **original** image filename derived from the firmware version saved in step 2; this reconfigures XCONF so that steps 21–26 will download the original firmware back | XCONF firmware configuration updated with the original firmware filename; expected result: `update_existing_rule` with the original image name from step 2 |
| 21 | Check disk partition (before revert) | SSH `ls /dev/mmcblk0*` | wc -l` — counts disk partitions before initiating the **revert** firmware upgrade; partition count ≥ `4` routes through steps 22–23 (reboot-based partition revert path); count < `4` skips directly to step 24 (direct revert path) | Disk partition count retrieved and saved (e.g., `5` for devices with ≥ 4 partitions) |
| 22 | Update Firmware (revert — partition 4 path) | **Conditional** (step 21 partition count ≥ `4`) — Invoke `updateFirmware` on `org.rdk.System` (wait 60 seconds before invoking); device initiates reboot to download the original firmware from XCONF (reverting the upgrade)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success: true`; device reboots to start downloading original firmware (step skipped if partition count < 4) |
| 23 | Check disk partition (post-revert-reboot) | **Conditional** (step 21 partition count ≥ `4`) — SSH `ls /dev/mmcblk0*` | wc -l` after device reconnects from the reboot in step 22 — verifies partition count is ≥ `4` after the reboot-based revert; expected partition count = `4` (after_reboot check) | Partition count ≥ `4` confirmed after reboot (step skipped if partition count < 4) |
| 24 | Update Firmware (revert — direct trigger) | Invoke `updateFirmware` on `org.rdk.System` (wait 60 seconds) — for non-partition-4 devices this is the primary revert trigger; for partition-4 devices, this is the second push after the reboot from step 22<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success: true`; original firmware download begins |
| 25 | Check Current Version (verify revert) | Invoke `getDownloadedFirmwareInfo` on `org.rdk.System` — waits `<FIRMWARE_DOWNLOAD_REBOOT_IN_SECONDS>` seconds for device to install original firmware and reboot; plugin is re-activated after reboot (PluginOnStep)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Downloaded firmware version matches the **original** firmware version saved in step 2, confirming successful revert to the original firmware |
| 26 | Check Time Sync (post-revert) | SSH `date` on device to get DUT UTC time — compare against the actual current UTC time (wall clock at time of execution) to verify time sync is active after the revert reboot | DUT UTC time matches current UTC time (within 1 minute), confirming time sync is active on the reverted firmware |

---

<a id="system_check_model_number-sys_23"></a>
### System_Check_Model_Number (SYS_23)

**Objective:** Checks the model number of the DUT

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | SSH to device: `grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs` reads the `model_number` field from the device details cache file (path from config key `SYSTEM_DEVICE_DETAILS_FILE_PATH`) | Model number read from device cache file successfully and saved for comparison in step 2 |
| 2 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System` (version 2) with `query`: `"DeviceInfo.model"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.model"}}' http://127.0.0.1:9998/jsonrpc` | `MODEL_NUMBER` returned by `getPlatformConfiguration` matches the `model_number` value read from device cache file in step 1 |

---

<a id="system_check_device_mac_address-sys_24"></a>
### System_Check_Device_Mac_Address (SYS_24)

**Objective:** Checks the device MAC address

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | SSH to device: `grep estb_mac /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs` — reads the `estb_mac` field from the device details cache file (path from config key `SYSTEM_DEVICE_DETAILS_FILE_PATH`) | ESTB MAC address read from device cache file successfully and saved for comparison in step 2 |
| 2 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System` (version 2) with `query`: `"AccountInfo.deviceMACAddress"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.deviceMACAddress"}}' http://127.0.0.1:9998/jsonrpc` | `deviceMACAddress` returned by `getPlatformConfiguration` matches the `estb_mac` value read from device cache file in step 1 |

---

<a id="system_check_firmware_upgrade_status-sys_25"></a>
### System_Check_Firmware_Upgrade_Status (SYS_25)

**Objective:** Checks the firmware upgrade status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get SWUpdate File Status | SSH to device: `[ -f "/opt/swupdate.conf" ] && echo 1 \|\| echo 0` — checks whether `/opt/swupdate.conf` exists; if file exists → `FIRMWARE_UPGRADE_STATUS: true`; if not → `FIRMWARE_UPGRADE_STATUS: false` result saved for comparison in step 2 | `/opt/swupdate.conf` presence checked successfully `FIRMWARE_UPGRADE_STATUS` saved (`true` or `false`) |
| 2 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System` (version 2) with `query`: `"AccountInfo.firmwareUpdateDisabled"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.firmwareUpdateDisabled"}}' http://127.0.0.1:9998/jsonrpc` | `firmwareUpdateDisabled` value returned by `getPlatformConfiguration` matches the `FIRMWARE_UPGRADE_STATUS` read from `/opt/swupdate.conf` in step 1 |

---

<a id="system_check_public_ip_address-sys_26"></a>
### System_Check_Public_IP_Address (SYS_26)

**Objective:** Checks the public IP address

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Public IP Address | SSH to device: `curl -s ifconfig.me` — fetches the device's public IP address from the external service; result saved as `PUBLIC_IP` for comparison in step 2 | Public IP address retrieved successfully from device and saved |
| 2 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System` (version 2) with `query`: `"DeviceInfo.publicIP"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.publicIP"}}' http://127.0.0.1:9998/jsonrpc` | `publicIP` returned by `getPlatformConfiguration` matches the `PUBLIC_IP` value retrieved via `ifconfig.me` in step 1 |

---

<a id="system_check_hdr_capabilities-sys_27"></a>
### System_Check_HDR_Capabilities (SYS_27)

**Objective:** Checks the HDR Capabilities of the device

**Pre-condition:**

#### Pre-condition 1: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |

#### Pre-condition 2: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration"}' http://127.0.0.1:9998/jsonrpc` | HDR capabilities returned match expected value `<SYSTEM_SUPPORTED_HDR_CAPABILITIES>` from device config file |

---

<a id="setandget_all_time_zones-sys_28"></a>
### SetAndGet_All_Time_Zones (SYS_28)

**Objective:** Set and get all the time zones

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke `getTimeZones` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Full list of supported time zones returned successfully and saved for iteration |
| 2 | Set TimeZone DST | For each timezone in list from step 1 — Invoke `setTimeZoneDST` on `org.rdk.System` with `timeZone`: `"<result_step_1>"` (iterating over each entry)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Timezone set successfully (`success: true`) for each iteration |
| 3 | Get TimeZone DST | Invoke `getTimeZoneDST` on `org.rdk.System` (wait 1 second before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the timezone set in the current iteration |

---

<a id="system_toggle_network_standby_mode_status-sys_29"></a>
### System_Toggle_Network_Standby_Mode_Status (SYS_29)

**Objective:** Toggle Network Standby Mode Status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Network Standby Mode | Invoke `getNetworkStandbyMode` on `org.rdk.System` to retrieve current status before toggling<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Current network standby mode returned as `true` or `false` and saved as baseline for toggle |
| 2 | Set Network Standby Mode | Invoke `setNetworkStandbyMode` on `org.rdk.System` with `nwStandby` set to the toggled value (opposite of step 1)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setNetworkStandbyMode", "params": {"nwStandby": "<toggled_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Network standby mode set successfully (`success: true`) |
| 3 | Get Network Standby Mode | Invoke `getNetworkStandbyMode` on `org.rdk.System` to verify toggle was applied<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Network standby mode returned matches the toggled value (opposite of step 1) |
| 4 | Check Network Standby Mode Changed Event | Listen for event `onNetworkStandbyModeChanged` (wait up to 3 seconds) | Event received with `nwStandby` value matching the toggled value set in step 2 |

---

<a id="check_power_state_before_reboot_on_standby_state-sys_30"></a>
### Check_Power_State_Before_Reboot_On_Standby_State (SYS_30)

**Objective:** Checks the powerstate before reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power State returned successfully |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"STANDBY"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |
| 3 | Get Power State | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `LIGHT_SLEEP,STANDBY` |
| 4 | System reboot | Invoke `reboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag: `system_check_set_operation` |
| 5 | Get Power State Before Reboot | Invoke `getPowerStateBeforeReboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Expected: `compared against value from step 3` |

**Post-condition:**

#### Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check power state | Invoke `getPowerState` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `LIGHT_SLEEP,STANDBY` |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"<value>"`, `powerState`: `"ON"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power State set successfully |

---

<a id="check_time_zones_persist_after_reboot-sys_31"></a>
### Check_Time_Zones_Persist_After_Reboot (SYS_31)

**Objective:** Checks whether time zone setting is persist after reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke `getTimeZones` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Full list of supported time zones returned successfully and saved for iteration |
| 2 | Set TimeZone DST | For each timezone in list from step 1 Invoke `setTimeZoneDST` on `org.rdk.System` with iterating timezone<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Timezone set successfully (`success: true`) for each iteration |
| 3 | System reboot | Invoke `reboot` on `org.rdk.System` to test persistence<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 4 | Get TimeZone DST | Invoke `getTimeZoneDST` on `org.rdk.System` (wait 1 second after reconnect)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned after reboot matches the timezone set in step 2, confirming persistence |

---

<a id="system_reboot_and_check_system_uptime-sys_32"></a>
### System_Reboot_And_Check_System_Uptime (SYS_32)

**Objective:** To reboot and check the system uptime

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Uptime | Invoke `requestSystemUptime` on `org.rdk.System` to record uptime before reboot<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | System uptime returned successfully and must not be empty |
| 2 | System reboot | Invoke `reboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 3 | Get System Uptime | Invoke `requestSystemUptime` on `org.rdk.System` after device reconnects<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | System uptime after reboot is less than `<SYSTEM_UPTIME_IN_SECONDS>` seconds, confirming device rebooted successfully |

---

<a id="system_check_on_timezonedst_changed_event-sys_33"></a>
### System_Check_On_TimeZoneDST_Changed_Event (SYS_33)

**Objective:** Checks whether the `onTimeZoneDSTChanged` event is fired correctly when the timezone is changed, iterating over a set of timezones selected from the full list returned by `getTimeZones`

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke `getTimeZones` on `org.rdk.System` and save the returned list; a subset of timezones is selected for loop iteration<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.2.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Full list of supported time zones returned successfully and timezones saved for iteration |
| 2 | Set TimeZone DST | Invoke `setTimeZoneDST` on `org.rdk.System` with a baseline `timeZone` value to establish a known starting point before the loop<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<baseline_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Timezone set successfully (`success: true`) |
| 3 | Get TimeZone DST | Invoke `getTimeZoneDST` on `org.rdk.System` (wait 1 second before invoking) to verify the baseline timezone<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the baseline timezone set in step 2 |
| 4 | Get TimeZone DST *(loop — repeated for each timezone in the iteration set)* | Invoke `getTimeZoneDST` on `org.rdk.System` to capture the current timezone before setting the next one in the iteration<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Current timezone returned successfully and saved as the old timezone for event validation |
| 5 | Set TimeZone DST *(loop)* | For each timezone in the iteration set from step 1 — Invoke `setTimeZoneDST` on `org.rdk.System` with the current iteration timezone<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<iteration_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Timezone set successfully (`success: true`) for each iteration |
| 6 | Get TimeZone DST *(loop)* | Invoke `getTimeZoneDST` on `org.rdk.System` (wait 1 second before invoking) to verify the timezone was applied<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the timezone set in step 5 for the current iteration |
| 7 | Check On TimeZoneDST Event *(loop)* | Listen for event `onTimeZoneDSTChanged` (wait up to 2 seconds) after each timezone change in the loop | Event received with `newTimeZone` matching the timezone set in step 5 and `oldTimeZone` matching the timezone captured in step 4 of the same iteration |

---

<a id="system_check_rfc_status-sys_34"></a>
### System_Check_RFC_Status (SYS_34)

**Objective:** Checks whether the RFC value is correctly reflected using getRFCConfig

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check RFC Status | Read current value of TR181 parameter `<SYSTEM_RFC_PARAMETER_NAME>` from device config and save for reference | TR181 parameter value read from device successfully and saved |
| 2 | Disable RFC Parameter | Disable TR181 parameter `<SYSTEM_RFC_PARAMETER_NAME>` on the device via configuration | TR181 parameter disabled successfully |
| 3 | System reboot | Invoke `reboot` on `org.rdk.System` (wait 5 seconds for device to restart)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 4 | Get System RFC Config | Invoke `getRFCConfig` on `org.rdk.System` with `rfcList`: `"<SYSTEM_RFC_PARAMETER_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | RFC parameter value returned is `false`, confirming the disabled state persists after reboot |
| 5 | Enable RFC Parameter | Enable TR181 parameter `<SYSTEM_RFC_PARAMETER_NAME>` on the device via configuration | TR181 parameter enabled successfully |
| 6 | System reboot | Invoke `reboot` on `org.rdk.System` (wait 5 seconds for device to restart)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 7 | Get System RFC Config | Invoke `getRFCConfig` on `org.rdk.System` with `rfcList`: `"<SYSTEM_RFC_PARAMETER_NAME>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | RFC parameter value returned is `true`, confirming the enabled state persists after reboot |

---

<a id="system_setandget_friendly_name-sys_35"></a>
### System_SetandGet_Friendly_Name (SYS_35)

**Objective:** Check whether able to set and get friendly name

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System` to record current name before modification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Current friendly name returned successfully and saved for revert |
| 2 | Set Friendly Name | Invoke `setFriendlyName` on `org.rdk.System` with `friendlyName`: `"Test_Value"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Friendly name set successfully (`success: true`) |
| 3 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System` to verify set operation<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly name returned is `"Test_Value"`, confirming the set in step 2 was applied |
| 4 | Check On Friendly Name Changed Event | Listen for event `onFriendlyNameChanged` (wait up to 2 seconds) | Event received with `friendlyName`: `"Test_Value"` |

---

<a id="system_check_friendly_name_persist-sys_36"></a>
### System_Check_Friendly_Name_Persist (SYS_36)

**Objective:** Check friendly name is persisting on reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System` to record current name before modification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Current friendly name returned successfully and saved for revert |
| 2 | Set Friendly Name | Invoke `setFriendlyName` on `org.rdk.System` with `friendlyName`: `"Test_Value"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Friendly name set successfully (`success: true`) |
| 3 | System reboot | Invoke `reboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 4 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System` after device reconnects<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly name `"Test_Value"` persists after reboot and is returned successfully |

---

<a id="system_set_invalid_timezone_dst-sys_37"></a>
### System_Set_Invalid_TimeZone_DST (SYS_37)

**Objective:** Checks whether able to set invalid timezone

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke `setTimeZoneDST` on `org.rdk.System` with `timeZone`: `"TestValue1/TestValue2"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "TestValue1/TestValue2"}}' http://127.0.0.1:9998/jsonrpc` | `setTimeZoneDST` returns an error response with `success: false` for the invalid timezone `"TestValue1/TestValue2"` |

---

<a id="system_check_rfclist_with_empty_value-sys_38"></a>
### System_Check_RFCList_with_Empty_Value (SYS_38)

**Objective:** Check RFC configurations list with empty value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check RFC Config List Empty | Invoke `getRFCConfig` on `org.rdk.System` with `rfcList`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": ""}}' http://127.0.0.1:9998/jsonrpc` | `getRFCConfig` with empty `rfcList` returns a valid response (`success: true`) with an empty RFC configuration list no error, but no entries returned |

---

<a id="system_check_device_type-sys_39"></a>
### System_Check_Device_Type (SYS_39)

**Objective:** Check the device type of the DUT with getPlatformConfiguration API

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Platform Configuration | Invoke `getPlatformConfiguration` on `org.rdk.System` with `query`: `"DeviceInfo.deviceType"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration", "params": {"query": "DeviceInfo.deviceType"}}' http://127.0.0.1:9998/jsonrpc` | Device type returned matches expected value `<DEVICEINFO_DEVICE_TYPE>` from device config file |

---

<a id="system_check_device_ssh_state_after_reboot_on_standby_state-sys_40"></a>
### System_Check_Device_SSH_State_After_Reboot_On_Standby_State (SYS_40)

**Objective:** Check whether the box sshable or not in standbymode after reboot

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke `getPowerState` on `org.rdk.System` to record current power state before modification<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, or `ON` — current power state returned successfully |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"APIUnitTest"`, `powerState`: `"STANDBY"` to put device into standby<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power state set to `STANDBY` successfully |
| 3 | Get Power State | Invoke `getPowerState` on `org.rdk.System` to confirm device is in standby before reboot<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `LIGHT_SLEEP` or `STANDBY` |
| 4 | System Reboot | Invoke `reboot` on `org.rdk.System` (wait for device to come back up after reboot)<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success: true`) |
| 5 | Check Device SSH State | After device is back up, verify the device is SSH-accessible (external function: `check_device_ssh_state` creates SSH session, retrieves MAC address via `ifconfig`) | Device is SSH-accessible after reboot in standby state (`Box is SSH able`) |

**Post-condition:**

#### Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Power State | Invoke `getPowerState` on `org.rdk.System` to confirm current standby state before reverting<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected: `LIGHT_SLEEP` or `STANDBY` |
| 2 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `standbyReason`: `"APIUnitTest"`, `powerState`: `"ON"` to revert device to ON state<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"ON"}}' http://127.0.0.1:9998/jsonrpc` | Power state reverted to `ON` successfully |

---

<a id="system_set_invalid_territory_and_region-sys_41"></a>
### System_Set_Invalid_Territory_And_Region (SYS_41)

**Objective:** Sets invalid territory and region

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke `setTerritory` on `org.rdk.System` with `territory`: `"ABC"`, `region`: `"AB-CD"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "AB-CD"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid territory` |

---

<a id="system_set_empty_territory_and_region-sys_42"></a>
### System_Set_Empty_Territory_And_Region (SYS_42)

**Objective:** Sets empty territory and region

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke `setTerritory` on `org.rdk.System` with `territory`: `""`, `region`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid territory` |

---

<a id="system_set_invalid_territory_and_valid_region-sys_43"></a>
### System_Set_Invalid_Territory_And_Valid_Region (SYS_43)

**Objective:** Sets invalid territory and valid region

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke `setTerritory` on `org.rdk.System` with `territory`: `"ABC"`, `region`: `"US-AS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid territory` |

---

<a id="system_set_empty_territory_and_valid_region-sys_44"></a>
### System_Set_Empty_Territory_And_Valid_Region (SYS_44)

**Objective:** Sets empty territory and valid region

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke `setTerritory` on `org.rdk.System` with `territory`: `""`, `region`: `"US-AS"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid territory` |

---

<a id="system_set_and_get_territory_region-sys_45"></a>
### System_Set_And_Get_Territory_Region (SYS_45)

**Objective:** Check whether able to set and get territory and region

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get territory And region Config File | Read territory and region pairs from device config file `<SYSTEM_TERRITORYS>` and save for loop iteration | Territory/region pairs read successfully and saved for iteration |
| 2 | System Set Territory | For each territory/region pair from step 1 — Invoke `setTerritory` on `org.rdk.System` with `territory` and `region` values from the current iteration<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "<territory>", "region": "<region>"}}' http://127.0.0.1:9998/jsonrpc` | Territory and region set successfully (`success: true`) for each iteration |
| 3 | Check Territory Change Event | Listen for event `onTerritoryChanged` | Event received with `territory` and `region` matching the values set in step 2 |
| 4 | System Get Territory | Invoke `getTerritory` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTerritory"}' http://127.0.0.1:9998/jsonrpc` | Territory and region returned match the values set in step 2 |

---

<a id="system_verify_set_territory_without_params-sys_46"></a>
### System_Verify_Set_Territory_without_Params (SYS_46)

**Objective:** Verify that the setTerritory method returns an error when both territory and region are not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Only Territory | Invoke `setTerritory` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid territory name` |

---

<a id="system_set_valid_territory_and_set_invalid_region-sys_47"></a>
### System_Set_Valid_Territory_And_Set_Invalid_Region (SYS_47)

**Objective:** Check whether able to set valid territory and invalid region to set territory API

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Valid Territory And Set Invalid Region | Invoke `setTerritory` on `org.rdk.System` with `territory`: `"CHN"`, `region`: `"TestingValue"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": "TestingValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `invalid region` |

---

<a id="system_set_valid_territory_and_set_empty_region-sys_48"></a>
### System_Set_Valid_Territory_And_Set_Empty_Region (SYS_48)

**Objective:** Check whether able to set valid territory and empty region to set territory API

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Valid Territory And Set Empty Region | Invoke `setTerritory` on `org.rdk.System` with `territory`: `"CHN"`, `region`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | `setTerritory` returns an error response with `success: false` for valid territory `"CHN"` with empty region |

---

<a id="system_get_mfg_serial_number-sys_49"></a>
### System_Get_Mfg_Serial_Number (SYS_49)

**Objective:** Check whether able to get the manufacturing serial number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Get Mfg Serial Number | Invoke `getMfgSerialNumber` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMfgSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Manufacturing serial number returned successfully and must not be empty |

---

<a id="system_activatedeactivate_event_test-sys_50"></a>
### System_ActivateDeactivate_Event_Test (SYS_50)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `onStateChanged` from Controller (wait up to 2 seconds) | Event received with callsign `org.rdk.System`, state `deactivated`, reason `requested` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate System Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"` (wait 1 second before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Plugin activated successfully |
| 5 | Check State Change Event | Listen for event `onStateChanged` from Controller (wait up to 2 seconds) | Event received with callsign `org.rdk.System`, state `activated`, reason `requested` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="system_invalid_set_mode-sys_51"></a>
### System_Invalid_Set_Mode (SYS_51)

**Objective:** Validate by setting up invalid mode

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Mode | Invoke `setMode` on `org.rdk.System` with `param`: `"INVALID"`, `duration`: `0`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"param": "INVALID", "duration": 0}}' http://127.0.0.1:9998/jsonrpc` | `setMode` returns an error response with `success: false` for the invalid mode value `"INVALID"` |

---

<a id="system_setandget_empty_friendly_name-sys_52"></a>
### System_SetandGet_Empty_Friendly_Name (SYS_52)

**Objective:** Check whether able to set and get empty friendly name

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly Name returned successfully |
| 2 | Set Friendly Name | Invoke `setFriendlyName` on `org.rdk.System` with `friendlyName`: `" "`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": " "}}' http://127.0.0.1:9998/jsonrpc` | Friendly Name set successfully |
| 3 | Get Friendly Name | Invoke `getFriendlyName` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly name returned is a space character `" "`, confirming empty/space name was accepted |
| 4 | Check On Friendly Name Changed Event | Listen for event `onFriendlyNameChanged` (wait up to 2 seconds) | Event received with `friendlyName`: `" "` (space character) |
| 5 | Set Friendly Name | Invoke `setFriendlyName` on `org.rdk.System` with `friendlyName`: `"My Device"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "My Device"}}' http://127.0.0.1:9998/jsonrpc` | Friendly Name set successfully |

---

<a id="system_invalid_set_power_state-sys_53"></a>
### System_Invalid_Set_Power_State (SYS_53)

**Objective:** Validate by setting up invalid power state

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Power State | Invoke `setPowerState` on `org.rdk.System` with `powerState`: `"INVALID"`, `standbyReason`: `"APIUnitTest"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "INVALID", "standbyReason": "APIUnitTest"}}' http://127.0.0.1:9998/jsonrpc` | `setPowerState` returns an error response with `success: false` for the invalid power state value `"INVALID"` |

---

<a id="system_invalid_timezone_errorvalidation-sys_54"></a>
### System_Invalid_TimeZone_ErrorValidation (SYS_54)

**Objective:** Set and get Invalid DST time zone

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke `setTimeZoneDST` on `org.rdk.System` with `timeZone`: `" "`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Expected file not found` |

---

<a id="system_invalid_key_errormessage-sys_55"></a>
### System_Invalid_Key_ErrorMessage (SYS_55)

**Objective:** Validate error message with invalid key in deviceInfo api

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Info | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"INVALID"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "INVALID"}}' http://127.0.0.1:9998/jsonrpc` | `getDeviceInfo` returns an error response with `success: false` for the invalid key `"INVALID"` |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 70 minutes |
| Priority | Medium |
| TDK Release Version | M81 |