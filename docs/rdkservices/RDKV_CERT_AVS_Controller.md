## TestScript Name
RDKV_CERT_AVS_Controller

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [Controller_Start_Discovery](#controller_start_discovery)
   - [Controller_Get_Subsystems_Status](#controller_get_subsystems_status)
   - [Controller_Get_Process_Info](#controller_get_process_info)
   - [Controller_Get_Environment_Variables](#controller_get_environment_variables)
   - [Controller_Get_Active_Connections_Info](#controller_get_active_connections_info)
   - [Controller_Get_All_Plugins_Status](#controller_get_all_plugins_status)
   - [Controller_Get_DeviceInfo_Configuration](#controller_get_deviceinfo_configuration)
   - [Controller_Store_Configuration](#controller_store_configuration)
   - [Controller_Delete_Directory_Contents](#controller_delete_directory_contents)
   - [Controller_Get_Plugins_State](#controller_get_plugins_state)
   - [Controller_Get_WPE_Process_Status](#controller_get_wpe_process_status)
   - [Controller_StateChange_And_All_Events_For_DeviceInfo_plugin](#controller_statechange_and_all_events_for_deviceinfo_plugin)
   - [Controller_Set_DeviceInfo_Plugin_Unavailable](#controller_set_deviceinfo_plugin_unavailable)
   - [Controller_Set_Device_Info_Plugin_Unavailable_In_Activated_State](#controller_set_device_info_plugin_unavailable_in_activated_state)
   - [Controller_Set_DeviceInfo_Unavailable_And_Query_Plugin](#controller_set_deviceinfo_unavailable_and_query_plugin)
   - [Controller_Set_Controller_Plugin_Unavailable](#controller_set_controller_plugin_unavailable)
   - [Controller_Activate_Deactivate_Controller_Plugin](#controller_activate_deactivate_controller_plugin)
   - [Controller_Invalid_Environment_Variable_Response](#controller_invalid_environment_variable_response)
   - [Controller_Deactivate_DeviceInfo_And_API_Response](#controller_deactivate_deviceinfo_and_api_response)
   - [Controller_Give_Empty_Path_To_Delete_Directory_Contents](#controller_give_empty_path_to_delete_directory_contents)
   - [Controller_Configuration_With_Empty_Value](#controller_configuration_with_empty_value)
   - [Controller_Set_DeviceInfo_Plugin_Unavailable_And_Activate](#controller_set_deviceinfo_plugin_unavailable_and_activate)
   - [Controller_Activate_Invalid_callsign](#controller_activate_invalid_callsign)
   - [Controller_Activate_Empty_callsign](#controller_activate_empty_callsign)
   - [Controller_Deactivate_Invalid_callsign](#controller_deactivate_invalid_callsign)
   - [Controller_Deactivate_empty_callsign](#controller_deactivate_empty_callsign)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **Controller** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `Controller` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of System plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the all event | Register a WebSocket event listener for `all` to receive `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "all", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure environment variables | `CONTROLLER_ENVIRONMENT_VARIABLES` must be set to the environment variables defined in /lib/systemd/system/wpeframework.service file | The `CONTROLLER_ENVIRONMENT_VARIABLES` value should be correctly configured in the device-specific config file |
| 2 | Configure supported features | `CONTROLLER_SUPPORTED_FEATURES` must be set to the supported features in device. If device supports NetworkDiscovery, add NetworkDiscovery | The `CONTROLLER_SUPPORTED_FEATURES` value should be correctly configured in the device-specific config file |
| 3 | Configure file delete path | `CONTROLLER_FILE_DELETE_PATH` must be set to the persistent path for file deletion as configured in /etc/WPEFramework/config.json | The `CONTROLLER_FILE_DELETE_PATH` value should be correctly configured in the device-specific config file |
| 4 | Configure WPE processes list | `WPE_PROCESSES_LIST` must be set to the WPE processes to check the status | The `WPE_PROCESSES_LIST` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="controller_start_discovery"></a>
### TestCase Name
Controller_Start_Discovery

### TestCase ID
Controller_01

### TestCase Objective
Starts the network discovery

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Start plugin discovery via Controller | Invoke startdiscovery on Controller with ttl: 2<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.startdiscovery", "params": {"ttl": 2}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 2 | Get discovery results | Invoke discoveryresults on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.discoveryresults"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains an array of discovered devices with `locator`, `latency`, `model`, and `secure` fields  |

---

<a id="controller_get_subsystems_status"></a>
### TestCase Name
Controller_Get_Subsystems_Status

### TestCase ID
Controller_02

### TestCase Objective
Status of the subsystems

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Controller subsystems status | Invoke subsystems on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.subsystems"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains a non-empty array of subsystem objects with `name` (string) and `initialized` (boolean) fields  |

---

<a id="controller_get_process_info"></a>
### TestCase Name
Controller_Get_Process_Info

### TestCase ID
Controller_03

### TestCase Objective
Gives information about the framework process

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Controller process information | Invoke processinfo on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.processinfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains framework process details including `id` (PID), `path`, `memory`, and `threads` fields with non-empty values  |

---

<a id="controller_get_environment_variables"></a>
### TestCase Name
Controller_Get_Environment_Variables

### TestCase ID
Controller_04

### TestCase Objective
Gets the value of the environment variables

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get environment variable | Invoke environment on Controller for <CONTROLLER_ENVIRONMENT_VARIABLES><br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.environment@<CONTROLLER_ENVIRONMENT_VARIABLES>"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains the value of the requested environment variable as a non-empty string  |

---

<a id="controller_get_active_connections_info"></a>
### TestCase Name
Controller_Get_Active_Connections_Info

### TestCase ID
Controller_05

### TestCase Objective
Gives information about the framework process

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get active connections info | Invoke links on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.links"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains a non-empty array of active JSON-RPC connections with `id`, `activity`, `remote`, and `state` fields  |

---

<a id="controller_get_all_plugins_status"></a>
### TestCase Name
Controller_Get_All_Plugins_Status

### TestCase ID
Controller_06

### TestCase Objective
Gets the plugin current status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugins status | Invoke status on Controller for <Supported_Plugins><br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@<Supported_Plugins>"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the plugin state is returned for each supported plugin with `callsign`, `state`, `module`, and `version` fields present  |

---

<a id="controller_get_deviceinfo_configuration"></a>
### TestCase Name
Controller_Get_DeviceInfo_Configuration

### TestCase ID
Controller_07

### TestCase Objective
Gets the configuration of DeviceInfo plugin

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get plugin configuration | Invoke configuration on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.configuration@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the response contains the non-empty JSON configuration object of the `DeviceInfo` plugin with `callsign`, `classname`, `locator`, and `autostart` fields  |

---

<a id="controller_store_configuration"></a>
### TestCase Name
Controller_Store_Configuration

### TestCase ID
Controller_08

### TestCase Objective
Stores the configuration

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Store current runtime configuration | Invoke storeconfig on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.storeconfig"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the current runtime configuration is saved to persistent storage successfully  |

---

<a id="controller_delete_directory_contents"></a>
### TestCase Name
Controller_Delete_Directory_Contents

### TestCase ID
Controller_09

### TestCase Objective
Removes contents of a directory from the persistent storage

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Execute shell command on device | Create test file TDK_TEST_FILE.txt at <CONTROLLER_FILE_DELETE_PATH> on the device | Confirm that the file is created successfully at the specified path |
| 2 | Delete directory contents | Invoke delete on Controller with path: "TDK_TEST_FILE.txt"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.delete", "params": {"path": "TDK_TEST_FILE.txt"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the file `TDK_TEST_FILE.txt` is removed from persistent storage successfully  |
| 3 | Execute shell command on device | Verify file no longer exists at <CONTROLLER_FILE_DELETE_PATH> on the device | Verify that the response is `File does not exist`, confirming the file is absent from the filesystem  |

### TestCase Post-condition

#### TestCase Post-condition 1: Delete_Test_files

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Execute shell command on device | Delete test file on the device | Verify that the external function executed successfully and reference data is collected |

---

<a id="controller_get_plugins_state"></a>
### TestCase Name
Controller_Get_Plugins_State

### TestCase ID
Controller_10

### TestCase Objective
Checks the plugin status

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Initiate system reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the system reboot is initiated successfully  |
| 2 | Check plugins status | Invoke status on Controller for <Supported_Plugins><br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@<Supported_Plugins>"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and each plugin is in its expected default state after reboot (`activated`, `deactivated`, or `suspended` as configured)  |

---

<a id="controller_get_wpe_process_status"></a>
### TestCase Name
Controller_Get_WPE_Process_Status

### TestCase ID
Controller_11

### TestCase Objective
Checks whether WPE Process is running or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check WPE process | Verify WPE processes listed in WPE_PROCESSES_LIST are running on the device | Verify that all WPE processes listed in `<WPE_PROCESSES_LIST>` are active and running  |

---

<a id="controller_statechange_and_all_events_for_deviceinfo_plugin"></a>
### TestCase Name
Controller_StateChange_And_All_Events_For_DeviceInfo_plugin

### TestCase ID
Controller_12

### TestCase Objective
Checks the StateChange and All Events by activating and deactivating the DeviceInfo plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 3 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `deviceinfo` with state `"deactivated"` |
| 4 | Check all event | Listen for Event_Controller_All event | Verify that the `all` event is received for callsign `deviceinfo` with state `"deactivated"` |
| 5 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |
| 7 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `deviceinfo` with state `"activated"` |
| 8 | Check all event | Listen for Event_Controller_All event (wait 2s) | Verify that the `all` event is received for callsign `deviceinfo` with state `"activated"` |

---

<a id="controller_set_deviceinfo_plugin_unavailable"></a>
### TestCase Name
Controller_Set_DeviceInfo_Plugin_Unavailable

### TestCase ID
Controller_13

### TestCase Objective
Checks whether able to make DeviceInfo plugin unavailable

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 3 | Set DeviceInfo plugin unavailable | Invoke unavailable on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the `DeviceInfo` plugin is marked as unavailable  |
| 4 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is unavailable |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `deviceinfo` with state `"unavailable"` |
| 6 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the plugin is deactivated from the unavailable state successfully  |
| 7 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 8 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 9 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_Device_Info_Plugin_State

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Activate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 4 | Check plugin active status | *(Conditional statement executed only if previous step condition is met)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="controller_set_device_info_plugin_unavailable_in_activated_state"></a>
### TestCase Name
Controller_Set_Device_Info_Plugin_Unavailable_In_Activated_State

### TestCase ID
Controller_14

### TestCase Objective
Checks whether able to make the plugin unavailable in activated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set DeviceInfo plugin unavailable | Invoke unavailable on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `The service is in an illegal state!!!.` / `5` |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_Device_Info_Plugin_State

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Activate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 4 | Check plugin active status | *(Conditional statement executed only if previous step condition is met)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="controller_set_deviceinfo_unavailable_and_query_plugin"></a>
### TestCase Name
Controller_Set_DeviceInfo_Unavailable_And_Query_Plugin

### TestCase ID
Controller_15

### TestCase Objective
Queries the DeviceInfo plugin APIs after setting it as unavailable

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 3 | Set DeviceInfo plugin unavailable | Invoke unavailable on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the `DeviceInfo` plugin is marked as unavailable  |
| 4 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is unavailable |
| 5 | Check json response of DeviceInfo plugin | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 6 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 7 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 8 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 9 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_Device_Info_Plugin_State

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Activate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 4 | Check plugin active status | *(Conditional statement executed only if previous step condition is met)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="controller_set_controller_plugin_unavailable"></a>
### TestCase Name
Controller_Set_Controller_Plugin_Unavailable

### TestCase ID
Controller_16

### TestCase Objective
Sets the controller plugin as unavailable and validate the error message

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set controller plugin unavailable | Invoke unavailable on Controller with callsign: "Controller"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |

---

<a id="controller_activate_deactivate_controller_plugin"></a>
### TestCase Name
Controller_Activate_Deactivate_Controller_Plugin

### TestCase ID
Controller_17

### TestCase Objective
Activates/Deactivates the controller plugin and validates the error code

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Activate plugin | Invoke activate on Controller with callsign: "Controller"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |
| 2 | Deactivate plugin | Invoke deactivate on Controller with callsign: "Controller"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |

---

<a id="controller_invalid_environment_variable_response"></a>
### TestCase Name
Controller_Invalid_Environment_Variable_Response

### TestCase ID
Controller_18

### TestCase Objective
Passes the invalid environment variable and validates the error code

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get environment variable | Invoke environment on Controller for invalid<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.environment@invalid"}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` must be configured: the environment variable `"invalid"` does not exist on the system |

---

<a id="controller_deactivate_deviceinfo_and_api_response"></a>
### TestCase Name
Controller_Deactivate_DeviceInfo_And_API_Response

### TestCase ID
Controller_19

### TestCase Objective
Queries the DeviceInfo plugin APIs after deactivated it

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 3 | Check DeviceInfo API response | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 4 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="controller_give_empty_path_to_delete_directory_contents"></a>
### TestCase Name
Controller_Give_Empty_Path_To_Delete_Directory_Contents

### TestCase ID
Controller_20

### TestCase Objective
Give the empty path and validate the error message and code

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Delete directory contents | Invoke delete on Controller with path: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.delete", "params": {"path": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` must be configured: empty path is not a valid persistent storage path |

---

<a id="controller_configuration_with_empty_value"></a>
### TestCase Name
Controller_Configuration_With_Empty_Value

### TestCase ID
Controller_21

### TestCase Objective
Check if able to get the error message when querying configuration for empty value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get plugin configuration | Invoke configuration on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.configuration"}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` must be configured: no plugin callsign specified in the request |

---

<a id="controller_set_deviceinfo_plugin_unavailable_and_activate"></a>
### TestCase Name
Controller_Set_DeviceInfo_Plugin_Unavailable_And_Activate

### TestCase ID
Controller_22

### TestCase Objective
To make deviceinfo plugin unavailable and validates the error message on activating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 3 | Set DeviceInfo plugin unavailable | Invoke unavailable on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the `DeviceInfo` plugin is marked as unavailable  |
| 4 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is unavailable |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (wait 2s) | Verify that the `statechange` event is received for callsign `deviceinfo` with state `"unavailable"` |
| 6 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `The service is in an illegal state!!!.` / `5` must be configured: plugin cannot be activated from unavailable state |
| 7 | Deactivate DeviceInfo plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 8 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 9 | Activate DeviceInfo plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 10 | Check plugin active status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_Device_Info_Plugin_State

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Deactivate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is deactivated successfully |
| 3 | Activate plugin | *(Conditional statement executed only if previous step condition is met)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 4 | Check plugin active status | *(Conditional statement executed only if previous step condition is met)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="controller_activate_invalid_callsign"></a>
### TestCase Name
Controller_Activate_Invalid_callsign

### TestCase ID
Controller_23

### TestCase Objective
Validate error message by activating with invalid callsign

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Activate plugin | Invoke activate on Controller with callsign: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` must be configured: callsign `"invalid"` is not a registered plugin |

---

<a id="controller_activate_empty_callsign"></a>
### TestCase Name
Controller_Activate_Empty_callsign

### TestCase ID
Controller_24

### TestCase Objective
Validate error message by activating with empty callsign

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Activate plugin | Invoke activate on Controller with callsign: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` must be configured: empty callsign is not a registered plugin |

---

<a id="controller_deactivate_invalid_callsign"></a>
### TestCase Name
Controller_Deactivate_Invalid_callsign

### TestCase ID
Controller_25

### TestCase Objective
Validate error message by deactivating with invalid callsign

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate plugin | Invoke deactivate on Controller with callsign: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` must be configured: callsign `"invalid"` is not a registered plugin |

---

<a id="controller_deactivate_empty_callsign"></a>
### TestCase Name
Controller_Deactivate_empty_callsign

### TestCase ID
Controller_26

### TestCase Objective
Validate error message by deactivating with empty callsign

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate plugin | Invoke deactivate on Controller with callsign: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` must be configured: empty callsign is not a registered plugin |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the all event | Unregister the WebSocket event listener for `all` to stop receiving `all` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "all", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 7 mins

**Priority** : High

**Release Version** : M83

<div align="right"><a href="#testscript-name">Go to Top</a></div>
