## TestScript Name
RDKV_CERT_AVS_System

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
   - [System_Get_ESTB_MAC](#system_get_estb_mac)
   - [System_Get_Serial_Number](#system_get_serial_number)
   - [System_Get_Version](#system_get_version)
   - [System_Get_Uptime](#system_get_uptime)
   - [System_Get_RFC_Config](#system_get_rfc_config)
   - [System_SetAndGet_Power_State](#system_setandget_power_state)
   - [System_SetAndGet_TimeZone_DST](#system_setandget_timezone_dst)
   - [System_Set_NORMAL_Mode](#system_set_normal_mode)
   - [System_GetMac_Address](#system_getmac_address)
   - [System_Get_Image_Version](#system_get_image_version)
   - [System_Get_model_number](#system_get_model_number)
   - [System_Get_boxIP](#system_get_boxip)
   - [System_Get_build_type](#system_get_build_type)
   - [System_Get_eth_mac](#system_get_eth_mac)
   - [System_Get_rf4ce_mac](#system_get_rf4ce_mac)
   - [System_Get_Bluetooth_mac](#system_get_bluetooth_mac)
   - [System_Get_WiFi_Mac](#system_get_wifi_mac)
   - [Check_Power_State_Before_Reboot](#check_power_state_before_reboot)
   - [System_Check_On_SystemMode_Changed](#system_check_on_systemmode_changed)
   - [System_Check_Reboot_Reason_Event](#system_check_reboot_reason_event)
   - [Enable_And_Disable_Telemetry_OptOut_Status](#enable_and_disable_telemetry_optout_status)
   - [System_Validate_Firmware_Upgrade](#system_validate_firmware_upgrade)
   - [System_Check_Model_Number](#system_check_model_number)
   - [System_Check_Device_Mac_Address](#system_check_device_mac_address)
   - [System_Check_Firmware_Upgrade_Status](#system_check_firmware_upgrade_status)
   - [System_Check_Public_IP_Address](#system_check_public_ip_address)
   - [System_Check_HDR_Capabilities](#system_check_hdr_capabilities)
   - [SetAndGet_All_Time_Zones](#setandget_all_time_zones)
   - [System_Toggle_Network_Standby_Mode_Status](#system_toggle_network_standby_mode_status)
   - [Check_Power_State_Before_Reboot_On_Standby_State](#check_power_state_before_reboot_on_standby_state)
   - [Check_Time_Zones_Persist_After_Reboot](#check_time_zones_persist_after_reboot)
   - [System_Reboot_And_Check_System_Uptime](#system_reboot_and_check_system_uptime)
   - [System_Check_On_TimeZoneDST_Changed_Event](#system_check_on_timezonedst_changed_event)
   - [System_Check_RFC_Status](#system_check_rfc_status)
   - [System_SetandGet_Friendly_Name](#system_setandget_friendly_name)
   - [System_Check_Friendly_Name_Persist](#system_check_friendly_name_persist)
   - [System_Set_Invalid_TimeZone_DST](#system_set_invalid_timezone_dst)
   - [System_Check_RFCList_with_Empty_Value](#system_check_rfclist_with_empty_value)
   - [System_Check_Device_Type](#system_check_device_type)
   - [System_Check_Device_SSH_State_After_Reboot_On_Standby_State](#system_check_device_ssh_state_after_reboot_on_standby_state)
   - [System_Set_Invalid_Territory_And_Region](#system_set_invalid_territory_and_region)
   - [System_Set_Empty_Territory_And_Region](#system_set_empty_territory_and_region)
   - [System_Set_Invalid_Territory_And_Valid_Region](#system_set_invalid_territory_and_valid_region)
   - [System_Set_Empty_Territory_And_Valid_Region](#system_set_empty_territory_and_valid_region)
   - [System_Set_And_Get_Territory_Region](#system_set_and_get_territory_region)
   - [System_Verify_Set_Territory_without_Params](#system_verify_set_territory_without_params)
   - [System_Set_Valid_Territory_And_Set_Invalid_Region](#system_set_valid_territory_and_set_invalid_region)
   - [System_Set_Valid_Territory_And_Set_Empty_Region](#system_set_valid_territory_and_set_empty_region)
   - [System_Get_Mfg_Serial_Number](#system_get_mfg_serial_number)
   - [System_ActivateDeactivate_Event_Test](#system_activatedeactivate_event_test)
   - [System_Invalid_Set_Mode](#system_invalid_set_mode)
   - [System_SetandGet_Empty_Friendly_Name](#system_setandget_empty_friendly_name)
   - [System_Invalid_Set_Power_State](#system_invalid_set_power_state)
   - [System_Invalid_TimeZone_ErrorValidation](#system_invalid_timezone_errorvalidation)
   - [System_Invalid_Key_ErrorMessage](#system_invalid_key_errormessage)
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **System** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.System` (version 1)

## APIs Under Test

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

## Events Under Test

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

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_MacAddresses_Retreived` on `System` plugin

- Register and listen to event `Event_PowerState_Changed` on `System` plugin

- Register and listen to event `Event_SystemMode_Changed` on `System` plugin

- Register and listen to event `Event_Reboot_Request` on `System` plugin

- Register and listen to event `Event_On_Network_Standby_Mode_Changed` on `System` plugin

- Register and listen to event `Event_On_TimeZoneDST_Changed` on `System` plugin

- Register and listen to event `Event_On_Friendly_Name_Changed` on `System` plugin

- Register and listen to event `Event_On_Territory_Changed` on `System` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

## Test Cases

<a id="system_get_estb_mac"></a>
### TestCase Name
System_Get_ESTB_MAC

### TestCase ID
SYS_01

### TestCase Objective
Get requested device detail

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device ESTB MAC | Invoke getDeviceInfo on org.rdk.System with params: "<SYSTEM_DEVICE_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that device info response for `<SYSTEM_DEVICE_PARAMS>` is returned successfully and the value must not be empty |

---

<a id="system_get_serial_number"></a>
### TestCase Name
System_Get_Serial_Number

### TestCase ID
SYS_02

### TestCase Objective
Gets the serial number

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Serial No | Invoke getSerialNumber on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the serial number is returned successfully |

---

<a id="system_get_version"></a>
### TestCase Name
System_Get_Version

### TestCase ID
SYS_03

### TestCase Objective
Gets system version details

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Version | Invoke getSystemVersions on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSystemVersions"}' http://127.0.0.1:9998/jsonrpc` | Verify that system versions are returned successfully |

---

<a id="system_get_uptime"></a>
### TestCase Name
System_Get_Uptime

### TestCase ID
SYS_04

### TestCase Objective
Gets system version details

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | The uptime value should be returned and must not be empty |

---

<a id="system_get_rfc_config"></a>
### TestCase Name
System_Get_RFC_Config

### TestCase ID
SYS_05

### TestCase Objective
Gets RFC configurations

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System RFC Config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that RFC config is returned successfully |

---

<a id="system_setandget_power_state"></a>
### TestCase Name
System_SetAndGet_Power_State

### TestCase ID
SYS_06

### TestCase Objective
Set and get device power state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set Power State | Invoke setPowerState on org.rdk.System with standbyReason: "APIUnitTest", powerState: "STANDBY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power state set to `STANDBY` successfully |
| 3 | Power State Changed Event | Listen for event onSystemPowerStateChanged (wait up to 30 seconds) | Event `onSystemPowerStateChanged` is received with new state matching `STANDBY` (the value set in step 2) |
| 4 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power state returned is `STANDBY`, confirming the set operation in step 2 was successful |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Power State | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set Power State | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Power state reverted to `ON` successfully |
| 3 | Check Power State | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Power state returned is `ON`, confirming device is restored to original state |

---

<a id="system_setandget_timezone_dst"></a>
### TestCase Name
System_SetAndGet_TimeZone_DST

### TestCase ID
SYS_07

### TestCase Objective
Set and get DST time zone

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "America/New_York"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "America/New_York"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the time zone DST is set successfully |
| 2 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Expected `America/New_York` |

---

<a id="system_set_normal_mode"></a>
### TestCase Name
System_Set_NORMAL_Mode

### TestCase ID
SYS_08

### TestCase Objective
Set STB mode to NORMAL

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set STB Mode NORMAL | Invoke setMode on org.rdk.System with duration: "<value>", mode: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": "<value>", "mode": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the mode is set successfully |

---

<a id="system_getmac_address"></a>
### TestCase Name
System_GetMac_Address

### TestCase ID
SYS_09

### TestCase Objective
Get Mac Address

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get MacAddress | Invoke getMacAddresses on org.rdk.System with GUID: "61734787891723481"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMacAddresses", "params": {"GUID": "61734787891723481"}}' http://127.0.0.1:9998/jsonrpc` | `asyncResponse` is `true` and `success` is `true`, confirming the async MAC address retrieval was triggered successfully |
| 2 | Check Mac Address | Listen for event onMacAddressesRetrieved (wait up to 2 seconds for async response) | Event is received and all MAC address fields (`ECM_MAC`, `ESTB_MAC`, `MOCA_MAC`, `ETH_MAC`, `WIFI_MAC`, `BLUETOOTH_MAC`, `RF4CE_MAC`) are validated against the pattern `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` each non-zero MAC must match a valid format |

---

<a id="system_get_image_version"></a>
### TestCase Name
System_Get_Image_Version

### TestCase ID
SYS_10

### TestCase Objective
Gets the image version

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Image Version | Invoke getDeviceInfo on org.rdk.System with params: "imageVersion"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "imageVersion"}}' http://127.0.0.1:9998/jsonrpc` | `imageVersion` is returned successfully and must not be empty |

---

<a id="system_get_model_number"></a>
### TestCase Name
System_Get_model_number

### TestCase ID
SYS_11

### TestCase Objective
Gets the model number

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device model number | Invoke getDeviceInfo on org.rdk.System with params: "model_number"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "model_number"}}' http://127.0.0.1:9998/jsonrpc` | `model_number` is returned successfully and must not be empty |

---

<a id="system_get_boxip"></a>
### TestCase Name
System_Get_boxIP

### TestCase ID
SYS_12

### TestCase Objective
Gets the box IP

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device boxIP | Invoke getDeviceInfo on org.rdk.System with params: "boxIP"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "boxIP"}}' http://127.0.0.1:9998/jsonrpc` | `boxIP` value is returned successfully and must not be empty |

---

<a id="system_get_build_type"></a>
### TestCase Name
System_Get_build_type

### TestCase ID
SYS_13

### TestCase Objective
Gets the build type

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device build type | Invoke getDeviceInfo on org.rdk.System with params: "build_type"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "build_type"}}' http://127.0.0.1:9998/jsonrpc` | `build_type` value is returned successfully and must not be empty |

---

<a id="system_get_eth_mac"></a>
### TestCase Name
System_Get_eth_mac

### TestCase ID
SYS_14

### TestCase Objective
Gets eth mac of the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device eth mac | Invoke getDeviceInfo on org.rdk.System with params: "eth_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "eth_mac"}}' http://127.0.0.1:9998/jsonrpc` | `eth_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="system_get_rf4ce_mac"></a>
### TestCase Name
System_Get_rf4ce_mac

### TestCase ID
SYS_15

### TestCase Objective
Gets the rf4ce mac of the device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device rf4ce mac | Invoke getDeviceInfo on org.rdk.System with params: "rf4ce_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "rf4ce_mac"}}' http://127.0.0.1:9998/jsonrpc` | `rf4ce_mac` value is returned successfully and must not be empty (8-byte RF4CE MAC format) |

---

<a id="system_get_bluetooth_mac"></a>
### TestCase Name
System_Get_Bluetooth_mac

### TestCase ID
SYS_16

### TestCase Objective
Gets device bluetooth mac

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Bluetooth Mac | Invoke getDeviceInfo on org.rdk.System with params: "bluetooth_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "bluetooth_mac"}}' http://127.0.0.1:9998/jsonrpc` | `bluetooth_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="system_get_wifi_mac"></a>
### TestCase Name
System_Get_WiFi_Mac

### TestCase ID
SYS_17

### TestCase Objective
Gets device WiFi mac

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device WiFi Mac | Invoke getDeviceInfo on org.rdk.System with params: "wifi_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "wifi_mac"}}' http://127.0.0.1:9998/jsonrpc` | `wifi_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address |

---

<a id="check_power_state_before_reboot"></a>
### TestCase Name
Check_Power_State_Before_Reboot

### TestCase ID
SYS_18

### TestCase Objective
Checks the powerstate before reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON`, saved for comparison in step 3 |
| 2 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 3 | Get Power State Before Reboot | Invoke getPowerStateBeforeReboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Power state before reboot matches the state recorded in step 1 |

---

<a id="system_check_on_systemmode_changed"></a>
### TestCase Name
System_Check_On_SystemMode_Changed

### TestCase ID
SYS_19

### TestCase Objective
Checks for the system mode changed event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set STB Mode WAREHOUSE | Invoke setMode on org.rdk.System with mode: "WAREHOUSE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": 5, "mode": "WAREHOUSE"}}' http://127.0.0.1:9998/jsonrpc` | Mode set to `WAREHOUSE` successfully (`success` : `true`) |
| 2 | Check On SystemMode Changed Event | Listen for event onSystemModeChanged (triggered immediately when mode is set to WAREHOUSE) | Event received with `mode`: `"WAREHOUSE"` |
| 3 | Check On SystemMode Changed Event | Listen for event onSystemModeChanged (wait up to 5 seconds for auto-revert) | Event received with `mode`: `"NORMAL"` confirming automatic revert after duration expires |

---

<a id="system_check_reboot_reason_event"></a>
### TestCase Name
System_Check_Reboot_Reason_Event

### TestCase ID
SYS_20

### TestCase Objective
Retrieve basic information about a reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System reboot | Invoke reboot on org.rdk.System with rebootReason: "API Validation"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot", "params": {"rebootReason": "API Validation"}}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 2 | Check On Reboot Request Event | Listen for event onRebootRequest (wait up to 60 seconds) | Event received with `rebootReason`: `"API Validation"` and `requestedApp`: `"SystemServices"` |

---

<a id="enable_and_disable_telemetry_optout_status"></a>
### TestCase Name
Enable_And_Disable_Telemetry_OptOut_Status

### TestCase ID
SYS_21

### TestCase Objective
Checks whether able to enable and disable the telemetry opt-out status

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OptOut Telemetry Status | Invoke isOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | `optOut` status returned successfully as `true` or `false` — saved for revert |
| 2 | Set OptOut Telemetry Status | Invoke setOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setOptOutTelemetry", "params": {"Opt-Out": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the telemetry opt-out status is set successfully (`success` : `true`) for each iteration |
| 3 | Get OptOut Telemetry Status | Invoke isOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | `optOut` value matches the value set in step 2 for the current iteration (`true` then `false`) |

---

<a id="system_validate_firmware_upgrade"></a>
### TestCase Name
System_Validate_Firmware_Upgrade

### TestCase ID
SYS_22

### TestCase Objective
Upgrades to specified firmware version

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Version File | SSH to device: verify /version.txt exists ([ -f "/version.txt" ] && echo 1 \|\| echo 0) and is not empty ([ -s "/version.txt" ] && echo 1 \|\| echo 0) before the firmware upgrade test begins | `/version.txt` file exists and is not empty on the device |
| 2 | Get Downloaded Firmware Info | Invoke getDownloadedFirmwareInfo on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current firmware version is returned successfully |
| 3 | Get Model Name | *(Conditional statement executed only if previous step condition is met)*<br>SSH read model_number from device details cache file <SYSTEM_DEVICE_DETAILS_FILE_PATH>: grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs model string saved for XCONF rule targeting | Verify that the model number is read from the device cache file successfully |
| 4 | Check Existing Model ID | Query XCONF REST API: GET /xconfAdminService/queries/models/TDK_{MODEL}_TEST_MODEL using model from step 3 checks whether a model ID entry already exists for this device | XCONF query executed successfully existing model ID returned and saved (or `null` if not found — triggers step 5) |
| 5 | Create New Model ID | *(Conditional statement executed only if the condition in Step 4 is met)*<br>Create model ID rule in XCONF: POST /xconfAdminService/updates/models with model name from step 3 | New model ID rule `TDK_{MODEL}_TEST_MODEL` created in XCONF successfully (step skipped if model ID already existed in step 4) |
| 6 | Check Existing Firmware Configuration | *(Conditional statement executed only if previous step condition is met)*<br>Query XCONF REST API: GET /xconfAdminService/queries/firmwares/model/TDK_{MODEL}_TEST_MODEL?applicationType=stb — checks whether a firmware configuration already exists for this model | XCONF query executed; existing firmware configuration returned and saved (or empty — triggers step 7) |
| 7 | Create New Firmware Configuration | *(Conditional statement executed only if the condition in Step 6 is met)*<br>Create firmware configuration in XCONF: POST /xconfAdminService/updates/firmwares linking model to target firmware <FIRMWARE_VERSION> | New firmware configuration `TDK_{MODEL}_TEST_FIRMWARE_CONFIGURATION` created in XCONF (step skipped if configuration already existed in step 6) |
| 8 | Get ESTB MAC | Invoke getDeviceInfo on org.rdk.System with params: "<SYSTEM_DEVICE_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | ESTB MAC address returned and must not be empty — saved for use in steps 9–12 |
| 9 | Check Existing Firmware Rule | Query XCONF REST API: GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_RULE&applicationType=stb&templateId=MAC_RULE using ESTB MAC (step 8), model (step 3), and firmware config (step 6/7) | XCONF query executed; existing firmware rule returned and saved (or `null` — triggers step 10) |
| 10 | Create New Firmware Rule | *(Conditional statement executed only if the condition in Step 9 is met)*<br>Create MAC-based firmware rule in XCONF: POST /xconfAdminService/firmwarerule/importAll?applicationType=stb with condition eStbMac IS <ESTB_MAC>, configId from step 6/7, rebootImmediately: true | New firmware rule `TDK_{MODEL}_TEST_FIRMWARE_RULE` imported to XCONF — `IMPORTED` list non-empty (step skipped if rule already existed) |
| 11 | Check Existing Firmware Local Server Rule | Query XCONF REST API: GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE&applicationType=stb&templateId=DOWNLOAD_LOCATION_FILTER — checks if local server download filter rule exists for this device | XCONF query executed; existing local server rule returned (or `null` — triggers step 12) |
| 12 | Create New Firmware Local Server Rule | *(Conditional statement executed only if the condition in Step 11 is met)*<br>Create DOWNLOAD_LOCATION_FILTER rule in XCONF: POST /xconfAdminService/firmwarerule/importAll?applicationType=stb with firmwareLocation: https://tdktest.rdkcentral.com:8443/images/, firmwareDownloadProtocol: http, matching device ESTB MAC from step 8 | New local server rule `TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE` imported to XCONF (step skipped if rule already existed) |
| 13 | Check disk partition | SSH ls /dev/mmcblk0* | wc -l` — counts disk partitions before initiating upgrade; partition count ≥ `4` routes through steps 14–15 (reboot-based partition upgrade path); count < `4` skips directly to step 16 (direct upgrade path) | Disk partition count retrieved and saved (e.g., `5` for devices with ≥ 4 partitions) |
| 14 | Update Firmware (upgrade — partition 4 path) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success` : `true`; device reboots to start downloading new firmware (step skipped if partition count < 4) |
| 15 | Check disk partition (post-upgrade-reboot) | *(Conditional statement executed only if the condition in Step 13 is met)*<br>SSH ls /dev/mmcblk0* | wc -l` after device reconnects from the reboot in step 14 — verifies partition count is ≥ `4` after the reboot-based upgrade step; expected partition count = `4` (after_reboot check) | Partition count ≥ `4` confirmed after reboot, validating partition upgrade path is proceeding correctly (step skipped if partition count < 4) |
| 16 | Update Firmware (upgrade — direct trigger) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success` : `true`; firmware download to target version begins |
| 17 | Check Current Version (verify upgrade) | Invoke getDownloadedFirmwareInfo on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Downloaded firmware version matches `<FIRMWARE_VERSION>` from device config file, confirming upgrade to the new firmware succeeded |
| 18 | Check Time Sync (post-upgrade) | SSH date on device to get DUT UTC time — compare against the actual current UTC time (wall clock at time of execution) to verify time sync is active after the upgrade reboot | DUT UTC time matches current UTC time (within 1 minute), confirming NTP/time sync is active on the upgraded firmware |
| 19 | Check Version File (post-upgrade) | SSH verify /version.txt exists and is not empty after upgrade reboot: [ -f "/version.txt" ] && echo 1 \|\| echo 0 | `/version.txt` exists and is not empty on the upgraded firmware, confirming version file is present post-upgrade |
| 20 | Update Firmware Configuration (prepare revert) | Query XCONF for current firmware configuration (GET /xconfAdminService/queries/firmwares/model/{MODEL}), then update it (PUT /xconfAdminService/updates/firmwares) — sets firmwareFilename to the **original** image filename derived from the firmware version saved in step 2; this reconfigures XCONF so that steps 21–26 will download the original firmware back | XCONF firmware configuration updated with the original firmware filename; expected result `update_existing_rule` with the original image name from step 2 |
| 21 | Check disk partition (before revert) | SSH ls /dev/mmcblk0* | wc -l` — counts disk partitions before initiating the **revert** firmware upgrade; partition count ≥ `4` routes through steps 22–23 (reboot-based partition revert path); count < `4` skips directly to step 24 (direct revert path) | Disk partition count retrieved and saved (e.g., `5` for devices with ≥ 4 partitions) |
| 22 | Update Firmware (revert — partition 4 path) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success` : `true`; device reboots to start downloading original firmware (step skipped if partition count < 4) |
| 23 | Check disk partition (post-revert-reboot) | *(Conditional statement executed only if the condition in Step 21 is met)*<br>SSH ls /dev/mmcblk0* | wc -l` after device reconnects from the reboot in step 22 — verifies partition count is ≥ `4` after the reboot-based revert; expected partition count = `4` (after_reboot check) | Partition count ≥ `4` confirmed after reboot (step skipped if partition count < 4) |
| 24 | Update Firmware (revert — direct trigger) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | `updateFirmware` returns `success` : `true`; original firmware download begins |
| 25 | Check Current Version (verify revert) | Invoke getDownloadedFirmwareInfo on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Downloaded firmware version matches the **original** firmware version saved in step 2, confirming successful revert to the original firmware |
| 26 | Check Time Sync (post-revert) | SSH date on device to get DUT UTC time — compare against the actual current UTC time (wall clock at time of execution) to verify time sync is active after the revert reboot | DUT UTC time matches current UTC time (within 1 minute), confirming time sync is active on the reverted firmware |

---

<a id="system_check_model_number"></a>
### TestCase Name
System_Check_Model_Number

### TestCase ID
SYS_23

### TestCase Objective
Checks the model number of the DUT

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | SSH to device: grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs reads the model_number field from the device details cache file (path from config key SYSTEM_DEVICE_DETAILS_FILE_PATH) | Verify that the model number is read from the device cache file successfully |
| 2 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.model"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.model"}}' http://127.0.0.1:9998/jsonrpc` | `MODEL_NUMBER` returned by `getPlatformConfiguration` matches the `model_number` value read from device cache file in step 1 |

---

<a id="system_check_device_mac_address"></a>
### TestCase Name
System_Check_Device_Mac_Address

### TestCase ID
SYS_24

### TestCase Objective
Checks the device MAC address

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | SSH to device: grep estb_mac /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs — reads the estb_mac field from the device details cache file (path from config key SYSTEM_DEVICE_DETAILS_FILE_PATH) | Verify that the ESTB MAC address is read from the device cache file successfully |
| 2 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "AccountInfo.deviceMACAddress"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.deviceMACAddress"}}' http://127.0.0.1:9998/jsonrpc` | `deviceMACAddress` returned by `getPlatformConfiguration` matches the `estb_mac` value read from device cache file in step 1 |

---

<a id="system_check_firmware_upgrade_status"></a>
### TestCase Name
System_Check_Firmware_Upgrade_Status

### TestCase ID
SYS_25

### TestCase Objective
Checks the firmware upgrade status

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get SWUpdate File Status | SSH to device: [ -f "/opt/swupdate.conf" ] && echo 1 \|\| echo 0 — checks whether /opt/swupdate.conf exists; if file exists → FIRMWARE_UPGRADE_STATUS: true; if not → FIRMWARE_UPGRADE_STATUS: false result saved for comparison in step 2 | `/opt/swupdate.conf` presence checked successfully `FIRMWARE_UPGRADE_STATUS` saved (`true` or `false`) |
| 2 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "AccountInfo.firmwareUpdateDisabled"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.firmwareUpdateDisabled"}}' http://127.0.0.1:9998/jsonrpc` | `firmwareUpdateDisabled` value returned by `getPlatformConfiguration` matches the `FIRMWARE_UPGRADE_STATUS` read from `/opt/swupdate.conf` in step 1 |

---

<a id="system_check_public_ip_address"></a>
### TestCase Name
System_Check_Public_IP_Address

### TestCase ID
SYS_26

### TestCase Objective
Checks the public IP address

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Public IP Address | SSH to device: curl -s ifconfig.me — fetches the device's public IP address from the external service; result saved as PUBLIC_IP for comparison in step 2 | Verify that the public IP address is retrieved from the device successfully |
| 2 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.publicIP"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.publicIP"}}' http://127.0.0.1:9998/jsonrpc` | `publicIP` returned by `getPlatformConfiguration` matches the `PUBLIC_IP` value retrieved via `ifconfig.me` in step 1 |

---

<a id="system_check_hdr_capabilities"></a>
### TestCase Name
System_Check_HDR_Capabilities

### TestCase ID
SYS_27

### TestCase Objective
Checks the HDR Capabilities of the device

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |

#### TestCase Pre-condition 2: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration"}' http://127.0.0.1:9998/jsonrpc` | HDR capabilities returned match expected value `<SYSTEM_SUPPORTED_HDR_CAPABILITIES>` from device config file |

---

<a id="setandget_all_time_zones"></a>
### TestCase Name
SetAndGet_All_Time_Zones

### TestCase ID
SYS_28

### TestCase Objective
Set and get all the time zones

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 3 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the timezone set in the current iteration |

---

<a id="system_toggle_network_standby_mode_status"></a>
### TestCase Name
System_Toggle_Network_Standby_Mode_Status

### TestCase ID
SYS_29

### TestCase Objective
Toggle Network Standby Mode Status

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Network Standby Mode | Invoke getNetworkStandbyMode on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Current network standby mode returned as `true` or `false` and saved as baseline for toggle |
| 2 | Set Network Standby Mode | Invoke setNetworkStandbyMode on org.rdk.System with nwStandby: "<toggled_from_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setNetworkStandbyMode", "params": {"nwStandby": "<toggled_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that network standby mode is set successfully (`success` : `true`) |
| 3 | Get Network Standby Mode | Invoke getNetworkStandbyMode on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Network standby mode returned matches the toggled value (opposite of step 1) |
| 4 | Check Network Standby Mode Changed Event | Listen for event onNetworkStandbyModeChanged (wait up to 3 seconds) | Event received with `nwStandby` value matching the toggled value set in step 2 |

---

<a id="check_power_state_before_reboot_on_standby_state"></a>
### TestCase Name
Check_Power_State_Before_Reboot_On_Standby_State

### TestCase ID
SYS_30

### TestCase Objective
Checks the powerstate before reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set Power State | Invoke setPowerState on org.rdk.System with standbyReason: "<value>", powerState: "STANDBY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |
| 3 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `LIGHT_SLEEP,STANDBY` |
| 4 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag `system_check_set_operation` |
| 5 | Get Power State Before Reboot | Invoke getPowerStateBeforeReboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Expected `compared against value from step 3` |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `LIGHT_SLEEP,STANDBY` |
| 2 | Set Power State | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |

---

<a id="check_time_zones_persist_after_reboot"></a>
### TestCase Name
Check_Time_Zones_Persist_After_Reboot

### TestCase ID
SYS_31

### TestCase Objective
Checks whether time zone setting is persist after reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 3 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 4 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned after reboot matches the timezone set in step 2, confirming persistence |

---

<a id="system_reboot_and_check_system_uptime"></a>
### TestCase Name
System_Reboot_And_Check_System_Uptime

### TestCase ID
SYS_32

### TestCase Objective
To reboot and check the system uptime

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the system uptime is returned and must not be empty |
| 2 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 3 | Get System Uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | System uptime after reboot is less than `<SYSTEM_UPTIME_IN_SECONDS>` seconds, confirming device rebooted successfully |

---

<a id="system_check_on_timezonedst_changed_event"></a>
### TestCase Name
System_Check_On_TimeZoneDST_Changed_Event

### TestCase ID
SYS_33

### TestCase Objective
Checks whether time zone setting is persist after reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Time Zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.2.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<baseline_timezone>"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<baseline_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) |
| 3 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the baseline timezone set in step 2 |
| 4 | Get TimeZone DST *(loop — repeated for each timezone in the iteration set)* | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current timezone is returned successfully |
| 5 | Set TimeZone DST *(loop)* | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<iteration_timezone>"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<iteration_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 6 | Get TimeZone DST *(loop)* | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Timezone returned matches the timezone set in step 5 for the current iteration |
| 7 | Check On TimeZoneDST Event *(loop)* | Listen for event onTimeZoneDSTChanged (wait up to 2 seconds) after each timezone change in the loop | Event received with `newTimeZone` matching the timezone set in step 5 and `oldTimeZone` matching the timezone captured in step 4 of the same iteration |

---

<a id="system_check_rfc_status"></a>
### TestCase Name
System_Check_RFC_Status

### TestCase ID
SYS_34

### TestCase Objective
Checks whether the RFC value is correctly reflected using getRFCConfig

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check RFC Status | Read current value of TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> from device config and save for reference | Verify that the TR181 parameter value is read from the device successfully |
| 2 | Disable RFC Parameter | Disable TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> on the device via configuration | Confirm that TR181 parameter is disabled successfully |
| 3 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 4 | Get System RFC Config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMETER_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | RFC parameter value returned is `false`, confirming the disabled state persists after reboot |
| 5 | Enable RFC Parameter | Enable TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> on the device via configuration | Confirm that TR181 parameter is enabled successfully |
| 6 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 7 | Get System RFC Config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMETER_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | RFC parameter value returned is `true`, confirming the enabled state persists after reboot |

---

<a id="system_setandget_friendly_name"></a>
### TestCase Name
System_SetandGet_Friendly_Name

### TestCase ID
SYS_35

### TestCase Objective
Check whether able to set and get friendly name

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current friendly name is returned successfully |
| 2 | Set Friendly Name | Invoke setFriendlyName on org.rdk.System with friendlyName: "Test_Value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully (`success` : `true`) |
| 3 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly name returned is `"Test_Value"`, confirming the set in step 2 was applied |
| 4 | Check On Friendly Name Changed Event | Listen for event onFriendlyNameChanged (wait up to 2 seconds) | Event received with `friendlyName`: `"Test_Value"` |

---

<a id="system_check_friendly_name_persist"></a>
### TestCase Name
System_Check_Friendly_Name_Persist

### TestCase ID
SYS_36

### TestCase Objective
Check friendly name is persisting on reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current friendly name is returned successfully |
| 2 | Set Friendly Name | Invoke setFriendlyName on org.rdk.System with friendlyName: "Test_Value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully (`success` : `true`) |
| 3 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 4 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that friendly name `"Test_Value"` persists after reboot and is returned successfully |

---

<a id="system_set_invalid_timezone_dst"></a>
### TestCase Name
System_Set_Invalid_TimeZone_DST

### TestCase ID
SYS_37

### TestCase Objective
Checks whether able to set invalid timezone

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "TestValue1/TestValue2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "TestValue1/TestValue2"}}' http://127.0.0.1:9998/jsonrpc` | `setTimeZoneDST` returns an error response with `success: false` for the invalid timezone `"TestValue1/TestValue2"` |

---

<a id="system_check_rfclist_with_empty_value"></a>
### TestCase Name
System_Check_RFCList_with_Empty_Value

### TestCase ID
SYS_38

### TestCase Objective
Check RFC configurations list with empty value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check RFC Config List Empty | Invoke getRFCConfig on org.rdk.System with rfcList: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": ""}}' http://127.0.0.1:9998/jsonrpc` | `getRFCConfig` with empty `rfcList` returns a valid response (`success` : `true`) with an empty RFC configuration list no error, but no entries returned |

---

<a id="system_check_device_type"></a>
### TestCase Name
System_Check_Device_Type

### TestCase ID
SYS_39

### TestCase Objective
Check the device type of the DUT with getPlatformConfiguration API

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Platform Configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.deviceType"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration", "params": {"query": "DeviceInfo.deviceType"}}' http://127.0.0.1:9998/jsonrpc` | Device type returned matches expected value `<DEVICEINFO_DEVICE_TYPE>` from device config file |

---

<a id="system_check_device_ssh_state_after_reboot_on_standby_state"></a>
### TestCase Name
System_Check_Device_SSH_State_After_Reboot_On_Standby_State

### TestCase ID
SYS_40

### TestCase Objective
Check whether the box sshable or not in standbymode after reboot

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, or `ON` |
| 2 | Set Power State | Invoke setPowerState on org.rdk.System with standbyReason: "APIUnitTest", powerState: "STANDBY"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Power state set to `STANDBY` successfully |
| 3 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `LIGHT_SLEEP` or `STANDBY` |
| 4 | System Reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Reboot triggered successfully (`success` : `true`) |
| 5 | Check Device SSH State | After device is back up, verify the device is SSH-accessible (external function: check_device_ssh_state creates SSH session, retrieves MAC address via ifconfig) | Device is SSH-accessible after reboot in standby state (`Box is SSH able`) |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Power State | Get Power State from System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Expected `LIGHT_SLEEP` or `STANDBY` |
| 2 | Set Power State | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"ON"}}' http://127.0.0.1:9998/jsonrpc` | Power state reverted to `ON` successfully |

---

<a id="system_set_invalid_territory_and_region"></a>
### TestCase Name
System_Set_Invalid_Territory_And_Region

### TestCase ID
SYS_41

### TestCase Objective
Sets invalid territory and region

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke setTerritory on org.rdk.System with territory: "ABC", region: "AB-CD"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "AB-CD"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_empty_territory_and_region"></a>
### TestCase Name
System_Set_Empty_Territory_And_Region

### TestCase ID
SYS_42

### TestCase Objective
Sets empty territory and region

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke setTerritory on org.rdk.System with territory: "", region: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_invalid_territory_and_valid_region"></a>
### TestCase Name
System_Set_Invalid_Territory_And_Valid_Region

### TestCase ID
SYS_43

### TestCase Objective
Sets invalid territory and valid region

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke setTerritory on org.rdk.System with territory: "ABC", region: "US-AS"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_empty_territory_and_valid_region"></a>
### TestCase Name
System_Set_Empty_Territory_And_Valid_Region

### TestCase ID
SYS_44

### TestCase Objective
Sets empty territory and valid region

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Territory | Invoke setTerritory on org.rdk.System with territory: "", region: "US-AS"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_and_get_territory_region"></a>
### TestCase Name
System_Set_And_Get_Territory_Region

### TestCase ID
SYS_45

### TestCase Objective
Check whether able to set and get territory and region

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get territory And region Config File | Read territory and region pairs from device config file <SYSTEM_TERRITORYS> and save for loop iteration | Verify that territory/region pairs are read successfully |
| 2 | System Set Territory | Invoke setTerritory on org.rdk.System with territory: "<territory>", region: "<region>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "<territory>", "region": "<region>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that territory and region are set successfully (`success` : `true`) for each iteration |
| 3 | Check Territory Change Event | Listen for event onTerritoryChanged | Event received with `territory` and `region` matching the values set in step 2 |
| 4 | System Get Territory | Invoke getTerritory on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTerritory"}' http://127.0.0.1:9998/jsonrpc` | Territory and region returned match the values set in step 2 |

---

<a id="system_verify_set_territory_without_params"></a>
### TestCase Name
System_Verify_Set_Territory_without_Params

### TestCase ID
SYS_46

### TestCase Objective
Verify that the setTerritory method returns an error when both territory and region are not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Only Territory | Invoke setTerritory on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory name` |

---

<a id="system_set_valid_territory_and_set_invalid_region"></a>
### TestCase Name
System_Set_Valid_Territory_And_Set_Invalid_Region

### TestCase ID
SYS_47

### TestCase Objective
Check whether able to set valid territory and invalid region to set territory API

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Valid Territory And Set Invalid Region | Invoke setTerritory on org.rdk.System with territory: "CHN", region: "TestingValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": "TestingValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid region` |

---

<a id="system_set_valid_territory_and_set_empty_region"></a>
### TestCase Name
System_Set_Valid_Territory_And_Set_Empty_Region

### TestCase ID
SYS_48

### TestCase Objective
Check whether able to set valid territory and empty region to set territory API

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Set Valid Territory And Set Empty Region | Invoke setTerritory on org.rdk.System with territory: "CHN", region: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | `setTerritory` returns an error response with `success: false` for valid territory `"CHN"` with empty region |

---

<a id="system_get_mfg_serial_number"></a>
### TestCase Name
System_Get_Mfg_Serial_Number

### TestCase ID
SYS_49

### TestCase Objective
Check whether able to get the manufacturing serial number

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System Get Mfg Serial Number | Invoke getMfgSerialNumber on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMfgSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the manufacturing serial number is returned and must not be empty |

---

<a id="system_activatedeactivate_event_test"></a>
### TestCase Name
System_ActivateDeactivate_Event_Test

### TestCase ID
SYS_50

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate System Plugin | Invoke deactivate on Controller with callsign: "org.rdk.System"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for event onStateChanged from Controller (wait up to 2 seconds) | Event received with callsign `org.rdk.System`, state `deactivated`, reason `requested` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate System Plugin | Invoke activate on Controller with callsign: "org.rdk.System"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Check State Change Event | Listen for event onStateChanged from Controller (wait up to 2 seconds) | Event received with callsign `org.rdk.System`, state `activated`, reason `requested` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="system_invalid_set_mode"></a>
### TestCase Name
System_Invalid_Set_Mode

### TestCase ID
SYS_51

### TestCase Objective
Validate by setting up invalid mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Mode | Invoke setMode on org.rdk.System with param: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"param": "INVALID", "duration": 0}}' http://127.0.0.1:9998/jsonrpc` | `setMode` returns an error response with `success: false` for the invalid mode value `"INVALID"` |

---

<a id="system_setandget_empty_friendly_name"></a>
### TestCase Name
System_SetandGet_Empty_Friendly_Name

### TestCase ID
SYS_52

### TestCase Objective
Check whether able to set and get empty friendly name

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the friendly name is returned successfully |
| 2 | Set Friendly Name | Invoke setFriendlyName on org.rdk.System with friendlyName: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": " "}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully |
| 3 | Get Friendly Name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Friendly name returned is a space character `" "`, confirming empty/space name was accepted |
| 4 | Check On Friendly Name Changed Event | Listen for event onFriendlyNameChanged (wait up to 2 seconds) | Event received with `friendlyName`: `" "` (space character) |
| 5 | Set Friendly Name | Invoke setFriendlyName on org.rdk.System with friendlyName: "My Device"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "My Device"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully |

---

<a id="system_invalid_set_power_state"></a>
### TestCase Name
System_Invalid_Set_Power_State

### TestCase ID
SYS_53

### TestCase Objective
Validate by setting up invalid power state

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Power State | Invoke setPowerState on org.rdk.System with powerState: "INVALID", standbyReason: "APIUnitTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "INVALID", "standbyReason": "APIUnitTest"}}' http://127.0.0.1:9998/jsonrpc` | `setPowerState` returns an error response with `success: false` for the invalid power state value `"INVALID"` |

---

<a id="system_invalid_timezone_errorvalidation"></a>
### TestCase Name
System_Invalid_TimeZone_ErrorValidation

### TestCase ID
SYS_54

### TestCase Objective
Set and get Invalid DST time zone

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Expected file not found` |

---

<a id="system_invalid_key_errormessage"></a>
### TestCase Name
System_Invalid_Key_ErrorMessage

### TestCase ID
SYS_55

### TestCase Objective
Validate error message with invalid key in deviceInfo api

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Info | Invoke getDeviceInfo on org.rdk.System with params: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "INVALID"}}' http://127.0.0.1:9998/jsonrpc` | `getDeviceInfo` returns an error response with `success: false` for the invalid key `"INVALID"` |

## Plugin Post-conditions

_No plugin-level post-conditions defined_

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 70 minutes |
| Priority | Medium |
| TDK Release Version | M81 |
