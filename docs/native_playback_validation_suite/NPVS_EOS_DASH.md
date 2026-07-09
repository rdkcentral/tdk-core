## TestCase ID
NATIVE_PLAYBACK_149

## TestCase Name
NPVS_EOS_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate DASH H.264/AAC stream (15-second duration) playback to completion and End-Of-Stream (EOS) signal detection via GStreamer pipeline. Verify  retrieves pipeline bus and  successfully detects  when stream reaches natural end. Test confirms playback completion via message polling loop with timeout validation and pipeline state cleanup.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC_15Sec/master.mpd"` in MediaValidationVariables.py. Stream contains 15-second H.264/AAC media (H.264 video codec, AAC audio codec, DASH container format) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_short_duration_dash` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC_15Sec/master.mpd"` | Verify `video_src_url_short_duration_dash` resolves to valid DASH manifest URL, manifest contains valid MPD structure |
| 4 | EOS Detection Timeout Configuration | `NATIVE_PLAYBACK_EOS_TIMEOUT` configuration must be set in device configuration file (default: 10 seconds if not configured). For 15-second stream, recommended timeout: 20 seconds (stream duration + 5-second buffer). | Verify timeout is set appropriately to allow 15-second stream completion |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264 decoder libraries, ) must be defined in `/opt/TDK/TDK.env` for GStreamer plugin and codec access | Verify `/opt/TDK/TDK.env` exists with all required variables, H.264 hardware decoder plugins loaded via GST_PLUGIN_PATH, Wayland display available |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Setup Pipeline | Source environment variables from `/opt/TDK/TDK.env` for GStreamer plugin paths and codec libraries. Create `playbin` element via . Set stream URI via . Create and attach `westerossink` video sink via . Register `first-video-frame-callback` signal via  on westerossink. Transition pipeline to  via . Wait for first-frame signal | Verify playbin element created, stream URI property set to DASH manifest, westerossink configured as video sink, pipeline transitions to PLAYING state, first-video-frame-callback received, video rendering starts without errors |
| 2 | Optionally Check AV Status | If device configurationis set to "yes", verify video playback status via SOC-level video decoder check (proc entry inspection for rendering statistics). This step is performed only if `checkAVStatus` flag is enabled | Verify AV status check completes successfully if enabled, video decoder reports active playback |
| 3 | Retrieve Pipeline Bus Reference | Retrieve GStreamer pipeline bus via . Verify bus is non-null | Verify bus retrieved successfully from playbin element, bus reference is valid |
| 4 | Initialize EOS Detection Loop | Retrieve device configuration value for `NATIVE_PLAYBACK_EOS_TIMEOUT` via configuration retrieval (default: 10 seconds if not configured, or configured timeout value). Start high-resolution timeout clock via `std::chrono::steady_clock::now()`. Initialize `received_EOS` flag to false | Verify timeout value retrieved from device config, timeout clock started, EOS flag initialized |
| 5 | Poll Pipeline Bus for EOS Message | Enter polling loop to continuously call  at each iteration. Check if returned message is non-null and message type equals  via . If EOS detected, set `received_EOS = true` and break loop. Check elapsed time against timeout threshold via `std::chrono::steady_clock::now() - start > std::chrono::seconds(timeout_value)`. If timeout exceeded, break loop without EOS detection | Verify EOS message detected on bus when stream completes naturally, polling loop continues until EOS or timeout, no error messages received from pipeline |
| 6 | Validate EOS Reception | Assert that `received_EOS == true` after polling loop exits. Verify assertion passes indicating EOS message successfully received from pipeline. Unreference bus message via  | Verify EOS message was received before timeout expiration, assertion passes without failure, message unreferenced |
| 7 | Verify Test Success Indicators | Validate test framework output for success strings: "Failures: 0", "Errors: 0", or "failed: 0". Confirm mediapipelinetests application execution completed without errors | Verify test output contains required success indicators, no playback errors reported |
| 8 | Terminate Pipeline and Release Resources | Set pipeline state to  via . Unreference bus via . Unreference playbin element via . Close logging file and free allocated memory | Verify pipeline reaches GST_STATE_NULL, all GStreamer object references released, resources freed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
