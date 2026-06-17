## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [Read_EDID_Without_TV (DSWTV_1)](#read_edid_without_tv-dswtv_1)
   - [Check_Connected_Video_Displays_Without_TV_Connected (DSWTV_2)](#check_connected_video_displays_without_tv_connected-dswtv_2)
   - [Check_Active_Input_Status_Without_TV_Connected (DSWTV_3)](#check_active_input_status_without_tv_connected-dswtv_3)
   - [Check_Connected_AudioPorts_Without_TV_Connected (DSWTV_4)](#check_connected_audioports_without_tv_connected-dswtv_4)
   - [Check_HDCP_Status_Without_TV_Connected (DSWTV_5)](#check_hdcp_status_without_tv_connected-dswtv_5)
   - [Check_GetCurrentResolution_Status_Without_TV_Connected (DSWTV_6)](#check_getcurrentresolution_status_without_tv_connected-dswtv_6)
   - [Check_SetCurrentResolution_Status_Without_TV_Connected (DSWTV_7)](#check_setcurrentresolution_status_without_tv_connected-dswtv_7)
   - [Check_GetDefaultResolution_Status_Without_TV_Connected (DSWTV_8)](#check_getdefaultresolution_status_without_tv_connected-dswtv_8)
   - [Check_PortName_Status_Without_TV_Connected (DSWTV_9)](#check_portname_status_without_tv_connected-dswtv_9)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DisplaySettingsWithoutTV** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DisplaySettingsWithoutTV` (version 1)

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_HdcpProfile_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

## Test Cases

<a id="read_edid_without_tv-dswtv_1"></a>
### Read_EDID_Without_TV (DSWTV_1)

**Objective:** Check the EDID status when TV is disconnected

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `true`, connected video displays list is empty (TV not connected) |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|------------------|
| 1 | Check EDID Status Of Disconnected Device | Invoke `readEDID` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `false` (readEDID returns failure when TV is not connected) |

---

<a id="check_connected_video_displays_without_tv_connected-dswtv_2"></a>
### Check_Connected_Video_Displays_Without_TV_Connected (DSWTV_2)

**Objective:** Checks whether getConnectedVideoDisplays API is returning empty list when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |

---

<a id="check_active_input_status_without_tv_connected-dswtv_3"></a>
### Check_Active_Input_Status_Without_TV_Connected (DSWTV_3)

**Objective:** Checks active input status with and without passing video port name when TV is not connected

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `true`, connected video displays list is empty (TV not connected) |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Active Input Status With Video Port | Invoke `getActiveInput` on `org.rdk.DisplaySettings` with `videoDisplay`: `"HDMI0"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput", "params": {"videoDisplay": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `true`, `activeInput`: `false` |
| 2 | Check Active Input Status Without Video Port | Invoke `getActiveInput` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput"}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `true`, `activeInput`: `false` |

---

<a id="check_connected_audioports_without_tv_connected-dswtv_4"></a>
### Check_Connected_AudioPorts_Without_TV_Connected (DSWTV_4)

**Objective:** Checks whether getConnectedAudioPorts API does not return HDMI0 when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Check AudioPorts Connected Status | Invoke `getConnectedAudioPorts` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI0 not present in connected audio ports |

---

<a id="check_hdcp_status_without_tv_connected-dswtv_5"></a>
### Check_HDCP_Status_Without_TV_Connected (DSWTV_5)

**Objective:** Checks getHDCPStatus API response when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Get HDCP Status | Invoke `getHDCPStatus` on `org.rdk.HdcpProfile`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getHDCPStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected: `success` `true`, `HDCPStatus.isConnected`: `false`, `HDCPStatus.isHDCPCompliant`: `false`, `HDCPStatus.isHDCPEnabled`: `false` (all fields reflect disconnected state from Step 1) |

---

<a id="check_getcurrentresolution_status_without_tv_connected-dswtv_6"></a>
### Check_GetCurrentResolution_Status_Without_TV_Connected (DSWTV_6)

**Objective:** Checks getCurrentResolution API response when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Get CurrentResolution Status | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="check_setcurrentresolution_status_without_tv_connected-dswtv_7"></a>
### Check_SetCurrentResolution_Status_Without_TV_Connected (DSWTV_7)

**Objective:** Checks setCurrentResolution API response when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Check SetCurrentResolution Status | Invoke `setCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"HDMI0"`, `resolution`: `"720p"`, `persist`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": "720p", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="check_getdefaultresolution_status_without_tv_connected-dswtv_8"></a>
### Check_GetDefaultResolution_Status_Without_TV_Connected (DSWTV_8)

**Objective:** Checks getDefaultResolution API response when TV is not connected

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Check GetDefaultResolution Status | Invoke `getDefaultResolution` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="check_portname_status_without_tv_connected-dswtv_9"></a>
### Check_PortName_Status_Without_TV_Connected (DSWTV_9)

**Objective:** Checks portname API response when TV is not connected

**Pre-condition:**

#### Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`, HDMI input not present in connected video displays |
| 2 | Check PortName Status | Invoke `portname` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.portname"}' http://127.0.0.1:9998/jsonrpc` | API call succeeds with null/empty result |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 2 minutes |
| Priority | Medium |
| TDK Release Version | M103 |