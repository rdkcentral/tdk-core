## TestScript Name
RDKV_CERT_AVS_System

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
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
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **System** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.System` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_System_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onMacAddressesRetreived event | Register a WebSocket event listener for `onMacAddressesRetreived` to receive `onMacAddressesRetreived` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onMacAddressesRetreived", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the onSystemPowerStateChanged event | Register a WebSocket event listener for `onSystemPowerStateChanged` to receive `onSystemPowerStateChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onSystemPowerStateChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the onSystemModeChanged event | Register a WebSocket event listener for `onSystemModeChanged` to receive `onSystemModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onSystemModeChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 4 | Subscribe to the onRebootRequest event | Register a WebSocket event listener for `onRebootRequest` to receive `onRebootRequest` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onRebootRequest", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 5 | Subscribe to the onNetworkStandbyModeChanged event | Register a WebSocket event listener for `onNetworkStandbyModeChanged` to receive `onNetworkStandbyModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onNetworkStandbyModeChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 6 | Subscribe to the onTimeZoneDSTChanged event | Register a WebSocket event listener for `onTimeZoneDSTChanged` to receive `onTimeZoneDSTChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onTimeZoneDSTChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 7 | Subscribe to the onFriendlyNameChanged event | Register a WebSocket event listener for `onFriendlyNameChanged` to receive `onFriendlyNameChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onFriendlyNameChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 8 | Subscribe to the onTerritoryChanged event | Register a WebSocket event listener for `onTerritoryChanged` to receive `onTerritoryChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.register", "params": {"event": "onTerritoryChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 9 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure RFC params | `SYSTEM_RFC_PARAMS` must be set to the RFC parameter names to query from the device | The `SYSTEM_RFC_PARAMS` value should be correctly configured in the device-specific config file |
| 2 | Configure device params | `SYSTEM_DEVICE_PARAMS` must be set to the device property names to retrieve via the System API | The `SYSTEM_DEVICE_PARAMS` value should be correctly configured in the device-specific config file |
| 3 | Configure device details file path | `SYSTEM_DEVICE_DETAILS_FILE_PATH` must be set to the path to the device details cache file on the DUT | The `SYSTEM_DEVICE_DETAILS_FILE_PATH` value should be correctly configured in the device-specific config file |
| 4 | Configure power state managed by device | `SYSTEM_POWER_STATE_MANAGED_BY_DEVICE` must be set to 'true' if power state transitions are managed by the DUT, otherwise 'false' | The `SYSTEM_POWER_STATE_MANAGED_BY_DEVICE` value should be correctly configured in the device-specific config file |
| 5 | Configure supported HDR capabilities | `SYSTEM_SUPPORTED_HDR_CAPABILITIES` must be set to the HDR capabilities supported by the DUT | The `SYSTEM_SUPPORTED_HDR_CAPABILITIES` value should be correctly configured in the device-specific config file |
| 6 | Configure uptime in seconds | `SYSTEM_UPTIME_IN_SECONDS` must be set to the minimum device uptime in seconds required before running uptime-related tests | The `SYSTEM_UPTIME_IN_SECONDS` value should be correctly configured in the device-specific config file |
| 7 | Configure territories | `SYSTEM_TERRITORYS` must be set to the territory and region codes to test in format TERRITORY:REGION | The `SYSTEM_TERRITORYS` value should be correctly configured in the device-specific config file |
| 8 | Configure RFC parameter name | `SYSTEM_RFC_PARAMETER_NAME` must be set to the boolean RFC parameter name from /etc/datamodel.xml for enable/disable testing | The `SYSTEM_RFC_PARAMETER_NAME` value should be correctly configured in the device-specific config file |
| 9 | Configure device features | `SYSTEM_DEVICE_FEATURES` must be set to the system feature names supported by the DUT | The `SYSTEM_DEVICE_FEATURES` value should be correctly configured in the device-specific config file |
| 10 | Configure rf4ce mac | `RF4CE_MAC` must be set to 'enable' if RF4CE MAC is applicable for the DUT, otherwise 'disable' | The `RF4CE_MAC` value should be correctly configured in the device-specific config file |
| 11 | Configure xconf server support | `XCONF_SERVER_SUPPORT` must be set to 'yes' if an XCONF server is available in the test setup, otherwise 'no' | The `XCONF_SERVER_SUPPORT` value should be correctly configured in the device-specific config file |
| 12 | Configure firmware download reboot in seconds | `FIRMWARE_DOWNLOAD_REBOOT_IN_SECONDS` must be set to the maximum device reboot wait time in seconds after firmware download | The `FIRMWARE_DOWNLOAD_REBOOT_IN_SECONDS` value should be correctly configured in the device-specific config file |
| 13 | Configure firmware download protocol | `FIRMWARE_DOWNLOAD_PROTOCOL` must be set to the firmware download protocol used by the XCONF server | The `FIRMWARE_DOWNLOAD_PROTOCOL` value should be correctly configured in the device-specific config file |
| 14 | Configure firmware filename | `FIRMWARE_FILENAME` must be set to the target firmware image filename for the XCONF upgrade test | The `FIRMWARE_FILENAME` value should be correctly configured in the device-specific config file |
| 15 | Configure firmware location | `FIRMWARE_LOCATION` must be set to the base URL of the server hosting the firmware image | The `FIRMWARE_LOCATION` value should be correctly configured in the device-specific config file |
| 16 | Configure firmware version | `FIRMWARE_VERSION` must be set to the target firmware version expected after the XCONF upgrade | The `FIRMWARE_VERSION` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="system_get_estb_mac"></a>
### TestCase Name
System_Get_ESTB_MAC

### TestCase ID
SYS_01

### TestCase Objective
Get requested device detail

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device ESTB MAC | Invoke getDeviceInfo on org.rdk.System with params: "<SYSTEM_DEVICE_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that device info response for `<SYSTEM_DEVICE_PARAMS>` is returned successfully and the value must not be empty |

---

<a id="system_get_serial_number"></a>
### TestCase Name
System_Get_Serial_Number

### TestCase ID
SYS_02

### TestCase Objective
Gets the serial number

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device serial no | Invoke getSerialNumber on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the serial number is returned successfully |

---

<a id="system_get_version"></a>
### TestCase Name
System_Get_Version

### TestCase ID
SYS_03

### TestCase Objective
Gets system version details

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get system version | Invoke getSystemVersions on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSystemVersions"}' http://127.0.0.1:9998/jsonrpc` | Verify that system versions are returned successfully |

