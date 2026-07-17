## TestCase ID
RDKV_NATIVE_PLAYBACK_315

## TestCase Name
RDKV_CERT_NPVS_EOS_OPUS_Only_Audio

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate OPUS audio-only stream (15-second duration) playback to completion and End-Of-Stream (EOS) signal detection GStreamer pipeline. Verify retrieves pipeline bus and successfully detects when audio stream reaches natural end. Test confirms playback completion message polling loop with timeout validation and pipeline state cleanup.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  OPUS audio-only stream must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_OPUS_Audio_only_15sec.webm"` in MediaValidationVariables.py. Stream contains 15-second OPUS audio media (OPUS audio codec, WebM container format, audio-only content))<br>Stream variable `audio_src_url_short_duration_webm_opus` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_OPUS_Audio_only_15sec.webm"`  | Verify OPUS audio file is accessible and readable from configured path, appropriate audio decoder and demuxer available Verify `audio_src_url_short_duration_webm_opus` resolves to valid audio stream URL, WebM container structure is valid |
| 3 | EOS Detection Timeout Configuration | `NATIVE_PLAYBACK_EOS_TIMEOUT` configuration must be set in device configuration file (default: 10 seconds if not configured)<br> For 15-second stream, recommended timeout: 20 seconds (stream duration + 5-second buffer)<br> | Verify timeout is set appropriately to allow 15-second stream completion |
| 4 | Platform-Specific Environment Variables |  Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor OPUS decoder libraries, `GST_PLUGIN_PATH`))<br>must be defined in `/opt/TDK/TDK.env` for GStreamer plugin and codec access  | Verify `/opt/TDK/TDK.env` exists with all required variables, OPUS hardware decoder plugins loaded via GST_PLUGIN_PATH |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Setup Pipeline |  Source environment variables from `/opt/TDK/TDK.env` for GStreamer plugin paths and codec libraries. Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Set stream URI<br>via `g_object_set(playbin, "uri", audio_stream_URL, NULL)`. Create and attach audio sink<br>via `g_object_set(playbin, "audio-sink", audiosink, NULL)`. Register `first-audio-frame-callback` signal<br>via `g_signal_connect()` on audio sink. Transition pipeline to `GST_STATE_PLAYING`<br>via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Wait for first-frame signal  | Verify playbin element created, stream URI property set to audio stream, audio sink configured, pipeline transitions to PLAYING state, first-audio-frame-callback received, audio playback starts without errors |
| 2 | Optionally Check AV Status | If device configurationis set to "yes", verify audio playback status via SOC-level audio decoder check<br> This step is performed only if `checkAVStatus` flag is enabled | Verify AV status check completes successfully if enabled, audio decoder reports active playback |
| 3 | Retrieve Pipeline Bus Reference | Retrieve GStreamer pipeline bus via `gst_element_get_bus(playbin)`. Verify bus is non-null | Verify bus retrieved successfully from playbin element, bus reference is valid |
| 4 | Initialize EOS Detection Loop |  Retrieve device configuration value for `NATIVE_PLAYBACK_EOS_TIMEOUT`<br>via configuration retrieval (default: 10 seconds if not configured, or configured timeout value). Start high-resolution timeout clock<br>via `std::chrono::steady_clock::now()`. Initialize `received_EOS` flag to false  | Verify timeout value retrieved from device config, timeout clock started, EOS flag initialized |
| 5 | Poll Pipeline Bus for EOS Message |  Enter polling loop to continuously call `gst_bus_pop_filtered(bus, GST_MESSAGE_EOS)` at each iteration. Check if returned message is non-null and message type equals `GST_MESSAGE_EOS`<br>via `GST_MESSAGE_TYPE(message) == GST_MESSAGE_EOS`. If EOS detected, set `received_EOS = true` and break loop. Check elapsed time against timeout threshold<br>via `std::chrono::steady_clock::now() - start > std::chrono::seconds(timeout_value)`. If timeout exceeded, break loop without EOS detection  | Verify EOS message detected on bus when audio stream completes naturally, polling loop continues until EOS or timeout, no error messages received from pipeline |
| 6 | Validate EOS Reception | Assert that `received_EOS == true` after polling loop exits<br> Verify assertion passes indicating EOS message successfully received from pipeline<br> Unreference bus message via `gst_message_unref(message)` | Verify EOS message was received before timeout expiration, assertion passes without failure, message unreferenced |
| 7 | Verify Test Success Indicators | Validate test framework output for success strings: "Failures: 0", "Errors: 0", or "failed: 0"<br> Confirm mediapipelinetests application execution completed without errors | Verify test output contains required success indicators, no audio playback errors reported |
| 8 | Terminate Pipeline and Release Resources |  Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference bus<br>via `gst_object_unref(bus)`. Unreference playbin element<br>via `gst_object_unref(playbin)`. Close logging file and free allocated memory  | Verify pipeline reaches GST_STATE_NULL, all GStreamer object references released, resources freed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121






