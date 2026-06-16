## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Get_HDCP_Details (HDCP_01)](#get_hdcp_details-hdcp_01)
   - [Get_STB_Supported_HDCP_Version (HDCP_02)](#get_stb_supported_hdcp_version-hdcp_02)
   - [HdcpProfile_ActivateDeactivate_Event_Test (HDCP_03)](#hdcpprofile_activatedeactivate_event_test-hdcp_03)
   - [HdcpProfile_ActivateDeactivate_All_Event_Test (HDCP_04)](#hdcpprofile_activatedeactivate_all_event_test-hdcp_04)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **HDCPProfile** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.HdcpProfile` (version 1)

**API Coverage**

- **State / Query APIs**: `getHDCPStatus`, `getSettopHDCPSupport`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getHDCPStatus` | Provides interface for HDCP related data and events |
| `getSettopHDCPSupport` | Returns which version of HDCP is supported by the STB |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

---

## Test Cases

<a id="get_hdcp_details-hdcp_01"></a>
### Get_HDCP_Details (HDCP_01)

**Objective:** Get HDCP related data and verify

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | Get HDCP Status | Invoke `getHDCPStatus` on `org.rdk.HdcpProfile`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getHDCPStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected `compared against value from step 1` |

---

<a id="get_stb_supported_hdcp_version-hdcp_02"></a>
### Get_STB_Supported_HDCP_Version (HDCP_02)

**Objective:** Get HDCP version supported by STB

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get STB Supported HDCP Version | Invoke `getSettopHDCPSupport` on `org.rdk.HdcpProfile`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getSettopHDCPSupport"}' http://127.0.0.1:9998/jsonrpc` | Settop HDCP support returned successfully |

---

<a id="hdcpprofile_activatedeactivate_event_test-hdcp_03"></a>
### HdcpProfile_ActivateDeactivate_Event_Test (HDCP_03)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdcpProfile Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdcpProfile Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdcpprofile_activatedeactivate_all_event_test-hdcp_04"></a>
### HdcpProfile_ActivateDeactivate_All_Event_Test (HDCP_04)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdcpProfile Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for event `Event_Controller_All` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdcpProfile Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for event `Event_Controller_All` | Event data validated successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | High |
| TDK Release Version | M81 |