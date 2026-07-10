# RDK Services — OCDM Plugin Requirements

> **Module:** OCDM (`OCDM.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_OCDM.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_OCDM.md)
> **Total requirements:** 2 | **Total test cases:** 2

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | DRM key system information query | Content Protection API | 1 | OCDM_Get_All_DRM_Info |
| RDKSVC-REQ-002 | Plugin lifecycle event notifications | Event API | 1 | OCDM_ActivateDeactivate_Event_Test |
| | **Total** | | **2** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL return a list of all registered DRM key systems with their capabilities and status information in the correct response schema. |
| `RDKSVC-REQ-002` | SHALL fire a plugin state change notification with the correct plugin identifier and state during OCDM plugin activation and deactivation. |
