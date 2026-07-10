# RDK Services — MaintenanceManager Plugin Requirements

> **Module:** MaintenanceManager (`org.rdk.MaintenanceManager.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_MaintenanceManager.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_MaintenanceManager.md)
> **Total requirements:** 6 | **Total test cases:** 29

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | Maintenance status and mode queries — getMaintenanceActivityStatus, getMaintenanceMode | Query API | 5 | MaintenanceManager_Get_MaintenanceActivity_Status, MaintenanceManager_Get_Maintenance_Mode, MaintenanceManager_Check_MaintenanceActivity_Status, MaintenanceManager_Check_Get_MaintenanceActivity_Status_Error, MaintenanceManager_Check_Get_Maintenance_StartTime_Error |
| RDKSVC-REQ-002 | Start and stop maintenance — startMaintenance, stopMaintenance | Control API | 3 | MaintenanceManager_Start_Stop_Maintenance, MaintenanceManager_Check_Start_Maintenance_Twice, MaintenanceManager_Check_Stop_Maintenance_Error |
| RDKSVC-REQ-003 | setMaintenanceMode — valid BACKGROUND and FOREGROUND modes with opt-out | Configuration API | 4 | MaintenanceManager_Background_OptOutModes_Test, MaintenanceManager_Foreground_OptOutModes_Test, MaintenanceManager_Set_MaintenanceMode_Parameter_Only, MaintenanceManager_Set_Optout_Parameter_Only |
| RDKSVC-REQ-004 | setMaintenanceMode — invalid and empty parameter inputs | Configuration API | 7 | MaintenanceManager_Set_MaintenanceMode_With_Invalid_Parameters, MaintenanceManager_Set_MaintenanceMode_With_Empty_Parameters, MaintenanceManager_Set_Invalid_Optout, MaintenanceManager_Set_Invalid_Maintenancemode, MaintenanceManager_Set_MaintenanceMode_Without_Parameters, MaintenanceManager_Set_Empty_Maintenancemode, MaintenanceManager_Set_Empty_Optoutmode |
| RDKSVC-REQ-005 | setMaintenanceMode — boundary combinations of mode and opt-out types | Configuration API | 8 | MaintenanceManager_Set_Foreground_MaintenanceMode_with_Invalid_OptOut, MaintenanceManager_Set_Background_MaintenanceMode_with_Empty_OptOut, MaintenanceManager_Set_Specialchars_MaintenanceMode_with_BYPASS_OPTOUT, MaintenanceManager_Set_Numeric_MaintenanceMode_with_None_OptOut, MaintenanceManager_Set_Foreground_MaintenanceMode_with_Numeric_OptOut, MaintenanceManager_Set_Specialchars_MaintenanceMode_with_ENFORCE_OPTOUT_OptOut, MaintenanceManager_Set_Specialchars_MaintenanceMode_with_None_OptOut, MaintenanceManager_Set_Foreground_MaintenanceMode_with_Specialchars_OptOut |
| RDKSVC-REQ-006 | Maintenance status change events and plugin lifecycle events | Event API | 2 | MaintenanceManager_Check_On_Maintenance_StatusChange_Event, MaintenanceManager_Activate_Deactivate_Event_Test |
| | **Total** | | **29** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the MaintenanceManager `getMaintenanceActivityStatus`, `getMaintenanceMode`, and `getMaintenanceStartTime` JSON-RPC methods to return current maintenance activity status and maintenance mode, and return correct error responses when the plugin is not in a state that permits these queries. |
| `RDKSVC-REQ-002` | SHALL implement the MaintenanceManager `startMaintenance` and `stopMaintenance` JSON-RPC methods to initiate and halt maintenance activity, return a correct error when `startMaintenance` is called while maintenance is already running, and return a correct error for `stopMaintenance` when no maintenance is active. |
| `RDKSVC-REQ-003` | SHALL implement the MaintenanceManager `setMaintenanceMode` JSON-RPC method to set BACKGROUND and FOREGROUND maintenance modes with opt-out modes, accept a request with only the maintenanceMode parameter, and accept a request with only the optout parameter. |
| `RDKSVC-REQ-004` | SHALL return correct error codes for `setMaintenanceMode` requests with invalid parameters, empty parameters, an invalid opt-out value, an invalid maintenance mode value, no parameters, an empty maintenance mode value, and an empty opt-out mode value. |
| `RDKSVC-REQ-005` | SHALL return correct error codes for `setMaintenanceMode` requests with boundary combinations — including FOREGROUND mode with invalid or numeric or special-character opt-out, BACKGROUND mode with empty opt-out, special-character mode with BYPASS_OPTOUT or ENFORCE_OPTOUT or NONE opt-out, and numeric mode with NONE opt-out. |
| `RDKSVC-REQ-006` | SHALL fire the `onMaintenanceStatusChange` event with correct maintenance status payload when maintenance activity status transitions, and fire the `statechange` event with correct plugin identifier and state payload during MaintenanceManager plugin activate and deactivate operations. |
