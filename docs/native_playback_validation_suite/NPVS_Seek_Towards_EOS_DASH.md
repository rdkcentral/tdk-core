## TestCase ID
NATIVE_PLAYBACK_261

## TestCase Name
NPVS_Seek_Towards_EOS_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on DASH (Dynamic Adaptive Streaming over HTTP) media presentation by invoking  to reposition playback near the stream's final position. The test verifies that the seek target position is reached within ±1 second tolerance using position queries every 100ms, and that playback continues smoothly through remaining stream segments until  is detected. Validates frame rendering continues with correct PTS monotonicity while dashdemux properly handles segment selection and MPD (Media Presentation Description) updates during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for EOS seeking testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_dash` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec, DASH streaming (dashdemux), and Wayland display. Establish Wayland session. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, DASH and H.264 plugins available |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via . Configure URI via  with .mpd endpoint. Set `westerossink` as video sink | Playbin created, DASH URI configured, westerossink set, dashdemux auto-selected |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via . Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus handler for ERROR, EOS, STATE_CHANGED messages | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set  via . Query stream duration via  (requires dashdemux MPD parsing). Transition . Monitor first-frame signal | Pipeline PLAYING, duration queried from MPD, first frame detected |
| 5 |  Calculate seek target as (duration - 5 seconds). Invoke  handling manifest updates | Seek completes, dashdemux selects near-EOS segments, playback continues |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for .  Handle segment boundaries in manifest | Position matches seek target ±1000ms, EOS seek confirmed on DASH stream |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second. Verify rendered_frames increment, dropped < 1%. Monitor position advancing through final segments to EOS | Rendered frames increase per second, dropped < 1%, position advances through final DASH segments |
| 8 | Monitor EOS Detection and Stream Completion | Continue until  on bus via . Verify no  during streaming and seeking | EOS detected when stream ends, no errors on DASH presentation |
| 9 |  Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