---

<a id="system_get_uptime"></a>
### TestCase Name
System_Get_Uptime

### TestCase ID
SYS_04

### TestCase Objective
Get the uptime of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get system uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the uptime value is returned and must not be empty  |

---

<a id="system_get_rfc_config"></a>
### TestCase Name
System_Get_RFC_Config

### TestCase ID
SYS_05

### TestCase Objective
Gets RFC configurations

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get system RFC config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that RFC config is returned successfully |

---

<a id="system_setandget_power_state"></a>
### TestCase Name
System_SetAndGet_Power_State

### TestCase ID
SYS_06

### TestCase Objective
Set and get device power state

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set power state | Invoke setPowerState on org.rdk.System with standbyReason: "APIUnitTest", powerState: "STANDBY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is set to `STANDBY` successfully  |
| 3 | Power state changed event | Listen for event onSystemPowerStateChanged (wait up to 30 seconds) | Verify that the `onSystemPowerStateChanged` event is received with the new state matching `STANDBY` (the value set in step 2)  |
| 4 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state returned is `STANDBY`, confirming the set operation in step 2 was successful  |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON` |
| 2 | Set power state | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "APIUnitTest", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is reverted to `ON` successfully, restoring the original state  |
| 3 | Check power state | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state returned is `ON`, confirming the device is restored to its original state  |

---

<a id="system_setandget_timezone_dst"></a>
### TestCase Name
System_SetAndGet_TimeZone_DST

### TestCase ID
SYS_07

### TestCase Objective
Set and get DST time zone

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "America/New_York"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "America/New_York"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the time zone DST is set successfully |
| 2 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the timezone is set to `America/New_York` as expected  |

---

<a id="system_set_normal_mode"></a>
### TestCase Name
System_Set_NORMAL_Mode

### TestCase ID
SYS_08

### TestCase Objective
Set STB mode to NORMAL

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set STB mode NORMAL | Invoke setMode on org.rdk.System with duration: 10, mode: "NORMAL"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": 10, "mode": "NORMAL"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the mode is set successfully |

---

<a id="system_getmac_address"></a>
### TestCase Name
System_GetMac_Address

### TestCase ID
SYS_09

### TestCase Objective
Get Mac Address

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device MAC addresses | Invoke getMacAddresses on org.rdk.System with GUID: "61734787891723481"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMacAddresses", "params": {"GUID": "61734787891723481"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `asyncResponse` is `true` and `success` is `true`, confirming the async MAC address retrieval was triggered successfully  |
| 2 | Check mac address | Listen for event onMacAddressesRetrieved (wait up to 2 seconds for async response) | Verify that the event is received and all MAC address fields (`ECM_MAC`, `ESTB_MAC`, `MOCA_MAC`, `ETH_MAC`, `WIFI_MAC`, `BLUETOOTH_MAC`) are present and valid  |

---

<a id="system_get_image_version"></a>
### TestCase Name
System_Get_Image_Version

### TestCase ID
SYS_10

### TestCase Objective
Gets the image version

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device image version | Invoke getDeviceInfo on org.rdk.System with params: "imageVersion"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "imageVersion"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `imageVersion` is returned successfully and must not be empty  |

---

<a id="system_get_model_number"></a>
### TestCase Name
System_Get_model_number

### TestCase ID
SYS_11

### TestCase Objective
Gets the model number

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device model number | Invoke getDeviceInfo on org.rdk.System with params: "model_number"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "model_number"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `model_number` is returned successfully and must not be empty  |

---

<a id="system_get_boxip"></a>
### TestCase Name
System_Get_boxIP

### TestCase ID
SYS_12

### TestCase Objective
Gets the box IP

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device boxIP | Invoke getDeviceInfo on org.rdk.System with params: "boxIP"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "boxIP"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `boxIP` value is returned successfully and must not be empty  |

---

<a id="system_get_build_type"></a>
### TestCase Name
System_Get_build_type

### TestCase ID
SYS_13

### TestCase Objective
Gets the build type

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device build type | Invoke getDeviceInfo on org.rdk.System with params: "build_type"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "build_type"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `build_type` value is returned successfully and must not be empty  |

---

<a id="system_get_eth_mac"></a>
### TestCase Name
System_Get_eth_mac

### TestCase ID
SYS_14

### TestCase Objective
Gets eth mac of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device eth mac | Invoke getDeviceInfo on org.rdk.System with params: "eth_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "eth_mac"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `eth_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address  |

---

<a id="system_get_rf4ce_mac"></a>
### TestCase Name
System_Get_rf4ce_mac

### TestCase ID
SYS_15

### TestCase Objective
Gets the rf4ce mac of the device

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device rf4ce mac | Invoke getDeviceInfo on org.rdk.System with params: "rf4ce_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "rf4ce_mac"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `rf4ce_mac` value is returned successfully and must not be empty (8-byte RF4CE MAC format)  |

---

