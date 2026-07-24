## TestScript Name
RDKV_CERT_AVS_Display_Info

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [DisplayInfo_GET_audiopassthrough](#displayinfo_get_audiopassthrough)
   - [DisplayInfo_GET_HDMI_Connected](#displayinfo_get_hdmi_connected)
   - [DisplayInfo_GET_resolution_width](#displayinfo_get_resolution_width)
   - [DisplayInfo_GET_resolution_height](#displayinfo_get_resolution_height)
   - [DisplayInfo_GET_vertical_frequency](#displayinfo_get_vertical_frequency)
   - [DisplayInfo_GET_HDCP_protocol_version](#displayinfo_get_hdcp_protocol_version)
   - [DisplayInfo_GET_portname](#displayinfo_get_portname)
   - [DisplayInfo_Get_EDID_DATA](#displayinfo_get_edid_data)
   - [DisplayInfo_ActivateDeactivate_STRESS](#displayinfo_activatedeactivate_stress)
   - [DisplayInfo_GET_HDR_Formats_TV](#displayinfo_get_hdr_formats_tv)
   - [DisplayInfo_GET_HDR_Formats_STB](#displayinfo_get_hdr_formats_stb)
   - [DisplayInfo_GET_HDR_Format_In_Use](#displayinfo_get_hdr_format_in_use)
   - [DisplayInfo_Get_Total_GPU_RAM](#displayinfo_get_total_gpu_ram)
   - [DisplayInfo_Get_Free_GPU_RAM](#displayinfo_get_free_gpu_ram)
   - [DisplayInfo_Get_Widthincentimeters](#displayinfo_get_widthincentimeters)
   - [DisplayInfo_Get_Heightincentimeters](#displayinfo_get_heightincentimeters)
   - [DisplayInfo_Check_Resolution_PostChange_Event](#displayinfo_check_resolution_postchange_event)
   - [DisplayInfo_Check_HDMI_Connection_Status_Without_TV](#displayinfo_check_hdmi_connection_status_without_tv)
   - [DisplayInfo_GET_Color_Space](#displayinfo_get_color_space)
   - [DisplayInfo_Get_Colour_Depth](#displayinfo_get_colour_depth)
   - [DisplayInfo_Get_Quantization_Range](#displayinfo_get_quantization_range)
   - [DisplayInfo_Get_Colorimetry](#displayinfo_get_colorimetry)
   - [DisplayInfo_Get_EOTF](#displayinfo_get_eotf)
   - [DisplayInfo_ActivateDeactivate_Event_Test](#displayinfo_activatedeactivate_event_test)
   - [DisplayInfo_Check_Resolution_PreChange_Event](#displayinfo_check_resolution_prechange_event)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **DisplayInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `DisplayInfo` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DisplayInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the updated event | Register a WebSocket event listener for `updated` to receive `updated` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.register", "params": {"event": "updated", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 4: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure EDID data length | `DISPLAYINFO_EDID_DATA_LENGTH` must be set to the expected length of the EDID data returned by the connected TV | The `DISPLAYINFO_EDID_DATA_LENGTH` value should be correctly configured in the device-specific config file |
| 2 | Configure supported colorimetry list | `DISPLAYINFO_SUPPORTED_COLORIMETRY_LIST` must be set to the colorimetry values supported by the connected TV | The `DISPLAYINFO_SUPPORTED_COLORIMETRY_LIST` value should be correctly configured in the device-specific config file |
| 3 | Configure NA tests | `DISPLAYINFO_NA_TESTS` must be set to the DisplayInfo test names to skip when not applicable on the DUT | The `DISPLAYINFO_NA_TESTS` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="displayinfo_get_audiopassthrough"></a>
### TestCase Name
DisplayInfo_GET_audiopassthrough

### TestCase ID
DISP_01

### TestCase Objective
Read isaudioPassthrough property on HDMI.

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check audio passthrough status | Invoke isaudiopassthrough on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.isaudiopassthrough"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains `isaudiopassthrough` boolean field — `true` if HDMI audio is passed through directly to the TV, `false` otherwise  |

---

<a id="displayinfo_get_hdmi_connected"></a>
### TestCase Name
DisplayInfo_GET_HDMI_Connected

### TestCase ID
DISP_02

### TestCase Objective
Is HDMI connected.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check HDMI connection status | Invoke connected on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response contains `connected` boolean field — `true` if an HDMI display is currently connected, `false` otherwise  |

---

<a id="displayinfo_get_resolution_width"></a>
### TestCase Name
DisplayInfo_GET_resolution_width

### TestCase ID
DISP_03

### TestCase Objective
Get width of the current resolution.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get supported resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Check resolution width | Invoke width on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.width"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the horizontal resolution width in pixels, matching the width mapped from the current resolution  |

---

<a id="displayinfo_get_resolution_height"></a>
### TestCase Name
DisplayInfo_GET_resolution_height

### TestCase ID
DISP_04

### TestCase Objective
Get height of the current resolution.

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get supported resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Check resolution height | Invoke height on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.height"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the vertical resolution height in pixels, matching the height mapped from the current resolution  |

---

<a id="displayinfo_get_vertical_frequency"></a>
### TestCase Name
DisplayInfo_GET_vertical_frequency

### TestCase ID
DISP_05

### TestCase Objective
Get Vertical frequency.

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check vertical refresh frequency | Invoke verticalfreq on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.verticalfreq"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns vertical refresh frequency in mHz as a non-zero positive integer  |

---

<a id="displayinfo_get_hdcp_protocol_version"></a>
### TestCase Name
DisplayInfo_GET_HDCP_protocol_version

### TestCase ID
DISP_06

### TestCase Objective
Get HDCP version.

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check HDCP protocol version | Invoke hdcpprotection on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdcpprotection"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current HDCP protocol version — one of `HdcpUnencrypted`, `Hdcp1X`, `Hdcp2X`, or `HdcpAuto`  |

---

<a id="displayinfo_get_portname"></a>
### TestCase Name
DisplayInfo_GET_portname

### TestCase ID
DISP_07

### TestCase Objective
Get portname used for TV connection.

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check video output port name | Invoke portname on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.portname"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns a non-empty video output port name used for the TV connection  |

---

<a id="displayinfo_get_edid_data"></a>
### TestCase Name
DisplayInfo_Get_EDID_DATA

### TestCase ID
DISP_08

### TestCase Objective
Get EDID of connected display

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Read EDID from DisplaySettings | Invoke readEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | Verify that the EDID data string returned from the connected display via `org.rdk.DisplaySettings` is a non-empty base64-encoded string  |
| 2 | Check EDID data matches DisplaySettings | Invoke edid on DisplayInfo with length: "<DISPLAYINFO_EDID_DATA_LENGTH>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.edid", "params": {"length": "<DISPLAYINFO_EDID_DATA_LENGTH>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the EDID data returned by `DisplayInfo` matches the EDID data retrieved from `org.rdk.DisplaySettings` in step 1  |

---

<a id="displayinfo_activatedeactivate_stress"></a>
### TestCase Name
DisplayInfo_ActivateDeactivate_STRESS

### TestCase ID
DISP_09

### TestCase Objective
Activates and deactivates the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

> **Stress Loop:** The step sequence below forms one iteration block. It is repeated **`<STRESS_TEST_REPEAT_COUNT>`** times as set in the device configuration file

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check DisplayInfo plugin status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate DisplayInfo plugin | Invoke deactivate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 3 | Activate DisplayInfo plugin | Invoke activate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 4 | Check CPU load | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the CPU load is retrieved and validated successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_PluginActive_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DeviceInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="displayinfo_get_hdr_formats_tv"></a>
### TestCase Name
DisplayInfo_GET_HDR_Formats_TV

### TestCase ID
DISP_10

### TestCase Objective
Gets the HDR formats supported by TV

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check HDR formats supported by TV | Invoke tvcapabilities on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.tvcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns a non-empty array of HDR formats supported by the connected TV (one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, or `HdrDolbyVision`)  |

---

<a id="displayinfo_get_hdr_formats_stb"></a>
### TestCase Name
DisplayInfo_GET_HDR_Formats_STB

### TestCase ID
DISP_11

### TestCase Objective
Gets the HDR formats supported by STB

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check HDR formats supported by STB | Invoke stbcapabilities on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.stbcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns a non-empty array of HDR formats supported by the STB (one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, or `HdrDolbyVision`)  |

---

<a id="displayinfo_get_hdr_format_in_use"></a>
### TestCase Name
DisplayInfo_GET_HDR_Format_In_Use

### TestCase ID
DISP_12

### TestCase Objective
Gets the HDR formats in use

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check active HDR format | Invoke hdrsetting on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdrsetting"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the HDR format currently active on the display (one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, or `HdrDolbyVision`)  |

---

<a id="displayinfo_get_total_gpu_ram"></a>
### TestCase Name
DisplayInfo_Get_Total_GPU_RAM

### TestCase ID
DISP_13

### TestCase Objective
Gets the total GPU DRAM memory in bytes

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check total GPU RAM | Invoke totalgpuram on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.totalgpuram"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns total GPU DRAM memory in bytes as a non-zero positive integer  |

---

<a id="displayinfo_get_free_gpu_ram"></a>
### TestCase Name
DisplayInfo_Get_Free_GPU_RAM

### TestCase ID
DISP_14

### TestCase Objective
Gets the free GPU DRAM memory in bytes

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check free GPU RAM | Invoke freegpuram on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.freegpuram"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns free GPU DRAM memory in bytes as a non-negative integer (value ≤ `totalgpuram`)  |

---

<a id="displayinfo_get_widthincentimeters"></a>
### TestCase Name
DisplayInfo_Get_Widthincentimeters

### TestCase ID
DISP_15

### TestCase Objective
Gets the horizontal size in centimeters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check screen width in centimeters | Invoke widthincentimeters on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.widthincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns horizontal screen size in centimeters as a non-zero positive integer  |

---

<a id="displayinfo_get_heightincentimeters"></a>
### TestCase Name
DisplayInfo_Get_Heightincentimeters

### TestCase ID
DISP_16

### TestCase Objective
Gets the vertical size in centimeters

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check screen height in centimeters | Invoke heightincentimeters on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.heightincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns vertical screen size in centimeters as a non-zero positive integer  |

---

<a id="displayinfo_check_resolution_postchange_event"></a>
### TestCase Name
DisplayInfo_Check_Resolution_PostChange_Event

### TestCase ID
DISP_17

### TestCase Objective
Checks for the Resolution Post Change event

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get supported resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get current resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 4 | Retrieve current resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 5 | Set display resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay, resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the resolution change is applied to the display |
| 6 | Check applied resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned resolution matches the value set in step 5  |
| 7 | Check updated post requisite change event | *(Conditional statement executed only if resolution changed between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event and wait up to 2 second(s) | Verify that the `postresolutionchange` event is received, confirming the resolution change completed successfully  |
| 8 | Check updated post requisite change event | *(Conditional statement executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event and wait up to 2 second(s) | Verify that no `postresolutionchange` event is received — resolution was already at the target value; event is absent or empty  |

---

<a id="displayinfo_check_hdmi_connection_status_without_tv"></a>
### TestCase Name
DisplayInfo_Check_HDMI_Connection_Status_Without_TV

### TestCase ID
DISP_18

### TestCase Objective
Checks the HDMI connection status when TV is not connected

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response does not contain any connected video display information |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check HDMI connection status | Invoke connected on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | Verify that `connected` is `false` — HDMI display is not connected (test requires TV disconnected as pre-condition)  |

---

<a id="displayinfo_get_color_space"></a>
### TestCase Name
DisplayInfo_GET_Color_Space

### TestCase ID
DISP_19

### TestCase Objective
Gets the display color space

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check color space | Invoke colorspace on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorspace"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current display color space (one of `FORMATUNKNOWN`, `FORMATOTHER`, `FORMATRGB444`, `FORMATYCBCR444`, etc.)  |

---

<a id="displayinfo_get_colour_depth"></a>
### TestCase Name
DisplayInfo_Get_Colour_Depth

### TestCase ID
DISP_20

### TestCase Objective
Gets the display colour depth

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display colour depth | Invoke colourdepth on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colourdepth"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current display colour depth (one of `COLORDEPTHUNKNOWN`, `COLORDEPTH8BIT`, `COLORDEPTH10BIT`, `COLORDEPTH12BIT`)  |

---

<a id="displayinfo_get_quantization_range"></a>
### TestCase Name
DisplayInfo_Get_Quantization_Range

### TestCase ID
DISP_21

### TestCase Objective
Gets the display quantization range

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display quantization range | Invoke quantizationrange on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.quantizationrange"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current display quantization range (one of `QUANTIZATIONRANGEUNKNOWN`, `QUANTIZATIONRANGELIMITED`, or `QUANTIZATIONRANGEFULL`)  |

---

<a id="displayinfo_get_colorimetry"></a>
### TestCase Name
DisplayInfo_Get_Colorimetry

### TestCase ID
DISP_22

### TestCase Objective
Gets the display colorimetry

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display colorimetry | Invoke colorimetry on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorimetry"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current display colorimetry as one of the values configured in `DISPLAYINFO_SUPPORTED_COLORIMETRY_LIST`  |

---

<a id="displayinfo_get_eotf"></a>
### TestCase Name
DisplayInfo_Get_EOTF

### TestCase ID
DISP_23

### TestCase Objective
Gets the display Electro Optical Transfer Function

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check current EOTF value | Invoke eotf on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.eotf"}' http://127.0.0.1:9998/jsonrpc` | Verify that the response returns the current Electro Optical Transfer Function in use (one of `EOTFUNKNOWN`, `EOTFOTHER`, `EOTFBT1886`, `EOTFST2084`, or `EOTFHLG`)  |

---

<a id="displayinfo_activatedeactivate_event_test"></a>
### TestCase Name
DisplayInfo_ActivateDeactivate_Event_Test

### TestCase ID
DISP_24

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

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
| 1 | Deactivate DisplayInfo plugin | Invoke deactivate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `displayinfo` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DisplayInfo plugin | Invoke activate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event and wait up to 2 second(s) | Verify that the `statechange` event is received for callsign `displayinfo` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="displayinfo_check_resolution_prechange_event"></a>
### TestCase Name
DisplayInfo_Check_Resolution_PreChange_Event

### TestCase ID
DISP_25

### TestCase Objective
Checks for the Resolution Pre Change event

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get supported resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get current resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 4 | Retrieve current resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 5 | Set display resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay, resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the resolution change is applied to the display |
| 6 | Check applied resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned resolution matches the value set in step 5  |
| 7 | Check updated pre resolution change event | *(Conditional statement executed only if resolution changed between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event and wait up to 2 second(s) | Verify that the `preresolutionchange` event is received, confirming the display is about to apply the new resolution  |
| 8 | Check updated pre resolution change event | *(Conditional statement executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event and wait up to 2 second(s) | Verify that no `preresolutionchange` event is received — resolution was already at the target value; event is absent or empty  |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the updated event | Unregister the WebSocket event listener for `updated` to stop receiving `updated` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.unregister", "params": {"event": "updated", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 20 mins

**Priority** : High

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
