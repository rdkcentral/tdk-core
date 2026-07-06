## TestCase ID
NATIVE_PLAYBACK_166

## TestCase Name
NPVS_PauseSeek_Forward_HEVC

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and forward seek operation on HEVC (H.265) encoded video streams using playbin pipeline with westerossink. Execute controlled seek operations via `gst_element_seek()` with `GST_SEEK_FLAG_FLUSH` to seek to a forward position from current playback location during paused state, then resume playback to verify smooth transition and correct rendering at seeked location. Confirm playback position advances correctly after seek via `gst_element_query_position()` and validate frame rendering statistics via `westerossinkâ†’stats` show no frame discontinuities across seek boundary.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest containing HEVC video must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains HEVC (H.265) video and AAC audio (DASH container format for HEVC pause-seek testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux and HEVC decoder plugins available for parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_hevc` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_HEVC_AAC/atfms_291_dash_tdk_hevc_aac_fmp4.mpd"` | Verify `video_src_url_hevc` resolves to valid DASH manifest URL with HEVC content, manifest contains valid MPD structure with HEVC codec profile |
| 4 | Playback Timeout Configuration | Invoke `gst_element_seek()` with GST_SEEK_FLAG_FLUSH to seek forward from current position | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments. Load HEVC stream configuration from MediaValidationVariables.py | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline for HEVC |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with HEVC stream URI, set `westerossink` as video sink, trigger `NULLâ†’READYâ†’PAUSEDâ†’PLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered from HEVC stream, no `GST_MESSAGE_ERROR` |
| 4 | Execute Pause-Then-Seek Operation | Transition to `GST_STATE_PAUSED` after reaching intermediate playback position. Query current position via `gst_element_query_position()`. Invoke `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to seek forward to `NATIVE_PLAYBACK_SEEK_POSITION` | Verify pipeline pauses successfully, position query returns valid paused position, forward seek completes within 1 second |
| 5 | Monitor Playback Progress | Resume `GST_STATE_PLAYING` after seek. Poll playback position via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (Â±250ms tolerance per second) | Verify playback resumes from seeked position without stalls, position advances smoothly without backward jumps |
| 6 | Validate Frame Rendering | Query `westerossink2192stats` to extract `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