<a id="system_get_bluetooth_mac"></a>
### TestCase Name
System_Get_Bluetooth_mac

### TestCase ID
SYS_16

### TestCase Objective
Gets device bluetooth mac

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device Bluetooth mac | Invoke getDeviceInfo on org.rdk.System with params: "bluetooth_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "bluetooth_mac"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `bluetooth_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address  |

---

<a id="system_get_wifi_mac"></a>
### TestCase Name
System_Get_WiFi_Mac

### TestCase ID
SYS_17

### TestCase Objective
Gets device WiFi mac

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device WiFi mac | Invoke getDeviceInfo on org.rdk.System with params: "wifi_mac"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "wifi_mac"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `wifi_mac` value is returned and validated against MAC format `[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$` must be a valid non-empty MAC address  |

---

<a id="check_power_state_before_reboot"></a>
### TestCase Name
Check_Power_State_Before_Reboot

### TestCase ID
SYS_18

### TestCase Objective
Checks the powerstate before reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is returned successfully and must be one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, `ON`, saved for comparison in step 3 |
| 2 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 3 | Get power state before reboot | Invoke getPowerStateBeforeReboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state before reboot matches the state recorded in step 1  |

---

<a id="system_check_on_systemmode_changed"></a>
### TestCase Name
System_Check_On_SystemMode_Changed

### TestCase ID
SYS_19

### TestCase Objective
Checks for the system mode changed event

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set STB mode WAREHOUSE | Invoke setMode on org.rdk.System with mode: "WAREHOUSE", duration: 5<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"duration": 5, "mode": "WAREHOUSE"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the mode is set to `WAREHOUSE` successfully with `success`: `true`  |
| 2 | Check on SystemMode changed event | Listen for event onSystemModeChanged (triggered immediately when mode is set to WAREHOUSE) | Verify that the event is received with `mode` as `"WAREHOUSE"`, confirming the warehouse mode was set  |
| 3 | Check on SystemMode changed event | Listen for event onSystemModeChanged (wait up to 5 seconds for auto-revert) | Verify that the event is received with `mode` as `"NORMAL"`, confirming automatic revert after the duration expires  |

---

<a id="system_check_reboot_reason_event"></a>
### TestCase Name
System_Check_Reboot_Reason_Event

### TestCase ID
SYS_20

### TestCase Objective
Retrieve basic information about a reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Initiate system reboot | Invoke reboot on org.rdk.System with rebootReason: "API Validation"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot", "params": {"rebootReason": "API Validation"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 2 | Check on reboot request event | Listen for event onRebootRequest (wait up to 60 seconds) | Verify that the event is received with `rebootReason` as `"API Validation"` and `requestedApp` as `"SystemServices"`  |

---

<a id="enable_and_disable_telemetry_optout_status"></a>
### TestCase Name
Enable_And_Disable_Telemetry_OptOut_Status

### TestCase ID
SYS_21

### TestCase Objective
Checks whether able to enable and disable the telemetry opt-out status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get OptOut telemetry status | Invoke isOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | Verify that the `optOut` status is returned successfully as `true` or `false` saved for revert  |
| 2 | Set OptOut telemetry status | Invoke setOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setOptOutTelemetry", "params": {"Opt-Out": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the telemetry opt-out status is set successfully (`success` : `true`) for each iteration |
| 3 | Get OptOut telemetry status | Invoke isOptOutTelemetry on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.isOptOutTelemetry"}' http://127.0.0.1:9998/jsonrpc` | Verify that the `optOut` value matches the value set in step 2 for the current iteration (`true` then `false`)  |

---

<a id="system_validate_firmware_upgrade"></a>
### TestCase Name
System_Validate_Firmware_Upgrade

### TestCase ID
SYS_22

