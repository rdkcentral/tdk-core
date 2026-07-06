**TestCase ID**
NATIVE_PLAYBACK_319

**TestCase Name**
NPVS_Seek_Towards_EOS_with_Pause_MKV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on MKV Matroska H.264 stream with playback pause intervals by invoking `gst_element_seek()` to reposition playback near stream's final position. The test verifies that the seek target is reached within ±1 second tolerance, and validates state machine transitions through pause/resume cycles. Validates frame rendering continues with correct PTS monotonicity during pause-resume-seek sequences and matroskademux maintains proper cluster state through pause recovery operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MKV container stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_MKV.mkv"` in MediaValidationVariables.py. Stream contains H.264 video and audio in MKV container format | Verify MKV file is accessible and matroskademux can parse container |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mkv` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_MKV.mkv"` | Verify stream URL resolves to valid, accessible MKV file location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered, no `GST_MESSAGE_ERROR` |
| 4 | Execute Seek Operation | Invoke `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to reposition playback. Verify position matches the seek target within ±250ms tolerance | Verify test operation completes successfully with expected results |
| 5 | Monitor Playback Progress | Poll `gst_element_query_position()` at 100ms intervals to verify position advances at expected rate | Verify position increments are consistent, no stalls or backward jumps detected |
| 6 | Validate Frame Rendering | Poll `westerossink→stats` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
