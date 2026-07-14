## TestCase ID
NATIVE_PLAYBACK_218

## TestCase Name
NPVS_CheckLatency_FastForward_2x_EAC3

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency when transitioning to 2.0x fast-forward playback rate on H.264/EAC3 DASH stream. Record latency from setting playback rate to 2.0x via  to first frame rendering at new rate, validating that latency remains below configured threshold (default 100 milliseconds). Verify audio/video remain synchronized during rate-changed playback and westerossink renders frames within latency budget.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | DASH H.264/EAC3 Stream Provisioning | H.264/Avc With Eac3 Audio stream must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"`  in MediaValidationVariables.py (DASH MPD with fMP4 segments, 1080p, 5+ minutes) | Verify DASH H.264/EAC3 stream is accessible and parseable, segments downloadable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_ec3` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_H264_EC3/atfms_291_dash_tdk_avc_eac3_fmp4.mpd"`  (format: DASH MPD with fMP4 segments) | Verify `video_src_url_ec3` resolves to valid, accessible stream with valid segments |
| 4 | Playback Timeout Configuration | Invoke  with 2.0x rate parameter and verify playback acceleration
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches  with first frame rendered, no  |
| 4 | Execute Fast-Forward 2x Rate Operation with Latency Measurement | Invoke  with playback rate parameter set to 2.0x for double-speed playback. Record timestamp at seek initiation for latency calculation. Verify position advances at exactly 2x rate and `westerossink→stats` shows accelerated frame rendering at 2x multiplier. Calculate latency from seek to first frame at new rate | Verify test operation completes successfully with expected results and latency below configured threshold (default 100ms) |
| 5 | Monitor Playback Progress and Verify Latency Metrics |  Calculate end-to-end latency from rate change command to stable fast-forward playback. Validate that latency metrics are captured and remain within acceptable bounds (default: 100 milliseconds) | Verify position increments are consistent with 2x rate, no stalls or backward jumps detected, latency metrics logged and within threshold |
| 6 | Validate Frame Rendering | Poll `westerossink→stats` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to  and release all codec, decoder, and sink resources | Verify pipeline reaches  and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
