## TestScript Name
RDKV_CERT_AVS_Device_Info

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [DeviceInfo_Get_All_System_Info](#deviceinfo_get_all_system_info)
   - [DeviceInfo_Get_All_Network_Interfaces](#deviceinfo_get_all_network_interfaces)
   - [DeviceInfo_Get_SocketInfo_Negative_Case](#deviceinfo_get_socketinfo_negative_case)
   - [DeviceInfo_ActivateDeactivate_STRESS](#deviceinfo_activatedeactivate_stress)
   - [DeviceInfo_Get_Serial_Number](#deviceinfo_get_serial_number)
   - [DeviceInfo_Check_Model_Name](#deviceinfo_check_model_name)
   - [DeviceInfo_Check_Firmware_Version](#deviceinfo_check_firmware_version)
   - [DeviceInfo_Check_Supported_Audio_Ports](#deviceinfo_check_supported_audio_ports)
   - [DeviceInfo_Check_Supported_Video_Displays](#deviceinfo_check_supported_video_displays)
   - [DeviceInfo_Check_Host_EDID](#deviceinfo_check_host_edid)
   - [DeviceInfo_Check_Default_Resolution](#deviceinfo_check_default_resolution)
   - [DeviceInfo_Check_Supported_HDCP_Version](#deviceinfo_check_supported_hdcp_version)
   - [DeviceInfo_Check_Model_ID](#deviceinfo_check_model_id)
   - [DeviceInfo_Check_Device_Type](#deviceinfo_check_device_type)
   - [DeviceInfo_ActivateDeactivate_Event_Test](#deviceinfo_activatedeactivate_event_test)
   - [DeviceInfo_Validate_Firmware_Version](#deviceinfo_validate_firmware_version)
   - [DeviceInfo_Validate_Serial_Number](#deviceinfo_validate_serial_number)
   - [DeviceInfo_Validate_Supported_Audio_Ports](#deviceinfo_validate_supported_audio_ports)
   - [DeviceInfo_Validate_Supported_Video_Ports](#deviceinfo_validate_supported_video_ports)
   - [DeviceInfo_Validate_Host_EDID](#deviceinfo_validate_host_edid)
   - [DeviceInfo_Validate_HDCP_Version](#deviceinfo_validate_hdcp_version)
   - [DeviceInfo_Validate_Default_Resolution](#deviceinfo_validate_default_resolution)
   - [DeviceInfo_Check_SystemInfo_API_Date_Matches_DUT_Date](#deviceinfo_check_systeminfo_api_date_matches_dut_date)
   - [DeviceInfo_Get_Device_SocName](#deviceinfo_get_device_socname)
   - [DeviceInfo_Get_Device_Manufacturer](#deviceinfo_get_device_manufacturer)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **DeviceInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `DeviceInfo` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Activate_System_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 4: Activate_HdcpProfile_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of HdcpProfile Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 5: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 6: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure ESN Support | `DEVICEINFO_ESN_SUPPORT` must be set to 'yes' if ESN support is available on the DUT, otherwise 'no' | The `DEVICEINFO_ESN_SUPPORT` value should be correctly configured in the device-specific config file |
| 2 | Configure Supported HDCP Version | `DEVICEINFO_SUPPORTED_HDCP_VERSION` must be set to the HDCP version supported by the DUT | The `DEVICEINFO_SUPPORTED_HDCP_VERSION` value should be correctly configured in the device-specific config file |
| 3 | Configure Device Details File Path | `DEVICEINFO_DEVICE_DETAILS_FILE_PATH` must be set to the path to the device properties file on the DUT | The `DEVICEINFO_DEVICE_DETAILS_FILE_PATH` value should be correctly configured in the device-specific config file |
| 4 | Configure Device Type | `DEVICEINFO_DEVICE_TYPE` must be set to the type of the DUT | The `DEVICEINFO_DEVICE_TYPE` value should be correctly configured in the device-specific config file |
| 5 | Configure NA Tests | `DEVICEINFO_NA_TESTS` must be set to the DeviceInfo test names to skip when not applicable on the DUT | The `DEVICEINFO_NA_TESTS` value should be correctly configured in the device-specific config file |
## Test Cases

<a id="deviceinfo_get_all_system_info"></a>
### TestCase Name
DeviceInfo_Get_All_System_Info

### TestCase ID
DI_01

### TestCase Objective
Gets all system information

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get System Info | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that system information is returned successfully |

---

<a id="deviceinfo_get_all_network_interfaces"></a>
### TestCase Name
DeviceInfo_Get_All_Network_Interfaces

### TestCase ID
DI_02

### TestCase Objective
Gets all network interfaces

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Network Interfaces | Invoke addresses on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.addresses"}' http://127.0.0.1:9998/jsonrpc` | Verify that the DeviceInfo network information is returned and validated successfully  |

---

<a id="deviceinfo_get_socketinfo_negative_case"></a>
### TestCase Name
DeviceInfo_Get_SocketInfo_Negative_Case

### TestCase ID
DI_03

### TestCase Objective
Checks the negative scenario for Socket info API

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Socket Info | Invoke socketinfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.socketinfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Unknown method.` |

---

<a id="deviceinfo_activatedeactivate_stress"></a>
### TestCase Name
DeviceInfo_ActivateDeactivate_STRESS

### TestCase ID
DI_04

### TestCase Objective
Activates and deactivates the plugin

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check DeviceInfo Active Status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Deactivate DeviceInfo Plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 3 | Activate DeviceInfo Plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 4 | Get CPU Load | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the CPU load is retrieved and validated successfully |

---

<a id="deviceinfo_get_serial_number"></a>
### TestCase Name
DeviceInfo_Get_Serial_Number

### TestCase ID
DI_05

### TestCase Objective
Checks the serial number

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Serial Number | Invoke serialnumber on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.serialnumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the DeviceInfo API response is returned and validated successfully  |

---

<a id="deviceinfo_check_model_name"></a>
### TestCase Name
DeviceInfo_Check_Model_Name

### TestCase ID
DI_06

### TestCase Objective
Checks the model name of the DUT

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Details | Read expected model name by executing: grep FRIENDLY_ID <DEVICEINFO_DEVICE_DETAILS_FILE_PATH> \| cut -d'=' -f2- \| xargs | Verify that the `FRIENDLY_ID` value is retrieved successfully and saved for comparison  |
| 2 | Get Model Name | Invoke modelname on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.modelname"}' http://127.0.0.1:9998/jsonrpc` | Verify that the model name returned by the API matches the `FRIENDLY_ID` value retrieved in step 1  |

---

<a id="deviceinfo_check_firmware_version"></a>
### TestCase Name
DeviceInfo_Check_Firmware_Version

### TestCase ID
DI_07

### TestCase Objective
Checks the firmware version of the DUT

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Current Image Version | Retrieve current firmware image version from device | Verify that the current firmware image version is retrieved from the device successfully |
| 2 | Get Firmware Version | Invoke firmwareversion on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.firmwareversion"}' http://127.0.0.1:9998/jsonrpc` | Verify that the firmware version matches the expected value retrieved from the device  |

---

<a id="deviceinfo_check_supported_audio_ports"></a>
### TestCase Name
DeviceInfo_Check_Supported_Audio_Ports

### TestCase ID
DI_08

### TestCase Objective
Check whether settop lists supported audio ports

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported Audio Ports | Invoke supportedaudioports on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedaudioports"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio ports match the expected value `<SUPPORTED_AUDIO_PORTS>` from the device config file  |

---

<a id="deviceinfo_check_supported_video_displays"></a>
### TestCase Name
DeviceInfo_Check_Supported_Video_Displays

### TestCase ID
DI_09

### TestCase Objective
Check whether settop displays supported video displays

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported Video Displays | Invoke supportedvideodisplays on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedvideodisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported video displays match the expected value `<SUPPORTED_VIDEO_DISPLAYS>` from the device config file  |

---

<a id="deviceinfo_check_host_edid"></a>
### TestCase Name
DeviceInfo_Check_Host_EDID

### TestCase ID
DI_10

### TestCase Objective
Check the EDID status of host

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Host EDID Details | Invoke hostedid on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.hostedid"}' http://127.0.0.1:9998/jsonrpc` | Verify that the information retrieved from the hostedid API is not empty  |

---

<a id="deviceinfo_check_default_resolution"></a>
### TestCase Name
DeviceInfo_Check_Default_Resolution

### TestCase ID
DI_11

### TestCase Objective
Check whether the default resolution is available in supported resolutions

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get Supported Resolutions | Invoke supportedresolutions on DeviceInfo with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedresolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the information retrieved from the supportedresolutions API is not empty  |
| 3 | Get Default Resolution | Invoke defaultresolution on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.defaultresolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that the returned value matches the value captured in step 2  |

---

<a id="deviceinfo_check_supported_hdcp_version"></a>
### TestCase Name
DeviceInfo_Check_Supported_HDCP_Version

### TestCase ID
DI_12

### TestCase Objective
Checks the supported HDCP version

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get Supported HDCP | Invoke supportedhdcp on DeviceInfo with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedhdcp", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the HDCP version matches the expected value from the device configuration  |

---

<a id="deviceinfo_check_model_id"></a>
### TestCase Name
DeviceInfo_Check_Model_ID

### TestCase ID
DI_13

### TestCase Objective
Checks the model id of the DUT

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Details | Read expected model id by executing grep ^MODEL_NUM <DEVICEINFO_DEVICE_DETAILS_FILE_PATH> \| cut -d'=' -f2- \| xargs | Verify that the `MODEL_NUM` value is retrieved successfully and saved for comparison |
| 2 | Get Model ID | Invoke modelid on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.modelid"}' http://127.0.0.1:9998/jsonrpc` | Verify that the API response matches the expected value from step 1 |

---

<a id="deviceinfo_check_device_type"></a>
### TestCase Name
DeviceInfo_Check_Device_Type

### TestCase ID
DI_14

### TestCase Objective
Checks the device type of the DUT

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Type | Invoke devicetype on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.devicetype"}' http://127.0.0.1:9998/jsonrpc` | Verify that the device type returned by the API matches the expected value `<DEVICEINFO_DEVICE_TYPE>` from the device config file  |

---

<a id="deviceinfo_activatedeactivate_event_test"></a>
### TestCase Name
DeviceInfo_ActivateDeactivate_Event_Test

### TestCase ID
DI_15

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DeviceInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DeviceInfo Plugin | Invoke deactivate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 3 | Check PluginActive Status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DeviceInfo Plugin | Invoke activate on Controller with callsign: "DeviceInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 6 | Check PluginActive Status | Invoke status on Controller for DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="deviceinfo_validate_firmware_version"></a>
### TestCase Name
DeviceInfo_Validate_Firmware_Version

### TestCase ID
DI_16

### TestCase Objective
Verify whether the firmware version returned by deviceinfo API matches the firmware version in system or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeviceInfo Get Firmware Version | Invoke firmwareversion on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.firmwareversion"}' http://127.0.0.1:9998/jsonrpc` | Verify that the firmware version is retrieved successfully from DeviceInfo API |
| 2 | System Get Device Image Version | Invoke getDeviceInfo on org.rdk.System with params: "imageVersion"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "imageVersion"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the image version is retrieved successfully from System API |
| 3 | Comparison of Two API Results | Compare firmware version from step 1 (DeviceInfo API) against image version from step 2 (System API) | Verify that the firmware version returned by `DeviceInfo.firmwareversion` matches the image version returned by `System.getDeviceInfo`  |

---

<a id="deviceinfo_validate_serial_number"></a>
### TestCase Name
DeviceInfo_Validate_Serial_Number

### TestCase ID
DI_17

### TestCase Objective
Verify whether the serial number returned by deviceinfo API matches the serial number in system or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeviceInfo Get Serial Number | Invoke serialnumber on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.serialnumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the serial number is retrieved successfully from DeviceInfo API |
| 2 | System Get Device Serial Number | Invoke getSerialNumber on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Verify that the serial number is retrieved successfully from System API |
| 3 | Comparison of Two API Results | Compare serial number from step 1 (DeviceInfo API) against serial number from step 2 (System API) | Verify that the serial number returned by `DeviceInfo.serialnumber` matches the serial number returned by `System.getSerialNumber`  |

---

<a id="deviceinfo_validate_supported_audio_ports"></a>
### TestCase Name
DeviceInfo_Validate_Supported_Audio_Ports

### TestCase ID
DI_18

### TestCase Objective
Verify whether the audio ports returned by deviceinfo API matches the audio ports in displaysettings or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeviceInfo Get Supported Audio Ports | Invoke supportedaudioports on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedaudioports"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio ports are retrieved successfully from DeviceInfo API |
| 2 | DisplaySettings Get Supported Audio Ports | Invoke getSupportedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio ports returned by `DisplaySettings.getSupportedAudioPorts` match the ports returned by `DeviceInfo.supportedaudioports`  |

---

<a id="deviceinfo_validate_supported_video_ports"></a>
### TestCase Name
DeviceInfo_Validate_Supported_Video_Ports

### TestCase ID
DI_19

### TestCase Objective
Verify whether the video ports returned by deviceinfo API matches the video ports in displaysettings or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeviceInfo Get Supported Video Displays | Invoke supportedvideodisplays on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedvideodisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported video displays are retrieved successfully from DeviceInfo API |
| 2 | DisplaySettings Get Supported Video Displays | Invoke getSupportedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported video displays returned by `DisplaySettings.getSupportedVideoDisplays` match the displays returned by `DeviceInfo.supportedvideodisplays`  |

---

<a id="deviceinfo_validate_host_edid"></a>
### TestCase Name
DeviceInfo_Validate_Host_EDID

### TestCase ID
DI_20

### TestCase Objective
Verify whether the host EDID details returned by deviceinfo API matches the EDID details in displaysettings or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | DeviceInfo Get Host EDID Details | Invoke hostedid on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.hostedid"}' http://127.0.0.1:9998/jsonrpc` | Verify that the host EDID details are retrieved successfully from DeviceInfo API |
| 2 | DisplaySettings Get Host EDID Details | Invoke readHostEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readHostEDID"}' http://127.0.0.1:9998/jsonrpc` | Verify that the host EDID details are retrieved successfully from DisplaySettings API |
| 3 | Comparison of Two API Results | Compare host EDID from step 1 (DeviceInfo API) against host EDID from step 2 (DisplaySettings API) | Verify that the host EDID returned by `DeviceInfo.hostedid` matches the EDID returned by `DisplaySettings.readHostEDID`  |

---

<a id="deviceinfo_validate_hdcp_version"></a>
### TestCase Name
DeviceInfo_Validate_HDCP_Version

### TestCase ID
DI_21

### TestCase Objective
Verify whether the HDCP version returned by deviceinfo API matches the HDCP version in HdcpProfile plugin or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video display name is retrieved successfully |
| 2 | DeviceInfo Get Supported HDCP | Invoke supportedhdcp on DeviceInfo with videoDisplay<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedhdcp", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported HDCP version is retrieved successfully from DeviceInfo API |
| 3 | HdcpProfile Get Supported HDCP | Invoke getSettopHDCPSupport on org.rdk.HdcpProfile<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getSettopHDCPSupport"}' http://127.0.0.1:9998/jsonrpc` | Verify that the HDCP version returned by `HdcpProfile.getSettopHDCPSupport` matches the version returned by `DeviceInfo.supportedhdcp`  |

---

<a id="deviceinfo_validate_default_resolution"></a>
### TestCase Name
DeviceInfo_Validate_Default_Resolution

### TestCase ID
DI_22

### TestCase Objective
Check whether the default resolution returned by deviceinfo API matches the default resolution in displaysettings plugin or not

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video display name is retrieved successfully |
| 2 | DeviceInfo Get Default Resolution | Invoke defaultresolution on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.defaultresolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that the default resolution is retrieved successfully from DeviceInfo API |
| 3 | DisplaySettings Get Default Resolution | Invoke getDefaultResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that the default resolution returned by `DisplaySettings.getDefaultResolution` matches the resolution returned by `DeviceInfo.defaultresolution`  |

---

<a id="deviceinfo_check_systeminfo_api_date_matches_dut_date"></a>
### TestCase Name
DeviceInfo_Check_SystemInfo_API_Date_Matches_DUT_Date

### TestCase ID
DI_23

### TestCase Objective
Check if the date returned by the systeminfo API matches the DUT date

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get SystemInfo API Date | Invoke systeminfo on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the system date is retrieved successfully from DeviceInfo API |
| 2 | Get DUT Date | Retrieve current date directly from the DUT system | Verify that the DUT system date is retrieved successfully and saved for comparison  |
| 3 | Compare SystemInfo API Date With DUT Date | Compare date from step 1 (DeviceInfo systeminfo API) against date from step 2 (DUT system date) | Verify that the date returned by `DeviceInfo.systeminfo` matches the current date on the DUT  |

---

<a id="deviceinfo_get_device_socname"></a>
### TestCase Name
DeviceInfo_Get_Device_SocName

### TestCase ID
DI_24

### TestCase Objective
Checks the device SOC Name

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device SocName | Invoke socname on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.socname"}' http://127.0.0.1:9998/jsonrpc` | Verify that the information retrieved from the socname API is not empty  |

---

<a id="deviceinfo_get_device_manufacturer"></a>
### TestCase Name
DeviceInfo_Get_Device_Manufacturer

### TestCase ID
DI_25

### TestCase Objective
Checks the device manufacturer

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Device Manufacturer | Invoke make on DeviceInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.make"}' http://127.0.0.1:9998/jsonrpc` | Verify that the information retrieved from the make API is not empty  |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5 mins

**Priority** : Medium

**Release Version** : M81

<div align="right"><a href="#testscript-name">Go to Top</a></div>