### TestCase Objective
Upgrades to specified firmware version

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check version file | SSH to device and verify `/version.txt` exists (`[ -f "/version.txt" ] && echo 1 \|\| echo 0`) and is not empty (`[ -s "/version.txt" ] && echo 1 \|\| echo 0`) before the firmware upgrade test begins | Verify that `/version.txt` exists and is not empty on the device before the upgrade begins |
| 2 | Get downloaded firmware info | Invoke getDownloadedFirmwareInfo on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current firmware version is returned and saved successfully (e.g., `lib32-rdk-fullstack-image-<MODEL>-<TIMESTAMP>`) |
| 3 | Get model name | SSH to device and read `model_number` from device details cache file `<SYSTEM_DEVICE_DETAILS_FILE_PATH>`: `grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs` model string is saved for XCONF rule targeting | Verify that the model number (e.g., `RPI4`) is read from the device cache file and saved successfully |
| 4 | Check existing model ID | Query XCONF REST API: `GET /xconfAdminService/queries/models/TDK_{MODEL}_TEST_MODEL` using the model name from step 3 checks whether a model ID entry already exists for this device | Verify that the XCONF query executes successfully; existing model ID is returned and saved (or `null` if not found triggers step 5) |
| 5 | Create new model ID | *(Conditional statement executed only if previous step condition is met)*<br>Create model ID rule in XCONF: `POST /xconfAdminService/updates/models` with the model name from step 3 | Verify that new model ID rule `TDK_{MODEL}_TEST_MODEL` is created in XCONF successfully (step skipped if model ID already existed in step 4) |
| 6 | Check existing firmware configuration | Query XCONF REST API: `GET /xconfAdminService/queries/firmwares/model/TDK_{MODEL}_TEST_MODEL?applicationType=stb` checks whether a firmware configuration already exists for this model | Verify that the XCONF query executes successfully; existing firmware configuration is returned and saved (or empty triggers step 7) |
| 7 | Create new firmware configuration | *(Conditional statement executed only if previous step condition is met)*<br>Create firmware configuration in XCONF: `POST /xconfAdminService/updates/firmwares` linking the model to target firmware `<FIRMWARE_VERSION>` | Verify that new firmware configuration `TDK_{MODEL}_TEST_FIRMWARE_CONFIGURATION` is created in XCONF successfully (step skipped if configuration already existed in step 6) |
| 8 | Get ESTB MAC | Invoke getDeviceInfo on org.rdk.System with params: `<SYSTEM_DEVICE_PARAMS>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "<SYSTEM_DEVICE_PARAMS>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the ESTB MAC address is returned with `success`: `true` and the MAC value is non-empty saved for use in steps 9–12 |
| 9 | Check existing firmware rule | Query XCONF REST API: `GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_RULE&applicationType=stb&templateId=MAC_RULE` using ESTB MAC from step 8, model from step 3, and firmware config from step 6/7 | Verify that the XCONF query executes successfully; existing firmware rule is returned and saved (or `null` if not found triggers step 10) |
| 10 | Create new firmware rule | *(Conditional statement executed only if previous step condition is met)*<br>Create MAC-based firmware rule in XCONF: `POST /xconfAdminService/firmwarerule/importAll?applicationType=stb` with condition `eStbMac IS <ESTB_MAC>`, configId from step 6/7, and `rebootImmediately: true` | Verify that new firmware rule `TDK_{MODEL}_TEST_FIRMWARE_RULE` is imported to XCONF with `IMPORTED` list non-empty (step skipped if rule already existed in step 9) |
| 11 | Check existing firmware local server rule | Query XCONF REST API: `GET /xconfAdminService/firmwarerule/filtered?name=TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE&applicationType=stb&templateId=DOWNLOAD_LOCATION_FILTER` checks if a local server download filter rule exists for this device | Verify that the XCONF query executes successfully; existing local server rule is returned and saved (or `null` if not found triggers step 12) |
| 12 | Create new firmware local server rule | *(Conditional statement executed only if previous step condition is met)*<br>Create `DOWNLOAD_LOCATION_FILTER` rule in XCONF: `POST /xconfAdminService/firmwarerule/importAll?applicationType=stb` with `firmwareLocation`, `firmwareDownloadProtocol: http`, matching device ESTB MAC from step 8 | Verify that new local server rule `TDK_{MODEL}_TEST_FIRMWARE_LOCAL_SERVER_RULE` is imported to XCONF with `IMPORTED` list non-empty (step skipped if rule already existed in step 11) |
| 13 | Check disk partition | SSH to device and count disk partitions: `ls /dev/mmcblk0* \| wc -l` partition count = `4` routes through steps 14–15 (reboot-based upgrade path); count ≠ `4` skips directly to step 16 (direct upgrade path) | Verify that the disk partition count is retrieved and saved successfully (e.g., `5`); routing to upgrade path determined by this value |
| 14 | Update firmware (upgrade partition path) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | Verify that `updateFirmware` returns `success`: `true` and the device reboots to start downloading new firmware (step skipped if partition count ≠ 4 in step 13) |
| 15 | Check disk partition (post-upgrade-reboot) | *(Conditional statement executed only if previous step condition is met)*<br>SSH to device after reconnection from the reboot in step 14: `ls /dev/mmcblk0* \| wc -l` verifies partition count after the reboot-based upgrade; expected count = `4` | Verify that the disk partition count is `4` after the reboot-based upgrade step, confirming the partition upgrade path completed (step skipped if partition count ≠ 4 in step 13) |
| 16 | Update firmware (upgrade direct trigger) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | Verify that `updateFirmware` returns `success`: `true` and firmware download to the target version begins |
| 17 | Check current version (verify upgrade) | *(Waits for `FIRMWARE_DOWNLOAD_REBOOT_IN_SECONDS` seconds as configured in the device config file before executing allows time for firmware download and device reboot to complete)*<br>Invoke getDownloadedFirmwareInfo on org.rdk.System after firmware download and reboot completes<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the downloaded firmware version matches `<FIRMWARE_VERSION>` from the device config file, confirming successful upgrade to the new firmware |
| 18 | Check time sync (post-upgrade) | SSH to device and run `date` to get DUT UTC time compare against the actual current UTC time to verify time sync is active after the upgrade reboot | Verify that DUT UTC time matches current UTC time within 1 minute, confirming NTP/time sync is active on the upgraded firmware |
| 19 | Check version file (post-upgrade) | SSH to device and verify `/version.txt` exists (`[ -f "/version.txt" ] && echo 1 \|\| echo 0`) and is not empty (`[ -s "/version.txt" ] && echo 1 \|\| echo 0`) after upgrade reboot | Verify that `/version.txt` exists and is not empty on the upgraded firmware, confirming the version file is present post-upgrade |
| 20 | Update firmware configuration (prepare revert) | Query XCONF for current firmware configuration (`GET /xconfAdminService/queries/firmwares/model/{MODEL}`), then update it (`PUT /xconfAdminService/updates/firmwares`) sets `firmwareFilename` to the original image filename derived from the firmware version saved in step 2, so that steps 21–26 will download the original firmware back | Verify that the XCONF firmware configuration is updated successfully with the original firmware filename and the result contains `update_existing_rule` with the original image name from step 2 |
| 21 | Check disk partition (before revert) | SSH to device and count disk partitions: `ls /dev/mmcblk0* \| wc -l` partition count = `4` routes through steps 22–23 (reboot-based revert path); count ≠ `4` skips directly to step 24 (direct revert path) | Verify that the disk partition count is retrieved and saved successfully (e.g., `5`); routing to revert path determined by this value |
| 22 | Update firmware (revert partition path) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | Verify that `updateFirmware` returns `success`: `true` and the device reboots to start downloading the original firmware (step skipped if partition count ≠ 4 in step 21) |
| 23 | Check disk partition (post-revert-reboot) | *(Conditional statement executed only if previous step condition is met)*<br>SSH to device after reconnection from the reboot in step 22: `ls /dev/mmcblk0* \| wc -l` verifies partition count after the reboot-based revert; expected count = `4` | Verify that the disk partition count is `4` after the reboot-based revert step, confirming the partition revert path completed (step skipped if partition count ≠ 4 in step 21) |
| 24 | Update firmware (revert direct trigger) | Invoke updateFirmware on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.updateFirmware"}' http://127.0.0.1:9998/jsonrpc` | Verify that `updateFirmware` returns `success`: `true` and the original firmware download begins |
| 25 | Check current version (verify revert) | Invoke getDownloadedFirmwareInfo on org.rdk.System after revert download and reboot completes<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDownloadedFirmwareInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the downloaded firmware version matches the original firmware version saved in step 2, confirming successful revert to the original firmware |
| 26 | Check time sync (post-revert) | SSH to device and run `date` to get DUT UTC time compare against the actual current UTC time to verify time sync is active after the revert reboot | Verify that DUT UTC time matches current UTC time within 1 minute, confirming time sync is active on the reverted firmware |

