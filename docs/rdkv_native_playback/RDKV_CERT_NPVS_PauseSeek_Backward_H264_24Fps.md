## TestCase ID
RDKV_NATIVE_PLAYBACK_241

## TestCase Name
RDKV_CERT_NPVS_PauseSeek_Backward_H264_24Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on H264 encoded 24fps DASH video streams using playbin pipeline with westerossink. Execute controlled seek operations to seek to specified position during paused state, then resume playback to verify smooth transition and correct rendering at seeked 24fps location. Confirm playback position advances correctly after seek and validate frame rendering statistics show no frame discontinuities across seek boundary.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | H264 24fps DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`)<br> Stream: `DASH_H264_24fps/master.mpd` configured in `MediaValidationVariables.py` as `video_src_url_dash_h264_24fps` Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_dash_h264_24fps` = `test_streams_base_path + "DASH_H264_24fps/master.mpd"` | Verify H264 24fps DASH stream is accessible via network and MPD manifest can be parsed by GStreamer H264 demuxer Verify stream URL resolves to valid, accessible H264 24fps DASH manifest location |
| 3 | Playback Timeout and Seek Position Configuration |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds))<br>and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds))<br>must be configured in device configuration file for seek validation  | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H264 decoder libraries, `GST_PLUGIN_PATH`)<br>must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and H264 decoder plugin paths |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H264 decoder libraries, and Wayland display configuration<br> Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, H264 decoder plugin paths configured, GStreamer H264 plugin is available |
| 2 | Configure Playback Pipeline | Create `playbin` element and set `uri` property to H264 24fps DASH stream (`DASH_H264_24fps/master.mpd` from MediaValidationVariables.py)<br> Configure `westerossink` as video sink | Verify playbin created successfully, URI property set, westerossink linked to video output |
| 3 | Perform Initial Playback | Transition pipeline to `GST_STATE_PLAYING` state<br> Wait for playback startup with initial media buffering<br> Verify `first-video-frame-callback` signal to confirm H264 24fps rendering started | Verify pipeline reaches `GST_STATE_PLAYING`, first frame detected on westerossink without errors |
| 4 | Pause Pipeline Before Seek | Transition to `GST_STATE_PAUSED` after initial playback duration (timeout + 20 seconds)<br> Monitor state transition to verify pipeline halts without errors | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current playback position via `gst_element_query_position()`<br> Invoke `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0)<br> Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, no seek errors detected |
| 6 | Resume Playback After Seek | Transition to `GST_STATE_PLAYING` state<br> Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (+/-250ms tolerance per second)<br> Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate |
| 7 | Validate Frame Rendering Continuity | Query `g_object_get(westerossink, "stats")` to extract `rendered_frames` and `dropped_frames` values<br> Verify frame increments are consistent for 24fps (~41ms per frame) and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek at 24fps cadence |
| 8 | Release Pipeline Resources | Set pipeline to `GST_STATE_NULL`. Unreference playbin element to deallocate H264 decoder, demuxer, and sink resources | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer resources released, no memory leaks detected |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-Client

**Estimated Duration:** 4 mins

**Priority:** High













