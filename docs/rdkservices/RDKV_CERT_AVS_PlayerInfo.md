## TestScript Name
RDKV_CERT_AVS_PlayerInfo

## Table of Contents

1. [Objective](#objective)
2. [APIs Under Test](#apis-under-test)
3. [Events Under Test](#events-under-test)
4. [Plugin Pre-conditions](#plugin-pre-conditions)
5. [Test Cases](#test-cases)
   - [PlayerInfo_Check_Audio_Codecs](#playerinfo_check_audio_codecs)
   - [PlayerInfo_Check_Video_Codecs](#playerinfo_check_video_codecs)
   - [PlayerInfo_Check_AudioEquivalence_Enabled](#playerinfo_check_audioequivalence_enabled)
   - [PlayerInfo_Check_Dolby_Atmos_MetaData](#playerinfo_check_dolby_atmos_metadata)
   - [PlayerInfo_Check_Dolby_Sound_mode](#playerinfo_check_dolby_sound_mode)
   - [Enable_Disable_Audio_Atmos_Output](#enable_disable_audio_atmos_output)
   - [SetAndGet_All_Supported_Resolutions](#setandget_all_supported_resolutions)
   - [Check_Dolby_AudioMode_Changed_Event](#check_dolby_audiomode_changed_event)
   - [PlayerInfo_ActivateDeactivate_Event_Test](#playerinfo_activatedeactivate_event_test)
6. [Plugin Post-conditions](#plugin-post-conditions)
7. [Test Attributes](#test-attributes)

## Objective

The **PlayerInfo** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `PlayerInfo` (version 1)

## APIs Under Test

| API | Description |
| --- | --- |
| `audiocodecs` | Returns supported Audio codecs |
| `dolby_atmosmetadata` | Atmos capabilities of Sink |
| `dolby_enableatmosoutput` | Enables Atmos Audio Output |
| `dolby_soundmode` | Gets the dolby sound mode |
| `isaudioequivalenceenabled` | Checks Loudness Equivalence in platform |
| `resolution` | Returns current Video playback resolution |
| `videocodecs` | Returns supported Video codecs |

## Events Under Test

| Event | Description |
| --- | --- |
| `dolby_audiomodechanged` | Notifies audio mode changed event |

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Activate_DisplaySettings_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.DisplaySettings"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of DisplaySettings Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.DisplaySettings"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 3: Register_And_Listen_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the dolby_audiomodechanged event | Register a WebSocket event listener for `dolby_audiomodechanged` to receive `dolby_audiomodechanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.register", "params": {"event": "dolby_audiomodechanged", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |
| 2 | Subscribe to the statechange event | Register a WebSocket event listener for `statechange` to receive `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.register", "params": {"event": "statechange", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

## Test Cases

<a id="playerinfo_check_audio_codecs"></a>
### TestCase Name
PlayerInfo_Check_Audio_Codecs

### TestCase ID
PI_01

### TestCase Objective
checks the audio codecs list

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Audio Codecs | Invoke audiocodecs on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.audiocodecs"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio codecs match the expected value `<SUPPORTED_AUDIO_CODECS>` from the device config file  |

---

<a id="playerinfo_check_video_codecs"></a>
### TestCase Name
PlayerInfo_Check_Video_Codecs

### TestCase ID
PI_02

### TestCase Objective
checks the video codecs list

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Video Codecs | Invoke videocodecs on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.videocodecs"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported video codecs match the expected value `<SUPPORTED_Video_CODECS>` from the device config file  |

---

<a id="playerinfo_check_audioequivalence_enabled"></a>
### TestCase Name
PlayerInfo_Check_AudioEquivalence_Enabled

### TestCase ID
PI_03

### TestCase Objective
Checks Loudness Equivalence in platform

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Is AudioEquivalence Enabled | Invoke isaudioequivalenceenabled on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.isaudioequivalenceenabled"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Playerinfo validate boolean result  |

---

<a id="playerinfo_check_dolby_atmos_metadata"></a>
### TestCase Name
PlayerInfo_Check_Dolby_Atmos_MetaData

### TestCase ID
PI_04

### TestCase Objective
Gets the Atmos capabilities of Sink

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dolby Atmos MetaData | Invoke dolby_atmosmetadata on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_atmosmetadata"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` Playerinfo validate boolean result  |

---

<a id="playerinfo_check_dolby_sound_mode"></a>
### TestCase Name
PlayerInfo_Check_Dolby_Sound_mode

### TestCase ID
PI_05

### TestCase Objective
Checks the dolby sound mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Dolby SoundMode | Invoke dolby_soundmode on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_soundmode"}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported sound modes include `Unknown`, `Mono`, `Stereo`, `Surround`, `Passthru`, and `SoundmodeAuto`  |

---

<a id="enable_disable_audio_atmos_output"></a>
### TestCase Name
Enable_Disable_Audio_Atmos_Output

### TestCase ID
PI_06

### TestCase Objective
Check whether audio atmos output is possible to enable and disable

### Test Steps

> **Value Loop (Step 1):** Step 1 repeats **2 times**, once for each value of `enable`: `True`, `False`

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Enable Disable Audio Atmos Output | Invoke dolby_enableatmosoutput on PlayerInfo with enable: "<ENABLE_VALUE>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.dolby_enableatmosoutput", "params": {"enable": "<ENABLE_VALUE>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the API call succeeds with null or empty response |

---

<a id="setandget_all_supported_resolutions"></a>
### TestCase Name
SetAndGet_All_Supported_Resolutions

### TestCase ID
PI_07

### TestCase Objective
Set and get all the supported resolution by both TV and STB

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Display Connected Status | Invoke getConnectedVideoDisplays on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedVideoDisplays"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected video displays are returned successfully |
| 2 | Get Supported Resolutions | Invoke getSupportedResolutions on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedResolutions", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported resolutions are returned successfully |
| 3 | Get Current Resolution | Invoke getCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getCurrentResolution", "params": {"videoDisplay": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` supported resolutions matches value from step 2  |
| 4 | Set Resolution | Invoke setCurrentResolution on org.rdk.DisplaySettings with videoDisplay: "<result_step_1>", resolution: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setCurrentResolution", "params": {"videoDisplay": "<result_step_1>", "resolution": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the current resolution is set successfully |
| 5 | Get Resolution | Invoke resolution on PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.resolution"}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="check_dolby_audiomode_changed_event"></a>
### TestCase Name
Check_Dolby_AudioMode_Changed_Event

### TestCase ID
PI_08

### TestCase Objective
Checks for the audio mode changed event

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Connected AudioPorts | Invoke getConnectedAudioPorts on org.rdk.DisplaySettings<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getConnectedAudioPorts"}' http://127.0.0.1:9998/jsonrpc` | Verify that the connected audio ports are returned successfully |
| 2 | Get Supported Audio Modes | Invoke getSupportedAudioModes on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSupportedAudioModes", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that the supported audio modes are returned successfully |
| 3 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` supported sound modes matches value from step 2  |
| 4 | Set Sound Mode | Invoke setSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>", soundMode: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.setSoundMode", "params": {"audioPort": "<result_step_1>", "soundMode": "<result_step_2>", "persist": false}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the sound mode is set successfully |
| 5 | Get Sound Mode | Invoke getSoundMode on org.rdk.DisplaySettings with audioPort: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.DisplaySettings.1.getSoundMode", "params": {"audioPort": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |
| 6 | Check Dolby AudioMode Changed Event | Listen for Event_AudioMode_Changed event (wait2s) | Verify that `success` : `true` returned value matches the iterated value set in the previous step  |

---

<a id="playerinfo_activatedeactivate_event_test"></a>
### TestCase Name
PlayerInfo_ActivateDeactivate_Event_Test

### TestCase ID
PI_09

### TestCase Objective
Validates statechange event on Activating/deactivating the plugin

### TestCase Pre-condition

#### TestCase Pre-condition 1: Activate_Plugins

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check PluginActive Status | Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Check PluginActive Status | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of PlayerInfo Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Deactivate PlayerInfo Plugin | Invoke deactivate on Controller with callsign: "PlayerInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.deactivate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is disabled successfully |
| 2 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait2s) | Verify that the `statechange` event is received for callsign `playerinfo` with state `"deactivated"` |
| 3 | Check PluginActive Status | Invoke status on Controller for PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is deactivated |
| 4 | Activate PlayerInfo Plugin | Invoke activate on Controller with callsign: "PlayerInfo"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "PlayerInfo"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the feature is enabled successfully |
| 5 | Check State Change Event | Listen for Event_Controller_State_Changed event (wait2s) | Verify that the `statechange` event is received for callsign `playerinfo` with state `"activated"` |
| 6 | Check PluginActive Status | Invoke status on Controller for PlayerInfo<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@PlayerInfo"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

## Plugin Post-conditions


### Plugin Post-condition 1: Unregister_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the dolby_audiomodechanged event | Unregister the WebSocket event listener for `dolby_audiomodechanged` to stop receiving `dolby_audiomodechanged` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "PlayerInfo.1.unregister", "params": {"event": "dolby_audiomodechanged", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |
| 2 | Unsubscribe from the statechange event | Unregister the WebSocket event listener for `statechange` to stop receiving `statechange` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.unregister", "params": {"event": "statechange", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |


## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 5 minutes |
| Priority | Medium |
| TDK Release Version | M88 |

<div align="right"><a href="#">&#8593; Go to Top</a></div>
