## TestCase ID
RDKV_NATIVE_PLAYBACK_373

## TestCase Name
RDKV_CERT_NPVS_Play_VP9_HDR

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate HDR VP9 video codec playback with WebM OPUS stream. Initialize playbin with HDR-capable configuration, parse HDR metadata from stream via WebM container. Query video dimensions via westerossink 'video-height' and 'video-width' properties, verify HDR properties preserved. Execute 10-second playback with continuous position polling. Monitor frame rendering statistics confirming proper HDR tone mapping and color space handling.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  WebM VP9 OPUS stream (`TDK_Asset_Sunrise_VP9_HDR.webm`))<br>must be accessible via HTTPS (`souphttpsrc`))<br>or local file system (`filesrc`))<br>element with `matroskademux` capable of parsing WebM container `video_src_url_vp9_hdr` must be configured in `MediaValidationVariables.py` as `test_streams_base_path + "TDK_Asset_Sunrise_VP9_HDR.webm"`  | Verify WebM stream is accessible and contains valid VP9 and OPUS representations Verify `video_src_url_vp9_hdr` resolves to valid WebM location with correct codec support |
|  3  |  Playback Timeout Configuration  |  `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config  | Verify timeout configured for standard playback (10 seconds); Verify timeout configured for standard playback (10 seconds); Verify `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` is set to 10 seconds in configuration file; Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`;<br>Establish Wayland display session with HDR-capable display configuration | Verify environment loaded, HDR display initialized |
| 2 | Configure HDR Playback | Retrieve stream URL from `video_src_url_vp9_hdr`; Configure playbin with HDR-capable sink parameters;<br>Execute `mediapipelinetests test_generic_playback <URL>` | Verify HDR stream loaded with proper configuration |
| 3 | Construct HDR VP9 Pipeline | Create `playbin` element; Configure `uri` to video_src_url_vp9_hdr (WebM); Set `westerossink` with HDR tone mapping enabled;<br>Transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING` with HDR settings |
| 4 | Query HDR Metadata and Video Properties | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` to confirm resolution;<br>Query HDR-specific properties from video pad caps | Verify video dimensions valid; Verify HDR metadata present |
| 5 | Play HDR Stream and Monitor Position | Execute continuous playback for 10 seconds; Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (+/-1 second) |
| 6 | Validate HDR Rendering | Query `g_object_get(westerossink, "stats")` for frame rendering statistics; Verify proper HDR tone mapping applied to rendered frames | Verify `rendered_frames` increment; Verify HDR applied |
| 7 | Verify Color Space and Tone Mapping | Monitor HDR color space handling and tone mapping process; Verify no color clipping or metadata loss during playback | Verify HDR integrity throughout playback |
| 8 | Monitor Bus and Release Resources | Monitor message bus for errors; Release pipeline resources via `terminatePipeline(playbin)` | Verify no errors; Verify clean shutdown |
| 9 | Confirm HDR Test Success | Verify test output confirms HDR playback successful with proper tone mapping | Verify test passed with "Failures: 0" |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121










