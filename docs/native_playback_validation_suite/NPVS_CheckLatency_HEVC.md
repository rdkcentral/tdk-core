## TestCase ID
NATIVE_PLAYBACK_205

## TestCase Name
NPVS_CheckLatency_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency from pipeline PLAYING state to first frame rendering using HEVC content. The test executes DASH HEVC playback and measures elapsed time when playback position reaches 1 second, validating that latency remains below the configured threshold. Verify frame rendering completes within latency budget for HEVC codec compliance.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | DASH HEVC/AAC Stream Provisioning | Hevc/H.265 With Aac Audio stream must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"`  in MediaValidationVariables.py (DASH MPD with fMP4 segments, 1080p, 5+ minutes) | Verify DASH HEVC/AAC stream is accessible and parseable, segments downloadable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hevc` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"`  (format: DASH MPD with fMP4 segments) | Verify `video_src_url_hevc` resolves to valid, accessible stream with valid segments |
| 4 | Latency Threshold Configuration | Latency threshold must be retrieved from device configuration file: `NATIVE_PLAYBACK_PLAYBACK_LATENCY_THRESHOLD` (default: 100 milliseconds) for pass/fail validation. Secondary timeout: `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) for overall playback duration | Verify latency threshold is set (default 100ms accepted if config unavailable) and playback timeout is accessible |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve `NATIVE_PLAYBACK_PLAYBACK_LATENCY_THRESHOLD` from device config (default: 100ms) and `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) | Verify environment variables load correctly, Wayland display created, latency threshold retrieved |
| 2 | Create Playbin and Configure DASH HEVC Stream | Create playbin element via . Set DASH HEVC stream URL from `MediaValidationVariables.video_src_url_hevc` as URI property. Set playback flags to enable video and audio via  | Verify playbin element created successfully, DASH HEVC stream URL configured, flags set for A/V playback |
| 3 | Create westerossink and Register Callbacks | Create westerossink element via . Connect westerossink as video-sink to playbin via . Register `first-video-frame-callback` signal on westerossink to capture frame rendered event | Verify westerossink created successfully, connected as video sink, first-frame callback registered |
| 4 | Transition Pipeline to PLAYING State | Start latency measurement by recording current time (start_latency = std::chrono::high_resolution_clock::now()). Set pipeline to PLAYING state via . Poll  until GST_STATE_CHANGE_SUCCESS and pipeline reaches GST_STATE_PLAYING | Verify pipeline successfully transitions to PLAYING state without GST_MESSAGE_ERROR, latency timer started |
| 5 |  Check if position reaches 1 second (currentPosition/GST_SECOND >= 1). Stop latency measurement when position reaches 1 second (stop_latency = now(), then subtract 1 second: stop_latency -= std::chrono::seconds(1)) | Verify position advances continuously, reaches 1-second mark within 3-second timeout, latency calculation time recorded |
| 6 | Calculate Latency in Milliseconds | Convert latency duration to milliseconds: `latency_ms = std::chrono::duration_cast<std::chrono::milliseconds>(stop_latency - start_latency).count()`. Extract integer milliseconds value from chrono duration object | Verify latency calculated as positive integer milliseconds value representing time from PLAYING state to 1-second playback position |
| 7 | Write Latency Measurement to Log File | Open latency log file at `{TDK_PATH}/latency_log`. Write latency value in format "Latency = {latency_ms} milliseconds\n" to file. Close file pointer. Also print to console: "Time measured: {latency_ms} milliseconds." | Verify file created/written successfully at configured path, latency value recorded with correct format |
| 8 | Validate Latency Against Threshold | Compare measured latency_ms with `latencyThreshold` (default: 100ms from config). If latency_ms < latencyThreshold, test PASSES. If latency_ms >= latencyThreshold, test FAILS. Check first-video-frame callback was triggered (firstFrameReceived == true) | Verify latency comparison completed, pass/fail determination made, first-frame signal confirmed |
| 9 | Verify First Frame Signal Received | Assert that `firstFrameReceived == true` was set by westerossink callback during step 5. This confirms video actually rendered, not just position advanced | Verify first-video-frame-callback signal was received and `firstFrameReceived` flag is true |
| 10 |  Close logging file. Verify all GStreamer resources freed | Verify pipeline reaches NULL state cleanly, all objects unreferenced, no resource leaks, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
