# RDK Services — HDCPProfile Plugin Requirements

> **Module:** HDCPProfile (`org.rdk.HdcpProfile.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_HDCP_Profile.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HDCP_Profile.md)
> **Total requirements:** 2 | **Total test cases:** 4

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | HDCP connection details and supported version — getHDCPStatus, getSettopHDCPSupport | Content Protection API | 2 | Get_HDCP_Details, Get_STB_Supported_HDCP_Version |
| RDKSVC-REQ-002 | Plugin event notifications — statechange, all events | Event API | 2 | HdcpProfile_ActivateDeactivate_Event_Test, HdcpProfile_ActivateDeactivate_All_Event_Test |
| | **Total** | | **4** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the HDCPProfile `getHDCPStatus` and `getSettopHDCPSupport` JSON-RPC methods to return current HDCP connection details including encryption status and negotiated protocol version, and the HDCP version supported by the STB hardware. |
| `RDKSVC-REQ-002` | SHALL fire the `statechange` event with correct plugin identifier and state payload during HDCPProfile plugin activate and deactivate operations, and correctly handle all-event (`all`) registration for system-wide notifications. |
