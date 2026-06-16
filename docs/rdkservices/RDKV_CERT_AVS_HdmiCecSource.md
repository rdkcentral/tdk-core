## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [HdmiCecSource_Verify_Get_Device_List (HdmiCecSource_01)](#hdmicecsource_verify_get_device_list-hdmicecsource_01)
   - [HdmiCecSource_Check_Empty_Device_List (HdmiCecSource_02)](#hdmicecsource_check_empty_device_list-hdmicecsource_02)
   - [HdmiCecSource_Enable_Disable_HdmiCec_Driver (HdmiCecSource_03)](#hdmicecsource_enable_disable_hdmicec_driver-hdmicecsource_03)
   - [HdmiCecSource_Verify_Get_OSD_Name (HdmiCecSource_04)](#hdmicecsource_verify_get_osd_name-hdmicecsource_04)
   - [HdmiCecSource_Enable_Disable_OTP_Option (HdmiCecSource_05)](#hdmicecsource_enable_disable_otp_option-hdmicecsource_05)
   - [HdmiCecSource_Verify_Get_Vendor_Id (HdmiCecSource_06)](#hdmicecsource_verify_get_vendor_id-hdmicecsource_06)
   - [HdmiCecSource_Verify_Send_Standby_Message (HdmiCecSource_07)](#hdmicecsource_verify_send_standby_message-hdmicecsource_07)
   - [HdmiCecSource_Verify_Send_Standby_Message_Error_When_HdmiCec_Driver_Not_Enabled (HdmiCecSource_08)](#hdmicecsource_verify_send_standby_message_error_when_hdmicec_driver_not_enabled-hdmicecsource_08)
   - [HdmiCecSource_Set_Enabled_No_Params (HdmiCecSource_09)](#hdmicecsource_set_enabled_no_params-hdmicecsource_09)
   - [HdmiCecSource_Set_OTP_Enabled_No_Params (HdmiCecSource_10)](#hdmicecsource_set_otp_enabled_no_params-hdmicecsource_10)
   - [HdmiCecSource_Verify_Set_Vendor_Id (HdmiCecSource_11)](#hdmicecsource_verify_set_vendor_id-hdmicecsource_11)
   - [HdmiCecSource_Verify_Perform_OTP_Action_Error_When_OTP_Action_Not_Enabled (HdmiCecSource_12)](#hdmicecsource_verify_perform_otp_action_error_when_otp_action_not_enabled-hdmicecsource_12)
   - [HdmiCecSource_Verify_SendKeyPressEvent_without_Params (HdmiCecSource_13)](#hdmicecsource_verify_sendkeypressevent_without_params-hdmicecsource_13)
   - [HdmiCecSource_Check_Empty_DeviceList_with_No-CEC-Devices_Connected (HdmiCecSource_14)](#hdmicecsource_check_empty_devicelist_with_no-cec-devices_connected-hdmicecsource_14)
   - [HdmiCecSource_Verify_Get_Active_Source_Status_False (HdmiCecSource_15)](#hdmicecsource_verify_get_active_source_status_false-hdmicecsource_15)
   - [HdmiCecSource_Verify_Get_Active_Source_Status_True (HdmiCecSource_16)](#hdmicecsource_verify_get_active_source_status_true-hdmicecsource_16)
   - [HdmiCecSource_Verify_OnDevice_InfoUpdated Event (HdmiCecSource_17)](#hdmicecsource_verify_ondevice_infoupdated-event-hdmicecsource_17)
   - [HdmiCecSource_Verify_Standby_MessageReceived_Event (HdmiCecSource_18)](#hdmicecsource_verify_standby_messagereceived_event-hdmicecsource_18)
   - [HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_StandbyCalled (HdmiCecSource_19)](#hdmicecsource_verify_on_activesource_statusupdated_event_when_standbycalled-hdmicecsource_19)
   - [HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_PerformOTPCalled (HdmiCecSource_20)](#hdmicecsource_verify_on_activesource_statusupdated_event_when_performotpcalled-hdmicecsource_20)
   - [HdmiCecSource_ActivateDeactivate_Event_Test (HdmiCecSource_21)](#hdmicecsource_activatedeactivate_event_test-hdmicecsource_21)
   - [HdmiCecSource_ActivateDeactivate_All_Event_Test (HdmiCecSource_22)](#hdmicecsource_activatedeactivate_all_event_test-hdmicecsource_22)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_same_OSD_name (HdmiCecSource_23)](#hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_same_osd_name-hdmicecsource_23)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_no_changes (HdmiCecSource_24)](#hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_no_changes-hdmicecsource_24)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_triggered (HdmiCecSource_25)](#hdmicecsource_verify_ondeviceinfoupdated_event_triggered-hdmicecsource_25)
   - [HdmiCecSource_Verify_Get_Vendor_ID_Error (HdmiCecSource_26)](#hdmicecsource_verify_get_vendor_id_error-hdmicecsource_26)
   - [HdmiCecSource_Verify_Get_OSD_Name_Error (HdmiCecSource_27)](#hdmicecsource_verify_get_osd_name_error-hdmicecsource_27)
   - [HdmiCecSource_Verify_Get_Device_List_Error (HdmiCecSource_28)](#hdmicecsource_verify_get_device_list_error-hdmicecsource_28)
   - [HdmiCecSource_Verify_Get_Enabled_Error (HdmiCecSource_29)](#hdmicecsource_verify_get_enabled_error-hdmicecsource_29)
   - [HdmiCecSource_Verify_Get_OTP_Enabled_Error (HdmiCecSource_30)](#hdmicecsource_verify_get_otp_enabled_error-hdmicecsource_30)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_LogicalAddress (HdmiCecSource_31)](#hdmicecsource_verify_send_key_press_event_invalid_logicaladdress-hdmicecsource_31)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Keycode (HdmiCecSource_32)](#hdmicecsource_verify_send_key_press_event_invalid_keycode-hdmicecsource_32)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Params (HdmiCecSource_33)](#hdmicecsource_verify_send_key_press_event_invalid_params-hdmicecsource_33)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_No_KeyCode (HdmiCecSource_34)](#hdmicecsource_verify_send_key_press_event_no_keycode-hdmicecsource_34)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Error_No_Logical_Address (HdmiCecSource_35)](#hdmicecsource_verify_send_key_press_event_error_no_logical_address-hdmicecsource_35)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_No_Param (HdmiCecSource_36)](#hdmicecsource_verify_send_key_press_event_no_param-hdmicecsource_36)
   - [Set_Invalid_OSD_Name (HdmiCecSource_37)](#set_invalid_osd_name-hdmicecsource_37)
   - [Set_Empty_VendorID (HdmiCecSource_38)](#set_empty_vendorid-hdmicecsource_38)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **HdmiCecSource** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.HdmiCecSource` (version 1)

**API Coverage**

- **State / Query APIs**: `getActiveSourceStatus`, `getDeviceList`, `getEnabled`, `getOSDName`, `getOTPEnabled`, `getVendorId`
- **Lifecycle / Control APIs**: `sendKeyPressEvent`, `sendStandbyMessage`
- **Configuration APIs**: `setEnabled`, `setOSDName`, `setOTPEnabled`, `setVendorId`
- **Events**: `onActiveSourceStatusUpdated`, `onDeviceInfoUpdated`, `standbyMessageReceived`
- **Other APIs**: `performOTPAction`

### APIs Under Test

| API | Description |
|-----|-------------|
| `getActiveSourceStatus` | Gets the active source status of the device |
| `getDeviceList` | Gets the list of CEC enabled devices connected and system information for each device. The information includes logicalAddress,OSD name and vendor ID |
| `getEnabled` | Returns if CEC is enabled |
| `getOSDName` | Gets the OSD name used by host device |
| `getOTPEnabled` | Returns HDMI-CEC OTP option enabled status |
| `getVendorId` | Gets the current vendor ID used by host device |
| `performOTPAction` | Turns on the TV and takes back the input to the device |
| `sendKeyPressEvent` | Sends the CEC User Control Pressed and User Control Release message when TV remote key is pressed |
| `sendStandbyMessage` | Sends a CEC Standby message to the logical address of the device |
| `setEnabled` | Enables or disables CEC |
| `setOSDName` | Sets the OSD name of the application |
| `setOTPEnabled` | Enables or disables HDMI-CEC OTP option |
| `setVendorId` | Sets the vendor ID of the application |

### Events Under Test

| Event | Description |
|-------|-------------|
| `onActiveSourceStatusUpdated` | Triggered when the device active source status changes |
| `onDeviceInfoUpdated` | Triggered when device system information is updated (vendorID, osdName) |
| `standbyMessageReceived` | Triggered when the source device changes status to STANDBY |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

- Register and listen to event `Event_On_Device_Info_Updated` on `HdmiCecSource` plugin

- Register and listen to event `Event_Standby_Message_Received` on `HdmiCecSource` plugin

- Register and listen to event `Event_On_Active_Source_Status_Updated` on `HdmiCecSource` plugin

---

## Test Cases

<a id="hdmicecsource_verify_get_device_list-hdmicecsource_01"></a>
### HdmiCecSource_Verify_Get_Device_List (HdmiCecSource_01)

**Objective:** Verify that the getDeviceList method returns a list of devices that support CEC

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check CEC Enabled Devices List | Invoke `getDeviceList` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Device List returned successfully |

---

<a id="hdmicecsource_check_empty_device_list-hdmicecsource_02"></a>
### HdmiCecSource_Check_Empty_Device_List (HdmiCecSource_02)

**Objective:** Verify that the getDeviceList method returns empty when the HDMI-CEC driver is disabled

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check CEC Enabled Devices List | Invoke `getDeviceList` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Device List should not return |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_Driver

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |

---

<a id="hdmicecsource_enable_disable_hdmicec_driver-hdmicecsource_03"></a>
### HdmiCecSource_Enable_Disable_HdmiCec_Driver (HdmiCecSource_03)

**Objective:** Enables and disables hdmicec driver

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Toggles the `enabled` value from Step 1, if Step 1 returned `true` sets `false`, if `false`, sets `true`)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `<toggled_value_from_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": <toggled_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<toggled_value_from_step_1>` |

**Post-condition:**

#### Post-condition 1: Revert_HdmiCec_Driver_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Enabled | Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 2 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |

---

<a id="hdmicecsource_verify_get_osd_name-hdmicecsource_04"></a>
### HdmiCecSource_Verify_Get_OSD_Name (HdmiCecSource_04)

**Objective:** Verify that the OSD (On-Screen Display) name can be set to a specified value and then retrieved correctly

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | OSD Name returned successfully |
| 2 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 3 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |

**Post-condition:**

#### Post-condition 1: Revert_OSD_Name

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `<original_value_from_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "<original_value_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name restored successfully |
| 2 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `<original_value_from_step_1>` |

---

<a id="hdmicecsource_enable_disable_otp_option-hdmicecsource_05"></a>
### HdmiCecSource_Enable_Disable_OTP_Option (HdmiCecSource_05)

**Objective:** Enables and Disables the HdmiCec OTP option

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Toggles the `enabled` value from Step 1: if Step 1 returned `true`, sets `false`; if `false`, sets `true`)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `<toggled_value_from_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": <toggled_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<toggled_value_from_step_1>` |

**Post-condition:**

#### Post-condition 1: Revert_OTP_Enabled_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OTP Enabled | Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `<original_value_from_step_1>`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": <original_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled restored successfully |
| 2 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<original_value_from_step_1>` |

---

<a id="hdmicecsource_verify_get_vendor_id-hdmicecsource_06"></a>
### HdmiCecSource_Verify_Get_Vendor_Id (HdmiCecSource_06)

**Objective:** Verify that the getVendorId method returns the correct vendor ID when called

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Vendor ID | Invoke `getVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Vendor Id returned successfully |

---

<a id="hdmicecsource_verify_send_standby_message-hdmicecsource_07"></a>
### HdmiCecSource_Verify_Send_Standby_Message (HdmiCecSource_07)

**Objective:** Verify if the sendStandbyMessage method sends a CEC standby message to the logical address of the device when the device is active

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Send Standby Message | Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`  |

---

<a id="hdmicecsource_verify_send_standby_message_error_when_hdmicec_driver_not_enabled-hdmicecsource_08"></a>
### HdmiCecSource_Verify_Send_Standby_Message_Error_When_HdmiCec_Driver_Not_Enabled (HdmiCecSource_08)

**Objective:** Verify if the sendstandbymessage method returns an error when the hdmicec driver is not enabled

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 8 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check Send Standby Message | Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_Driver

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Enabled set successfully |
| 3 | Get Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |

---

<a id="hdmicecsource_set_enabled_no_params-hdmicecsource_09"></a>
### HdmiCecSource_Set_Enabled_No_Params (HdmiCecSource_09)

**Objective:** Verify that the setEnabled method returns an error when the 'enabled' parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Set Enabled No Params | Invoke `setEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_set_otp_enabled_no_params-hdmicecsource_10"></a>
### HdmiCecSource_Set_OTP_Enabled_No_Params (HdmiCecSource_10)

**Objective:** Verify if the setOTPEnabled method returns an error when 'enabled' parameter is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Set OTP Enabled No Params | Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_set_vendor_id-hdmicecsource_11"></a>
### HdmiCecSource_Verify_Set_Vendor_Id (HdmiCecSource_11)

**Objective:** Verify if the setVendorId method successfully sets the vendor ID when a valid vendor ID is provided

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Vendor ID | Invoke `getVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Vendor Id returned successfully |
| 2 | Set Vendor ID | Invoke `setVendorId` on `org.rdk.HdmiCecSource` with `vendorid`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setVendorId", "params": {"vendorid": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Vendor Id set successfully |
| 3 | Get Vendor ID | Invoke `getVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` hdmicecsource get previous vendor id matches value from step 1 |

---

<a id="hdmicecsource_verify_perform_otp_action_error_when_otp_action_not_enabled-hdmicecsource_12"></a>
### HdmiCecSource_Verify_Perform_OTP_Action_Error_When_OTP_Action_Not_Enabled (HdmiCecSource_12)

**Objective:** Verify if the performOTPAction method returns an error when the OTP action is not enabled

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `false`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `disabled` state returned |
| 4 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |

---

<a id="hdmicecsource_verify_sendkeypressevent_without_params-hdmicecsource_13"></a>
### HdmiCecSource_Verify_SendKeyPressEvent_without_Params (HdmiCecSource_13)

**Objective:** Verify that the sendKeyPressEvent method returns an error when both the logical address and keycode are not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Without LogicalAddress and Keycode | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_check_empty_devicelist_with_no-cec-devices_connected-hdmicecsource_14"></a>
### HdmiCecSource_Check_Empty_DeviceList_with_No-CEC-Devices_Connected (HdmiCecSource_14)

**Objective:** Verify that the getDeviceList method returns an empty list when no CEC-enabled devices are connected

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check CEC Enabled Devices List | Invoke `getDeviceList` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Device List returned successfully |

---

<a id="hdmicecsource_verify_get_active_source_status_false-hdmicecsource_15"></a>
### HdmiCecSource_Verify_Get_Active_Source_Status_False (HdmiCecSource_15)

**Objective:** Verify that the getActiveSourceStatus method returns the correct active source status when the status is false

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Active Source Status returned successfully |
| 2 | Check Perform OTP Action | *(Conditional: executed only if previous step condition is met)*<br>Invoke `performOTPAction` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`  |
| 3 | Check Send Standby Message | Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |
| 4 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected `False` |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`  |

---

<a id="hdmicecsource_verify_get_active_source_status_true-hdmicecsource_16"></a>
### HdmiCecSource_Verify_Get_Active_Source_Status_True (HdmiCecSource_16)

**Objective:** Verify that the getActiveSourceStatus method returns the correct active source status when the status is true

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Active Source Status returned successfully |
| 2 | Check Send Standby Message | *(Conditional: executed only if previous step condition is met)*<br>Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |
| 3 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` |
| 4 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

---

<a id="hdmicecsource_verify_ondevice_infoupdated-event-hdmicecsource_17"></a>
### HdmiCecSource_Verify_OnDevice_InfoUpdated Event (HdmiCecSource_17)

**Objective:** Check if the ondeviceinfoupdated event was triggered when updating the OSD name

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | OSD Name returned successfully |
| 2 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 3 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Check Device Info Updated Event | Listen for `Event_On_Device_Info_Updated` event (timeout: 5s) | Event received and validated |

---

<a id="hdmicecsource_verify_standby_messagereceived_event-hdmicecsource_18"></a>
### HdmiCecSource_Verify_Standby_MessageReceived_Event (HdmiCecSource_18)

**Objective:** Check whether the standbymessagereceived event has been triggered

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Send Standby Message | Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |
| 2 | Check Standby MessageReceived Event | Listen for `Event_Standby_Message_Received` event (timeout: 5s) | Event received and validated |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` |

---

<a id="hdmicecsource_verify_on_activesource_statusupdated_event_when_standbycalled-hdmicecsource_19"></a>
### HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_StandbyCalled (HdmiCecSource_19)

**Objective:** Check whether the onActiveSourceStatusUpdated event has been triggered when the standby call is made

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Active Source Status returned successfully |
| 2 | Check Perform OTP Action | *(Conditional: executed only if previous step condition is met)*<br>Invoke `performOTPAction` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` |
| 3 | Check Send Standby Message | Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |
| 4 | Check On ActiveSource StatusUpdated Event | Listen for `Event_On_Active_Source_Status_Updated` event (timeout: 10s) | Event received and validated |

**Post-condition:**

#### Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `setOTPEnabled` on `org.rdk.HdmiCecSource` with `enabled`: `true`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | OTP Enabled set successfully |
| 3 | Get OTP Enabled | *(Conditional: executed only if previous step condition is met)*<br>Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 5 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`  |

---

<a id="hdmicecsource_verify_on_activesource_statusupdated_event_when_performotpcalled-hdmicecsource_20"></a>
### HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_PerformOTPCalled (HdmiCecSource_20)

**Objective:** Check whether the onActiveSourceStatusUpdated event has been triggered when the perform OTP call is made

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings` (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke `getActiveSourceStatus` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Active Source Status returned successfully |
| 2 | Check Send Standby Message | *(Conditional: executed only if previous step condition is met)*<br>Invoke `sendStandbyMessage` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Standby Message sent successfully |
| 3 | Check Perform OTP Action | Invoke `performOTPAction` on `org.rdk.HdmiCecSource` (wait 10 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `true`  |
| 4 | Check On ActiveSource StatusUpdated Event | Listen for `Event_On_Active_Source_Status_Updated` event (timeout: 10s) | Event received and validated |

---

<a id="hdmicecsource_activatedeactivate_event_test-hdmicecsource_21"></a>
### HdmiCecSource_ActivateDeactivate_Event_Test (HdmiCecSource_21)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_activatedeactivate_all_event_test-hdmicecsource_22"></a>
### HdmiCecSource_ActivateDeactivate_All_Event_Test (HdmiCecSource_22)

**Objective:** Validates all event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check All Event | Listen for `Event_Controller_All` event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_same_osd_name-hdmicecsource_23"></a>
### HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_same_OSD_name (HdmiCecSource_23)

**Objective:** Verify if the onDeviceInfoUpdated event is not triggered when the OSD name is set to the same value as before

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | OSD Name returned successfully |
| 2 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 3 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 5 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 6 | Check Device Info Updated Event | Listen for `Event_On_Device_Info_Updated` event (timeout: 5s) | Event should not occur |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_no_changes-hdmicecsource_24"></a>
### HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_no_changes (HdmiCecSource_24)

**Objective:** Verify if the onDeviceInfoUpdated event is not triggered when no changes are made to the vendor ID and OSD name

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | OSD Name returned successfully |
| 2 | Get Vendor ID | Invoke `getVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Vendor Id returned successfully |
| 3 | Check Device Info Updated Event | Listen for `Event_On_Device_Info_Updated` event (timeout: 5s) | Event should not occur |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_triggered-hdmicecsource_25"></a>
### HdmiCecSource_Verify_onDeviceInfoUpdated_event_triggered (HdmiCecSource_25)

**Objective:** Verify if the onDeviceInfoUpdated event is triggered when the OSD name is updated multiple times in quick succession

**Pre-condition:**

#### Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | OSD Name returned successfully |
| 2 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 3 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `"Television1"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television1"}}' http://127.0.0.1:9998/jsonrpc` | OSD Name set successfully |
| 5 | Get OSD Name | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television1` |
| 6 | Check Device Info Updated Event | Listen for `Event_On_Device_Info_Updated` event (timeout: 5s) | Event received and validated |

---

<a id="hdmicecsource_verify_get_vendor_id_error-hdmicecsource_26"></a>
### HdmiCecSource_Verify_Get_Vendor_ID_Error (HdmiCecSource_26)

**Objective:** Verify that the getVendorId method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Vendor ID API Response | Invoke `getVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_osd_name_error-hdmicecsource_27"></a>
### HdmiCecSource_Verify_Get_OSD_Name_Error (HdmiCecSource_27)

**Objective:** Verify that the getOSDName method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get OSD Name API Response | Invoke `getOSDName` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_device_list_error-hdmicecsource_28"></a>
### HdmiCecSource_Verify_Get_Device_List_Error (HdmiCecSource_28)

**Objective:** Verify that the getDeviceList method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Device List API Response | Invoke `getDeviceList` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_enabled_error-hdmicecsource_29"></a>
### HdmiCecSource_Verify_Get_Enabled_Error (HdmiCecSource_29)

**Objective:** Verify that the getEnabled method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Enabled API Response | Invoke `getEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_otp_enabled_error-hdmicecsource_30"></a>
### HdmiCecSource_Verify_Get_OTP_Enabled_Error (HdmiCecSource_30)

**Objective:** Verify that the getOTPEnabled method returns an error when the plugin is in a deactivated state

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | *(Conditional: executed only if plugin is currently deactivated)*<br>Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get OTP Enabled API Response | Invoke `getOTPEnabled` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdmiCecSource"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 6 | Check State Change Event | Listen for `Event_Controller_State_Changed` event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_logicaladdress-hdmicecsource_31"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_LogicalAddress (HdmiCecSource_31)

**Objective:** Verify if the sendKeyPressEvent method returns an error when an invalid logical address is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Address | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `"InvalidAddress"`, `keyCode`: `65`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "InvalidAddress", "keyCode": 65}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_keycode-hdmicecsource_32"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Keycode (HdmiCecSource_32)

**Objective:** Verify if the sendKeyPressEvent method returns an error when an invalid keycode is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Keycode | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `0`, `keyCode`: `"InvalidKeycode"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": 0, "keyCode": "InvalidKeycode"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_params-hdmicecsource_33"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Params (HdmiCecSource_33)

**Objective:** Verify if the sendKeyPressEvent method returns an error when both the logical address and keycode are invalid

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Params | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `"InvalidAddress"`, `keyCode`: `"InvalidKeycode"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "InvalidAddress", "keyCode": "InvalidKeycode"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_no_keycode-hdmicecsource_34"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_No_KeyCode (HdmiCecSource_34)

**Objective:** Verify if the sendKeyPressEvent method returns an error when the logical address is valid but the keycode is not provide

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No KeyCode | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `0`, `keyCode`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": 0, "keyCode": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_error_no_logical_address-hdmicecsource_35"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_Error_No_Logical_Address (HdmiCecSource_35)

**Objective:** Verify if the sendKeyPressEvent method returns an error when the keycode is valid but the logical address is not provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No Logical Address | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `""`, `keyCode`: `65`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "", "keyCode": 65}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_no_param-hdmicecsource_36"></a>
### HdmiCecSource_Verify_Send_Key_Press_Event_No_Param (HdmiCecSource_36)

**Objective:** Verify if the sendKeyPressEvent method returns an error when neither the logical address nor the keycode is provided

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No Params | Invoke `sendKeyPressEvent` on `org.rdk.HdmiCecSource` with `logicalAddress`: `""`, `keyCode`: `""`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "", "keyCode": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="set_invalid_osd_name-hdmicecsource_37"></a>
### Set_Invalid_OSD_Name (HdmiCecSource_37)

**Objective:** Validate by setting up invalid OSD Name

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OSD Name | Invoke `setOSDName` on `org.rdk.HdmiCecSource` with `name`: `123`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": 123}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="set_empty_vendorid-hdmicecsource_38"></a>
### Set_Empty_VendorID (HdmiCecSource_38)

**Objective:** Validate by setting up empty Vendor ID

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | HdmiCecSource Set Vendor ID | Invoke `setVendorId` on `org.rdk.HdmiCecSource`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setVendorId"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

---

## Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M129 |