## TestCase ID
NATIVE_PLAYBACK_16

## TestCase Name
NPVS_Same_Asset_Twice_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pipeline initialization, resource cleanup, and reinitilization capability by playing the same AAC audio stream via dashdemux demuxer twice sequentially. Test creates `playbin` with `westerossink` video-sink, executes first playback with position  Verify no decoder state errors, memory leaks, or resource stalls between playbacks and confirm "Failures: 0" output for both attempts.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary, GStreamer plugins (dashdemux demuxer, necessary decoders), and westerossink element | Verify TDK_Package is installed, binary is executable, dashdemux element available in GStreamer |
| 2 | Media Stream Provisioning | AAC stream must be accessible via network (`souphttpsrc` element for streaming) or local file system (`filesrc`). Stream file path configured in MediaValidationVariables.py as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd is accessible via HTTP or local storage with sufficient duration for at least two sequential playbacks |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_aac` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"`  for both first and second playback attempts | Verify `video_src_url_aac` resolves to valid, accessible AAC stream location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with timeout value (default: 10 seconds). SecondChannelTimeout (same value) used for second playback validation | Verify timeout is set to required value for full stream playback or minimum required time for validation |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables, westerossink available, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, dashdemux demuxer, decoders, westerossink, and Wayland display configuration. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Set ChannelChangeTest flag = true to enable second playback validation | Verify all environment variables load correctly, Wayland display session created successfully, ChannelChangeTest flag configured, logging initialized without errors |
| 2 | Configure Test Framework and Load Stream (First Playback) | Set test name to `test_generic_playback`, Load AAC stream via `video_src_url_aac` variable from MediaValidationVariables.py. Store stream URL in channel_url variable for second playback use. Set timeout to NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT | Verify test case name configured, DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd stream URI resolved and stored, timeout set correctly |
| 3 | Create Playbin Pipeline and Configure Westerossink (First Attempt) | Create `playbin` element via . Set `uri` property to stream URL via . Set `video-sink` property to `westerossink` element (or `autoaudiosink` for audio-only) via  | Verify playbin element created successfully, URI property set to DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd, video-sink properly configured |
| 4 | First Playback: Transition to PLAYING and Monitor Position | Set pipeline state to  via . Monitor  on GStreamer bus. Execute `PlaybackValidation()` function which  Verify position advances at expected rate (1 second per 1 second real-time ±250ms tolerance) for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds | Verify pipeline transitions to PLAYING state without errors, position advances at expected rate with no backward jumps or stalls, timeout playback completes successfully |
| 5 | Release First Playback Pipeline to NULL | Set pipeline state to  via . Verify state transition succeeds without GST_STATE_CHANGE_FAILURE (reference source: MediaPipelineSuite.cpp line 2720). Wait for all buffers to drain and decoders to finalize state | Verify pipeline reaches GST_STATE_NULL state successfully, all pipeline elements transitioned to NULL state, no error messages during state release |
| 6 | Re Initialize data structure flags: `streamStart = FALSE`, `terminate = FALSE` (reference source: MediaPipelineSuite.cpp lines 2733-2734). Verify URI property changed to same stream for second attempt | Verify URI property successfully updated to same stream, internal state flags reset, playbin ready for second playback cycle |
| 7 | Second Playback: Transition to PLAYING and Monitor GST_MESSAGE_STREAM_START | Set pipeline state to  via . Monitor GStreamer bus via  with 2-second timeout (reference source: MediaPipelineSuite.cpp lines 2744-2746). Handle messages and verify `streamStart = TRUE` within timeout without `terminate = TRUE` flag | Verify pipeline transitions to PLAYING state, GST_MESSAGE_STREAM_START detected on bus within 2 seconds, no GST_MESSAGE_ERROR or GST_MESSAGE_EOS initially detected |
| 8 | Second Playback: Validate Position and Playback Continuity | Call `PlaybackValidation()` for second playback with SecondChannelTimeout duration.  Verify position advances at expected rate (±250ms tolerance) identical to first playback. Verify no GST_MESSAGE_ERROR or GST_MESSAGE_WARNING on bus. Query sink properties to verify frame rendering continues without decoder errors (reference source: MediaPipelineSuite.cpp lines 2784-2786) | Verify position advances at consistent rate matching first playback, no position backward jumps or stalls, no error/warning messages on bus, identical playback behavior as first attempt |
| 9 |  Free allocated memory and close logging file. Verify test framework output shows "Failures: 0" and "Errors: 0" for BOTH first and second playback attempts in mediapipelinetests console output | Verify pipeline reaches GST_STATE_NULL, all GStreamer resources released without segmentation faults, test reports zero failures and errors for both playback cycles, no resource leaks detected |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
