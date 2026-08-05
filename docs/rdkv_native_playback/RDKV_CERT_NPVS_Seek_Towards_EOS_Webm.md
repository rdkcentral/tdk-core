## TestCase ID
RDKV_NATIVE_PLAYBACK_264

## TestCase Name
RDKV_CERT_NPVS_Seek_Towards_EOS_Webm

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test validates seeking capability towards end-of-stream (EOS) on WebM VP9 video stream by invoking to reposition playback near the stream's final position. The test verifies that the seek target position is reached within +/-1 second tolerance using position queries every 100ms, and that playback continues smoothly through remaining stream until is detected. Validates frame rendering continues with correct PTS monotonicity while webmmux properly handles frame positioning during near-EOS seeking operations.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | WebM container with VP9 video stream must be accessible via local file system (`filesrc`) or HTTPS (`souphttpsrc`) for EOS seeking validation<br> Stream file configured as `test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"` in MediaValidationVariables.py<br> Stream contains VP9 video codec in WebM container format Stream variable `video_src_url_webm` configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Sunrise_VP9_Opus.webm"` pointing to valid WebM file with VP9 codec (matroskademux compatible format) for EOS seeking | Verify WebM stream file is accessible and contains complete stream with valid duration for EOS detection Verify WebM stream resolves to valid, accessible file with complete duration |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source `/opt/TDK/TDK.env` to load GStreamer plugins, VP9 codec libraries, webmmux, and Wayland display<br> Establish Wayland session<br> Setup logging to `/opt/TDK/mediapipeline_trickplay_test_step.log` | Environment variables load, Wayland created, VP9 and webmmux plugins available |
| 2 | Create Playbin and Configure Video Sink |  Create `playbin` element<br>via `gst_element_factory_make("playbin", NULL)`. Configure URI<br>via `g_object_set(playbin, "uri", webm_stream_url, NULL)`. Set `westerossink` as video sink  | Playbin created, WebM URI configured, westerossink set |
| 3 | Register Callbacks and Setup State Machine | Register `first-video-frame-callback` signal via `g_signal_connect()`<br> Set playbin flags (VIDEO, AUDIO, BUFFERING)<br> Register bus handler for ERROR, EOS, STATE_CHANGED | Signals registered, flags configured, bus monitoring active |
| 4 | Transition Pipeline to Playing State | Set `GST_STATE_PAUSED`<br> Query stream duration via `gst_element_query_duration()`<br> Transition `GST_STATE_PLAYING`<br> Monitor first-frame signal | Pipeline PLAYING, duration queried, first frame detected |
| 5 | Execute Seek Towards EOS | Query position via `gst_element_query_position()`<br> Calculate seek target as (duration - 5 seconds)<br> Invoke `gst_element_seek(playbin, 1.0, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` | Seek completes, VP9 stream positioned near EOS, playback continues |
| 6 | Validate EOS Seek Target Accuracy | Monitor bus for `GST_MESSAGE_ASYNC_DONE`<br> Poll `gst_element_query_position()` every 100ms within +/-1000ms of target<br> Confirm position stabilizes | Position matches seek target +/-1000ms |
| 7 | Monitor Video Rendering Through EOS Boundary | Poll westerossink stats every 1 second<br> Verify rendered_frames increment, dropped < 1%<br> Monitor position advancing to stream end | Rendered frames increase, dropped < 1%, position advances to EOS |
| 8 | Monitor EOS Detection and Stream Completion | Continue until `GST_MESSAGE_EOS` on bus. Verify no `GST_MESSAGE_ERROR`. Confirm stream reaches end without errors | EOS detected at stream end, no errors |
| 9 | Release Pipeline Resources | Set `GST_STATE_NULL`. Unreference playbin via `gst_object_unref()`. Close logging, free memory | Pipeline NULL, resources released |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121







