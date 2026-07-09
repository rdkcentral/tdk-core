## TestCase ID
NATIVE_PLAYBACK_264

## TestCase Name
NPVS_Seek_Towards_EOS_Webm

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on WebM VP9 video stream by invoking  to reposition playback near the stream's final position. The test verifies that the seek target position is reached within ±1 second tolerance using position queries every 100ms, and that playback continues smoothly through remaining stream until  is detected. Validates frame rendering continues with correct PTS monotonicity while webmmux properly handles frame positioning during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | WebM container with VP9 video stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for EOS seeking validation. Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"` in MediaValidationVariables.py. Stream contains VP9 video codec in WebM container format | Verify WebM stream file is accessible and contains complete stream with valid duration for EOS detection |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_webm` configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"` pointing to valid WebM file with VP9 codec (matroskademux compatible format) for EOS seeking | Verify WebM stream resolves to valid, accessible file with complete duration |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, VP9 codec libraries, webmmux, and Wayland display. Establish Wayland session. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, VP9 and webmmux plugins available |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via . Configure URI via . Set `westerossink` as video sink | Playbin created, WebM URI configured, westerossink set |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via . Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus handler for ERROR, EOS, STATE_CHANGED | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set . Query stream duration via . Transition . Monitor first-frame signal | Pipeline PLAYING, duration queried, first frame detected |
| 5 |  Calculate seek target as (duration - 5 seconds). Invoke  | Seek completes, VP9 stream positioned near EOS, playback continues |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for .  Confirm position stabilizes | Position matches seek target ±1000ms |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second. Verify rendered_frames increment, dropped < 1%. Monitor position advancing to stream end | Rendered frames increase, dropped < 1%, position advances to EOS |
| 8 | Monitor EOS Detection and Stream Completion | Continue until  on bus. Verify no . Confirm stream reaches end without errors | EOS detected at stream end, no errors |
| 9 |  Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
