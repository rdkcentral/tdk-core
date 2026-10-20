## TestScript Name
RDKV_CERT_AVS_PlayerInfo

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [PlayerInfo_Get_Audio_Codecs](#playerinfo_get_audio_codecs)
   - [PlayerInfo_Get_Video_Codecs](#playerinfo_get_video_codecs)
   - [PlayerInfo_Get_AudioEquivalence_Enabled](#playerinfo_get_audioequivalence_enabled)
   - [PlayerInfo_Get_Dolby_Atmos_MetaData](#playerinfo_get_dolby_atmos_metadata)
   - [PlayerInfo_Get_Dolby_Sound_mode](#playerinfo_get_dolby_sound_mode)
   - [PlayerInfo_Enable_Disable_Audio_Atmos_Output](#playerinfo_enable_disable_audio_atmos_output)
   - [PlayerInfo_SetAndGet_All_Supported_Resolutions](#playerinfo_setandget_all_supported_resolutions)
   - [PlayerInfo_Dolby_AudioMode_Changed_Event](#playerinfo_dolby_audiomode_changed_event)
   - [PlayerInfo_ActivateDeactivate_Event_Test](#playerinfo_activatedeactivate_event_test)
   - [PlayerInfo_Get_Dolby_Mode](#playerinfo_get_dolby_mode)
   - [PlayerInfo_Set_And_Get_Dolby_Mode](#playerinfo_set_and_get_dolby_mode)
   - [PlayerInfo_Set_Dolby_Mode_Invalid_Mode](#playerinfo_set_dolby_mode_invalid_mode)
   - [PlayerInfo_Set_Dolby_Mode_Empty_Mode](#playerinfo_set_dolby_mode_empty_mode)
   - [PlayerInfo_Set_Dolby_Mode_Numeric_Mode](#playerinfo_set_dolby_mode_numeric_mode)
   - [PlayerInfo_Set_Dolby_Mode_Special_Character_Mode](#playerinfo_set_dolby_mode_special_character_mode)
   - [PlayerInfo_Set_Dolby_Mode_Without_Mode](#playerinfo_set_dolby_mode_without_mode)
   - [PlayerInfo_Set_Atmos_Output_Invalid_Enable](#playerinfo_set_atmos_output_invalid_enable)
   - [PlayerInfo_Set_Atmos_Output_Empty_Enable](#playerinfo_set_atmos_output_empty_enable)
   - [PlayerInfo_Set_Atmos_Output_Numeric_Enable](#playerinfo_set_atmos_output_numeric_enable)
   - [PlayerInfo_Set_Atmos_Output_Special_Character_Enable](#playerinfo_set_atmos_output_special_character_enable)
   - [PlayerInfo_Set_Atmos_Output_Without_Enable](#playerinfo_set_atmos_output_without_enable)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **PlayerInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `PlayerInfo` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_PlayerInfo_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of DisplaySettings plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the dolby_audiomodechanged event | Register a WebSocket event listener for `dolby_audiomodechanged` to receive `dolby_audiomodechanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.register", "params": {"event": "dolby_audiomodechanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 4: Configure_Device_Parameter

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure supported audio codecs | `SUPPORTED_AUDIO_CODECS` must be set to the audio codec formats supported by the DUT | The `SUPPORTED_AUDIO_CODECS` value should be correctly configured in the device-specific config file |
| 2 | Configure supported video codecs | `SUPPORTED_VIDEO_CODECS` must be set to the video codec formats supported by the DUT | The `SUPPORTED_VIDEO_CODECS` value should be correctly configured in the device-specific config file |
| 3 | Configure NA tests | `PLAYERINFO_NA_TESTS` must be set to the PlayerInfo test names to skip when not applicable on the DUT | The `PLAYERINFO_NA_TESTS` value should be correctly configured in the device-specific config file |
| 4 | Configure dolby mode | `PLAYERINFO_DOLBY_MODE` must be set to the dolby audio modes supported by the DUT | The `PLAYERINFO_DOLBY_MODE` value should be correctly configured in the device-specific config file |

## Test Cases

<a id="playerinfo_get_audio_codecs"></a>
### TestCase Name
PlayerInfo_Get_Audio_Codecs

### TestCase ID
PI_01

### TestCase Objective
checks the audio codecs list

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get audio codecs | Invoke audiocodecs on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.audiocodecs"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio codecs match the expected value `<SUPPORTED_AUDIO_CODECS>` from the device config file  |

---

<a id="playerinfo_get_video_codecs"></a>
### TestCase Name
PlayerInfo_Get_Video_Codecs

### TestCase ID
PI_02

### TestCase Objective
checks the video codecs list

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get video codecs | Invoke videocodecs on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.videocodecs"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported video codecs match the expected value `<SUPPORTED_Video_CODECS>` from the device config file  |

---

<a id="playerinfo_get_audioequivalence_enabled"></a>
### TestCase Name
PlayerInfo_Get_AudioEquivalence_Enabled

### TestCase ID
PI_03

### TestCase Objective
Checks Loudness Equivalence in platform

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Is AudioEquivalence enabled | Invoke isaudioequivalenceenabled on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.isaudioequivalenceenabled"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Playerinfo validate boolean result  |

---

<a id="playerinfo_get_dolby_atmos_metadata"></a>
### TestCase Name
PlayerInfo_Get_Dolby_Atmos_MetaData

### TestCase ID
PI_04

### TestCase Objective
Gets the Atmos capabilities of Sink

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get dolby atmos MetaData | Invoke dolby_atmosmetadata on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_atmosmetadata"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Playerinfo validate boolean result  |

---

<a id="playerinfo_get_dolby_sound_mode"></a>
### TestCase Name
PlayerInfo_Get_Dolby_Sound_mode

### TestCase ID
PI_05

### TestCase Objective
Checks the dolby sound mode

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get dolby SoundMode | Invoke dolby_soundmode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_soundmode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported sound modes include `Unknown`, `Mono`, `Stereo`, `Surround`, `Passthru`, and `SoundmodeAuto`  |

---

<a id="playerinfo_enable_disable_audio_atmos_output"></a>
### TestCase Name
PlayerInfo_Enable_Disable_Audio_Atmos_Output

### TestCase ID
PI_06

### TestCase Objective
Check whether audio atmos output is possible to enable and disable

### Test Steps

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `enable`: `True`, `False`

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable disable audio atmos output | Invoke dolby_enableatmosoutput on PlayerInfo with enable: "<ENABLE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": "<ENABLE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null or empty response |

---

<a id="playerinfo_setandget_all_supported_resolutions"></a>
### TestCase Name
PlayerInfo_SetAndGet_All_Supported_Resolutions

### TestCase ID
PI_07

### TestCase Objective
Set and get all the supported resolution by both TV and STB

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check display connected status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get supported resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get current resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` supported resolutions matches value from step 2  |
| 4 | Set display resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the current resolution is set successfully |
| 5 | Get current player resolution | Invoke resolution on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.resolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="playerinfo_dolby_audiomode_changed_event"></a>
### TestCase Name
PlayerInfo_Dolby_AudioMode_Changed_Event

### TestCase ID
PI_08

### TestCase Objective
Checks for the audio mode changed event

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected audio ports are returned successfully |
| 2 | Get supported audio modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio modes are returned successfully |
| 3 | Get sound mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` supported sound modes matches value from step 2  |
| 4 | Set sound mode | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>", soundMode: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "<result_step_1>", "soundMode": "<result_step_2>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the sound mode is set successfully |
| 5 | Get sound mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |
| 6 | Check dolby AudioMode changed event | Listen for Event_AudioMode_Changed event (wait2s) | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="playerinfo_activatedeactivate_event_test"></a>
### TestCase Name
PlayerInfo_ActivateDeactivate_Event_Test

### TestCase ID
PI_09

### TestCase Objective
Validates statechange event on activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check plugin active status | Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check plugin active status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check active status of PlayerInfo plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate PlayerInfo plugin | Invoke deactivate on Controller with callsign: "PlayerInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check state change event | Listen for Event_Controller_State_Changed event (wait2s) | Verify that the `statechange` event is received for callsign `playerinfo` with state `"deactivated"` |
| 3 | Check plugin active status | Invoke status on Controller for PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate PlayerInfo plugin | Invoke activate on Controller with callsign: "PlayerInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check state change event | Listen for Event_Controller_State_Changed event (wait2s) | Verify that the `statechange` event is received for callsign `playerinfo` with state `"activated"` |
| 6 | Check plugin active status | Invoke status on Controller for PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

---

<a id="playerinfo_get_dolby_mode"></a>
### TestCase Name
PlayerInfo_Get_Dolby_Mode

### TestCase ID
PI_10

### TestCase Objective
Get the dolby mode

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get dolby mode | Invoke dolby_mode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the dolby mode is returned successfully |

---

<a id="playerinfo_set_and_get_dolby_mode"></a>
### TestCase Name
PlayerInfo_Set_And_Get_Dolby_Mode

### TestCase ID
PI_11

### TestCase Objective
Set and get all the supported dolby modes

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get dolby mode | Invoke dolby_mode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the dolby mode is returned successfully |
| 2 | Set dolby mode | Invoke dolby_mode on PlayerInfo with mode: "<PLAYERINFO_DOLBY_MODE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode", "params": {"mode": "<PLAYERINFO_DOLBY_MODE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null/empty result |
| 3 | Get dolby mode | Invoke dolby_mode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode"}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned value matches the iterated value set in the previous step |

---

<a id="playerinfo_set_dolby_mode_invalid_mode"></a>
### TestCase Name
PlayerInfo_Set_Dolby_Mode_Invalid_Mode

### TestCase ID
PI_12

### TestCase Objective
SetDolbyMode rejects an invalid mode value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set dolby mode invalid mode | Invoke dolby_mode on PlayerInfo with mode: "INVALID_MODE"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode", "params": {"mode": "INVALID_MODE"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_dolby_mode_empty_mode"></a>
### TestCase Name
PlayerInfo_Set_Dolby_Mode_Empty_Mode

### TestCase ID
PI_13

### TestCase Objective
SetDolbyMode rejects an empty mode value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set dolby mode empty mode | Invoke dolby_mode on PlayerInfo with mode: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode", "params": {"mode": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_dolby_mode_numeric_mode"></a>
### TestCase Name
PlayerInfo_Set_Dolby_Mode_Numeric_Mode

### TestCase ID
PI_14

### TestCase Objective
SetDolbyMode rejects a numeric mode value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set dolby mode numeric mode | Invoke dolby_mode on PlayerInfo with mode: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode", "params": {"mode": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_dolby_mode_special_character_mode"></a>
### TestCase Name
PlayerInfo_Set_Dolby_Mode_Special_Character_Mode

### TestCase ID
PI_15

### TestCase Objective
SetDolbyMode rejects special characters in the mode value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set dolby mode special character mode | Invoke dolby_mode on PlayerInfo with mode: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode", "params": {"mode": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_dolby_mode_without_mode"></a>
### TestCase Name
PlayerInfo_Set_Dolby_Mode_Without_Mode

### TestCase ID
PI_16

### TestCase Objective
SetDolbyMode rejects invocation without the required mode parameter

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set dolby mode without mode | Invoke dolby_mode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_mode"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_atmos_output_invalid_enable"></a>
### TestCase Name
PlayerInfo_Set_Atmos_Output_Invalid_Enable

### TestCase ID
PI_17

### TestCase Objective
SetAtmosOutput rejects an invalid enable value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set atmos output invalid enable | Invoke dolby_enableatmosoutput on PlayerInfo with enable: "invalid_enable"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": "invalid_enable"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_atmos_output_empty_enable"></a>
### TestCase Name
PlayerInfo_Set_Atmos_Output_Empty_Enable

### TestCase ID
PI_18

### TestCase Objective
SetAtmosOutput rejects an empty enable value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set atmos output empty enable | Invoke dolby_enableatmosoutput on PlayerInfo with enable: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": ""}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_atmos_output_numeric_enable"></a>
### TestCase Name
PlayerInfo_Set_Atmos_Output_Numeric_Enable

### TestCase ID
PI_19

### TestCase Objective
SetAtmosOutput rejects a numeric enable value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set atmos output numeric enable | Invoke dolby_enableatmosoutput on PlayerInfo with enable: 12345<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": 12345}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_atmos_output_special_character_enable"></a>
### TestCase Name
PlayerInfo_Set_Atmos_Output_Special_Character_Enable

### TestCase ID
PI_20

### TestCase Objective
SetAtmosOutput rejects special characters in the enable value

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set atmos output special character enable | Invoke dolby_enableatmosoutput on PlayerInfo with enable: "()^*!"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": "()^*!"}}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |

---

<a id="playerinfo_set_atmos_output_without_enable"></a>
### TestCase Name
PlayerInfo_Set_Atmos_Output_Without_Enable

### TestCase ID
PI_21

### TestCase Objective
SetAtmosOutput rejects invocation without the required enable parameter

### Test Steps

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Set atmos output without enable | Invoke dolby_enableatmosoutput on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput"}' http://127.0.0.1:9998/jsonrpc` | API returns expected error `ERROR_GENERAL` |


## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| # | Step Name | Step Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the dolby_audiomodechanged event | Unregister the WebSocket event listener for `dolby_audiomodechanged` to stop receiving `dolby_audiomodechanged` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.unregister", "params": {"event": "dolby_audiomodechanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

**Supported Models** : Video_Accelerator, RPI-Client

**Estimated duration** : 5 mins

**Priority** : High

**Release Version** : M88

<div align="right"><a href="#testscript-name">Go to Top</a></div>
