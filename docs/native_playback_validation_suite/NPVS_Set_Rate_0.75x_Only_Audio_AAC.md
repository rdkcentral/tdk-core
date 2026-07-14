## TestCase ID
NATIVE_PLAYBACK_279

## TestCase Name
NPVS_Set_Rate_0.75x_Only_Audio_AAC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate playback rate control at 0.75x speed (three-quarter normal) with audio-only AAC stream. The test sets rate to 0.75 and verifies audio position advances at exactly three-quarter the normal speed. Confirm audio decoding continues without discontinuities or buffer underflow during rate changes.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | AAC audio-only stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4"` in MediaValidationVariables.py (audio-only stream with no video track for audio rate control validation) | Verify AAC audio stream file is accessible, readable, contains audio track only (no video), and contains minimum 60 seconds of audio content |
| 3 | Stream Variable Configuration | Stream variable `audio_src_url_mp4_aac` configured in `MediaValidationVariables.py` with path: `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_audio_1.mp4` (stream must contain AAC audio track only, no video track) | Verify `audio_src_url_mp4_aac` resolves to valid, accessible audio-only AAC MP4 file location with AAC codec confirmation |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULLâ†’READYâ†’PAUSEDâ†’PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches  with first frame rendered, no  |
| 4 | Execute Playback Rate Change | Invoke  with playback rate set to 0.75 and GST_SEEK_FLAG_FLUSH flag. Verify position progression matches 0.75x speed (three-quarter normal speed) with maintained audio/video sync | Verify test operation completes successfully with expected results |
| 5 | Monitor Playback Progress | 75x rate (expected increment: 0.075 seconds per 100ms ±25% tolerance) | Verify position increments are consistent, no stalls or backward jumps detected |
| 6 | Validate Frame Rendering | Poll `westerossinkâ†’stats` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to  and release all codec, decoder, and sink resources | Verify pipeline reaches  and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
