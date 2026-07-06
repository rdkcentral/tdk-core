**TestCase ID**
NATIVE_PLAYBACK_152

**TestCase Name**
NPVS_High_Bitrate_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate H.264 video playback at high bitrate using playbin element with westerossink video rendering. Test dynamically adjusts connection_speed and output height based on device type: Video_Accelerator uses connection_speed=15000 kbps with 2160p resolution, while RPI-CLIENT devices use connection_speed=10000 kbps with 1080p resolution. Verify frame rendering performance and A/V synchronization are maintained during sustained high-bitrate playback via continuous monitoring of `westerossink→stats.rendered_frames` and playback position via `gst_element_query_position()`. Confirm no frame drops or stalls occur during high-bitrate H.264 playback, validating video decoder and rendering pipeline capacity for premium bitrate streams across supported device variants.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent GStreamer libraries including H.264 decoder | Verify TDK_Package is installed, binary is executable, all libraries are available, H.264 decoder plugins loaded |
| 2 | Media Stream Provisioning | DASH stream with H.264 video at high bitrate must be accessible via HTTP/HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file path configured as `video_src_url_bitrate_h264` in MediaValidationVariables.py (external stream). Stream contains H.264 video at high bitrate (15000 kbps Video_Accelerator, 10000 kbps RPI-CLIENT) and AAC audio | Verify DASH stream accessible with high bitrate capability, dashdemux available for MPD parsing at configured bitrate |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_bitrate_h264` configured in `MediaValidationVariables.py` with external DASH stream URL containing H.264 video at high bitrate. Connection_speed property: Video_Accelerator=15000 kbps, RPI-CLIENT=10000 kbps; Height property: Video_Accelerator=2160, RPI-CLIENT=1080 | Verify `video_src_url_bitrate_h264` resolves to valid external DASH manifest with device-specific bitrate configuration |
| 4 | Playback Timeout and AV Status Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config file. `NATIVE_PLAYBACK_CHECK_AV_STATUS` must be configured (yes/no) for SOC-level decoder verification | Verify timeout set to minimum 10 seconds and CHECK_AV_STATUS configuration exists |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` for high bitrate H.264 support on Video_Accelerator and RPI-CLIENT devices | Verify `/opt/TDK/TDK.env` exists with all required environment variables for H.264 hardware decoding at 2160p (Video_Accelerator) or 1080p (RPI-CLIENT) |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Apply Device-Specific Properties | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer H.264 decoder plugins and vendor libraries via `LD_PRELOAD`. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Detect device type (Video_Accelerator vs RPI-CLIENT) and apply connection_speed property (15000 kbps for Video_Accelerator, 10000 kbps for RPI-CLIENT) and height property (2160 for Video_Accelerator, 1080 for RPI-CLIENT) | Verify all environment variables load correctly, H.264 plugins available, Wayland display created, device type detected, and connection_speed/height properties applied per device |
| 2 | Retrieve Configuration and Construct Playbin Pipeline with Bitrate Properties | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and `NATIVE_PLAYBACK_CHECK_AV_STATUS` from device config file. Apply connection_speed property (15000 kbps for Video_Accelerator, 10000 kbps for RPI-CLIENT) and height property (2160 for Video_Accelerator, 1080 for RPI-CLIENT). Retrieve stream variable `video_src_url_bitrate_h264` from MediaValidationVariables.py. Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set URI property via `g_object_set(playbin, "uri", <stream_url>, NULL)` | Verify playbin element created with correct connection_speed/height properties for device type, stream URL configured for H.264 high bitrate playback |
| 3 | Configure Westerossink and Register Callbacks | Create `westerossink` element via `gst_element_factory_make("westerossink", NULL)`. Connect as video sink via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal via `g_signal_connect()` to verify rendering begins. Set playback flags to `GST_PLAY_FLAG_VIDEO \| GST_PLAY_FLAG_AUDIO` via `g_object_set()` | Verify westerossink configured for 2160p playback (or 1080p for RPI), first-frame callback registered |
| 4 | Transition Pipeline to PLAYING State with Bitrate Configuration | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Poll `gst_element_get_state()` until state change completes. Confirm `firstFrameReceived == true` callback indicates H.264 frame rendering started at configured 15000 kbps (or 10000 kbps for RPI-CLIENT) with corresponding 2160p (or 1080p for RPI-CLIENT) resolution | Verify pipeline reaches `GST_STATE_PLAYING` without `GST_MESSAGE_ERROR`, first-frame signal detected within timeout, rendering at correct bitrate/resolution |
| 5 | Monitor High-Bitrate Frame Rendering Performance | Poll `westerossink→stats` via `g_object_get(westerossink, "stats", &structure, NULL)` at 100ms intervals. Extract `rendered_frames` and `dropped_frames` counters via `gst_structure_get_uint64()`. Verify `rendered_frames` increments smoothly (no stalls) throughout high-bitrate playback. Confirm `dropped_frames` remains at 0 or below 1% of rendered (baseline threshold) | Verify frame statistics show healthy high-bitrate rendering with minimal or zero drops |
| 6 | Validate Playback Position Advancement at High-Bitrate Rate | Query playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)` at 100ms intervals. Verify position advances at 1x rate (1 second per real-time second ±250ms tolerance) under 15000 kbps (or 10000 kbps for RPI-CLIENT) connection_speed. Confirm no backward jumps or stalls in position during high-bitrate playback | Verify position advances smoothly without gaps at 15000/10000 kbps, validating decoder performance under high-bitrate load |
| 7 | Monitor Sustained Playback and Buffer Status at High Bitrate | Continue monitoring for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` seconds (typically 10 seconds) to validate sustained high-bitrate playback stability at 15000 kbps (or 10000 kbps for RPI-CLIENT). Poll pipeline bus via `gst_bus_timed_pop_filtered()` to check for `GST_MESSAGE_ERROR` or buffer underflow conditions. Verify no decode errors occur during extended high-bitrate stream playback | Verify playback sustained without errors for full timeout duration at high bitrate, no buffer underruns despite elevated decoder load |
| 8 | Execute Pause-Resume Cycle to Validate State Management | Transition pipeline to `GST_STATE_PAUSED` via `gst_element_set_state()`. Verify playback halts and position freezes. Resume to `GST_STATE_PLAYING`. Verify playback resumes without drops and position continues from pause point. Confirm rendered_frames counter resumes incrementing | Verify state transitions successful, pause halts playback completely, resume continues smoothly |
| 9 | Release Pipeline and Cleanup Resources | Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state()`. Unreference playbin element via `gst_object_unref()`. Monitor test framework output for "Failures: 0" and "Errors: 0" or "failed: 0" string. Close logging file and verify all GStreamer resources freed | Verify pipeline reaches `GST_STATE_NULL`, test status shows zero failures, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
