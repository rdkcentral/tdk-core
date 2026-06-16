## Table of Contents

1. [Objective](#objective)
2. [Pre-conditions](#pre-conditions)
3. [Test Cases](#test-cases)
   - [DeviceInfo_Get_All_System_Info (DI_01)](#deviceinfo_get_all_system_info-di_01)
   - [DeviceInfo_Get_All_Network_Interfaces (DI_02)](#deviceinfo_get_all_network_interfaces-di_02)
   - [DeviceInfo_Get_SocketInfo_Negative_Case (DI_03)](#deviceinfo_get_socketinfo_negative_case-di_03)
   - [DeviceInfo_ActivateDeactivate_STRESS (DI_04)](#deviceinfo_activatedeactivate_stress-di_04)
   - [DeviceInfo_Get_Serial_Number (DI_05)](#deviceinfo_get_serial_number-di_05)
   - [DeviceInfo_Check_Model_Name (DI_06)](#deviceinfo_check_model_name-di_06)
   - [DeviceInfo_Check_Firmware_Version (DI_07)](#deviceinfo_check_firmware_version-di_07)
   - [DeviceInfo_Check_Supported_Audio_Ports (DI_08)](#deviceinfo_check_supported_audio_ports-di_08)
   - [DeviceInfo_Check_Supported_Video_Displays (DI_09)](#deviceinfo_check_supported_video_displays-di_09)
   - [DeviceInfo_Check_Host_EDID (DI_10)](#deviceinfo_check_host_edid-di_10)
   - [DeviceInfo_Check_Default_Resolution (DI_11)](#deviceinfo_check_default_resolution-di_11)
   - [DeviceInfo_Check_Supported_HDCP_Version (DI_12)](#deviceinfo_check_supported_hdcp_version-di_12)
   - [DeviceInfo_Check_Model_ID (DI_13)](#deviceinfo_check_model_id-di_13)
   - [DeviceInfo_Check_Device_Type (DI_14)](#deviceinfo_check_device_type-di_14)
   - [DeviceInfo_ActivateDeactivate_Event_Test (DI_15)](#deviceinfo_activatedeactivate_event_test-di_15)
   - [DeviceInfo_Validate_Firmware_Version (DI_16)](#deviceinfo_validate_firmware_version-di_16)
   - [DeviceInfo_Validate_Serial_Number (DI_17)](#deviceinfo_validate_serial_number-di_17)
   - [DeviceInfo_Validate_Supported_Audio_Ports (DI_18)](#deviceinfo_validate_supported_audio_ports-di_18)
   - [DeviceInfo_Validate_Supported_Video_Ports (DI_19)](#deviceinfo_validate_supported_video_ports-di_19)
   - [DeviceInfo_Validate_Host_EDID (DI_20)](#deviceinfo_validate_host_edid-di_20)
   - [DeviceInfo_Validate_HDCP_Version (DI_21)](#deviceinfo_validate_hdcp_version-di_21)
   - [DeviceInfo_Validate_Default_Resolution (DI_22)](#deviceinfo_validate_default_resolution-di_22)
   - [DeviceInfo_Check_SystemInfo_API_Date_Matches_DUT_Date (DI_23)](#deviceinfo_check_systeminfo_api_date_matches_dut_date-di_23)
   - [DeviceInfo_Get_Device_SocName (DI_24)](#deviceinfo_get_device_socname-di_24)
   - [DeviceInfo_Get_Device_Manufacturer (DI_25)](#deviceinfo_get_device_manufacturer-di_25)
4. [Post-conditions](#post-conditions)
5. [Test Attributes](#test-attributes)

---

## Objective

The **DeviceInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `DeviceInfo` (version 1)

**API Coverage**

- **Configuration APIs**: `addresses`
- **Other APIs**: `defaultresolution`, `devicetype`, `firmwareversion`, `hostedid`, `make`, `modelid`, `modelname`, `serialnumber`, `socketinfo`, `socname`, `supportedaudioports`, `supportedhdcp`, `supportedresolutions`, `supportedvideodisplays`, `systeminfo`

### APIs Under Test

| API | Description |
|-----|-------------|
| `addresses` | Network interface addresses |
| `defaultresolution` | Default resolution on the selected video display port |
| `devicetype` | Provides access to the device type |
| `firmwareversion` | Provides access to the versions maintained in version.txt |
| `hostedid` | Provides access to the EDID of the host |
| `make` | Provides access to the device manufacturer |
| `modelid` | Provides access to the device model number or SKU |
| `modelname` | Provides access to the friendly device model name |
| `serialnumber` | Provides access to the serial number set by manufacturer |
| `socketinfo` | Socket information |
| `socname` | Provides access to the SOC Name |
| `supportedaudioports` | Provides access to the audio ports supported on the device |
| `supportedhdcp` | Supported HDCP version on the selected video display port |
| `supportedresolutions` | Supported resolutions on the selected video display port |
| `supportedvideodisplays` | Provides access to the video ports supported on the device |
| `systeminfo` | System general information |

---

## Pre-conditions

### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.DisplaySettings"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 3: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.System"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 4: Activate_HdcpProfile_Plugin

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"org.rdk.HdcpProfile"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.HdcpProfile"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.HdcpProfile"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

### Pre-condition 5: Register_And_Listen_Events

- Register and listen to event `Event_Controller_State_Changed` on `Controller` plugin

---

## Test Cases

<a id="deviceinfo_get_all_system_info-di_01"></a>
### DeviceInfo_Get_All_System_Info (DI_01)

**Objective:** Gets all system information

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get System Info | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | System information returned successfully |

---

<a id="deviceinfo_get_all_network_interfaces-di_02"></a>
### DeviceInfo_Get_All_Network_Interfaces (DI_02)

**Objective:** Gets all network interfaces

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Network Interfaces | Invoke `addresses` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.addresses"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag: `deviceinfo_get_network_info` |

---

<a id="deviceinfo_get_socketinfo_negative_case-di_03"></a>
### DeviceInfo_Get_SocketInfo_Negative_Case (DI_03)

**Objective:** Checks the negative scenario for Socket info API

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Socket Info | Invoke `socketinfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.socketinfo"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message: `Unknown method.` |

---

<a id="deviceinfo_activatedeactivate_stress-di_04"></a>
### DeviceInfo_ActivateDeactivate_STRESS (DI_04)

**Objective:** Activates and deactivates the plugin

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check DeviceInfo Active Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Deactivate DeviceInfo Plugin | Repeat this sequence for `<STRESS_TEST_REPEAT_COUNT>` iterations.<br>Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 3 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 4 | Get CPU Load | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | CPU load is retrieved and validated successfully |

---

<a id="deviceinfo_get_serial_number-di_05"></a>
### DeviceInfo_Get_Serial_Number (DI_05)

**Objective:** Checks the serial number

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Serial Number | Invoke `serialnumber` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.serialnumber"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag: `deviceinfo_get_api_info` |

---

<a id="deviceinfo_check_model_name-di_06"></a>
### DeviceInfo_Check_Model_Name (DI_06)

**Objective:** Checks the model name of the DUT

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | Read expected model name by executing: `grep FRIENDLY_ID <DEVICEINFO_DEVICE_DETAILS_FILE_PATH> \| cut -d'=' -f2- \| xargs` | `FRIENDLY_ID` value retrieved successfully and saved for comparison |
| 2 | Get Model Name | Invoke `modelname` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.modelname"}' http://127.0.0.1:9998/jsonrpc` | Model name returned by API matches `FRIENDLY_ID` value retrieved in step 1 |

---

<a id="deviceinfo_check_firmware_version-di_07"></a>
### DeviceInfo_Check_Firmware_Version (DI_07)

**Objective:** Checks the firmware version of the DUT

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Current Image Version | Retrieve current firmware image version from device | Current firmware image version retrieved from device successfully |
| 2 | Get Firmware Version | Invoke `firmwareversion` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.firmwareversion"}' http://127.0.0.1:9998/jsonrpc` | Firmware version matches expected value retrieved from device |

---

<a id="deviceinfo_check_supported_audio_ports-di_08"></a>
### DeviceInfo_Check_Supported_Audio_Ports (DI_08)

**Objective:** Check whether settop lists supported audio ports

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Supported Audio Ports | Invoke `supportedaudioports` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedaudioports"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<SUPPORTED_AUDIO_PORTS>` |

---

<a id="deviceinfo_check_supported_video_displays-di_09"></a>
### DeviceInfo_Check_Supported_Video_Displays (DI_09)

**Objective:** Check whether settop displays supported video displays

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Supported Video Displays | Invoke `supportedvideodisplays` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedvideodisplays"}' http://127.0.0.1:9998/jsonrpc` | Expected: `<SUPPORTED_VIDEO_DISPLAYS>` |

---

<a id="deviceinfo_check_host_edid-di_10"></a>
### DeviceInfo_Check_Host_EDID (DI_10)

**Objective:** Check the EDID status of host

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Host EDID Details | Invoke `hostedid` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.hostedid"}' http://127.0.0.1:9998/jsonrpc` | The information retrieved from the hostedid API must not be empty |

---

<a id="deviceinfo_check_default_resolution-di_11"></a>
### DeviceInfo_Check_Default_Resolution (DI_11)

**Objective:** Check whether the default resolution is available in supported resolutions

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | Get Supported Resolutions | Invoke `supportedresolutions` on `DeviceInfo` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedresolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | The information retrieved from the supportedresolutions API must not be empty |
| 3 | Get Default Resolution | Invoke `defaultresolution` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.defaultresolution"}' http://127.0.0.1:9998/jsonrpc` | Expected `compared against value from step 2` |

---

<a id="deviceinfo_check_supported_hdcp_version-di_12"></a>
### DeviceInfo_Check_Supported_HDCP_Version (DI_12)

**Objective:** Checks the supported HDCP version

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected Video Displays returned successfully |
| 2 | Get Supported HDCP | Invoke `supportedhdcp` on `DeviceInfo` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedhdcp", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | HDCP version matches expected value from configuration |

---

<a id="deviceinfo_check_model_id-di_13"></a>
### DeviceInfo_Check_Model_ID (DI_13)

**Objective:** Checks the model id of the DUT

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Details | Read expected `^MODEL_NUM` value from device config file `<DEVICEINFO_DEVICE_DETAILS_FILE_PATH>` | Expected `^MODEL_NUM` value read from device config file successfully |
| 2 | Get Model ID | Invoke `modelid` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.modelid"}' http://127.0.0.1:9998/jsonrpc` | API response matches expected value from `step 1` |

---

<a id="deviceinfo_check_device_type-di_14"></a>
### DeviceInfo_Check_Device_Type (DI_14)

**Objective:** Checks the device type of the DUT

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Type | Invoke `devicetype` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.devicetype"}' http://127.0.0.1:9998/jsonrpc` | Device type returned by API matches expected value `<DEVICEINFO_DEVICE_TYPE>` from device config file |

---

<a id="deviceinfo_activatedeactivate_event_test-di_15"></a>
### DeviceInfo_ActivateDeactivate_Event_Test (DI_15)

**Objective:** Validates statechange event on Activating/deactivating the plugin

**Pre-condition:**

#### Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state returned successfully |
| 2 | Activate Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Deactivate DeviceInfo Plugin | Invoke `deactivate` on `Controller` with `callsign`: `"DeviceInfo"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Disabled successfully |
| 2 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 3 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `deactivated` |
| 4 | Activate DeviceInfo Plugin | Invoke `activate` on `Controller` with `callsign`: `"DeviceInfo"` (wait 1 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "DeviceInfo"}}' http://127.0.0.1:9998/jsonrpc` | Enabled successfully |
| 5 | Check State Change Event | Listen for event `Event_Controller_State_Changed` | Event data validated successfully |
| 6 | Check PluginActive Status | Invoke `status` on `Controller`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@DeviceInfo"}' http://127.0.0.1:9998/jsonrpc` | Plugin state matches `activated` |

---

<a id="deviceinfo_validate_firmware_version-di_16"></a>
### DeviceInfo_Validate_Firmware_Version (DI_16)

**Objective:** Verify whether the firmware version returned by deviceinfo API matches the firmware version in system or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeviceInfo Get Firmware Version | Invoke `firmwareversion` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.firmwareversion"}' http://127.0.0.1:9998/jsonrpc` | Firmware version retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | System Get Device Image Version | Invoke `getDeviceInfo` on `org.rdk.System` with `params`: `"imageVersion"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getDeviceInfo", "params": {"params": "imageVersion"}}' http://127.0.0.1:9998/jsonrpc` | Image version retrieved successfully from System API and saved for comparison |
| 3 | Comparison of Two API Results | Compare firmware version from step 1 (DeviceInfo API) against image version from step 2 (System API) | Firmware version returned by `DeviceInfo.firmwareversion` matches the image version returned by `System.getDeviceInfo` |

---

<a id="deviceinfo_validate_serial_number-di_17"></a>
### DeviceInfo_Validate_Serial_Number (DI_17)

**Objective:** Verify whether the serial number returned by deviceinfo API matches the serial number in system or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeviceInfo Get Serial Number | Invoke `serialnumber` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.serialnumber"}' http://127.0.0.1:9998/jsonrpc` | Serial number retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | System Get Device Serial Number | Invoke `getSerialNumber` on `org.rdk.System`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getSerialNumber"}' http://127.0.0.1:9998/jsonrpc` | Serial number retrieved successfully from System API and saved for comparison |
| 3 | Comparison of Two API Results | Compare serial number from step 1 (DeviceInfo API) against serial number from step 2 (System API) | Serial number returned by `DeviceInfo.serialnumber` matches the serial number returned by `System.getSerialNumber` |

---

<a id="deviceinfo_validate_supported_audio_ports-di_18"></a>
### DeviceInfo_Validate_Supported_Audio_Ports (DI_18)

**Objective:** Verify whether the audio ports returned by deviceinfo API matches the audio ports in displaysettings or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeviceInfo Get Supported Audio Ports | Invoke `supportedaudioports` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedaudioports"}' http://127.0.0.1:9998/jsonrpc` | Supported audio ports retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | DisplaySettings Get Supported Audio Ports | Invoke `getSupportedAudioPorts` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Supported audio ports returned by `DisplaySettings.getSupportedAudioPorts` matches the ports returned by `DeviceInfo.supportedaudioports` in step 1 |

---

<a id="deviceinfo_validate_supported_video_ports-di_19"></a>
### DeviceInfo_Validate_Supported_Video_Ports (DI_19)

**Objective:** Verify whether the video ports returned by deviceinfo API matches the video ports in displaysettings or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeviceInfo Get Supported Video Displays | Invoke `supportedvideodisplays` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedvideodisplays"}' http://127.0.0.1:9998/jsonrpc` | Supported video displays retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | DisplaySettings Get Supported Video Displays | Invoke `getSupportedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Supported video displays returned by `DisplaySettings.getSupportedVideoDisplays` matches the displays returned by `DeviceInfo.supportedvideodisplays` in step 1 |

---

<a id="deviceinfo_validate_host_edid-di_20"></a>
### DeviceInfo_Validate_Host_EDID (DI_20)

**Objective:** Verify whether the host EDID details returned by deviceinfo API matches the EDID details in displaysettings or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | DeviceInfo Get Host EDID Details | Invoke `hostedid` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.hostedid"}' http://127.0.0.1:9998/jsonrpc` | Host EDID details retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | DisplaySettings Get Host EDID Details | Invoke `readHostEDID` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readHostEDID"}' http://127.0.0.1:9998/jsonrpc` | Host EDID details retrieved successfully from DisplaySettings API and saved for comparison |
| 3 | Comparison of Two API Results | Compare host EDID from step 1 (DeviceInfo API) against host EDID from step 2 (DisplaySettings API) | Host EDID returned by `DeviceInfo.hostedid` matches the EDID returned by `DisplaySettings.readHostEDID` |

---

<a id="deviceinfo_validate_hdcp_version-di_21"></a>
### DeviceInfo_Validate_HDCP_Version (DI_21)

**Objective:** Verify whether the HDCP version returned by deviceinfo API matches the HDCP version in HdcpProfile plugin or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected video display name retrieved successfully and saved for use in step 2 |
| 2 | DeviceInfo Get Supported HDCP | Invoke `supportedhdcp` on `DeviceInfo` with `videoDisplay`: `"<result_step_1>"`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.supportedhdcp", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Supported HDCP version retrieved successfully from DeviceInfo API and saved for comparison |
| 3 | HdcpProfile Get Supported HDCP | Invoke `getSettopHDCPSupport` on `org.rdk.HdcpProfile`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.HdcpProfile.1.getSettopHDCPSupport"}' http://127.0.0.1:9998/jsonrpc` | HDCP version returned by `HdcpProfile.getSettopHDCPSupport` matches the version returned by `DeviceInfo.supportedhdcp` in step 2 |

---

<a id="deviceinfo_validate_default_resolution-di_22"></a>
### DeviceInfo_Validate_Default_Resolution (DI_22)

**Objective:** Check whether the default resolution returned by deviceinfo API matches the default resolution in displaysettings plugin or not

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Check Display Connected Status | Invoke `getConnectedVideoDisplays` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Connected video display name retrieved successfully and saved for use in subsequent steps |
| 2 | DeviceInfo Get Default Resolution | Invoke `defaultresolution` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.defaultresolution"}' http://127.0.0.1:9998/jsonrpc` | Default resolution retrieved successfully from DeviceInfo API and saved for comparison |
| 3 | DisplaySettings Get Default Resolution | Invoke `getDefaultResolution` on `org.rdk.DisplaySettings`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | Default resolution returned by `DisplaySettings.getDefaultResolution` matches the resolution returned by `DeviceInfo.defaultresolution` in step 2 |

---

<a id="deviceinfo_check_systeminfo_api_date_matches_dut_date-di_23"></a>
### DeviceInfo_Check_SystemInfo_API_Date_Matches_DUT_Date (DI_23)

**Objective:** Check if the date returned by the systeminfo API matches the DUT date

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get SystemInfo API Date | Invoke `systeminfo` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.systeminfo"}' http://127.0.0.1:9998/jsonrpc` | System date retrieved successfully from DeviceInfo API and saved for comparison |
| 2 | Get DUT Date | Retrieve current date directly from the DUT system | DUT system date retrieved successfully and saved for comparison |
| 3 | Compare SystemInfo API Date With DUT Date | Compare date from step 1 (DeviceInfo `systeminfo` API) against date from step 2 (DUT system date) | Date returned by `DeviceInfo.systeminfo` matches the current date on the DUT |

---

<a id="deviceinfo_get_device_socname-di_24"></a>
### DeviceInfo_Get_Device_SocName (DI_24)

**Objective:** Checks the device SOC Name

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device SocName | Invoke `socname` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.socname"}' http://127.0.0.1:9998/jsonrpc` | The information retrieved from the socname API must not be empty` |

---

<a id="deviceinfo_get_device_manufacturer-di_25"></a>
### DeviceInfo_Get_Device_Manufacturer (DI_25)

**Objective:** Checks the device manufacturer

**Test Steps:**

| Step ID | Step Name | Description | Expected Result |
|---------|-----------|-------------|-----------------|
| 1 | Get Device Manufacturer | Invoke `make` on `DeviceInfo`<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "DeviceInfo.1.make"}' http://127.0.0.1:9998/jsonrpc` | The information retrieved from the make API must not be empty |

---

---

## Post-conditions

_No plugin-level post-conditions defined._

---

## Test Attributes

| Attribute | Value |
|-----------|-------|
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M81 |