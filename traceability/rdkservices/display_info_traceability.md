# RDK Services — DisplayInfo Plugin Traceability

> **Module:** DisplayInfo (`DisplayInfo.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 9 | **Total test cases:** 25
> **Source:** [RDKV_CERT_AVS_Display_Info.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── display_info_requirements.md
├── display_info_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (2 tests  — HDMI connection status)
    ├── RDKSVC-REQ-002/   (4 tests  — Display resolution and output)
    ├── RDKSVC-REQ-003/   (3 tests  — EDID and physical dimensions)
    ├── RDKSVC-REQ-004/   (3 tests  — HDR capabilities and active format)
    ├── RDKSVC-REQ-005/   (5 tests  — Color and signal metadata)
    ├── RDKSVC-REQ-006/   (2 tests  — Content protection)
    ├── RDKSVC-REQ-007/   (2 tests  — GPU memory)
    ├── RDKSVC-REQ-008/   (2 tests  — Resolution change events)
    ├── RDKSVC-REQ-009/   (2 tests  — Plugin lifecycle stress and events)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 2 | [DisplayInfo_GET_HDMI_Connected](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_hdmi_connected) [DisplayInfo_Check_HDMI_Connection_Status_Without_TV](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_check_hdmi_connection_status_without_tv) |
| `RDKSVC-REQ-002` | 4 | [DisplayInfo_GET_resolution_width](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_resolution_width) [DisplayInfo_GET_resolution_height](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_resolution_height) [DisplayInfo_GET_vertical_frequency](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_vertical_frequency) [DisplayInfo_GET_portname](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_portname) |
| `RDKSVC-REQ-003` | 3 | [DisplayInfo_Get_EDID_DATA](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_edid_data) [DisplayInfo_Get_Widthincentimeters](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_widthincentimeters) [DisplayInfo_Get_Heightincentimeters](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_heightincentimeters) |
| `RDKSVC-REQ-004` | 3 | [DisplayInfo_GET_HDR_Formats_TV](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_hdr_formats_tv) [DisplayInfo_GET_HDR_Formats_STB](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_hdr_formats_stb) [DisplayInfo_GET_HDR_Format_In_Use](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_hdr_format_in_use) |
| `RDKSVC-REQ-005` | 5 | [DisplayInfo_GET_Color_Space](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_color_space) [DisplayInfo_Get_Colour_Depth](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_colour_depth) [DisplayInfo_Get_Quantization_Range](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_quantization_range) [DisplayInfo_Get_Colorimetry](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_colorimetry) [DisplayInfo_Get_EOTF](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_eotf) |
| `RDKSVC-REQ-006` | 2 | [DisplayInfo_GET_HDCP_protocol_version](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_hdcp_protocol_version) [DisplayInfo_GET_audiopassthrough](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_audiopassthrough) |
| `RDKSVC-REQ-007` | 2 | [DisplayInfo_Get_Total_GPU_RAM](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_total_gpu_ram) [DisplayInfo_Get_Free_GPU_RAM](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_get_free_gpu_ram) |
| `RDKSVC-REQ-008` | 2 | [DisplayInfo_Check_Resolution_PreChange_Event](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_check_resolution_prechange_event) [DisplayInfo_Check_Resolution_PostChange_Event](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_check_resolution_postchange_event) |
| `RDKSVC-REQ-009` | 2 | [DisplayInfo_ActivateDeactivate_STRESS](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_activatedeactivate_stress) [DisplayInfo_ActivateDeactivate_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Display_Info.md#displayinfo_activatedeactivate_event_test) |
