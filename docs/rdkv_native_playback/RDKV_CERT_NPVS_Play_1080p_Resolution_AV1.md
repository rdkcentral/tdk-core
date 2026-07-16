## TestCase ID
RDKV_NATIVE_PLAYBACK_106

## TestCase Name
RDKV_CERT_NPVS_Play_1080p_Resolution_AV1

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate 1080p (1920�1080) resolution playback function with AV1 video codec and AAC audio. Initialize playbin with qtdemux demuxing, query video sink properties and verify resolution matches expected 1920�1080 (+/-5 pixel tolerance). Execute 10-second playback monitoring position, validate frame rendering statistics. Confirm clean pipeline state transitions and error-free playback.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  MP4 AV1 AAC stream (`1080p.mp4`))<br>must be accessible via HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`))<br>element with `qtdemux` capable of parsing MP4 container `video_src_url_mp4_1080p_av1` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "Waterfall_DASH_AV1_AAC/1080p.mp4"`  | Verify MP4 stream is accessible and contains valid AV1 and AAC representations Verify `video_src_url_mp4_1080p_av1` resolves to valid MP4 location with correct codec support |
|  3  |  Playback Timeout Configuration  |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config  | Verify timeout configured for standard playback (10 seconds); Verify timeout configured for standard playback (10 seconds); Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`;<br>Establish Wayland display session via RDKWindowManager;<br>Set up logging file | Verify environment loaded, Wayland display created |
| 2 | Configure Test with Resolution Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_mp4_1080p_av1`;<br>Execute `mediapipelinetests test_generic_playback <URL> timeout=<seconds>` | Verify mediapipelinetests initializes with 1080p stream |
| 3 | Construct AV1 Pipeline with Resolution Stream | Create `playbin` element; Configure `uri` to video_src_url_mp4_1080p_av1 (MP4); Set `westerossink` as video sink;<br>Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, MP4 parsed successfully |
| 4 | Query Video Dimensions and Validate Resolution | Query `westerossink→video-height` and `westerossink→video-width` via `g_object_get()`;<br>Extract values (1920+/-5 height, 1080+/-5 width expected) | Verify video-height == 1080+/-5 pixels; Verify video-width == 1920+/-5 pixels |
| 5 | Play Stream and Monitor Position | Execute continuous playback for configured timeout (10 seconds);<br>Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (+/-1 second), no stalls |
| 6 | Validate Frame Rendering at Resolution | Query `westerossink→stats` to verify `rendered_frames` increments consistently at 1080p resolution;<br>Verify `dropped_frames` < 1% of rendered_frames | Verify frame statistics indicate proper 1080p rendering |
| 7 | Monitor GStreamer Bus | Monitor message bus via `gst_bus_pop()` for errors or warnings; Verify clean decoding without format errors | Verify no decoder or format errors |
| 8 | Release Resources and Verify Success | Call `terminatePipeline(playbin)` to release all resources;<br>Verify test output contains "Failures: 0" confirming 4K playback successful | Verify clean shutdown; Verify test passed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121












