## TestCase ID
RDKV_NATIVE_PLAYBACK_184

## TestCase Name
RDKV_CERT_NPVS_Standard_Bitrate_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HEVC (H.265) video playback at standard bitrate using playbin element with westerossink video rendering. Test applies fixed connection_speed=1600 kbps and height=480p across all supported devices (Video_Accelerator only; no device-specific adjustment). Verify frame rendering performance and A/V synchronization are maintained during sustained standard-bitrate playback continuous monitoring of and playback position. Confirm no frame drops or stalls occur during standard-bitrate HEVC playback, validating video decoder and rendering pipeline capacity for typical HEVC bitrate streams.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent GStreamer libraries including HEVC decoder | Verify TDK_Package is installed, binary is executable, all libraries are available, HEVC decoder plugins loaded |
| 2 | Stream Provisioning and Configuration |  HEVC video stream configured for standard bitrate must be accessible via HTTP/HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`). Stream file path configured as `video_src_url_bitrate_hevc` in MediaValidationVariables.py (external stream). Fixed device properties applied: connection_speed=1600 kbps, height=480 (applies uniformly to Video_Accelerator))<br>Stream variable `video_src_url_bitrate_hevc` configured in `MediaValidationVariables.py` with external DASH stream URL containing HEVC standard-bitrate stream. Fixed connection_speed=1600 kbps and height=480 properties must be applied uniformly across Video_Accelerator (only supported model)  | Verify HEVC standard-bitrate stream file is accessible and readable with 480p resolution for Video_Accelerator Verify `video_src_url_bitrate_hevc` resolves to valid external HEVC standard-bitrate stream with connection_speed=1600 and height=480 applied to Video_Accelerator |
| 3 | Playback Timeout and AV Status Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config file | Verify timeout is set to minimum 10 seconds |
| 4 | Platform-Specific Environment Variables |  Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor HEVC decoder libraries, `GST_PLUGIN_PATH`))<br>must be defined in `/opt/TDK/TDK.env` for standard-bitrate HEVC playback support on Video_Accelerator (only supported model)  | Verify `/opt/TDK/TDK.env` exists with all required environment variables for HEVC decoding at 480p resolution |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Apply Fixed Device Properties |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer HEVC decoder plugins and vendor libraries<br>via `LD_PRELOAD`. Establish Wayland display session<br>via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Apply fixed connection_speed property (1600 kbps))<br>and height property (480))<br>for Video_Accelerator. No device-specific adjustment required for HEVC standard-bitrate  | Verify all environment variables load correctly, HEVC plugins available, Wayland display created, fixed connection_speed=1600 and height=480 properties applied for Video_Accelerator |
| 2 | Retrieve Configuration and Construct Playbin Pipeline with Standard Bitrate Properties |  Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device config file. Apply fixed connection_speed property (1600 kbps))<br>and height property (480))<br>for Video_Accelerator. Retrieve stream variable `video_src_url_bitrate_hevc` from MediaValidationVariables.py. Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set URI property via `g_object_set(playbin, "uri", <stream_url>, NULL)`  | Verify playbin element created with connection_speed=1600/height=480 properties for Video_Accelerator, stream URL configured for HEVC standard-bitrate playback |
|  3  |  Configure Westerossink and Register Callbacks  |   Create `westerossink` element<br>via `gst_element_factory_make("westerossink", NULL)`. Connect as video sink<br>via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal<br>via `g_signal_connect()` to verify rendering begins. Set playback flags to `GST_PLAY_FLAG_VIDEO` and `GST_PLAY_FLAG_AUDIO` via `g_object_set()` | Verify westerossink configured for standard-bitrate resolution playback, first-frame callback registered
| 4 | Transition Pipeline to PLAYING State with Standard Bitrate Configuration | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`<br> Poll `gst_element_get_state()` until state change completes<br> Confirm `firstFrameReceived == true` callback indicates HEVC frame rendering started at configured 1600 kbps with 480p resolution for Video_Accelerator | Verify pipeline reaches `GST_STATE_PLAYING` without `GST_MESSAGE_ERROR`, first-frame signal detected within timeout, rendering at 1600 kbps/480p |
| 5 | Monitor Standard-Bitrate Frame Rendering Performance |  Poll `g_object_get(westerossink, "stats")`<br>via `g_object_get(westerossink, "stats", &structure, NULL)` at 100ms intervals. Extract `rendered_frames` and `dropped_frames` counters<br>via `gst_structure_get_uint64()`. Verify `rendered_frames` increments smoothly (no stalls))<br>throughout standard-bitrate 1600 kbps playback. Confirm `dropped_frames` remains at 0 or below 1% of rendered (baseline threshold)  | Verify frame statistics show healthy 1600 kbps standard-bitrate HEVC rendering with minimal or zero drops |
| 6 | Validate Playback Position Advancement at 1600 kbps Standard Rate |  Query playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)` at 100ms intervals. Verify position advances at 1x rate (1 second per real-time second +/-250ms tolerance))<br>under 1600 kbps connection_speed. Confirm no backward jumps or stalls in position during standard-bitrate playback  | Verify position advances smoothly without gaps at 1600 kbps, validating HEVC decoder performance under typical bandwidth conditions |
| 7 | Monitor Sustained Playback and Buffer Status at 1600 kbps |  Continue monitoring for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` seconds (typically 10 seconds))<br>to validate sustained playback stability at standard 1600 kbps HEVC bitrate. Poll pipeline bus<br>via `gst_bus_timed_pop_filtered()` to check for `GST_MESSAGE_ERROR` or buffer underflow conditions. Verify no decode errors occur during extended standard-bitrate HEVC stream playback  | Verify playback sustained without errors for full timeout duration at 1600 kbps, no buffer underruns for HEVC typical bandwidth |
| 8 | Execute Pause-Resume Cycle to Validate State Management | Transition pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`<br> Verify playback halts and position freezes<br> Resume to `GST_STATE_PLAYING`<br> Verify playback resumes without drops and position continues from pause point<br> Confirm rendered_frames counter resumes incrementing | Verify state transitions successful, pause halts playback completely, resume continues smoothly |
| 9 | Release Pipeline and Cleanup Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state()`. Unreference playbin element<br>via `gst_object_unref()`. Monitor test framework output for "Failures: 0" and "Errors: 0" or "failed: 0" string. Close logging file and verify all GStreamer resources freed  | Verify pipeline reaches `GST_STATE_NULL`, test status shows zero failures, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 5 mins

**Priority:** High

**Release Version:** M121












