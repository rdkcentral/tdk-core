## TestScript Name
RDKV_CERT_AVS_HdmiCecSource

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [HdmiCecSource_Verify_Get_Device_List](#hdmicecsource_verify_get_device_list)
   - [HdmiCecSource_Check_Empty_Device_List](#hdmicecsource_check_empty_device_list)
   - [HdmiCecSource_Enable_Disable_HdmiCec_Driver](#hdmicecsource_enable_disable_hdmicec_driver)
   - [HdmiCecSource_Verify_Get_OSD_Name](#hdmicecsource_verify_get_osd_name)
   - [HdmiCecSource_Enable_Disable_OTP_Option](#hdmicecsource_enable_disable_otp_option)
   - [HdmiCecSource_Verify_Get_Vendor_Id](#hdmicecsource_verify_get_vendor_id)
   - [HdmiCecSource_Verify_Send_Standby_Message](#hdmicecsource_verify_send_standby_message)
   - [HdmiCecSource_Verify_Send_Standby_Message_Error_When_HdmiCec_Driver_Not_Enabled](#hdmicecsource_verify_send_standby_message_error_when_hdmicec_driver_not_enabled)
   - [HdmiCecSource_Set_Enabled_No_Params](#hdmicecsource_set_enabled_no_params)
   - [HdmiCecSource_Set_OTP_Enabled_No_Params](#hdmicecsource_set_otp_enabled_no_params)
   - [HdmiCecSource_Verify_Set_Vendor_Id](#hdmicecsource_verify_set_vendor_id)
   - [HdmiCecSource_Verify_Perform_OTP_Action_Error_When_OTP_Action_Not_Enabled](#hdmicecsource_verify_perform_otp_action_error_when_otp_action_not_enabled)
   - [HdmiCecSource_Verify_SendKeyPressEvent_without_Params](#hdmicecsource_verify_sendkeypressevent_without_params)
   - [HdmiCecSource_Check_Empty_DeviceList_with_No-CEC-Devices_Connected](#hdmicecsource_check_empty_devicelist_with_no-cec-devices_connected)
   - [HdmiCecSource_Verify_Get_Active_Source_Status_False](#hdmicecsource_verify_get_active_source_status_false)
   - [HdmiCecSource_Verify_Get_Active_Source_Status_True](#hdmicecsource_verify_get_active_source_status_true)
   - [HdmiCecSource_Verify_OnDevice_InfoUpdated Event](#hdmicecsource_verify_ondevice_infoupdated-event)
   - [HdmiCecSource_Verify_Standby_MessageReceived_Event](#hdmicecsource_verify_standby_messagereceived_event)
   - [HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_StandbyCalled](#hdmicecsource_verify_on_activesource_statusupdated_event_when_standbycalled)
   - [HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_PerformOTPCalled](#hdmicecsource_verify_on_activesource_statusupdated_event_when_performotpcalled)
   - [HdmiCecSource_ActivateDeactivate_Event_Test](#hdmicecsource_activatedeactivate_event_test)
   - [HdmiCecSource_ActivateDeactivate_All_Event_Test](#hdmicecsource_activatedeactivate_all_event_test)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_same_OSD_name](#hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_same_osd_name)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_no_changes](#hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_no_changes)
   - [HdmiCecSource_Verify_onDeviceInfoUpdated_event_triggered](#hdmicecsource_verify_ondeviceinfoupdated_event_triggered)
   - [HdmiCecSource_Verify_Get_Vendor_ID_Error](#hdmicecsource_verify_get_vendor_id_error)
   - [HdmiCecSource_Verify_Get_OSD_Name_Error](#hdmicecsource_verify_get_osd_name_error)
   - [HdmiCecSource_Verify_Get_Device_List_Error](#hdmicecsource_verify_get_device_list_error)
   - [HdmiCecSource_Verify_Get_Enabled_Error](#hdmicecsource_verify_get_enabled_error)
   - [HdmiCecSource_Verify_Get_OTP_Enabled_Error](#hdmicecsource_verify_get_otp_enabled_error)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_LogicalAddress](#hdmicecsource_verify_send_key_press_event_invalid_logicaladdress)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Keycode](#hdmicecsource_verify_send_key_press_event_invalid_keycode)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Params](#hdmicecsource_verify_send_key_press_event_invalid_params)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_No_KeyCode](#hdmicecsource_verify_send_key_press_event_no_keycode)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_Error_No_Logical_Address](#hdmicecsource_verify_send_key_press_event_error_no_logical_address)
   - [HdmiCecSource_Verify_Send_Key_Press_Event_No_Param](#hdmicecsource_verify_send_key_press_event_no_param)
   - [Set_Invalid_OSD_Name](#set_invalid_osd_name)
   - [Set_Empty_VendorID](#set_empty_vendorid)
4. [Plugin Post-conditions](#plugin-post-conditions)
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

## APIs Under Test

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

## Events Under Test

| Event | Description |
|-------|-------------|
| `onActiveSourceStatusUpdated` | Triggered when the device active source status changes |
| `onDeviceInfoUpdated` | Triggered when device system information is updated (vendorID, osdName) |
| `standbyMessageReceived` | Triggered when the source device changes status to STANDBY |

---

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Plugin Pre-condition 3: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

- Register and listen to event `Event_Controller_All` on `Controller` plugin

- Register and listen to event `Event_On_Device_Info_Updated` on `HdmiCecSource` plugin

- Register and listen to event `Event_Standby_Message_Received` on `HdmiCecSource` plugin

- Register and listen to event `Event_On_Active_Source_Status_Updated` on `HdmiCecSource` plugin

---

## Test Cases

<a id="hdmicecsource_verify_get_device_list"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Device_List

### TestCase ID
HdmiCecSource_01

### TestCase Objective
Verify that the getDeviceList method returns a list of devices that support CEC

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check CEC Enabled Devices List | Invoke getDeviceList on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Verify that the device list is returned successfully |

---

<a id="hdmicecsource_check_empty_device_list"></a>
### TestCase Name
HdmiCecSource_Check_Empty_Device_List

### TestCase ID
HdmiCecSource_02

### TestCase Objective
Verify that the getDeviceList method returns empty when the HDMI-CEC driver is disabled

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check CEC Enabled Devices List | Invoke getDeviceList on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Device List should not return |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_Driver

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Get Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |

---

<a id="hdmicecsource_enable_disable_hdmicec_driver"></a>
### TestCase Name
HdmiCecSource_Enable_Disable_HdmiCec_Driver

### TestCase ID
HdmiCecSource_03

### TestCase Objective
Enables and disables hdmicec driver

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Toggles the enabled value from Step 1, if Step 1 returned true sets false, if false, sets true)*<br>Invoke setEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": <toggled_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<toggled_value_from_step_1>` |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_HdmiCec_Driver_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set Enabled | Set Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 2 | Get Enabled | Get Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `true` |

---

<a id="hdmicecsource_verify_get_osd_name"></a>
### TestCase Name
HdmiCecSource_Verify_Get_OSD_Name

### TestCase ID
HdmiCecSource_04

### TestCase Objective
Verify that the OSD (On-Screen Display) name can be set to a specified value and then retrieved correctly

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the OSD name is returned successfully |
| 2 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 3 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_OSD_Name

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OSD Name | Set OSD Name on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "<original_value_from_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is restored successfully |
| 2 | Get OSD Name | Get OSD Name from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `<original_value_from_step_1>` |

---

<a id="hdmicecsource_enable_disable_otp_option"></a>
### TestCase Name
HdmiCecSource_Enable_Disable_OTP_Option

### TestCase ID
HdmiCecSource_05

### TestCase Objective
Enables and Disables the HdmiCec OTP option

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke getOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Toggles the enabled value from Step 1: if Step 1 returned true, sets false; if false, sets true)*<br>Invoke setOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": <toggled_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | Invoke getOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<toggled_value_from_step_1>` |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_OTP_Enabled_State

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OTP Enabled | Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": <original_value_from_step_1>}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is restored successfully |
| 2 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | Expected `<original_value_from_step_1>` |

---

<a id="hdmicecsource_verify_get_vendor_id"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Vendor_Id

### TestCase ID
HdmiCecSource_06

### TestCase Objective
Verify that the getVendorId method returns the correct vendor ID when called

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Vendor ID | Invoke getVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Verify that the vendor ID is returned successfully |

---

<a id="hdmicecsource_verify_send_standby_message"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Standby_Message

### TestCase ID
HdmiCecSource_07

### TestCase Objective
Verify if the sendStandbyMessage method sends a CEC standby message to the logical address of the device when the device is active

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Send Standby Message | Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Perform OTP Action on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`  |

---

<a id="hdmicecsource_verify_send_standby_message_error_when_hdmicec_driver_not_enabled"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Standby_Message_Error_When_HdmiCec_Driver_Not_Enabled

### TestCase ID
HdmiCecSource_08

### TestCase Objective
Verify if the sendstandbymessage method returns an error when the hdmicec driver is not enabled

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check Send Standby Message | Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_Driver

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Enabled | Get Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the enabled state is set successfully |
| 3 | Get Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |

---

<a id="hdmicecsource_set_enabled_no_params"></a>
### TestCase Name
HdmiCecSource_Set_Enabled_No_Params

### TestCase ID
HdmiCecSource_09

### TestCase Objective
Verify that the setEnabled method returns an error when the 'enabled' parameter is not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Set Enabled No Params | Invoke setEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_set_otp_enabled_no_params"></a>
### TestCase Name
HdmiCecSource_Set_OTP_Enabled_No_Params

### TestCase ID
HdmiCecSource_10

### TestCase Objective
Verify if the setOTPEnabled method returns an error when 'enabled' parameter is not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Set OTP Enabled No Params | Invoke setOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_set_vendor_id"></a>
### TestCase Name
HdmiCecSource_Verify_Set_Vendor_Id

### TestCase ID
HdmiCecSource_11

### TestCase Objective
Verify if the setVendorId method successfully sets the vendor ID when a valid vendor ID is provided

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Vendor ID | Invoke getVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Verify that the vendor ID is returned successfully |
| 2 | Set Vendor ID | Invoke setVendorId on org.rdk.HdmiCecSource with vendorid: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setVendorId", "params": {"vendorid": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the vendor ID is set successfully |
| 3 | Get Vendor ID | Invoke getVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` hdmicecsource get previous vendor id matches value from step 1 |

---

<a id="hdmicecsource_verify_perform_otp_action_error_when_otp_action_not_enabled"></a>
### TestCase Name
HdmiCecSource_Verify_Perform_OTP_Action_Error_When_OTP_Action_Not_Enabled

### TestCase ID
HdmiCecSource_12

### TestCase Objective
Verify if the performOTPAction method returns an error when the OTP action is not enabled

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Invoke getOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `disabled` state returned |
| 4 | Check Perform OTP Action | Invoke performOTPAction on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |

---

<a id="hdmicecsource_verify_sendkeypressevent_without_params"></a>
### TestCase Name
HdmiCecSource_Verify_SendKeyPressEvent_without_Params

### TestCase ID
HdmiCecSource_13

### TestCase Objective
Verify that the sendKeyPressEvent method returns an error when both the logical address and keycode are not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Without LogicalAddress and Keycode | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent"}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_check_empty_devicelist_with_no-cec-devices_connected"></a>
### TestCase Name
HdmiCecSource_Check_Empty_DeviceList_with_No-CEC-Devices_Connected

### TestCase ID
HdmiCecSource_14

### TestCase Objective
Verify that the getDeviceList method returns an empty list when no CEC-enabled devices are connected

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check CEC Enabled Devices List | Invoke getDeviceList on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | Verify that the device list is returned successfully |

---

<a id="hdmicecsource_verify_get_active_source_status_false"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Active_Source_Status_False

### TestCase ID
HdmiCecSource_15

### TestCase Objective
Verify that the getActiveSourceStatus method returns the correct active source status when the status is false

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the active source status is returned successfully |
| 2 | Check Perform OTP Action | *(Conditional statement executed only if previous step condition is met)*<br>Invoke performOTPAction on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`  |
| 3 | Check Send Standby Message | Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |
| 4 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected `False` |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Perform OTP Action on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`  |

---

<a id="hdmicecsource_verify_get_active_source_status_true"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Active_Source_Status_True

### TestCase ID
HdmiCecSource_16

### TestCase Objective
Verify that the getActiveSourceStatus method returns the correct active source status when the status is true

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the active source status is returned successfully |
| 2 | Check Send Standby Message | *(Conditional statement executed only if previous step condition is met)*<br>Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |
| 3 | Check Perform OTP Action | Invoke performOTPAction on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` |
| 4 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Expected `True` |

---

<a id="hdmicecsource_verify_ondevice_infoupdated-event"></a>
### TestCase Name
HdmiCecSource_Verify_OnDevice_InfoUpdated Event

### TestCase ID
HdmiCecSource_17

### TestCase Objective
Check if the ondeviceinfoupdated event was triggered when updating the OSD name

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the OSD name is returned successfully |
| 2 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 3 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Check Device Info Updated Event | Listen for Event_On_Device_Info_Updated event (timeout: 5s) | Verify that the event is received and validated |

---

<a id="hdmicecsource_verify_standby_messagereceived_event"></a>
### TestCase Name
HdmiCecSource_Verify_Standby_MessageReceived_Event

### TestCase ID
HdmiCecSource_18

### TestCase Objective
Check whether the standbymessagereceived event has been triggered

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Send Standby Message | Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |
| 2 | Check Standby MessageReceived Event | Listen for Event_Standby_Message_Received event (timeout: 5s) | Verify that the event is received and validated |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Perform OTP Action on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` |

---

<a id="hdmicecsource_verify_on_activesource_statusupdated_event_when_standbycalled"></a>
### TestCase Name
HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_StandbyCalled

### TestCase ID
HdmiCecSource_19

### TestCase Objective
Check whether the onActiveSourceStatusUpdated event has been triggered when the standby call is made

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the active source status is returned successfully |
| 2 | Check Perform OTP Action | *(Conditional statement executed only if previous step condition is met)*<br>Invoke performOTPAction on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` |
| 3 | Check Send Standby Message | Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |
| 4 | Check On ActiveSource StatusUpdated Event | Listen for Event_On_Active_Source_Status_Updated event (timeout: 10s) | Verify that the event is received and validated |

### TestCase Post-condition

#### TestCase Post-condition 1: Enabling_HdmiCec_OTP

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OTP Enabled | Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 2 | Set OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Set OTP Enabled on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOTPEnabled", "params": {"enabled": true}}' http://127.0.0.1:9998/jsonrpc` | Confirm that OTP enabled state is set successfully |
| 3 | Get OTP Enabled | *(Conditional statement executed only if previous step condition is met)*<br>Get OTP Enabled from HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true` `enabled` state returned |
| 4 | Check Perform OTP Action | Perform OTP Action on HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`  |

---

<a id="hdmicecsource_verify_on_activesource_statusupdated_event_when_performotpcalled"></a>
### TestCase Name
HdmiCecSource_Verify_On_ActiveSource_StatusUpdated_Event_when_PerformOTPCalled

### TestCase ID
HdmiCecSource_20

### TestCase Objective
Check whether the onActiveSourceStatusUpdated event has been triggered when the perform OTP call is made

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Active Source Status | Invoke getActiveSourceStatus on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getActiveSourceStatus"}' http://127.0.0.1:9998/jsonrpc` | Verify that the active source status is returned successfully |
| 2 | Check Send Standby Message | *(Conditional statement executed only if previous step condition is met)*<br>Invoke sendStandbyMessage on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendStandbyMessage"}' http://127.0.0.1:9998/jsonrpc` | Confirm that the standby message is sent successfully |
| 3 | Check Perform OTP Action | Invoke performOTPAction on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.performOTPAction"}' http://127.0.0.1:9998/jsonrpc` | `success` : `true`  |
| 4 | Check On ActiveSource StatusUpdated Event | Listen for Event_On_Active_Source_Status_Updated event (timeout: 10s) | Verify that the event is received and validated |

---

<a id="hdmicecsource_activatedeactivate_event_test"></a>
### TestCase Name
HdmiCecSource_ActivateDeactivate_Event_Test

### TestCase ID
HdmiCecSource_21

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_activatedeactivate_all_event_test"></a>
### TestCase Name
HdmiCecSource_ActivateDeactivate_All_Event_Test

### TestCase ID
HdmiCecSource_22

### TestCase Objective
Validates all event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check All Event | Listen for Event_Controller_All event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check All Event | Listen for Event_Controller_All event (timeout: 2s) | Controller `all` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_same_osd_name"></a>
### TestCase Name
HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_same_OSD_name

### TestCase ID
HdmiCecSource_23

### TestCase Objective
Verify if the onDeviceInfoUpdated event is not triggered when the OSD name is set to the same value as before

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the OSD name is returned successfully |
| 2 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 3 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 5 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 6 | Check Device Info Updated Event | Listen for Event_On_Device_Info_Updated event (timeout: 5s) | Event should not occur |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_not_triggered_no_changes"></a>
### TestCase Name
HdmiCecSource_Verify_onDeviceInfoUpdated_event_not_triggered_no_changes

### TestCase ID
HdmiCecSource_24

### TestCase Objective
Verify if the onDeviceInfoUpdated event is not triggered when no changes are made to the vendor ID and OSD name

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the OSD name is returned successfully |
| 2 | Get Vendor ID | Invoke getVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | Verify that the vendor ID is returned successfully |
| 3 | Check Device Info Updated Event | Listen for Event_On_Device_Info_Updated event (timeout: 5s) | Event should not occur |

---

<a id="hdmicecsource_verify_ondeviceinfoupdated_event_triggered"></a>
### TestCase Name
HdmiCecSource_Verify_onDeviceInfoUpdated_event_triggered

### TestCase ID
HdmiCecSource_25

### TestCase Objective
Verify if the onDeviceInfoUpdated event is triggered when the OSD name is updated multiple times in quick succession

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Verify that the OSD name is returned successfully |
| 2 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 3 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television` |
| 4 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource with name: "Television1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": "Television1"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the OSD name is set successfully |
| 5 | Get OSD Name | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | Expected `Television1` |
| 6 | Check Device Info Updated Event | Listen for Event_On_Device_Info_Updated event (timeout: 5s) | Verify that the event is received and validated |

---

<a id="hdmicecsource_verify_get_vendor_id_error"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Vendor_ID_Error

### TestCase ID
HdmiCecSource_26

### TestCase Objective
Verify that the getVendorId method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Vendor ID API Response | Invoke getVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getVendorId"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_osd_name_error"></a>
### TestCase Name
HdmiCecSource_Verify_Get_OSD_Name_Error

### TestCase ID
HdmiCecSource_27

### TestCase Objective
Verify that the getOSDName method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get OSD Name API Response | Invoke getOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOSDName"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_device_list_error"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Device_List_Error

### TestCase ID
HdmiCecSource_28

### TestCase Objective
Verify that the getDeviceList method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Device List API Response | Invoke getDeviceList on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getDeviceList"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_enabled_error"></a>
### TestCase Name
HdmiCecSource_Verify_Get_Enabled_Error

### TestCase ID
HdmiCecSource_29

### TestCase Objective
Verify that the getEnabled method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get Enabled API Response | Invoke getEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getEnabled"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_get_otp_enabled_error"></a>
### TestCase Name
HdmiCecSource_Verify_Get_OTP_Enabled_Error

### TestCase ID
HdmiCecSource_30

### TestCase Objective
Verify that the getOTPEnabled method returns an error when the plugin is in a deactivated state

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is currently deactivated)*<br>Check Active Status of HdmiCecSource Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate HdmiCecSource Plugin | Invoke deactivate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Check HdmiCecSource Get OTP Enabled API Response | Invoke getOTPEnabled on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.getOTPEnabled"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `Service is not active` / `ERROR_UNAVAILABLE` / `The service is in an illegal state!!!.` |
| 5 | Activate HdmiCecSource Plugin | Invoke activate on Controller with callsign: "org.rdk.HdmiCecSource"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdmiCecSource"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 6 | Check State Change Event | Listen for Event_Controller_State_Changed event (timeout: 2s) | `statechange` event received; callsign = `org.rdk.hdmicecsource`, state = `"activated"` |
| 7 | Check PluginActive Status | Invoke status on Controller for org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdmiCecSource"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_logicaladdress"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_LogicalAddress

### TestCase ID
HdmiCecSource_31

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when an invalid logical address is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Address | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with logicalAddress: "InvalidAddress"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "InvalidAddress", "keyCode": 65}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_keycode"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Keycode

### TestCase ID
HdmiCecSource_32

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when an invalid keycode is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Keycode | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with keyCode: "InvalidKeycode"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": 0, "keyCode": "InvalidKeycode"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_invalid_params"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_Invalid_Params

### TestCase ID
HdmiCecSource_33

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when both the logical address and keycode are invalid

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event Invalid Params | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with logicalAddress: "InvalidAddress", keyCode: "InvalidKeycode"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "InvalidAddress", "keyCode": "InvalidKeycode"}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_no_keycode"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_No_KeyCode

### TestCase ID
HdmiCecSource_34

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when the logical address is valid but the keycode is not provide

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No KeyCode | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with keyCode: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": 0, "keyCode": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_error_no_logical_address"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_Error_No_Logical_Address

### TestCase ID
HdmiCecSource_35

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when the keycode is valid but the logical address is not provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No Logical Address | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with logicalAddress: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "", "keyCode": 65}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="hdmicecsource_verify_send_key_press_event_no_param"></a>
### TestCase Name
HdmiCecSource_Verify_Send_Key_Press_Event_No_Param

### TestCase ID
HdmiCecSource_36

### TestCase Objective
Verify if the sendKeyPressEvent method returns an error when neither the logical address nor the keycode is provided

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Send Key Press Event No Params | Invoke sendKeyPressEvent on org.rdk.HdmiCecSource with logicalAddress: "", keyCode: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.sendKeyPressEvent", "params": {"logicalAddress": "", "keyCode": ""}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="set_invalid_osd_name"></a>
### TestCase Name
Set_Invalid_OSD_Name

### TestCase ID
HdmiCecSource_37

### TestCase Objective
Validate by setting up invalid OSD Name

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Set OSD Name | Invoke setOSDName on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setOSDName", "params": {"name": 123}}' http://127.0.0.1:9998/jsonrpc` | `success`: `false` (expected error response) |

---

<a id="set_empty_vendorid"></a>
### TestCase Name
Set_Empty_VendorID

### TestCase ID
HdmiCecSource_38

### TestCase Objective
Validate by setting up empty Vendor ID

### Test Steps

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | HdmiCecSource Set Vendor ID | Invoke setVendorId on org.rdk.HdmiCecSource<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdmiCecSource.1.setVendorId"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

---

## Plugin Post-conditions

_No plugin-level post-conditions defined_

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 15 minutes |
| Priority | Medium |
| TDK Release Version | M129 |