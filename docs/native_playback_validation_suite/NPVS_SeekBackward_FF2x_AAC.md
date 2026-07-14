## TestCase ID
NATIVE_PLAYBACK_185

## TestCase Name
NPVS_SeekBackward_FF2x_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates backward seeking capability on AAC audio stream by invoking  to rewind playback to a position earlier in the media stream. The test verifies that the seek target position is reached correctly using position queries every 100ms with tolerance of ±1 second. Validates playback resumes normally from the backward-seeked position with continuous audio frame rendering and no PTS errors detected.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | AAC audio-only stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for backward seek testing. Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"` in MediaValidationVariables.py. Stream must contain audio track only (no video track) | Verify AAC audio stream file is accessible, readable, contains audio track only, and minimum 60 seconds duration for seek operations |
| 3 | Stream Variable Configuration | Stream variable `audio_src_url_mp4_aac` configured in `MediaValidationVariables.py` with path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4` (local file access required, not DASH/HLS) | Verify `audio_src_url_mp4_aac` resolves to valid, accessible audio-only AAC MP4 file location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config. Backward seek operations require sufficient timeout for position stabilization
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables for audio playback pipeline |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, AAC codec libraries, audio pipeline libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, GStreamer plugins available, logging initialized |
| 2 | Create Playbin and Configure Audio Components | Create `playbin` element via . Configure URI via  with AAC stream path. Set playbin flags (AUDIO, BUFFERING) via  | Playbin created, URI set to AAC stream, audio flags configured |
| 3 | Register Callbacks and Setup Audio Monitoring | Register `first-audio-frame-callback` signal via  for audio frame detection. Register bus message handler via  for , , . Set async-handling via  | All signals registered, bus handler active, async-handling enabled |
| 4 | Transition Pipeline to Playing State | Set pipeline state to  via . Query initial position via .  via . Monitor first-audio-frame-callback signal | Pipeline state changed to PLAYING, first audio frame signal detected, baseline position recorded |
| 5 | Execute Backward Seek Operation | Query current position via . Calculate backward seek target (e.g., -30 seconds from current). Invoke  | Seek operation completes without errors, pipeline continues playing |
| 6 | Validate Seek Target Accuracy | Monitor bus for  confirming seek completion.  Confirm position stabilizes at target | Position queries show currentPosition ≈ seekPosition ±1000ms, seek confirmed successful |
| 7 | Monitor Audio Rendering and Validate Continuity | Every 1 second, retrieve audio sink statistics. Continue polling position every 100ms. Verify audio renders continuously without dropouts. Check for  on bus | Audio frames render continuously, no dropouts, position advances at normal rate ±250ms, no errors |
| 8 | Monitor EOS and Confirm Test Integrity | Continue monitoring until  detected on bus or timeout reached. Verify no  throughout operation | EOS detected or timeout reached, no errors, audio quality maintained |
| 9 | Release Pipeline Resources | Set pipeline state to  via . Unreference playbin via . Close logging file, free allocated memory | Pipeline state becomes NULL, all resources released, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121

