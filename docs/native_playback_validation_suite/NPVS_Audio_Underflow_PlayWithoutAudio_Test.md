**TestCase ID**
NATIVE_PLAYBACK_143

**TestCase Name**
NPVS_Audio_Underflow_PlayWithoutAudio_Test

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate audio buffer underflow detection and recovery during intentional data starvation. The test registers callback handlers for "buffer-underflow-callback" signals on the audio pipeline, then intentionally starves the audio data feed to trigger underflow conditions. Verify underflow callback signals are received when audio demux buffer becomes depleted, confirming proper signal delivery and handler execution. Once data supply resumes, validate pipeline recovers and audio rendering recommences without extended silence or glitches. Confirm underflow recovery maintains audio/video synchronization and does not introduce codec state corruption or permanent failure conditions.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | Media stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) | Verify stream is accessible and appropriate demuxer can parse the stream |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with valid HTTPS URL or local file path | Verify stream URL resolves to valid, accessible stream location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm playbin, audio, and video element availability | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and audio/video elements confirmed |
| 2 | Retrieve Device Configuration and Stream Parameters | Retrieve configuration parameters from device config file: `NATIVE_PLAYBACK_CHECK_AV_STATUS`, `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT`, `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_START_POINT`, `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_END_POINT`, `NATIVE_PLAYBACK_AVSYNC_ENABLED` (indicates audio/video sync state). Retrieve stream URL from `MediaValidationVariables.video_src_url_audio_underflow` | Verify all configuration values retrieved successfully, stream URL resolves to valid audio underflow test file path |
| 3 | Create Playbin Element and Configure Audio Underflow Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to audio underflow stream via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "TDK_Asset_Audio_underflow_v2.mp4"`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `element-setup` signal via `g_signal_connect()` to discover audio decoder and audio sink elements during pipeline construction | Verify playbin element created successfully, `uri` property configured to audio underflow stream path, `video-sink` set to westerossink, `element-setup` signal will enable audio element discovery |
| 4 | Register Audio Element Underflow Callbacks | During `element-setup` signal callback, identify audio decoder and audio sink elements and register underflow detection callbacks: `g_signal_connect(audio_decoder_element, "buffer-underflow-callback", G_CALLBACK(callback_func), &audio_underflow_received)` and `g_signal_connect(audio_sink_element, "underrun-callback", G_CALLBACK(callback_func), &audio_underflow_received)`. Callback sets `audio_underflow_received = true` when signal is received | Verify audio element callbacks are registered successfully on correct elements (decoder and sink) |
| 5 | Transition Pipeline to Playing and Wait for Audio Underflow Signal | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin combined audio/video stream playback. Continuously poll video position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms. Play stream for duration specified in `NATIVE_PLAYBACK_UNDERFLOW_AUDIO_END_POINT` seconds while monitoring for `buffer-underflow-callback` or `underrun-callback` signals from audio elements | Verify pipeline transitions to PLAYING state, audio and video playback begins without errors, `audio_underflow_received` flag becomes true when audio buffer starves |
| 6 | Verify Audio Underflow Signal Reception and Video Continuation | Validate that `audio_underflow_received == true` indicating audio element properly emitted underflow signal when audio buffer depleted. Confirm video continues rendering frames via westerossink (video-only playback state without audio) | Verify audio underflow signal was properly detected, video frames continue rendering at expected rate |
| 7 | Continue Playback in Video-Only Mode After Audio Underflow | Pipeline remains in `GST_STATE_PLAYING` without pause or seek operation. Continuously monitor playback continuation by querying westerossink statistics every 1 second via `g_object_get(westerossink, "stats", &stats_structure)` and retrieve rendered video frames via `gst_structure_get_uint64(stats_structure, "rendered", &video_frames)`. Verify video frames counter increments continuously at expected rate while audio remains in underflow state. Continue monitoring for minimum 5-10 seconds to establish stable video-only playback pattern (no pause/resume cycle) | Verify pipeline remains in PLAYING state without interruption, westerossink renders video frames at expected rate, frame counter increments continuously (no video stalls or gaps), video-only playback established smoothly |
| 8 | Validate Test Success and Release Resources | Query final playback position via `gst_element_query_position()`. Verify test framework output shows `Failures: 0` and `Errors: 0`. Confirm video frame statistics show continuous rendering without drops or extended silence. Verify audio remains in underflow state (audio frames not rendering) while video continues uninterrupted for entire monitoring period. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects via `gst_object_unref()` | Verify final position advances steadily, test shows no failures/errors, video frame rendering statistics confirm continuous stable playback without underflow recovery seeking, audio remains muted throughout test, pipeline reaches GST_STATE_NULL, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
