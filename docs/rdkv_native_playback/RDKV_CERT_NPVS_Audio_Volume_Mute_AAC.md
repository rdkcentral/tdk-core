## TestCase ID
RDKV_NATIVE_PLAYBACK_140

## TestCase Name
RDKV_CERT_NPVS_Audio_Volume_Mute_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify if audio stream playback volume can be muted (set to 0.0) on AAC codec H.264 DASH stream while maintaining continuous playback. Validate mute operation does not interrupt video/audio rendering pipeline and confirm both playbin volume level and audio-sink element "volume" property are synchronized to mute state. Verify volume control precision and pipeline stability during mute transitions.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries (mediapipelinetests<br>binary implements GStreamer playbin pipeline with GST_STREAM_VOLUME interface and westerossink video output) | Verify TDK_Package is installed, `tdk_mediapipelinetests` binary is executable, all GStreamer plugin dependencies available |
| 2 | Stream Provisioning and Configuration | AAC H.264 DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) or local file system<br> Stream URL is configured via MediaValidationVariables.py variable `video_src_url_aac` = `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"`<br> Resolves to: `http://<TM_IP>:8080/TDK_Clear_Test_Streams_Sunrise/DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd` Stream variable `video_src_url_aac` must be configured in `MediaValidationVariables.py`<br> Path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd` containing AAC audio track with H.264 video codec | Verify DASH manifest is accessible and parseable, contains H.264 video codec streams and AAC audio codec streams, stream files can be downloaded via HTTP(S) Verify `video_src_url_aac` variable resolves to valid, accessible DASH stream location with AAC audio codec and H.264 video codec available |
| 3 | Test Parameters and Volume Configuration | Test execution parameters must include: `volume_set="0"` (CUBIC scale: 0 = mute, 1.0 = maximum volume), `timeout="10"` seconds (playback duration at mute state) | Verify volume_set=0 parameter is configured for mute validation, timeout=10 seconds is set for playback monitoring duration |
| 4 | Platform-Specific Environment and GStreamer Configuration |  Platform-specific environment variables must be defined in `/opt/TDK/TDK.env`: `WAYLAND_DISPLAY` (Wayland display server),<br>`XDG_RUNTIME_DIR` (runtime directory for Wayland sockets),<br>`LD_PRELOAD` with vendor audio/video libraries, `GST_PLUGIN_PATH` (GStreamer plugin directory). GStreamer must have: playbin element, westerossink video sink, and GST_STREAM_VOLUME interface implementation  | Verify `/opt/TDK/TDK.env` exists with all environment variables, Wayland display functional, GStreamer 1.16+ installed with playbin, westerossink, and GST_STREAM_VOLUME support in GST_PLUGIN_PATH |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration (GST_PLUGIN_PATH, LD_PRELOAD, WAYLAND_DISPLAY, XDG_RUNTIME_DIR). Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Verify GStreamer library version and confirm `playbin` and `GST_STREAM_VOLUME` interface availability  | Verify all environment variables load correctly from TDK.env, Wayland display is created successfully, logging initialized without errors, GStreamer 1.16+ with playbin and GST_STREAM_VOLUME support confirmed |
| 2 | Create Playbin Element and Configure DASH AAC Stream |  Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Configure `uri` property to DASH AAC stream URL<br>via `g_object_set(playbin, "uri", stream_url, NULL)` where stream_url = `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` (resolves to full HTTP/HTTPS path from MediaValidationVariables.py). Set `video-sink` property to `westerossink`<br>via `g_object_set(playbin, "video-sink", westerossink, NULL)` for video rendering  | Verify playbin element created successfully, `uri` property configured to DASH_H264_AAC stream location, `video-sink` property set to westerossink, stream file accessible |
| 3 | Transition Pipeline to Playing State | Set pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` to begin AAC stream playback at initial full volume<br> Play stream for 5 seconds at full volume to establish stable playback | Verify pipeline state transitions to PLAYING state, playback begins without errors, stream data flowing to decoders |
| 4 | Query Initial Playbin Volume Before Mute |  Query current playbin volume using `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin),<br>GST_STREAM_VOLUME_FORMAT_CUBIC)` to capture initial volume level. Expected value: 1.0 representing 100% volume on CUBIC scale  | Verify volume query returns 1.0 confirming playbin initialized with full volume |
| 5 | Set Playbin Volume to Mute (0.0) Using gst_stream_volume_set_volume API |  Execute volume mute operation<br>via `gst_stream_volume_set_volume(GST_STREAM_VOLUME(playbin),<br>GST_STREAM_VOLUME_FORMAT_CUBIC, 0.0)` to set playbin volume to 0.0 (complete mute on CUBIC scale). Immediately verify mute was applied by calling `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin),<br>GST_STREAM_VOLUME_FORMAT_CUBIC)` - should return 0.0  | Verify `gst_stream_volume_set_volume()` call completes successfully, immediate follow-up query via `gst_stream_volume_get_volume()` returns 0.0 confirming mute applied |
| 6 | Monitor Playback Position During Mute State (10 seconds) |  Continue playback for 10 seconds while volume is muted (0.0). Query playback position every 100ms<br>via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` to verify position advances at expected rate (1 second position per 1 second real-time +/-250ms tolerance))<br>with no backward jumps  | Verify playback position advances continuously during 10-second mute period within +/-250ms tolerance per second, no backward position jumps detected, playback continues smoothly despite mute |
| 7 | Verify Final Mute State and Release Resources |  Query final playbin volume<br>via `gst_stream_volume_get_volume(GST_STREAM_VOLUME(playbin), GST_STREAM_VOLUME_FORMAT_CUBIC)` - should still return 0.0. Verify test framework output shows `Failures: 0` and `Errors: 0`. Set pipeline to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)` to stop playback. Unreference GStreamer objects: `gst_object_unref(playbin)`, `gst_object_unref(westerossink)`  | Verify final volume query returns 0.0 confirming mute maintained throughout playback, test execution shows `Failures: 0, Errors: 0`, pipeline transitions to GST_STATE_NULL, all objects unreferenced and resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121






