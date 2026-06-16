## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [DisplayInfo_GET_audiopassthrough (DISP_01)](#displayinfo_get_audiopassthrough-disp_01)
   - [DisplayInfo_GET_HDMI_Connected (DISP_02)](#displayinfo_get_hdmi_connected-disp_02)
   - [DisplayInfo_GET_resolution_width (DISP_03)](#displayinfo_get_resolution_width-disp_03)
   - [DisplayInfo_GET_resolution_height (DISP_04)](#displayinfo_get_resolution_height-disp_04)
   - [DisplayInfo_GET_vertical_frequency (DISP_05)](#displayinfo_get_vertical_frequency-disp_05)
   - [DisplayInfo_GET_HDCP_protocol_version (DISP_06)](#displayinfo_get_hdcp_protocol_version-disp_06)
   - [DisplayInfo_GET_portname (DISP_07)](#displayinfo_get_portname-disp_07)
   - [DisplayInfo_Get_EDID_DATA (DISP_08)](#displayinfo_get_edid_data-disp_08)
   - [DisplayInfo_ActivateDeactivate_STRESS (DISP_09)](#displayinfo_activatedeactivate_stress-disp_09)
   - [DisplayInfo_GET_HDR_Formats_TV (DISP_10)](#displayinfo_get_hdr_formats_tv-disp_10)
   - [DisplayInfo_GET_HDR_Formats_STB (DISP_11)](#displayinfo_get_hdr_formats_stb-disp_11)
   - [DisplayInfo_GET_HDR_Format_In_Use (DISP_12)](#displayinfo_get_hdr_format_in_use-disp_12)
   - [DisplayInfo_Get_Total_GPU_RAM (DISP_13)](#displayinfo_get_total_gpu_ram-disp_13)
   - [DisplayInfo_Get_Free_GPU_RAM (DISP_14)](#displayinfo_get_free_gpu_ram-disp_14)
   - [DisplayInfo_Get_Widthincentimeters (DISP_15)](#displayinfo_get_widthincentimeters-disp_15)
   - [DisplayInfo_Get_Heightincentimeters (DISP_16)](#displayinfo_get_heightincentimeters-disp_16)
   - [DisplayInfo_Check_Resolution_PostChange_Event (DISP_17)](#displayinfo_check_resolution_postchange_event-disp_17)
   - [DisplayInfo_Check_HDMI_Connection_Status_Without_TV (DISP_18)](#displayinfo_check_hdmi_connection_status_without_tv-disp_18)
   - [DisplayInfo_GET_Color_Space (DISP_19)](#displayinfo_get_color_space-disp_19)
   - [DisplayInfo_Get_Colour_Depth (DISP_20)](#displayinfo_get_colour_depth-disp_20)
   - [DisplayInfo_Get_Quantization_Range (DISP_21)](#displayinfo_get_quantization_range-disp_21)
   - [DisplayInfo_Get_Colorimetry (DISP_22)](#displayinfo_get_colorimetry-disp_22)
   - [DisplayInfo_Get_EOTF (DISP_23)](#displayinfo_get_eotf-disp_23)
   - [DisplayInfo_ActivateDeactivate_Event_Test (DISP_24)](#displayinfo_activatedeactivate_event_test-disp_24)
   - [DisplayInfo_Check_Resolution_PreChange_Event (DISP_25)](#displayinfo_check_resolution_prechange_event-disp_25)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DisplayInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `DisplayInfo` (version 1)

**API Coverage**

- **State / Query APIs**: `isaudiopassthrough`
- **Lifecycle / Control APIs**: `connected`
- **Events**: `updated`
- **Other APIs**: `colorimetry`, `colorspace`, `colourdepth`, `edid`, `eotf`, `freegpuram`, `hdcpprotection`, `hdrsetting`, `height`, `heightincentimeters`, `portname`, `quantizationrange`, `stbcapabilities`, `totalgpuram`, `tvcapabilities`, `verticalfreq`, `width`, `widthincentimeters`

### APIs Under Test

| API | Description |
|-----|-------------|
| `colorimetry` | Provides access to the display colorimetry |
| `colorspace` | Provides access to the display color space |
| `colourdepth` | Provides access to the display colour depth |
| `connected` | Check for display isconnected |
| `edid` | Provides TV's Extended Display Identification Data |
| `eotf` | Provides access to the display Electro Optical Transfer Function |
| `freegpuram` | Gets the free GPU DRAM memory in bytes |
| `hdcpprotection` | Get HDCP Version |
| `hdrsetting` | Gets HDR format in use |
| `height` | Provide vertical resolution of TV. |
| `heightincentimeters` | Gets the vertical size in centimeters |
| `isaudiopassthrough` | Read isaudioPassthrough property on HDMI. |
| `portname` | Get Video output port on the STB used for connection to TV |
| `quantizationrange` | Provides access to the display quantization range |
| `stbcapabilities` | Gets HDR formats supported by STB |
| `totalgpuram` | Gets the total GPU DRAM memory in bytes |
| `tvcapabilities` | Gets HDR formats supported by TV |
| `verticalfreq` | Get Vertical Frequency |
| `width` | Provides horizontal resolution of TV. |
| `widthincentimeters` | Gets the horizontal size in centimeters |

### Events Under Test

| Event | Description |
|-------|-------------|
| `updated` | Fires on changing the resolution |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Register_And_Listen_Events

- Register and listen to event `Event_Pre_Post_Resolution_Change` on `DisplayInfo` plugin

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="displayinfo_get_audiopassthrough-disp_01"></a>
### DisplayInfo_GET_audiopassthrough (DISP_01)

**Objective:** Read isaudioPassthrough property on HDMI.

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | IsAudiopassthrough | Invoke `isaudiopassthrough` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.isaudiopassthrough"}' http://127.0.0.1:9998/jsonrpc` | Response contains `isaudiopassthrough` boolean field — `true` if HDMI audio is passed through directly to the TV, `false` otherwise |

---

<a id="displayinfo_get_hdmi_connected-disp_02"></a>
### DisplayInfo_GET_HDMI_Connected (DISP_02)

**Objective:** Is HDMI connected.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | IsHDMIConnected | Invoke `connected` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | Response contains `connected` boolean field — `true` if an HDMI display is currently connected, `false` otherwise |

---

<a id="displayinfo_get_resolution_width-disp_03"></a>
### DisplayInfo_GET_resolution_width (DISP_03)

**Objective:** Get width of the current resolution.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | DisplaySettings getsupportedresolutions | Invoke `getSupportedResolutions` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Supported Resolutions returned successfully |
| 3 | Getresolutionwidth | Invoke `width` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.width"}' http://127.0.0.1:9998/jsonrpc` | Response returns horizontal resolution width in pixels — value matches the width mapped from the current resolution retrieved in Step 2 |

---

<a id="displayinfo_get_resolution_height-disp_04"></a>
### DisplayInfo_GET_resolution_height (DISP_04)

**Objective:** Get height of the current resolution.

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | DisplaySettings getsupportedresolutions | Invoke `getSupportedResolutions` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Supported Resolutions returned successfully |
| 3 | Getresolutionheight | Invoke `height` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.height"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical resolution height in pixels — value matches the height mapped from the current resolution retrieved in Step 2 |

---

<a id="displayinfo_get_vertical_frequency-disp_05"></a>
### DisplayInfo_GET_vertical_frequency (DISP_05)

**Objective:** Get Vertical frequency.

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Getverticalfrequency | Invoke `verticalfreq` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.verticalfreq"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical refresh frequency in mHz as a non-zero positive integer |

---

<a id="displayinfo_get_hdcp_protocol_version-disp_06"></a>
### DisplayInfo_GET_HDCP_protocol_version (DISP_06)

**Objective:** Get HDCP version.

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Gethdcpversion | Invoke `hdcpprotection` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdcpprotection"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current HDCP protocol version — one of: `HdcpUnencrypted`, `Hdcp1X`, `Hdcp2X`, or `HdcpAuto` |

---

<a id="displayinfo_get_portname-disp_07"></a>
### DisplayInfo_GET_portname (DISP_07)

**Objective:** Get portname used for TV connection.

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Getportname | Invoke `portname` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.portname"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty video output port name used for the TV connection |

---

<a id="displayinfo_get_edid_data-disp_08"></a>
### DisplayInfo_Get_EDID_DATA (DISP_08)

**Objective:** Get EDID of connected display

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Connected Device  EDID Details | Invoke `readEDID` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | EDID data string returned from the connected display via `org.rdk.DisplaySettings` (base64-encoded, non-empty) |
| 2 | GetEDID | Invoke `edid` on `DisplayInfo` with `length`: `"<DISPLAYINFO_EDID_DATA_LENGTH>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.edid", "params": {"length": "<DISPLAYINFO_EDID_DATA_LENGTH>"}}' http://127.0.0.1:9998/jsonrpc` | EDID data returned by `DisplayInfo` matches the EDID data retrieved from `org.rdk.DisplaySettings` in Step 1 |

---

<a id="displayinfo_activatedeactivate_stress-disp_09"></a>
### DisplayInfo_ActivateDeactivate_STRESS (DISP_09)

**Objective:** Activates and deactivates the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

> **Stress Loop:** The step sequence below forms one iteration block. It is repeated **`<STRESS_TEST_REPEAT_COUNT>`** times as set in the device configuration file (key: `STRESS_TEST_REPEAT_COUNT`).

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check DisplayInfo Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate DisplayInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate DisplayInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Get CPU Load | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | CPU load is retrieved and validated successfully |

**Post-condition:**

#### Post-condition 1: Check_PluginActive_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="displayinfo_get_hdr_formats_tv-disp_10"></a>
### DisplayInfo_GET_HDR_Formats_TV (DISP_10)

**Objective:** Gets the HDR formats supported by TV

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetHDRFormatsTV | Invoke `tvcapabilities` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.tvcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty array of HDR formats supported by the connected TV — each entry is one of: `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

---

<a id="displayinfo_get_hdr_formats_stb-disp_11"></a>
### DisplayInfo_GET_HDR_Formats_STB (DISP_11)

**Objective:** Gets the HDR formats supported by STB

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetHDRFormatsSTB | Invoke `stbcapabilities` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.stbcapabilities"}' http://127.0.0.1:9998/jsonrpc` | Response returns a non-empty array of HDR formats supported by the STB — each entry is one of: `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

---

<a id="displayinfo_get_hdr_format_in_use-disp_12"></a>
### DisplayInfo_GET_HDR_Format_In_Use (DISP_12)

**Objective:** Gets the HDR formats in use

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | GetHDRFormatInUse | Invoke `hdrsetting` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.hdrsetting"}' http://127.0.0.1:9998/jsonrpc` | Response returns the HDR format currently active on the display — one of: `HdrOff`, `Hdr10`, `Hdr10Plus`, `HdrHlg`, `HdrDolbyvision`, `HdrTechnicolor` |

---

<a id="displayinfo_get_total_gpu_ram-disp_13"></a>
### DisplayInfo_Get_Total_GPU_RAM (DISP_13)

**Objective:** Gets the total GPU DRAM memory in bytes

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Total GPU RAM | Invoke `totalgpuram` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.totalgpuram"}' http://127.0.0.1:9998/jsonrpc` | Response returns total GPU DRAM memory in bytes as a non-zero positive integer |

---

<a id="displayinfo_get_free_gpu_ram-disp_14"></a>
### DisplayInfo_Get_Free_GPU_RAM (DISP_14)

**Objective:** Gets the free GPU DRAM memory in bytes

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Free GPU RAM | Invoke `freegpuram` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.freegpuram"}' http://127.0.0.1:9998/jsonrpc` | Response returns free GPU DRAM memory in bytes as a non-negative integer (value ≤ `totalgpuram`) |

---

<a id="displayinfo_get_widthincentimeters-disp_15"></a>
### DisplayInfo_Get_Widthincentimeters (DISP_15)

**Objective:** Gets the horizontal size in centimeters

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Width In Centimeters | Invoke `widthincentimeters` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.widthincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Response returns horizontal screen size in centimeters as a non-zero positive integer |

---

<a id="displayinfo_get_heightincentimeters-disp_16"></a>
### DisplayInfo_Get_Heightincentimeters (DISP_16)

**Objective:** Gets the vertical size in centimeters

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Height In Centimeters | Invoke `heightincentimeters` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.heightincentimeters"}' http://127.0.0.1:9998/jsonrpc` | Response returns vertical screen size in centimeters as a non-zero positive integer |

---

<a id="displayinfo_check_resolution_postchange_event-disp_17"></a>
### DisplayInfo_Check_Resolution_PostChange_Event (DISP_17)

**Objective:** Checks for the Resolution Post Change event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | Get Supported Resolutions | Invoke `getSupportedResolutions` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Supported Resolutions returned successfully |
| 3 | Get Current Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Current Resolution returned successfully |
| 4 | Retrieve Current Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Current Resolution returned successfully |
| 5 | Set Resolution | *(Loop: iterates for each resolution listed in `RESOLUTION_WIDTH_HEIGHT_MAPPING`)* Invoke `setCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`, `resolution`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Resolution change applied to the display |
| 6 | Get Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Returned resolution matches the value set in Step 5 |
| 7 | Check Updated PostRequisite Change Event | *(Conditional: executed only if resolution changed between Step 4 and Step 6)*<br>Listen for `Event_Pre_Post_Resolution_Change` event (timeout: 2s) | Expected `postresolutionchange` event received confirming the resolution change completed |
| 8 | Check Updated PostRequisite Change Event | *(Conditional: executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for `Event_Pre_Post_Resolution_Change` event (timeout: 2s) | No `postresolutionchange` event received — resolution was already at the target value; event is absent or empty |

---

<a id="displayinfo_check_hdmi_connection_status_without_tv-disp_18"></a>
### DisplayInfo_Check_HDMI_Connection_Status_Without_TV (DISP_18)

**Objective:** Checks the HDMI connection status when TV is not connected

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | IsHDMIConnected | Invoke `connected` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.connected"}' http://127.0.0.1:9998/jsonrpc` | `connected`: `false` — HDMI display is not connected (test requires TV disconnected as pre-condition) |

---

<a id="displayinfo_get_color_space-disp_19"></a>
### DisplayInfo_GET_Color_Space (DISP_19)

**Objective:** Gets the display color space

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Color Space | Invoke `colorspace` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorspace"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display color space — one of: `FORMATUNKNOWN`, `FORMATOTHER`, `FORMATRGB444`, `FORMATYCBCR444`, `FORMATYCBCR422`, `FORMATYCBCR420` |

---

<a id="displayinfo_get_colour_depth-disp_20"></a>
### DisplayInfo_Get_Colour_Depth (DISP_20)

**Objective:** Gets the display colour depth

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Colour Depth | Invoke `colourdepth` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colourdepth"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display colour depth — one of: `COLORDEPTHUNKNOWN`, `COLORDEPTH8BIT`, `COLORDEPTH10BIT`, `COLORDEPTH12BIT` |

---

<a id="displayinfo_get_quantization_range-disp_21"></a>
### DisplayInfo_Get_Quantization_Range (DISP_21)

**Objective:** Gets the display quantization range

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Quantization Range | Invoke `quantizationrange` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.quantizationrange"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display quantization range — one of: `QUANTIZATIONRANGEUNKNOWN`, `QUANTIZATIONRANGELIMITED`, `QUANTIZATIONRANGEFULL` |

---

<a id="displayinfo_get_colorimetry-disp_22"></a>
### DisplayInfo_Get_Colorimetry (DISP_22)

**Objective:** Gets the display colorimetry

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Colorimetry | Invoke `colorimetry` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.colorimetry"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current display colorimetry — one of the values configured in `DISPLAYINFO_SUPPORTED_COLORIMETRY_LIST` (e.g., `BT2020cL`, `BT2020ncl`, `DCI_P3`, `Sycc601`) |

---

<a id="displayinfo_get_eotf-disp_23"></a>
### DisplayInfo_Get_EOTF (DISP_23)

**Objective:** Gets the display Electro Optical Transfer Function

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get EOTF | Invoke `eotf` on `DisplayInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DisplayInfo.1.eotf"}' http://127.0.0.1:9998/jsonrpc` | Response returns the current Electro Optical Transfer Function in use — one of: `EOTFUNKNOWN`, `EOTFOTHER`, `EOTFBT1886`, `EOTFBT2100`, `EOTFSMPTEST2084` |

---

<a id="displayinfo_activatedeactivate_event_test-disp_24"></a>
### DisplayInfo_ActivateDeactivate_Event_Test (DISP_24)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DisplayInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DisplayInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `displayinfo`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DisplayInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DisplayInfo"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DisplayInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `displayinfo`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DisplayInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="displayinfo_check_resolution_prechange_event-disp_25"></a>
### DisplayInfo_Check_Resolution_PreChange_Event (DISP_25)

**Objective:** Checks for the Resolution Pre Change event

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | Get Supported Resolutions | Invoke `getSupportedResolutions` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Supported Resolutions returned successfully |
| 3 | Get Current Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Current Resolution returned successfully |
| 4 | Retrieve Current Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Current Resolution returned successfully |
| 5 | Set Resolution | *(Loop: iterates for each resolution listed in `RESOLUTION_WIDTH_HEIGHT_MAPPING`)* Invoke `setCurrentResolution` on `org.rdk.DisplaySettings` with `videoDisplay`: `"<result_step_1>"`, `resolution`: `"<result_step_2>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Resolution change applied to the display |
| 6 | Get Resolution | Invoke `getCurrentResolution` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Returned resolution matches the value set in Step 5 |
| 7 | Check Updated PreResolution Change Event | *(Conditional: executed only if resolution changed between Step 4 and Step 6)*<br>Listen for `Event_Pre_Post_Resolution_Change` event (timeout: 2s) | Expected `preresolutionchange` event received confirming the display is about to apply the new resolution |
| 8 | Check Updated PreResolution Change Event | *(Conditional: executed only if resolution was unchanged between Step 4 and Step 6)*<br>Listen for `Event_Pre_Post_Resolution_Change` event (timeout: 2s) | No `preresolutionchange` event received — resolution was already at the target value; event is absent or empty |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M81 |