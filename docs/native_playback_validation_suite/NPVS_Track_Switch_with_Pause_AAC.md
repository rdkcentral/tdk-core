## TestCase ID
NATIVE_PLAYBACK_131

## TestCase Name
NPVS_Track_Switch_with_Pause_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify if dynamic audio track switching is possible during pause/resume state transitions while maintaining playback position consistency using GStreamer playbin `current-audio` property. Validate that audio tracks can be switched between different tracks (same AAC codec) in the same multi-track stream with pause-resume operations without interrupting video playback or causing position discontinuities. Specifically validate audio rendering quality, position synchronization during pause, and track switching timing accuracy during paused state.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Multi-track AAC stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_MultiTrack_AAC.mp4"` in MediaValidationVariables.py (stream contains multiple AAC audio tracks for track switching validation with pause operations) | Verify multi-track AAC stream file is accessible and readable, multiple AAC audio tracks are present in stream |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_multi_audio_aac` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_MultiTrack_AAC.mp4` (stream must contain at least 2 AAC audio tracks with same codec) | Verify `video_src_url_multi_audio_aac` resolves to valid, accessible multi-track AAC stream location with multiple tracks |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration must be set to time duration (in seconds) for audio track switch validation with pause operations. Typical value: 20 seconds total (10 seconds per track with pause-resume cycles) | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load Multi-Track AAC Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)` and configure `uri` property to multi-track stream path via `g_object_set(playbin, "uri", stream_url, NULL)`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Verify playbin element created successfully, `uri` property configured to multi-track AAC stream containing multiple AAC tracks, `video-sink` property is set |
| 3 | Retrieve Stream Properties and Verify Multiple Audio Tracks | Query playbin to determine number of audio streams via `g_object_get(playbin, "n-audio", &n_audio, NULL)`. Verify that stream contains at least 2 audio tracks (multiple AAC tracks). Query current audio stream index via `g_object_get(playbin, "current-audio", &current_audio, NULL)` to identify starting audio track | Verify n-audio value is at least 2 (confirming multiple AAC track presence), current audio stream index successfully retrieved |
| 4 | Verify Default Audio Playback (First AAC Track) and Execute Pause-Resume Cycle | Set pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`. Transition pipeline to `GST_STATE_PLAYING` via `gst_element_set_state()` to start playback with default (first) audio track (AAC codec, index 0). Record initial playback position via `gst_element_query_position()`. Emit "get-audio-tags" signal to retrieve codec metadata via `g_signal_emit_by_name(playbin, "get-audio-tags", 0, &tags)`. Log audio-tags for baseline verification. Transition to `GST_STATE_PAUSED` via `gst_element_set_state()` and verify position stops advancing. Query position during pause to confirm it remains at recorded value Â±10ms | Verify pipeline state transitions to PLAYING with first AAC track, audio-tags successfully retrieved and logged, pipeline transitions to PAUSED, position stops advancing during pause |
| 5 | Monitor First Track Playback and Resume from Pause | Transition pipeline back to `GST_STATE_PLAYING` via `gst_element_set_state()`. Verify playback resumes from paused position without position jumps via `gst_element_query_position()`. Poll playback position at 100ms intervals for 3-5 seconds. Verify position advances at expected rate (1 second position per 1 second real-time Â±250ms tolerance) from resumed position. Monitor `pts-error-callback` signal to detect presentation timestamp errors. Confirm first AAC track continues rendering smoothly without glitches | Verify playback resumes without position jumps, position advances linearly from paused point, no `pts-error-callback` signals detected, first AAC track rendering stable after resume |
| 6 | Switch Audio Track During Paused State | Set pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()` while first AAC track is playing. Record position at pause point. Set `current-audio` property via `g_object_set(playbin, "current-audio", 1, NULL)` to switch from first AAC track (index 0) to second AAC track (index 1) during paused state. Verify audio stream switches successfully by querying `current-audio` property via `g_object_get(playbin, "current-audio", &current_audio, NULL)`. Flush pipeline using `gst_element_send_event(playbin, gst_event_new_flush_start())` followed by `gst_element_send_event(playbin, gst_event_new_flush_stop())` to clear buffered audio and synchronize with new track | Verify `current-audio` property successfully set to index 1 during pause, pipeline flush events processed successfully, confirmation query returns value 1 |
| 7 | Verify Second Track Playback After Pause-Resume-Switch Cycle | Transition pipeline to `GST_STATE_PLAYING` via `gst_element_set_state()` to resume playback with second AAC track now active. Emit "get-audio-tags" signal to retrieve codec metadata for second audio track via `g_signal_emit_by_name(playbin, "get-audio-tags", 1, &tags)`. Parse tag list and log audio-tags to verify track switch. Query playback position via `gst_element_query_position()` to confirm position advances from paused point. Compare logged audio-tags from Step 4 (first AAC track) with current audio-tags (second AAC track) to confirm track change | Verify second AAC track audio-tags successfully retrieved and logged, track change confirmed through audio-tags comparison, playback position advances from previous paused point |
| 8 | Monitor Second Track Playback and Execute Pause-Resume During Second Track | Poll playback position via `gst_element_query_position()` at 100ms intervals for 3-5 seconds. Verify position advances at expected rate (1 second position per 1 second real-time Â±250ms tolerance). Transition pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`. Record position during pause and verify it stops advancing (Â±10ms tolerance). Transition back to `GST_STATE_PLAYING` via `gst_element_set_state()`. Verify playback resumes without position jumps and continues advancing at expected rate. Monitor `pts-error-callback` signal throughout pause-resume cycle | Verify second AAC track position advances linearly, pause stops position advance, resume continues from paused point without jumps, no `pts-error-callback` signals detected, second track rendering stable through pause-resume cycle |
| 9 | Validate Multi-Track Support with Pause-Resume Cycling | Review logged audio-tags from Step 4 (first AAC track) and Step 7 (second AAC track). Verify both codec names are AAC and track change is confirmed. Confirm all position queries during pause/resume cycles show expected behavior (position halts during pause, resumes without jumps). Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state()`. Unreference playbin element via `gst_object_unref()` to release all codec decoders, audio sink, demultiplexer resources. Free allocated memory and close logging file | Verify audio-tags logs confirm both AAC tracks were active, track switching during pause validated, position behavior during pause-resume cycles confirmed correct, test execution completed successfully, pipeline reaches `GST_STATE_NULL`, all GStreamer resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
