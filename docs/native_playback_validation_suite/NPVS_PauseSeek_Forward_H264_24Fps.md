**TestCase ID**
NATIVE_PLAYBACK_242

**TestCase Name**
NPVS_PauseSeek_Forward_H264_24Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and forward seek operation on H264 encoded 24fps DASH video streams using playbin pipeline with westerossink. Execute controlled seek operations via `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to a forward position from current playback location during paused state, then resume playback to verify smooth transition and correct rendering at seeked 24fps location. Confirm playback position advances correctly after seek via `gst_element_query_position()` and validate frame rendering statistics via `westerossink→stats` show no frame discontinuities across seek boundary.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest at 24fps must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_24fps/master.mpd"` in MediaValidationVariables.py. Stream contains H.264 video at 24fps and AAC audio (DASH container format for 24fps pause-seek testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing at 24fps |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_dash_h264_24fps` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_24fps/master.mpd"` | Verify `video_src_url_dash_h264_24fps` resolves to valid DASH manifest URL at 24fps, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Timeout Configuration | Invoke `gst_element_seek()` with GST_SEEK_FLAG_FLUSH to seek forward from current position | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments. Load H264 24fps format configuration from MediaValidationVariables.py | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline for 24fps format |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with H264 stream URI, set `westerossink` as video sink, trigger `NULL→READY→PAUSED→PLAYING` state transition, verify `first-video-frame-callback` signal at 24fps framerate | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered at 24fps, no `GST_MESSAGE_ERROR` |
| 4 | Perform Initial Playback | Transition pipeline to `GST_STATE_PLAYING` state. Monitor playback for initial buffering and verify first frame rendered successfully | Verify pipeline transitions to PLAYING, first frame renders successfully, no GST_MESSAGE_ERROR detected |
| 5 | Pause Pipeline Before Forward Seek | Transition to `GST_STATE_PAUSED` after reaching intermediate playback position. Monitor state transition to verify pipeline halts without `GST_MESSAGE_ERROR` | Verify pipeline successfully pauses, position query returns valid paused position |
| 6 | Execute Forward Seek Operation | Query current position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`. Invoke `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (forward position timestamp). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, seek moves forward from current position, no seek errors detected |
| 7 | Resume Playback After Seek | Transition to `GST_STATE_PLAYING` state. Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (±250ms tolerance per second). Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate without backward jumps |
| 8 | Validate Frame Rendering Continuity | Query `westerossink→stats` structure via `g_object_get(westerosSink, "stats", &structure, NULL)`. Extract `rendered_frames` and `dropped_frames` via `gst_structure_get_uint64()`. Verify frame increments are consistent for 24fps (~41ms per frame) and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek at 24fps cadence |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Priority:** High

**Release Version:** M121
