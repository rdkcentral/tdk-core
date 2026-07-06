## TestCase ID
NATIVE_PLAYBACK_139

## TestCase Name
NPVS_Audio_Volume_Stress_OPUS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Stress test to verify audio volume control stability and synchronization by rapidly cycling through multiple volume levels `{1.0 (100%), 0.75 (75%), 0.5 (50%), 0.25 (25%), 0.0 (mute)}` on OPUS codec H.264 DASH stream. Validate that `gst_stream_volume_set_volume()` and `gst_stream_volume_get_volume()` GStreamer APIs function correctly under repeated rapid volume changes without audio/video artifacts, pipeline interruption, or synchronization issues. Verify continuous playback with position advancement despite rapid volume transitions across the CUBIC volume scale.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests binary implements GStreamer playbin pipeline with GST_STREAM_VOLUME interface and westerossink video output) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer plugin dependencies available |
| 2 | Media Stream Provisioning | OPUS H.264 DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) or local file system. Stream URL is configured via MediaValidationVariables.py variable `video_src_url_opus` = `test_streams_base_path + "DASH_H264_OPUS/atfms_291_dash_tdk_avc_opus_fmp4.mpd"`. Resolves to: `http://<TM_IP>:8080/TDK_Clear_Test_Streams_Sunrise/DASH_H264_OPUS/atfms_291_dash_tdk_avc_opus_fmp4.mpd` | Verify DASH manifest is accessible and parseable, contains H.264 video codec streams and OPUS audio codec streams, stream files can be downloaded via HTTP(S) |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_opus` must be configured in `MediaValidationVariables.py`. Path: `DASH_H264_OPUS/atfms_291_dash_tdk_avc_opus_fmp4.mpd` containing OPUS audio track with H.264 video codec | Verify `video_src_url_opus` variable resolves to valid, accessible DASH stream location with OPUS audio codec and H.264 video codec available |
| 4 | Test Parameters and Volume Stress Configuration | Test execution parameters must include: volume stress levels = `{1.0, 0.75, 0.5, 0.25, 0.0}` (CUBIC scale), playback duration per level = `15` seconds (5 seconds initial + 10 seconds continued), timeout = `75` seconds total (5 levels Ã— 15 seconds each) | Verify volume_stress_levels are defined, 15-second duration per level configured, total timeout set to 75 seconds |
| 5 | Platform-Specific Environment and GStreamer Configuration | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, westerossink video sink, and GST_STREAM_VOLUME interface implementation | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin, westerossink, and GST_STREAM_VOLUME support in GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm `playbin` and `GST_STREAM_VOLUME` interface availability | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and GST_STREAM_VOLUME support confirmed |
| 2 | Create Playbin Element and Configure DASH OPUS Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to DASH OPUS stream URL via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "DASH_H264_OPUS/atfms_291_dash_tdk_avc_opus_fmp4.mpd"` (resolves to full HTTP/HTTPS path from MediaValidationVariables.py). Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)` for video rendering | Verify playbin element created successfully, `uri` property configured to DASH_H264_OPUS stream location, `video-sink` property set to westerossink, stream file accessible |
| 3 | Transition Pipeline to Playing State and Initial Playback | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin OPUS stream playback at initial full volume (1.0). Play stream for 5 seconds at full volume to establish stable playback | Verify pipeline state transitions to PLAYING state, playback begins without errors, stream data flowing to decoders |
| 4 | Execute Volume Stress Loop - Set First Volume Level (1.0) | Query current playbin volume using `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin), GST_STREAM_VOLUME_FORMAT_CUBIC)`. Expected value: 1.0 representing 100% volume on CUBIC scale | Verify volume query returns 1.0 confirming playbin initialized with full volume |
| 5 | Execute Volume Stress Loop - Cycle Through 5 Volume Levels | Execute stress loop cycling through volume levels `{1.0, 0.75, 0.5, 0.25, 0.0}` in descending order. For each volume level: (a) Set volume via `gst_stream_volume_set_volume(GST_STREAM_VOLUME(playbin), GST_STREAM_VOLUME_FORMAT_CUBIC, volume_level)`, (b) Immediately verify mute was applied via `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin), GST_STREAM_VOLUME_FORMAT_CUBIC)` - should return exact volume_level set, (c) Continue playback for 15 seconds at that volume level, (d) Query playback position every 100ms via `gst_element_query_position()` to verify smooth position advancement during volume change | Verify for each volume level: `gst_stream_volume_set_volume()` call completes successfully, immediate follow-up `gst_stream_volume_get_volume()` returns expected volume level, playback continues smoothly without audio artifacts or interruptions, position advances at expected rate (Â±250ms tolerance per second) |
| 6 | Monitor Continuous Playback During All Volume Transitions | Throughout the entire stress loop (75 seconds total across all 5 levels), continuously monitor position advancement and verify no backward jumps or stalls occur. Verify pipeline remains in `PLAYING` state despite rapid volume changes | Verify playback position advances continuously across all volume level transitions within Â±250ms tolerance per second, no backward position jumps detected, no audio/video artifacts reported, pipeline maintains `GST_STATE_PLAYING` |
| 7 | Verify Final State and Release Resources | Query final playbin volume via `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin), GST_STREAM_VOLUME_FORMAT_CUBIC)` - should return 0.0 (last level in stress loop). Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects: `gst_object_unref(playbin)`, `gst_object_unref(westerossink)` | Verify final volume query returns 0.0 confirming last volume level (mute) maintained, test execution shows `Failures: 0, Errors: 0`, all volume transitions completed without errors, pipeline transitions to GST_STATE_NULL, all objects unreferenced and resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes (75 seconds stress test + setup/cleanup overhead)

**Priority:** High

**Release Version:** M121
