## TestCase ID
RDKV_NATIVE_PLAYBACK_206

## TestCase Name
RDKV_CERT_NPVS_CheckLatency_VP9

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Measure playback latency from pipeline PLAYING state to first frame rendering on westerossink video sink using VP9 video codec with WebM container format. Execute VP9 DASH stream through playbin and measure elapsed time when playback position reaches 1 second, validating that latency remains below configured threshold (default 100 milliseconds). Verify westerossink successfully renders VP9 frames within latency budget and logs measurement for VP9 codec compliance validation.

## Preconditions

| # | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary and all dependent libraries | Verify TDK_Package is installed, binary is executable, and all libraries are available |
| 2 | Stream Provisioning and Configuration | VP9/OPUS stream must be accessible via HTTP/HTTPS or filesrc, configured at `test_streams_base_path + "DASH_VP9_OPUS_WebM/master.mpd"` in MediaValidationVariables.py<br> Stream variable `video_src_url_vp9` must be configured with this path<br> (DASH MPD with WebM segments, 1080p, 5+ mins) | Verify DASH VP9/OPUS stream is accessible and parseable, `video_src_url_vp9` resolves to valid, accessible stream with valid segments |
| 3 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured with required timeout value (default: 10 seconds) in Video_Accelerator.config or RPI-Client.config | Verify timeout is set to required value in configuration file |
| 4 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists and contains all required environment variables |

## Test Steps

| # | Step Name | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment |  Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, library paths, and Wayland display configuration. Establish Wayland display session<br>via RDKWindowManager or westeros compositor. Set up logging file at `/opt/TDK/mediapipeline_test_step.log`. Retrieve `NATIVE_PLAYBACK_LATENCY_THRESHOLD` from device config (default: 100ms))<br>and `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` (default: 10 seconds)  | Verify environment variables load correctly, Wayland display created, latency threshold retrieved |
| 2 | Create Playbin and Configure VP9 DASH Stream | Create playbin element via `gst_element_factory_make("playbin", NULL)`<br> Set VP9 DASH stream URL from `MediaValidationVariables.video_src_url_vp9` as URI property<br> Set playback flags to enable video and audio via `GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO` ; Verify playbin element created successfully, VP9 DASH stream URL configured, flags set for A/V playback |
| 3 | Create westerossink and Register Callbacks |  Create westerossink element<br>via `gst_element_factory_make("westerossink", NULL)`. Connect westerossink as video-sink to playbin<br>via `g_object_set(playbin, "video-sink", westerossink, NULL)`. Register `first-video-frame-callback` signal on westerossink to capture frame rendered event  | Verify westerossink created successfully, connected as video sink, first-frame callback registered |
| 4 | Transition Pipeline to PLAYING State |  Start latency measurement by recording current time (start_latency = std::chrono::high_resolution_clock::now()). Set pipeline to PLAYING state<br>via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Poll `gst_element_get_state()` until GST_STATE_CHANGE_SUCCESS and pipeline reaches GST_STATE_PLAYING  | Verify pipeline successfully transitions to PLAYING state without GST_MESSAGE_ERROR, latency timer started |
| 5 | Poll Playback Position Until 1-Second Mark | Loop for maximum 3 seconds querying playback position via `gst_element_query_position(playbin, GST_FORMAT_TIME, &currentPosition)`<br> Check if position reaches 1 second (currentPosition/GST_SECOND >= 1)<br> Stop latency measurement when position reaches 1 second (stop_latency = now(), then subtract 1 second: stop_latency -= std::chrono::seconds(1)) | Verify position advances continuously, reaches 1-second mark within 3-second timeout, latency calculation time recorded |
| 6 | Calculate Latency in Milliseconds | Convert latency duration to milliseconds: `latency_ms = std::chrono::duration_cast<std::chrono::milliseconds>(stop_latency - start_latency).count()`<br> Extract integer milliseconds value from chrono duration object | Verify latency calculated as positive integer milliseconds value representing time from PLAYING state to 1-second playback position |
| 7 | Write Latency Measurement to Log File | Open latency log file at `{TDK_PATH}/latency_log`<br> Write latency value in format "Latency = {latency_ms} milliseconds\n" to file<br> Close file pointer<br> Also print to console: "Time measured: {latency_ms} milliseconds." | Verify file created/written successfully at configured path, latency value recorded with correct format |
| 8 | Validate Latency Against Threshold | Compare measured latency_ms with `latencyThreshold` (default: 100ms from config)<br> If latency_ms < latencyThreshold, test PASSES<br> If latency_ms >= latencyThreshold, test FAILS<br> Check first-video-frame callback was triggered (firstFrameReceived == true) | Verify latency comparison completed, pass/fail determination made, first-frame signal confirmed |
| 9 | Verify First Frame Signal Received | Assert that `firstFrameReceived == true` was set by westerossink callback during step 5<br> This confirms video actually rendered, not just position advanced | Verify first-video-frame-callback signal was received and `firstFrameReceived` flag is true |
| 10 | Release Pipeline and Cleanup Resources |  Set pipeline to NULL state<br>via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and westerossink objects<br>via `gst_object_unref()`. Close logging file. Verify all GStreamer resources freed  | Verify pipeline reaches NULL state cleanly, all objects unreferenced, no resource leaks, system ready for next test |

## Test Attributes

**Supported Models:** Video_Accelerator

**Estimated Duration:** 5 mins

**Priority:** High

**Release Version:** M121








