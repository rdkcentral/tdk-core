# RDK Services — MessageControl Plugin Traceability

> **Module:** MessageControl (`MessageControl.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Total requirements:** 6 | **Total test cases:** 17
> **Source:** [RDKV_CERT_AVS_Message_Control.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md)

---

## Deliverable 2 — Test Case Folder Structure

```
testcases/rdkservices/
├── messagecontrol_requirements.md
├── messagecontrol_traceability.md
└── testcases/
    ├── RDKSVC-REQ-001/   (2 tests  — System log category trace levels)
    ├── RDKSVC-REQ-002/   (2 tests  — Security and content protection plugin trace levels)
    ├── RDKSVC-REQ-003/   (2 tests  — Connectivity and sync plugin trace levels)
    ├── RDKSVC-REQ-004/   (4 tests  — Media player and display plugin trace levels)
    ├── RDKSVC-REQ-005/   (6 tests  — Platform service plugin trace levels)
    ├── RDKSVC-REQ-006/   (1 test  — Plugin lifecycle events)
```

---

## Deliverable 3 — Requirements Traceability Matrix (RTM)

| Req ID | # Tests | Test Cases |
|--------|---------|------------|
| `RDKSVC-REQ-001` | 2 | [MessageControl_Application_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_application_toggle_all_tracelevels) [MessageControl_SysLog_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_syslog_toggle_all_tracelevels) |
| `RDKSVC-REQ-002` | 2 | [MessageControl_OCDM_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_ocdm_plugin_toggle_all_tracelevels) [MessageControl_SecurityAgent_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_securityagent_plugin_toggle_all_tracelevels) |
| `RDKSVC-REQ-003` | 2 | [MessageControl_LocationSync_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_locationsync_plugin_toggle_all_tracelevels) [MessageControl_LISA_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_lisa_plugin_toggle_all_tracelevels) |
| `RDKSVC-REQ-004` | 4 | [MessageControl_Cobalt_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_cobalt_plugin_toggle_all_tracelevels) [MessageControl_DisplayInfo_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_displayinfo_plugin_toggle_all_tracelevels) [MessageControl_PlayerInfo_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_playerinfo_plugin_toggle_all_tracelevels) [MessageControl_WebKitBrowser_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_webkitbrowser_plugin_toggle_all_tracelevels) |
| `RDKSVC-REQ-005` | 6 | [MessageControl_System_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_system_plugin_toggle_all_tracelevels) [MessageControl_Monitor_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_monitor_plugin_toggle_all_tracelevels) [MessageControl_Messenger_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_messenger_plugin_toggle_all_tracelevels) [MessageControl_DeviceIdentification_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_deviceidentification_plugin_toggle_all_tracelevels) [MessageControl_DeviceInfo_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_deviceinfo_plugin_toggle_all_tracelevels) [MessageControl_MessageControl_Plugin_Toggle_All_Tracelevels](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_messagecontrol_plugin_toggle_all_tracelevels) |
| `RDKSVC-REQ-006` | 1 | [MessageControl_ActivateDeactivate_Event_Test](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_Message_Control.md#messagecontrol_activatedeactivate_event_test) |
