**TestCase ID**
NATIVE_PLAYBACK_81

**TestCase Name**
NPVS_Set_Rate_0

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify playback rate control at 0.5x speed using GStreamer `gst_element_seek()` function with H.264 60fps high-framerate stream. Validate that position advances at exactly 0.5x speed (half normal speed) through periodic `gst_element_query_position()` polling with position increment expected at ±25% tolerance around 0.05 seconds per 100ms interval. Verify audio/video remain synchronized during rate change and frame rendering continues without discontinuities with 60fps framerate baseline.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | H.264 encoded MP4 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_60fps.mp4"` in MediaValidationVariables.py (60fps H.264 high-framerate stream for rate control validation) | Verify H.264 MP4 stream file is accessible, readable, and contains minimum 60 seconds of content for rate testing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mp4_60fps` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_60fps.mp4` (stream must have H.264 codec at 60fps framerate) | Verify `video_src_url_mp4_60fps` resolves to valid, accessible H.264 MP4 file location with 60fps encoding |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, GST_PLUGIN_PATH includes H.264 plugins, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load H.264 Stream | Create `playbin` element via `gst_element_factory_make("playbin", NULL)` and configure `uri` property to H.264 stream path via `g_object_set(playbin, "uri", url, NULL)`. Set `video-sink` property to `westerossink` via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Verify playbin element created successfully, `uri` property configured to H.264 MP4 stream, `video-sink` property is set to westerossink |
| 3 | Register Signals and Setup Callbacks | Register `first-video-frame-callback` signal via `g_signal_connect()` to detect first frame rendering. Register `pts-error-callback` signal to detect presentation timestamp errors. Connect to GStreamer bus via `gst_element_get_bus()` to monitor `GST_MESSAGE_ERROR`, `GST_MESSAGE_EOS`, and `GST_MESSAGE_STATE_CHANGED` messages | Verify all signals registered successfully, bus message handler is active |
| 4 | Transition Pipeline to Playing State and Confirm Rendering | Set pipeline state to `GST_STATE_PAUSED` via `gst_element_set_state()`. Transition to `GST_STATE_PLAYING` via `gst_element_set_state()`. Monitor `first-video-frame-callback` signal to confirm first frame rendering started. Query initial playback position via `gst_element_query_position()` as baseline. Verify no `GST_MESSAGE_ERROR` on bus | Verify pipeline transitions to PLAYING state, first frame signal is detected, baseline position recorded |
| 5 | Invoke gst_element_seek() with 0.5x Playback Rate | Invoke `gst_element_seek(playbin, 0.5, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_ACCURATE, GST_SEEK_TYPE_SET, 0, GST_SEEK_TYPE_NONE, -1)` to set playback rate to 0.5x (half-speed). Verify seek operation completes successfully. Monitor bus for `GST_MESSAGE_STATE_CHANGED` to confirm rate application. Record position immediately after seek as rate-change reference point | Verify gst_element_seek() completes without errors, rate change is applied to pipeline, position reference recorded |
| 6 | Poll Position and Validate 0.5x Rate Compliance | Poll playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms for duration of 20-30 seconds. Calculate position increment per 100ms interval: (current_position - previous_position) / GST_SECOND. For 0.5x rate, expected increment is ~0.05 seconds per 100ms (tolerance: 0.05 ±0.0125 = 0.0375-0.0625 seconds). Flag any increments outside tolerance as rate violation. Verify no position backward jumps occur | Verify all position increments within 0.5x rate tolerance, no backward jumps, no stalls detected during rate-controlled playback |
| 7 | Validate Frame Rendering Statistics During Rate Change | Every 500ms, poll `westerossink→stats` property via `g_object_get(westerossink, "stats", &structure, NULL)`. Extract `rendered` count via `gst_structure_get_uint64(structure, "rendered", &rendered_frames)` and `dropped` count. Calculate dropped_frame_percentage = dropped_frames / (rendered_frames + dropped_frames). Verify dropped frame percentage < 1% throughout rate-controlled playback. Monitor for any frame timing anomalies | Verify rendered frame count increments consistently, dropped frames minimal (< 1%), frame rendering continues smoothly at 0.5x speed |
| 8 | Monitor Pipeline EOS and Validate Test Completion | Continue position polling until `GST_MESSAGE_EOS` is detected on bus via `gst_bus_pop_filtered()`. When EOS detected, verify test metrics collected: total position advancement, average rate compliance, frame statistics. Cross-check if total test duration at 0.5x rate is approximately 2x the stream duration (due to 0.5x slowdown) | Verify `GST_MESSAGE_EOS` detected on bus, test metrics collected, rate compliance summary calculated |
| 9 | Release Pipeline and Cleanup Resources | Monitor `pts-error-callback` signal - verify no pts-error signals were detected during entire rate-controlled test. Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin element via `gst_object_unref(playbin)`. Free allocated memory and close logging file | Verify no pts-error signals detected during test, pipeline reaches `GST_STATE_NULL`, all GStreamer objects unreferenced, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