---

<a id="system_check_model_number"></a>
### TestCase Name
System_Check_Model_Number

### TestCase ID
SYS_23

### TestCase Objective
Checks the model number of the DUT

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device details | SSH to device: grep model_number /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs reads the model_number field from the device details cache file (path from config key SYSTEM_DEVICE_DETAILS_FILE_PATH) | Verify that the model number is read from the device cache file successfully |
| 2 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.model"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.model"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `MODEL_NUMBER` returned by `getPlatformConfiguration` matches the `model_number` value read from device cache file in step 1  |

---

<a id="system_check_device_mac_address"></a>
### TestCase Name
System_Check_Device_Mac_Address

### TestCase ID
SYS_24

### TestCase Objective
Checks the device MAC address

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device details | SSH to device: grep estb_mac /tmp/.deviceDetails.cache \| cut -d'=' -f2- \| xargs reads the estb_mac field from the device details cache file (path from config key SYSTEM_DEVICE_DETAILS_FILE_PATH) | Verify that the ESTB MAC address is read from the device cache file successfully |
| 2 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "AccountInfo.deviceMACAddress"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.deviceMACAddress"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `deviceMACAddress` returned by `getPlatformConfiguration` matches the `estb_mac` value read from device cache file in step 1  |

---

<a id="system_check_firmware_upgrade_status"></a>
### TestCase Name
System_Check_Firmware_Upgrade_Status

### TestCase ID
SYS_25

### TestCase Objective
Checks the firmware upgrade status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get SWUpdate file status | SSH to device: [ -f "/opt/swupdate.conf" ] && echo 1 \|\| echo 0 checks whether /opt/swupdate.conf exists; if file exists → FIRMWARE_UPGRADE_STATUS: true; if not → FIRMWARE_UPGRADE_STATUS: false result saved for comparison in step 2 | Verify that the `/opt/swupdate.conf` presence is checked successfully `FIRMWARE_UPGRADE_STATUS` saved (`true` or `false`)  |
| 2 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "AccountInfo.firmwareUpdateDisabled"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "AccountInfo.firmwareUpdateDisabled"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `firmwareUpdateDisabled` value returned by `getPlatformConfiguration` matches the `FIRMWARE_UPGRADE_STATUS` read from `/opt/swupdate.conf` in step 1  |

---

<a id="system_check_public_ip_address"></a>
### TestCase Name
System_Check_Public_IP_Address

### TestCase ID
SYS_26

