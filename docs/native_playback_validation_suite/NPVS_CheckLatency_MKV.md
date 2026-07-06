## TestCase ID
NATIVE_PLAYBACK_317

## TestCase Name
NPVS_CheckLatency_MKV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency from pipeline PLAYING state to first frame rendering on westerossink video sink using Matroska/MKV container format. Execute MKV stream through playbin with matroskademux element and measure elapsed time when playback position reaches 1 second, validating that latency remains below configured threshold (default 100 milliseconds). Verify westerossink successfully renders MKV-sourced frames within latency budget and logs measurement for container format compliance validation.
## Preconditions## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | MKV AV1 4K Stream Provisioning | Av1 4K stream must be accessible via HTTP/HTTPS or filesrc. Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_AV1_MKV.mkv"`  in MediaValidationVariables.py (Matroska container (MKV), 1080p, 5+ minutes) | Verify MKV AV1 4K stream is accessible and parseable, segments downloadable |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_4k_av1_mkv` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "TDK_Asset_Sunrise_AV1_MKV.mkv"`  (format: Matroska container (MKV)) | Verify `video_src_url_4k_av1_mkv` resolves to valid, accessible stream with valid segments |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve `NATIVE_PLAYBACK_PLAYBACK_LATENCY_THRESHOLD` from device config (default: 100ms) and `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) | Verify environment variables load correctly, Wayland display created, latency threshold retrieved |
| 2 | Create Playbin and Configure MKV Stream | Create playbin element via `gst_element_factory_make("playbin", NULL)`. Set MKV file URL from `MediaValidationVariables.video_src_url_4k_av1_mkv` as URI property (local file:// or HTTP URL). Set playback flags to enable video and audio via `GST_PLAY_FLAG_VIDEO \| GST_PLAY_FLAG_AUDIO` | Verify playbin element created successfully, MKV stream URL configured, flags set for A/V playback |
| 3 | Create westerossink and Register Callbacks | Create westerossink element via `gst_element_factory_make("westerossink", NULL)`. Connect westerossink as video-sink to playbin via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal on westerossink to capture frame rendered event | Verify westerossink created successfully, connected as video sink, first-frame callback registered |
| 4 | Transition Pipeline to PLAYING State | Start latency measurement by recording current time (start_latency = std::chrono::high_resolution_clock::now()). Set pipeline to PLAYING state via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Poll `gst_element_get_state()` until GST_STATE_CHANGE_SUCCESS and pipeline reaches GST_STATE_PLAYING | Verify pipeline successfully transitions to PLAYING state without GST_MESSAGE_ERROR, latency timer started |
| 5 | Poll Playback Position Until 1-Second Mark | Loop for maximum 3 seconds querying playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Check if position reaches 1 second (currentPosition/GST_SECOND >= 1). Stop latency measurement when position reaches 1 second (stop_latency = now(), then subtract 1 second: stop_latency -= std::chrono::seconds(1)) | Verify position advances continuously, reaches 1-second mark within 3-second timeout, latency calculation time recorded |
| 6 | Calculate Latency in Milliseconds | Convert latency duration to milliseconds: `latency_ms = std::chrono::duration_cast<std::chrono::milliseconds>(stop_latency - start_latency).count()`. Extract integer milliseconds value from chrono duration object | Verify latency calculated as positive integer milliseconds value representing time from PLAYING state to 1-second playback position |
| 7 | Write Latency Measurement to Log File | Open latency log file at `{TDK_PATH}/latency_log`. Write latency value in format "Latency = {latency_ms} milliseconds\n" to file. Close file pointer. Also print to console: "Time measured: {latency_ms} milliseconds." | Verify file created/written successfully at configured path, latency value recorded with correct format |
| 8 | Validate Latency Against Threshold | Compare measured latency_ms with `latencyThreshold` (default: 100ms from config). If latency_ms < latencyThreshold, test PASSES. If latency_ms >= latencyThreshold, test FAILS. Check first-video-frame callback was triggered (firstFrameReceived == true) | Verify latency comparison completed, pass/fail determination made, first-frame signal confirmed |
| 9 | Verify First Frame Signal Received | Assert that `firstFrameReceived == true` was set by westerossink callback during step 5. This confirms video actually rendered, not just position advanced | Verify first-video-frame-callback signal was received and `firstFrameReceived` flag is true |
| 10 | Release Pipeline and Cleanup Resources | Set pipeline to NULL state via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and westerossink objects via `gst_object_unref()`. Close logging file. Verify all GStreamer resources freed | Verify pipeline reaches NULL state cleanly, all objects unreferenced, no resource leaks, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
