# RDK Services — MessageControl Plugin Requirements

> **Module:** MessageControl (`MessageControl.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_Message_Control.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md)
> **Total requirements:** 6 | **Total test cases:** 17

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | Functional Capability | Classification | # Tests | Test Cases |
|--------|----------------------|----------------|---------|------------|
| RDKSVC-REQ-001 | System log category trace level control | Trace Control API | 2 | MessageControl_Application_Toggle_All_Tracelevels, MessageControl_SysLog_Toggle_All_Tracelevels |
| RDKSVC-REQ-002 | Security and content protection plugin trace level control | Trace Control API | 2 | MessageControl_OCDM_Plugin_Toggle_All_Tracelevels, MessageControl_SecurityAgent_Plugin_Toggle_All_Tracelevels |
| RDKSVC-REQ-003 | Network connectivity plugin trace level control | Trace Control API | 2 | MessageControl_LocationSync_Plugin_Toggle_All_Tracelevels, MessageControl_LISA_Plugin_Toggle_All_Tracelevels |
| RDKSVC-REQ-004 | Media player and display plugin trace level control | Trace Control API | 4 | MessageControl_Cobalt_Plugin_Toggle_All_Tracelevels, MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels, MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels, MessageControl_WebKitBrowser_Plugin_Toggle_All_Tracelevels |
| RDKSVC-REQ-005 | Platform service plugin trace level control | Trace Control API | 6 | MessageControl_System_Plugin_Toggle_All_Tracelevels, MessageControl_Monitor_Plugin_Toggle_All_Tracelevels, MessageControl_Messenger_Plugin_Toggle_All_Tracelevels, MessageControl_DeviceIdentification_Plugin_Toggle_All_Tracelevels, MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels, MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels |
| RDKSVC-REQ-006 | Plugin lifecycle event notifications | Event API | 1 | MessageControl_ActivateDeactivate_Event_Test |
| | **Total** | | **17** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the MessageControl JSON-RPC API to enable and disable all trace levels for the Application and SysLog system-level log categories. |
| `RDKSVC-REQ-002` | SHALL implement the MessageControl JSON-RPC API to enable and disable all trace levels for the OCDM and SecurityAgent plugin log categories. |
| `RDKSVC-REQ-003` | SHALL implement the MessageControl JSON-RPC API to enable and disable all trace levels for the LocationSync and LISA plugin log categories. |
| `RDKSVC-REQ-004` | SHALL implement the MessageControl JSON-RPC API to enable and disable all trace levels for the Cobalt, DisplayInfo, PlayerInfo, and WebKitBrowser plugin log categories. |
| `RDKSVC-REQ-005` | SHALL implement the MessageControl JSON-RPC API to enable and disable all trace levels for the System, Monitor, Messenger, DeviceIdentification, DeviceInfo, and MessageControl plugin log categories, including the MessageControl plugin controlling its own trace levels. |
| `RDKSVC-REQ-006` | SHALL fire the `statechange` event with correct plugin identifier and state payload during MessageControl plugin activate and deactivate operations. |
