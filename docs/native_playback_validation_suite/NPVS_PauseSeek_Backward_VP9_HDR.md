**TestCase ID**
NATIVE_PLAYBACK_379

**TestCase Name**
NPVS_PauseSeek_Backward_VP9_HDR

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on VP9 HDR encoded WebM video streams using playbin pipeline with westerossink. Execute controlled seek operations via `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to specified position during paused state, then resume playback to verify smooth transition and correct HDR rendering at seeked location. Confirm playback position advances correctly after seek via `gst_element_query_position()` and validate frame rendering statistics via `westerossink→stats` show no frame discontinuities across VP9 HDR seek boundary.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | VP9 HDR Media Stream Provisioning | VP9 HDR WebM stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream: `TDK_Asset_Waterfall_VP9_HDR.webm` configured in `MediaValidationVariables.py` as `video_src_url_vp9_hdr` | Verify VP9 HDR WebM stream is accessible via network and WebM container can be parsed by GStreamer VP9 demuxer with HDR metadata |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_vp9_hdr` = `test_streams_base_path + "TDK_Asset_Waterfall_VP9_HDR.webm"` | Verify stream URL resolves to valid, accessible VP9 HDR WebM manifest location |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor VP9 HDR decoder libraries, `GST_PLUGIN_PATH`, HDR color space configuration) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables, VP9 HDR decoder plugin paths, and HDR metadata handling configured |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, VP9 HDR decoder libraries, HDR color space metadata handlers, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, VP9 HDR decoder plugin paths configured, GStreamer VP9 plugin with HDR capability is available |
| 2 | Configure Playback Pipeline | Create `playbin` element and set `uri` property to VP9 HDR WebM stream (`TDK_Asset_Waterfall_VP9_HDR.webm` from MediaValidationVariables.py). Configure `westerossink` as video sink with HDR capability | Verify playbin created successfully, URI property set to VP9 HDR WebM manifest, westerossink linked to video output |
| 3 | Perform Initial Playback | Transition pipeline to `GST_STATE_PLAYING` state. Wait for playback startup with HDR metadata negotiation. Verify `first-video-frame-callback` signal to confirm VP9 HDR rendering started with correct color space | Verify pipeline reaches `GST_STATE_PLAYING`, first frame detected with HDR metadata without errors |
| 4 | Pause Pipeline Before Seek | Transition to `GST_STATE_PAUSED` after initial playback duration (timeout + 20 seconds). Monitor state transition to verify pipeline halts with HDR state preserved | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current playback position via `gst_element_query_position()`. Invoke `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance, HDR metadata remains valid, no seek errors detected |
| 6 | Resume Playback After Seek | Transition to `GST_STATE_PLAYING` state. Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (±250ms tolerance per second). Monitor westerossink to verify HDR rendering maintained post-seek | Verify playback resumes without stalls, HDR rendering maintained, position advances at expected rate |
| 7 | Validate Frame Rendering Continuity and HDR Metadata | Query `westerossink→stats` to extract `rendered_frames` and `dropped_frames`. Verify frame increments consistent and HDR color metadata preserved across seek boundary | Verify no frame drops at seek boundary, HDR color space maintained, frame rendering smooth post-seek |
| 8 | Release Pipeline Resources | Set pipeline to `GST_STATE_NULL`. Unreference playbin element and restore HDR configuration | Verify pipeline reaches `GST_STATE_NULL`, all resources released, HDR configuration restored |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121

