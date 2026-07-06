**TestCase ID**
NATIVE_PLAYBACK_84

**TestCase Name**
NPVS_Set_Rate_0

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify playback rate control at 0.75x speed using GStreamer `gst_element_seek()` function with rate parameter set to 0.75 and GST_SEEK_FLAG_FLUSH flag. Validate that position advances at exactly 0.75x speed (three-quarter normal speed) through periodic `gst_element_query_position()` polling with position increment expected at ±25% tolerance around 0.075 seconds per 100ms interval. Verify audio/video remain synchronized during rate change and frame rendering continues without discontinuities using `westerossink` frame statistics validation.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | H.264 encoded MP4 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_30fps_v2.mp4"` in MediaValidationVariables.py (30fps H.264 baseline stream for rate control validation) | Verify H.264 MP4 stream file is accessible, readable, and contains minimum 60 seconds of content for rate testing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mp4_30fps` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_30fps_v2.mp4` (stream must have H.264 codec at 30fps framerate) | Verify `video_src_url_mp4_30fps` resolves to valid, accessible H.264 MP4 file location with 30fps encoding |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered, no `GST_MESSAGE_ERROR` |
| 4 | Execute Playback Rate Change | Invoke `gst_element_seek()` with playback rate set to 0.75 and GST_SEEK_FLAG_FLUSH flag. Verify position progression matches 0.75x speed (three-quarter normal speed) with maintained audio/video sync | Verify test operation completes successfully with expected results |
| 5 | Monitor Playback Progress | Poll `gst_element_query_position()` at 100ms intervals to verify position advances at 0.75x rate (expected increment: 0.075 seconds per 100ms ±25% tolerance) | Verify position increments are consistent, no stalls or backward jumps detected |
| 6 | Validate Frame Rendering | Poll `westerossink→stats` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
