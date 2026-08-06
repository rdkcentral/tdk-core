## TestCase ID
RDKV_NATIVE_PLAYBACK_380

## TestCase Name
RDKV_CERT_NPVS_PauseSeek_Forward_VP9_HDR

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate pause and forward seek operation on VP9 HDR encoded WebM video streams using playbin pipeline with westerossink. Execute controlled seek operations to seek to a forward position from current playback location during paused state, then resume playback to verify smooth HDR rendering at seeked location. Confirm playback position advances correctly after seek and validate frame rendering statistics show no frame discontinuities across VP9 HDR seek boundary.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  WebM container with VP9 HDR video stream must be accessible via local file system (`filesrc`))<br>or HTTPS (`souphttpsrc`). Stream file configured as `test_streams_base_path + "TDK_Asset_Waterfall_VP9_HDR.webm"` in MediaValidationVariables.py. Stream contains VP9 HDR (High Dynamic Range))<br>video with Opus audio in WebM container format (for VP9 HDR pause-seek testing))<br>Stream variable `video_src_url_vp9_hdr` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "TDK_Asset_Waterfall_VP9_HDR.webm"`  | Verify WebM file is accessible and readable from configured path, matroskademux and VP9 HDR decoder plugins available for playback Verify `video_src_url_vp9_hdr` resolves to valid WebM container file with VP9 HDR video and Opus audio data |
| 3 | Playback Timeout Configuration | Invoke `gst_element_seek()` with GST_SEEK_FLAG_FLUSH to seek forward from current position | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session<br>via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments<br> Load VP9 HDR stream configuration from MediaValidationVariables.py | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline for VP9 HDR |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with VP9 HDR stream URI, set `westerossink` as video sink, trigger `NULLREADYPAUSEDPLAYING` state transition, verify<br>`first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered from VP9 HDR stream, no `GST_MESSAGE_ERROR` |
| 4 | Execute Pause-Then-Seek Operation | Transition to `GST_STATE_PAUSED` after reaching intermediate playback position<br> Query current position via `gst_element_query_position()`<br> Invoke `gst_element_seek(playbin, NORMAL_PLAYBACK_RATE, GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH, GST_SEEK_TYPE_SET, seekPosition, GST_SEEK_TYPE_NONE, GST_CLOCK_TIME_NONE)` to seek forward to `NATIVE_PLAYBACK_SEEK_POSITION` | Verify pipeline pauses successfully, position query returns valid paused position, forward seek completes within 1 second |
| 5 | Monitor Playback Progress |  Resume `GST_STATE_PLAYING` after seek. Poll playback position<br>via `gst_element_query_position()` at 100ms intervals to verify position advances at normal playback rate (+/-250ms tolerance per second)  | Verify playback resumes from seeked position without stalls, position advances smoothly without backward jumps |
| 6 | Validate Frame Rendering | Query `g_object_get(westerossink, "stats")` to extract `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121











