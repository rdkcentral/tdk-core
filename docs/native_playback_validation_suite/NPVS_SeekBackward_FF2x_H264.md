## TestCase ID
NATIVE_PLAYBACK_188

## TestCase Name
NPVS_SeekBackward_FF2x_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate backward seek operation to prior position within already-played stream content. The test invokes  with target position prior to current timestamp, simulating user rewind/review behavior. Verify seek operation safely repositions without underflowing past stream start (GST_CLOCK_TIME_NONE) or causing pipeline errors. Confirm position queries return values matching the backward seek target, and validate demuxer correctly repositions to earlier segments (dashdemux/hlsdemux) or cluster boundaries (matroskademux) within the container. Resume playback and verify rendering continues without discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for backward fast-forward testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash_h264` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_dash_h264` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config. Backward seek operations require sufficient timeout for position stabilization
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, H.264 plugins available, logging initialized |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via . Configure URI via  with H.264 stream path. Create and set `westerossink` as video sink via  | Playbin created successfully, URI configured, westerossink set as video sink |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via  for frame detection. Set playbin flags (VIDEO, AUDIO, BUFFERING) via . Register bus message handler | All signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set pipeline state  via .  via . Query initial position via . Monitor first-frame signal for rendering confirmation | Pipeline state changed to PLAYING, first frame signal detected, baseline position recorded |
| 5 | Execute Backward Seek Operation | Query current playback position via . Calculate seek target earlier in stream (e.g., -30 seconds from current). Invoke  | Seek operation completes without errors, pipeline continues playing |
| 6 | Validate Seek Target Accuracy | Monitor bus via  for  confirming seek completion.  Confirm position stabilizes at target | Position queries show currentPosition ≈ seekPosition ±1000ms, seek confirmed successful |
| 7 | Monitor Playback Continuation and Frame Statistics | Continue polling position every 100ms. Every 1 second, poll westerossink stats via . Extract rendered_frames and dropped_frames via . Verify rendered frames increment, dropped frames < 1%. Query video-pts via  | Rendered frame count increases per second, dropped < 1%, PTS advances without gaps |
| 8 | Monitor EOS and Validate Playback Quality | Continue monitoring until  detected on bus via . Verify no  messages detected. Confirm PTS monotonicity maintained - no backward jumps | EOS detected or timeout reached, no errors, PTS strictly increasing |
| 9 | Release Pipeline Resources | Set pipeline state  via . Unreference playbin via . Close logging, free memory, verify system ready | Pipeline state becomes NULL, all resources released, logging closed |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121

