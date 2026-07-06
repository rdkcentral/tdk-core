
## TestCase ID
NATIVE_PLAYBACK_35

## TestCase Name
NPVS_FastForward_2x_H264
## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate fast-forward playback at 2.0x rate via `gst_element_seek()` on supported stream. Verify playback rate acceleration through `gst_query_segment()` to retrieve current playback rate and compare against requested 2.0x rate. Test confirms position advancement at double-speed and pipeline stability during accelerated playback.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Media Stream Provisioning | DASH stream with MPD manifest must be accessible via HTTPS or local file system (`filesrc`). Stream file configured as `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` in MediaValidationVariables.py. Stream contains H.264 video and AAC audio (DASH container format for fast-forward testing) | Verify master.mpd manifest file is accessible and readable from configured path, dashdemux plugin available for MPD parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_aac` must be configured in `MediaValidationVariables.py` with value: `test_streams_base_path + "DASH_H264_AAC/atfms_291_dash_tdk_avc_aac_fmp4.mpd"` | Verify `video_src_url_aac` resolves to valid DASH manifest URL, manifest contains valid MPD structure with Period, AdaptationSet, Representation elements |
| 4 | Playback Rate and Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` configuration must be set in device configuration file (default: 10 seconds if not configured). For fast-forward testing, timeout should be minimum 20 seconds to allow stream playback at 2.0x rate. | Verify timeout is set appropriately |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor H.264/AAC decoder libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` for GStreamer plugin and codec access | Verify `/opt/TDK/TDK.env` exists with all required variables, H.264 and AAC hardware decoder plugins loaded via GST_PLUGIN_PATH, Wayland display available |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment and Setup Pipeline | Source environment variables from `/opt/TDK/TDK.env` for GStreamer plugin paths and codec libraries. Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set DASH stream URI via `g_object_set(playbin, "uri", manifest_URL)`. Attach `westerossink` as video sink via `g_object_set(playbin, "video-sink", westerossink)`. Register `first-video-frame-callback` signal on westerossink to detect when rendering begins. Transition pipeline to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)` and wait for callback | Verify playbin element created, stream URI set to DASH manifest, westerossink configured as video sink, pipeline transitions to PLAYING state, first-video-frame-callback received, video rendering starts without errors |
| 2 | Optionally Check AV Status | If device configurationis set to "yes", verify video playback status via SOC-level video decoder check (proc entry inspection for rendering statistics). This step is performed only if `checkAVStatus` flag is enabled | Verify AV status check completes successfully if enabled, video decoder reports active playback |
| 3 | Initiate Fast-Forward Seek Operation | Invoke `gst_element_seek()` to set playback rate to 2.0x. Parameters specify rate=2.0, format=GST_FORMAT_TIME, flush buffers via GST_SEEK_FLAG_FLUSH, start from currentPosition, and play to stream end (GST_CLOCK_TIME_NONE). This initiates double-speed playback from the current stream position | Verify `gst_element_seek()` returns TRUE indicating rate change accepted, pipeline begins accelerated playback without errors |
| 4 | Poll Bus for State Change Notification | Retrieve GStreamer pipeline bus via `gst_element_get_bus(playbin)`. Poll bus using `gst_bus_pop_filtered()` to monitor pipeline messages including STATE_CHANGED, ASYNC_DONE, ERROR, and EOS. Continue polling until rate change completes or RATE_SET_TIMEOUT expires | Verify bus retrieved successfully, STATE_CHANGED or ASYNC_DONE message received indicating rate change processed, no ERROR messages detected |
| 5 | Query and Validate Current Playback Rate | Upon state change notification, create and execute segment query via `gst_query_new_segment()` and `gst_element_query()` to retrieve current playback rate. Parse query via `gst_query_parse_segment()` to extract currentRate value. Verify currentRate equals 2.0, confirming rate change was successfully applied | Verify `gst_element_query()` succeeds, extracted currentRate equals 2.0 confirming double-speed playback activated |
| 6 | Monitor Position Advancement During Fast-Forward | Poll `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` at 100ms intervals during fast-forward playback. Verify position advances at 2x rate: elapsed time of 1 second should show position advancement of ~2 seconds. Continue monitoring for full test duration via `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` parameter | Verify position increments at 2x multiplier consistently, no stalls or backward jumps detected, frame rendering continues at accelerated rate |
| 7 | Verify Test Success Indicators | Validate test framework output for success strings: "Failures: 0", "Errors: 0", or "failed: 0". Confirm mediapipelinetests application execution completed without errors related to seek operation or rate change. Verify no GST_MESSAGE_ERROR on bus during acceleration | Verify test output contains required success indicators, no playback errors or codec errors reported during fast-forward operation |
| 8 | Terminate Pipeline and Release Resources | Stop playback by setting pipeline to `GST_STATE_NULL` via `gst_element_set_state()`. Release all GStreamer object references via `gst_object_unref()` for bus, query, and playbin. Close logging files and free dynamically allocated memory. Return pipeline to pre-test state | Verify pipeline reaches GST_STATE_NULL, all resources released without memory leaks, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 3 minutes

**Priority:** High

**Release Version:** M121
