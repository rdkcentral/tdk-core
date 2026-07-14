## TestCase ID
NATIVE_PLAYBACK_252

## TestCase Name
NPVS_SeekForward_FF2x_H264_24Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate forward seek operation to future position beyond current playback location. The test invokes  with target position ahead of current timestamp, simulating user fast-skip behavior. Verify seek operation repositions pipeline to the forward target without stalling or buffer underflow exceptions. Confirm position queries return values matching the forward seek target, and for DASH streams verify dashdemux correctly repositions to the appropriate segment boundary; for HLS verify hlsdemux skips to correct playlist segment. Resume playback from seeked position and validate continuous rendering without glitches.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest at 24fps must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_24fps/master.mpd"` in MediaValidationVariables.py. Stream contains H.264 video at 24fps and AAC audio (DASH container format for 24fps forward fast-forward testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing at 24fps |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash_h264_24fps` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_24fps/master.mpd"` | Verify `video_src_url_dash_h264_24fps` resolves to valid DASH manifest URL at 24fps, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, H.264 plugins available, logging initialized |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via . Configure URI via  with H.264 24fps stream. Create and set `westerossink` as video sink | Playbin created, URI configured, westerossink set as video sink |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via  for frame detection. Set playbin flags (VIDEO, AUDIO, BUFFERING) via . Register bus message handler | All signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set pipeline state .  via . Query initial position via . Monitor first-frame signal | Pipeline state changed to PLAYING, first frame detected, baseline position recorded |
| 5 | Execute Forward Seek Operation | Query current position via . Calculate seek target later in stream. Invoke  | Seek operation completes without errors, pipeline continues playing |
| 6 | Validate Seek Target Accuracy | Monitor bus for  confirming seek completion.  Extract rendered_frames and dropped_frames via . Verify rendered frames increment, dropped < 1%. Query video-pts for monotonicity | Rendered frames increase per second, dropped < 1%, PTS advances without gaps |
| 8 | Monitor EOS and Validate Quality | Continue monitoring until  on bus or timeout. Verify no  throughout operation | EOS detected or timeout, no errors, PTS strictly increasing |
| 9 |  Close logging, free memory | Pipeline NULL, all resources released, system ready |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121

