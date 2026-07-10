# RDK Services — MiracastService Plugin Requirements

> **Module:** MiracastService (`org.rdk.MiracastService.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_MiracastService.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MiracastService.md)
> **Total requirements:** 4 | **Total test cases:** 7

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Miracast service enable state management | Service Control API | 3 | MiracastService_Get_Enable, MiracastService_Set_Get_Enable, MiracastService_Set_Enable_Without_Parameter |
| RDKSVC-REQ-002 | Miracast client connection management | Connection API | 2 | MiracastService_Accept_Client_Connection, MiracastService_Reject_Client_Connection |
| RDKSVC-REQ-003 | Miracast video display area configuration | Display API | 1 | MiracastService_Set_VideoRectangle |
| RDKSVC-REQ-004 | Plugin lifecycle event notifications | Event API | 1 | MiracastService_ActivateDeactivate_Event_Test |
| | **Total** | | **7** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHOULD implement the MiracastService `getEnable` and `setEnable` JSON-RPC methods to return the current Miracast service state and toggle it, and return a correct error code for `setEnable` calls submitted without required parameters. |
| `RDKSVC-REQ-002` | SHOULD implement the MiracastService `acceptClientConnection` and `rejectClientConnection` JSON-RPC methods to accept and reject incoming Miracast client connection requests and return correct response status. |
| `RDKSVC-REQ-003` | SHOULD implement the MiracastService `setVideoRectangle` JSON-RPC method to set the display rectangle coordinates for the Miracast video output and return a successful response. |
| `RDKSVC-REQ-004` | SHOULD fire the `statechange` event with correct plugin identifier and state payload during MiracastService plugin activate and deactivate operations. |
