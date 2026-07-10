# RDK Services — HdmiCecSource Plugin Requirements

> **Module:** HdmiCecSource (`org.rdk.HdmiCecSource.1`) | **Req ID Prefix:** `RDKSVC-REQ`
> **Source:** [RDKV_CERT_AVS_HdmiCecSource.md](https://github.com/rdkcentral/tdk-core/blob/main/docs/rdkservices/RDKV_CERT_AVS_HdmiCecSource.md)
> **Total requirements:** 10 | **Total test cases:** 38

---

## Step 1 — Requirement Categorisation Grouping

| Req ID | API Category | Classification | # Tests | Test Cases |
|--------|-------------|----------------|---------|------------|
| RDKSVC-REQ-001 | CEC device list — getDeviceList | Device Discovery API | 4 | HdmiCecSource_Verify_Get_Device_List, HdmiCecSource_Check_Empty_Device_List, HdmiCecSource_Check_Empty_DeviceList_with_No-CEC-Devices_Connected, HdmiCecSource_Verify_Get_Device_List_Error |
| RDKSVC-REQ-002 | CEC driver control — setEnabled, getEnabled | Driver Control API | 3 | HdmiCecSource_Enable_Disable_HdmiCec_Driver, HdmiCecSource_Set_Enabled_No_Params, HdmiCecSource_Verify_Get_Enabled_Error |
| RDKSVC-REQ-003 | OSD name — getOSDName, setOSDName | Device Identity API | 3 | HdmiCecSource_Verify_Get_OSD_Name, HdmiCecSource_Verify_Get_OSD_Name_Error, Set_Invalid_OSD_Name |
| RDKSVC-REQ-004 | One-Touch-Play — setOTPEnabled, performOTPAction | OTP API | 4 | HdmiCecSource_Enable_Disable_OTP_Option, HdmiCecSource_Set_OTP_Enabled_No_Params, HdmiCecSource_Verify_Perform_OTP_Action_Error_When_OTP_Action_Not_Enabled, HdmiCecSource_Verify_Get_OTP_Enabled_Error |
| RDKSVC-REQ-005 | Vendor ID — getVendorId, setVendorId | Device Identity API | 4 | HdmiCecSource_Verify_Get_Vendor_Id, HdmiCecSource_Verify_Set_Vendor_Id, HdmiCecSource_Verify_Get_Vendor_ID_Error, Set_Empty_VendorID |
| RDKSVC-REQ-006 | Standby message — sendStandbyMessage | CEC Messaging API | 2 | HdmiCecSource_Verify_Send_Standby_Message, HdmiCecSource_Verify_Send_Standby_Message_Error_When_HdmiCec_Driver_Not_Enabled |
| RDKSVC-REQ-007 | Active source status — getActiveSourceStatus | Source Status API | 2 | HdmiCecSource_Verify_Get_Active_Source_Status_False, HdmiCecSource_Verify_Get_Active_Source_Status_True |
| RDKSVC-REQ-008 | Key press events — sendKeyPressEvent | CEC Messaging API | 7 | HdmiCecSource_Verify_SendKeyPressEvent_without_Params, HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_LogicalAddress, HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Keycode, HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Params, HdmiCecSource_Verify_Send_Key_Press_Event_No_KeyCode, HdmiCecSource_Verify_Send_Key_Press_Event_Error_No_Logical_Address, HdmiCecSource_Verify_Send_Key_Press_Event_No_Param |
| RDKSVC-REQ-009 | Device info updated events — onDeviceInfoUpdated | Event API | 4 | HdmiCecSource_Verify_OnDevice_InfoUpdated Event, HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_same_OSD_name, HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_no_changes, HdmiCecSource_Verify_onDeviceInfoUpdated_event_triggered |
| RDKSVC-REQ-010 | CEC message events and plugin lifecycle events | Event API | 5 | HdmiCecSource_Verify_Standby_MessageReceived_Event, HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_StandbyCalled, HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_PerformOTPCalled, HdmiCecSource_ActivateDeactivate_Event_Test, HdmiCecSource_ActivateDeactivate_All_Event_Test |
| | **Total** | | **38** | |

---

## Deliverable 1 — Requirements Document

| Req ID | Test Scope *(Verify that the DUT...)* |
|--------|---------------------------------------|
| `RDKSVC-REQ-001` | SHALL implement the HdmiCecSource `getDeviceList` JSON-RPC method to return connected CEC devices, return an empty list when no devices are connected, handle a scenario with no CEC devices physically connected, and return a correct error response when the driver is disabled. |
| `RDKSVC-REQ-002` | SHALL implement the HdmiCecSource `setEnabled` and `getEnabled` JSON-RPC methods to enable and disable the HDMI CEC driver and report its state, return a correct error for `setEnabled` calls without required parameters, and return a correct error for `getEnabled` calls when the driver is not available. |
| `RDKSVC-REQ-003` | SHALL implement the HdmiCecSource `getOSDName` and `setOSDName` JSON-RPC methods to return the current OSD name, return a correct error when the driver is not enabled, and return a correct error for `setOSDName` calls with an invalid OSD name. |
| `RDKSVC-REQ-004` | SHALL implement the HdmiCecSource `setOTPEnabled` and `getOTPEnabled` JSON-RPC methods to enable and disable the OTP feature, return a correct error for `setOTPEnabled` calls without required parameters, return a correct error for `performOTPAction` when OTP is not enabled, and return a correct error for `getOTPEnabled` calls when the driver is unavailable. |
| `RDKSVC-REQ-005` | SHALL implement the HdmiCecSource `getVendorId` and `setVendorId` JSON-RPC methods to return and update the device vendor ID, return a correct error when the driver is not enabled, and return a correct error for `setVendorId` calls with an empty vendor ID. |
| `RDKSVC-REQ-006` | SHALL implement the HdmiCecSource `sendStandbyMessage` JSON-RPC method to broadcast a CEC standby message to connected devices, and return a correct error when the HDMI CEC driver is not enabled. |
| `RDKSVC-REQ-007` | SHALL implement the HdmiCecSource `getActiveSourceStatus` JSON-RPC method to correctly return `false` when the STB is not the active CEC source and `true` when it is the active source. |
| `RDKSVC-REQ-008` | SHALL implement the HdmiCecSource `sendKeyPressEvent` JSON-RPC method and return correct error codes for calls without parameters, with an invalid logical address, with an invalid key code, with invalid parameter combinations, without a key code, without a logical address, and without any parameter. |
| `RDKSVC-REQ-009` | SHALL fire the `onDeviceInfoUpdated` event when CEC device information changes, and correctly suppress the event when the OSD name is set to the same value and when no device information changes occur. |
| `RDKSVC-REQ-010` | SHALL fire the `standbyMessageReceived` event when a standby CEC message is received, fire the `onActiveSourceStatusUpdated` event when active source status changes after a standby or OTP action, and fire `statechange` and `all` events with correct payload during plugin activate and deactivate operations. |
