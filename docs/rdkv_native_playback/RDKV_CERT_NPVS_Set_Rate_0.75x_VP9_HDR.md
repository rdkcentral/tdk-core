## TestCase ID
RDKV_NATIVE_PLAYBACK_382

## TestCase Name
RDKV_CERT_NPVS_Set_Rate_0.75x_VP9_HDR

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Test to verify playback rate control at 0.75x speed function with VP9 HDR (High Dynamic Range) content in WebM container. Validate that position advances at exactly 0.75x speed (three-quarter normal speed) through periodic polling with position increment expected at +/-25% tolerance around 0.075 seconds per 100ms interval. Verify WebM container parsing and HDR metadata preservation during rate change, audio/video remain synchronized, and frame rendering continues without discontinuities.
## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration |  VP9 HDR (High Dynamic Range))<br>encoded WebM stream must be accessible via local file system (`filesrc`))<br>or HTTPS (`souphttpsrc`). Stream file path configured as `test_streams_base_path + "TDK_Asset_Waterfall_VP9_HDR.webm"` in MediaValidationVariables.py (VP9 HDR content in WebM container with HDR metadata for rate control validation))<br>Stream variable `video_src_url_vp9_hdr` configured in `MediaValidationVariables.py` with path: `TDK_Asset_Waterfall_VP9_HDR.webm` (stream must have VP9 codec in WebM container with HDR color space and metadata)  | Verify VP9 HDR WebM stream file is accessible, readable, HDR metadata present, and stream contains minimum 60 seconds of content Verify `video_src_url_vp9_hdr` resolves to valid, accessible VP9 HDR WebM file location with proper HDR metadata |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Initialize test environment by sourcing variables from `/opt/TDK/TDK.env` and establish Wayland display session<br>via RDKWindowManager | Verify environment variables load correctly and Wayland display is created |
| 2 | Configure and Execute Test Application | Retrieve configuration and stream URL, then execute `tdk_mediapipelinetests` with test case name, stream URL, and timeout arguments | Verify configuration is retrieved and `tdk_mediapipelinetests` initializes playbin pipeline |
| 3 | Construct Pipeline and Initiate Playback | Create `playbin` element with stream URI, set `westerossink` as video sink, trigger `NULLREADYPAUSEDPLAYING` state transition, verify `first-video-frame-callback` signal | Verify `playbin` reaches `GST_STATE_PLAYING` with first frame rendered, no `GST_MESSAGE_ERROR` |
| 4 | Execute Playback Rate Change | Invoke `gst_element_seek()` with playback rate set to 0.75 and GST_SEEK_FLAG_FLUSH flag<br> Verify position progression matches 0.75x speed (three-quarter normal speed) with maintained audio/video sync | Verify test operation completes successfully with expected results |
| 5 | Monitor Playback Progress | Poll `gst_element_query_position()` at 100ms intervals to verify position advances at 0.75x rate (expected increment: 0.075 seconds per 100ms +/-25% tolerance) | Verify position increments are consistent, no stalls or backward jumps detected |
| 6 | Validate Frame Rendering | Poll `g_object_get(westerossink, "stats")` to verify `rendered_frames` increments and `dropped_frames` remains acceptable | Verify frame statistics indicate proper video rendering |
| 7 | Validate Test Success Indicators | Parse GCheck framework output and verify test-specific metrics match expected values | Verify GCheck shows `Failures: 0`, `Errors: 0`, and metrics are correct |
| 8 | Release Pipeline Resources | Set pipeline state to `GST_STATE_NULL` and release all codec, decoder, and sink resources | Verify pipeline reaches `GST_STATE_NULL` and system restored to pre-test state |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 3 mins

**Priority:** High

**Release Version:** M121










