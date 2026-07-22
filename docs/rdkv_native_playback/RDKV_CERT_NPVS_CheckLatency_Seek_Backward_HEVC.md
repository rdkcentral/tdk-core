## TestCase ID
RDKV_NATIVE_PLAYBACK_222

## TestCase Name
RDKV_CERT_NPVS_CheckLatency_Seek_Backward_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency when performing a backward seek operation on HEVC/H.265 DASH stream. Record latency from initiating seek-to-position to first frame rendering at new position, validating that latency remains below configured threshold (default 100 milliseconds). Verify seek completes accurately to target position and westerossink renders frames within latency budget after backward seek completes.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | HEVC/AAC stream must be accessible via HTTP/HTTPS or filesrc, configured at `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` in MediaValidationVariables.py<br> Stream variable `video_src_url_hevc` must be configured with this path<br> (DASH MPD with fMP4 segments, 1080p, 5+ mins) | Verify DASH HEVC/AAC stream is accessible and parseable, `video_src_url_hevc` resolves to valid, accessible stream with valid segments |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session<br>via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULL → READY → PAUSED → PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered, no `GST_MESSAGE_ERROR` |
| 4 | Execute Seek Operation with Latency Measurement | Invoke `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to reposition playback<br> Record timestamp at seek initiation for latency calculation<br> Verify position matches the seek target within +/-250ms tolerance<br> Calculate latency from seek command to first frame at new position | Verify test operation completes successfully with latency below configured threshold (default 100ms) and position matches target within tolerance |
| 5 | Monitor Playback Progress and Verify Latency Metrics | Poll `gst_element_query_position()` at 100ms intervals to verify position advances at expected rate from seek target<br> Calculate end-to-end latency from seek command to stable playback at new position<br> Validate that latency metrics are captured and remain within acceptable bounds (default: 100 milliseconds) | Verify position increments are consistent from new position, no stalls or backward jumps detected, latency metrics logged and within threshold |
| 6 | Validate Frame Rendering | Poll `g_object_get(westerossink, "stats")` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121













