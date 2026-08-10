## TestScript Name
RDKV_CERT_AVS_Message_Control

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [MessageControl_Application_Toggle_All_Tracelevels](#messagecontrol_application_toggle_all_tracelevels)
   - [MessageControl_SysLog_Toggle_All_Tracelevels](#messagecontrol_syslog_toggle_all_tracelevels)
   - [MessageControl_OCDM_Plugin_Toggle_All_Tracelevels](#messagecontrol_ocdm_plugin_toggle_all_tracelevels)
   - [MessageControl_System_Plugin_Toggle_All_Tracelevels](#messagecontrol_system_plugin_toggle_all_tracelevels)
   - [MessageControl_Monitor_Plugin_Toggle_All_Tracelevels](#messagecontrol_monitor_plugin_toggle_all_tracelevels)
   - [MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels](#messagecontrol_displayinfo_plugin_toggle_all_tracelevels)
   - [MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels](#messagecontrol_deviceinfo_plugin_toggle_all_tracelevels)
   - [MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels](#messagecontrol_playerinfo_plugin_toggle_all_tracelevels)
   - [MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels](#messagecontrol_messagecontrol_plugin_toggle_all_tracelevels)
   - [MessageControl_ActivateDeactivate_Event_Test](#messagecontrol_activatedeactivate_event_test)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **MessageControl** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `MessageControl` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="messagecontrol_application_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_Application_Toggle_All_Tracelevels

### TestCase ID
MC_01

### TestCase Objective
Toggles all traces levels of the application module

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`)*<br>Invoke controls on MessageControl with module: "Application", category: each of Activity, WebFlow, SocketFlow, TextFlow, Information, Discovery<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Application", category: each of Activity, WebFlow, SocketFlow, TextFlow, Information, Discovery<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Application", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Application", category: each of Activity, WebFlow, SocketFlow, TextFlow, Information, Discovery<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Application", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_syslog_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_SysLog_Toggle_All_Tracelevels

### TestCase ID
MC_02

### TestCase Objective
Toggles all traces levels of the SysLog module

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`)*<br>Invoke controls on MessageControl with module: "SysLog", category: each of Crash, Startup, Shutdown, ParsingError, Notification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`)*<br>Invoke enable on MessageControl with type: "Logging", enabled: "<result_step_1>", module: "SysLog", category: each of Crash, Startup, Shutdown, ParsingError, Notification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "SysLog", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Logging", enabled: "<result_step_1>", module: "SysLog", category: each of Crash, Startup, Shutdown, ParsingError, Notification<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "SysLog", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_ocdm_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_OCDM_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_03

### TestCase Objective
Toggles all traces levels of the OCDM module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_OCDM_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check OCDM Active Status | Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check OCDM Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of OCDM Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`, `Error`, `Fatal`, `Warning`)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: each of Information, Error, Fatal, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`, `Error`, `Fatal`, `Warning`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_OCDM", category: each of Information, Error, Fatal, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_OCDM", category: each of Information, Error, Fatal, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_system_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_System_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_04

### TestCase Objective
Toggles all traces levels of the System module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`, `Error`)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`, `Error`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_SystemServices", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_SystemServices", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_monitor_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_Monitor_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_05

### TestCase Objective
Toggles all traces levels of the Monitor module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of Monitor Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of Monitor Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`, `Error`, `Fatal`)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: each of Information, Error, Fatal<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`, `Error`, `Fatal`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_Monitor", category: each of Information, Error, Fatal<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_Monitor", category: each of Information, Error, Fatal<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_displayinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_06

### TestCase Objective
Toggles all traces levels of the DisplayInfo  module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`, `Error`)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`, `Error`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DisplayInfo", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DisplayInfo", category: each of Information, Error<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_deviceinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_07

### TestCase Objective
Toggles all traces levels of the DeviceInfo module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_DeviceInfo_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Device Info Active Status | Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Device Info Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DeviceInfo", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DeviceInfo", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_playerinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_08

### TestCase Objective
Toggles all traces levels of the PlayerInfo module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_PlayerInfo_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Player Info Active Status | Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Player Info Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Error`, `Warning`)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: each of Error, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Error`, `Warning`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_PlayerInfo", category: each of Error, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_PlayerInfo", category: each of Error, Warning<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_messagecontrol_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_09

### TestCase Objective
Toggles all traces levels of the MessageControl module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_MessageControl_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Message Control Active Status | Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Message Control Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Controls | *(Value loop: iterates for each `category` value: `Information`)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and Messagecontrol get controls |
| 2 | Enable | *(Value loop: iterates for each `category` value: `Information`)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_MessageControl", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and `enabled` state matches toggled value from step 1 |
| 4 | Enable | *(Value loop: runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_MessageControl", category: each of Information<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Controls | *(Value loop: runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and messagecontrol get original state matches value from step 1 |

---

<a id="messagecontrol_activatedeactivate_event_test"></a>
### TestCase Name
MessageControl_ActivateDeactivate_Event_Test

### TestCase ID
MC_10

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 3 | Check Plugin Active Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of MessageControl Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate | Invoke deactivate on Controller with callsign: "MessageControl"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is disabled successfully |
| 2 | Listen for event controller state changed event | Listen for `Event_Controller_State_Changed` event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `messagecontrol` with state `deactivated` |
| 3 | Status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate | Invoke activate on Controller with callsign: "MessageControl" (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is enabled successfully |
| 5 | Listen for event controller state changed event | Listen for `Event_Controller_State_Changed` event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `messagecontrol` with state `activated` |
| 6 | Status | Invoke status on Controller<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions

### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 10 mins

**Priority** : High

**Release Version** : M120

<div align="right"><a href="#testscript-name">Go to Top</a></div>
