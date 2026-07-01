## TestScript Name
RDKV_CERT_AVS_Display_Settings

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
   - [Check_Settop_Supported_Resolutions](#check_settop_supported_resolutions)
   - [Check_Supported_Tv_Resolutions](#check_supported_tv_resolutions)
   - [Check_Supported_Video_Displays](#check_supported_video_displays)
   - [Check_Supported_Audio_Ports](#check_supported_audio_ports)
   - [Check_Settop_HDR_Support](#check_settop_hdr_support)
   - [Check_TV_HDR_Support](#check_tv_hdr_support)
   - [Read_Host_EDID](#read_host_edid)
   - [Read_Connected_Device_EDID](#read_connected_device_edid)
   - [Set_And_Get_Supported_Audio_Modes_HDMI0](#set_and_get_supported_audio_modes_hdmi0)
   - [Set_And_Get_Zoom_Settings](#set_and_get_zoom_settings)
   - [Set_And_Get_VideoPort_Status_InStandby_Negative_Case](#set_and_get_videoport_status_instandby_negative_case)
   - [Set_And_Get_MS12_Audio_Compression](#set_and_get_ms12_audio_compression)
   - [Check_Current_Output_Settings](#check_current_output_settings)
   - [Check_Active_Input_Value](#check_active_input_value)
   - [SetAndGet_All_Supported_Resolutions](#setandget_all_supported_resolutions)
   - [Enable_And_Disable_Dolby_Volume_Mode](#enable_and_disable_dolby_volume_mode)
   - [Set_And_Get_Dialog_Enhancement](#set_and_get_dialog_enhancement)
   - [Set_And_Get_Intelligent_Equalizer_Mode](#set_and_get_intelligent_equalizer_mode)
   - [Set_And_Get_Volume_Leveller_HDMI0](#set_and_get_volume_leveller_hdmi0)
   - [Set_And_Get_DRC_Mode_HDMI0](#set_and_get_drc_mode_hdmi0)
   - [Set_And_Get_Volume_Level_HDMI0](#set_and_get_volume_level_hdmi0)
   - [Set_And_Get_Gain_HDMI0](#set_and_get_gain_hdmi0)
   - [Mute_And_Unmute_Audio_HDMI0](#mute_and_unmute_audio_hdmi0)
   - [Set_And_Get_Audio_Delay_HDMI0](#set_and_get_audio_delay_hdmi0)
   - [Set_And_Get_Audio_Delay_Offset_HDMI0](#set_and_get_audio_delay_offset_hdmi0)
   - [Check_Sink_Atmos_Capability](#check_sink_atmos_capability)
   - [Enable_Disable_Audio_Atmos_Output_Mode](#enable_disable_audio_atmos_output_mode)
   - [Get_TV_HDR_Capabilities](#get_tv_hdr_capabilities)
   - [Is_Connected_Device_Repeater](#is_connected_device_repeater)
   - [Get_Default_Resolution](#get_default_resolution)
   - [Set_And_Get_Supported_Audio_Modes_SPDIF0](#set_and_get_supported_audio_modes_spdif0)
   - [Set_And_Get_Supported_Audio_Modes_IDLR0](#set_and_get_supported_audio_modes_idlr0)
   - [Set_And_Get_Supported_Audio_Modes_SPEAKER0](#set_and_get_supported_audio_modes_speaker0)
   - [Set_And_Get_Volume_Leveller_SPDIF0](#set_and_get_volume_leveller_spdif0)
   - [Set_And_Get_Volume_Leveller_IDLR0](#set_and_get_volume_leveller_idlr0)
   - [Set_And_Get_Volume_Leveller_SPEAKER0](#set_and_get_volume_leveller_speaker0)
   - [Set_And_Get_DRC_Mode_SPDIF0](#set_and_get_drc_mode_spdif0)
   - [Set_And_Get_DRC_Mode_IDLR0](#set_and_get_drc_mode_idlr0)
   - [Set_And_Get_DRC_Mode_SPEAKER0](#set_and_get_drc_mode_speaker0)
   - [Set_And_Get_Volume_Level_SPDIF0](#set_and_get_volume_level_spdif0)
   - [Set_And_Get_Volume_Level_IDLR0](#set_and_get_volume_level_idlr0)
   - [Set_And_Get_Volume_Level_SPEAKER0](#set_and_get_volume_level_speaker0)
   - [Set_And_Get_Gain_SPDIF0](#set_and_get_gain_spdif0)
   - [Set_And_Get_Gain_IDLR0](#set_and_get_gain_idlr0)
   - [Set_And_Get_Gain_SPEAKER0](#set_and_get_gain_speaker0)
   - [Mute_And_Unmute_Audio_SPDIF0](#mute_and_unmute_audio_spdif0)
   - [Mute_And_Unmute_Audio_IDLR0](#mute_and_unmute_audio_idlr0)
   - [Mute_And_Unmute_Audio_SPEAKER0](#mute_and_unmute_audio_speaker0)
   - [Set_And_Get_Audio_Delay_SPDIF0](#set_and_get_audio_delay_spdif0)
   - [Set_And_Get_Audio_Delay_IDLR0](#set_and_get_audio_delay_idlr0)
   - [Set_And_Get_Audio_Delay_SPEAKER0](#set_and_get_audio_delay_speaker0)
   - [Set_And_Get_Audio_Delay_Offset_SPDIF0](#set_and_get_audio_delay_offset_spdif0)
   - [Set_And_Get_Audio_Delay_Offset_IDLR0](#set_and_get_audio_delay_offset_idlr0)
   - [Set_And_Get_Audio_Delay_Offset_SPEAKER0](#set_and_get_audio_delay_offset_speaker0)
   - [Enable_And_Disable_AudioPort_HDMI0](#enable_and_disable_audioport_hdmi0)
   - [Enable_And_Disable_AudioPort_SPDIF0](#enable_and_disable_audioport_spdif0)
   - [Enable_And_Disable_AudioPort_IDLR0](#enable_and_disable_audioport_idlr0)
   - [Enable_And_Disable_AudioPort_SPEAKER0](#enable_and_disable_audioport_speaker0)
   - [Check_Settop_Audio_Capabilities_HDMI0](#check_settop_audio_capabilities_hdmi0)
   - [Check_Settop_MS12_Capabilities_HDMI0](#check_settop_ms12_capabilities_hdmi0)
   - [Set_And_Get_Volume_Leveller_Modes_HDMI0](#set_and_get_volume_leveller_modes_hdmi0)
   - [Check_Supported_Resolutions](#check_supported_resolutions)
   - [Check_Active_Input_Value_For_Invalid_Display](#check_active_input_value_for_invalid_display)
   - [Check_VideoPort_Standby_Status_For_Invalid_Display](#check_videoport_standby_status_for_invalid_display)
   - [Set_And_Get_Negative_Audio_Delay](#set_and_get_negative_audio_delay)
   - [Check_Supported_Audio_Modes_Without_Audio_Port](#check_supported_audio_modes_without_audio_port)
   - [Check_Current_And_Supported_Video_Formats](#check_current_and_supported_video_formats)
   - [Check_Current_And_Supported_Audio_Formats](#check_current_and_supported_audio_formats)
   - [Check_Resolution_Persisted_After_Reboot](#check_resolution_persisted_after_reboot)
   - [Check_Resolution_Not_Persisted_After_Reboot](#check_resolution_not_persisted_after_reboot)
   - [SetAndGet_Supported_Color_Depth_Capabilities](#setandget_supported_color_depth_capabilities)
   - [Check_Resolution_PreChange_Event](#check_resolution_prechange_event)
   - [Check_Resolution_Persisted_For_30Seconds_After_Reboot](#check_resolution_persisted_for_30seconds_after_reboot)
   - [Check_Mute_Status_Changed_Event_HDMI0](#check_mute_status_changed_event_hdmi0)
   - [Check_Volume_Level_Changed_Event_HDMI0](#check_volume_level_changed_event_hdmi0)
   - [Set_And_Get_Negative_Volume_Level_HDMI0](#set_and_get_negative_volume_level_hdmi0)
   - [Set_and_Get_Fader_Control_HDMI0](#set_and_get_fader_control_hdmi0)
   - [Set_Empty_Fader_Control_HDMI0](#set_empty_fader_control_hdmi0)
   - [Set_Fader_Control_OutofRange_HDMI0](#set_fader_control_outofrange_hdmi0)
   - [Set_and_Get_Audio_Mixing_Status_HDMI0](#set_and_get_audio_mixing_status_hdmi0)
   - [DisplaySettings_ActivateDeactivate_Event_Test](#displaysettings_activatedeactivate_event_test)
   - [DisplaySettings_Using_KeyCode_Verify_MuteStatus_After_Increasing_Volume_HDMI0](#displaysettings_using_keycode_verify_mutestatus_after_increasing_volume_hdmi0)
   - [DisplaySettings_Using_KeyCode_Verify_MuteStatus_After_decreasing_Volume_HDMI0](#displaysettings_using_keycode_verify_mutestatus_after_decreasing_volume_hdmi0)
   - [DisplaySettings_Using_KeyCode_Verify_MuteStatus_HDMI0](#displaysettings_using_keycode_verify_mutestatus_hdmi0)
   - [Set_Mute_Invalid_audioPort](#set_mute_invalid_audioport)
   - [Set_Mute_empty_audioPort](#set_mute_empty_audioport)
   - [Get_Dialog_Enhancement_InvalidAudioPort](#get_dialog_enhancement_invalidaudioport)
   - [Get_Dialog_Enhancement_EmptyAudioPort](#get_dialog_enhancement_emptyaudioport)
   - [Get_Volume_Level_Invalid](#get_volume_level_invalid)
   - [Get_Volume_Level_EmptyAudioPort](#get_volume_level_emptyaudioport)
   - [DisplaySettings_Verify_VolumeLevelChanged_Event_Not_Triggered_with_Same_VolumeLevel_HDMI0](#displaysettings_verify_volumelevelchanged_event_not_triggered_with_same_volumelevel_hdmi0)
   - [DisplaySettings_Verify_MuteStatusChanged_Event_Not_Triggered_with_Same_MuteStatus_HDMI0](#displaysettings_verify_mutestatuschanged_event_not_triggered_with_same_mutestatus_hdmi0)
   - [Set_Invalid_Resolution](#set_invalid_resolution)
   - [Set_Empty_Resolution](#set_empty_resolution)
   - [Set_InvalidDataType_Resolution](#set_invaliddatatype_resolution)
   - [Set_Empty_VideoDisplay](#set_empty_videodisplay)
   - [Set_Invalid_VideoDisplay](#set_invalid_videodisplay)
   - [Set_Invalid_Persist](#set_invalid_persist)
   - [Set_Resolution_WithoutParameter](#set_resolution_withoutparameter)
   - [DisplaySettings_Check_Display_Connected_Status_After_Light_Sleep_HDMI0](#displaysettings_check_display_connected_status_after_light_sleep_hdmi0)
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **DisplaySettings** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.DisplaySettings` (version 1)

## APIs Under Test

| API | Description |
| --- | --- |
| `enableSurroundDecoder` | Enable or disable the surround decoder |
| `getActiveInput` | Get the active input status |
| `getAssociatedAudioMixing` | Returns the Associated Audio Mixing status |
| `getAudioDelay` | Get the audio delay value |
| `getAudioDelayOffset` | Get the audio delay offset value |
| `getAudioFormat` | Returns the current and supported audio formats |
| `getBassEnhancer` | Get the bass enhancer status |
| `getColorDepthCapabilities` | Returns supported color depth capabilities |
| `getConnectedAudioPorts` | Get the connected audio port details |
| `getConnectedVideoDisplays` | Get the connected video display details |
| `getCurrentOutputSettings` | Get the current output settings details |
| `getCurrentResolution` | Get the current resolution details |
| `getDRCMode` | Get the DRC mode value |
| `getDefaultResolution` | Get the default resolution value |
| `getDialogEnhancement` | Get the Dialog Enhancement value |
| `getDolbyVolumeMode` | Get the dolby volume mode status |
| `getEnableAudioPort` | Gets the current port enable status of specified input audioPort |
| `getFaderControl` | Returns the mixerbalance betweeen main and associated audio |
| `getGain` | Get the audio port gain value |
| `getGraphicEqualizerMode` | Gets the Graphic equalizer mode for specified audio port |
| `getIntelligentEqualizerMode` | Get the intelligent equalizer modevalue |
| `getMISteering` | Get the MI steering status |
| `getMS12AudioCompression` | Get the MS12Audio compression  details |
| `getMS12AudioProfile` | Gets the current MS12 audio profile |
| `getMuted` | Get the audio mute status |
| `getPreferredColorDepth` | Returns the current color depth on the selected video display port |
| `getSettopAudioCapabilities` | Gets the set-top audio capabilities for the specified audio port |
| `getSettopHDRSupport` | Get the Settop HDR support details |
| `getSettopMS12Capabilities` | Gets the set-top MS12 audio capabilities for the specified audio port |
| `getSinkAtmosCapability` | Get the sink atmos capability |
| `getSoundMode` | Get the sound mode details |
| `getSupportedAudioModes` | Get the supported audio modes details |
| `getSupportedAudioPorts` | Get the supported audio port details |
| `getSupportedMS12AudioProfiles` | Gets the supported MS12 audio profiles |
| `getSupportedResolutions` | Get the supported resolutions details |
| `getSupportedSettopResolutions` | Get the supported Set top box Resolutions details |
| `getSupportedTvResolutions` | Get the supported TV Resolutions details |
| `getSupportedVideoDisplays` | Get the supported video display details |
| `getSurroundVirtualizer` | Get the surround virtualizer value |
| `getTVHDRCapabilities` | Get the TV HDR  capability |
| `getTvHDRSupport` | Get the TV HDR support details |
| `getVideoFormat` | Returns the current and supported video formats |
| `getVideoPortStatusInStandby` | Get the video port status to be used in standby mode |
| `getVolumeLevel` | Get the Volume level |
| `getVolumeLeveller` | Get the volume leveller value |
| `getZoomSetting` | Get the zoom setting details |
| `isConnectedDeviceRepeater` | Get the TV HDR capability |
| `isSurroundDecoderEnabled` | Get the surround decoder status |
| `readEDID` | Read the EDID of connected output device |
| `readHostEDID` | Read the Host(STB) EDID details |
| `resetBassEnhancer` | Resets the dialog enhancer level to its default bassboost value |
| `resetDialogEnhancement` | Resets the dialog enhancer level to its default enhancer level |
| `resetSurroundVirtualizer` | Resets the surround virtualizer to its default boost value |
| `resetVolumeLeveller` | Resets the Volume Leveller level to default volume value |
| `setAssociatedAudioMixing` | Sets the Associated Audio Mixing Enable/Disable |
| `setAudioAtmosOutputMode` | Enable or disable the audio atmos output modee |
| `setAudioDelay` | Set the audio delay value |
| `setAudioDelayOffset` | Set the audio delay offset value |
| `setBassEnhancer` | Enable or disable the bass enhancer |
| `setCurrentResolution` | Set the current resolution values |
| `setDRCMode` | Set the DRC mode values |
| `setDialogEnhancement` | Set the dialog enhancement values |
| `setDolbyVolumeMode` | Set the dolby volume mode as true or false |
| `setEnableAudioPort` | Enable or disable specified audioPort based on the input audio port |
| `setFaderControl` | Sets the set the mixerbalance betweeen main and associated audio |
| `setGain` | Set the audio port gain value |
| `setGraphicEqualizerMode` | Sets the Graphic  equalizer mode for specified audio port |
| `setIntelligentEqualizerMode` | Set the intelligent equalizer mode values |
| `setMISteering` | Enable or disable the MI Steering |
| `setMS12AudioCompression` | Set the MS12Audio compression values |
| `setMS12AudioProfile` | Configures selected MS12 Audio Profile |
| `setMS12ProfileSettingsOverride` | Overrides individual MS12 audio settings in order to optimize the customer experience |
| `setMuted` | Set the audio mute |
| `setPreferredColorDepth` | Sets the current color depth for the videoDisplay |
| `setScartParameter` | Set Scart parameter values |
| `setSoundMode` | Set the sound mode values |
| `setSurroundVirtualizer` | Set the surround virtualizer values |
| `setVideoPortStatusInStandby` | Set the video port status to be used in standby mode |
| `setVolumeLevel` | Set the volume level value |
| `setVolumeLeveller` | Set the volume leveller values |
| `setZoomSetting` | Set the zoom setting values |

## Events Under Test

| Event | Description |
| --- | --- |
| `muteStatusChanged` | Triggered on resolution pre-change |
| `resolutionChanged` | Fires on changing resolution |
| `resolutionPreChange` | Triggered on resolution pre-change |
| `volumeLevelChanged` | Triggered on resolution pre-change |
| `zoomSettingUpdated` | Zoom settings updated event |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_System_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.System"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of System Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.System"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the zoomSettingUpdated event | Register a WebSocket event listener for `zoomSettingUpdated` to receive `zoomSettingUpdated` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "zoomSettingUpdated", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the resolutionChanged event | Register a WebSocket event listener for `resolutionChanged` to receive `resolutionChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "resolutionChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 3 | Subscribe to the resolutionPreChange event | Register a WebSocket event listener for `resolutionPreChange` to receive `resolutionPreChange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "resolutionPreChange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 4 | Subscribe to the muteStatusChanged event | Register a WebSocket event listener for `muteStatusChanged` to receive `muteStatusChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "muteStatusChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 5 | Subscribe to the volumeLevelChanged event | Register a WebSocket event listener for `volumeLevelChanged` to receive `volumeLevelChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.register", "params": {"event": "volumeLevelChanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 6 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="check_settop_supported_resolutions"></a>
### TestCase Name
Check_Settop_Supported_Resolutions

### TestCase ID
DS_01

### TestCase Objective
Check whether settop displays all supported resoltions

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Settop Supported Resolutions | Invoke getSupportedSettopResolutions on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedSettopResolutions"}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list for settop should match the configured `SETTOP_SUPPORTED_RESOLUTIONS` values and `success` should be `true` |

---

<a id="check_supported_tv_resolutions"></a>
### TestCase Name
Check_Supported_Tv_Resolutions

### TestCase ID
DS_02

### TestCase Objective
Check whether settop displays supported TV resoltions

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Tv Resolutions | Invoke getSupportedTvResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedTvResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list for TV should be non-empty and `success` should be `true` |

---

<a id="check_supported_video_displays"></a>
### TestCase Name
Check_Supported_Video_Displays

### TestCase ID
DS_03

### TestCase Objective
Check whether settop displays supported video displays

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported Video Displays | Invoke getSupportedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Expected `<SUPPORTED_VIDEO_DISPLAYS>` |

---

<a id="check_supported_audio_ports"></a>
### TestCase Name
Check_Supported_Audio_Ports

### TestCase ID
DS_04

### TestCase Objective
Check whether settop lists supported audio ports

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Supported Audio Ports | Invoke getSupportedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Expected `<SUPPORTED_AUDIO_PORTS>` |

---

<a id="check_settop_hdr_support"></a>
### TestCase Name
Check_Settop_HDR_Support

### TestCase ID
DS_05

### TestCase Objective
Check whether settop has HDR support or not

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Settop HDR Support Details | Invoke getSettopHDRSupport on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSettopHDRSupport"}' http://127.0.0.1:9998/jsonrpc` | `standards` list should include the configured `HDR_SUPPORT` values and `success` should be `true` |

---

<a id="check_tv_hdr_support"></a>
### TestCase Name
Check_TV_HDR_Support

### TestCase ID
DS_06

### TestCase Objective
Check whether TV has HDR support or not

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get TV HDR Support Details | Invoke getTvHDRSupport on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getTvHDRSupport"}' http://127.0.0.1:9998/jsonrpc` | `TVSUPPORTSHDR` should be `True` or `False` |

---

<a id="read_host_edid"></a>
### TestCase Name
Read_Host_EDID

### TestCase ID
DS_07

### TestCase Objective
Check the EDID status of host

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Host EDID Details | Invoke readHostEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readHostEDID"}' http://127.0.0.1:9998/jsonrpc` | `EDID` field should be a non-empty base64-encoded string and `success` should be `true` |

---

<a id="read_connected_device_edid"></a>
### TestCase Name
Read_Connected_Device_EDID

### TestCase ID
DS_08

### TestCase Objective
Check the EDID status of connected device

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Connected Device  EDID Details | Invoke readEDID on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.readEDID"}' http://127.0.0.1:9998/jsonrpc` | `EDID` field should be a non-empty base64-encoded string and `success` should be `true` |

---

<a id="set_and_get_supported_audio_modes_hdmi0"></a>
### TestCase Name
Set_And_Get_Supported_Audio_Modes_HDMI0

### TestCase ID
DS_09

### TestCase Objective
Check whether supported audio modes are able to set HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 3 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `supportedAudioModes` list should be non-empty and `success` should be `true` |
| 4 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should be one of the modes returned in `supportedAudioModes` from step 3 and `success` should be `true` |
| 5 | Set Sound Mode (iterate each mode) | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "HDMI0", soundMode: "<each_supported_mode>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "HDMI0", "soundMode": "<each_supported_mode>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 6 | Get Sound Mode (verify after each set) | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should match the mode set in the corresponding iteration of step 5 |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_Sound_Mode

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Sound Mode | Get Sound Mode from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should match the original value recorded in step 4; if it already matches, no revert is required |

---

<a id="set_and_get_zoom_settings"></a>
### TestCase Name
Set_And_Get_Zoom_Settings

### TestCase ID
DS_10

### TestCase Objective
Check whether supported zoom modes are able to set and get

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Zoom Setting | Invoke getZoomSetting on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getZoomSetting"}' http://127.0.0.1:9998/jsonrpc` | `zoomSetting` should match one of the configured `ZOOM_SETTINGS` values and `success` should be `true` |
| 2 | Set Zoom Setting | Invoke setZoomSetting on org.rdk.DisplaySettings with zoomSetting: "<ZOOM_SETTINGS>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setZoomSetting", "params": {"zoomSetting": "<ZOOM_SETTINGS>"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 3 | Get Zoom Setting | Invoke getZoomSetting on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getZoomSetting"}' http://127.0.0.1:9998/jsonrpc` | `zoomSetting` should match the value set in step 2 |
| 4 | Check Zoom Settings Updated Change Event | Listen for event Event_Zoom_Settings_Updated | `onZoomSettingsUpdated` event should be received with `zoomSetting` matching the value set in step 2 |

---

<a id="set_and_get_videoport_status_instandby_negative_case"></a>
### TestCase Name
Set_And_Get_VideoPort_Status_InStandby_Negative_Case

### TestCase ID
DS_11

### TestCase Objective
Checks the negative scenario for video port status in standby

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get VideoPort Status InStandby | Invoke getVideoPortStatusInStandby on org.rdk.DisplaySettings with portName: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVideoPortStatusInStandby", "params": {"portName": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Unknown method.` |
| 3 | Set VideoPort Status InStandby | Invoke setVideoPortStatusInStandby on org.rdk.DisplaySettings with portName: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVideoPortStatusInStandby", "params": {"portName": "<result_step_1>", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Unknown method.` |

---

<a id="set_and_get_ms12_audio_compression"></a>
### TestCase Name
Set_And_Get_MS12_Audio_Compression

### TestCase ID
DS_12

### TestCase Objective
Check whether MS12 audio compression values are able to set and get

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get MS12 Audio Compression | Invoke getMS12AudioCompression on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMS12AudioCompression"}' http://127.0.0.1:9998/jsonrpc` | `compressionlevel` should be a valid integer in the range `0–10` and `success` should be `true` |
| 2 | Set MS12 Audio Compression (iterate each value) | Invoke setMS12AudioCompression on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMS12AudioCompression", "params": {"compresionLevel": <compression_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each compression level set |
| 3 | Get MS12 Audio Compression (verify after each set) | Invoke getMS12AudioCompression on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMS12AudioCompression"}' http://127.0.0.1:9998/jsonrpc` | `compressionlevel` should match the value set in the corresponding iteration of step 2 and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_MS12_Audio_Compression

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set MS12 Audio Compression | Set MS12Audio Compression on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMS12AudioCompression", "params": {"compresionLevel": <original_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 2 | Get MS12 Audio Compression | Get MS12Audio Compression from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMS12AudioCompression"}' http://127.0.0.1:9998/jsonrpc` | `compressionlevel` should match the original value recorded in step 1 and `success` should be `true` |

---

<a id="check_current_output_settings"></a>
### TestCase Name
Check_Current_Output_Settings

### TestCase ID
DS_13

### TestCase Objective
Check the current output settings of device

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Current Output Settings | Invoke getCurrentOutputSettings on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentOutputSettings"}' http://127.0.0.1:9998/jsonrpc` | `colorSpace` should be in `[0,1,2,3,4,5]`, `matrixCoefficients` should be in `[0,1,2,3,4,5,6,7]`, and `success` should be `true` |

---

<a id="check_active_input_value"></a>
### TestCase Name
Check_Active_Input_Value

### TestCase ID
DS_14

### TestCase Objective
Check the active input value

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Get Active Input | Invoke getActiveInput on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput"}' http://127.0.0.1:9998/jsonrpc` | `activeInput` should be `True` or `False` and `success` should be `true` |

---

<a id="setandget_all_supported_resolutions"></a>
### TestCase Name
SetAndGet_All_Supported_Resolutions

### TestCase ID
DS_15

### TestCase Objective
Set and get all the supported resolution by both TV and STB, also checks for the resolution changed event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` (record this value for post-condition revert) |
| 4 | Retrieve Current Resolution (per iteration) | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should reflect the currently active resolution and `success` should be `true` |
| 5 | Set Resolution (iterate each supported resolution) | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<each_supported_resolution>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<each_supported_resolution>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each resolution set |
| 6 | Get Resolution (verify after each set) | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should match the value set in the corresponding iteration of step 5 and `success` should be `true` |
| 7 | Check Resolution Changed Event | *(Conditional statement executed only if previous step condition is met)*<br>Listen for event Event_Resolution_Changed after each setCurrentResolution call in step 5 | `onResolutionChanged` event should be received with `resolution` matching the value set in step 5 |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_Resolution

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Resolution | Set Current Resolution on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<original_resolution>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 2 | Get Current Resolution | Get Current Resolution from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should match the original value recorded in step 3 and `success` should be `true` |

---

<a id="enable_and_disable_dolby_volume_mode"></a>
### TestCase Name
Enable_And_Disable_Dolby_Volume_Mode

### TestCase ID
DS_16

### TestCase Objective
Check whether dolby volume mode can enable and disable

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dolby Volume Mode | Invoke getDolbyVolumeMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDolbyVolumeMode"}' http://127.0.0.1:9998/jsonrpc` | `dolbyVolumeMode` should be `true` or `false` and `success` should be `true` |
| 2 | Set Dolby Volume Mode (iterate each value) | Invoke setDolbyVolumeMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDolbyVolumeMode", "params": {"dolbyVolumeMode": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 3 | Get Dolby Volume Mode (verify after each set) | Invoke getDolbyVolumeMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDolbyVolumeMode"}' http://127.0.0.1:9998/jsonrpc` | `dolbyVolumeMode` should match the value set in the corresponding iteration of step 2 and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Revert_Dolby_Volume_Mode

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Dolby Volume Mode | Set Dolby Volume Mode on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDolbyVolumeMode", "params": {"dolbyVolumeMode": <original_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |

---

<a id="set_and_get_dialog_enhancement"></a>
### TestCase Name
Set_And_Get_Dialog_Enhancement

### TestCase ID
DS_17

### TestCase Objective
Check whether dialog enhancement values are able to set and get

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dialog Enhancement | Invoke getDialogEnhancement on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDialogEnhancement"}' http://127.0.0.1:9998/jsonrpc` | `enhancerlevel` should be a valid integer and `success` should be `true` |
| 2 | Set Dialog Enhancement (iterate each level) | Invoke setDialogEnhancement on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDialogEnhancement", "params": {"enhancerlevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each level set |
| 3 | Get Dialog Enhancement (verify after each set) | Invoke getDialogEnhancement on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDialogEnhancement"}' http://127.0.0.1:9998/jsonrpc` | `enhancerlevel` should match the value set in the corresponding iteration of step 2 and `success` should be `true` |

---

<a id="set_and_get_intelligent_equalizer_mode"></a>
### TestCase Name
Set_And_Get_Intelligent_Equalizer_Mode

### TestCase ID
DS_18

### TestCase Objective
Check whether intelligent equalizer mode values are able to set and get

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Intelligent Equalizer Mode | Invoke getIntelligentEqualizerMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getIntelligentEqualizerMode"}' http://127.0.0.1:9998/jsonrpc` | `intelligentEqualizerMode` should be a valid integer and `success` should be `true` |
| 2 | Set Intelligent Equalizer Mode (iterate each mode) | Invoke setIntelligentEqualizerMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setIntelligentEqualizerMode", "params": {"intelligentEqualizerMode": <each_mode>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 3 | Get Intelligent Equalizer Mode (verify after each set) | Invoke getIntelligentEqualizerMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getIntelligentEqualizerMode"}' http://127.0.0.1:9998/jsonrpc` | `intelligentEqualizerMode` should match the value set in the corresponding iteration of step 2 and `success` should be `true` |

---

<a id="set_and_get_volume_leveller_hdmi0"></a>
### TestCase Name
Set_And_Get_Volume_Leveller_HDMI0

### TestCase ID
DS_19

### TestCase Objective
Check whether volume values are able to set and get for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |
| 3 | Set Volume Leveller (iterate each level) | Invoke setVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLeveller", "params": {"audioPort": "HDMI0", "level": <each_level_value>, "mode": 1}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each level set |
| 4 | Get Volume Leveller (verify after each set) | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_drc_mode_hdmi0"></a>
### TestCase Name
Set_And_Get_DRC_Mode_HDMI0

### TestCase ID
DS_20

### TestCase Objective
Check whether DRC mode values are able to set and get for HDMI0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get DRC Mode | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should be `0` (line) or `1` (rf) and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set DRC Mode (iterate each mode) | Invoke setDRCMode on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDRCMode", "params": {"audioPort": "HDMI0", "DRCMode": <each_drc_mode>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 4 | Get DRC Mode (verify after each set) | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_level_hdmi0"></a>
### TestCase Name
Set_And_Get_Volume_Level_HDMI0

### TestCase ID
DS_21

### TestCase Objective
Check whether volume level values are able to set and get for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set Volume Level (iterate each value) | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each volume level set |
| 4 | Get Volume Level (verify after each set) | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_gain_hdmi0"></a>
### TestCase Name
Set_And_Get_Gain_HDMI0

### TestCase ID
DS_22

### TestCase Objective
Check whether audio port gain values are able to set and get for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Gain | Invoke getGain on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should be a valid float and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set Gain (iterate each value) | Invoke setGain on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setGain", "params": {"audioPort": "HDMI0", "gain": <each_gain_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each gain value set |
| 4 | Get Gain (verify after each set) | Invoke getGain on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="mute_and_unmute_audio_hdmi0"></a>
### TestCase Name
Mute_And_Unmute_Audio_HDMI0

### TestCase ID
DS_23

### TestCase Objective
Check whether audio is able to mute and unmute  for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (iterate each value) | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Muted (verify after each set) | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_hdmi0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_HDMI0

### TestCase ID
DS_24

### TestCase Objective
Check whether audio delay values are able to set and get for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay (iterate each value) | Invoke setAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelay", "params": {"audioPort": "HDMI0", "audioDelay": <each_delay_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each delay value set |
| 4 | Get Audio Delay (verify after each set) | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_offset_hdmi0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_Offset_HDMI0

### TestCase ID
DS_25

### TestCase Objective
Check whether audio delay offset values are able to set and get for HDMI0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Audio Delay Offset | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay Offset (iterate each value) | Invoke setAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelayOffset", "params": {"audioPort": "HDMI0", "audioDelayOffset": <each_offset_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each offset value set |
| 4 | Get Audio Delay Offset (verify after each set) | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="check_sink_atmos_capability"></a>
### TestCase Name
Check_Sink_Atmos_Capability

### TestCase ID
DS_26

### TestCase Objective
Check the the Atmos capability of the sink

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Sink Atmos Capability | Invoke getSinkAtmosCapability on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSinkAtmosCapability"}' http://127.0.0.1:9998/jsonrpc` | `atmos_capability` should be a valid integer (`0`, `1`, or `2`) and `success` should be `true` |

---

<a id="enable_disable_audio_atmos_output_mode"></a>
### TestCase Name
Enable_Disable_Audio_Atmos_Output_Mode

### TestCase ID
DS_27

### TestCase Objective
Check whether audio atmos output mode is possile to enable and disable

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable/Disable Audio Atmos Output Mode (iterate each value) | Invoke setAudioAtmosOutputMode on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioAtmosOutputMode", "params": {"enable": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each enable/disable value set |

---

<a id="get_tv_hdr_capabilities"></a>
### TestCase Name
Get_TV_HDR_Capabilities

### TestCase ID
DS_28

### TestCase Objective
Check the HDR capabilities of TV

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get TV HDR Capabilities | Invoke getTVHDRCapabilities on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getTVHDRCapabilities"}' http://127.0.0.1:9998/jsonrpc` | `capabilities` should be a valid integer bitmask and `success` should be `true` |

---

<a id="is_connected_device_repeater"></a>
### TestCase Name
Is_Connected_Device_Repeater

### TestCase ID
DS_29

### TestCase Objective
Check whether connected device is a repeater

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Is Connected Device Repeater | Invoke isConnectedDeviceRepeater on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.isConnectedDeviceRepeater"}' http://127.0.0.1:9998/jsonrpc` | `isDeviceRepeater` should be `true` or `false` and `success` should be `true` |

---

<a id="get_default_resolution"></a>
### TestCase Name
Get_Default_Resolution

### TestCase ID
DS_30

### TestCase Objective
Check whether the default resolution is available in supported resolutions

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Default Resolution | Invoke getDefaultResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | `defaultResolution` should be present in the `supportedResolutions` list from step 2 and `success` should be `true` |

---

<a id="set_and_get_supported_audio_modes_spdif0"></a>
### TestCase Name
Set_And_Get_Supported_Audio_Modes_SPDIF0

### TestCase ID
DS_31

### TestCase Objective
Check whether supported audio modes are able to set for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 3 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `supportedAudioModes` list should be non-empty and `success` should be `true` |
| 4 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should be one of the modes returned in `supportedAudioModes` from step 3 and `success` should be `true` |
| 5 | Set Sound Mode (iterate each mode) | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "SPDIF0", soundMode: "<each_supported_mode>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "SPDIF0", "soundMode": "<each_supported_mode>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 6 | Get Sound Mode (verify after each set) | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should match the mode set in the corresponding iteration of step 5 and `success` should be `true` |

---

<a id="set_and_get_supported_audio_modes_idlr0"></a>
### TestCase Name
Set_And_Get_Supported_Audio_Modes_IDLR0

### TestCase ID
DS_32

### TestCase Objective
Check whether supported audio modes are able to set for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 3 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `supportedAudioModes` list should be non-empty and `success` should be `true` |
| 4 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should be one of the modes returned in `supportedAudioModes` from step 3 and `success` should be `true` |
| 5 | Set Sound Mode (iterate each mode) | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "IDLR0", soundMode: "<each_supported_mode>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "IDLR0", "soundMode": "<each_supported_mode>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 6 | Get Sound Mode (verify after each set) | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should match the mode set in the corresponding iteration of step 5 and `success` should be `true` |

---

<a id="set_and_get_supported_audio_modes_speaker0"></a>
### TestCase Name
Set_And_Get_Supported_Audio_Modes_SPEAKER0

### TestCase ID
DS_33

### TestCase Objective
Check whether supported audio modes are able to set for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 3 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `supportedAudioModes` list should be non-empty and `success` should be `true` |
| 4 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should be one of the modes returned in `supportedAudioModes` from step 3 and `success` should be `true` |
| 5 | Set Sound Mode (iterate each mode) | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0", soundMode: "<each_supported_mode>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "SPEAKER0", "soundMode": "<each_supported_mode>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 6 | Get Sound Mode (verify after each set) | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `soundMode` should match the mode set in the corresponding iteration of step 5 and `success` should be `true` |

---

<a id="set_and_get_volume_leveller_spdif0"></a>
### TestCase Name
Set_And_Get_Volume_Leveller_SPDIF0

### TestCase ID
DS_34

### TestCase Objective
Check whether volume values are able to set and get for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |
| 3 | Set Volume Leveller (iterate each level) | Invoke setVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLeveller", "params": {"audioPort": "SPDIF0", "level": <each_level_value>, "mode": 1}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each level set |
| 4 | Get Volume Leveller (verify after each set) | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_leveller_idlr0"></a>
### TestCase Name
Set_And_Get_Volume_Leveller_IDLR0

### TestCase ID
DS_35

### TestCase Objective
Check whether volume values are able to set and get for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |
| 3 | Set Volume Leveller (iterate each level) | Invoke setVolumeLeveller on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLeveller", "params": {"audioPort": "IDLR0", "level": <each_level_value>, "mode": 1}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each level set |
| 4 | Get Volume Leveller (verify after each set) | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_leveller_speaker0"></a>
### TestCase Name
Set_And_Get_Volume_Leveller_SPEAKER0

### TestCase ID
DS_36

### TestCase Objective
Check whether volume values are able to set and get for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |
| 3 | Set Volume Leveller (iterate each level) | Invoke setVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLeveller", "params": {"audioPort": "SPEAKER0", "level": <each_level_value>, "mode": 1}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each level set |
| 4 | Get Volume Leveller (verify after each set) | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_drc_mode_spdif0"></a>
### TestCase Name
Set_And_Get_DRC_Mode_SPDIF0

### TestCase ID
DS_37

### TestCase Objective
Check whether DRC mode values are able to set and get for SPDIF0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get DRC Mode | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should be `0` (line) or `1` (rf) and `success` should be `true` |
| 3 | Set DRC Mode (iterate each mode) | Invoke setDRCMode on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDRCMode", "params": {"audioPort": "SPDIF0", "DRCMode": <each_drc_mode>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 4 | Get DRC Mode (verify after each set) | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_drc_mode_idlr0"></a>
### TestCase Name
Set_And_Get_DRC_Mode_IDLR0

### TestCase ID
DS_38

### TestCase Objective
Check whether DRC mode values are able to set and get for IDLR0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get DRC Mode | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should be `0` (line) or `1` (rf) and `success` should be `true` |
| 3 | Set DRC Mode (iterate each mode) | Invoke setDRCMode on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDRCMode", "params": {"audioPort": "IDLR0", "DRCMode": <each_drc_mode>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 4 | Get DRC Mode (verify after each set) | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_drc_mode_speaker0"></a>
### TestCase Name
Set_And_Get_DRC_Mode_SPEAKER0

### TestCase ID
DS_39

### TestCase Objective
Check whether DRC mode values are able to set and get for SPEAKER0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get DRC Mode | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should be `0` (line) or `1` (rf) and `success` should be `true` |
| 3 | Set DRC Mode (iterate each mode) | Invoke setDRCMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setDRCMode", "params": {"audioPort": "SPEAKER0", "DRCMode": <each_drc_mode>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 4 | Get DRC Mode (verify after each set) | Invoke getDRCMode on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDRCMode", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `DRCMode` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_level_spdif0"></a>
### TestCase Name
Set_And_Get_Volume_Level_SPDIF0

### TestCase ID
DS_40

### TestCase Objective
Check whether volume level values are able to set and get for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set Volume Level (iterate each value) | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "SPDIF0", "volumeLevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each volume level set |
| 4 | Get Volume Level (verify after each set) | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_level_idlr0"></a>
### TestCase Name
Set_And_Get_Volume_Level_IDLR0

### TestCase ID
DS_41

### TestCase Objective
Check whether volume level values are able to set and get for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set Volume Level (iterate each value) | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "IDLR0", "volumeLevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each volume level set |
| 4 | Get Volume Level (verify after each set) | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_volume_level_speaker0"></a>
### TestCase Name
Set_And_Get_Volume_Level_SPEAKER0

### TestCase ID
DS_42

### TestCase Objective
Check whether volume level values are able to set and get for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value for post-condition revert) |
| 3 | Set Volume Level (iterate each value) | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "SPEAKER0", "volumeLevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each volume level set |
| 4 | Get Volume Level (verify after each set) | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_gain_spdif0"></a>
### TestCase Name
Set_And_Get_Gain_SPDIF0

### TestCase ID
DS_43

### TestCase Objective
Check whether audio port gain values are able to set and get for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Gain | Invoke getGain on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should be a valid float and `success` should be `true` |
| 3 | Set Gain (iterate each value) | Invoke setGain on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setGain", "params": {"audioPort": "SPDIF0", "gain": <each_gain_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each gain value set |
| 4 | Get Gain (verify after each set) | Invoke getGain on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_gain_idlr0"></a>
### TestCase Name
Set_And_Get_Gain_IDLR0

### TestCase ID
DS_44

### TestCase Objective
Check whether audio port gain values are able to set and get for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Gain | Invoke getGain on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should be a valid float and `success` should be `true` |
| 3 | Set Gain (iterate each value) | Invoke setGain on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setGain", "params": {"audioPort": "IDLR0", "gain": <each_gain_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each gain value set |
| 4 | Get Gain (verify after each set) | Invoke getGain on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_gain_speaker0"></a>
### TestCase Name
Set_And_Get_Gain_SPEAKER0

### TestCase ID
DS_45

### TestCase Objective
Check whether audio port gain values are able to set and get for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Gain | Invoke getGain on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should be a valid float and `success` should be `true` |
| 3 | Set Gain (iterate each value) | Invoke setGain on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setGain", "params": {"audioPort": "SPEAKER0", "gain": <each_gain_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each gain value set |
| 4 | Get Gain (verify after each set) | Invoke getGain on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getGain", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `gain` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="mute_and_unmute_audio_spdif0"></a>
### TestCase Name
Mute_And_Unmute_Audio_SPDIF0

### TestCase ID
DS_46

### TestCase Objective
Check whether audio is able to mute and unmute for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (iterate each value) | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "SPDIF0", "muted": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Muted (verify after each set) | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="mute_and_unmute_audio_idlr0"></a>
### TestCase Name
Mute_And_Unmute_Audio_IDLR0

### TestCase ID
DS_47

### TestCase Objective
Check whether audio is able to mute and unmute for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (iterate each value) | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "IDLR0", "muted": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Muted (verify after each set) | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="mute_and_unmute_audio_speaker0"></a>
### TestCase Name
Mute_And_Unmute_Audio_SPEAKER0

### TestCase ID
DS_48

### TestCase Objective
Check whether audio is able to mute and unmute for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (iterate each value) | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "SPEAKER0", "muted": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Muted (verify after each set) | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_spdif0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_SPDIF0

### TestCase ID
DS_49

### TestCase Objective
Check whether audio delay values are able to set and get for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay (iterate each value) | Invoke setAudioDelay on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelay", "params": {"audioPort": "SPDIF0", "audioDelay": <each_delay_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each delay value set |
| 4 | Get Audio Delay (verify after each set) | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_idlr0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_IDLR0

### TestCase ID
DS_50

### TestCase Objective
Check whether audio delay values are able to set and get for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay (iterate each value) | Invoke setAudioDelay on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelay", "params": {"audioPort": "IDLR0", "audioDelay": <each_delay_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each delay value set |
| 4 | Get Audio Delay (verify after each set) | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_speaker0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_SPEAKER0

### TestCase ID
DS_51

### TestCase Objective
Check whether audio delay values are able to set and get for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay (iterate each value) | Invoke setAudioDelay on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelay", "params": {"audioPort": "SPEAKER0", "audioDelay": <each_delay_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each delay value set |
| 4 | Get Audio Delay (verify after each set) | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_offset_spdif0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_Offset_SPDIF0

### TestCase ID
DS_52

### TestCase Objective
Check whether audio delay offset values are able to set and get for SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Audio Delay Offset | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay Offset (iterate each value) | Invoke setAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelayOffset", "params": {"audioPort": "SPDIF0", "audioDelayOffset": <each_offset_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each offset value set |
| 4 | Get Audio Delay Offset (verify after each set) | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_offset_idlr0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_Offset_IDLR0

### TestCase ID
DS_53

### TestCase Objective
Check whether audio delay offset values are able to set and get for IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Audio Delay Offset | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay Offset (iterate each value) | Invoke setAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelayOffset", "params": {"audioPort": "IDLR0", "audioDelayOffset": <each_offset_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each offset value set |
| 4 | Get Audio Delay Offset (verify after each set) | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_and_get_audio_delay_offset_speaker0"></a>
### TestCase Name
Set_And_Get_Audio_Delay_Offset_SPEAKER0

### TestCase ID
DS_54

### TestCase Objective
Check whether audio delay offset values are able to set and get for SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Audio Delay Offset | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay Offset (iterate each value) | Invoke setAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelayOffset", "params": {"audioPort": "SPEAKER0", "audioDelayOffset": <each_offset_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each offset value set |
| 4 | Get Audio Delay Offset (verify after each set) | Invoke getAudioDelayOffset on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelayOffset", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelayOffset` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="enable_and_disable_audioport_hdmi0"></a>
### TestCase Name
Enable_And_Disable_AudioPort_HDMI0

### TestCase ID
DS_55

### TestCase Objective
Check whether able to enable and disable HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should be `true` or `false` and `success` should be `true` |
| 3 | Set Enable Audio Port (iterate each value) | Invoke setEnableAudioPort on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setEnableAudioPort", "params": {"audioPort": "HDMI0", "enable": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each enable/disable value set |
| 4 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should match the value set in the previous `setEnableAudioPort` call and `success` should be `true` |

---

<a id="enable_and_disable_audioport_spdif0"></a>
### TestCase Name
Enable_And_Disable_AudioPort_SPDIF0

### TestCase ID
DS_56

### TestCase Objective
Check whether able to enable and disable SPDIF0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPDIF0` and `success` should be `true` |
| 2 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should be `true` or `false` and `success` should be `true` |
| 3 | Set Enable Audio Port (iterate each value) | Invoke setEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setEnableAudioPort", "params": {"audioPort": "SPDIF0", "enable": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each enable/disable value set |
| 4 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPDIF0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "SPDIF0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should match the value set in the previous `setEnableAudioPort` call and `success` should be `true` |

---

<a id="enable_and_disable_audioport_idlr0"></a>
### TestCase Name
Enable_And_Disable_AudioPort_IDLR0

### TestCase ID
DS_57

### TestCase Objective
Check whether able to enable and disable IDLR0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `IDLR0` and `success` should be `true` |
| 2 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should be `true` or `false` and `success` should be `true` |
| 3 | Set Enable Audio Port (iterate each value) | Invoke setEnableAudioPort on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setEnableAudioPort", "params": {"audioPort": "IDLR0", "enable": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each enable/disable value set |
| 4 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "IDLR0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "IDLR0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should match the value set in the previous `setEnableAudioPort` call and `success` should be `true` |

---

<a id="enable_and_disable_audioport_speaker0"></a>
### TestCase Name
Enable_And_Disable_AudioPort_SPEAKER0

### TestCase ID
DS_58

### TestCase Objective
Check whether able to enable and disable SPEAKER0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `SPEAKER0` and `success` should be `true` |
| 2 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should be `true` or `false` and `success` should be `true` |
| 3 | Set Enable Audio Port (iterate each value) | Invoke setEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setEnableAudioPort", "params": {"audioPort": "SPEAKER0", "enable": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each enable/disable value set |
| 4 | Get Enable Audio Port | Invoke getEnableAudioPort on org.rdk.DisplaySettings with audioPort: "SPEAKER0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getEnableAudioPort", "params": {"audioPort": "SPEAKER0"}}' http://127.0.0.1:9998/jsonrpc` | `enable` should match the value set in the previous `setEnableAudioPort` call and `success` should be `true` |

---

<a id="check_settop_audio_capabilities_hdmi0"></a>
### TestCase Name
Check_Settop_Audio_Capabilities_HDMI0

### TestCase ID
DS_59

### TestCase Objective
Check whether settop displays all supported audio capabilities

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Settop Audio Capabilities | Invoke getSettopAudioCapabilities on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSettopAudioCapabilities", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioCapabilities` list should match the configured `SETTOP_SUPPORTED_AUDIO_CAPABILITIES` values and `success` should be `true` |

---

<a id="check_settop_ms12_capabilities_hdmi0"></a>
### TestCase Name
Check_Settop_MS12_Capabilities_HDMI0

### TestCase ID
DS_60

### TestCase Objective
Check whether settop displays all supported MS12 capabilities

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Settop MS12 Capabilities | Invoke getSettopMS12Capabilities on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSettopMS12Capabilities", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `ms12Capabilities` list should match the configured `SETTOP_SUPPORTED_MS12_CAPABILITIES` values and `success` should be `true` |

---

<a id="set_and_get_volume_leveller_modes_hdmi0"></a>
### TestCase Name
Set_And_Get_Volume_Leveller_Modes_HDMI0

### TestCase ID
DS_61

### TestCase Objective
Check whether able to enables or disables volume leveling for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |
| 3 | Set Volume Leveller (iterate each mode) | Invoke setVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLeveller", "params": {"audioPort": "HDMI0", "mode": <each_mode>, "level": 10}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each mode set |
| 4 | Get Volume Leveller | Invoke getVolumeLeveller on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLeveller", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `level` should be in range `[0, 10]`, `mode` should be in `[0, 1, 2]`, and `success` should be `true` |

---

<a id="check_supported_resolutions"></a>
### TestCase Name
Check_Supported_Resolutions

### TestCase ID
DS_62

### TestCase Objective
Checks whether the supported resolutions list contains the common resolutions present in the supported TV and Settop resolutions

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Tv Resolutions | Invoke getSupportedTvResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedTvResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list for TV should be non-empty and `success` should be `true` |
| 3 | Get Settop Supported Resolutions | Invoke getSupportedSettopResolutions on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedSettopResolutions"}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list for settop should match the configured `SETTOP_SUPPORTED_RESOLUTIONS` values and `success` should be `true` |
| 4 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should contain only the common resolutions present in both TV and settop supported resolution lists from steps 2 and 3 |

---

<a id="check_active_input_value_for_invalid_display"></a>
### TestCase Name
Check_Active_Input_Value_For_Invalid_Display

### TestCase ID
DS_63

### TestCase Objective
Checks the active input value for invalid video display

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Get Active Input | Invoke getActiveInput on org.rdk.DisplaySettings with videoDisplay: "Invalid0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getActiveInput", "params": {"videoDisplay": "Invalid0"}}' http://127.0.0.1:9998/jsonrpc` | Expected `False` |

---

<a id="check_videoport_standby_status_for_invalid_display"></a>
### TestCase Name
Check_VideoPort_Standby_Status_For_Invalid_Display

### TestCase ID
DS_64

### TestCase Objective
Checks the video port standby status for invalid display

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get VideoPort Status InStandby | Invoke getVideoPortStatusInStandby on org.rdk.DisplaySettings with portName: "Invalid0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVideoPortStatusInStandby", "params": {"portName": "Invalid0"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Unknown method.` |
| 2 | Set VideoPort Status InStandby | Invoke setVideoPortStatusInStandby on org.rdk.DisplaySettings with portName: "Invalid0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVideoPortStatusInStandby", "params": {"portName": "Invalid0", "enabled": true}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error message `Unknown method.` |

---

<a id="set_and_get_negative_audio_delay"></a>
### TestCase Name
Set_And_Get_Negative_Audio_Delay

### TestCase ID
DS_65

### TestCase Objective
Check whether audio delay api accepts negative values

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `audioDelay` should be a valid integer and `success` should be `true` |
| 3 | Set Audio Delay | Invoke setAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0", audioDelay: "-10,-50,-100"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAudioDelay", "params": {"audioPort": "HDMI0", "audioDelay": "-10,-50,-100"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Audio Delay | Invoke getAudioDelay on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioDelay", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `defaultResolution` should be present in the `supportedResolutions` list from step 2 and `success` should be `true` |

---

<a id="check_supported_audio_modes_without_audio_port"></a>
### TestCase Name
Check_Supported_Audio_Modes_Without_Audio_Port

### TestCase ID
DS_66

### TestCase Objective
Validates the results of supported audio modes without passing audio port parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 3 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes"}' http://127.0.0.1:9998/jsonrpc` | `supportedAudioModes` list should be non-empty and `success` should be `true` |

---

<a id="check_current_and_supported_video_formats"></a>
### TestCase Name
Check_Current_And_Supported_Video_Formats

### TestCase ID
DS_67

### TestCase Objective
Checks the current and supported video formats

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Video Formats | Invoke getVideoFormat on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVideoFormat"}' http://127.0.0.1:9998/jsonrpc` | `currentVideoFormat` and `supportedVideoFormat` list should be non-empty and `success` should be `true` |

---

<a id="check_current_and_supported_audio_formats"></a>
### TestCase Name
Check_Current_And_Supported_Audio_Formats

### TestCase ID
DS_68

### TestCase Objective
Checks the current and supported audio formats

### TestCase Pre-condition

#### TestCase Pre-condition 1: Get_Display_Connected_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Get Connected Video Displays from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Audio Formats | Invoke getAudioFormat on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAudioFormat"}' http://127.0.0.1:9998/jsonrpc` | `currentAudioFormat` and `supportedAudioFormat` list should be non-empty and `success` should be `true` |

---

<a id="check_resolution_persisted_after_reboot"></a>
### TestCase Name
Check_Resolution_Persisted_After_Reboot

### TestCase ID
DS_69

### TestCase Objective
Checks whether resolution persisted after reboot if persist set as true

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 4 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2,3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2,3>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 5 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag `system_check_set_operation` |
| 6 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |

---

<a id="check_resolution_not_persisted_after_reboot"></a>
### TestCase Name
Check_Resolution_Not_Persisted_After_Reboot

### TestCase ID
DS_70

### TestCase Objective
Checks whether resolution not persisted after reboot if persist set as false

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 4 | Get Default Resolution | Invoke getDefaultResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDefaultResolution"}' http://127.0.0.1:9998/jsonrpc` | `defaultResolution` should be present in the `supportedResolutions` list from step 2 and `success` should be `true` |
| 5 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2,3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2,3>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 6 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag `system_check_set_operation` |
| 7 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | Expected `compared against value from step 4` |

---

<a id="setandget_supported_color_depth_capabilities"></a>
### TestCase Name
SetAndGet_Supported_Color_Depth_Capabilities

### TestCase ID
DS_71

### TestCase Objective
Set and get all the supported color depth capabilities

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Color Depth Capabilities | Invoke getColorDepthCapabilities on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getColorDepthCapabilities"}' http://127.0.0.1:9998/jsonrpc` | `supportedColorDepth` list should be non-empty and `success` should be `true` |
| 3 | Get Preferred Color Depth | Invoke getPreferredColorDepth on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getPreferredColorDepth", "params": {"videoDisplay": "<result_step_1>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `colorDepth` should be a valid string from the supported list and `success` should be `true` |
| 4 | Set Preferred Color Depth | Invoke setPreferredColorDepth on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", colorDepth: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setPreferredColorDepth", "params": {"videoDisplay": "<result_step_1>", "colorDepth": "<result_step_2>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 5 | Get Color Depth Capabilities | Invoke getColorDepthCapabilities on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getColorDepthCapabilities"}' http://127.0.0.1:9998/jsonrpc` | `supportedColorDepth` list should be non-empty and `success` should be `true` |

---

<a id="check_resolution_prechange_event"></a>
### TestCase Name
Check_Resolution_PreChange_Event

### TestCase ID
DS_72

### TestCase Objective
Set and get all the supported resolution by both TV and STB, also checks for the resolution prechanged event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 4 | Retrieve Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 5 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 6 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 7 | Check Resolution PreChange Event | *(Conditional statement executed only if previous step condition is met)*<br>Listen for event Event_Resolution_PreChange | Verify that event data is validated successfully |
| 8 | Check Resolution PreChange Event | *(Conditional statement executed only if previous step condition is met)*<br>Listen for event Event_Resolution_PreChange | Verify that event data is validated successfully |

---

<a id="check_resolution_persisted_for_30seconds_after_reboot"></a>
### TestCase Name
Check_Resolution_Persisted_For_30Seconds_After_Reboot

### TestCase ID
DS_73

### TestCase Objective
Checks whether resolution persisted for 30 seconds after reboot if persist set as true

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `supportedResolutions` list should be non-empty and `success` should be `true` |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |
| 4 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2,3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2,3>", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 5 | System reboot | Invoke reboot on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.reboot"}' http://127.0.0.1:9998/jsonrpc` | Validation succeeded using method tag `system_check_set_operation` |
| 6 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution"}' http://127.0.0.1:9998/jsonrpc` | `resolution` should be a valid resolution string and `success` should be `true` |

---

<a id="check_mute_status_changed_event_hdmi0"></a>
### TestCase Name
Check_Mute_Status_Changed_Event_HDMI0

### TestCase ID
DS_74

### TestCase Objective
Check whether audio is able to mute and unmute  for HDMI0 port and check Mute status changed event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (iterate each value) | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Muted (verify after each set) | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |
| 5 | Check MuteStatus Changed Event | Listen for event Event_MuteStatus_Changed after each setMuted call in step 3 | `onMuteStatusChanged` event should be received with `muted` matching the value set in step 3 |

---

<a id="check_volume_level_changed_event_hdmi0"></a>
### TestCase Name
Check_Volume_Level_Changed_Event_HDMI0

### TestCase ID
DS_75

### TestCase Objective
Check whether volume level values are able to set and get for HDMI0 port and check for volume level changed event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Set Volume Level (iterate each value) | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": <each_level>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each volume level set |
| 3 | Get Volume Level (verify after each set) | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should match the value set in the corresponding iteration of step 2 and `success` should be `true` |
| 4 | Check VolumeLevel Changed Event | Listen for event Event_VolumeLevel_Changed after each setVolumeLevel call in step 2 | `onVolumeLevelChanged` event should be received with `volumeLevel` matching the value set in step 2 |

---

<a id="set_and_get_negative_volume_level_hdmi0"></a>
### TestCase Name
Set_And_Get_Negative_Volume_Level_HDMI0

### TestCase ID
DS_76

### TestCase Objective
Check whether negative volume level values are able to set and get for HDMI0 port

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Set Volume Level | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0", volumeLevel: "-10,-25,-50,-100"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": "-10,-25,-50,-100"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 3 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` |

---

<a id="set_and_get_fader_control_hdmi0"></a>
### TestCase Name
Set_and_Get_Fader_Control_HDMI0

### TestCase ID
DS_77

### TestCase Objective
Checks if able to set and get the mixerbalance betweeen main and associated audio

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Fader Control | Invoke getFaderControl on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getFaderControl", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `mixerBalance` should be a valid integer in range `[-32, 32]` and `success` should be `true` |
| 3 | Set Fader Control (iterate each value) | Invoke setFaderControl on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setFaderControl", "params": {"audioPort": "HDMI0", "mixerBalance": <each_balance_value>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each balance value set |
| 4 | Get Fader Control (verify after each set) | Invoke getFaderControl on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getFaderControl", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `mixerBalance` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="set_empty_fader_control_hdmi0"></a>
### TestCase Name
Set_Empty_Fader_Control_HDMI0

### TestCase ID
DS_78

### TestCase Objective
Checks if able to set the mixerbalance as empty

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Set Fader Control | Invoke setFaderControl on org.rdk.DisplaySettings with audioPort: "HDMI0", mixerBalance: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setFaderControl", "params": {"audioPort": "HDMI0", "mixerBalance": ""}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |

---

<a id="set_fader_control_outofrange_hdmi0"></a>
### TestCase Name
Set_Fader_Control_OutofRange_HDMI0

### TestCase ID
DS_79

### TestCase Objective
Checks if able to set the mixerbalance as out of range

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Set Fader Control | Invoke setFaderControl on org.rdk.DisplaySettings with audioPort: "HDMI0", mixerBalance: "-60,-40,-38,38,40,60"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setFaderControl", "params": {"audioPort": "HDMI0", "mixerBalance": "-60,-40,-38,38,40,60"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |

---

<a id="set_and_get_audio_mixing_status_hdmi0"></a>
### TestCase Name
Set_and_Get_Audio_Mixing_Status_HDMI0

### TestCase ID
DS_80

### TestCase Objective
Checks if able to enable/disable associated audio mixing

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Associated Audio Mixing | Invoke getAssociatedAudioMixing on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAssociatedAudioMixing", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `mixing` should be `true` or `false` and `success` should be `true` |
| 3 | Set Associated Audio Mixing (iterate each value) | Invoke setAssociatedAudioMixing on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setAssociatedAudioMixing", "params": {"audioPort": "HDMI0", "mixing": <true_or_false>}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` for each value set |
| 4 | Get Associated Audio Mixing (verify after each set) | Invoke getAssociatedAudioMixing on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getAssociatedAudioMixing", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `mixing` should match the value set in the corresponding iteration of step 3 and `success` should be `true` |

---

<a id="displaysettings_activatedeactivate_event_test"></a>
### TestCase Name
DisplaySettings_ActivateDeactivate_Event_Test

### TestCase ID
DS_81

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate DisplaySettings Plugin | Invoke deactivate on Controller with callsign: "org.rdk.DisplaySettings"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 3 | Check PluginActive Status | Invoke status on Controller for org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate DisplaySettings Plugin | Invoke activate on Controller with callsign: "org.rdk.DisplaySettings"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for event Event_Controller_State_Changed | Verify that event data is validated successfully |
| 6 | Check PluginActive Status | Invoke status on Controller for org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="displaysettings_using_keycode_verify_mutestatus_after_increasing_volume_hdmi0"></a>
### TestCase Name
DisplaySettings_Using_KeyCode_Verify_MuteStatus_After_Increasing_Volume_HDMI0

### TestCase ID
DS_82

### TestCase Objective
Verify the mute status after adjusting the volume (increase) using keycode on HDMI0

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_RDKWindowManager_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RDKWindowManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` |
| 3 | Set Volume Level (decrease key — conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke generateKey on org.rdk.RDKWindowManager with modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"keyCode": 174, "modifiers": "", "delay": 1.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the key event is dispatched successfully with null/empty result |
| 4 | Get Volume Level (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be less than the value recorded in step 2 and `success` should be `true` |
| 5 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 6 | Set Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 7 | Get Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` and `success` should be `true` |
| 8 | Retrieve Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value as baseline before increase key) |
| 9 | Set Volume Level Using KeyCode (increase) | Invoke generateKey on org.rdk.RDKWindowManager with modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"keyCode": 175, "modifiers": "", "delay": 1.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the key event is dispatched successfully with null/empty result |
| 10 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be greater than the value recorded in step 8 (volume increased by key press) and `success` should be `true` |
| 11 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` (increasing volume un-mutes audio) and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_Muted_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Get Connected Audio Ports from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted | *(Conditional statement executed only if previous step condition is met)*<br>Set Muted on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Muted | *(Conditional statement executed only if previous step condition is met)*<br>Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` and `success` should be `true` |

---

<a id="displaysettings_using_keycode_verify_mutestatus_after_decreasing_volume_hdmi0"></a>
### TestCase Name
DisplaySettings_Using_KeyCode_Verify_MuteStatus_After_decreasing_Volume_HDMI0

### TestCase ID
DS_83

### TestCase Objective
Verify the mute status after adjusting the volume (decrease) using keycode on HDMI0

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_RDKWindowManager_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RDKWindowManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` |
| 3 | Set Volume Level (increase key — conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke generateKey on org.rdk.RDKWindowManager with modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"keyCode": 175, "modifiers": "", "delay": 1.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the key event is dispatched successfully with null/empty result |
| 4 | Get Volume Level (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be greater than the value recorded in step 2 and `success` should be `true` |
| 5 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 6 | Set Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 7 | Get Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` and `success` should be `true` |
| 8 | Retrieve Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` (record this value as baseline before decrease key) |
| 9 | Set Volume Level Using KeyCode (decrease) | Invoke generateKey on org.rdk.RDKWindowManager with modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"keyCode": 174, "modifiers": "", "delay": 1.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the key event is dispatched successfully with null/empty result |
| 10 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be less than the value recorded in step 8 (volume decreased by key press) and `success` should be `true` |
| 11 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` (decreasing volume un-mutes audio) and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_Muted_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Get Connected Audio Ports from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted | *(Conditional statement executed only if previous step condition is met)*<br>Set Muted on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Muted | *(Conditional statement executed only if previous step condition is met)*<br>Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` and `success` should be `true` |

---

<a id="displaysettings_using_keycode_verify_mutestatus_hdmi0"></a>
### TestCase Name
DisplaySettings_Using_KeyCode_Verify_MuteStatus_HDMI0

### TestCase ID
DS_84

### TestCase Objective
Verify the mute status using keycode on HDMI0

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_RDKWindowManager_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Plugin state should be `activated` and `success` should be `true` |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.RDKWindowManager"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of RDKWindowManager Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.RDKWindowManager"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Mute Status Using KeyCode | Invoke generateKey on org.rdk.RDKWindowManager with modifiers: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.RDKWindowManager.1.generateKey", "params": {"keyCode": 173, "modifiers": "", "delay": 1.0}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 4 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be toggled from the value recorded in step 2 (`true` if was `false`; `false` if was `true`) and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_Muted_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Get Connected Audio Ports from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Set Muted on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Muted (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` and `success` should be `true` |

---

<a id="set_mute_invalid_audioport"></a>
### TestCase Name
Set_Mute_Invalid_audioPort

### TestCase ID
DS_85

### TestCase Objective
Validate by setting up mute for invalid audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Muted | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "INVALID", "muted": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid audio port (`"INVALID"`) — `success` should be `false` |

---

<a id="set_mute_empty_audioport"></a>
### TestCase Name
Set_Mute_empty_audioPort

### TestCase ID
DS_86

### TestCase Objective
Validate by setting up mute for empty audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Muted | Invoke setMuted on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": null, "muted": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for null/empty audio port — `success` should be `false` |

---

<a id="get_dialog_enhancement_invalidaudioport"></a>
### TestCase Name
Get_Dialog_Enhancement_InvalidAudioPort

### TestCase ID
DS_87

### TestCase Objective
Validate by getting dialogEnhancement for invalid audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dialog Enhancement | Invoke getDialogEnhancement on org.rdk.DisplaySettings with audioPort: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDialogEnhancement", "params": {"audioPort": "INVALID"}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid audio port (`"INVALID"`) — `success` should be `false` |

---

<a id="get_dialog_enhancement_emptyaudioport"></a>
### TestCase Name
Get_Dialog_Enhancement_EmptyAudioPort

### TestCase ID
DS_88

### TestCase Objective
Validate by getting dialogEnhancement for empty audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dialog Enhancement | Invoke getDialogEnhancement on org.rdk.DisplaySettings with audioPort: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getDialogEnhancement", "params": {"audioPort": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for empty/blank audio port — `success` should be `false` |

---

<a id="get_volume_level_invalid"></a>
### TestCase Name
Get_Volume_Level_Invalid

### TestCase ID
DS_89

### TestCase Objective
Validate by getting VolumeLevel for invalid audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "INVALID"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "INVALID"}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid audio port (`"INVALID"`) — `success` should be `false` |

---

<a id="get_volume_level_emptyaudioport"></a>
### TestCase Name
Get_Volume_Level_EmptyAudioPort

### TestCase ID
DS_90

### TestCase Objective
Validate by getting VolumeLevel for empty audioport

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: " "<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": " "}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for empty/blank audio port — `success` should be `false` |

---

<a id="displaysettings_verify_volumelevelchanged_event_not_triggered_with_same_volumelevel_hdmi0"></a>
### TestCase Name
DisplaySettings_Verify_VolumeLevelChanged_Event_Not_Triggered_with_Same_VolumeLevel_HDMI0

### TestCase ID
DS_91

### TestCase Objective
To confirm that the volume level change event is not triggered when the volume remains the same for HDMI0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be a valid integer in range `[0, 100]` and `success` should be `true` |
| 3 | Set Volume Level | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": 50}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Volume Level | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be `50` and `success` should be `true` |
| 5 | Set Volume Level | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": 100}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 6 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should be `100` and `success` should be `true` |
| 7 | Check VolumeLevel Changed Event | Listen for event Event_VolumeLevel_Changed | `onVolumeLevelChanged` event should be triggered with `volumeLevel`: `100` (since volume changed from `50` to `100`) |
| 8 | Set Volume Level | Invoke setVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setVolumeLevel", "params": {"audioPort": "HDMI0", "volumeLevel": 100}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 9 | Get Volume Level | Invoke getVolumeLevel on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getVolumeLevel", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `volumeLevel` should remain `100` and `success` should be `true` |
| 10 | Check VolumeLevel Changed Event | Listen for event Event_VolumeLevel_Changed | `onVolumeLevelChanged` event should **NOT** be triggered when volume level remains the same (`100`) |

---

<a id="displaysettings_verify_mutestatuschanged_event_not_triggered_with_same_mutestatus_hdmi0"></a>
### TestCase Name
DisplaySettings_Verify_MuteStatusChanged_Event_Not_Triggered_with_Same_MuteStatus_HDMI0

### TestCase ID
DS_92

### TestCase Objective
To confirm that the mute status change event is not triggered when the mute status remains the same for HDMI0

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": true}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Muted | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` and `success` should be `true` |
| 5 | Set Muted | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 6 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` and `success` should be `true` |
| 7 | Check MuteStatus Changed Event | Listen for event Event_MuteStatus_Changed | `onMuteStatusChanged` event should be triggered with `muted`: `false` (since mute status changed from `true` to `false`) |
| 8 | Set Muted | Invoke setMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 9 | Get Muted | Invoke getMuted on org.rdk.DisplaySettings with audioPort: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should remain `false` and `success` should be `true` |
| 10 | Check MuteStatus Changed Event | Listen for event Event_MuteStatus_Changed | `onMuteStatusChanged` event should **NOT** be triggered when mute status remains the same (`false`) |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_Muted_Status

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Get Connected Audio Ports from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | `connectedAudioPorts` list should include `HDMI0` and `success` should be `true` |
| 2 | Get Muted | Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `true` or `false` and `success` should be `true` |
| 3 | Set Muted | *(Conditional statement executed only if previous step condition is met)*<br>Set Muted on DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setMuted", "params": {"audioPort": "HDMI0", "muted": false}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Muted | *(Conditional statement executed only if previous step condition is met)*<br>Get Muted from DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getMuted", "params": {"audioPort": "HDMI0"}}' http://127.0.0.1:9998/jsonrpc` | `muted` should be `false` and `success` should be `true` |

---

<a id="set_invalid_resolution"></a>
### TestCase Name
Set_Invalid_Resolution

### TestCase ID
DS_93

### TestCase Objective
Validate by setting up invalid resolution

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": 7, "persist": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid resolution value (numeric type `7` instead of string) — `success` should be `false` |

---

<a id="set_empty_resolution"></a>
### TestCase Name
Set_Empty_Resolution

### TestCase ID
DS_94

### TestCase Objective
Validate by setting up empty resolution

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0", resolution: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": "", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for empty resolution string — `success` should be `false` |

---

<a id="set_invaliddatatype_resolution"></a>
### TestCase Name
Set_InvalidDataType_Resolution

### TestCase ID
DS_95

### TestCase Objective
Validate by setting up invalid data type in resolution

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0", resolution: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": "invalid", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid string value in resolution field — `success` should be `false` |

---

<a id="set_empty_videodisplay"></a>
### TestCase Name
Set_Empty_VideoDisplay

### TestCase ID
DS_96

### TestCase Objective
Validate by setting up empty videoDisplay

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "", resolution: "720p"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "", "resolution": "720p", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for empty `videoDisplay` parameter — `success` should be `false` |

---

<a id="set_invalid_videodisplay"></a>
### TestCase Name
Set_Invalid_VideoDisplay

### TestCase ID
DS_97

### TestCase Objective
Validate by setting up invalid videoDisplay

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "invalid", resolution: "720p"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "invalid", "resolution": "720p", "persist": true}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid `videoDisplay` string — `success` should be `false` |

---

<a id="set_invalid_persist"></a>
### TestCase Name
Set_Invalid_Persist

### TestCase ID
DS_98

### TestCase Objective
Validate by setting up invalid persist

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution Negative | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0", resolution: "720p", persist: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "resolution": "720p", "persist": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for invalid `persist` value type (string instead of boolean) — `success` should be `false` |

---

<a id="set_resolution_withoutparameter"></a>
### TestCase Name
Set_Resolution_WithoutParameter

### TestCase ID
DS_99

### TestCase Objective
Validate set currentResolution API without passing the parameter

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set Current Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "HDMI0", persist: "invalid"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "HDMI0", "persist": "invalid"}}' http://127.0.0.1:9998/jsonrpc` | API returns error response for missing `resolution` parameter — `success` should be `false` |

---

<a id="displaysettings_check_display_connected_status_after_light_sleep_hdmi0"></a>
### TestCase Name
DisplaySettings_Check_Display_Connected_Status_After_Light_Sleep_HDMI0

### TestCase ID
DS_100

### TestCase Objective
Verify that the getConnectedVideoDisplays method returns the TV connected status when the device in light sleep mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |
| 2 | Get Power State | Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | `powerState` should be a valid string (`ON`, `STANDBY`, `LIGHT_SLEEP`, `DEEP_SLEEP`) and `success` should be `true` |
| 3 | Set Power State (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke setPowerState on org.rdk.System with standbyReason: "", powerState: "LIGHT_SLEEP"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "", "powerState": "LIGHT_SLEEP"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 4 | Get Power State (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Invoke getPowerState on org.rdk.System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | `powerState` should be `LIGHT_SLEEP` (device may report `STANDBY` for this mode) and `success` should be `true` |
| 5 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | `videoDisplay` list should be non-empty and `success` should be `true` |

### TestCase Post-condition

#### TestCase Post-condition 1: Reverting_PowerState_ON

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check power state | Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | `powerState` should be a valid string (`ON`, `STANDBY`, `LIGHT_SLEEP`, `DEEP_SLEEP`) and `success` should be `true` |
| 2 | Set Power State (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Set Power State on System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.setPowerState", "params": {"standbyReason": "", "powerState": "ON"}}' http://127.0.0.1:9998/jsonrpc` | `success` should be `true` |
| 3 | Check power state (conditional) | *(Conditional statement executed only if previous step condition is met)*<br>Get Power State from System<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.System.1.getPowerState"}' http://127.0.0.1:9998/jsonrpc` | `powerState` should be `ON` and `success` should be `true` |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the zoomSettingUpdated event | Unregister the WebSocket event listener for `zoomSettingUpdated` to stop receiving `zoomSettingUpdated` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.unregister", "params": {"event": "zoomSettingUpdated", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the resolutionChanged event | Unregister the WebSocket event listener for `resolutionChanged` to stop receiving `resolutionChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.unregister", "params": {"event": "resolutionChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 3 | Unsubscribe from the resolutionPreChange event | Unregister the WebSocket event listener for `resolutionPreChange` to stop receiving `resolutionPreChange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.unregister", "params": {"event": "resolutionPreChange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 4 | Unsubscribe from the muteStatusChanged event | Unregister the WebSocket event listener for `muteStatusChanged` to stop receiving `muteStatusChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.unregister", "params": {"event": "muteStatusChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 5 | Unsubscribe from the volumeLevelChanged event | Unregister the WebSocket event listener for `volumeLevelChanged` to stop receiving `volumeLevelChanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.unregister", "params": {"event": "volumeLevelChanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 6 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 42 minutes |
| Priority | Medium |
| TDK Release Version | M81 |
