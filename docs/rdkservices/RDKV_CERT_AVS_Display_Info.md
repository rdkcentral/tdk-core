## TestScript Name
RDKV_CERT_AVS_Display_Info

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
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
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **DisplayInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `DisplayInfo` (version 1)

## APIs Under Test

| API | Description |
| --- | --- |
| `colorimetry` | Provides access to the display colorimetry |
| `colorspace` | Provides access to the display color space |
| `colourdepth` | Provides access to the display colour depth |
| `connected` | Check for display isconnected |
| `edid` | Provides TV's Extended Display Identification Data |
| `eotf` | Provides access to the display Electro Optical Transfer Function |
| `freegpuram` | Gets the free GPU DRAM memory in bytes |
| `hdcpprotection` | Get HDCP Version |
| `hdrsetting` | Gets HDR format in use |
| `height` | Provide vertical resolution of TV |
| `heightincentimeters` | Gets the vertical size in centimeters |
| `isaudiopassthrough` | Read isaudioPassthrough property on HDMI |
| `portname` | Get Video output port on the STB used for connection to TV |
| `quantizationrange` | Provides access to the display quantization range |
| `stbcapabilities` | Gets HDR formats supported by STB |
| `totalgpuram` | Gets the total GPU DRAM memory in bytes |
| `tvcapabilities` | Gets HDR formats supported by TV |
| `verticalfreq` | Get Vertical Frequency |
| `width` | Provides horizontal resolution of TV |
| `widthincentimeters` | Gets the horizontal size in centimeters |

## Events Under Test

| Event | Description |
| --- | --- |
| `updated` | Fires on changing the resolution |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the updated event | Register a WebSocket event listener for `updated` to receive `updated` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.register", "params": {"event": "updated", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | IsAudiopassthrough | Invoke isaudiopassthrough on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.isaudiopassthrough"}' http://127.0.0.1:9998/jsonrpc` | Response contains `isaudiopassthrough` boolean field — `true` if HDMI audio is passed through directly to the TV, `false` otherwise |

---

<a id="displayinfo_get_hdmi_connected"></a>
### TestCase Name
DisplayInfo_GET_HDMI_Connected

### TestCase ID
DISP_02

### TestCase Objective
Is HDMI connected.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | IsHDMIConnected | Invoke connected on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | Response contains `connected` boolean field — `true` if an HDMI display is currently connected, `false` otherwise |

---

<a id="displayinfo_get_resolution_width"></a>
### TestCase Name
DisplayInfo_GET_resolution_width

### TestCase ID
DISP_03

### TestCase Objective
Get width of the current resolution.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | DisplaySettings getsupportedresolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Getresolutionwidth | Invoke width on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.width"}' http://127.0.0.1:9998/jsonrpc` | Response returns horizontal resolution width in pixels — value matches the width mapped from the current resolution retrieved in Step 2 |

---

<a id="displayinfo_get_resolution_height"></a>
### TestCase Name
DisplayInfo_GET_resolution_height

### TestCase ID
DISP_04

### TestCase Objective
Get height of the current resolution.

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | DisplaySettings getsupportedresolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Getresolutionheight | Invoke height on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.height"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical resolution height in pixels — value matches the height mapped from the current resolution retrieved in Step 2 |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Getverticalfrequency | Invoke verticalfreq on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.verticalfreq"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical refresh frequency in mHz as a non-zero positive integer |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Gethdcpversion | Invoke hdcpprotection on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdcpprotection"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current HDCP protocol version — one of `HdcpUnencrypted`, `Hdcp1X`, `Hdcp2X`, or `HdcpAuto` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Getportname | Invoke portname on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.portname"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty video output port name used for the TV connection |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Connected Device  EDID Details | Invoke readEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | EDID data string returned from the connected display via `org.rdk.DisplaySettings` (base64-encoded, non-empty) |
| 2 | GetEDID | Invoke edid on DisplayInfo with length: "<DISPLAYINFO_EDID_DATA_LENGTH>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.edid", "params": {"length": "<DISPLAYINFO_EDID_DATA_LENGTH>"}}' http://127.0.0.1:9998/jsonrpc` | EDID data returned by `DisplayInfo` matches the EDID data retrieved from `org.rdk.DisplaySettings` in Step 1 |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

