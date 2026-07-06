## TestScript Name
RDKV_CERT_AVS_Display_Settings_Without_TV

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [Read_EDID_Without_TV](#read_edid_without_tv)
   - [Check_Connected_Video_Displays_Without_TV_Connected](#check_connected_video_displays_without_tv_connected)
   - [Check_Active_Input_Status_Without_TV_Connected](#check_active_input_status_without_tv_connected)
   - [Check_Connected_AudioPorts_Without_TV_Connected](#check_connected_audioports_without_tv_connected)
   - [Check_HDCP_Status_Without_TV_Connected](#check_hdcp_status_without_tv_connected)
   - [Check_GetCurrentResolution_Status_Without_TV_Connected](#check_getcurrentresolution_status_without_tv_connected)
   - [Check_SetCurrentResolution_Status_Without_TV_Connected](#check_setcurrentresolution_status_without_tv_connected)
   - [Check_GetDefaultResolution_Status_Without_TV_Connected](#check_getdefaultresolution_status_without_tv_connected)
   - [Check_PortName_Status_Without_TV_Connected](#check_portname_status_without_tv_connected)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

**DisplaySettingsWithoutTV** is a test scenario that validates DisplaySettings API behavior in a no-TV-connected environment. The API responses are obtained through the `org.rdk.DisplaySettings` interface (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_HdcpProfile_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Test Cases

<a id="read_edid_without_tv"></a>
### TestCase Name
Read_EDID_Without_TV

### TestCase ID
DSWTV_1

### TestCase Objective
Check the EDID status when TV is disconnected

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the connected video displays list is empty, as expected when the TV is not connected  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check EDID Status Of Disconnected Device | Invoke readEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false`, indicating that `readEDID` fails when the TV is not connected  |

---

<a id="check_connected_video_displays_without_tv_connected"></a>
### TestCase Name
Check_Connected_Video_Displays_Without_TV_Connected

### TestCase ID
DSWTV_2

### TestCase Objective
Checks whether getConnectedVideoDisplays API is returning empty list when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |

---

<a id="check_active_input_status_without_tv_connected"></a>
### TestCase Name
Check_Active_Input_Status_Without_TV_Connected

### TestCase ID
DSWTV_3

### TestCase Objective
Checks active input status with and without passing video port name when TV is not connected

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and the connected video displays list is empty, as expected when the TV is not connected  |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Active Input Status With Video Port | Invoke getActiveInput on org.rdk.DisplaySettings with videoDisplay: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput", "params": {"videoDisplay": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and `activeInput` is `false`, as expected for an invalid video display  |
| 2 | Check Active Input Status Without Video Port | Invoke getActiveInput on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` and `activeInput` is `false`, as expected for an invalid video display  |

---

<a id="check_connected_audioports_without_tv_connected"></a>
### TestCase Name
Check_Connected_AudioPorts_Without_TV_Connected

### TestCase ID
DSWTV_4

### TestCase Objective
Checks whether getConnectedAudioPorts API does not return HDMI0 when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Check AudioPorts Connected Status | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI0 not present in connected audio ports  |

---

<a id="check_hdcp_status_without_tv_connected"></a>
### TestCase Name
Check_HDCP_Status_Without_TV_Connected

### TestCase ID
DSWTV_5

### TestCase Objective
Checks getHDCPStatus API response when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Get HDCP Status | Invoke getHDCPStatus on org.rdk.HdcpProfile<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getHDCPStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `true` with `HDCPStatus.isConnected`: `false` and `HDCPStatus.isHDCPCompliant`: `false`, as expected when the TV is not connected  |

---

<a id="check_getcurrentresolution_status_without_tv_connected"></a>
### TestCase Name
Check_GetCurrentResolution_Status_Without_TV_Connected

### TestCase ID
DSWTV_6

### TestCase Objective
Checks getCurrentResolution API response when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Get CurrentResolution Status | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="check_setcurrentresolution_status_without_tv_connected"></a>
### TestCase Name
Check_SetCurrentResolution_Status_Without_TV_Connected

### TestCase ID
DSWTV_7

### TestCase Objective
Checks setCurrentResolution API response when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Check SetCurrentResolution Status | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0", resolution: "720p"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": "720p", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="check_getdefaultresolution_status_without_tv_connected"></a>
### TestCase Name
Check_GetDefaultResolution_Status_Without_TV_Connected

### TestCase ID
DSWTV_8

### TestCase Objective
Checks getDefaultResolution API response when TV is not connected

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Check GetDefaultResolution Status | Invoke getDefaultResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` is `false` (expected error response)  |

---

<a id="check_portname_status_without_tv_connected"></a>
### TestCase Name
Check_PortName_Status_Without_TV_Connected

### TestCase ID
DSWTV_9

### TestCase Objective
Checks portname API response when TV is not connected

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true`, HDMI input not present in connected video displays  |
| 2 | Check PortName Status | Invoke portname on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.portname"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |

## Plugin Post-conditions

_No plugin-level post-conditions defined_

## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 2 minutes |
| Priority | Medium |
| TDK Release Version | M103 |

<div align="right"><a href="#">&#8593; Go to Top</a></div>
