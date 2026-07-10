# RDK Services — Monitor Plugin Requirements

> **Module:** Monitor (`Monitor.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_Monitor.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Monitor.md)
> **Total requirements:** 3 | **Total test cases:** 6

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Plugin resource statistics monitoring | Statistics API | 2 | Monitor_Reset_Statistics_NetworkManager, Monitor_Get_Status_NetworkManager |
| RDKSVC-REQ-002 | Process restart threshold configuration | Configuration API | 2 | Monitor_Restart_Limits_NetworkManager, Monitor_Verify_restartlimits_Info_Error |
| RDKSVC-REQ-003 | Plugin lifecycle event notifications | Event API | 2 | Monitor_ActivateDeactivate_Event_Test, Monitor_ActivateDeactivate_All_Event_Test |
| | **Total** | | **6** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the Monitor `resetStatistics` and `status` JSON-RPC methods to reset collected CPU and memory statistics for a monitored plugin (NetworkManager) and return current resource usage statistics with correct response schema. |
| `RDKSVC-REQ-002` | SHALL implement the Monitor `restartLimits` JSON-RPC method to set process restart limits for a monitored plugin (NetworkManager), and return a correct error response for `restartLimits` requests with invalid or missing plugin information. |
| `RDKSVC-REQ-003` | SHALL fire the `statechange` event with correct plugin identifier and state payload during Monitor plugin activate and deactivate operations, and correctly handle all-event (`all`) registration for system-wide notifications. |
