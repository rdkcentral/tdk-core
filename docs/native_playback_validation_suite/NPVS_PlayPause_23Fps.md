## TestCase ID
NATIVE_PLAYBACK_20

## TestCase Name
NPVS_PlayPause_23Fps

## Table of Contents

- [Objective](#objective)
- [Preconditions](#preconditions)
- [Test Steps](#test-steps)
- [Test Attributes](#test-attributes)

## Objective
Validate play-pause-resume state transitions during MP4 H.264/AAC playback via `playbin` element with westerossink video sink and audio sink. Test creates `playbin` with `gst_element_factory_make()`, configures stream via `g_object_set(playbin, "uri", <stream>, NULL)`, transitions pipeline between `GST_STATE_PLAYING` and `GST_STATE_PAUSED` states via `gst_element_set_state()`, and validates position remains stationary during pause via `gst_element_query_position()` with 0ms drift tolerance while verifying position advances 1x rate during play via Â±100ms tolerance. Confirm frame rendering statistics from westerossink via `stats` property show rendered_frames increment ONLY during PLAYING state and remain static during PAUSED state, no GST_MESSAGE_ERROR on bus, and "Failures: 0" output for all state transitions.

## Preconditions

| ID | Step Name | Step Description | Expected Result |
|----|-----------|------------------|-----------------|  
| 1 | TDK Package Installation | TDK_Package must be installed on the Device Under Test (DUT) with `tdk_mediapipelinetests` binary, GStreamer plugins (qtdemux demuxer, necessary decoders), and westerossink element | Verify TDK_Package is installed, binary is executable, qtdemux element available in GStreamer |
| 2 | Media Stream Provisioning | MP4 H.264/AAC stream must be accessible via local file system or HTTP streaming. Stream file path configured in MediaValidationVariables.py as `test_streams_base_path + "TDK_Asset_Sunrise_23fps.mp4"` | Verify stream file is accessible with valid Video: H.264, Audio: AAC, qtdemux element for MP4 parsing |
| 3 | Stream Variable Configuration | Stream variable `video_src_url_mp4_23fps` configured in `MediaValidationVariables.py` with path: `test_streams_base_path + "TDK_Asset_Sunrise_23fps.mp4"` | Verify `video_src_url_mp4_23fps` resolves to valid, accessible stream location |
| 4 | Playback Timeout Configuration | `NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT` must be configured (default: 10 seconds) in device config to allow complete play-pause cycles | Verify timeout configured for minimum 3 play-pause cycles (minimum 30 seconds per cycle = 90 seconds total) |
| 5 | Platform-Specific Environment Variables | Platform-specific environment variables (`WAYLAND_DISPLAY`, `XDG_RUNTIME_DIR`, `LD_PRELOAD` with vendor libraries, `GST_PLUGIN_PATH`) must be defined in `/opt/TDK/TDK.env` | Verify `/opt/TDK/TDK.env` exists with all required variables, westerossink available, Wayland display active |

## Test Steps

| ID | StepName | Step Description | Expected Result |
|----|----------|------------------|-----------------|  
| 1 | Initialize Test Environment | Source environment variables from `/opt/TDK/TDK.env` to load GStreamer plugins, qtdemux demuxer, decoders, westerossink, and Wayland display configuration. Establish Wayland display session via RDKWindowManager. Set up logging file at `/opt/TDK/mediapipeline_test_step.log` | Verify all environment variables load correctly, Wayland display session created successfully, logging initialized without errors |
| 2 | Configure Test Framework and Load Stream | Set test name to `test_play_pause_pipeline`, Load MP4 H.264/AAC stream via `video_src_url_mp4_23fps` variable from MediaValidationVariables.py. Set timeout to NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT | Verify test case name configured, stream URI resolved correctly, timeout set for minimum 3 play-pause cycles |
| 3 | Create Playbin Pipeline and Configure Sinks | Create `playbin` element via `gst_element_factory_make("playbin", NULL)`. Set `uri` property to stream URL via `g_object_set(playbin, "uri", stream_url, NULL)`. Set video-sink to `westerossink` and audio-sink to `autoaudiosink` via `g_object_set(playbin, "video-sink", westerossink, NULL)` | Verify playbin element created successfully, URI property set to stream, sinks properly configured |
| 4 | Transition Pipeline to PLAYING State | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Monitor `GST_MESSAGE_STREAM_START` on GStreamer bus via `gst_bus_pop_filtered()`. Wait for state change completion via `gst_element_get_state()` polling until `GST_STATE_CHANGE_SUCCESS` | Verify pipeline transitions to PLAYING state without errors, qtdemux active, first frame rendered via westerossink callback |
| 5 | Validate Initial Playback Position and Frame Rendering | Execute position query via `gst_element_query_position(playbin, GST_FORMAT_TIME, &position)` to establish baseline. Query westerossink `stats` property via `g_object_get()` to retrieve rendered_frames and dropped_frames counters. Verify rendered_frames > 0 | Verify initial position obtained within stream bounds, rendered_frames counter increments during PLAYING state, dropped_frames < 1% of rendered_frames |
| 6 | Transition Pipeline to PAUSED State | Set pipeline state to `GST_STATE_PAUSED` via `gst_element_set_state(playbin, GST_STATE_PAUSED)`. Monitor state change completion via `gst_element_get_state()` polling. Query position via `gst_element_query_position()` to capture pause position | Verify pipeline transitions to PAUSED state without errors, state change completes successfully |
| 7 | Validate Position Halt During PAUSED State | Poll `gst_element_query_position()` at 100ms intervals for minimum 1 second during PAUSED state. Verify position remains constant (Â±0 movement, 0ms drift tolerance). Query westerossink `stats` property to verify rendered_frames counter remains static (no increment) | Verify position does NOT advance during PAUSED state with Â±0 tolerance, rendered_frames counter unchanged, video rendering halted |
| 8 | Transition Pipeline Back to PLAYING State | Set pipeline state to `GST_STATE_PLAYING` via `gst_element_set_state(playbin, GST_STATE_PLAYING)`. Monitor state change completion via `gst_element_get_state()` polling until `GST_STATE_CHANGE_SUCCESS` | Verify pipeline successfully resumes to PLAYING state without errors, state change completes synchronously |
| 9 | Validate Resumed Playback Position Advancement and Frame Rendering | Execute position query via `gst_element_query_position()` at 100ms intervals for NATIVE_PLAYBACK_MEDIAPLAYBACK_TIMEOUT seconds. Verify position advances at 1x rate (1 second per 1 second real-time Â±100ms tolerance) with no backward jumps. Query westerossink `stats` property to verify rendered_frames counter resumes incrementing at expected rate. Verify no GST_MESSAGE_ERROR on bus | Verify position advances smoothly at 1x rate with Â±100ms tolerance, rendered_frames counter increments, no errors detected |
| 10 | Repeat Play-Pause Cycles Minimum 3 Times | Repeat steps 6-9 (PAUSED -> PLAYING transitions) minimum 3 times total for comprehensive state transition validation. Each cycle must complete without errors or timeouts | Verify all 3+ play-pause cycles complete successfully with consistent behavior, no performance degradation across cycles |
| 11 | Release Pipeline and Verify Test Success | Set pipeline state to `GST_STATE_NULL` via `gst_element_set_state(playbin, GST_STATE_NULL)`. Unreference playbin and westerossink elements via `gst_object_unref()`. Free allocated memory and close logging file. Verify test framework output shows "Failures: 0" and "Errors: 0" | Verify pipeline reaches `GST_STATE_NULL`, all GStreamer resources released without segmentation faults, test reports zero failures and errors for all play-pause cycles |

## Test Attributes

**Supported Models:** Video_Accelerator, RPI-CLIENT

**Estimated Duration:** 2-3 minutes

**Priority:** High

**Release Version:** M121
