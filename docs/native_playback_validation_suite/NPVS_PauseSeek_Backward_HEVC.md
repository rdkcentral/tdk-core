## TestCase ID
NATIVE_PLAYBACK_157

## TestCase Name
NPVS_PauseSeek_Backward_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and backward seek operation on HEVC DASH video streams. The test executes controlled seek operations to a backward position while paused, then resumes playback to verify smooth transition and correct rendering at the seeked location. Confirm playback position advances correctly after seek and frame rendering shows no discontinuities.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | HEVC Media Stream Provisioning | HEVC DASH stream must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`). Stream: `DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd` configured in `MediaValidationVariables.py` as `video_src_url_hevc` | Verify HEVC DASH stream is accessible via network and MPD manifest can be parsed by GStreamer HEVC demuxer |
| 3 | Stream Variable Configuration | Stream URL must be configured in `MediaValidationVariables.py` with variable `video_src_url_hevc` = `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` | Verify stream URL resolves to valid, accessible HEVC DASH manifest location |
| 4 | Playback Timeout and Seek Position Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds) and `NATIVE_PLAYBACK_SEEK_POSITION` (default: 0 seconds) must be configured in device configuration file for seek validation | Verify timeout values are set appropriately for pause, seek, and resume operations |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor HEVC decoder libraries, ) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required environment variables and HEVC decoder plugin paths |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, HEVC decoder libraries, and Wayland display configuration. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` for test execution trace | Verify all environment variables load correctly, HEVC decoder plugin paths configured, GStreamer HEVC plugin is available |
| 2 | Configure Playback Pipeline | Create `playbin` element and set `uri` property to HEVC DASH stream (`DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd` from MediaValidationVariables.py).  Wait for playback startup with initial media buffering. Verify `first-video-frame-callback` signal to confirm HEVC rendering started | Verify pipeline reaches , first frame detected on westerossink without errors |
| 4 | Pause Pipeline Before Seek |  after initial playback duration (timeout + 20 seconds). Monitor state transition to verify pipeline halts without errors | Verify pipeline successfully pauses, position query returns valid paused position |
| 5 | Execute Backward Seek Operation | Query current playback position via . Invoke  with  to seek to `NATIVE_PLAYBACK_SEEK_POSITION` (typically 0). Verify seek completion via `ASYNC_DONE` message | Verify seek position achieved within 1 second tolerance of target position, no seek errors detected |
| 6 | Resume Playback After Seek |  state.  Monitor `westerossink→stats` to verify `rendered_frames` increments smoothly | Verify playback resumes from seeked position without stalls, position advances at expected rate |
| 7 | Validate Frame Rendering Continuity | Query `westerossink→stats` to extract `rendered_frames` and `dropped_frames` values. Verify frame increments are consistent and dropped frames remain below acceptable threshold | Verify no frame drops at seek boundary, frame rendering continues smoothly post-seek |
| 8 | Release Pipeline Resources | Set pipeline to . Unreference playbin element to deallocate HEVC decoder, demuxer, and sink resources | Verify pipeline reaches , all GStreamer resources released, no memory leaks detected |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3-4 minutes

**Priority:** High

**Release Version:** M121

