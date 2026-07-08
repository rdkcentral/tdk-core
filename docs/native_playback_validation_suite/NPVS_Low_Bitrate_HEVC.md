## TestCase ID
NATIVE_PLAYBACK_155

## TestCase Name
NPVS_Low_Bitrate_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HEVC video playback at low bitrate. The test applies fixed low-bitrate configuration to verify frame rendering performance and A/V synchronization during sustained low-bitrate playback. Confirm no frame drops or stalls occur during low-bitrate HEVC playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent GStreamer libraries including HEVC decoder | Verify TDK_Package is installed, binary is executable, all libraries are available, HEVC decoder plugins loaded |
| 2 | Media Stream Provisioning | HEVC video stream configured for low bitrate must be accessible via HTTP/HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream file path configured as `video_src_url_bitrate_hevc` in MediaValidationVariables.py (external stream). Fixed device properties applied: connection_speed=550 kbps, height=288 (applies uniformly to Video_Accelerator) | Verify HEVC low-bitrate stream file is accessible and readable with 288p resolution for Video_Accelerator |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_bitrate_hevc` configured in `MediaValidationVariables.py` with external DASH stream URL containing HEVC low-bitrate stream. Fixed connection_speed=550 kbps and height=288 properties must be applied uniformly across Video_Accelerator (only supported model) | Verify `video_src_url_bitrate_hevc` resolves to valid external HEVC low-bitrate stream with connection_speed=550 and height=288 applied to Video_Accelerator |
| 4 | Playback Timeout and AV Status Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` passed as command-line argument (`timeout=10`) to test binary; specifies minimum timeout duration for low-bitrate stream playback verification at 300 kbps connection speed | Verify timeout parameter passed is minimum 10 seconds for sustained low-bitrate playback |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor HEVC decoder libraries, ) must be defined in `/opt/TDK/TDK.env` for low-bitrate HEVC playback support on Video_Accelerator (only supported model) | Verify `/opt/TDK/TDK.env` exists with all required environment variables for HEVC decoding at 288p resolution |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Apply Fixed Device Properties | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer HEVC decoder plugins and vendor libraries via `LD_PRELOAD`. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace. Apply fixed connection_speed property (550 kbps) and height property (288) for Video_Accelerator. No device-specific adjustment required for HEVC low-bitrate | Verify all environment variables load correctly, HEVC plugins available, Wayland display created, fixed connection_speed=550 and height=288 properties applied for Video_Accelerator |
| 2 | Retrieve Configuration and Construct Playbin Pipeline with Low-Bitrate Properties | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` from device config file. Apply fixed connection_speed property (550 kbps) and height property (288) for Video_Accelerator. Retrieve stream variable `video_src_url_bitrate_hevc` from MediaValidationVariables.py. Create `playbin` element via . Set URI property via  | Verify playbin element created with connection_speed=550/height=288 properties for Video_Accelerator, stream URL configured for HEVC low-bitrate playback |
| 3 | Configure Westerossink and Register Callbacks | Create `westerossink` element via . Connect as video sink via . Register `first-video-frame-callback` signal via  to verify rendering begins. Set playback flags to  via  | Verify westerossink configured for low-bitrate resolution playback, first-frame callback registered |
| 4 | Transition Pipeline to PLAYING State with Low-Bitrate Configuration | Set pipeline state to  via . Poll  until state change completes. Confirm `firstFrameReceived == true` callback indicates HEVC frame rendering started at configured 550 kbps with 288p resolution for Video_Accelerator | Verify pipeline reaches  without , first-frame signal detected within timeout, rendering at 550 kbps/288p |
| 5 | Monitor Low-Bitrate Frame Rendering Performance | Poll `westerossink→stats` via  at 100ms intervals. Extract `rendered_frames` and `dropped_frames` counters via . Verify `rendered_frames` increments smoothly (no stalls) throughout low-bitrate 550 kbps playback. Confirm `dropped_frames` remains at 0 or minimal (baseline threshold) | Verify frame statistics show consistent rendering with acceptable frame delivery for 550 kbps low-bitrate HEVC stream |
| 6 | Validate Playback Position Advancement at 550 kbps Low-Bitrate Rate | Query playback position via  at 100ms intervals. Verify position advances at 1x rate (1 second per real-time second ±250ms tolerance) under 550 kbps connection_speed. Confirm no backward jumps or stalls in position during low-bitrate playback | Verify position advances smoothly without gaps at 550 kbps, validating HEVC decoder performance under low-bandwidth constraints |
| 7 | Monitor Sustained Playback and Buffer Status at 550 kbps | Continue monitoring for `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` seconds (typically 10 seconds) to validate sustained playback stability at 550 kbps. Poll pipeline bus via  to check for  or buffer underflow conditions. Verify no decode errors occur during extended low-bitrate stream playback | Verify playback sustained without errors for full timeout duration at 550 kbps, no buffer underruns from HEVC bitrate constraints |
| 8 | Execute Pause-Resume Cycle to Validate State Management | Transition pipeline to  via . Verify playback halts and position freezes. Resume to . Verify playback resumes without drops and position continues from pause point. Confirm rendered_frames counter resumes incrementing | Verify state transitions successful, pause halts playback completely, resume continues smoothly |
| 9 |  Monitor test framework output for "Failures: 0" and "Errors: 0" or "failed: 0" string. Close logging file and verify all GStreamer resources freed | Verify pipeline reaches , test status shows zero failures, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-5 minutes

**Priority:** High

**Release Version:** M121