> **Stress Loop:** The step sequence below forms one iteration block. It is repeated **`<STRESS_TEST_REPEAT_COUNT>`** times as set in the device configuration file

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check DisplayInfo Active Status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate DisplayInfo Plugin | Invoke deactivate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 3 | Activate DisplayInfo Plugin | Invoke activate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 4 | Get CPU Load | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the CPU load is retrieved and validated successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Check_PluginActive_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetHDRFormatsTV | Invoke tvcapabilities on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.tvcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty array of HDR formats supported by the connected TV — each entry is one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetHDRFormatsSTB | Invoke stbcapabilities on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.stbcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty array of HDR formats supported by the STB — each entry is one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | GetHDRFormatInUse | Invoke hdrsetting on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdrsetting"}' http://127.0.0.1:9998/jsonrpc` | Response returns the HDR format currently active on the display — one of `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Total GPU RAM | Invoke totalgpuram on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.totalgpuram"}' http://127.0.0.1:9998/jsonrpc` | Response returns total GPU DRAM memory in bytes as a non-zero positive integer |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Free GPU RAM | Invoke freegpuram on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.freegpuram"}' http://127.0.0.1:9998/jsonrpc` | Response returns free GPU DRAM memory in bytes as a non-negative integer (value ≤ `totalgpuram`) |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Width In Centimeters | Invoke widthincentimeters on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.widthincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Response returns horizontal screen size in centimeters as a non-zero positive integer |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Height In Centimeters | Invoke heightincentimeters on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.heightincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical screen size in centimeters as a non-zero positive integer |

---

<a id="displayinfo_check_resolution_postchange_event"></a>
### TestCase Name
DisplayInfo_Check_Resolution_PostChange_Event

### TestCase ID
DISP_17

### TestCase Objective
Checks for the Resolution Post Change event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 4 | Retrieve Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 5 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the resolution change is applied to the display |
| 6 | Get Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Returned resolution matches the value set in Step 5 |
| 7 | Check Updated PostRequisite Change Event | *(Conditional statement executed only if resolution changed between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event (timeout: 2s) | Expected `postresolutionchange` event received confirming the resolution change completed |
| 8 | Check Updated PostRequisite Change Event | *(Conditional statement executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event (timeout: 2s) | No `postresolutionchange` event received — resolution was already at the target value; event is absent or empty |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | IsHDMIConnected | Invoke connected on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | `connected`: `false` — HDMI display is not connected (test requires TV disconnected as pre-condition) |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Color Space | Invoke colorspace on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorspace"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display color space — one of `FORMATUNKNOWN`, `FORMATOTHER`, `FORMATRGB444`, `FORMATYCBCR444`, `FORMATYCBCR422`, `FORMATYCBCR420` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Colour Depth | Invoke colourdepth on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colourdepth"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display colour depth — one of `COLORDEPTHUNKNOWN`, `COLORDEPTH8BIT`, `COLORDEPTH10BIT`, `COLORDEPTH12BIT` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Quantization Range | Invoke quantizationrange on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.quantizationrange"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display quantization range — one of `QUANTIZATIONRANGEUNKNOWN`, `QUANTIZATIONRANGELIMITED`, `QUANTIZATIONRANGEFULL` |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Colorimetry | Invoke colorimetry on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorimetry"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display colorimetry — one of the values configured in `DISPLAYINFO_SUPPORTED_COLORIMETRY_LIST` (e.g., `BT2020cL`, `BT2020ncl`, `DCI_P3`, `Sycc601`) |

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

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get EOTF | Invoke eotf on DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.eotf"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current Electro Optical Transfer Function in use — one of `EOTFUNKNOWN`, `EOTFOTHER`, `EOTFBT1886`, `EOTFBT2100`, `EOTFSMPTEST2084` |

---

<a id="displayinfo_activatedeactivate_event_test"></a>
### TestCase Name
DisplayInfo_ActivateDeactivate_Event_Test

### TestCase ID
DISP_24

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplayInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DisplayInfo Plugin | Invoke deactivate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `displayinfo` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DisplayInfo Plugin | Invoke activate on Controller with callsign: "DisplayInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | Verify that the `statechange` event is received for callsign `displayinfo` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for DisplayInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="displayinfo_check_resolution_prechange_event"></a>
### TestCase Name
DisplayInfo_Check_Resolution_PreChange_Event

### TestCase ID
DISP_25

### TestCase Objective
Checks for the Resolution Pre Change event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 4 | Retrieve Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the current resolution is returned successfully |
| 5 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the resolution change is applied to the display |
| 6 | Get Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Returned resolution matches the value set in Step 5 |
| 7 | Check Updated PreResolution Change Event | *(Conditional statement executed only if resolution changed between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event (timeout: 2s) | Expected `preresolutionchange` event received confirming the display is about to apply the new resolution |
| 8 | Check Updated PreResolution Change Event | *(Conditional statement executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for Event_Pre_Post_Resolution_Change event (timeout: 2s) | No `preresolutionchange` event received — resolution was already at the target value; event is absent or empty |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the updated event | Unregister the WebSocket event listener for `updated` to stop receiving `updated` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.unregister", "params": {"event": "updated", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M81 |
