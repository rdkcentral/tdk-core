## TestCase ID
RDKV_NATIVE_PLAYBACK_270

## TestCase Name
RDKV_CERT_NPVS_Appsrc_Video_Underflow_Signal_AV1

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify the presence of `buffer-underflow-callback` signal when Appsrc buffer underflows for AV1 streams. Validate that the signal is correctly emitted and detected through the GStreamer pipeline during intentional buffer starvation with BYTES_THRESHOLD = 17002704 bytes, and verify pipeline recovers after buffer refill operations.

## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | AV1 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for Appsrc feeding<br> Stream file path configured as `test_streams_base_path + "TDK_Asset_Waterfall_720p_AV1.mp4"` in MediaValidationVariables.py Stream variable `video_src_url_mp4_720p_av1` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Waterfall_720p_AV1.mp4` (Appsrc requires local file access, not DASH/HLS streams) | Verify AV1 stream file is accessible and readable from filesystem Verify `video_src_url_mp4_720p_av1` resolves to valid, accessible AV1 file location |
| 3 | Appsrc Buffer Threshold Configuration |  `BYTES_THRESHOLD` must be configured to 17002704 bytes (actual threshold value from test script))<br>to trigger av1 underflow condition. This value defines the Appsrc buffer fill level before starvation signal is triggered  | Verify BYTES_THRESHOLD = 17002704 bytes is set in Appsrc configuration or test parameters |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables and Wayland display is active |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace  | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Appsrc Pipeline and Load Media | Create `playbin` element via `gst_element_factory_make()` and configure `uri` property to `appsrc://` via `g_object_set()`<br> Set `video-sink` property via `g_object_set()` | Verify playbin element created successfully, `uri` property configured to `appsrc://`, and `video-sink` property is set |
| 3 | Register Appsrc Callbacks and Setup Pipeline |  Register `source-setup` signal<br>via `g_signal_connect()`. Set Appsrc `size` property<br>via `g_object_set()`. Register sink element signals `buffer-underflow-callback`, `first-video-frame-callback` or `first-video-frame-callback`, and `pts-error-callback`<br>via `g_signal_connect()`. Configure `video-sink` property to `westerossink`<br>via `g_object_set()`  | Verify `source-setup`, `buffer-underflow-callback`, frame callback, and `pts-error-callback` signals are registered, Appsrc `size` property is set, and `video-sink` property is configured |
| 4 | Start Appsrc Data Feeding and Transition to Playing State |  Set pipeline to `GST_STATE_PAUSED`<br>via `gst_element_set_state()`. Emit `push-buffer` action on Appsrc<br>via `g_signal_emit_by_name()` until `BYTES_THRESHOLD = 17002704 bytes` is reached. Transition to `GST_STATE_PLAYING`<br>via `gst_element_set_state()`. Monitor first-frame signal to confirm rendering started  | Verify pipeline state transitions to PAUSED then PLAYING, buffers pushed to Appsrc reach 17002704 bytes threshold, first-frame signal is detected |
| 5 | Intentionally Starve Buffer to Trigger Underflow | Stop emitting `push-buffer` action on Appsrc to create buffer starvation<br> Monitor `buffer-underflow-callback` signal to detect underflow condition | Verify `buffer-underflow-callback` signal is detected when sink buffer depletes |
| 6 | Resume Data Feeding with Increased Buffer Threshold and Emit EOS | Resume emitting `push-buffer` action on Appsrc to accumulate `2 * BYTES_THRESHOLD = 34005408 bytes`<br> After all media data is transferred to Appsrc, emit `end-of-stream` action via `g_signal_emit_by_name()` | Verify buffers accumulated to 34005408 bytes threshold and `end-of-stream` action is emitted |
| 7 | Validate Playback Recovery After Buffer Refill | Transition to `GST_STATE_PLAYING` via `gst_element_set_state()`<br> Query playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at expected rate (1 second position per 1 second real-time +/-250ms tolerance)<br> Monitor `pts-error-callback` signal to detect presentation timestamp errors<br> Query sink element properties to verify frame rendering continues | Verify position advances at expected rate with no backward jumps, no `pts-error-callback` signals detected, sink continues rendering without stalls |
| 8 | Monitor Pipeline EOS and Validate Test Completion | Monitor GStreamer bus via `gst_bus_pop()` to detect `GST_MESSAGE_EOS` message from pipeline<br> Verify test framework output confirms execution success<br> Compare recorded playback metrics against expected baseline values | Verify `GST_MESSAGE_EOS` is detected on bus, test execution completed successfully with expected metrics matching baseline |
| 9 | Release Pipeline and Cleanup Resources | Set pipeline to `GST_STATE_NULL` via `gst_element_set_state()`<br> Unreference playbin element via `gst_object_unref()`<br> Free allocated memory and close logging file | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer resources released, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121





