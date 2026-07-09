## TestCase ID
NATIVE_PLAYBACK_210

## TestCase Name
NPVS_SeekForward_FF2x_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates forward seeking capability on HLS (.m3u8) streaming media by invoking  to jump playback ahead to a position later in the media playlist. The test verifies that the seek target position is reached correctly using position queries every 100ms with tolerance of ±1 second, handling playlist segment availability and discontinuities. Validates playback resumes normally from the forward-seeked position with continuous video frame rendering and no PTS errors detected.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | HLS stream with M3U8 playlist must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (HLS container format for forward fast-forward testing) | Verify master.m3u8 playlist file is accessible and readable from configured path, hlsdemux plugin available for M3U8 parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hls` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` | Verify `video_src_url_hls` resolves to valid HLS manifest URL, playlist contains valid M3U8 structure with variant streams and segment references |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec, HLS streaming libraries. Establish Wayland display. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, HLS plugins available |
| 2 | Create Playbin and Configure Video | Create `playbin` element via . Configure URI via  with .m3u8 playlist. Set `westerossink` as video sink | Playbin created, HLS URI configured, westerossink set |
| 3 | Register Callbacks and Setup Monitoring | Register `first-video-frame-callback` signal via . Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus message handler for ERROR, EOS, STATE_CHANGED | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing | Set state  via . Query initial position via . Transition . Monitor first-frame signal | Pipeline PLAYING, first frame detected, baseline position recorded |
| 5 | Execute Forward Seek on HLS Stream | Query current position via . Calculate forward seek target. Invoke  handling playlist updates | Seek completes, HLS demux updates playlist, playback continues |
| 6 | Validate Forward Seek Accuracy on Streaming | Monitor bus for .  Handle segment boundaries in playlist | Position matches target within ±1000ms, seek confirmed on streaming content |
| 7 | Monitor Video Rendering on Streaming | Every 1 second poll westerossink stats. Extract rendered_frames and dropped_frames. Verify rendered frames increment, dropped < 1%. Query video-pts for monotonicity | Rendered frames increase per second, dropped < 1%, PTS continuous |
| 8 | Monitor EOS and Validate Stream Integrity | Continue until  or timeout. Verify no  during streaming and seeking operations | EOS or timeout detected, no errors on HLS stream |
| 9 |  Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
