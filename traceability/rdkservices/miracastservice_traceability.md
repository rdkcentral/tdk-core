# RDK Services — MiracastService Plugin Traceability

> **Module:** MiracastService (`org.rdk.MiracastService.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 4 | **Total test cases:** 7
> **Source:** [RDKV_CERT_AVS_MiracastService.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── miracastservice_requirements.md
├── miracastservice_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (3 tests  — Miracast enable state)
    ├── RDKSVC-REQ-002/   (2 tests  — Client connection management)
    ├── RDKSVC-REQ-003/   (1 test  — Video display area)
    ├── RDKSVC-REQ-004/   (1 test  — Plugin lifecycle events)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 3 | [MiracastService_Get_Enable](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_get_enable) [MiracastService_Set_Get_Enable](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_set_get_enable) [MiracastService_Set_Enable_Without_Parameter](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_set_enable_without_parameter) |
| `RDKSVC-REQ-002` | 2 | [MiracastService_Accept_Client_Connection](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_accept_client_connection) [MiracastService_Reject_Client_Connection](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_reject_client_connection) |
| `RDKSVC-REQ-003` | 1 | [MiracastService_Set_VideoRectangle](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_set_videorectangle) |
| `RDKSVC-REQ-004` | 1 | [MiracastService_ActivateDeactivate_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md#miracastservice_activatedeactivate_event_test) |
