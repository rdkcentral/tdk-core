**TestCase ID**
NATIVE_PLAYBACK_150

**TestCase Name**
NPVS_EOS_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HLS H.264/AAC stream (15-second duration) playback to completion and End-Of-Stream (EOS) signal detection via GStreamer pipeline. Verify `gst_element_get_bus()` retrieves pipeline bus and `gst_bus_pop_filtered(bus, GST_MESSAGE_EOS)` successfully detects `GST_MESSAGE_EOS` when stream reaches natural end. Test confirms playback completion via message polling loop with timeout validation and pipeline state cleanup.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | HLS stream with M3U8 manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "HLS_H264_AAC_15Sec/master.m3u8"` in MediaValidationVariables.py. Stream contains 15-second H.264/AAC media (H.264 video codec, AAC audio codec, HLS container format) | Verify master.m3u8 manifest file is accessible and readable from configured path, hlsdemux plugin available for M3U8 parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_short_duration_hls` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "HLS_H264_AAC_15Sec/master.m3u8"` | Verify `video_src_url_short_duration_hls` resolves to valid HLS manifest URL, manifest contains valid M3U8 structure |
| 4 | EOS Detection Timeout Configuration | `NATIVE_PLAYBACK_EOS_TIMEOUT` configuration must be set in device configuration file (default: 10 seconds if not configured). For 15-second stream, recommended timeout: 20 seconds (stream duration + 5-second buffer). `NATIVE_PLAYBACK_CHECK_AV_STATUS` (default: "no") controls whether SOC-level video decoder status verification is performed | Verify timeout is set to minimum 20 seconds to allow 15-second stream completion, check AV status parameter is configured |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` for GStreamer plugin and codec access | Verify `/opt/TDK/TDK.env` exists with all required variables, H.264 hardware decoder plugins loaded via GST_PLUGIN_PATH, Wayland display available |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Setup Pipeline | Source environment variables from `/opt/TDK/TDK.env` for GStreamer plugin paths and codec libraries. Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set stream URI via `g_object_set(playbin, "uri", HLS_manifest_URL, NULL)`. Create and attach `westerossink` video sink via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal via `g_signal_connect()` on westerossink. Transition pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Wait for first-frame signal | Verify playbin element created, stream URI property set to HLS manifest, westerossink configured as video sink, pipeline transitions to PLAYING state, first-video-frame-callback received, video rendering starts without errors |
| 2 | Optionally Check AV Status | If device configuration `NATIVE_PLAYBACK_CHECK_AV_STATUS` is set to "yes", verify video playback status via SOC-level video decoder check (proc entry inspection for rendering statistics). This step is performed only if `checkAVStatus` flag is enabled | Verify AV status check completes successfully if enabled, video decoder reports active playback |
| 3 | Retrieve Pipeline Bus Reference | Retrieve GStreamer pipeline bus via `gst_element_get_bus(playbin)`. Verify bus is non-null | Verify bus retrieved successfully from playbin element, bus reference is valid |
| 4 | Initialize EOS Detection Loop | Retrieve device configuration value for `NATIVE_PLAYBACK_EOS_TIMEOUT` via configuration retrieval (default: 10 seconds if not configured, or configured timeout value). Start high-resolution timeout clock via `std::chrono::steady_clock::now()`. Initialize `received_EOS` flag to false | Verify timeout value retrieved from device config, timeout clock started, EOS flag initialized |
| 5 | Poll Pipeline Bus for EOS Message | Enter polling loop to continuously call `gst_bus_pop_filtered(bus, GST_MESSAGE_EOS)` at each iteration. Check if returned message is non-null and message type equals `GST_MESSAGE_EOS` via `GST_MESSAGE_TYPE(message) == GST_MESSAGE_EOS`. If EOS detected, set `received_EOS = true` and break loop. Check elapsed time against timeout threshold via `std::chrono::steady_clock::now() - start > std::chrono::seconds(timeout_value)`. If timeout exceeded, break loop without EOS detection | Verify EOS message detected on bus when stream completes naturally, polling loop continues until EOS or timeout, no error messages received from pipeline |
| 6 | Validate EOS Reception | Assert that `received_EOS == true` after polling loop exits. Verify assertion passes indicating EOS message successfully received from pipeline. Unreference bus message via `gst_message_unref(message)` | Verify EOS message was received before timeout expiration, assertion passes without failure, message unreferenced |
| 7 | Verify Test Success Indicators | Validate test framework output for success strings: "Failures: 0", "Errors: 0", or "failed: 0". Confirm mediapipelinetests application execution completed without errors | Verify test output contains required success indicators, no playback errors reported |
| 8 | Terminate Pipeline and Release Resources | Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference bus via `gst_object_unref(bus)`. Unreference playbin element via `gst_object_unref(playbin)`. Close logging file and free allocated memory | Verify pipeline reaches GST_STATE_NULL, all GStreamer object references released, resources freed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
