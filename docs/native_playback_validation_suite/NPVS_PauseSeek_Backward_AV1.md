## TestCase ID
NATIVE_PLAYBACK_158

## TestCase Name
NPVS_PauseSeek_Backward_AV1

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on AV1 encoded video streams using playbin pipeline with westerossink. Execute controlled seek operations via `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to specified position during paused state, then resume playback to verify smooth transition and correct rendering at seeked location. Confirm playback position advances correctly after seek via `gst_element_query_position()` and validate frame rendering statistics via `westerossinkâ†’stats` show no frame discontinuities across seek boundary.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | AV1 Media Stream Provisioning | AV1 DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream: `TDK_Asset_DASH_AV1_AAC/master.mpd` configured in `MediaValidationVariables.py` as `video_src_url_av1` | Verify AV1 DASH stream is accessible via network and MPD manifest can be parsed by GStreamer AV1 demuxer |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_av1` = `test_streams_base_path + "TDK_Asset_DASH_AV1_AAC/master.mpd"` | Verify stream URL resolves to valid, accessible AV1 DASH manifest location |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor AV1 decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and AV1 decoder plugin paths |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, AV1 decoder libraries, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, AV1 decoder plugin paths configured, GStreamer AV1 plugin is available |
| 2 | Configure Playback Pipeline | Create `playbin` element and set `uri` property to AV1 DASH stream (`TDK_Asset_DASH_AV1_AAC/master.mpd` from MediaValidationVariables.py). Configure `westerossink` as video sink | Verify playbin created successfully, URI property set to AV1 DASH manifest, westerossink linked to video output |
| 3 | Perform Initial Playback | Transition pipeline to `GST_STATE_PLAYING` state. Wait for playback startup with initial media buffering. Verify `first-video-frame-callback` signal to confirm AV1 rendering started | Verify pipeline reaches `GST_STATE_PLAYING`, first frame detected on westerossink without errors |
| 4 | Pause Pipeline Before Seek | Transition to `GST_STATE_PAUSED` after initial playback duration (timeout + 20 seconds). Monitor state transition to verify pipeline halts without errors | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current playback position via `gst_element_query_position()`. Invoke `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, no seek errors detected |
| 6 | Resume Playback After Seek | Transition to `GST_STATE_PLAYING` state. Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (Â±250ms tolerance per second). Monitor `westerossinkâ†’stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate |
| 7 | Validate Frame Rendering Continuity | Query `westerossinkâ†’stats` to extract `rendered_frames` and `dropped_frames` values. Verify frame increments are consistent and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek |
| 8 | Release Pipeline Resources | Set pipeline to `GST_STATE_NULL`. Unreference playbin element to deallocate AV1 decoder, demuxer, and sink resources | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer resources released, no memory leaks detected |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121
