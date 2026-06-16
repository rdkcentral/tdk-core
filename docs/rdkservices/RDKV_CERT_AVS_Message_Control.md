## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [MessageControl_Application_Toggle_All_Tracelevels (MC_01)](#messagecontrol_application_toggle_all_tracelevels-mc_01)
   - [MessageControl_SysLog_Toggle_All_Tracelevels (MC_02)](#messagecontrol_syslog_toggle_all_tracelevels-mc_02)
   - [MessageControl_LocationSync_Plugin_Toggle_All_Tracelevels (MC_03)](#messagecontrol_locationsync_plugin_toggle_all_tracelevels-mc_03)
   - [MessageControl_OCDM_Plugin_Toggle_All_Tracelevels (MC_04)](#messagecontrol_ocdm_plugin_toggle_all_tracelevels-mc_04)
   - [MessageControl_SecurityAgent_Plugin_Toggle_All_Tracelevels (MC_05)](#messagecontrol_securityagent_plugin_toggle_all_tracelevels-mc_05)
   - [MessageControl_LISA_Plugin_Toggle_All_Tracelevels (MC_06)](#messagecontrol_lisa_plugin_toggle_all_tracelevels-mc_06)
   - [MessageControl_System_Plugin_Toggle_All_Tracelevels (MC_07)](#messagecontrol_system_plugin_toggle_all_tracelevels-mc_07)
   - [MessageControl_Cobalt_Plugin_Toggle_All_Tracelevels (MC_08)](#messagecontrol_cobalt_plugin_toggle_all_tracelevels-mc_08)
   - [MessageControl_Messenger_Plugin_Toggle_All_Tracelevels (MC_09)](#messagecontrol_messenger_plugin_toggle_all_tracelevels-mc_09)
   - [MessageControl_Monitor_Plugin_Toggle_All_Tracelevels (MC_10)](#messagecontrol_monitor_plugin_toggle_all_tracelevels-mc_10)
   - [MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels (MC_11)](#messagecontrol_displayinfo_plugin_toggle_all_tracelevels-mc_11)
   - [MessageControl_DeviceIdentification_Plugin_Toggle_All_Tracelevels (MC_12)](#messagecontrol_deviceidentification_plugin_toggle_all_tracelevels-mc_12)
   - [MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels (MC_13)](#messagecontrol_deviceinfo_plugin_toggle_all_tracelevels-mc_13)
   - [MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels (MC_14)](#messagecontrol_playerinfo_plugin_toggle_all_tracelevels-mc_14)
   - [MessageControl_WebKitBrowser_Plugin_Toggle_All_Tracelevels (MC_15)](#messagecontrol_webkitbrowser_plugin_toggle_all_tracelevels-mc_15)
   - [MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels (MC_16)](#messagecontrol_messagecontrol_plugin_toggle_all_tracelevels-mc_16)
   - [MessageControl_ActivateDeactivate_Event_Test (MC_17)](#messagecontrol_activatedeactivate_event_test-mc_17)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **MessageControl** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `MessageControl` (version 1)

**API Coverage**

- **Configuration APIs**: `enable`
- **Other APIs**: `controls`

### APIs Under Test

| API | Description |
|-----|-------------|
| `controls` | Provides access to retrieve a list of current message controls |
| `enable` | Enables/disables a message control |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"MessageControl"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="messagecontrol_application_toggle_all_tracelevels-mc_01"></a>
### MessageControl_Application_Toggle_All_Tracelevels (MC_01)

**Objective:** Toggles all traces levels of the application module

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **6 times**, once for each value of `category`: `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **6 times**, once for each value of `category`: `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Application Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Application"`, `category`: each of `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set Application Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Application"`, `category`: each of `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get Application Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Application"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert Application Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Application"`, `category`: each of `Activity`, `WebFlow`, `SocketFlow`, `TextFlow`, `Information`, `Discovery`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Application", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get Application Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Application"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Application", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_syslog_toggle_all_tracelevels-mc_02"></a>
### MessageControl_SysLog_Toggle_All_Tracelevels (MC_02)

**Objective:** Toggles all traces levels of the SysLog module

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **5 times**, once for each value of `category`: `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **5 times**, once for each value of `category`: `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get SysLog Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"SysLog"`, `category`: each of `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set SysLog Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Logging"`, `enabled`: `"<result_step_1>"`, `module`: `"SysLog"`, `category`: each of `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get SysLog Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"SysLog"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert SysLog Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Logging"`, `enabled`: `"<result_step_1>"`, `module`: `"SysLog"`, `category`: each of `Crash`, `Startup`, `Shutdown`, `ParsingError`, `Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Logging", "enabled": "<result_step_1>", "module": "SysLog", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get SysLog Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"SysLog"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "SysLog", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_locationsync_plugin_toggle_all_tracelevels-mc_03"></a>
### MessageControl_LocationSync_Plugin_Toggle_All_Tracelevels (MC_03)

**Objective:** Toggles all traces levels of the LocationSync module

**Pre-condition:**

#### Pre-condition 1: Activate_LocationSync_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check LocationSync Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@LocationSync"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"LocationSync"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "LocationSync"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check LocationSync Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@LocationSync"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get LocationSync Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LocationSync"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LocationSync", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set LocationSync Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_LocationSync"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_LocationSync", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get LocationSync Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LocationSync"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LocationSync", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert LocationSync Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_LocationSync"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_LocationSync", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get LocationSync Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LocationSync"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LocationSync", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_ocdm_plugin_toggle_all_tracelevels-mc_04"></a>
### MessageControl_OCDM_Plugin_Toggle_All_Tracelevels (MC_04)

**Objective:** Toggles all traces levels of the OCDM module

**Pre-condition:**

#### Pre-condition 1: Activate_OCDM_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check OCDM Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"OCDM"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "OCDM"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check OCDM Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@OCDM"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **4 times**, once for each value of `category`: `Information`, `Error`, `Fatal`, `Warning`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **4 times**, once for each value of `category`: `Information`, `Error`, `Fatal`, `Warning`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OCDM Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_OCDM"`, `category`: each of `Information`, `Error`, `Fatal`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set OCDM Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_OCDM"`, `category`: each of `Information`, `Error`, `Fatal`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get OCDM Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_OCDM"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert OCDM Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_OCDM"`, `category`: each of `Information`, `Error`, `Fatal`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_OCDM", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get OCDM Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_OCDM"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_OCDM", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_securityagent_plugin_toggle_all_tracelevels-mc_05"></a>
### MessageControl_SecurityAgent_Plugin_Toggle_All_Tracelevels (MC_05)

**Objective:** Toggles all traces levels of the SecurityAgent module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@SecurityAgent"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"SecurityAgent"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "SecurityAgent"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@SecurityAgent"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get SecurityAgent Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SecurityAgent"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SecurityAgent", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set SecurityAgent Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_SecurityAgent"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SecurityAgent", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get SecurityAgent Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SecurityAgent"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SecurityAgent", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert SecurityAgent Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_SecurityAgent"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SecurityAgent", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get SecurityAgent Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SecurityAgent"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SecurityAgent", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_lisa_plugin_toggle_all_tracelevels-mc_06"></a>
### MessageControl_LISA_Plugin_Toggle_All_Tracelevels (MC_06)

**Objective:** Toggles all traces levels of the LISA module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@LISA"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"LISA"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "LISA"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@LISA"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `category`: `Information`, `Error`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **2 times**, once for each value of `category`: `Information`, `Error`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get LISA Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LISA"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LISA", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set LISA Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_LISA"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_LISA", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get LISA Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LISA"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LISA", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert LISA Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_LISA"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_LISA", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get LISA Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_LISA"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_LISA", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_system_plugin_toggle_all_tracelevels-mc_07"></a>
### MessageControl_System_Plugin_Toggle_All_Tracelevels (MC_07)

**Objective:** Toggles all traces levels of the System module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `category`: `Information`, `Error`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **2 times**, once for each value of `category`: `Information`, `Error`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SystemServices"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set System Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_SystemServices"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get System Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SystemServices"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert System Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_SystemServices"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_SystemServices", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get System Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_SystemServices"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_SystemServices", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_cobalt_plugin_toggle_all_tracelevels-mc_08"></a>
### MessageControl_Cobalt_Plugin_Toggle_All_Tracelevels (MC_08)

**Objective:** Toggles all traces levels of the Cobalt module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Cobalt"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Cobalt"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Cobalt"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Cobalt"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 4 | Is Cobalt Resumed | Invoke `state` on `Cobalt`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Cobalt.1.state"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`; Cobalt get state |
| 5 | Resume Cobalt | *(Conditional: executed only if previous step condition is met)*<br>Invoke `state` on `Cobalt` with `state`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Cobalt.1.state", "params": {"state": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | N/A |
| 6 | Is Cobalt Resumed | *(Conditional: executed only if previous step condition is met)*<br>Invoke `state` on `Cobalt` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Cobalt.1.state"}' http://127.0.0.1:9998/jsonrpc` | Expected: `resumed` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Cobalt Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Cobalt"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Cobalt", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set Cobalt Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Cobalt"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Cobalt", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get Cobalt Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Cobalt"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Cobalt", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert Cobalt Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Cobalt"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Cobalt", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get Cobalt Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Cobalt"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Cobalt", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_messenger_plugin_toggle_all_tracelevels-mc_09"></a>
### MessageControl_Messenger_Plugin_Toggle_All_Tracelevels (MC_09)

**Objective:** Toggles all traces levels of the Messenger module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Messenger"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Messenger"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Messenger"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Messenger"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **3 times**, once for each value of `category`: `Information`, `Error`, `Warning`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **3 times**, once for each value of `category`: `Information`, `Error`, `Warning`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Messenger Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Messenger"`, `category`: each of `Information`, `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Messenger", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set Messenger Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Messenger"`, `category`: each of `Information`, `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Messenger", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get Messenger Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Messenger"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Messenger", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert Messenger Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Messenger"`, `category`: each of `Information`, `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Messenger", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get Messenger Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Messenger"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Messenger", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_monitor_plugin_toggle_all_tracelevels-mc_10"></a>
### MessageControl_Monitor_Plugin_Toggle_All_Tracelevels (MC_10)

**Objective:** Toggles all traces levels of the Monitor module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"Monitor"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "Monitor"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@Monitor"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **3 times**, once for each value of `category`: `Information`, `Error`, `Fatal`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **3 times**, once for each value of `category`: `Information`, `Error`, `Fatal`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Monitor Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Monitor"`, `category`: each of `Information`, `Error`, `Fatal`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set Monitor Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Monitor"`, `category`: each of `Information`, `Error`, `Fatal`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get Monitor Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Monitor"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert Monitor Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_Monitor"`, `category`: each of `Information`, `Error`, `Fatal`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_Monitor", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get Monitor Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_Monitor"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_Monitor", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_displayinfo_plugin_toggle_all_tracelevels-mc_11"></a>
### MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels (MC_11)

**Objective:** Toggles all traces levels of the DisplayInfo  module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `category`: `Information`, `Error`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **2 times**, once for each value of `category`: `Information`, `Error`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get DisplayInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DisplayInfo"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set DisplayInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DisplayInfo"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get DisplayInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DisplayInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert DisplayInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DisplayInfo"`, `category`: each of `Information`, `Error`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DisplayInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get DisplayInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DisplayInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DisplayInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_deviceidentification_plugin_toggle_all_tracelevels-mc_12"></a>
### MessageControl_DeviceIdentification_Plugin_Toggle_All_Tracelevels (MC_12)

**Objective:** Toggles all traces levels of the DeviceIdentification  module

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceIdentification"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceIdentification"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceIdentification"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceIdentification"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get DeviceIdentification Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceIdentification"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceIdentification", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set DeviceIdentification Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DeviceIdentification"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceIdentification", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get DeviceIdentification Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceIdentification"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceIdentification", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert DeviceIdentification Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DeviceIdentification"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceIdentification", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get DeviceIdentification Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceIdentification"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceIdentification", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_deviceinfo_plugin_toggle_all_tracelevels-mc_13"></a>
### MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels (MC_13)

**Objective:** Toggles all traces levels of the DeviceInfo module

**Pre-condition:**

#### Pre-condition 1: Activate_DeviceInfo_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check DeviceInfo Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check DeviceInfo Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get DeviceInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceInfo"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set DeviceInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DeviceInfo"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get DeviceInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert DeviceInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_DeviceInfo"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_DeviceInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get DeviceInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_DeviceInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_DeviceInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_playerinfo_plugin_toggle_all_tracelevels-mc_14"></a>
### MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels (MC_14)

**Objective:** Toggles all traces levels of the PlayerInfo module

**Pre-condition:**

#### Pre-condition 1: Activate_PlayerInfo_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PlayerInfo Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"PlayerInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PlayerInfo Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `category`: `Error`, `Warning`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **2 times**, once for each value of `category`: `Error`, `Warning`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get PlayerInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_PlayerInfo"`, `category`: each of `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set PlayerInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_PlayerInfo"`, `category`: each of `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get PlayerInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_PlayerInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert PlayerInfo Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_PlayerInfo"`, `category`: each of `Error`, `Warning`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_PlayerInfo", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get PlayerInfo Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_PlayerInfo"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_PlayerInfo", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_webkitbrowser_plugin_toggle_all_tracelevels-mc_15"></a>
### MessageControl_WebKitBrowser_Plugin_Toggle_All_Tracelevels (MC_15)

**Objective:** Toggles all traces levels of the WebKitBrowser module

**Pre-condition:**

#### Pre-condition 1: Activate_WebKitBrowser_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check WebKitBrowser Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@WebKitBrowser"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"WebKitBrowser"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "WebKitBrowser"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check WebKitBrowser Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@WebKitBrowser"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated,resumed` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **6 times**, once for each value of `category`: `Error`, `Notification`, `ParsingError`, `Information`, `Fatal`, `HTML5Notification`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **6 times**, once for each value of `category`: `Error`, `Notification`, `ParsingError`, `Information`, `Fatal`, `HTML5Notification`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get WebKitBrowser Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_WebKitBrowser"`, `category`: each of `Error`, `Notification`, `ParsingError`, `Information`, `Fatal`, `HTML5Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_WebKitBrowser", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set WebKitBrowser Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_WebKitBrowser"`, `category`: each of `Error`, `Notification`, `ParsingError`, `Information`, `Fatal`, `HTML5Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_WebKitBrowser", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get WebKitBrowser Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_WebKitBrowser"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_WebKitBrowser", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert WebKitBrowser Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_WebKitBrowser"`, `category`: each of `Error`, `Notification`, `ParsingError`, `Information`, `Fatal`, `HTML5Notification`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_WebKitBrowser", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get WebKitBrowser Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_WebKitBrowser"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_WebKitBrowser", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_messagecontrol_plugin_toggle_all_tracelevels-mc_16"></a>
### MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels (MC_16)

**Objective:** Toggles all traces levels of the MessageControl module

**Pre-condition:**

#### Pre-condition 1: Activate_MessageControl_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check MessageControl Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"MessageControl"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check MessageControl Active Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Value Loop (Step 1):** Step 1 repeats **1 times**, once for each value of `category`: `Information`.

> **Value Loop (Steps 2–5):** Steps 2–5 repeat **1 times**, once for each value of `category`: `Information`.

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get MessageControl Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_MessageControl"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Response contains the current `enabled` state (boolean) for the requested `module`/`category` combination — `enabled` field is present and indicates whether the trace category is currently active |
| 2 | Set MessageControl Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_MessageControl"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Get MessageControl Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_MessageControl"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field confirms the toggled value — if Step 1 returned `true`, now `false`; if Step 1 returned `false`, now `true` |
| 4 | Revert MessageControl Tracelevel | Invoke `enable` on `MessageControl` with `type`: `"Tracing"`, `enabled`: `"<result_step_1>"`, `module`: `"Plugin_MessageControl"`, `category`: each of `Information`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.enable", "params": {"type": "Tracing", "enabled": "<result_step_1>", "module": "Plugin_MessageControl", "category": "<CATEGORY_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Get MessageControl Tracelevel | Invoke `controls` on `MessageControl` with `module`: `"Plugin_MessageControl"`, `category`: `"<value>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "MessageControl.1.controls", "params": {"module": "Plugin_MessageControl", "category": "<value>"}}' http://127.0.0.1:9998/jsonrpc` | `enabled` field matches the original value captured in Step 1 — trace level successfully restored to its pre-test state |

---

<a id="messagecontrol_activatedeactivate_event_test-mc_17"></a>
### MessageControl_ActivateDeactivate_Event_Test (MC_17)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"MessageControl"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate MessageControl Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"MessageControl"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `messagecontrol`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate MessageControl Plugin | Invoke `activate` on `Controller` with `callsign`: `"MessageControl"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "MessageControl"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `messagecontrol`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@MessageControl"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 10 minutes |
| Priority | Medium |
| TDK Release Version | M120 |