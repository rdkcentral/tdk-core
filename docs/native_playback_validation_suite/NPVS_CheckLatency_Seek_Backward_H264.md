## TestCase ID
NATIVE_PLAYBACK_221

## TestCase Name
NPVS_CheckLatency_Seek_Backward_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency for backward seek operations on H.264 DASH streams. The test performs a backward seek operation and records latency from seek initiation to first frame rendering at the new position, validating that latency remains below the configured threshold. Verify seek completes accurately to the target position and frames render within latency budget.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | DASH H.264/AAC Stream Provisioning | H.264/Avc With Aac Audio stream must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"`  in MediaValidationVariables.py (DASH MPD with fMP4 segments, 1080p, 5+ minutes) | Verify DASH H.264/AAC stream is accessible and parseable, segments downloadable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash_h264` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"`  (format: DASH MPD with fMP4 segments) | Verify `video_src_url_dash_h264` resolves to valid, accessible stream with valid segments |
| 4 | Playback Timeout Configuration | Invoke  with GST_SEEK_FLAG_FLUSH to seek backward from current position
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches  with first frame rendered, no  |
| 4 |  Record timestamp at seek initiation for latency calculation. Verify position matches the seek target within ±250ms tolerance. Calculate latency from seek command to first frame at new position | Verify test operation completes successfully with latency below configured threshold (default 100ms) and position matches target within tolerance |
| 5 | Monitor Playback Progress and Verify Latency Metrics |  Calculate end-to-end latency from seek command to stable playback at new position. Validate that latency metrics are captured and remain within acceptable bounds (default: 100 milliseconds) | Verify position increments are consistent from new position, no stalls or backward jumps detected, latency metrics logged and within threshold |
| 6 | Validate Frame Rendering | Poll `westerossink→stats` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to  and release all codec, decoder, and sink resources | Verify pipeline reaches  and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