### TestCase Objective
Checks the public IP address

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get public IP address | SSH to device: curl -s ifconfig.me fetches the device's public IP address from the external service; result saved as PUBLIC_IP for comparison in step 2 | Verify that the public IP address is retrieved from the device successfully |
| 2 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.publicIP"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.2.getPlatformConfiguration", "params": {"query": "DeviceInfo.publicIP"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `publicIP` returned by `getPlatformConfiguration` matches the `PUBLIC_IP` value is retrieved via `ifconfig.me` in step 1  |

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

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |

#### TestCase Pre-condition 2: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration"}' http://127.0.0.1:9998/jsonrpc` | Verify that the HDR capabilities returned match the expected value `<SYSTEM_SUPPORTED_HDR_CAPABILITIES>` from the device config file  |

---

<a id="setandget_all_time_zones"></a>
### TestCase Name
SetAndGet_All_Time_Zones

### TestCase ID
SYS_28

### TestCase Objective
Set and get all the time zones

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get time zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 3 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the timezone returned matches the timezone set in the current iteration  |

---

<a id="system_toggle_network_standby_mode_status"></a>
### TestCase Name
System_Toggle_Network_Standby_Mode_Status

### TestCase ID
SYS_29

### TestCase Objective
Toggle Network Standby Mode Status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current network standby mode is returned as `true` or `false` and saved as the baseline for toggle  |
| 2 | Set network standby mode | Invoke setNetworkStandbyMode on org.rdk.System with nwStandby: "<toggled_from_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setNetworkStandbyMode", "params": {"nwStandby": "<toggled_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that network standby mode is set successfully (`success` : `true`) |
| 3 | Get network standby mode | Invoke getNetworkStandbyMode on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getNetworkStandbyMode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the network standby mode returned matches the toggled value (opposite of step 1)  |
| 4 | Check network standby mode changed event | Listen for event onNetworkStandbyModeChanged (wait up to 3 seconds) | Verify that the event is received with `nwStandby` matching the toggled value set in step 2  |

---

<a id="check_power_state_before_reboot_on_standby_state"></a>
### TestCase Name
Check_Power_State_Before_Reboot_On_Standby_State

### TestCase ID
SYS_30

### TestCase Objective
Checks the powerstate before reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is returned successfully |
| 2 | Set power state | Invoke setPowerState on org.rdk.System with standbyReason: "<value>", powerState: "STANDBY"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |
| 3 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported power states include `LIGHT_SLEEP` and `STANDBY`  |
| 4 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the set operation on System API is completed and validated successfully  |
| 5 | Get power state before reboot | Invoke getPowerStateBeforeReboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerStateBeforeReboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the value captured in step 3  |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported power states include `LIGHT_SLEEP` and `STANDBY`  |
| 2 | Set power state | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "<value>", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the power state is set successfully |

---

<a id="check_time_zones_persist_after_reboot"></a>
### TestCase Name
Check_Time_Zones_Persist_After_Reboot

### TestCase ID
SYS_31

### TestCase Objective
Checks whether time zone setting is persist after reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get time zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 3 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 4 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the timezone returned after reboot matches the timezone set in step 2, confirming persistence across reboots  |

---

<a id="system_reboot_and_check_system_uptime"></a>
### TestCase Name
System_Reboot_And_Check_System_Uptime

### TestCase ID
SYS_32

### TestCase Objective
To reboot and check the system uptime

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get system uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the system uptime is returned and must not be empty |
| 2 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 3 | Get system uptime | Invoke requestSystemUptime on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.requestSystemUptime"}' http://127.0.0.1:9998/jsonrpc` | Verify that the system uptime after reboot is less than `<SYSTEM_UPTIME_IN_SECONDS>` seconds, confirming the device rebooted successfully  |

---

<a id="system_check_on_timezonedst_changed_event"></a>
### TestCase Name
System_Check_On_TimeZoneDST_Changed_Event

### TestCase ID
SYS_33

### TestCase Objective
Checks whether time zone setting is persist after reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get time zones | Invoke getTimeZones on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.2.getTimeZones"}' http://127.0.0.1:9998/jsonrpc` | Verify that the full list of supported time zones is returned successfully |
| 2 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<baseline_timezone>"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<baseline_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) |
| 3 | Get TimeZone DST | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the timezone returned matches the baseline timezone set in step 2  |
| 4 | Get TimeZone DST *(loop repeated for each timezone in the iteration set)* | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current timezone is returned successfully |
| 5 | Set TimeZone DST *(loop)* | Invoke setTimeZoneDST on org.rdk.System with timeZone: "<iteration_timezone>"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setTimeZoneDST","params":{"timeZone":"<iteration_timezone>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that timezone is set successfully (`success` : `true`) for each iteration |
| 6 | Get TimeZone DST *(loop)* | Invoke getTimeZoneDST on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getTimeZoneDST"}' http://127.0.0.1:9998/jsonrpc` | Verify that the timezone returned matches the timezone set in step 5 for the current iteration  |
| 7 | Check on TimeZoneDST event *(loop)* | Listen for event onTimeZoneDSTChanged (wait up to 2 seconds) after each timezone change in the loop | Verify that the event is received with `newTimeZone` matching the timezone set in step 5 and `oldTimeZone` matching the timezone captured in step 1  |

---

<a id="system_check_rfc_status"></a>
### TestCase Name
System_Check_RFC_Status

### TestCase ID
SYS_34

### TestCase Objective
Checks whether the RFC value is correctly reflected using getRFCConfig

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check RFC status | Read current value of TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> from device config and save for reference | Verify that the TR181 parameter value is read from the device successfully |
| 2 | Disable RFC parameter | Disable TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> on the device via configuration | Confirm that TR181 parameter is disabled successfully |
| 3 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 4 | Get system RFC config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMETER_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the RFC parameter value returned is `false`, confirming the disabled state persists after reboot  |
| 5 | Enable RFC parameter | Enable TR181 parameter <SYSTEM_RFC_PARAMETER_NAME> on the device via configuration | Confirm that TR181 parameter is enabled successfully |
| 6 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 7 | Get system RFC config | Invoke getRFCConfig on org.rdk.System with rfcList: "<SYSTEM_RFC_PARAMETER_NAME>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": "<SYSTEM_RFC_PARAMETER_NAME>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the RFC parameter value returned is `true`, confirming the enabled state persists after reboot  |

---

<a id="system_setandget_friendly_name"></a>
### TestCase Name
System_SetandGet_Friendly_Name

### TestCase ID
SYS_35

### TestCase Objective
Check whether able to set and get friendly name

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current friendly name is returned successfully |
| 2 | Set friendly name | Invoke setFriendlyName on org.rdk.System with friendlyName: "Test_Value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully (`success` : `true`) |
| 3 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the friendly name returned is `"Test_Value"`, confirming the value set in step 2 was applied successfully  |
| 4 | Check on friendly name changed event | Listen for event onFriendlyNameChanged (wait up to 2 seconds) | Verify that the event is received with `friendlyName` as `"Test_Value"`, confirming the new name was applied  |

---

<a id="system_check_friendly_name_persist"></a>
### TestCase Name
System_Check_Friendly_Name_Persist

### TestCase ID
SYS_36

### TestCase Objective
Check friendly name is persisting on reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current friendly name is returned successfully |
| 2 | Set friendly name | Invoke setFriendlyName on org.rdk.System with friendlyName: "Test_Value"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "Test_Value"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully (`success` : `true`) |
| 3 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 4 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that friendly name `"Test_Value"` persists after reboot and is returned successfully |

---

<a id="system_set_invalid_timezone_dst"></a>
### TestCase Name
System_Set_Invalid_TimeZone_DST

### TestCase ID
SYS_37

### TestCase Objective
Checks whether able to set invalid timezone

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set TimeZone DST | Invoke setTimeZoneDST on org.rdk.System with timeZone: "TestValue1/TestValue2"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTimeZoneDST", "params": {"timeZone": "TestValue1/TestValue2"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `setTimeZoneDST` returns an error response with `success: false` for the invalid timezone `"TestValue1/TestValue2"`  |

---

<a id="system_check_rfclist_with_empty_value"></a>
### TestCase Name
System_Check_RFCList_with_Empty_Value

### TestCase ID
SYS_38

### TestCase Objective
Check RFC configurations list with empty value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check RFC config list empty | Invoke getRFCConfig on org.rdk.System with rfcList: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getRFCConfig", "params": {"rfcList": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `getRFCConfig` with empty `rfcList` returns a valid response (`success` : `true`) with an empty RFC configuration list no error, but no entries returned  |

---

<a id="system_check_device_type"></a>
### TestCase Name
System_Check_Device_Type

### TestCase ID
SYS_39

### TestCase Objective
Check the device type of the DUT with getPlatformConfiguration API

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get platform configuration | Invoke getPlatformConfiguration on org.rdk.System with query: "DeviceInfo.deviceType"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPlatformConfiguration", "params": {"query": "DeviceInfo.deviceType"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the device type returned matches the expected value `<DEVICEINFO_DEVICE_TYPE>` from the device config file  |

---

<a id="system_check_device_ssh_state_after_reboot_on_standby_state"></a>
### TestCase Name
System_Check_Device_SSH_State_After_Reboot_On_Standby_State

### TestCase ID
SYS_40

### TestCase Objective
Check whether the box sshable or not in standbymode after reboot

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the current power state is one of `STANDBY`, `DEEP_SLEEP`, `LIGHT_SLEEP`, or `ON` |
| 2 | Set power state | Invoke setPowerState on org.rdk.System with standbyReason: "APIUnitTest", powerState: "STANDBY"<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"STANDBY"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is set to `STANDBY` successfully  |
| 3 | Get power state | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned power state is either `LIGHT_SLEEP` or `STANDBY` as expected  |
| 4 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that the reboot is triggered successfully with `success`: `true`  |
| 5 | Check device SSH state | After device is back up, verify the device is SSH-accessible (external function: check_device_ssh_state creates SSH session, retrieves MAC address via ifconfig) | Verify that the device is SSH-accessible after reboot in standby state (confirms remote access is restored)  |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned power state is either `LIGHT_SLEEP` or `STANDBY` as expected  |
| 2 | Set power state | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc":"2.0","id":3,"method":"org.rdk.System.1.setPowerState","params":{"standbyReason":"APIUnitTest","powerState":"ON"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the power state is reverted to `ON` successfully, restoring the original state  |

---

<a id="system_set_invalid_territory_and_region"></a>
### TestCase Name
System_Set_Invalid_Territory_And_Region

### TestCase ID
SYS_41

### TestCase Objective
Sets invalid territory and region

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set territory | Invoke setTerritory on org.rdk.System with territory: "ABC", region: "AB-CD"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "AB-CD"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_empty_territory_and_region"></a>
### TestCase Name
System_Set_Empty_Territory_And_Region

### TestCase ID
SYS_42

### TestCase Objective
Sets empty territory and region

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set territory | Invoke setTerritory on org.rdk.System with territory: "", region: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_invalid_territory_and_valid_region"></a>
### TestCase Name
System_Set_Invalid_Territory_And_Valid_Region

### TestCase ID
SYS_43

### TestCase Objective
Sets invalid territory and valid region

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set territory | Invoke setTerritory on org.rdk.System with territory: "ABC", region: "US-AS"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "ABC", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_empty_territory_and_valid_region"></a>
### TestCase Name
System_Set_Empty_Territory_And_Valid_Region

### TestCase ID
SYS_44

### TestCase Objective
Sets empty territory and valid region

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set territory | Invoke setTerritory on org.rdk.System with territory: "", region: "US-AS"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "", "region": "US-AS"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory` |

---

<a id="system_set_and_get_territory_region"></a>
### TestCase Name
System_Set_And_Get_Territory_Region

### TestCase ID
SYS_45

### TestCase Objective
Check whether able to set and get territory and region

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get territory and region config file | Read territory and region pairs from device config file <SYSTEM_TERRITORYS> and save for loop iteration | Verify that territory/region pairs are read successfully |
| 2 | System set territory | Invoke setTerritory on org.rdk.System with territory: "<territory>", region: "<region>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "<territory>", "region": "<region>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that territory and region are set successfully (`success` : `true`) for each iteration |
| 3 | Check territory change event | Listen for event onTerritoryChanged | Verify that the event is received with `territory` and `region` matching the values set in step 2  |
| 4 | System get territory | Invoke getTerritory on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getTerritory"}' http://127.0.0.1:9998/jsonrpc` | Verify that the territory and region returned match the values set in step 2  |

---

<a id="system_verify_set_territory_without_params"></a>
### TestCase Name
System_Verify_Set_Territory_without_Params

### TestCase ID
SYS_46

### TestCase Objective
Verify that the setTerritory method returns an error when both territory and region are not provided

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set only territory | Invoke setTerritory on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid territory name` |

---

<a id="system_set_valid_territory_and_set_invalid_region"></a>
### TestCase Name
System_Set_Valid_Territory_And_Set_Invalid_Region

### TestCase ID
SYS_47

### TestCase Objective
Check whether able to set valid territory and invalid region to set territory API

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set valid territory and set invalid region | Invoke setTerritory on org.rdk.System with territory: "CHN", region: "TestingValue"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": "TestingValue"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `invalid region` |

---

<a id="system_set_valid_territory_and_set_empty_region"></a>
### TestCase Name
System_Set_Valid_Territory_And_Set_Empty_Region

### TestCase ID
SYS_48

### TestCase Objective
Check whether able to set valid territory and empty region to set territory API

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System set valid territory and set empty region | Invoke setTerritory on org.rdk.System with territory: "CHN", region: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setTerritory", "params": {"territory": "CHN", "region": ""}}' http://127.0.0.1:9998/jsonrpc` | Verify that `setTerritory` returns an error response with `success: false` for valid territory `"CHN"` with empty region  |

---

<a id="system_get_mfg_serial_number"></a>
### TestCase Name
System_Get_Mfg_Serial_Number

### TestCase ID
SYS_49

### TestCase Objective
Check whether able to get the manufacturing serial number

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | System get mfg serial number | Invoke getMfgSerialNumber on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getMfgSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the manufacturing serial number is returned and must not be empty |

---

<a id="system_activatedeactivate_event_test"></a>
### TestCase Name
System_ActivateDeactivate_Event_Test

### TestCase ID
SYS_50

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate system plugin | Invoke deactivate on Controller with callsign: "org.rdk.System"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for event onStateChanged from Controller (wait up to 2 seconds) | Verify that the event is received with callsign `org.rdk.System`, state `deactivated`, and reason `requested`  |
| 3 | Check plugin active status | Invoke status on Controller for org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate system plugin | Invoke activate on Controller with callsign: "org.rdk.System"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 5 | Check state change event | Listen for event onStateChanged from Controller (wait up to 2 seconds) | Verify that the event is received with callsign `org.rdk.System`, state `activated`, and reason `requested`  |
| 6 | Check plugin active status | Invoke status on Controller for org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="system_invalid_set_mode"></a>
### TestCase Name
System_Invalid_Set_Mode

### TestCase ID
SYS_51

### TestCase Objective
Validate by setting up invalid mode

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set system mode with invalid parameter (error case) | Invoke setMode on org.rdk.System with param: "INVALID", duration: 0<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setMode", "params": {"param": "INVALID", "duration": 0}}' http://127.0.0.1:9998/jsonrpc` | Verify that `setMode` returns an error response with `success: false` for the invalid mode value `"INVALID"`  |

---

<a id="system_setandget_empty_friendly_name"></a>
### TestCase Name
System_SetandGet_Empty_Friendly_Name

### TestCase ID
SYS_52

### TestCase Objective
Check whether able to set and get empty friendly name

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the friendly name is returned successfully |
| 2 | Set friendly name | Invoke setFriendlyName on org.rdk.System with friendlyName: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": " "}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully |
| 3 | Get friendly name | Invoke getFriendlyName on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getFriendlyName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the friendly name returned is a space character `" "`, confirming that an empty/space name is accepted  |
| 4 | Check on friendly name changed event | Listen for event onFriendlyNameChanged (wait up to 2 seconds) | Verify that the event is received with `friendlyName` as `" "` (space character), confirming an empty/space name was accepted  |
| 5 | Set friendly name | Invoke setFriendlyName on org.rdk.System with friendlyName: "My Device"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setFriendlyName", "params": {"friendlyName": "My Device"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the friendly name is set successfully |

---

<a id="system_invalid_set_power_state"></a>
### TestCase Name
System_Invalid_Set_Power_State

### TestCase ID
SYS_53

### TestCase Objective
Validate by setting up invalid power state

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set power state | Invoke setPowerState on org.rdk.System with powerState: "INVALID", standbyReason: "APIUnitTest"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"powerState": "INVALID", "standbyReason": "APIUnitTest"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `setPowerState` returns an error response with `success: false` for the invalid power state value `"INVALID"`  |

---

<a id="system_invalid_timezone_errorvalidation"></a>
### TestCase Name
System_Invalid_TimeZone_ErrorValidation

### TestCase ID
SYS_54

### TestCase Objective
Set and get Invalid DST time zone

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
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

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get device info | Invoke getDeviceInfo on org.rdk.System with params: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "INVALID"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `getDeviceInfo` returns an error response with `success: false` for the invalid key `"INVALID"`  |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onMacAddressesRetreived event | Unregister the WebSocket event listener for `onMacAddressesRetreived` to stop receiving `onMacAddressesRetreived` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onMacAddressesRetreived", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the onSystemPowerStateChanged event | Unregister the WebSocket event listener for `onSystemPowerStateChanged` to stop receiving `onSystemPowerStateChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onSystemPowerStateChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the onSystemModeChanged event | Unregister the WebSocket event listener for `onSystemModeChanged` to stop receiving `onSystemModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onSystemModeChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 4 | Unsubscribe from the onRebootRequest event | Unregister the WebSocket event listener for `onRebootRequest` to stop receiving `onRebootRequest` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onRebootRequest", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 5 | Unsubscribe from the onNetworkStandbyModeChanged event | Unregister the WebSocket event listener for `onNetworkStandbyModeChanged` to stop receiving `onNetworkStandbyModeChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onNetworkStandbyModeChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 6 | Unsubscribe from the onTimeZoneDSTChanged event | Unregister the WebSocket event listener for `onTimeZoneDSTChanged` to stop receiving `onTimeZoneDSTChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onTimeZoneDSTChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 7 | Unsubscribe from the onFriendlyNameChanged event | Unregister the WebSocket event listener for `onFriendlyNameChanged` to stop receiving `onFriendlyNameChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onFriendlyNameChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 8 | Unsubscribe from the onTerritoryChanged event | Unregister the WebSocket event listener for `onTerritoryChanged` to stop receiving `onTerritoryChanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.unregister", "params": {"event": "onTerritoryChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 9 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 70 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
