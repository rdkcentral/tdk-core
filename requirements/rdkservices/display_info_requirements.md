# RDK Services — DisplayInfo Plugin Requirements

> **Module:** DisplayInfo (`DisplayInfo.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_Display_Info.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md)
> **Total requirements:** 9 | **Total test cases:** 25

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | HDMI connection status — hdmiConnected | Display Connection API | 2 | DisplayInfo_GET_HDMI_Connected, DisplayInfo_Check_HDMI_Connection_Status_Without_TV |
| RDKSVC-REQ-002 | Display resolution and output — resolution, verticalFrequency, portName | Display Properties API | 4 | DisplayInfo_GET_resolution_width, DisplayInfo_GET_resolution_height, DisplayInfo_GET_vertical_frequency, DisplayInfo_GET_portname |
| RDKSVC-REQ-003 | EDID and physical dimensions — EDID data, widthInCentimeters, heightInCentimeters | EDID API | 3 | DisplayInfo_Get_EDID_DATA, DisplayInfo_Get_Widthincentimeters, DisplayInfo_Get_Heightincentimeters |
| RDKSVC-REQ-004 | HDR capabilities and active format — HDR formats (TV/STB), HDR in use | HDR API | 3 | DisplayInfo_GET_HDR_Formats_TV, DisplayInfo_GET_HDR_Formats_STB, DisplayInfo_GET_HDR_Format_In_Use |
| RDKSVC-REQ-005 | Color and signal metadata — colorSpace, colourDepth, quantizationRange, colorimetry, EOTF | Color Signal API | 5 | DisplayInfo_GET_Color_Space, DisplayInfo_Get_Colour_Depth, DisplayInfo_Get_Quantization_Range, DisplayInfo_Get_Colorimetry, DisplayInfo_Get_EOTF |
| RDKSVC-REQ-006 | Content protection — HDCP protocol version, audio passthrough | Content Protection API | 2 | DisplayInfo_GET_HDCP_protocol_version, DisplayInfo_GET_audiopassthrough |
| RDKSVC-REQ-007 | GPU memory — totalGpuRam, freeGpuRam | GPU Resource API | 2 | DisplayInfo_Get_Total_GPU_RAM, DisplayInfo_Get_Free_GPU_RAM |
| RDKSVC-REQ-008 | Resolution change events — resolutionPreChange, resolutionPostChange | Event API | 2 | DisplayInfo_Check_Resolution_PreChange_Event, DisplayInfo_Check_Resolution_PostChange_Event |
| RDKSVC-REQ-009 | Plugin lifecycle stress and events — activate/deactivate | Stability & Event API | 2 | DisplayInfo_ActivateDeactivate_STRESS, DisplayInfo_ActivateDeactivate_Event_Test |
| | **Total** | | **25** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the DisplayInfo `hdmiConnected` JSON-RPC property to return the current HDMI connection state, and correctly report a disconnected state when no TV is connected to the HDMI output. |
| `RDKSVC-REQ-002` | SHALL implement the DisplayInfo JSON-RPC properties to return the current display output resolution width and height in pixels, the vertical refresh frequency in Hz, and the active display port name. |
| `RDKSVC-REQ-003` | SHALL implement the DisplayInfo JSON-RPC properties to return the connected display EDID data, and the physical display width and height in centimetres. |
| `RDKSVC-REQ-004` | SHALL implement the DisplayInfo JSON-RPC properties to return the HDR formats supported by the connected TV, the HDR formats supported by the STB, and the HDR format currently in use on the active output. |
| `RDKSVC-REQ-005` | SHALL implement the DisplayInfo JSON-RPC properties to return the current output color space, colour depth in bits, quantization range, colorimetry standard, and EOTF (Electro-Optical Transfer Function) in use on the active display output. |
| `RDKSVC-REQ-006` | SHALL implement the DisplayInfo JSON-RPC properties to return the HDCP protocol version negotiated with the connected display and the audio passthrough capability state. |
| `RDKSVC-REQ-007` | SHALL implement the DisplayInfo JSON-RPC properties to return the total GPU RAM and the current free GPU RAM in bytes. |
| `RDKSVC-REQ-008` | SHALL fire the `resolutionPreChange` and `resolutionPostChange` events with correct display output information before and after a display resolution change operation completes. |
| `RDKSVC-REQ-009` | SHALL sustain repeated deactivate and activate cycles of the DisplayInfo plugin without failure, and fire the `statechange` event with correct plugin identifier and state payload during activate and deactivate operations. |
