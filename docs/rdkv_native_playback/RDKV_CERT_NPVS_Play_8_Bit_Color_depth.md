## TestCase ID
RDKV_NATIVE_PLAYBACK_133

## TestCase Name
RDKV_CERT_NPVS_Play_8_Bit_Color_depth

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate 8-bit color depth rendering with H.264 stream. Query video decoder hardware interface to extract source bit depth information via /proc/brcm/video_decoder (Broadcom), /lib/rdk/get_avstatus.sh (RTK), or GStreamer pad capabilities. Verify decoder reports 8-bit color depth and execute DASH playback with continuous position monitoring. Confirm color depth metadata preserved throughout 10-second playback window without errors.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  8-bit H.264 DASH stream with AAC audio must be accessible via HTTP(S) (`souphttpsrc`))<br>or local file system (`filesrc`). Stream configured as `video_src_url_aac` in MediaValidationVariables.py pointing to `DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd` (DASH manifest with H.264 8-bit color depth video))<br>Stream variable `video_src_url_aac` configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` pointing to 8-bit H.264 DASH stream  | Verify DASH stream is accessible and dashdemux can parse MPD manifest Verify `video_src_url_aac` resolves to valid, accessible DASH MPD manifest with 8-bit H.264 video |
| 3 | Bit Depth Configuration and Timeout | `bit_depth` parameter must be set to "8" in test execution to specify expected color depth<br> `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config for playback validation window | Verify bit_depth parameter set to 8; Verify timeout configured (minimum 10 seconds) |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env`;<br>Establish Wayland display session;<br>Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify environment loaded, Wayland display created |
| 2 | Configure Test with Bit Depth Parameter | Retrieve `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT`, and bit depth target (8);<br>Execute `mediapipelinetests test_color_depth <URL> bit_depth=8 timeout=<seconds>` | Verify mediapipelinetests initializes with 8-bit parameter |
| 3 | Construct H.264 DASH Pipeline | Create `playbin` element; Configure `uri` property to video_src_url_aac (DASH manifest/file); Set `westerossink` as video sink;<br>Trigger state transition to `GST_STATE_PLAYING` | Verify playbin reaches `GST_STATE_PLAYING`, DASH demuxer active |
| 4 | Execute Playback and Position Monitoring | Play stream for configured timeout (10 seconds);<br>Monitor position via `gst_element_query_position()` at 100ms intervals | Verify position advances at 1x rate (+/-1 second tolerance) |
|  5  |  Query Video Decoder Bit Depth  |  Execute platform-specific command: `sh /lib/rdk/get_avstatus.sh  | grep LumaBitDepth` to extract color depth; Parse output to extract 8-bit value via `atoi()` conversion; grep LumaBitDepth` to extract color depth; Parse output to extract 8-bit value via `atoi()` conversion; Verify 8-bit value successfully extracted from decoder |
| 6 | Validate Bit Depth Matches Expected | Compare retrieved bit depth against 8 parameter using assertion: `assert_failure(playbin, (expected==8), "Bit depth mismatch")`;<br>Log comparison result | Verify assertion passes; Verify Bit Depth == 8 |
| 7 | Query Video Dimensions and Frame Statistics | Query `g_object_get(westerossink, "video-height")` and `g_object_get(westerossink, "video-width")` to confirm resolution;<br>Query `g_object_get(westerossink, "stats")` for `rendered_frames` and `dropped_frames` | Verify dimensions valid; Verify frames rendered properly |
| 8 | Monitor Bus and Release Resources | Monitor GStreamer bus for errors;<br>Call `terminatePipeline(playbin)` to release resources;<br>Verify no errors or warnings detected | Verify clean shutdown; Verify test output shows "Failures: 0" |
| 9 | Verify Test Result | Parse test output and confirm color depth validation passed and all assertions successful | Verify color depth validation complete, no failures |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121












