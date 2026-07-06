## TestCase ID
NATIVE_PLAYBACK_318

## TestCase Name
NPVS_Seek_Towards_EOS_MKV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on MKV Matroska container with H.264 video by invoking `gst_element_seek()` to reposition playback near the stream's final position. The test verifies that the seek target position is reached within Â±1 second tolerance using position queries every 100ms, and that playback continues smoothly through remaining stream until `GST_MESSAGE_EOS` is detected. Validates frame rendering continues with correct PTS monotonicity while matroskademux properly handles cluster positioning during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MKV container stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_MKV.mkv"` in MediaValidationVariables.py. Stream contains H.264 video and audio in MKV container format | Verify MKV file is accessible and matroskademux can parse container |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mkv` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_MKV.mkv"` | Verify stream URL resolves to valid, accessible MKV file location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, matroskademux, H.264 codec libraries, and Wayland display. Establish Wayland session. Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, matroskademux and H.264 plugins available |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure URI via `g_object_set(playbin, "uri", mkv_stream_url, NULL)`. Set `westerossink` as video sink via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Playbin created, MKV URI configured, westerossink set, matroskademux auto-selected |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via `g_signal_connect()`. Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus handler for ERROR, EOS, STATE_CHANGED messages | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set `GST_STATE_PAUSED` via `gst_element_set_state()`. Query stream duration via `gst_element_query_duration()` for EOS position. Transition `GST_STATE_PLAYING`. Monitor first-frame signal | Pipeline PLAYING, duration queried, first frame detected |
| 5 | Execute Seek Towards EOS | Query position via `gst_element_query_position()`. Calculate seek target as (duration - 5 seconds). Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` | Seek completes, matroskademux positions to cluster near EOS, playback continues |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for `GST_MESSAGE_ASYNC_DONE`. Poll `gst_element_query_position()` every 100ms verifying position within Â±1000ms of target. Confirm position stabilizes | Position matches seek target Â±1000ms, EOS seek confirmed |
| 7 | Monitor Video Rendering Through EOS Boundary | Every 1 second poll westerossink stats. Extract rendered_frames and dropped_frames. Verify rendered frames increment, dropped < 1%. Monitor position advancing to stream end | Rendered frames increase per second, dropped < 1%, position advances to EOS |
| 8 | Monitor EOS Detection and Stream Completion | Continue until `GST_MESSAGE_EOS` on bus via `gst_bus_pop_filtered()`. Verify no `GST_MESSAGE_ERROR`. Confirm stream reaches end without errors or stalls | EOS detected at stream end, no errors, pipeline stable |
| 9 | Release Pipeline Resources | Set `GST_STATE_NULL` via `gst_element_set_state()`. Unreference playbin via `gst_object_unref()`. Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
