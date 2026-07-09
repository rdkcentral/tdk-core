## TestCase ID
NATIVE_PLAYBACK_259

## TestCase Name
NPVS_Appsrc_Audio_Underflow_Signal_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate buffer underflow signal detection during custom Appsrc audio pipeline. The test intentionally triggers buffer starvation and verifies that underflow signals are properly emitted and detected through the pipeline.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | AAC stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for Appsrc feeding. Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"` in MediaValidationVariables.py | Verify AAC stream file is accessible and readable from filesystem |
| 3 | Stream Variable Configuration | Stream variable `audio_src_url_mp4_aac` configured in `MediaValidationVariables.py` with path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4` (Appsrc requires local file access, not DASH/HLS streams) | Verify `audio_src_url_mp4_aac` resolves to valid, accessible AAC file location |
| 4 | Appsrc Buffer Threshold Configuration | `BYTES_THRESHOLD` must be configured to 548409 bytes (actual threshold value from test script) to trigger aac underflow condition. This value defines the Appsrc buffer fill level before starvation signal is triggered | Verify BYTES_THRESHOLD = 548409 bytes is set in Appsrc configuration or test parameters |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables and Wayland display is active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, Wayland display is created successfully, logging initialized without errors |
| 2 | Configure Appsrc Pipeline and Load Media | Create `playbin` element via  and configure `uri` property to `appsrc://` via . Set `video-sink` property via  | Verify playbin element created successfully, `uri` property configured to `appsrc://`, and `video-sink` property is set |
| 3 | Register Appsrc Callbacks and Setup Pipeline | Register `source-setup` signal via . Set Appsrc `size` property via . Register sink element signals `buffer-underflow-callback`, `first-audio-frame-callback` or `first-video-frame-callback`, and `pts-error-callback` via . Configure `video-sink` property to `westerossink` via  | Verify `source-setup`, `buffer-underflow-callback`, frame callback, and `pts-error-callback` signals are registered, Appsrc `size` property is set, and `video-sink` property is configured |
| 4 | Start Appsrc Data Feeding and Transition to Playing State | Set pipeline to  via . Emit `push-buffer` action on Appsrc via  until `BYTES_THRESHOLD = 548409 bytes` is reached.  via . Monitor first-frame signal to confirm rendering started | Verify pipeline state transitions to PAUSED then PLAYING, buffers pushed to Appsrc reach 548409 bytes threshold, first-frame signal is detected |
| 5 | Intentionally Starve Buffer to Trigger Underflow | Stop emitting `push-buffer` action on Appsrc to create buffer starvation. Monitor `buffer-underflow-callback` signal to detect underflow condition | Verify `buffer-underflow-callback` signal is detected when sink buffer depletes |
| 6 | Resume Data Feeding with Increased Buffer Threshold and Emit EOS | Resume emitting `push-buffer` action on Appsrc to accumulate `2 * BYTES_THRESHOLD = 1096818 bytes`. After all media data is transferred to Appsrc, emit `end-of-stream` action via  | Verify buffers accumulated to 1096818 bytes threshold and `end-of-stream` action is emitted |
| 7 | Validate Playback Recovery After Buffer Refill |  via . Query playback position via  at 100ms intervals to verify position advances at expected rate (1 second position per 1 second real-time ±250ms tolerance). Monitor `pts-error-callback` signal to detect presentation timestamp errors. Query sink element properties to verify frame rendering continues | Verify position advances at expected rate with no backward jumps, no `pts-error-callback` signals detected, sink continues rendering without stalls |
| 8 | Monitor Pipeline EOS and Validate Test Completion | Monitor GStreamer bus via  to detect  message from pipeline. Verify test framework output confirms execution success. Compare recorded playback metrics against expected baseline values | Verify  is detected on bus, test execution completed successfully with expected metrics matching baseline |
| 9 |  Free allocated memory and close logging file | Verify pipeline reaches , all GStreamer resources released, logging closed, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
