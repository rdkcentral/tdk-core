**TestCase ID**
NATIVE_PLAYBACK_148

**TestCase Name**
NPVS_Buffer_Underflow_Signal_Test

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify video buffer underflow signal detection capability on westerossink element without recovery validation. Monitor buffer-underflow-callback signal when video buffer depletes during continuous playback, then validate signal was properly emitted with queued-frames state captured. Specifically test underflow signal generation on H.264 video stream using GStreamer westerossink callback mechanism and verify signal propagates correctly when buffer starvation occurs.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests binary implements GStreamer playbin pipeline with westerossink video sink for underflow signal detection) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer video plugin dependencies available |
| 2 | Media Stream Provisioning | Video buffer underflow test stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream URL is configured via MediaValidationVariables.py variable `video_src_url_underflow_stream` = `test_streams_base_path + "TDK_Asset_Sunrise_underflow_stream_v2.mp4"`. This specialized stream contains intentional video buffer starvation points for underflow signal generation | Verify video underflow stream file is accessible and readable from filesystem |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_underflow_stream` must be configured in `MediaValidationVariables.py`. Path: `TDK_Asset_Sunrise_underflow_stream_v2.mp4` containing embedded underflow trigger points | Verify `video_src_url_underflow_stream` variable resolves to valid, accessible video underflow stream location |
| 4 | Device Configuration Parameters | Test execution parameters must be retrieved from device configuration file: `NATIVE_PLAYBACK_CHECK_AV_STATUS` (default: "no") for audio/video verification, `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for playback duration, `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` (playback duration before expected underflow signal) | Verify all device config parameters are accessible and contain valid values |
| 5 | Platform-Specific Environment and GStreamer Configuration | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, westerossink video sink, and buffer-underflow-callback support | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin and westerossink supporting underflow signals in GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm playbin and westerossink availability | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and westerossink confirmed |
| 2 | Retrieve Device Configuration and Stream Parameters | Retrieve configuration parameters from device config file: `NATIVE_PLAYBACK_CHECK_AV_STATUS` (for AV verification mode), `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration before underflow check), `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` (playback duration before expected underflow signal). Retrieve stream URL from `MediaValidationVariables.video_src_url_underflow_stream` | Verify all configuration values retrieved successfully, stream URL resolves to valid video underflow test file path |
| 3 | Create Playbin Element and Configure Video Underflow Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to video underflow stream via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "TDK_Asset_Sunrise_underflow_stream_v2.mp4"`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `element-setup` signal via `g_signal_connect()` to discover westerossink element | Verify playbin element created successfully, `uri` property configured to video underflow stream path, `video-sink` property set to westerossink, `element-setup` signal will enable westerossink discovery |
| 4 | Register Westerossink Buffer Underflow Callback for Signal Detection | During `element-setup` signal callback, identify westerossink element and register underflow detection callback: `g_signal_connect(westerossink, "buffer-underflow-callback", G_CALLBACK(callback_func), &video_underflow_received)`. Within the callback, query `g_object_get(westerossink, "queued-frames", &queued_frames, NULL)` to capture queued frame count at underflow moment. Callback sets `video_underflow_received = true` when signal is received | Verify westerossink buffer-underflow-callback is registered successfully |
| 5 | Transition Pipeline to Playing and Monitor for Underflow Signal | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin video stream playback. Continuously poll playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms. Play stream for duration specified in `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` seconds while monitoring for `buffer-underflow-callback` signal | Verify pipeline transitions to PLAYING state, playback begins without errors, `video_underflow_received` flag becomes true when westerossink emits underflow signal |
| 6 | Verify Underflow Signal Reception and Cleanup | Validate that `video_underflow_received == true` indicating westerossink properly emitted buffer-underflow-callback signal when video buffer depleted. Confirm queued_frames captured in callback shows depletion state. Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects via `gst_object_unref()` | Verify underflow signal was properly detected and flag set to true, test shows no failures/errors, pipeline reaches GST_STATE_NULL, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
