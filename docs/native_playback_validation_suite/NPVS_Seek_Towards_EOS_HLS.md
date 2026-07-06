**TestCase ID**
NATIVE_PLAYBACK_263

**TestCase Name**
NPVS_Seek_Towards_EOS_HLS

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on HLS (.m3u8) streaming format by invoking `gst_element_seek()` to reposition playback near the stream's final position. The test verifies that the seek target position is reached within ±1 second tolerance using position queries every 100ms, and that playback continues smoothly through remaining stream segments until `GST_MESSAGE_EOS` is detected. Validates frame rendering continues with correct PTS monotonicity while hlsdemux properly handles segment selection and playlist discontinuities during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | HLS stream with M3U8 playlist must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (HLS container format for EOS seeking testing) | Verify master.m3u8 playlist file is accessible and readable from configured path, hlsdemux plugin available for M3U8 parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hls` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "HLS_H264_AAC/master.m3u8"` | Verify `video_src_url_hls` resolves to valid HLS manifest URL, playlist contains valid M3U8 structure with variant streams and segment references |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec, HLS streaming (hlsdemux), and Wayland display. Establish Wayland session. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, HLS and H.264 plugins available |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure URI via `g_object_set(playbin, "uri", hls_playlist_url, NULL)` with .m3u8 endpoint. Set `westerossink` as video sink | Playbin created, HLS URI configured, westerossink set, hlsdemux auto-selected |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via `g_signal_connect()`. Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus handler for ERROR, EOS, STATE_CHANGED messages | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set `GST_STATE_PAUSED` via `gst_element_set_state()`. Query stream duration via `gst_element_query_duration()` (requires hlsdemux playlist parsing). Transition `GST_STATE_PLAYING`. Monitor first-frame signal | Pipeline PLAYING, duration queried from playlist, first frame detected |
| 5 | Execute Seek Towards EOS | Query position via `gst_element_query_position()`. Calculate seek target as (duration - 5 seconds). Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` handling playlist updates | Seek completes, hlsdemux selects near-EOS segments, playback continues |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for `GST_MESSAGE_ASYNC_DONE`. Poll `gst_element_query_position()` every 100ms verifying within ±1000ms of target. Handle segment boundaries in playlist | Position matches seek target ±1000ms, EOS seek confirmed on streaming |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second. Verify rendered_frames increment, dropped < 1%. Monitor position advancing through final segments to EOS | Rendered frames increase per second, dropped < 1%, position advances through final segments |
| 8 | Monitor EOS Detection and Stream Completion | Continue until `GST_MESSAGE_EOS` on bus via `gst_bus_pop_filtered()`. Verify no `GST_MESSAGE_ERROR` during streaming and seeking | EOS detected when playlist ends, no errors on HLS stream |
| 9 | Release Pipeline Resources | Set `GST_STATE_NULL`. Unreference playbin via `gst_object_unref()`. Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
