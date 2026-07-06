## TestCase ID
NATIVE_PLAYBACK_128

## TestCase Name
NPVS_Track_Switch_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify if dynamic audio track switching is possible while maintaining video playback continuity using GStreamer playbin `current-audio` property. Validate that audio tracks can be switched between different tracks (same AAC codec) in the same multi-track stream without interrupting video playback. Specifically validate audio rendering quality, position synchronization, and track switching timing accuracy using `g_object_set(playbin, "current-audio", track_index, NULL)` property during active playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-track AAC stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_AAC.mp4"` in MediaValidationVariables.py (stream contains multiple AAC audio tracks for track switching validation) | Verify multi-track AAC stream file is accessible and readable, multiple AAC audio tracks are present in stream |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_multi_audio_aac` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_MultiTrack_AAC.mp4` (stream must contain at least 2 AAC audio tracks with same codec) | Verify `video_src_url_multi_audio_aac` resolves to valid, accessible multi-track AAC stream location with multiple tracks |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration must be set to time duration (in seconds) for audio track switch validation. Typical value: 10 seconds playback per track configuration to ensure sufficient sampling | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load Multi-Track AAC Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)` and configure `uri` property to multi-track stream path via `g_object_set(playbin, "uri", stream_url, NULL)`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Verify playbin element created successfully, `uri` property configured to multi-track AAC stream containing multiple AAC tracks, `video-sink` property is set |
| 3 | Retrieve Stream Properties and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via `g_object_get(playbin, "n-audio", &n_audio, NULL)`. Verify that stream contains at least 2 audio tracks (multiple AAC tracks). Query current audio stream index via `g_object_get(playbin, "current-audio", &current_audio, NULL)` to identify starting audio track | Verify n-audio value is at least 2 (confirming multiple AAC track presence), current audio stream index successfully retrieved |
| 4 | Verify Default Audio Playback (First AAC Track) and Retrieve Audio-Tags | Set pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`. Transition pipeline to `GST_STATE_PLAYING` via `gst_element_set_state()` to start playback with default (first) audio track (AAC codec, index 0). Emit "get-audio-tags" signal to retrieve codec metadata via `g_signal_emit_by_name(playbin, "get-audio-tags", 0, &tags)`. Parse tag list using `gst_tag_list_foreach()` to identify codec name (AAC). Log retrieved audio-tags including codec type, sample rate, channels for baseline verification | Verify pipeline state transitions to PLAYING with first AAC audio track, playback position advances linearly, audio-tags successfully retrieved and logged showing AAC codec information, default track playback verified |
| 5 | Monitor First Audio Track Playback Progress | Poll playback position via `gst_element_query_position()` at 100ms intervals for configured timeout duration (e.g., 5-10 seconds). Verify position advances at expected rate (1 second position per 1 second real-time Â±250ms tolerance). Monitor `pts-error-callback` signal to detect presentation timestamp errors during first AAC track playback. Check for audio underflow conditions via underflow callback monitoring. Confirm first AAC track is rendering smoothly without glitches or interruptions | Verify first AAC track playback position advances linearly, no backward jumps, no `pts-error-callback` signals detected, no audio underflow signals, first AAC track rendering confirmed stable and continuous |
| 6 | Switch to Second Audio Track using current-audio Signal and Flush Pipeline | Set `current-audio` property via `g_object_set(playbin, "current-audio", 1, NULL)` to switch from first AAC track (index 0) to second AAC track (index 1). Verify audio stream switches successfully by querying `current-audio` property via `g_object_get(playbin, "current-audio", &current_audio, NULL)`. Flush pipeline using `gst_element_send_event(playbin, gst_event_new_flush_start())` followed by `gst_element_send_event(playbin, gst_event_new_flush_stop())` to clear buffered audio and synchronize with new track. Confirm `current-audio` query returns value 1 (second track index confirmed) | Verify `current-audio` property successfully set to index 1, pipeline flush-start and flush-stop events processed successfully, confirmation query returns value 1, audio switch ready for second track playback without stale buffers |
| 7 | Verify Second Audio Track Playback (Second AAC Track) and Retrieve Audio-Tags | After pipeline flush, playback continues automatically with second AAC track now active. Emit "get-audio-tags" signal to retrieve codec metadata for second audio track via `g_signal_emit_by_name(playbin, "get-audio-tags", 1, &tags)`. Parse tag list using `gst_tag_list_foreach()` to identify codec name (AAC). Log retrieved audio-tags including codec type, sample rate, channels to verify track switch from first to second AAC track. Compare logged audio-tags from Step 4 (first AAC track) with current audio-tags (second AAC track) to confirm track change | Verify second AAC track audio-tags successfully retrieved and logged showing AAC codec information, track change confirmed through audio-tags retrieval, second track playback verified active |
| 8 | Monitor Second Audio Track Playback Progress During Track Switch | Poll playback position via `gst_element_query_position()` at 100ms intervals for configured timeout duration (e.g., 5-10 seconds) after track switch. Verify position advances at expected rate (1 second position per 1 second real-time Â±250ms tolerance) with no backward jumps from pre-flush position. Monitor `pts-error-callback` signal to detect presentation timestamp errors during second AAC track playback. Check for audio underflow conditions via underflow callback monitoring. Confirm second AAC track is rendering smoothly after track change | Verify second AAC track playback position advances linearly from flush point, no backward jumps or position glitches, no `pts-error-callback` signals detected, no audio underflow signals, second AAC track rendering confirmed stable and continuous |
| 9 | Validate Multiple Audio Track Support using Audio-Tags Logs | Review logged audio-tags from Step 4 (first AAC track tags) and Step 7 (second AAC track tags). Verify codec names are both AAC but confirm track change occurred by comparing tag details (sample rate, channels may differ between tracks). Confirm both audio track tags were successfully retrieved, parsed, and logged. Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state()`. Unreference playbin element via `gst_object_unref()` to release all codec decoders, audio sink, demultiplexer resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both AAC tracks were active and properly identified, test execution completed successfully with multi-track validation via tags comparison, no failures or errors in test output, pipeline reaches `GST_STATE_NULL`, all GStreamer resources released, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
