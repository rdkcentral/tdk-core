**TestCase ID**
NATIVE_PLAYBACK_121

**TestCase Name**
NPVS_Audio_Change_AC3_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify if dynamic audio codec switching (AC3 to AAC) is possible while maintaining video playback continuity using GStreamer playbin `current-audio` property. Validate that audio track can be switched between different codec types (AC3 and AAC) present in the same multi-codec stream without interrupting video playback. Specifically validate audio rendering quality, position synchronization, and codec switching timing accuracy using `g_object_set(playbin, "current-audio", stream_index, NULL)` property during active playback. Verify codec identity using `g_signal_emit_by_name(playbin, "get-audio-tags", stream_index, &tags)` to confirm codec change.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-codec stream containing both AC3 and AAC audio tracks must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) with DASH manifest. Stream configured as `test_streams_base_path + "MultiCodecStreams/stream_with_ac3_aac.mpd"` in MediaValidationVariables.py | Verify multi-codec DASH stream accessible, both AC3 and AAC audio tracks present and parseable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_ac3_aac` configured in `MediaValidationVariables.py` with DASH manifest containing AC3 and AAC audio tracks | Verify `video_src_url_ac3_aac` resolves to valid multi-codec stream with dual audio tracks |
| 4 | Device Configuration Parameters | Configuration parameters `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default 10 seconds per codec) and `NATIVE_PLAYBACK_CHECK_AV_STATUS` must be retrievable from device configuration | Verify device config returns valid timeout and AV status check values |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland configuration. Establish Wayland display session via RDKWindowManager. Initialize logging to `/opt/TDK/mediapipeline_test_step.log` | Verify environment variables load without errors, Wayland display active, logging initialized |
| 2 | Configure Test Parameters and Load Multi-Codec Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and `NATIVE_PLAYBACK_CHECK_AV_STATUS` from device. Build `mediapipelinetests` command with test_name="test_playback_audio_change", stream_url=video_src_url_ac3_aac, parameters: checkavstatus=yes/no, timeout=N | Verify device config retrieved successfully, command constructed with correct parameters |
| 3 | Create Playbin Pipeline and Load Multi-Codec Stream | Create `playbin` element via `gst_element_factory_make()`. Set `uri` property to multi-codec DASH stream URL via `g_object_set(playbin, "uri", stream_url, NULL)`. Trigger state transitions to `GST_STATE_PLAYING` via `gst_element_set_state()` | Verify playbin created, URI configured to multi-codec DASH stream, pipeline transitions to PLAYING |
| 4 | Retrieve and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via `g_object_get(playbin, "n-audio", &n_audio, NULL)`. Verify n-audio >= 2 (confirming AC3 and AAC tracks present). Query current audio index via `g_object_get(playbin, "current-audio", &current_audio, NULL)` to identify default (AC3) track | Verify n-audio returns at least 2, current-audio successfully retrieved (typically 0 for first codec) |
| 5 | Verify Initial AC3 Audio Playback and Retrieve Audio-Tags | Emit "get-audio-tags" signal for default audio track via `g_signal_emit_by_name(playbin, "get-audio-tags", 0, &tags)`. Parse tag list using `gst_tag_list_foreach()` to identify codec name (AC3). Log audio-tags including codec type, sample rate, channels as baseline. Poll playback position for 5-10 seconds to verify AC3 audio plays without interruption | Verify audio-tags successfully retrieved showing AC3 codec (e.g., audio/x-ac3), playback position advances linearly, no audio glitches or stalls |
| 6 | Switch to AAC Codec using current-audio and Flush Pipeline | Set `current-audio` property via `g_object_set(playbin, "current-audio", 1, NULL)` to switch to AAC track (index 1). Verify switch succeeded via `g_object_get(playbin, "current-audio", &current_audio, NULL)` confirming value equals 1. Query current position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Flush pipeline via `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, currentPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to clear buffered AC3 data. Wait 2 seconds for buffer refill with AAC. Reset audio underflow flag | Verify current-audio property set to 1, position query succeeds, seek-flush executes successfully, 2-second wait completes, underflow flag reset |
| 7 | Verify Second AAC Audio Playback and Retrieve Audio-Tags | After seek-flush completes, playback continues with AAC codec now active. Emit "get-audio-tags" signal for AAC track via `g_signal_emit_by_name(playbin, "get-audio-tags", 1, &tags)`. Parse tag list using `gst_tag_list_foreach()` to identify codec name (AAC). Log audio-tags including codec type, sample rate, channels. Compare logged tags from Step 5 (AC3) with current tags (AAC) to confirm different codec | Verify audio-tags successfully retrieved showing AAC codec (e.g., audio/mpeg, different from AC3), codec change confirmed through tag comparison |
| 8 | Monitor AAC Playback Progress and Validate Continuity | Poll playback position for 5-10 seconds after codec switch via `gst_element_query_position()` at 100ms intervals. Verify position advances linearly from seek-flush point with no backward jumps. Monitor bus for `pts-error-callback` signals (should be none). Check for audio underflow conditions (should be none). Verify video playback continues uninterrupted during audio codec switch | Verify AAC position advances smoothly, no pts-error or underflow signals, video continues playing, audio output clear and artifact-free |
| 9 | Validate Dual Audio Codec Support and Release Resources | Review logged audio-tags from both codec playbacks. Verify codec identity confirmed via tags: Step 5 shows AC3, Step 7 shows AAC (distinctly different). Verify test framework output shows `Failures: 0`, `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state()`. Call `gst_object_unref(playbin)` to release all resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both codecs properly identified, test completed successfully with zero failures/errors, pipeline reaches NULL state, all GStreamer resources released |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
