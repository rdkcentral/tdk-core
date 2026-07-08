## TestCase ID
NATIVE_PLAYBACK_262

## TestCase Name
NPVS_Seek_Towards_EOS_MP4

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on MP4 H.264 video by invoking  to reposition playback near the stream's final position. The test verifies that the seek target position is reached within ±1 second tolerance using position queries every 100ms, and that playback continues smoothly through the remaining stream until  is detected. Validates frame rendering continues with correct PTS monotonicity and no errors are triggered during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | H.264 encoded MP4 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for EOS seeking validation. Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_30fps_v2.mp4"` in MediaValidationVariables.py | Verify H.264 MP4 stream file is accessible and contains complete stream with valid duration for EOS detection |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mp4_30fps` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_30fps_v2.mp4` (H.264 30fps stream for EOS seeking) | Verify `video_src_url_mp4_30fps` resolves to valid, accessible MP4 file with complete duration |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, H.264 plugins available, logging initialized |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via . Configure URI via  with MP4 stream. Create and set `westerossink` as video sink via  | Playbin created, URI configured to MP4 file, westerossink set as video sink |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via  for frame detection. Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus message handler for ERROR, EOS, STATE_CHANGED via  | All signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set pipeline state  via . Query stream duration via  to determine EOS position.  via . Monitor first-frame signal for rendering confirmation | Pipeline PLAYING, stream duration queried, first frame detected, baseline position recorded |
| 5 |  Calculate seek target as (stream_duration - 5 seconds) to seek near end. Invoke  to perform seek | Seek operation completes without errors, pipeline continues playing from near-EOS position |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for  confirming seek completion.  Confirm position stabilizes near EOS | Position queries show currentPosition ≈ seekPosition ±1000ms, EOS seek confirmed |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second. Extract rendered_frames and dropped_frames via . Verify rendered frames increment, dropped < 1%. Continue monitoring position to verify playback advances towards EOS | Rendered frame count increases per second, dropped < 1%, position advances towards stream end |
| 8 | Monitor EOS Detection and Stream Completion | Continue monitoring until  detected on bus via . Verify no  messages detected. Confirm stream reaches end position without errors or stalls | EOS detected when stream reaches end, no errors, pipeline remained stable |
| 9 |  Close logging, free memory, verify system ready | Pipeline NULL, all resources released, logging closed |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121

