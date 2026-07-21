## TestCase ID
RDKV_NATIVE_PLAYBACK_278

## TestCase Name
RDKV_CERT_NPVS_Set_Rate_0.5x_Only_Audio_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify playback rate control at 0.5x speed function with audio-only AAC stream (no video track). Validate that position advances at exactly 0.5x speed (half normal speed) through periodic polling with position increment expected at +/-25% tolerance around 0.05 seconds per 100ms interval. Verify audio pad is correctly configured, AAC audio remains synchronized during rate change, and audio decoding continues without discontinuities or buffer underflow.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  AAC audio-only stream must be accessible via local file system (`filesrc`))<br>or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"` in MediaValidationVariables.py (audio-only stream with no video track for audio rate control validation))<br>Stream variable `audio_src_url_mp4_aac` configured in `MediaValidationVariables.py` with path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4` (stream must contain AAC audio track only, no video track)  | Verify AAC audio stream file is accessible, readable, contains audio track only (no video), and contains minimum 60 seconds of audio content Verify `audio_src_url_mp4_aac` resolves to valid, accessible audio-only AAC MP4 file location with AAC codec confirmation |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, AAC audio codec library paths, and Wayland display configuration (audio-only rendering may skip video compositor)<br> Establish audio pipeline context<br> Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, AAC codec plugins available, GST_PLUGIN_PATH includes AAC audio plugins, logging initialized without errors |
| 2 | Configure Playbin Pipeline and Load AAC Audio Stream |  Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)` and configure `uri` property to AAC audio stream path<br>via `g_object_set(playbin, "uri", url, NULL)`. Verify no video track present in stream. Attach audio pad query handler to verify AAC audio pad configuration and format  | Verify playbin element created successfully, `uri` property configured to audio-only AAC stream, audio pad is active and properly configured for AAC decoding |
| 3 | Register Signals and Setup Callbacks |  Register `audio-level-callback` signal<br>via `g_signal_connect()` to monitor audio level progression. Register `pts-error-callback` signal to detect presentation timestamp errors. Connect to GStreamer bus<br>via `gst_element_get_bus()` to monitor `GST_MESSAGE_ERROR`, `GST_MESSAGE_EOS`, and `GST_MESSAGE_STATE_CHANGED` messages  | Verify all signals registered successfully, bus message handler is active |
| 4 | Transition Pipeline to Playing State and Confirm Audio Decoding |  Set pipeline state to `GST_STATE_PAUSED`<br>via `gst_element_set_state()`. Transition to `GST_STATE_PLAYING`<br>via `gst_element_set_state()`. Monitor audio pipeline to confirm audio decoding started. Query initial playback position<br>via `gst_element_query_position()` as baseline. Verify no `GST_MESSAGE_ERROR` on bus  | Verify pipeline transitions to PLAYING state, audio decoding is active, baseline position recorded |
|  5  |  Invoke gst_element_seek() with 0.5x Playback Rate  |  Invoke `gst_element_seek(playbin, 0.5, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH|GST_SEEK_FLAG_ACCURATE, GST_SEEK_TYPE_SET, 0, GST_SEEK_TYPE_NONE, -1)` to set audio playback rate to 0.5x (half-speed). Verify seek operation completes successfully. Monitor bus for `GST_MESSAGE_STATE_CHANGED` to confirm rate application. Record position immediately after seek as rate-change reference point | Verify gst_element_seek() completes without errors, rate change is applied to pipeline, position reference recorded |
| 6 | Poll Position and Validate 0.5x Rate Compliance | Poll playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` every 100ms for duration of 20-30 seconds<br> Calculate position increment per 100ms interval: (current_position - previous_position) / GST_SECOND<br> For 0.5x rate, expected increment is ~0.05 seconds per 100ms (tolerance: 0.05 +/-0.0125 = 0.0375-0.0625 seconds)<br> Flag any increments outside tolerance as rate violation<br> Verify no position backward jumps occur | Verify all position increments within 0.5x rate tolerance, no backward jumps, no stalls detected during audio rate-controlled playback |
| 7 | Validate Audio Decoding Statistics During Rate Change | Every 500ms, query audio buffer fill level via audio pad property query<br> Monitor for audio underflow conditions (buffer drops below threshold)<br> Verify audio output maintains continuity without dropouts or glitches<br> Monitor AAC frame timestamps for consistency at 0.5x rate | Verify audio buffer remains stable, no underflow detected, audio output continuous without dropouts, AAC frame timing consistent |
| 8 | Monitor Pipeline EOS and Validate Test Completion | Continue position polling until `GST_MESSAGE_EOS` is detected on bus via `gst_bus_pop_filtered()`<br> When EOS detected, verify test metrics collected: total position advancement, average rate compliance, audio frame statistics<br> Cross-check if total test duration at 0.5x rate is approximately 2x the stream duration (due to 0.5x slowdown) | Verify `GST_MESSAGE_EOS` detected on bus, test metrics collected, rate compliance summary calculated |
| 9 | Release Pipeline and Cleanup Resources |  Monitor `pts-error-callback` signal - verify no pts-error signals were detected during entire rate-controlled test. Set pipeline state to `GST_STATE_NULL`<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin element<br>via `gst_object_unref(playbin)`. Free allocated memory and close logging file  | Verify no pts-error signals detected during test, pipeline reaches `GST_STATE_NULL`, all GStreamer objects unreferenced, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121









