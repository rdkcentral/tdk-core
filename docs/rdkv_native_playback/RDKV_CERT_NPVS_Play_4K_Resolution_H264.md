## TestCase ID
RDKV_NATIVE_PLAYBACK_111

## TestCase Name
RDKV_CERT_NPVS_Play_4K_Resolution_H264

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate 4K (3840�2160) resolution playback function with H.264 video codec and AAC audio. Initialize playbin with qtdemux demuxing, query video sink properties and verify resolution matches expected 3840�2160 (+/-5 pixel tolerance). Execute 10-second playback monitoring position, validate frame rendering statistics. Confirm clean pipeline state transitions and error-free playback.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  MP4 H.264 AAC stream (`TDK_Asset_Sunrise_2160p.mp4`))<br>must be accessible via HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`))<br>element with `qtdemux` capable of parsing MP4 container `video_src_url_mp4_2160p` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_2160p.mp4"`  | Verify MP4 stream is accessible and contains valid H.264 and AAC representations Verify `video_src_url_mp4_2160p` resolves to valid MP4 location with correct codec support |
|  3  |  Playback Timeout Configuration  |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config  | Verify timeout configured for standard playback (10 seconds); Verify timeout configured for standard playback (10 seconds); Verify timeout is set to required value (minimum 10 seconds for 4K validation) |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`;<br>Establish Wayland display session via RDKWindowManager;<br>Set up logging file | Verify environment loaded, Wayland display created |
| 2 | Configure Test with Resolution Stream | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` and stream URL from `video_src_url_mp4_2160p`;<br>Execute `mediapipelinetests test_generic_playback <URL> timeout=<seconds>` | Verify mediapipelinetests initializes with 4K stream |
| 3 | Construct H.264 Pipeline with Resolution Stream | Create `playbin` element; Configure `uri` to video_src_url_mp4_2160p (MP4); Set `westerossink` as video sink;<br>Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, MP4 parsed successfully |
| 4 | Query Video Dimensions and Validate Resolution | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` via `g_object_get()`;<br>Extract values (3840+/-5 height, 2160+/-5 width expected) | Verify video-height == 2160+/-5 pixels; Verify video-width == 3840+/-5 pixels |
| 5 | Play Stream and Monitor Position | Execute continuous playback for configured timeout (10 seconds);<br>Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (+/-1 second), no stalls |
| 6 | Validate Frame Rendering at Resolution | Query `g_object_get(westerossink, "stats")` to verify `rendered_frames` increments consistently at 4K resolution;<br>Verify `dropped_frames` < 1% of rendered_frames | Verify frame statistics indicate proper 4K rendering |
| 7 | Monitor GStreamer Bus | Monitor message bus via `gst_bus_pop()` for errors or warnings; Verify clean decoding without format errors | Verify no decoder or format errors |
| 8 | Release Resources and Verify Success | Call `terminatePipeline(playbin)` to release all resources;<br>Verify test output contains "Failures: 0" confirming 4K playback successful | Verify clean shutdown; Verify test passed |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121













