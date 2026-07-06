**TestCase ID**
NATIVE_PLAYBACK_11

**TestCase Name**
NPVS_Play_4K_DASH

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate 4K (3840×2160) resolution playback via `test_generic_playback` function with H.264 video codec and AAC audio. Initialize playbin with dashdemux demuxing, query video sink properties via `westerossink→video-height` and `westerossink→video-width`. Verify resolution matches expected 3840×2160 (±5 pixel tolerance). Execute 10-second playback monitoring position via `gst_element_query_position()`, validate frame rendering statistics via `westerossink→stats`. Confirm clean pipeline state transitions and error-free playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH H.264 AAC stream (`atfms_291_dash_tdk_avc_aac_fmp4.mpd`) must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) element with `dashdemux` capable of parsing DASH container  | Verify DASH stream is accessible and contains valid H.264 and AAC representations |
| 3 | Stream Variable Configuration | `video_src_url_dash` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_dash` resolves to valid DASH location with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout configured for standard playback (10 seconds) | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`; Establish Wayland display session via RDKWindowManager; Set up logging file | Verify environment loaded, Wayland display created |
| 2 | Configure Test with Resolution Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_dash`; Execute `mediapipelinetests test_generic_playback <URL> timeout=<seconds>` | Verify mediapipelinetests initializes with 4K stream |
| 3 | Construct H.264 Pipeline with Resolution Stream | Create `playbin` element; Configure `uri` to video_src_url_dash (DASH); Set `westerossink` as video sink; Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, DASH parsed successfully |
| 4 | Query Video Dimensions and Validate Resolution | Query `westerossink→video-height` and `westerossink→video-width` via `g_object_get()`; Extract values (3840±5 height, 2160±5 width expected) | Verify video-height == 2160±5 pixels; Verify video-width == 3840±5 pixels |
| 5 | Play Stream and Monitor Position | Execute continuous playback for configured timeout (10 seconds); Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (±1 second), no stalls |
| 6 | Validate Frame Rendering at Resolution | Query `westerossink→stats` to verify `rendered_frames` increments consistently at 4K resolution; Verify `dropped_frames` < 1% of rendered_frames | Verify frame statistics indicate proper 4K rendering |
| 7 | Verify Audio-Video Synchronization | Query `n-audio` property to confirm audio stream; Verify audio and video remain synchronized throughout playback | Verify audio stream present; Verify A/V sync maintained |
| 8 | Monitor GStreamer Bus | Monitor message bus via `gst_bus_pop()` for errors or warnings; Verify clean decoding without format errors | Verify no decoder or format errors |
| 9 | Release Resources and Verify Success | Call `terminatePipeline(playbin)` to release all resources; Verify test output contains "Failures: 0" confirming 4K playback successful | Verify clean shutdown; Verify test passed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
