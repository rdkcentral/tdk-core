## TestScript Name
RDKV_CERT_AVS_SystemAudioPlayer

## Table of Contents

1. [Objective](#objective)
2. [Plugin Pre-conditions](#plugin-pre-conditions)
3. [Test Cases](#test-cases)
   - [SAP_Open_Player_PCM_HTTPSRC_System](#sap_open_player_pcm_httpsrc_system)
   - [SAP_Open_Player_MP3_HTTPSRC_System](#sap_open_player_mp3_httpsrc_system)
   - [SAP_Open_Player_WAV_HTTPSRC_System](#sap_open_player_wav_httpsrc_system)
   - [SAP_Open_Player_PCM_HTTPSRC_App](#sap_open_player_pcm_httpsrc_app)
   - [SAP_Open_Player_MP3_HTTPSRC_App](#sap_open_player_mp3_httpsrc_app)
   - [SAP_Open_Player_WAV_HTTPSRC_App](#sap_open_player_wav_httpsrc_app)
   - [SAP_Config_Player_PCM_Valid_Params_System](#sap_config_player_pcm_valid_params_system)
   - [SAP_Config_Player_PCM_Valid_Params_App](#sap_config_player_pcm_valid_params_app)
   - [SAP_Get_Player_Session_Id_WAV_HTTPSRC_System](#sap_get_player_session_id_wav_httpsrc_system)
   - [SAP_Get_Player_Session_Id_MP3_HTTPSRC_System](#sap_get_player_session_id_mp3_httpsrc_system)
   - [SAP_Get_Player_Session_Id_WAV_HTTPSRC_App](#sap_get_player_session_id_wav_httpsrc_app)
   - [SAP_Get_Player_Session_Id_MP3_HTTPSRC_App](#sap_get_player_session_id_mp3_httpsrc_app)
   - [SAP_Is_Speaking_MP3_HTTPSRC_System](#sap_is_speaking_mp3_httpsrc_system)
   - [SAP_Is_Speaking_WAV_HTTPSRC_System](#sap_is_speaking_wav_httpsrc_system)
   - [SAP_Is_Speaking_MP3_HTTPSRC_App](#sap_is_speaking_mp3_httpsrc_app)
   - [SAP_Is_Speaking_WAV_HTTPSRC_App](#sap_is_speaking_wav_httpsrc_app)
   - [SAP_Play_Pause_Stop_MP3_HTTPSRC_System](#sap_play_pause_stop_mp3_httpsrc_system)
   - [SAP_Play_Pause_Stop_WAV_HTTPSRC_System](#sap_play_pause_stop_wav_httpsrc_system)
   - [SAP_Play_Pause_Stop_MP3_HTTPSRC_App](#sap_play_pause_stop_mp3_httpsrc_app)
   - [SAP_Play_Pause_Stop_WAV_HTTPSRC_App](#sap_play_pause_stop_wav_httpsrc_app)
   - [SAP_Play_Pause_Resume_Stop_Audio_MP3_HTTPSRC_System](#sap_play_pause_resume_stop_audio_mp3_httpsrc_system)
   - [SAP_Play_Pause_Resume_Stop_Audio_WAV_HTTPSRC_System](#sap_play_pause_resume_stop_audio_wav_httpsrc_system)
   - [SAP_Play_Pause_Resume_Stop_Audio_MP3_HTTPSRC_App](#sap_play_pause_resume_stop_audio_mp3_httpsrc_app)
   - [SAP_Play_Pause_Resume_Stop_Audio_WAV_HTTPSRC_App](#sap_play_pause_resume_stop_audio_wav_httpsrc_app)
   - [SAP_Set_Mixer_Levels_MP3_HTTPSRC_System](#sap_set_mixer_levels_mp3_httpsrc_system)
   - [SAP_Set_Mixer_Levels_WAV_HTTPSRC_System](#sap_set_mixer_levels_wav_httpsrc_system)
   - [SAP_Set_Mixer_Levels_MP3_HTTPSRC_App](#sap_set_mixer_levels_mp3_httpsrc_app)
   - [SAP_Set_Mixer_Levels_WAV_HTTPSRC_App](#sap_set_mixer_levels_wav_httpsrc_app)
   - [SAP_Set_Smart_Volume_Control_PCM_HTTPSRC_System](#sap_set_smart_volume_control_pcm_httpsrc_system)
   - [SAP_Set_Smart_Volume_Control_MP3_HTTPSRC_System](#sap_set_smart_volume_control_mp3_httpsrc_system)
   - [SAP_Set_Smart_Volume_Control_WAV_HTTPSRC_System](#sap_set_smart_volume_control_wav_httpsrc_system)
   - [SAP_Set_Smart_Volume_Control_PCM_HTTPSRC_App](#sap_set_smart_volume_control_pcm_httpsrc_app)
   - [SAP_Set_Smart_Volume_Control_MP3_HTTPSRC_App](#sap_set_smart_volume_control_mp3_httpsrc_app)
   - [SAP_Set_Smart_Volume_Control_WAV_HTTPSRC_App](#sap_set_smart_volume_control_wav_httpsrc_app)
   - [SAP_Open_Player_Empty_Audiotype](#sap_open_player_empty_audiotype)
   - [SAP_Open_Player_Invalid_Audiotype](#sap_open_player_invalid_audiotype)
   - [SAP_Open_Player_Invalid_Sourcetype](#sap_open_player_invalid_sourcetype)
   - [SAP_Open_Player_Invalid_Playmode](#sap_open_player_invalid_playmode)
   - [SAP_Close_Player_Invalid_Id](#sap_close_player_invalid_id)
   - [SAP_Play_Audio_Invalid_Player_Id](#sap_play_audio_invalid_player_id)
   - [SAP_Play_Audio_Empty_URL](#sap_play_audio_empty_url)
   - [SAP_Pause_Audio_Invalid_Player_Id](#sap_pause_audio_invalid_player_id)
   - [SAP_Resume_Audio_Invalid_Player_Id](#sap_resume_audio_invalid_player_id)
   - [SAP_Stop_Audio_Invalid_Player_Id](#sap_stop_audio_invalid_player_id)
   - [SAP_Set_Mixer_Levels_Primary_Volume_OOR](#sap_set_mixer_levels_primary_volume_oor)
   - [SAP_Set_Mixer_Levels_Player_Volume_OOR](#sap_set_mixer_levels_player_volume_oor)
   - [SAP_Get_Player_Session_Id_Empty_URL](#sap_get_player_session_id_empty_url)
   - [SAP_Config_Player_Invalid_Id](#sap_config_player_invalid_id)
   - [SAP_Set_Smart_Vol_Threshold_Out_Of_Range](#sap_set_smart_vol_threshold_out_of_range)
   - [SAP_Smart_Vol_Control_Enable_Play_Disable_Lifecycle](#sap_smart_vol_control_enable_play_disable_lifecycle)
   - [SAP_Play_On_Closed_Player_Error_State](#sap_play_on_closed_player_error_state)
   - [SAP_Mixer_Levels_Min_Boundary_Values](#sap_mixer_levels_min_boundary_values)
   - [SAP_Mixer_Levels_Max_Boundary_Values](#sap_mixer_levels_max_boundary_values)
   - [SAP_Dual_Player_System_And_App_Mode](#sap_dual_player_system_and_app_mode)
   - [SAP_Play_Stop_Replay_Scenario](#sap_play_stop_replay_scenario)
4. [Plugin Post-conditions](#plugin-post-conditions)
5. [Test Attributes](#test-attributes)

## Objective

The **SystemAudioPlayer** plugin is a Thunder (WPEFramework) component
accessible via JSON-RPC under the callsign `org.rdk.SystemAudioPlayer` (version 1)

## Plugin Pre-conditions

### Plugin Pre-condition 1: Activate_SystemAudioPlayer_Plugin

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Check Plugin Active Status | Check Active Status of SystemAudioPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.SystemAudioPlayer"}' http://127.0.0.1:9998/jsonrpc` | Verify that the plugin state is returned successfully |
| 2 | Activate Plugin | *(Conditional statement executed only if plugin is currently deactivated)*<br>Activate SystemAudioPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.activate", "params": {"callsign": "org.rdk.SystemAudioPlayer"}}' http://127.0.0.1:9998/jsonrpc` | Confirm that the plugin is activated successfully |
| 3 | Verify Plugin Activated | *(Conditional statement executed only if plugin is activated in step 2)*<br>Check Active Status of SystemAudioPlayer Plugin<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "Controller.1.status@org.rdk.SystemAudioPlayer"}' http://127.0.0.1:9998/jsonrpc` | Verify plugin state is activated |

### Plugin Pre-condition 2: Register_SAP_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Subscribe to the onsapevents event | Register a WebSocket event listener for `onsapevents` to receive `onsapevents` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.register", "params": {"event": "onsapevents", "id": "client.events.1"}}` | Event registration should be established successfully and the event listener should be active |

### Plugin Pre-condition 3: Configure_Device_Parameter

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Configure WAV Audio File URL | `SAP_AUDIO_URL_HTTPSRC_WAV` must be set to the HTTPS hosted URL of the WAV audio file for System Audio Player playback testing | The `SAP_AUDIO_URL_HTTPSRC_WAV` value should be correctly configured in the device-specific config file |
| 2 | Configure MP3 Audio File URL | `SAP_AUDIO_URL_HTTPSRC_MP3` must be set to the HTTPS hosted URL of the MP3 audio file for System Audio Player playback testing | The `SAP_AUDIO_URL_HTTPSRC_MP3` value should be correctly configured in the device-specific config file |

## Test Cases

<a id="sap_open_player_pcm_httpsrc_system"></a>
### TestCase Name
SAP_Open_Player_PCM_HTTPSRC_System

### TestCase ID
SAP_01

### TestCase Objective
Opens a player with PCM audio type, HTTP source and system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player PCM HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Open_Player_MP3_HTTPSRC_System

### TestCase ID
SAP_02

### TestCase Objective
Opens a player with MP3 audio type, HTTP source and system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_wav_httpsrc_system"></a>
### TestCase Name
SAP_Open_Player_WAV_HTTPSRC_System

### TestCase ID
SAP_03

### TestCase Objective
Opens a player with WAV audio type, HTTP source and system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_pcm_httpsrc_app"></a>
### TestCase Name
SAP_Open_Player_PCM_HTTPSRC_App

### TestCase ID
SAP_04

### TestCase Objective
Opens a player with PCM audio type, HTTP source and app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player PCM HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Open_Player_MP3_HTTPSRC_App

### TestCase ID
SAP_05

### TestCase Objective
Opens a player with MP3 audio type, HTTP source and app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_wav_httpsrc_app"></a>
### TestCase Name
SAP_Open_Player_WAV_HTTPSRC_App

### TestCase ID
SAP_06

### TestCase Objective
Opens a player with WAV audio type, HTTP source and app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_config_player_pcm_valid_params_system"></a>
### TestCase Name
SAP_Config_Player_PCM_Valid_Params_System

### TestCase ID
SAP_07

### TestCase Objective
Configures a PCM player with valid format, rate, channels and layout parameters in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open PCM Player For Config | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Config PCM Player | Invoke config on org.rdk.SystemAudioPlayer with id: "<result_step_1>", format: "S16LE", rate: "2147483647", channels: "1", layout: "interleaved" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.config", "params": {"id": "<result_step_1>", "format": "S16LE", "rate": 2147483647, "channels": 1, "layout": "interleaved"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_config_player_pcm_valid_params_app"></a>
### TestCase Name
SAP_Config_Player_PCM_Valid_Params_App

### TestCase ID
SAP_08

### TestCase Objective
Configures a PCM player with valid format, rate, channels and layout parameters in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open PCM Player For Config | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Config PCM Player | Invoke config on org.rdk.SystemAudioPlayer with id: "<result_step_1>", format: "S16LE", rate: "2147483647", channels: "1", layout: "interleaved" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.config", "params": {"id": "<result_step_1>", "format": "S16LE", "rate": 2147483647, "channels": 1, "layout": "interleaved"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_get_player_session_id_wav_httpsrc_system"></a>
### TestCase Name
SAP_Get_Player_Session_Id_WAV_HTTPSRC_System

### TestCase ID
SAP_09

### TestCase Objective
Gets a session ID for WAV audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 6 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_get_player_session_id_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Get_Player_Session_Id_MP3_HTTPSRC_System

### TestCase ID
SAP_10

### TestCase Objective
Gets a session ID for MP3 audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 6 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_get_player_session_id_wav_httpsrc_app"></a>
### TestCase Name
SAP_Get_Player_Session_Id_WAV_HTTPSRC_App

### TestCase ID
SAP_11

### TestCase Objective
Gets a session ID for WAV audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 6 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_get_player_session_id_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Get_Player_Session_Id_MP3_HTTPSRC_App

### TestCase ID
SAP_12

### TestCase Objective
Gets a session ID for MP3 audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 6 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_is_speaking_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Is_Speaking_MP3_HTTPSRC_System

### TestCase ID
SAP_13

### TestCase Objective
Checks whether the player is speaking for MP3 audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_is_speaking_wav_httpsrc_system"></a>
### TestCase Name
SAP_Is_Speaking_WAV_HTTPSRC_System

### TestCase ID
SAP_14

### TestCase Objective
Checks whether the player is speaking for WAV audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_is_speaking_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Is_Speaking_MP3_HTTPSRC_App

### TestCase ID
SAP_15

### TestCase Objective
Checks whether the player is speaking for MP3 audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_is_speaking_wav_httpsrc_app"></a>
### TestCase Name
SAP_Is_Speaking_WAV_HTTPSRC_App

### TestCase ID
SAP_16

### TestCase Objective
Checks whether the player is speaking for WAV audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_stop_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Play_Pause_Stop_MP3_HTTPSRC_System

### TestCase ID
SAP_17

### TestCase Objective
Tests play, pause and stop operations for MP3 audio type with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 11 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_stop_wav_httpsrc_system"></a>
### TestCase Name
SAP_Play_Pause_Stop_WAV_HTTPSRC_System

### TestCase ID
SAP_18

### TestCase Objective
Tests play, pause and stop operations for WAV audio type with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 11 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_stop_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Play_Pause_Stop_MP3_HTTPSRC_App

### TestCase ID
SAP_19

### TestCase Objective
Tests play, pause and stop operations for MP3 audio type with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 11 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_stop_wav_httpsrc_app"></a>
### TestCase Name
SAP_Play_Pause_Stop_WAV_HTTPSRC_App

### TestCase ID
SAP_20

### TestCase Objective
Tests play, pause and stop operations for WAV audio type with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 11 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_resume_stop_audio_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Play_Pause_Resume_Stop_Audio_MP3_HTTPSRC_System

### TestCase ID
SAP_21

### TestCase Objective
Tests the play, pause, resume and stop functionality of the audio player with MP3 audio format and HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 5 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 6 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 8 | Resume SAP Audio | Invoke resume on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.resume", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 9 | Listen For PLAYBACK RESUMED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_RESUMED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 11 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 12 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 13 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_resume_stop_audio_wav_httpsrc_system"></a>
### TestCase Name
SAP_Play_Pause_Resume_Stop_Audio_WAV_HTTPSRC_System

### TestCase ID
SAP_22

### TestCase Objective
Tests the play, pause, resume and stop functionality of the audio player with WAV audio format and HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 5 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 6 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 8 | Resume SAP Audio | Invoke resume on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.resume", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 9 | Listen For PLAYBACK RESUMED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_RESUMED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 10 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 11 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 12 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 13 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_resume_stop_audio_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Play_Pause_Resume_Stop_Audio_MP3_HTTPSRC_App

### TestCase ID
SAP_23

### TestCase Objective
Tests the play, pause, resume and stop functionality of the audio player with MP3 audio format and HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Resume SAP Audio | Invoke resume on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.resume", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 10 | Listen For PLAYBACK RESUMED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_RESUMED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 11 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 12 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 13 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 14 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_play_pause_resume_stop_audio_wav_httpsrc_app"></a>
### TestCase Name
SAP_Play_Pause_Resume_Stop_Audio_WAV_HTTPSRC_App

### TestCase ID
SAP_24

### TestCase Objective
Tests the play, pause, resume and stop functionality of the audio player with WAV audio format and HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Pause SAP Audio | Invoke pause on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 7 | Listen For PLAYBACK PAUSED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_PAUSED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently paused |
| 9 | Resume SAP Audio | Invoke resume on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.resume", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 10 | Listen For PLAYBACK RESUMED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_RESUMED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 11 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 12 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 13 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 14 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_mixer_levels_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Set_Mixer_Levels_MP3_HTTPSRC_System

### TestCase ID
SAP_25

### TestCase Objective
Tests setting mixer levels for MP3 audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set SAP Mixer Levels | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "50", playerVolume: "30"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 50, "playerVolume": 30}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_mixer_levels_wav_httpsrc_system"></a>
### TestCase Name
SAP_Set_Mixer_Levels_WAV_HTTPSRC_System

### TestCase ID
SAP_26

### TestCase Objective
Tests setting mixer levels for WAV audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set SAP Mixer Levels | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "70", playerVolume: "40"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 70, "playerVolume": 40}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 7 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 8 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_mixer_levels_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Set_Mixer_Levels_MP3_HTTPSRC_App

### TestCase ID
SAP_27

### TestCase Objective
Tests setting mixer levels for MP3 audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player MP3 HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set SAP Mixer Levels | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "50", playerVolume: "30"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 50, "playerVolume": 30}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 6 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 7 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 9 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_mixer_levels_wav_httpsrc_app"></a>
### TestCase Name
SAP_Set_Mixer_Levels_WAV_HTTPSRC_App

### TestCase ID
SAP_28

### TestCase Objective
Tests setting mixer levels for WAV audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open SAP Player WAV HTTPSRC | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set SAP Mixer Levels | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "70", playerVolume: "40"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 70, "playerVolume": 40}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play SAP Audio HTTPSRC | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Get SAP Session Id | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and returned `sessionId` matches player ID from step 1 |
| 6 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 7 | Stop Audio Event Cleanup | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully |
| 8 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 9 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_pcm_httpsrc_system"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_PCM_HTTPSRC_System

### TestCase ID
SAP_29

### TestCase Objective
Tests setting smart volume control for PCM audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_mp3_httpsrc_system"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_MP3_HTTPSRC_System

### TestCase ID
SAP_30

### TestCase Objective
Tests setting smart volume control for MP3 audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_wav_httpsrc_system"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_WAV_HTTPSRC_System

### TestCase ID
SAP_31

### TestCase Objective
Tests setting smart volume control for WAV audio format with HTTP source in system play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_pcm_httpsrc_app"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_PCM_HTTPSRC_App

### TestCase ID
SAP_32

### TestCase Objective
Tests setting smart volume control for PCM audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_mp3_httpsrc_app"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_MP3_HTTPSRC_App

### TestCase ID
SAP_33

### TestCase Objective
Tests setting smart volume control for MP3 audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_smart_volume_control_wav_httpsrc_app"></a>
### TestCase Name
SAP_Set_Smart_Volume_Control_WAV_HTTPSRC_App

### TestCase ID
SAP_34

### TestCase Objective
Tests setting smart volume control for WAV audio format with HTTP source in app play mode

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol Enable | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable Smart Vol Control | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_open_player_empty_audiotype"></a>
### TestCase Name
SAP_Open_Player_Empty_Audiotype

### TestCase ID
SAP_35

### TestCase Objective
Attempts to open a player with an empty audiotype parameter, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player Empty Audiotype | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_open_player_invalid_audiotype"></a>
### TestCase Name
SAP_Open_Player_Invalid_Audiotype

### TestCase ID
SAP_36

### TestCase Objective
Attempts to open a player with an audiotype value not in the allowed enum (pcm/mp3/wav)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player Invalid Audiotype Ogg | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "ogg", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "ogg", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_open_player_invalid_sourcetype"></a>
### TestCase Name
SAP_Open_Player_Invalid_Sourcetype

### TestCase ID
SAP_37

### TestCase Objective
Attempts to open a player with a sourcetype value not in the allowed enum (data/httpsrc/filesrc/websocket)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player Invalid Sourcetype Value | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "invalidsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "invalidsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_open_player_invalid_playmode"></a>
### TestCase Name
SAP_Open_Player_Invalid_Playmode

### TestCase ID
SAP_38

### TestCase Objective
Attempts to open a player with a playmode value not in the allowed enum (system/app)

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player Invalid Playmode Value | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "pcm", sourcetype: "httpsrc", playmode: "background"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "pcm", "sourcetype": "httpsrc", "playmode": "background"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_close_player_invalid_id"></a>
### TestCase Name
SAP_Close_Player_Invalid_Id

### TestCase ID
SAP_39

### TestCase Objective
Attempts to close a player with a non-existent session ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Close Player With Invalid Id | Invoke close on org.rdk.SystemAudioPlayer with id: "-1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": -1}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_play_audio_invalid_player_id"></a>
### TestCase Name
SAP_Play_Audio_Invalid_Player_Id

### TestCase ID
SAP_40

### TestCase Objective
Attempts to play audio with a non-existent player ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Play Audio With Invalid Id | Invoke play on org.rdk.SystemAudioPlayer with id: "-1", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": -1, "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_play_audio_empty_url"></a>
### TestCase Name
SAP_Play_Audio_Empty_URL

### TestCase ID
SAP_41

### TestCase Objective
Attempts to play audio with an empty URL parameter, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Invalid URL Play | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Play Audio With Empty URL | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": ""}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_pause_audio_invalid_player_id"></a>
### TestCase Name
SAP_Pause_Audio_Invalid_Player_Id

### TestCase ID
SAP_42

### TestCase Objective
Attempts to pause audio on a non-existent player ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Pause Audio With Invalid Id | Invoke pause on org.rdk.SystemAudioPlayer with id: "-1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.pause", "params": {"id": -1}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_resume_audio_invalid_player_id"></a>
### TestCase Name
SAP_Resume_Audio_Invalid_Player_Id

### TestCase ID
SAP_43

### TestCase Objective
Attempts to resume audio on a non-existent player ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Resume Audio With Invalid Id | Invoke resume on org.rdk.SystemAudioPlayer with id: "-1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.resume", "params": {"id": -1}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_stop_audio_invalid_player_id"></a>
### TestCase Name
SAP_Stop_Audio_Invalid_Player_Id

### TestCase ID
SAP_44

### TestCase Objective
Attempts to stop audio on a non-existent player ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Stop Audio With Invalid Id | Invoke stop on org.rdk.SystemAudioPlayer with id: "-1"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": -1}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_set_mixer_levels_primary_volume_oor"></a>
### TestCase Name
SAP_Set_Mixer_Levels_Primary_Volume_OOR

### TestCase ID
SAP_45

### TestCase Objective
Attempts to set primary volume above maximum (100), expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Primary OOR | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set Mixer Primary Volume OOR | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "200", playerVolume: "7"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 200, "playerVolume": 7}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_set_mixer_levels_player_volume_oor"></a>
### TestCase Name
SAP_Set_Mixer_Levels_Player_Volume_OOR

### TestCase ID
SAP_46

### TestCase Objective
Attempts to set player volume above maximum (100), expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Player Vol OOR | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set Mixer Player Volume OOR | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "20", playerVolume: "150"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 20, "playerVolume": 150}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_get_player_session_id_empty_url"></a>
### TestCase Name
SAP_Get_Player_Session_Id_Empty_URL

### TestCase ID
SAP_47

### TestCase Objective
Attempts to get a session ID with an empty URL parameter, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Get Session Id With Empty URL | Invoke getPlayerSessionId on org.rdk.SystemAudioPlayer with url: ""<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.getPlayerSessionId", "params": {"url": ""}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_config_player_invalid_id"></a>
### TestCase Name
SAP_Config_Player_Invalid_Id

### TestCase ID
SAP_48

### TestCase Objective
Attempts to configure a player with a non-existent session ID, expects an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Config Player With Invalid Id | Invoke config on org.rdk.SystemAudioPlayer with id: "-1", format: "S16LE", rate: "22050", channels: "1", layout: "interleaved"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.config", "params": {"id": -1, "format": "S16LE", "rate": 22050, "channels": 1, "layout": "interleaved"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_set_smart_vol_threshold_out_of_range"></a>
### TestCase Name
SAP_Set_Smart_Vol_Threshold_Out_Of_Range

### TestCase ID
SAP_49

### TestCase Objective
Attempts to set smart volume control with audio level threshold above maximum (1.0), expects an error

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For SmartVol OOR | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set SmartVol Threshold OOR | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "2.5", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 2.5, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |
| 3 | Close Player Cleanup | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully |

---

<a id="sap_smart_vol_control_enable_play_disable_lifecycle"></a>
### TestCase Name
SAP_Smart_Vol_Control_Enable_Play_Disable_Lifecycle

### TestCase ID
SAP_50

### TestCase Objective
Tests enabling smart volume control, playing audio and then disabling smart volume control

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player SmartVol Lifecycle | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Enable SmartVol Before Play | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "true", playerAudioLevelThreshold: "0.5", playerDetectTimeMs: "300", playerHoldTimeMs: "500", primaryDuckingPercent: "25"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": true, "playerAudioLevelThreshold": 0.5, "playerDetectTimeMs": 300, "playerHoldTimeMs": 500, "primaryDuckingPercent": 25}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 3 | Play Audio SmartVol Active | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Audio SmartVol Lifecycle | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 7 | Disable SmartVol After Stop | Invoke setSmartVolControl on org.rdk.SystemAudioPlayer with id: "<result_step_1>", enable: "false", playerAudioLevelThreshold: "0.1", playerDetectTimeMs: "200", playerHoldTimeMs: "1000", primaryDuckingPercent: "50"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setSmartVolControl", "params": {"id": "<result_step_1>", "enable": false, "playerAudioLevelThreshold": 0.1, "playerDetectTimeMs": 200, "playerHoldTimeMs": 1000, "primaryDuckingPercent": 50}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that smart vol control is set successfully |
| 8 | Close Player SmartVol Lifecycle | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|

---

<a id="sap_play_on_closed_player_error_state"></a>
### TestCase Name
SAP_Play_On_Closed_Player_Error_State

### TestCase ID
SAP_51

### TestCase Objective
Verifies that attempting to play on an already-closed player ID returns an error response

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Error State | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Close Player To Create Error State | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>" (wait 3 second(s) before invoking)<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|
| 3 | Play On Closed Player | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` (expected error response for invalid input) |

---

<a id="sap_mixer_levels_min_boundary_values"></a>
### TestCase Name
SAP_Mixer_Levels_Min_Boundary_Values

### TestCase ID
SAP_52

### TestCase Objective
Tests setting mixer levels at minimum boundary values (0,0) and verifies playback succeeds

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Min Mixer | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set Mixer Min Boundary | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "0", playerVolume: "0"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 0, "playerVolume": 0}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play Audio At Min Volume | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Min Volume Playback | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 7 | Close Min Volume Player | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|

---

<a id="sap_mixer_levels_max_boundary_values"></a>
### TestCase Name
SAP_Mixer_Levels_Max_Boundary_Values

### TestCase ID
SAP_53

### TestCase Objective
Tests setting mixer levels at maximum boundary values (100,100) and verifies playback succeeds

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Max Mixer | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Set Mixer Max Boundary | Invoke setMixerLevels on org.rdk.SystemAudioPlayer with id: "<result_step_1>", primaryVolume: "100", playerVolume: "100"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.setMixerLevels", "params": {"id": "<result_step_1>", "primaryVolume": 100, "playerVolume": 100}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that mixer levels is set successfully |
| 3 | Play Audio At Max Volume | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop Max Volume Playback | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 7 | Close Max Volume Player | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|

---

<a id="sap_dual_player_system_and_app_mode"></a>
### TestCase Name
SAP_Dual_Player_System_And_App_Mode

### TestCase ID
SAP_54

### TestCase Objective
Opens two players simultaneously in system and app play modes, plays the system player and closes both

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open System Mode Player | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "wav", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "wav", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | Open App Mode Player | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "app"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "app"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 3 | Play System Mode Audio | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_WAV>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_WAV>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 4 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 5 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 6 | Stop System Mode Audio | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 7 | Close System Mode Player | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|
| 8 | Close App Mode Player | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_2>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_2>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|

---

<a id="sap_play_stop_replay_scenario"></a>
### TestCase Name
SAP_Play_Stop_Replay_Scenario

### TestCase ID
SAP_55

### TestCase Objective
Verifies that a player can successfully stop and restart audio playback on the same player instance

### Test Steps

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Open Player For Replay | Invoke open on org.rdk.SystemAudioPlayer with audiotype: "mp3", sourcetype: "httpsrc", playmode: "system"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.open", "params": {"audiotype": "mp3", "sourcetype": "httpsrc", "playmode": "system"}}' http://127.0.0.1:9998/jsonrpc` | Player opened successfully, `id` (player session ID) returned |
| 2 | First Play Audio | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 3 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 4 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 5 | First Stop Audio | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 6 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 7 | Replay Audio | Invoke play on org.rdk.SystemAudioPlayer with id: "<result_step_1>", url: "<SAP_AUDIO_URL_HTTPSRC_MP3>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.play", "params": {"id": "<result_step_1>", "url": "<SAP_AUDIO_URL_HTTPSRC_MP3>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` |
| 8 | Listen For PLAYBACK STARTED | Listen for `Event_On_SAP_Events` event and wait up to 3 second(s) | Verify that the `PLAYBACK_STARTED` event is received from `Event_On_SAP_Events` for player session opened in step 1  |
| 9 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` audio is currently playing |
| 10 | Second Stop Audio | Invoke stop on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.stop", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the stop operation is completed successfully|
| 11 | Check Is Speaking Status | Invoke isspeaking on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.isspeaking", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `false` audio is currently stopped |
| 12 | Close Player After Replay | Invoke close on org.rdk.SystemAudioPlayer with id: "<result_step_1>"<br>`curl -d '{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.close", "params": {"id": "<result_step_1>"}}' http://127.0.0.1:9998/jsonrpc` | API should return `success`: `true` and confirm that the close operation is completed successfully|

## Plugin Post-conditions

### Plugin Post-condition 1: Unregister_SAP_Events

| Step ID | Step Name | Description | Expected Result |
| --- | --- | --- | --- |
| 1 | Unsubscribe from the onsapevents event | Unregister the WebSocket event listener for `onsapevents` to stop receiving `onsapevents` event notifications.<br>`{"jsonrpc": "2.0", "id": 3, "method": "org.rdk.SystemAudioPlayer.1.unregister", "params": {"event": "onsapevents", "id": "client.events.1"}}` | Event unregistration should be completed successfully and the event listener should be inactive |

## Test Attributes

| Attribute | Value |
| --- | --- |
| Supported Models | Video Accelerator, RPI Client |
| Estimated Duration | 20 minutes |
| Priority | Medium |
| TDK Release Version | M150 |

<div align="right"><a href="#">&#8593; Go to Top</a></div>
