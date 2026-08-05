## TestCase ID
RDKV_NATIVE_PLAYBACK_154

## TestCase Name
RDKV_CERT_NPVS_Low_Bitrate_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate H.264 video playback at low bitrate using playbin element with westerossink video rendering. Test applies fixed connection_speed=300 kbps and height=180p across all supported devices (no device-specific adjustment). Verify frame rendering performance and A/V synchronization are maintained during sustained low-bitrate playback continuous monitoring of and playback position. Confirm no frame drops or stalls occur during low-bitrate H.264 playback, validating video decoder and rendering pipeline capacity for constrained-bandwidth streams.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent GStreamer libraries including H.264 decoder | Verify TDK_Package is installed, binary is executable, all libraries are available, H.264 decoder plugins loaded |
| 2 | Stream Provisioning and Configuration |  DASH stream with H.264 video at low bitrate must be accessible via HTTP/HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`). Stream file path configured as `video_src_url_bitrate_h264` in MediaValidationVariables.py (external stream). Stream contains H.264 video at low bitrate (300 kbps))<br>and AAC audio (Fixed properties for all devices: connection_speed=300 kbps, height=180))<br>Stream variable `video_src_url_bitrate_h264` configured in `MediaValidationVariables.py` with external DASH stream URL containing H.264 video at low bitrate. Fixed connection_speed=300 kbps and height=180 properties applied uniformly across all supported models  | Verify DASH stream accessible with low bitrate capability, dashdemux available for MPD parsing at 300 kbps and 180p resolution Verify `video_src_url_bitrate_h264` resolves to valid external DASH manifest with fixed connection_speed=300, height=180 applied to all devices |
| 3 | Playback Timeout and AV Status Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config file | Verify timeout is set to minimum 10 seconds |
| 4 | Platform-Specific Environment Variables |  Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, `GST_PLUGIN_PATH`))<br>must be defined in `/opt/TDK/TDK.env` for low-bitrate H.264 playback support on Video_Accelerator and RPI-Client devices  | Verify `/opt/TDK/TDK.env` exists with all required environment variables for H.264 decoding at 180p resolution |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Apply Fixed Device Properties |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer H.264 decoder plugins and vendor libraries<br>via `LD_PRELOAD`. Establish Wayland display session<br>via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Apply fixed connection_speed property (300 kbps))<br>and height property (180))<br>uniformly across all supported device types  | Verify all environment variables load correctly, H.264 plugins available, Wayland display created, fixed connection_speed=300 and height=180 properties applied |
| 2 | Retrieve Configuration and Construct Playbin Pipeline with Low-Bitrate Properties |  Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device config file. Apply fixed connection_speed property (300 kbps))<br>and height property (180). Retrieve stream variable `video_src_url_bitrate_h264` from MediaValidationVariables.py. Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Set URI property<br>via `g_object_set(playbin, "uri", <stream_url>, NULL)`  | Verify playbin element created with connection_speed=300/height=180 properties, stream URL configured for H.264 low-bitrate playback |
|  3  |  Configure Westerossink and Register Callbacks  |   Create `westerossink` element<br>via `gst_element_factory_make("westerossink", NULL)`. Connect as video sink<br>via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal<br>via `g_signal_connect()` to verify rendering begins. Set playback flags to `GST_PLAY_FLAG_VIDEO` and `GST_PLAY_FLAG_AUDIO` via `g_object_set()` | Verify westerossink configured for low-bitrate resolution playback, first-frame callback registered
| 4 | Transition Pipeline to PLAYING State with Low-Bitrate Configuration | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`<br> Poll `gst_element_get_state()` until state change completes<br> Confirm `firstFrameReceived == true` callback indicates H.264 frame rendering started at configured 300 kbps with 180p resolution | Verify pipeline reaches `GST_STATE_PLAYING` without `GST_MESSAGE_ERROR`, first-frame signal detected within timeout, rendering at 300 kbps/180p |
| 5 | Monitor Low-Bitrate Frame Rendering Performance |  Poll `g_object_get(westerossink, "stats")`<br>via `g_object_get(westerossink, "stats", &structure, NULL)` at 100ms intervals. Extract `rendered_frames` and `dropped_frames` counters<br>via `gst_structure_get_uint64()`. Verify `rendered_frames` increments smoothly (no stalls))<br>throughout low-bitrate 300 kbps playback. Confirm `dropped_frames` remains at 0 or minimal (baseline threshold)  | Verify frame statistics show consistent rendering with acceptable frame delivery for 300 kbps low-bitrate stream |
| 6 | Validate Playback Position Advancement at 300 kbps Low-Bitrate Rate |  Query playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)` at 100ms intervals. Verify position advances at 1x rate (1 second per real-time second +/-250ms tolerance))<br>under 300 kbps connection_speed. Confirm no backward jumps or stalls in position during low-bitrate playback  | Verify position advances smoothly without gaps at 300 kbps, validating decoder performance under extreme bandwidth constraints |
| 7 | Monitor Sustained Playback and Buffer Status at 300 kbps |  Continue monitoring for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` seconds (typically 10 seconds))<br>to validate sustained playback stability at extreme low bitrate (300 kbps). Poll pipeline bus<br>via `gst_bus_timed_pop_filtered()` to check for `GST_MESSAGE_ERROR` or buffer underflow conditions. Verify no decode errors occur despite bitrate constraints  | Verify playback sustained without errors for full timeout duration at 300 kbps, no buffer underruns despite extreme bitrate limitation |
| 8 | Execute Pause-Resume Cycle to Validate State Management | Transition pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`<br> Verify playback halts and position freezes<br> Resume to `GST_STATE_PLAYING`<br> Verify playback resumes without drops and position continues from pause point<br> Confirm rendered_frames counter resumes incrementing | Verify state transitions successful, pause halts playback completely, resume continues smoothly |
| 9 | Release Pipeline and Cleanup Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state()`. Unreference playbin element<br>via `gst_object_unref()`. Monitor test framework output for "Failures: 0" and "Errors: 0" or "failed: 0" string. Close logging file and verify all GStreamer resources freed  | Verify pipeline reaches `GST_STATE_NULL`, test status shows zero failures, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 5 mins

**Priority:** High

**Release Version:** M121












