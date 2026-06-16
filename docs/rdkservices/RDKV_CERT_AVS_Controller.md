## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Start_Discovery (Controller_01)](#start_discovery-controller_01)
   - [Get_Subsystems_Status (Controller_02)](#get_subsystems_status-controller_02)
   - [Get_Process_Info (Controller_03)](#get_process_info-controller_03)
   - [Get_Environment_Variables (Controller_04)](#get_environment_variables-controller_04)
   - [Get_Active_Connections_Info (Controller_05)](#get_active_connections_info-controller_05)
   - [Get_All_Plugins_Status (Controller_06)](#get_all_plugins_status-controller_06)
   - [Get_DeviceInfo_Configuration (Controller_07)](#get_deviceinfo_configuration-controller_07)
   - [Store_Configuration (Controller_08)](#store_configuration-controller_08)
   - [Delete_Directory_Contents (Controller_09)](#delete_directory_contents-controller_09)
   - [Check_Plugins_State (Controller_10)](#check_plugins_state-controller_10)
   - [Verify_WPE_Process_Status (Controller_11)](#verify_wpe_process_status-controller_11)
   - [Check_StateChange_And_All_Events_For_DeviceInfo_plugin (Controller_12)](#check_statechange_and_all_events_for_deviceinfo_plugin-controller_12)
   - [Set_DeviceInfo_Plugin_Unavailable (Controller_13)](#set_deviceinfo_plugin_unavailable-controller_13)
   - [Set_Device_Info_Plugin_Unavailable_In_Activated_State (Controller_14)](#set_device_info_plugin_unavailable_in_activated_state-controller_14)
   - [Set_DeviceInfo_Unavailable_And_Query_Plugin (Controller_15)](#set_deviceinfo_unavailable_and_query_plugin-controller_15)
   - [Set_Controller_Plugin_Unavailable (Controller_16)](#set_controller_plugin_unavailable-controller_16)
   - [Activate_Deactivate_Controller_Plugin (Controller_17)](#activate_deactivate_controller_plugin-controller_17)
   - [Check_Invalid_Environment_Variable_Response (Controller_18)](#check_invalid_environment_variable_response-controller_18)
   - [Deactivate_DeviceInfo_And_Check_API_Response (Controller_19)](#deactivate_deviceinfo_and_check_api_response-controller_19)
   - [Give_Empty_Path_To_Delete_Directory_Contents (Controller_20)](#give_empty_path_to_delete_directory_contents-controller_20)
   - [Controller_Configuration_With_Empty_Value (Controller_21)](#controller_configuration_with_empty_value-controller_21)
   - [Set_DeviceInfo_Plugin_Unavailable_And_Activate (Controller_22)](#set_deviceinfo_plugin_unavailable_and_activate-controller_22)
   - [Activate_Invalid_callsign (Controller_23)](#activate_invalid_callsign-controller_23)
   - [Activate_Empty_callsign (Controller_24)](#activate_empty_callsign-controller_24)
   - [Deactivate_Invalid_callsign (Controller_25)](#deactivate_invalid_callsign-controller_25)
   - [Deactivate_empty_callsign (Controller_26)](#deactivate_empty_callsign-controller_26)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **Controller** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `Controller` (version 1)

**API Coverage**

- **Lifecycle / Control APIs**: `activate`, `deactivate`, `startdiscovery`
- **Configuration APIs**: `delete`
- **Events**: `all`, `statechange`
- **Other APIs**: `configuration`, `discoveryresults`, `environment`, `links`, `processinfo`, `status`, `storeconfig`, `subsystems`, `unavailable`

### APIs Under Test

| API | Description |
|-----|-------------|
| `activate` | Activates a plugin |
| `configuration` | Provides access to the configuration object of a service |
| `deactivate` | deactivates a plugin |
| `delete` | Removes contents of a directory from the persistent storage |
| `discoveryresults` | Gives discovery results |
| `environment` | Gives value of an environment variable |
| `links` | Gives information about active connections |
| `processinfo` | Gives information about the framework process |
| `startdiscovery` | Starts the network discovery |
| `status` | Provides the information about plugins |
| `storeconfig` | Saves the current configuration |
| `subsystems` | Provides access to the status of the subsystems |
| `unavailable` | Sets a plugin unavailable for interaction |

### Events Under Test

| Event | Description |
|-------|-------------|
| `all` | Signals each and every event in the system |
| `statechange` | Signals a plugin state change |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="start_discovery-controller_01"></a>
### Start_Discovery (Controller_01)

**Objective:** Starts the network discovery

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Start Discovery | Invoke `startdiscovery` on `Controller` with `ttl`: `2`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.startdiscovery", "params": {"ttl": 2}}' http://127.0.0.1:9998/jsonrpc` | NA |
| 2 | Get Discovery Results | Invoke `discoveryresults` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.discoveryresults"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains array of discovered devices — each entry includes `locator`, `latency`, `model` and `secure` fields |

---

<a id="get_subsystems_status-controller_02"></a>
### Get_Subsystems_Status (Controller_02)

**Objective:** Status of the subsystems

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Subsystems Status | Invoke `subsystems` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.subsystems"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains a non-empty array of subsystem objects — each entry includes `name` (string) and `initialized` (boolean) fields |

---

<a id="get_process_info-controller_03"></a>
### Get_Process_Info (Controller_03)

**Objective:** Gives information about the framework process

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Process Info | Invoke `processinfo` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.processinfo"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains framework process details — `id` (PID), `path` (executable path), `memory` (allocated memory in bytes) and `threads` (active thread count) fields are present with non-empty values |

---

<a id="get_environment_variables-controller_04"></a>
### Get_Environment_Variables (Controller_04)

**Objective:** Gets the value of the environment variables

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Environment Variable | *(Loop: iterates for each variable listed in `CONTROLLER_ENVIRONMENT_VARIABLES`)* Invoke `environment` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.environment@<CONTROLLER_ENVIRONMENT_VARIABLES>"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains the value of the requested environment variable as a non-empty string |

---

<a id="get_active_connections_info-controller_05"></a>
### Get_Active_Connections_Info (Controller_05)

**Objective:** Gives information about the framework process

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Connections Info | Invoke `links` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.links"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains a non-empty array of active JSON-RPC connections — each entry includes `id`, `activity`, `remote` and `state` fields |

---

<a id="get_all_plugins_status-controller_06"></a>
### Get_All_Plugins_Status (Controller_06)

**Objective:** Gets the plugin current status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Plugins Status | *(Loop: iterates for each plugin listed in `Supported_Plugins`)* Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@<Supported_Plugins>"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Plugin state returned for each supported plugin — `callsign`, `state`, `module` and `version` fields are present |

---

<a id="get_deviceinfo_configuration-controller_07"></a>
### Get_DeviceInfo_Configuration (Controller_07)

**Objective:** Gets the configuration of DeviceInfo plugin

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Configuration | Invoke `configuration` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.configuration@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Response contains the non-empty JSON configuration object of the `DeviceInfo` plugin (includes `callsign`, `classname`, `locator` and `autostart` fields) |

---

<a id="store_configuration-controller_08"></a>
### Store_Configuration (Controller_08)

**Objective:** Stores the configuration

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Store Configuration | Invoke `storeconfig` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.storeconfig"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Current runtime configuration saved to persistent storage successfully |

---

<a id="delete_directory_contents-controller_09"></a>
### Delete_Directory_Contents (Controller_09)

**Objective:** Removes contents of a directory from the persistent storage

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Execute Command | Create test file `TDK_TEST_FILE.txt` at `<CONTROLLER_FILE_DELETE_PATH>` on the device | File created successfully at the specified path |
| 2 | Delete Directory Contents | Invoke `delete` on `Controller` with `path`: `"TDK_TEST_FILE.txt"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.delete", "params": {"path": "TDK_TEST_FILE.txt"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` File `TDK_TEST_FILE.txt` removed from persistent storage successfully |
| 3 | Execute Command | Verify file no longer exists at `<CONTROLLER_FILE_DELETE_PATH>` on the device | Expected `File does not exist` File is confirmed absent from the filesystem |

**Post-condition:**

#### Post-condition 1: Delete_Test_files

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Execute Command | Delete test file on the device | External function executed successfully; reference data collected |

---

<a id="check_plugins_state-controller_10"></a>
### Check_Plugins_State (Controller_10)

**Objective:** Checks the plugin status

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | System reboot | Invoke `reboot` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` System reboot initiated successfully |
| 2 | Check Plugins Status | *(Loop: iterates for each plugin listed in `Supported_Plugins`)* Invoke `status` on `Controller` (wait 10s after reboot)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@<Supported_Plugins>"}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Each plugin is in its expected default state after reboot (state matches the configured default — `activated`, `deactivated`, or `suspended`) |

---

<a id="verify_wpe_process_status-controller_11"></a>
### Verify_WPE_Process_Status (Controller_11)

**Objective:** Checks whether WPE Process is running or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check WPE Process | Verify WPE processes listed in `WPE_PROCESSES_LIST` are running on the device | Expected all WPE processes from `<WPE_PROCESSES_LIST>` are active and running |

---

<a id="check_statechange_and_all_events_for_deviceinfo_plugin-controller_12"></a>
### Check_StateChange_And_All_Events_For_DeviceInfo_plugin (Controller_12)

**Objective:** Checks the StateChange and All Events by activating and deactivating the DeviceInfo plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 3 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `deviceinfo`, state = `"deactivated"` |
| 4 | Check All Event | Listen for `Event_Controller_All` event | Controller `all` event received; callsign = `deviceinfo`, state = `"deactivated"` |
| 5 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |
| 7 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `deviceinfo`, state = `"activated"` |
| 8 | Check All Event | Listen for `Event_Controller_All` event (wait 2s) | Controller `all` event received; callsign = `deviceinfo`, state = `"activated"` |

---

<a id="set_deviceinfo_plugin_unavailable-controller_13"></a>
### Set_DeviceInfo_Plugin_Unavailable (Controller_13)

**Objective:** Checks whether able to make DeviceInfo plugin unavailable

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 3 | Set DeviceInfo Plugin Unavailable | Invoke `unavailable` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` `DeviceInfo` plugin marked as unavailable |
| 4 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `unavailable` |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `deviceinfo`, state = `"unavailable"` |
| 6 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` Plugin deactivated from unavailable state successfully |
| 7 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 8 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 9 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Post-condition:**

#### Post-condition 1: Check_Device_Info_Plugin_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="set_device_info_plugin_unavailable_in_activated_state-controller_14"></a>
### Set_Device_Info_Plugin_Unavailable_In_Activated_State (Controller_14)

**Objective:** Checks whether able to make the plugin unavailable in activated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set DeviceInfo Plugin Unavailable | Invoke `unavailable` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `The service is in an illegal state!!!.` / `5` |

**Post-condition:**

#### Post-condition 1: Check_Device_Info_Plugin_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="set_deviceinfo_unavailable_and_query_plugin-controller_15"></a>
### Set_DeviceInfo_Unavailable_And_Query_Plugin (Controller_15)

**Objective:** Queries the DeviceInfo plugin APIs after setting it as unavailable

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 3 | Set DeviceInfo Plugin Unavailable | Invoke `unavailable` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` `DeviceInfo` plugin marked as unavailable |
| 4 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `unavailable` |
| 5 | Check Json Response of DeviceInfo Plugin | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 6 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 7 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 8 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 9 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Post-condition:**

#### Post-condition 1: Check_Device_Info_Plugin_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="set_controller_plugin_unavailable-controller_16"></a>
### Set_Controller_Plugin_Unavailable (Controller_16)

**Objective:** Sets the controller plugin as unavailable and validate the error message

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Controller Plugin Unavailable | Invoke `unavailable` on `Controller` with `callsign`: `"Controller"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |

---

<a id="activate_deactivate_controller_plugin-controller_17"></a>
### Activate_Deactivate_Controller_Plugin (Controller_17)

**Objective:** Activates/Deactivates the controller plugin and validates the error code

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"Controller"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |
| 2 | Deactivate Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"Controller"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "Controller"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `method invocation not allowed.` / `-32604` |

---

<a id="check_invalid_environment_variable_response-controller_18"></a>
### Check_Invalid_Environment_Variable_Response (Controller_18)

**Objective:** Passes the invalid environment variable and validates the error code

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Environment Variable | Invoke `environment` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.environment@invalid"}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` — the environment variable `"invalid"` does not exist on the system |

---

<a id="deactivate_deviceinfo_and_check_api_response-controller_19"></a>
### Deactivate_DeviceInfo_And_Check_API_Response (Controller_19)

**Objective:** Queries the DeviceInfo plugin APIs after deactivated it

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 3 | Check DeviceInfo API Response | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 4 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="give_empty_path_to_delete_directory_contents-controller_20"></a>
### Give_Empty_Path_To_Delete_Directory_Contents (Controller_20)

**Objective:** Give the empty path and validate the error message and code

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Delete Directory Contents | Invoke `delete` on `Controller` with `path`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.delete", "params": {"path": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` — empty path is not a valid persistent storage path |

---

<a id="controller_configuration_with_empty_value-controller_21"></a>
### Controller_Configuration_With_Empty_Value (Controller_21)

**Objective:** Check if able to get the error message when querying configuration for empty value

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Configuration | Invoke `configuration` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.configuration"}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` / error code `22` — no plugin callsign specified in the request |

---

<a id="set_deviceinfo_plugin_unavailable_and_activate-controller_22"></a>
### Set_DeviceInfo_Plugin_Unavailable_And_Activate (Controller_22)

**Objective:** To make deviceinfo plugin unavailable and validates the error message on activating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 3 | Set DeviceInfo Plugin Unavailable | Invoke `unavailable` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unavailable", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Expected `success: true` `DeviceInfo` plugin marked as unavailable |
| 4 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `unavailable` |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (wait 2s) | `statechange` event received; callsign = `deviceinfo`, state = `"unavailable"` |
| 6 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `The service is in an illegal state!!!.` / `5` — plugin cannot be activated from unavailable state |
| 7 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 8 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 9 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 10 | Check PluginActive Status | Invoke `status` on `Controller` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Post-condition:**

#### Post-condition 1: Check_Device_Info_Plugin_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate Plugin | *(Conditional: executed only if previous step condition is met)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Check PluginActive Status | *(Conditional: executed only if previous step condition is met)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="activate_invalid_callsign-controller_23"></a>
### Activate_Invalid_callsign (Controller_23)

**Objective:** Validate error message by activating with invalid callsign

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` — callsign `"invalid"` is not a registered plugin |

---

<a id="activate_empty_callsign-controller_24"></a>
### Activate_Empty_callsign (Controller_24)

**Objective:** Validate error message by activating with empty callsign

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `" "`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` — empty callsign is not a registered plugin |

---

<a id="deactivate_invalid_callsign-controller_25"></a>
### Deactivate_Invalid_callsign (Controller_25)

**Objective:** Validate error message by deactivating with invalid callsign

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"invalid"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` — callsign `"invalid"` is not a registered plugin |

---

<a id="deactivate_empty_callsign-controller_26"></a>
### Deactivate_empty_callsign (Controller_26)

**Objective:** Validate error message by deactivating with empty callsign

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate Plugin | Invoke `deactivate` on `Controller` with `callsign`: `" "`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error `ERROR_UNKNOWN_KEY` — empty callsign is not a registered plugin |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 7 minutes |
| Priority | Medium |
| TDK Release Version | M83 |