# RDK Services — HDCPProfile Plugin Traceability

> **Module:** HDCPProfile (`org.rdk.HdcpProfile.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 2 | **Total test cases:** 4
> **Source:** [RDKV_CERT_AVS_HDCP_Profile.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── hdcp_profile_requirements.md
├── hdcp_profile_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (2 tests  — HDCP connection details and supported version)
    ├── RDKSVC-REQ-002/   (2 tests  — Plugin event notifications)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 2 | [Get_HDCP_Details](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md#get_hdcp_details) [Get_STB_Supported_HDCP_Version](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md#get_stb_supported_hdcp_version) |
| `RDKSVC-REQ-002` | 2 | [HdcpProfile_ActivateDeactivate_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md#hdcpprofile_activatedeactivate_event_test) [HdcpProfile_ActivateDeactivate_All_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md#hdcpprofile_activatedeactivate_all_event_test) |
