**TestCase ID**
NATIVE_PLAYBACK_370

**TestCase Name**
NPVS_PauseSeek_Backward_H264_MOV

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on H264 encoded MOV container video streams using playbin pipeline with westerossink. Execute controlled seek operations via `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to specified position during paused state, then resume playback to verify smooth transition and correct rendering at seeked location. Confirm playback position advances correctly after seek via `gst_element_query_position()` and validate frame rendering statistics via `westerossink→stats` show no frame discontinuities across seek boundary.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | H264 MOV Media Stream Provisioning | H264 MOV container stream must be accessible via HTTPS (`souphttpsrc`) or local file system. Stream: `TDK_Asset_Sunrise_H264_MOV.MOV` configured in `MediaValidationVariables.py` as `video_src_url_h264_mov` | Verify H264 MOV stream is accessible and MOV container can be parsed by GStreamer H264 demuxer |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_h264_mov` = `test_streams_base_path + "TDK_Asset_Sunrise_H264_MOV.MOV"` | Verify stream URL resolves to valid, accessible H264 MOV container location |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H264 decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and H264 decoder plugin paths |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H264 decoder libraries, MOV container demuxer, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, H264 decoder plugin paths configured, MOV container demuxer available, GStreamer H264 plugin is available |
| 2 | Configure Playback Pipeline | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set playbin `uri` property via `g_object_set(playbin, "uri", "TDK_Asset_Sunrise_H264_MOV.MOV", NULL)` from MediaValidationVariables.py. Configure `westerossink` via `g_object_set(playbin, "video-sink", westerosSink, NULL)` | Verify playbin created successfully, URI property set correctly to H264 MOV stream, westerossink linked to video output |
| 3 | Perform Initial Playback | Transition pipeline to `GST_STATE_PLAYING` state. Monitor playback for initial buffering and verify first frame rendered successfully | Verify pipeline transitions to PLAYING, first frame renders successfully, no GST_MESSAGE_ERROR detected |
| 4 | Pause Pipeline Before Seek | Transition to `GST_STATE_PAUSED` after initial playback duration (timeout + 20 seconds). Monitor state transition to verify pipeline halts without `GST_MESSAGE_ERROR` | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Invoke `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0 or earlier timestamp). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, no seek errors detected |
| 6 | Resume Playback After Seek | Transition to `GST_STATE_PLAYING` state. Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (±250ms tolerance per second). Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate without backward jumps |
| 7 | Validate Frame Rendering Continuity | Query `westerossink→stats` structure via `g_object_get(westerosSink, "stats", &structure, NULL)`. Extract `rendered_frames` and `dropped_frames` via `gst_structure_get_uint64()`. Verify frame increments are consistent and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek from MOV container |
| 8 | Release Pipeline Resources | Set pipeline to `GST_STATE_NULL` via `gst_element_set_state()`. Verify all GStreamer resources freed | Verify pipeline reaches GST_STATE_NULL, all resources released, no memory leaks |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121
