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
Test validates seeking capability towards end-of-stream (EOS) on MP4 H.264 video by invoking `gst_element_seek()` to reposition playback near the stream's final position. The test verifies that the seek target position is reached within Â±1 second tolerance using position queries every 100ms, and that playback continues smoothly through the remaining stream until `GST_MESSAGE_EOS` is detected. Validates frame rendering continues with correct PTS monotonicity and no errors are triggered during near-EOS seeking operations.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | H.264 encoded MP4 stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for EOS seeking validation. Stream file path configured as `test_streams_base_path + "TDK_Asset_Sunrise_30fps_v2.mp4"` in MediaValidationVariables.py | Verify H.264 MP4 stream file is accessible and contains complete stream with valid duration for EOS detection |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mp4_30fps` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Sunrise_30fps_v2.mp4` (H.264 30fps stream for EOS seeking) | Verify `video_src_url_mp4_30fps` resolves to valid, accessible MP4 file with complete duration |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H.264 codec libraries, and Wayland display configuration. Establish Wayland display session. Set up logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Verify all environment variables load correctly, Wayland display created, H.264 plugins available, logging initialized |
| 2 | Create Playbin and Configure Video Sink | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Configure URI via `g_object_set(playbin, "uri", stream_url, NULL)` with MP4 stream. Create and set `westerossink` as video sink via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Playbin created, URI configured to MP4 file, westerossink set as video sink |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via `g_signal_connect()` for frame detection. Set playbin flags (VIDEO, AUDIO, BUFFERING). Register bus message handler for ERROR, EOS, STATE_CHANGED via `gst_bus_pop_filtered()` | All signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set pipeline state `GST_STATE_PAUSED` via `gst_element_set_state()`. Query stream duration via `gst_element_query_duration()` to determine EOS position. Transition to `GST_STATE_PLAYING` via `gst_element_set_state()`. Monitor first-frame signal for rendering confirmation | Pipeline PLAYING, stream duration queried, first frame detected, baseline position recorded |
| 5 | Execute Seek Towards EOS | Query current playback position via `gst_element_query_position()`. Calculate seek target as (stream_duration - 5 seconds) to seek near end. Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to perform seek | Seek operation completes without errors, pipeline continues playing from near-EOS position |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for `GST_MESSAGE_ASYNC_DONE` confirming seek completion. Poll `gst_element_query_position()` every 100ms verifying position matches seek target within Â±GST_SECOND (Â±1000ms). Confirm position stabilizes near EOS | Position queries show currentPosition â‰ˆ seekPosition Â±1000ms, EOS seek confirmed |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second. Extract rendered_frames and dropped_frames via `gst_structure_get_uint64()`. Verify rendered frames increment, dropped < 1%. Continue monitoring position to verify playback advances towards EOS | Rendered frame count increases per second, dropped < 1%, position advances towards stream end |
| 8 | Monitor EOS Detection and Stream Completion | Continue monitoring until `GST_MESSAGE_EOS` detected on bus via `gst_bus_pop_filtered()`. Verify no `GST_MESSAGE_ERROR` messages detected. Confirm stream reaches end position without errors or stalls | EOS detected when stream reaches end, no errors, pipeline remained stable |
| 9 | Release Pipeline Resources | Set pipeline state `GST_STATE_NULL` via `gst_element_set_state()`. Unreference playbin via `gst_object_unref()`. Close logging, free memory, verify system ready | Pipeline NULL, all resources released, logging closed |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
