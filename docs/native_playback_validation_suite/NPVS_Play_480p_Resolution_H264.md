## TestCase ID
NATIVE_PLAYBACK_109

## TestCase Name
NPVS_Play_480p_Resolution_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate 480p (854Ã—480) resolution playback via `test_generic_playback` function with H.264 video codec and AAC audio. Initialize playbin with qtdemux demuxing, query video sink properties via `westerossinkâ†’video-height` and `westerossinkâ†’video-width`. Verify resolution matches expected 854Ã—480 (Â±5 pixel tolerance). Execute 10-second playback monitoring position via `gst_element_query_position()`, validate frame rendering statistics via `westerossinkâ†’stats`. Confirm clean pipeline state transitions and error-free playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | MP4 H.264 AAC stream (`atfms_291_dash_tdk_avc_aac_fmp4_480p.mp4`) must be accessible via HTTPS (`souphttpsrc`) or local file system (`filesrc`) element with `qtdemux` capable of parsing MP4 container  | Verify MP4 stream is accessible and contains valid H.264 and AAC representations |
| 3 | Stream Variable Configuration | `video_src_url_mp4_480p` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4_480p.mp4"` | Verify `video_src_url_mp4_480p` resolves to valid MP4 location with correct codec support |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout configured for standard playback (10 seconds) | Verify timeout is set to required value in configuration file |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`; Establish Wayland display session via RDKWindowManager; Set up logging file | Verify environment loaded, Wayland display created |
| 2 | Configure Test with Resolution Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_mp4_480p`; Execute `mediapipelinetests test_generic_playback <URL> timeout=<seconds>` | Verify mediapipelinetests initializes with 480p stream |
| 3 | Construct H.264 Pipeline with Resolution Stream | Create `playbin` element; Configure `uri` to video_src_url_mp4_480p (MP4); Set `westerossink` as video sink; Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, MP4 parsed successfully |
| 4 | Query Video Dimensions and Validate Resolution | Query `westerossinkâ†’video-height` and `westerossinkâ†’video-width` via `g_object_get()`; Extract values (854Â±5 height, 480Â±5 width expected) | Verify video-height == 480Â±5 pixels; Verify video-width == 854Â±5 pixels |
| 5 | Play Stream and Monitor Position | Execute continuous playback for configured timeout (10 seconds); Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (Â±1 second), no stalls |
| 6 | Validate Frame Rendering at Resolution | Query `westerossinkâ†’stats` to verify `rendered_frames` increments consistently at 480p resolution; Verify `dropped_frames` < 1% of rendered_frames | Verify frame statistics indicate proper 480p rendering |
| 7 | Verify Audio-Video Synchronization | Query 
-audio` property to confirm audio stream; Verify audio and video remain synchronized throughout playback | Verify audio stream present; Verify A/V sync maintained |
| 8 | Monitor GStreamer Bus | Monitor message bus via `gst_bus_pop()` for errors or warnings; Verify clean decoding without format errors | Verify no decoder or format errors |
| 9 | Release Resources and Verify Success | Call `terminatePipeline(playbin)` to release all resources; Verify test output contains "Failures: 0" confirming 480p playback successful | Verify clean shutdown; Verify test passed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
