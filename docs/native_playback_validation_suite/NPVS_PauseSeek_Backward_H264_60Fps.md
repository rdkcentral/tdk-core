## TestCase ID
NATIVE_PLAYBACK_161

## TestCase Name
NPVS_PauseSeek_Backward_H264_60Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on H.264 60fps DASH video streams. The test executes controlled seek operations to a backward position while paused, then resumes playback to verify smooth transition and correct rendering at the seeked 60fps location. Confirm playback position advances correctly after seek and frame rendering shows no discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | H264 60fps Media Stream Provisioning | H264 60fps DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream: `DASH_H264_60fps/atfms_291_dash_tdk_avc_aac_fmp4.mpd` configured in `MediaValidationVariables.py` as `video_src_url_dash_h264_60fps` | Verify H264 60fps DASH stream is accessible via network and MPD manifest can be parsed by GStreamer H264 demuxer |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_dash_h264_60fps` = `test_streams_base_path + "DASH_H264_60fps/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify stream URL resolves to valid, accessible H264 60fps DASH manifest location |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H264 decoder libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and H264 decoder plugin paths |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, H264 decoder libraries, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, H264 decoder plugin paths configured, GStreamer H264 plugin is available |
| 2 | Configure Playback Pipeline | Create `playbin` element via . Set playbin `uri` property via  from MediaValidationVariables.py.  Monitor playback for initial buffering and verify first frame rendered successfully | Verify pipeline transitions to PLAYING, first frame renders successfully, no GST_MESSAGE_ERROR detected |
| 4 | Pause Pipeline Before Seek |  after initial playback duration (timeout + 20 seconds). Monitor state transition to verify pipeline halts without  | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current position via . Invoke  to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0 or earlier timestamp). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, no seek errors detected |
| 6 | Resume Playback After Seek |  state.  Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate without backward jumps |
| 7 | Validate Frame Rendering Continuity | Query `westerossink→stats` structure via . Extract `rendered_frames` and `dropped_frames` via . Verify frame increments are consistent for 60fps (~16.67ms per frame) and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek at 60fps cadence |
| 8 | Release Pipeline Resources | Set pipeline to  via . Verify all GStreamer resources freed | Verify pipeline reaches GST_STATE_NULL, all resources released, no memory leaks |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121


