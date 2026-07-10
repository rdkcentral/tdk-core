# RDK Services — Monitor Plugin Traceability

> **Module:** Monitor (`Monitor.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 3 | **Total test cases:** 6
> **Source:** [RDKV_CERT_AVS_Monitor.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── monitor_requirements.md
├── monitor_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (2 tests  — Plugin statistics management)
    ├── RDKSVC-REQ-002/   (2 tests  — Restart limits configuration)
    ├── RDKSVC-REQ-003/   (2 tests  — Plugin lifecycle events)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 2 | [Monitor_Reset_Statistics_NetworkManager](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_reset_statistics_networkmanager) [Monitor_Get_Status_NetworkManager](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_get_status_networkmanager) |
| `RDKSVC-REQ-002` | 2 | [Monitor_Restart_Limits_NetworkManager](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_restart_limits_networkmanager) [Monitor_Verify_restartlimits_Info_Error](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_verify_restartlimits_info_error) |
| `RDKSVC-REQ-003` | 2 | [Monitor_ActivateDeactivate_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_activatedeactivate_event_test) [Monitor_ActivateDeactivate_All_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md#monitor_activatedeactivate_all_event_test) |
