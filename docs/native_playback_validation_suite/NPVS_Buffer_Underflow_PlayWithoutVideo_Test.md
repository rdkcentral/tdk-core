## TestCase ID
NATIVE_PLAYBACK_146

## TestCase Name
NPVS_Buffer_Underflow_PlayWithoutVideo_Test

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify video buffer underflow signal detection and audio-only playback recovery without video output. Monitor buffer-underflow-callback signal when video buffer depletes during continuous playback, then validate pipeline recovery by pausing, seeking to restart point, and resuming audio playback without video rendering. Specifically test underflow detection on H.264 video stream using GStreamer westerossink callback mechanism and verify post-recovery audio frame statistics while video remains in underflow state.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests binary implements GStreamer playbin pipeline with westerossink video sink and audio sink for underflow detection and audio-only playback) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer audio/video plugin dependencies available |
| 2 | Media Stream Provisioning | Video buffer underflow test stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream URL is configured via MediaValidationVariables.py variable `video_src_url_underflow_stream` = `test_streams_base_path + "TDK_Asset_Sunrise_underflow_stream_v2.mp4"`. This specialized stream contains intentional video buffer starvation points for underflow testing with embedded audio track | Verify video underflow stream file is accessible and readable from filesystem |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_underflow_stream` must be configured in `MediaValidationVariables.py`. Path: `TDK_Asset_Sunrise_underflow_stream_v2.mp4` containing embedded underflow trigger points and audio stream for audio-only playback | Verify `video_src_url_underflow_stream` variable resolves to valid, accessible video underflow stream with audio component |
| 4 | Device Configuration Parameters | Test execution parameters must be retrieved from device configuration file: , `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for playback duration, `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_START_POINT` and `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` (seek positions for underflow recovery) | Verify all device config parameters are accessible and contain valid values |
| 5 | Platform-Specific Environment and GStreamer Configuration | Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server), `XDG_RUNTIME_DIR` (runtime directory for Wayland sockets), `LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, westerossink video sink, audio sink elements, and buffer-underflow-callback support on westerossink | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin, westerossink, and audio elements supporting underflow signals in GST_PLUGIN_PATH |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm playbin, westerossink, and audio element availability | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and audio/video elements confirmed |
| 2 | Retrieve Device Configuration and Stream Parameters | Retrieve configuration parameters from device config file:`NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (playback duration before underflow check), `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_START_POINT` (seek start position after underflow), `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` (playback duration before expected underflow). Retrieve stream URL from `MediaValidationVariables.video_src_url_underflow_stream` | Verify all configuration values retrieved successfully, stream URL resolves to valid video underflow test file path |
| 3 | Create Playbin Element and Configure Video Underflow Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to video underflow stream via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "TDK_Asset_Sunrise_underflow_stream_v2.mp4"`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `element-setup` signal via `g_signal_connect()` to discover westerossink and audio sink elements during pipeline construction | Verify playbin element created successfully, `uri` property configured to video underflow stream path, `video-sink` set to westerossink, `element-setup` signal will enable element discovery |
| 4 | Register Westerossink Buffer Underflow Callback for Signal Detection | During `element-setup` signal callback, identify westerossink element and register underflow detection callback: `g_signal_connect(westerossink, "buffer-underflow-callback", G_CALLBACK(callback_func), &video_underflow_received)`. Within the callback, query `g_object_get(westerossink, "queued-frames", &queued_frames, NULL)` to capture queued frame count at underflow moment. Callback sets `video_underflow_received = true` when signal is received | Verify westerossink buffer-underflow-callback is registered successfully |
| 5 | Transition Pipeline to Playing and Wait for Underflow Signal | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin combined audio/video stream playback. Continuously poll playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms. Play stream for duration specified in `NATIVE_PLAYBACK_UNDERFLOW_VIDEO_END_POINT` seconds while monitoring for `buffer-underflow-callback` signal from westerossink | Verify pipeline transitions to PLAYING state, audio and video playback begins without errors, `video_underflow_received` flag becomes true when westerossink detects buffer starvation |
| 6 | Verify Video Buffer Underflow Signal Reception and Audio Continuation | Validate that `video_underflow_received == true` indicating westerossink properly emitted buffer-underflow-callback signal when video buffer depleted. Confirm audio continues rendering frames via audio sink (audio-only playback state without video) | Verify video underflow signal was properly detected, audio frames continue rendering at expected rate |
| 7 | Continue Playback in Audio-Only Mode After Video Underflow | Pipeline remains in `GST_STATE_PLAYING` without pause or seek operation. Continuously monitor playback continuation by querying audio sink statistics every 1 second via `g_object_get(audio_sink, "stats", &stats_structure)` and retrieve rendered audio frames via `gst_structure_get_uint64(stats_structure, "rendered", &audio_frames)`. Verify audio frames counter increments continuously at expected rate while video remains in underflow state. Continue monitoring for minimum 5-10 seconds to establish stable audio-only playback pattern (no pause/resume cycle) | Verify pipeline remains in PLAYING state without interruption, audio sink renders audio frames at expected rate, frame counter increments continuously (no audio stalls or gaps), audio-only playback established smoothly |
| 8 | Validate Test Success and Release Resources | Query final playback position via `gst_element_query_position()`. Verify test framework output shows `Failures: 0` and `Errors: 0`. Confirm audio frame statistics show continuous rendering without drops or extended silence. Verify video remains in underflow state (video frames not rendering) while audio continues uninterrupted for entire monitoring period. Set pipeline to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects via `gst_object_unref()` | Verify final position advances steadily, test shows no failures/errors, audio frame rendering statistics confirm continuous stable playback without underflow recovery seeking, video remains muted throughout test, pipeline reaches GST_STATE_NULL, all resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
