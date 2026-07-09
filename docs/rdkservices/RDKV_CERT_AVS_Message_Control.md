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
| 1 | Check plugin active status | Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

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
Toggles all trace levels of the application module

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get application tracelevel | *(Value loop: Iterates for each `category` value: `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`)*<br>Invoke controls on MessageControl with module: "Application", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set application tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Application", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get application tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Application", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert application tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Application", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get application tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Application", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_syslog_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_SysLog_Toggle_All_Tracelevels

### TestCase ID
MC_02

### TestCase Objective
Toggles all trace levels of the SysLog module

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get SysLog tracelevel | *(Value loop: Iterates for each `category` value: `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`)*<br>Invoke controls on MessageControl with module: "SysLog", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set SysLog tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Logging", enabled: "<result_step_1>", module: "SysLog", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get SysLog tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "SysLog", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert SysLog tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Logging", enabled: "<result_step_1>", module: "SysLog", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get SysLog tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "SysLog", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_ocdm_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_OCDM_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_03

### TestCase Objective
Toggles all trace levels of the OCDM module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_OCDM_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check OCDM active status | Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check OCDM active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of OCDM plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get OCDM tracelevel | *(Value loop: Iterates for each `category` value: `Information`, `Error`, `Fatal`, `Warning`)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set OCDM tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_OCDM", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get OCDM tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert OCDM tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_OCDM", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get OCDM tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_OCDM", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_system_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_System_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_04

### TestCase Objective
Toggles all trace levels of the System module

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
| 1 | Get system tracelevel | *(Value loop: Iterates for each `category` value: `Information`, `Error`)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set system tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_SystemServices", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get system tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert system tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_SystemServices", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get system tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_SystemServices", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_monitor_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_Monitor_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_05

### TestCase Objective
Toggles all trace levels of the Monitor module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of Monitor plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get monitor tracelevel | *(Value loop: Iterates for each `category` value: `Information`, `Error`, `Fatal`)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set monitor tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_Monitor", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get monitor tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert monitor tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_Monitor", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get monitor tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_Monitor", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_displayinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_06

### TestCase Objective
Toggles all trace levels of the DisplayInfo module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get DisplayInfo tracelevel | *(Value loop: Iterates for each `category` value: `Information`, `Error`)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set DisplayInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DisplayInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get DisplayInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert DisplayInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DisplayInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get DisplayInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DisplayInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_deviceinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_07

### TestCase Objective
Toggles all trace levels of the DeviceInfo module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_DeviceInfo_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check DeviceInfo active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check DeviceInfo active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get DeviceInfo tracelevel | *(Value loop: Iterates for each `category` value: `Information`)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set DeviceInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DeviceInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get DeviceInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert DeviceInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_DeviceInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get DeviceInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_DeviceInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_playerinfo_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_08

### TestCase Objective
Toggles all trace levels of the PlayerInfo module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_PlayerInfo_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PlayerInfo active status | Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PlayerInfo active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get PlayerInfo tracelevel | *(Value loop: Iterates for each `category` value: `Error`, `Warning`)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set PlayerInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_PlayerInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get PlayerInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert PlayerInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_PlayerInfo", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get PlayerInfo tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_PlayerInfo", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_messagecontrol_plugin_toggle_all_tracelevels"></a>
### TestCase Name
MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels

### TestCase ID
MC_09

### TestCase Objective
Toggles all trace levels of the MessageControl module

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_MessageControl_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check MessageControl active status | Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check MessageControl active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MessageControl tracelevel | *(Value loop: Iterates for each `category` value: `Information`)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains the current `enabled` state (boolean) for the requested `module`/`category` combination  |
| 2 | Set MessageControl tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_MessageControl", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 3 | Get MessageControl tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true`  |
| 4 | Revert MessageControl tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke enable on MessageControl with type: "Tracing", enabled: "<result_step_1>", module: "Plugin_MessageControl", category: "<CATEGORY_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Get MessageControl tracelevel | *(Value loop: Runs once per `category` value iteration)*<br>Invoke controls on MessageControl with module: "Plugin_MessageControl", category: "<value>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state  |

---

<a id="messagecontrol_activatedeactivate_event_test"></a>
### TestCase Name
MessageControl_ActivateDeactivate_Event_Test

### TestCase ID
MC_10

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of MessageControl plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate MessageControl plugin | Invoke deactivate on Controller with callsign: "MessageControl"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `messagecontrol` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for MessageControl<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate MessageControl plugin | Invoke activate on Controller with callsign: "MessageControl"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `messagecontrol` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for MessageControl<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

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
